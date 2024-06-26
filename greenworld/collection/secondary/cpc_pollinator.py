"""
This script queries and inserts relevant pollinator species into a seed data file
"""
from typing import List
import urllib.request
import json
import ssl
import re
from greenworld.collection.base import BaseDataCollector

class CpcPollinatorDataCollector(BaseDataCollector):

    def get_pollinator_species(self, species: str) -> List[str]:
        """
        Extract the pollinator species list for a given species
        """
        self.gw.log(f"Retrieving pollinators for {species}...")
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        count = -1
        processed = 0
        pollinators = []
        while count < 0 or processed < count:
            request = urllib.request.Request(
                "https://saveplants.org/app/ajax/FetchPollinatorData",
                method="POST",
                data=bytes(urllib.parse.urlencode({
                    "start": 0,
                    "length": 10,
                    "search": {
                        "value": "",
                        "regex": False
                    },
                    "dataType": "json",
                    "type": "plant",
                    "Family_ITIS": "",
                    "Genus_ITIS": "",
                    "AcceptedName_ITIS": species,
                    "In_National_Collection": ""
                }), encoding="utf-8"),
                headers={
                    # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                }
            )
            try:
                data = urllib.request.urlopen(request, context=context)
            except:
                return pollinators
            results = json.loads(data.read().decode("utf-8"))

            if count < 0:
                count = int(results["count"])
            processed += len(results["data"])
            pollinators += list(filter(lambda x: "Self pollinated" not in x and re.match(r"^[A-Z][a-z]+ [a-z]+", x), map(lambda x: x["pollinator_scientific"] or x["pollinator_name"], results["data"])))
        return pollinators

    def matches_input(self, key: str) -> bool:
        return re.match(r"^\(pollinators\)$", key)


    def collect_data(self, key: dict):
        """
        Goes through the process of adding pathology data to a given file
        """

        # Set up the citations
        citation_id = self.populate_works_cited(key, "https://saveplants.org/pollinator-search/")

        # Grab pollinators for each plant species
        for plant in key["plants"] if "plants" in key else []:
            pollinators = self.get_pollinator_species(plant["species"])
            self.add_ecology(key, plant, citation_id, pollinators, "Ecology.POLLINATOR")

        # Return the updated data
        return key
