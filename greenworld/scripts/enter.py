import copy
import json
import sys
import sqlalchemy
from schema import Schema, Optional, And, Or
from sqlalchemy_utils import NumericRangeType
from greenworld.lib import Greenworld
from greenworld.lib import orm
from greenworld.lib import defs

def expand_enum(e):
    return Or(*[f'{e.__name__}.{name}' for name in e.__members__.keys()])

json_schema = Schema({
    Optional('plants'): [
        {
            'id': int,
            'name': str,
            'species': str,
            'family': str,
            Optional('growth_habit'): expand_enum(defs.GrowthHabit),
            Optional('fruit_weight'): And([str], lambda x: len(x) == 2),
            Optional('height'): And([str], lambda x: len(x) == 2),
            Optional('spread'): And([str], lambda x: len(x) == 2),
            Optional('length'): And([str], lambda x: len(x) == 2),
            Optional('root_spread'): And([str], lambda x: len(x) == 2),
            Optional('root_depth'): And([str], lambda x: len(x) == 2),
            Optional('nitrogen'): expand_enum(defs.Nitrogen),
            Optional('temperature'): And([str], lambda x: len(x) == 2),
            Optional('sun'): expand_enum(defs.Sun),
            Optional('soil'): expand_enum(defs.Soil),
            Optional('pH'): And([float], lambda x: len(x) == 2 and x[0] >= 0 and x[1] <= 14 and x[0] <= x[1]),
            Optional('drainage'): expand_enum(defs.Drainage),
            'citations': {
                Optional(str): [str]
            },
            Optional('ecology'): [
                {
                    'species': str,
                    'relationship': expand_enum(defs.Ecology),
                    'citation': int
                }
            ]
        }
    ],
    Optional('others'): [
        {
            'species': str,
            'name': str,
            Optional('family'): str
        }
    ],
    Optional('works_cited'): [
        {
            'id': int,
            'citation': str
        }
    ]
})

# Conversions table for internal standard units
_conversions = {
    'f':   lambda f:   (f - 32) / 1.8,  # Convert fahrenheit to celsius
    'lbs': lambda lbs: lbs * 453.59237, # Convert pounds to grams
    'in':  lambda i:   i * 0.0254,      # Convert inches to meters
    'ft':  lambda ft:  ft * 0.3048      # Convert feet to meters
}

# Prints helpful information to the terminal
def print_help():
    print(
        'Usage: python3 enter [file [...]]',
        'This command inserts all data from the given JSON file(s) into the Greenworld database.',
        'Each file must follow the structure defined in README.md',
        sep='\n'
    )

# Converts value from unit to the internal standard unit
def convert_to_unit(value):
    if not ' ' in value:
        raise Exception(f'Scalar value \'{value}\' needs a space in between the number and the unit')
    val, unit = value.split(' ')
    val = float(val)
    unit = unit.lower()
    if unit in ['m', 'g', 'c']:
        return val
    if unit not in _conversions:
        raise Exception(f'Unknown unit \'{unit}\'')
    return round(_conversions[unit](val), 3)

# Returns the last ID from a table
def get_last_id(con, table):
    return (con.execute(table.select().order_by(table.c.id.desc()).limit(1)).mappings().fetchone() or { 'id': 0 })['id']

# Returns a row from some table where one column equals a given value
def select_by(con, table, column, value):
    return con.execute(table.select().where(table.c[column] == value)).mappings().fetchone()

# Parses a string representing an enum into its integer value
def parse_enum(name):
    enum = name.split('.')
    try:
        return getattr(defs, enum[0])[enum[1]].value
    except Exception as e:
        raise Exception(f'Unknown enum \'{name}\'') from e

# Process plant table bulk data entry for a JSON file
def enter_data(gw: Greenworld, db, filename):
    print('')
    gw.log(f'Writing data from {filename}...')
    with open(filename, 'r', encoding = 'utf-8') as file:
        data = json.load(file)
    assert json_schema.validate(data) == data
    with db.connect() as con:
        works_cited_map = get_works_cited_map(gw, con, data)

        # Write other species data to the database
        gw.log('Writing other species data...')
        last_other_id = get_last_id(con, orm.other_species_table)
        for row in (data['others'] if 'others' in data else []):
            values = copy.deepcopy(row)
            result = select_by(con, orm.other_species_table, 'species', values['species'])
            if result:
                new_values = {}
                new_values.update(result)
                new_values.update(values)
                gw.log(f'UPDATE {new_values}')
                con.execute(orm.other_species_table.update().where(orm.other_species_table.c['id'] == result['id']).values(**new_values))
            else:
                values['id'] = last_other_id + 1
                last_other_id += 1
                gw.log(f'INSERT {values}')
                con.execute(orm.other_species_table.insert().values(**values))
        print('')

        # Sanitize and write plant data to database
        ecology_data = {}
        gw.log('Writing plant and interaction data...')
        last_plant_id = get_last_id(con, orm.plants_table)
        for row in (data['plants'] if 'plants' in data else []):
            values = copy.deepcopy(row)
            local_ecology_data = values.pop('ecology') if 'ecology' in values else []

            # Map citations
            mapped_citations = {}
            for cite_key in (values['citations'] or {}).keys():
                mapped_citations[str(works_cited_map[int(cite_key)])] = values['citations'][cite_key]
            values['citations'] = mapped_citations

            # Map general properties of plant data
            for col, val in values.items():

                # Convert enum references to their integer values
                if isinstance(orm.plants_table.c[col].type, sqlalchemy.Integer) and isinstance(val, str):
                    values[col] = parse_enum(val)

                # Convert nonstandard units to internal standard units
                if isinstance(orm.plants_table.c[col].type, NumericRangeType) and isinstance(val[0], str):
                    values[col][0] = convert_to_unit(val[0])
                    values[col][1] = convert_to_unit(val[1])

            # Write sanitized values to database
            result = select_by(con, orm.plants_table, 'species', values['species'])
            if result:
                new_values = {}
                new_values.update(result)
                new_values.update(values)
                ecology_data[result['id']] = local_ecology_data
                gw.log(f'UPDATE {new_values}')
                con.execute(orm.plants_table.update().where(orm.plants_table.c['id'] == result['id']).values(**new_values))
            else:
                values['id'] = last_plant_id + 1
                last_plant_id += 1
                ecology_data[values['id']] = local_ecology_data
                gw.log(f'INSERT {values}')
                con.execute(orm.plants_table.insert().values(**values))

        # Handle ecological data
        for plant_id, data in ecology_data.items():
            process_ecological_fields(gw, con, works_cited_map, plant_id, data)
        con.commit()

# Map local references to the database (handles if they exist already or not)
def get_works_cited_map(gw: Greenworld, con, data):
    works_cited_map = {}
    gw.log('Writing works cited...')
    last_id = get_last_id(con, orm.works_cited_table)
    for row in (data['works_cited'] if 'works_cited' in data else []):
        values = copy.deepcopy(row)
        works_cited_result = select_by(con, orm.works_cited_table, 'citation', values['citation'])
        if works_cited_result:
            works_cited_map[row['id']] = works_cited_result['id']
        else:
            values['id'] = last_id + 1
            works_cited_map[row['id']] = values['id']
            gw.log(f'INSERT {values}')
            con.execute(orm.works_cited_table.insert().values(**values))
            last_id += 1
    print('')
    return works_cited_map

# Write ecological data with a many-to-many relationship to the database
def process_ecological_fields(gw: Greenworld, con, works_cited_map, plant_id, data):
    for row in data:

        # Retrieve (and/or create) plant or non-plant species
        is_plant = True
        result = select_by(con, orm.plants_table, 'species', row['species'])
        if not result:
            is_plant = False
            result = select_by(con, orm.other_species_table, 'species', row['species'])
        if not result:
            species = row['species']
            raise Exception(f'Unknown interactive species \'{species}\'')
        interaction = {
            'plant': plant_id,
            'relationship': parse_enum(row['relationship']),
            'citation': works_cited_map[row['citation']]
        }

        # Insert or update in database
        if is_plant:
            interaction['target'] = result['id']
            and_clause = sqlalchemy.and_(
                orm.ecology_plant_table.c['plant'] == plant_id,
                orm.ecology_plant_table.c['target'] == result['id']
            )
            existing = con.execute(orm.ecology_plant_table.select().where(and_clause)).fetchone()
            if existing:
                gw.log(f'UPDATE {interaction}')
                con.execute(orm.ecology_plant_table.update().where(and_clause).values(**interaction))
            else:
                gw.log(f'INSERT {interaction}')
                con.execute(orm.ecology_plant_table.insert().values(**interaction))
        else:
            interaction['non_plant'] = result['id']
            and_clause = sqlalchemy.and_(
                orm.ecology_other_table.c['plant'] == plant_id,
                orm.ecology_other_table.c['non_plant'] == result['id']
            )
            existing = con.execute(orm.ecology_other_table.select().where(and_clause)).fetchone()
            if existing:
                gw.log(f'UPDATE {interaction}')
                con.execute(orm.ecology_other_table.update().where(and_clause).values(**interaction))
            else:
                gw.log(f'INSERT {interaction}')
                con.execute(orm.ecology_other_table.insert().values(**interaction))

def main(gw: Greenworld, args):
    db = orm.init_db()
    for a, _ in enumerate(args):
        if args[a] == '--help':
            print_help()
            break
        enter_data(gw, db, args[a])

if __name__ == '__main__':
    main(Greenworld(), sys.argv[1:])
