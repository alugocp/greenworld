from typing import Dict, List
import re
import json
from greenworld.collection import BaseDataCollector
from greenworld.lib import Greenworld

class TaxizeDataCollector(BaseDataCollector):
    __cache: Dict[str, List[str]]

    def __init__(self, gw: Greenworld):
        super().__init__(gw)
        with open('referenced-data/taxize-cache.json', 'r') as file:
            self.__cache = json.loads(file.read())

    def destroy(self):
        with open('referenced-data/taxize-cache.json', 'w') as file:
            file.write(json.dumps(self.__cache))

    def search_cached_data(self, species: str):
        if species in self.__cache:
            return {
                'species': self.__cache[species][0],
                'name': self.__cache[species][1],
                'family': self.__cache[species][2]
            }
        return None

    def query_taxize(self, species: str):
        pass

    def matches_input(self, key: str) -> bool:
        return re.match(r'^plants.[0-9]+$', key) or re.match(r'^others.[0-9]+\(insect\)$', key)

    def collect_data(self, key: dict) -> dict:
        species = key['species']

        # Query cached Taxize results
        self.gw.log(f'Searching cached Taxize data for {species}...')
        cached = self.search_cached_data(species)
        if cached:
            return cached

        # Query Taxize live service
        self.gw.log(f'Querying Taxize service for {species}...')
        return self.query_taxize(species)
