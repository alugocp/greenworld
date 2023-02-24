import logging
import copy
import json
import csv
import sys
import re
import os
import xlrd
import sqlalchemy
from sqlalchemy_utils import NumericRangeType
from greenworld.lib import init_greenworld
from greenworld.lib import schema
from greenworld.lib import defs

# CLI options structure for global access
cli_options = {
    'range': None,
    'row-headers': None,
    'col-headers': None,
    'citation': None,
    'map': {}
}

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
        'Usage: python3 enter [option [...]] [file [...]]',
        'This command inserts all data from the given files to the Greenworld database, with the following rules:',
        ' • A JSON file must follow the structure defined in README.md',
        ' • Any matrix file (CSV) can be processed using the following options:',
        '   --range = <c0>:<c1>,<r0>:<r1>\t\t\tdefines the range of data to include (from c0, r0 to c1, r1 inclusive)',
        '   --row-headers = <filename> | <c0>:<c1>,<r0>:<r1>\tfilepath or range that points to a list of row headers)',
        '   --col-headers = <filename> | <c0>:<c1>,<r0>:<r1>\tfilepath or range that points to a list of column headers)',
        '   --citation = <filename>\t\t\t\traw citation text or a filepath that points to a citation file',
        '   --map <x> <Ecology enum field>\t\t\t\tmaps any value x into an Ecology enum value',
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

def retrieve_or_insert(con, table, column, data):
    row = select_by(con, table, column, data[column])
    if row:
        return row
    data['id'] = get_last_id(con, table) + 1
    con.execute(table.insert().values(**data))
    logging.info(data)
    return data

# Parses a string representing an enum into its integer value
def parse_enum(name):
    enum = name.split('.')
    try:
        return getattr(defs, enum[0])[enum[1]].value
    except:
        raise Exception(f'Unknown enum \'{name}\'')

def parse_species_name(cells):
    concatenated = ' '.join(cells).lower()
    return re.sub(r' \([^)]+\)', '', concatenated)

# Process plant table bulk data entry
def enter_data(db, filename):
    _, ext = os.path.splitext(filename)
    print('')
    logging.info('Writing data from %s...', filename)
    if ext == '.json':
        return enter_data_json(db, filename)
    if ext == '.csv':
        return enter_data_csv(db, filename)
    if ext == '.xls':
        return enter_data_xls(db, filename)
    raise Exception(f'Data file with extension \'{ext}\' is not supported')

# Process ecology data from XLS file
def enter_data_xls(db, filename):
    csv_filename = filename.replace('.xls', '.csv')
    excel = xlrd.open_workbook(filename)
    sheet = excel.sheet_by_index(0)
    with open(csv_filename, 'w', encoding = 'utf-8') as file:
        col = csv.writer(file)
        for a in range(sheet.nrows):
            col.writerow([cell.value for cell in sheet.row(a)])
    enter_data_csv(db, csv_filename)

# Process ecology data from CSV file
def enter_data_csv(db, filename):
    # Parse row and column headers
    if cli_options['row-headers'] is not None and isinstance(cli_options['row-headers'][0], int):
        cli_options['row-headers'] = extract_range_from_file(filename, cli_options['row-headers'])
        cli_options['row-headers'] = list(map(parse_species_name, cli_options['row-headers']))
    if cli_options['col-headers'] is not None and isinstance(cli_options['col-headers'][0], int):
        cli_options['col-headers'] = extract_range_from_file(filename, cli_options['col-headers'])
        cli_options['col-headers'] = list(map(parse_species_name, transposed(cli_options['col-headers'])))

    # Extract interaction matrix data
    if not cli_options['range']:
        raise Exception(f'No range specified for data file \'{filename}\'')
    data = extract_range_from_file(filename, cli_options['range'])
    if not len(data) == len(cli_options['row-headers']):
        raise Exception('Mismatched row headers length with number of data rows')
    if not len(data[0]) == len(cli_options['col-headers']):
        raise Exception('Mismatched column headers length with number of data columns')

    # Write data to database
    if not cli_options['citation']:
        raise Exception(f'No citation provided for data file {filename}')
    with db.connect() as con:
        citation = retrieve_or_insert(con, schema.works_cited_table, 'citation', {
            'citation': cli_options['citation']
        })
        for a, _ in enumerate(data):
            for b, _ in enumerate(data[a]):
                point = data[a][b]
                if point in cli_options['map']:
                    mapped = cli_options['map'][point]
                    latin1 = cli_options['row-headers'][a]
                    latin2 = cli_options['col-headers'][b]
                    logging.info('Visiting %s x %s', latin1, latin2)
                    species1 = select_by(con, schema.plants_table, 'species', latin1)
                    if species1:
                        species2_latin = latin2
                    else:
                        species1 = select_by(con, schema.plants_table, 'species', latin2)
                        species2_latin = latin1
                    if species1:
                        species2 = retrieve_or_insert(con, schema.other_species_table, 'species', {
                            'species': species2_latin,
                            'name': species2_latin
                        })
                        interaction = {
                            'plant': species1['id'],
                            'non_plant': species2['id'],
                            'relationship': mapped,
                            'citation': citation['id']
                        }
                        con.execute(schema.ecology_other_table.insert().values(**interaction))
                        logging.info(interaction)
        con.commit()

# Parses a line of a CSV file
def parse_csv_line(line):
    return list(csv.reader([line.rstrip()]))[0]

# Parse a file range string
def parse_range(text):
    result = re.match(r'([0-9]+):([0-9]+),([0-9]+):([0-9]+)', text)
    if not result:
        return None
    groups = list(result.groups())
    for i, group in enumerate(groups):
        groups[i] = None if group == '' else int(group)
        if i % 2 == 0 and groups[i] is None:
            groups[i] = 0
    return groups

# Extract a subset of a CSV file
def extract_range_from_file(filename, r):
    rows = []
    with open(filename, 'r', encoding = 'utf-8') as file:
        for i, row in enumerate(file.readlines()):
            if r[2] <= i <= r[3]:
                parsed = parse_csv_line(row)
                rows.append(parsed[r[0] : r[1] + 1])
    return rows

# Grab headers as a list of lines from a file
def extract_headers_from_file(filename):
    with open(filename, 'r', encoding = 'utf-8') as file:
        return file.read().rstrip().split('\n')

# Returns a transposed matrix
def transposed(matrix):
    result = [[0 for _ in range(len(matrix))] for _ in range(len(matrix[0]))]
    for a, _ in enumerate(matrix):
        for b, _ in enumerate(matrix[a]):
            result[b][a] = matrix[a][b]
    return result

# Process plant table bulk data entry for a JSON file
def enter_data_json(db, filename):
    with open(filename, 'r', encoding = 'utf-8') as file:
        data = json.load(file)
    with db.connect() as con:
        works_cited_map = get_works_cited_map(con, data)

        # Write other species data to the database
        logging.info('Writing other species data...')
        last_other_id = get_last_id(con, schema.other_species_table)
        for row in (data['others'] if 'others' in data else []):
            values = copy.deepcopy(row)
            values['id'] = last_other_id + 1
            last_other_id += 1
            logging.info(values)
            con.execute(schema.other_species_table.insert().values(**values))
        print('')

        # Sanitize and write plant data to database
        ecology_data = {}
        logging.info('Writing plant and interaction data...')
        last_plant_id = get_last_id(con, schema.plants_table)
        for row in (data['plants'] if 'plants' in data else []):
            values = copy.deepcopy(row)
            values['id'] = last_plant_id + 1
            last_plant_id += 1
            ecology_data[values['id']] = values.pop('ecology') if 'ecology' in values else []

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

        # Handle ecological data
        for plant_id, data in ecology_data.items():
            process_ecological_fields(con, works_cited_map, plant_id, data)
        con.commit()

# Map local references to the database (handles if they exist already or not)
def get_works_cited_map(con, data):
    works_cited_map = {}
    logging.info('Writing works cited...')
    last_id = get_last_id(con, schema.works_cited_table)
    for row in (data['works_cited'] if 'works_cited' in data else []):
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

# Write ecological data with a many-to-many relationship to the database
def process_ecological_fields(con, works_cited_map, plant_id, data):
    for row in data:

        # Retrieve (and/or create) plant or non-plant species
        is_plant = True
        result = select_by(con, schema.plants_table, 'species', row['species'])
        if not result:
            is_plant = False
            result = select_by(con, schema.other_species_table, 'species', row['species'])
        if not result:
            species = row['species']
            raise Exception(f'Unknown interactive species \'{species}\'')
        interaction = {
            'plant': plant_id,
            'relationship': parse_enum(row['relationship']),
            'citation': works_cited_map[row['citation']]
        }
        if is_plant:
            interaction['target'] = result['id']
            con.execute(schema.ecology_plant_table.insert().values(**interaction))
        else:
            interaction['non_plant'] = result['id']
            con.execute(schema.ecology_other_table.insert().values(**interaction))
        logging.info(interaction)

def main(args):
    init_greenworld()
    db = schema.init_db()
    a = 0
    while a < len(args):
        if args[a] == '--help':
            print_help()
            break
        if '--' in args[a] and args[a].index('--') == 0:
            if not len(args) > a + 2:
                raise Exception('Not enough CLI arguments')
            key = args[a][2:]
            if not key in cli_options:
                raise Exception(f'Unknown CLI option \'{key}\'')
            if key == 'map':
                cli_options['map'][args[a + 1]] = parse_enum('Ecology.' + args[a + 2])
            elif key == 'range':
                cli_options['range'] = parse_range(args[a + 2])
            elif key in ['row-headers', 'col-headers']:
                cli_options[key] = parse_range(args[a + 2]) or extract_headers_from_file(args[a + 2])
            else:
                cli_options[key] = args[a + 2]
            a += 3
        else:
            enter_data(db, args[a])
            a += 1

if __name__ == '__main__':
    main(sys.argv[1:])
