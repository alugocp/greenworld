from typing import Optional, List
import csv
import re
import xlrd
from greenworld.collection import BaseDataCollector
from greenworld.taxonomy import Taxon
from greenworld import defs

# CLI options structure for global access
# TODO design a way to auto-detect these or have them passed in
cli_options = {
    'range': [4, 100, 4, 279],
    'row-headers': [1, 2, 4, 279],
    'col-headers': [4, 100, 1, 2],
    'citation': 'https://iwdb.nceas.ucsb.edu/html/clements_1923.html',
    'map': {
        '1.0': 'Ecology.POLLINATOR'
    }
}

# Parses a string representing an enum into its integer value
def parse_enum(name):
    enum = name.split('.')
    try:
        return getattr(defs, enum[0])[enum[1]].value
    except Exception as e:
        raise ValueError(f'Unknown enum \'{name}\'') from e

def parse_species_name(cells):
    concatenated = ' '.join(cells).lower()
    return re.sub(r' \([^)]+\)', '', concatenated)

# Parses a line of a CSV file
def parse_csv_line(line):
    return list(map(lambda x: x.strip(), list(csv.reader([line]))[0]))

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

def find_by_species(ls: List[dict], species: str) -> Optional[dict]:
    for obj in ls:
        if obj['species'] == species:
            return obj
    return None

class IwebXlsDataCollector(BaseDataCollector):

    def matches_input(self, key: str) -> bool:
        return key == 'referenced-data/clements_1923.xls'

    def collect_data(self, key: str) -> dict:

        # Convert to CSV file
        csv_filename = key.replace('.xls', '.csv')
        excel = xlrd.open_workbook(key)
        sheet = excel.sheet_by_index(0)
        with open(csv_filename, 'w', encoding = 'utf-8') as file:
            col = csv.writer(file)
            for a in range(sheet.nrows):
                col.writerow([cell.value for cell in sheet.row(a)])

        # Parse row and column headers
        if cli_options['row-headers'] is not None and isinstance(cli_options['row-headers'][0], int):
            cli_options['row-headers'] = extract_range_from_file(csv_filename, cli_options['row-headers'])
            cli_options['row-headers'] = list(map(parse_species_name, cli_options['row-headers']))
        if cli_options['col-headers'] is not None and isinstance(cli_options['col-headers'][0], int):
            cli_options['col-headers'] = extract_range_from_file(csv_filename, cli_options['col-headers'])
            cli_options['col-headers'] = list(map(parse_species_name, transposed(cli_options['col-headers'])))

        # Extract interaction matrix data
        data = extract_range_from_file(csv_filename, cli_options['range'])
        if len(data) != len(cli_options['row-headers']):
            raise ValueError('Mismatched row headers length with number of data rows')
        if len(data[0]) != len(cli_options['col-headers']):
            raise ValueError('Mismatched column headers length with number of data columns')

        # Write data object
        output = {
            'plants': [],
            'others': [],
            'works_cited': [
                {
                    'id': 1,
                    'citation': cli_options['citation']
                }
            ]
        }
        for a, sublist in enumerate(data):
            for b, _ in enumerate(sublist):
                point = sublist[b]
                if point in cli_options['map']:
                    mapped = cli_options['map'][point]
                    latin1 = cli_options['row-headers'][a] # Non-plant
                    latin2 = cli_options['col-headers'][b] # Plant
                    if not Taxon().parse_species(latin1).species or not Taxon().parse_species(latin2).species:
                        continue
                    self.gw.log(f'Visiting {latin1} x {latin2}')
                    plant = find_by_species(output['plants'], latin2)
                    nonplant = find_by_species(output['others'], latin1)
                    if not plant:
                        plant_id = len(output['plants'])
                        plant = {
                            'id': plant_id + 1,
                            'name': '',
                            'species': latin2,
                            'family': '',
                            'citations': {},
                            'ecology': []
                        }
                        output['plants'].append(plant)
                        self.request_data(f'plants.{plant_id}')
                        self.request_data(f'plants.{plant_id}.nitrogen')
                    if not nonplant:
                        nonplant_index = len(output['others'])
                        nonplant = {
                            'species': latin1,
                            'name': ''
                        }
                        output['others'].append(nonplant)
                        self.request_data(f'others.{nonplant_index}(insect)')
                    plant['ecology'].append({
                        'species': nonplant['species'],
                        'relationship': mapped,
                        'citation': 1
                    })
        return output
