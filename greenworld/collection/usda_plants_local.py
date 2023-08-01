from typing import Dict, List
import re
import csv
from greenworld.collection import BaseDataCollector
from greenworld.lib import Greenworld

class UsdaPlantsLocalDataCollector(BaseDataCollector):
    __genera: Dict[str, List[str]] = {}
    __families: Dict[str, str] = {}

    def __init__(self, gw: Greenworld):
        super().__init__(gw)
        with open('referenced-data/usda_plants_database.txt', 'r', encoding = 'utf-8') as file:
            for line in file.readlines():
                sanitized = list(csv.reader([line]))[0]
                common = sanitized[3]
                if len(common) > 0:
                    genus = sanitized[2].lower().split(' ')[0]
                    family = sanitized[4].lower()
                    if genus not in self.__families:
                        self.__families[genus] = family
                    if genus not in self.__genera:
                        self.__genera[genus] = []
                    self.__genera[genus].append([sanitized[2].lower(), common])

    # TODO rewrite this function with binary search algorithm (data is in alphabetical order)
    def find_match(self, species: str) -> dict:
        genus = species.split(' ')[0]
        if genus in self.__genera:
            suffix = ' '.join(species.split(' ')[1:])
            for entry in self.__genera[genus]:
                if suffix in entry[0]:
                    return {
                        'name': entry[1],
                        'family': self.__families[genus]
                    }
        return None

    def matches_input(self, key: str) -> bool:
        return re.match(r'^plants.[0-9]+$', key)

    def collect_data(self, key: dict) -> dict:
        species = key['species']

        # Query cached USDA plants database
        self.gw.log(f'Searching cached USDA Plants Database for {species}...')
        return self.find_match(species)
