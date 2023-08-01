import re
import copy
from urllib.parse import unquote_plus
from intervals import DecimalInterval
import sqlalchemy
from flask import (
    Flask,
    render_template,
    request
)
from greenworld.lib import orm
from greenworld.lib import Greenworld
app = Flask(
    'Greenworld',
    template_folder = 'server/templates',
    static_folder = 'server/static'
)
Greenworld()
db = orm.init_db()

# Helpful values
plant_field_labels = {
    'id': 'Greenworld ID',
    'family': 'Family',
    'growth_habit': 'Growth Habit',
    'fruit_weight': 'Fruit Weight',
    'height': 'Height',
    'spread': 'Spread',
    'length': 'Length',
    'root_spread': 'Root Spread',
    'root_depth': 'Root Depth',
    'nitrogen': 'Nitrogen',
    'temperature': 'Temperature',
    'sun': 'Sun',
    'soil': 'Soil Type',
    'pH': 'pH',
    'drainage': 'Soil Drainage'
}

plant_field_units = {
    'family': '',
    'fruit_weight': 'g',
    'height': 'm',
    'spread': 'm',
    'length': 'm',
    'root_spread': 'm',
    'root_depth': 'm',
    'temperature': '° C',
    'pH': ''
}

plant_enum_values = {
    'growth_habit': ['Forb', 'Graminoid', 'Lichenous', 'Nonvascular', 'Shrub', 'Subshrub', 'Tree', 'Vine'],
    'nitrogen': ['Nitrogen fixer', 'Standard feeder', 'Heavy feeder'],
    'sun': ['Full shade', 'Partial sun', 'Full sun'],
    'soil': ['Sand', 'Clay', 'Silt', 'Loam'],
    'drainage': [
        'Very poorly drained',
        'Poorly drained',
        'Somewhat poorly drained',
        'Moderately well drained',
        'Well drained',
        'Somewhat excessively drained',
        'Excessively drained'
    ]
}

ecology_values = [
    'Negative allelopathic effect',
    'Positive allelopathic effect',
    'No allelopathic effect',
    'Pathogen',
    'Predator',
    'Seed disperser',
    'Pollinator'
]

# Internal transformation functions
def process_plant_dict(con, plant):
    if 'citations' in plant:
        ids = list(plant['citations'].keys())
        stmt = orm.works_cited_table.select().where(orm.works_cited_table.c.id.in_(ids))
        plant['citations'] = cite_fields(plant['citations'], list(con.execute(stmt).fetchall()))
    plant_id = plant['id'] if 'id' in plant else 0
    plant = transform_plant(plant)
    plant['ecology'] = grab_ecology_data(con, plant_id)
    return plant

def transform_plant(plant):
    fields = []
    for k, label in plant_field_labels.items():
        if plant[k] is None:
            value = '-'
        elif isinstance(plant[k], DecimalInterval):
            value = f'{plant[k].lower}{plant_field_units[k]} - {plant[k].upper}{plant_field_units[k]}'
        else:
            if k in ['id', 'family']:
                value = str(plant[k])
            else:
                value = plant_enum_values[k][plant[k]]
        field = '<td><b>' + label + '</b></td><td>' + value + '</td>'
        del plant[k]
        if k in plant['citations']:
            citation = plant['citations'][k]
            citation_text = citation_regex(citation)
            field += f'<td><a href="{citation}">{citation_text}</a></td>'
        fields.append(field)
    plant['fields'] = fields
    return plant

def grab_ecology_data(con, plant_id):
    ecology = []

    # Aggregate non-plant ecological interactions
    stmt = sqlalchemy.select(
        orm.other_species_table.c.name,
        orm.other_species_table.c.species,
        orm.ecology_other_table.c.relationship,
        orm.works_cited_table.c.citation
    ) \
    .join(orm.other_species_table, orm.other_species_table.c.id == orm.ecology_other_table.c.non_plant) \
    .join(orm.works_cited_table, orm.works_cited_table.c.id == orm.ecology_other_table.c.citation) \
    .where(orm.ecology_other_table.c.plant == plant_id)
    for row in con.execute(stmt).mappings():
        row = dict(row)
        row['relationship'] = ecology_values[row['relationship']]
        ecology.append(row)

    # Aggregate plant ecological interactions
    stmt = sqlalchemy.select(
        orm.plants_table.c.name,
        orm.plants_table.c.species,
        orm.ecology_plant_table.c.relationship,
        orm.works_cited_table.c.citation
    ) \
    .join(orm.plants_table, orm.plants_table.c.id == orm.ecology_plant_table.c.target) \
    .join(orm.works_cited_table, orm.works_cited_table.c.id == orm.ecology_plant_table.c.citation) \
    .where(orm.ecology_plant_table.c.plant == plant_id)
    for row in con.execute(stmt).mappings():
        row = dict(row)
        row['relationship'] = ecology_values[row['relationship']]
        ecology.append(row)
    return ecology

def cite_fields(citations, works_cited):
    new_citations = {}
    for k, v in citations.items():
        citation_link = next(x[1] for x in works_cited if str(x[0]) == k)
        for field in v:
            new_citations[field] = citation_link
    return new_citations

# Custom filters
@app.template_filter()
def citation_regex(href):
    return re.search(r'(?:[a-z]+://)(?:www\.)?([\w\d]+(\.[\w\d]+)*)/?', href).groups()[0]

# API endpoints
@app.route('/search/<prefix>')
def plant_search_endpoint(prefix):
    prefix = unquote_plus(prefix)
    if len(prefix) < 3:
        return []
    with db.connect() as con:
        stmt = sqlalchemy.select(
            orm.plants_table.c.id,
            orm.plants_table.c.species,
            orm.plants_table.c.name) \
        .where(sqlalchemy.or_(
            orm.plants_table.c.species.like(f'{prefix}%'),
            orm.plants_table.c.name.like(f'{prefix}%')
        )) \
        .limit(10)
        return list(map(dict, con.execute(stmt).mappings().fetchall()))

@app.route('/reports')
def grab_reports_endpoint():
    if 'species_list' not in request.args:
        return []
    species_list = request.args.get('species_list').split(',')
    stmt = orm.reports_table.select() \
    .where(sqlalchemy.or_(
        orm.reports_table.c.plant1.in_(species_list),
        orm.reports_table.c.plant2.in_(species_list)
    ))
    with db.connect() as con:
        return list(map(dict, con.execute(stmt).mappings().fetchall()))

@app.route('/neighbors/<int:id>/<float:thresh>')
def grab_neighbors_endpoint(id, thresh):
    stmt = orm.reports_table.select().where(sqlalchemy.and_(
        sqlalchemy.or_(
            orm.reports_table.c.plant1 == id,
            orm.reports_table.c.plant2 == id,
        ),
        orm.reports_table.c.range_union_min <= thresh
    ))
    def postprocess(x):
        x = dict(x)
        return x['plant1'] if x['plant2'] == id else x['plant2']
    with db.connect() as con:
        return list(map(postprocess, con.execute(stmt).mappings().fetchall()))

@app.route('/handlers')
def grab_handlers_endpoint():
    if 'ids' not in request.args:
        return []
    ids = request.args.get('ids').split(',')
    stmt = sqlalchemy.select(
        orm.plants_table.c.id,
        orm.plants_table.c.species,
        orm.plants_table.c.name
    ).where(orm.plants_table.c.id.in_(ids))
    with db.connect() as con:
        return list(map(dict, con.execute(stmt).mappings().fetchall()))

# HTML template endpoints
@app.route('/')
def homepage_endpoint():
    plant_stmt = sqlalchemy.select(sqlalchemy.func.count()).select_from(orm.plants_table)
    report_stmt = sqlalchemy.select(sqlalchemy.func.count()).select_from(orm.reports_table)
    with db.connect() as con:
        num_plants = con.execute(plant_stmt).fetchone()[0]
        num_reports = con.execute(report_stmt).fetchone()[0]
    return render_template('homepage.html', num_plants = num_plants, num_reports = num_reports)

@app.route('/plant/<species>')
def plant_view_endpoint(species):
    species = unquote_plus(species)
    with db.connect() as con:
        stmt = orm.plants_table.select().where(orm.plants_table.c.species == species)
        plant = con.execute(stmt).mappings().fetchone()
        if plant:
            plant = process_plant_dict(con, dict(plant))
            return render_template('plant.html', plant = plant)
    return render_template('404.html'), 404

@app.route('/report/<species1>/<species2>')
def report_view_endpoint(species1, species2):
    species1 = unquote_plus(species1)
    species2 = unquote_plus(species2)
    with db.connect() as con:
        stmt = orm.plants_table.select().where(orm.plants_table.c.species.in_([species1, species2]))
        plants = list(map(dict, con.execute(stmt).mappings().fetchall()))
        if len(plants) != 2:
            if species1 == species2:
                plants.append(copy.deepcopy(plants[0]))
            else:
                return render_template('404.html'), 404
        if plants[1]['id'] < plants[0]['id']:
            plants = [plants[1], plants[0]]
        stmt = orm.reports_table.select().where(orm.reports_table.c.plant1 == plants[0]['id']).where(orm.reports_table.c.plant2 == plants[1]['id'])
        report = dict(con.execute(stmt).mappings().fetchone())
        if not report:
            return render_template('404.html'), 404
        for i, plant in enumerate(plants):
            plants[i] = process_plant_dict(con, plant)
        return render_template(
            'report.html',
            report = report,
            plant1 = plants[0],
            plant2 = plants[1],
            MAX_PLANTING_RANGE = orm.MAX_PLANTING_RANGE
        )

@app.route('/placement')
def guild_placement_endpoint():
    return render_template('placement.html')

@app.route('/finder')
def guild_finder_endpoint():
    return render_template('finder.html')

@app.errorhandler(404)
def not_found_endpoint(_):
    return render_template('404.html')

# Main script
if __name__ == '__main__':
    # TODO this function is not intended for production use, please rewrite before launch
    # https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask.run
    app.run(host = '0.0.0.0', port = 2017)
