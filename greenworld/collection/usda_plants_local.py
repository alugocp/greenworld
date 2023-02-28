from typing import List
import re
import csv
from greenworld.collection import BaseDataCollector
from greenworld.lib import Greenworld

class UsdaPlantsLocalDataCollector(BaseDataCollector):
    __database: List[str] = []

    def __init__(self, gw: Greenworld):
        super().__init__(gw)
        with open('referenced-data/usda_plants_database.txt', 'r', encoding = 'utf-8') as file:
            for line in file.readlines():
                sanitized = re.fullmatch(r'^"[A-Z0-9]*","[A-Z0-9]*","([^\n]+)\n?$', line)
                if sanitized:
                    self.__database.append(sanitized.group(1).lower())

    # TODO rewrite this function with binary search algorithm (data is in alphabetical order)
    def find_match(self, species: str) -> dict:
        for line in self.__database:
            if line.startswith(species):
                row = list(csv.reader([f'"{line}']))[0]
                return {
                    'name': row[1].title(),
                    'family': row[2]
                }
        return None

    def matches_input(self, key: str) -> bool:
        return re.match(r'^plants.[0-9]+$', key)

    def collect_data(self, key: dict) -> dict:
        species = key['species']

        # Query cached USDA plants database
        self.gw.log(f'Searching cached USDA Plants Database for {species}...')
        return self.find_match(species)
