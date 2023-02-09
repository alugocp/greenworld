import os
import sys
from urllib.parse import unquote_plus
from intervals import DecimalInterval
from flask import (
    Flask,
    render_template
)
sys.path.append('.')
from greenworld import schema
app = Flask(
    'Greenworld',
    template_folder = 'server/templates'
)
os.environ['GREENWORLD_DB'] = 'sqlite:///greenworld.db'
db = schema.init_db()

# Helpful values
plant_field_labels = {
    'id': 'Internal ID',
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

# Internal transformation functions
def transform_plant(plant):
    fields = []
    for k, label in plant_field_labels.items():
        if plant[k] is None:
            value = '-'
        elif isinstance(plant[k], DecimalInterval):
            value = f'{plant[k].lower}{plant_field_units[k]} - {plant[k].upper}{plant_field_units[k]}'
        else:
            if k == 'id':
                value = str(plant[k])
            else:
                value = plant_enum_values[k][plant[k]]
        field = '<b>' + label + ':</b> ' + value
        del plant[k]
        if k in plant['citations']:
            citation = plant['citations'][k]
            field += f' <sup><a href="{citation}">citation</a></sup>'
        fields.append(field)
    plant['fields'] = fields
    return plant

def cite_fields(citations, works_cited):
    new_citations = {}
    for k, v in citations.items():
        citation_link = next(x[1] for x in works_cited if str(x[0]) == k)
        for field in v:
            new_citations[field] = citation_link
    return new_citations

# Endpoints
@app.route('/')
def homepage_endpoint():
    return render_template('homepage.html')

@app.route('/plant/<species>')
def plant_view_endpoint(species):
    species = unquote_plus(species)
    with db.connect() as con:
        stmt = schema.plants_table.select().where(schema.plants_table.c.species == species)
        plant = con.execute(stmt).mappings().fetchone()
        plant = dict(plant) if plant else {}
        if 'citations' in plant:
            ids = list(plant['citations'].keys())
            stmt = schema.works_cited_table.select().where(schema.works_cited_table.c.id.in_(ids))
            plant['citations'] = cite_fields(plant['citations'], list(con.execute(stmt).fetchall()))
    if len(plant.keys()) > 0:
        return render_template('plant.html', plant = transform_plant(plant))
    return f'Plant \'{species}\' not found', 404

@app.route('/report/<species1>/<species2>')
def report_view_endpoint(species1, species2):
    species1 = unquote_plus(species1)
    species2 = unquote_plus(species2)
    error_404 = f'No report for plants \'{species1}\' and \'{species2}\''
    with db.connect() as con:
        stmt = schema.plants_table.select().where(schema.plants_table.c.species.in_([species1, species2]))
        plants = list(con.execute(stmt).mappings().fetchall())
        if len(plants) != 2:
            return error_404, 404
        if plants[1].id < plants[0].id:
            plants = [plants[1], plants[0]]
        stmt = schema.reports_table.select().where(schema.reports_table.c.plant1 == plants[0].id).where(schema.reports_table.c.plant2 == plants[1].id)
        report = dict(con.execute(stmt).mappings().fetchone())
        if not report:
            return error_404, 404
        return render_template('report.html', report = report, plant1 = plants[0], plant2 = plants[1])

# Main script
if __name__ == '__main__':
    # TODO this function is not intended for production use, please rewrite before launch
    # https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask.run
    app.run(port = 2017)