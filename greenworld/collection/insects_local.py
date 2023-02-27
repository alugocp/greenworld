from typing import Dict
import re
from openpyxl import load_workbook
from greenworld.collection import BaseDataCollector
from greenworld.lib.taxonomy import Taxon
from greenworld.lib import Greenworld

class InsectsLocalDataCollector(BaseDataCollector):
    __database: Dict[str, dict] = {}

    def __init__(self):
        taxon = Taxon()
        wb = load_workbook(filename = 'referenced-data/Common_names_list_01-18-23.xlsx')
        for i, row in enumerate(wb.active.rows):
            if i < 4:
                continue
            if taxon.parse_species(row[1].value).species:
                self.__database[taxon.pretty_species()] = {
                    'name': row[0].value.title(),
                    'family': row[3].value.lower()
                }

    def find_match(self, species: str) -> dict:
        return self.__database[species] if species in self.__database else None

    def matches_input(self, key: str) -> bool:
        return re.match(r'^others.[0-9]+\(insect\)$', key)

    def collect_data(self, key: dict) -> dict:
        gw = Greenworld()
        species = key['species']

        # Query cached USDA plants database
        gw.log(f'Searching cached Entomological Society of America\'s Common Names of Insects Database for {species}...')
        return self.find_match(species)
