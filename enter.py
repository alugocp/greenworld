import logging
import copy
import json
import sys
import os
import sqlalchemy
from sqlalchemy_utils import NumericRangeType
from greenworld import schema
from greenworld import defs

# Conversions table for internal standard units
_conversions = {
    'f':   lambda f:   (f - 32) / 1.8,  # Convert to celsius
    'lbs': lambda lbs: lbs * 453.59237, # Convert to grams
    'in':  lambda x:   x * 0.0254,      # Convert to meters
    'ft':  lambda ft:  ft * 0.3048      # Convert to meters
}

# Prints helpful information to the terminal
def print_help():
    print(
        'Usage: python3 enter [file [...]]',
        'This command inserts all data from the given files to the Greenworld database, with the following rules:',
        ' • A JSON file must follow the structure defined in README.md',
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
    except:
        raise Exception(f'Unknown enum \'{name}\'')

# Process plant table bulk data entry
def enter_data(db, filename):
    _, ext = os.path.splitext(filename)
    if ext == '.json':
        return enter_data_json(db, filename)
    raise Exception(f'Data file with extension {ext} is not supported')

# Process plant table bulk data entry for a JSON file
def enter_data_json(db, filename):
    print('')
    logging.info('Writing data from %s...', filename)
    with open(filename, 'r', encoding = 'utf-8') as file:
        data = json.load(file)
    with db.connect() as con:
        works_cited_map = get_works_cited_map(con, data)

        # Sanitize and write plant data to database
        logging.info('Writing plant and interaction data...')
        last_plant_id = get_last_id(con, schema.plants_table)
        for row in (data['plants'] or []):
            values = copy.deepcopy(row)
            values['id'] = last_plant_id + 1
            last_plant_id += 1
            allelopathy = values.pop('allelopathy') if 'allelopathy' in values else []
            ecology = values.pop('ecology') if 'ecology' in values else []

            # Map citations
            mapped_citations = {}
            for cite_key in (values['citations'] or {}).keys():
                mapped_citations[str(works_cited_map[int(cite_key)])] = values['citations'][cite_key]
            values['citations'] = mapped_citations

            # Map general properties of plant data
            for col, val in values.items():

                # Convert enum references to their integer values
                if isinstance(schema.plants_table.c[col].type, sqlalchemy.Integer) and isinstance(val, str):
                    values[col] = parse_enum(val)

                # Convert nonstandard units to internal standard units
                if isinstance(schema.plants_table.c[col].type, NumericRangeType) and isinstance(val[0], str):
                    values[col][0] = convert_to_unit(val[0])
                    values[col][1] = convert_to_unit(val[1])

            # Write sanitized values to database
            logging.info(values)
            con.execute(schema.plants_table.insert().values(**values))

            # Handle allelochemical and ecology data
            process_graphed_fields(
                con, allelopathy,
                works_cited_map, values['id'], schema.allelochemicals_table,
                schema.allelopathy_table,
                'name',
                'allelochemical'
            )
            process_graphed_fields(
                con, ecology,
                works_cited_map, values['id'], schema.other_species_table,
                schema.ecology_table,
                'species',
                'species'
            )
        con.commit()

# Map local references to the database (handles if they exist already or not)
def get_works_cited_map(con, data):
    works_cited_map = {}
    if 'works_cited' in data:
        logging.info('Writing works cited...')
        last_id = get_last_id(con, schema.works_cited_table)
        for row in data['works_cited']:
            values = copy.deepcopy(row)
            works_cited_result = select_by(con, schema.works_cited_table, 'citation', values['citation'])
            if works_cited_result:
                works_cited_map[row['id']] = works_cited_result['id']
            else:
                values['id'] = last_id + 1
                works_cited_map[row['id']] = values['id']
                logging.info(values)
                con.execute(schema.works_cited_table.insert().values(**values))
                last_id += 1
        print('')
    return works_cited_map

# Write data with a many-to-many relationship to the plants table
def process_graphed_fields(con, data, works_cited_map, plant_id, entity_table, interaction_table, name_col, foreign_id_col):
    last_id = get_last_id(con, entity_table)
    for row in data:
        result = select_by(con, entity_table, name_col, row[name_col])
        if not result:
            result = { 'id': last_id + 1 }
            result[name_col] = row[name_col]
            last_id += 1
            logging.info(result)
            con.execute(entity_table.insert().values(**result))
        interaction = {
            'plant': plant_id,
            'relationship': parse_enum(row['relationship']),
            'citation': works_cited_map[row['citation']]
        }
        interaction[foreign_id_col] = result['id']
        logging.info(interaction)
        con.execute(interaction_table.insert().values(**interaction))

def main(args):
    os.environ['GREENWORLD_DB'] = 'sqlite:///greenworld.db'
    logging.basicConfig(level=logging.NOTSET)
    db = schema.init_db()
    a = 0
    while a < len(args):
        if args[a] == '--help':
            print_help()
            break
        enter_data(db, args[a])
        a += 1

if __name__ == '__main__':
    main(sys.argv[1:])
