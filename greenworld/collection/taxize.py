from typing import Dict, List
import re
import json
from greenworld.collection import BaseDataCollector
from greenworld import Greenworld

TAXIZE_BATCH_SIZE = 100


# https://docs.ropensci.org/taxize/reference/index.html
class TaxizeDataCollector(BaseDataCollector):
    __cache: Dict[str, List[str]]
    __query_paths: Dict[str, str]

    def __init__(self, gw: Greenworld):
        super().__init__(gw)
        self.__query_paths = {}
        try:
            with open("referenced-data/taxize-cache.json", "r", encoding = 'utf-8') as file:
                self.__cache = json.loads(file.read())
        except OSError:
            self.__cache = {}

    def destroy(self):
        with open("referenced-data/taxize-cache.json", "w", encoding = 'utf-8') as file:
            file.write(json.dumps(self.__cache))

    def search_cached_data(self, species: str):
        if species in self.__cache:
            del self.__query_paths[species]
            return self.__cache[species]
        return None

    def get(self, data, path):
        old = super().get(data, path)
        self.__query_paths[old["species"]] = path
        return old

    def final_fill(self, data):
        while len(self.__query_paths) > 0:
            l = len(self.__query_paths)
            self.gw.log(
                f'Querying Taxize service ({l} data points left)...'
            )
            species_list = list(self.__query_paths.keys())
            if len(species_list) > TAXIZE_BATCH_SIZE:
                species_list = species_list[0:TAXIZE_BATCH_SIZE]

            # Query Taxize via R script
            results = {
                "physaria didymocarpa": {
                    "species": "physaria didymocarpa",
                    "name": "common twinpod",
                    "family": "brassicaceae",
                }
            }

            # Fill in results
            for k, v in results.items():
                self.fill(data, self.__query_paths[k], v)
                self.__cache[k] = v
            for species in species_list:
                del self.__query_paths[species]

    # Make this work for plants and insects
    def matches_input(self, key: str) -> bool:
        return re.match(r"^plants.[0-9]+$", key) or re.match(
            r"^others.[0-9]+\(insect\)$", key
        )

    def collect_data(self, key: dict) -> dict:
        species = key["species"]

        # Query cached Taxize results
        self.gw.log(f"Searching cached Taxize data for {species}...")
        cached = self.search_cached_data(species)
        return cached if cached else None
