"""
This script queries and inserts relevant pathogen species into a seed data file
"""
from typing import List
import urllib.request
import ssl
import re
from greenworld.collection.base import BaseDataCollector

class PhiPathologyDataCollector(BaseDataCollector):

    def get_pathogen_species(self, species: str) -> List[str]:
        """
        Extract the pathogen species list for a given species
        """
        self.gw.log(f"Retrieving pathogens for {species}...")
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        species = species.replace(" ", "+")
        url = f"http://www.phi-base.org/searchFacet.htm?queryTerm={species}"
        with urllib.request.urlopen(url, context=context) as data:
            content = data.read().decode("utf-8")
            results = re.findall(
                r"<input  name=\'Pathogen_species\' type=\'checkbox\' value=\'([A-Za-z ]+)\'",
                content,
            )
            return list(map(lambda x: x.lower(), results))


    def matches_input(self, key: str) -> bool:
        return re.match(r"^\(pathogens\)$", key)


    def collect_data(self, key: dict):
        """
        Goes through the process of adding pathology data to a given file
        """

        # Set up the citations
        citation_id = self.populate_works_cited(key, "http://www.phi-base.org/searchFacet.htm?queryTerm=")

        # Grab pathogens for each plant species
        for plant in key["plants"] if "plants" in key else []:
            pathogens = self.get_pathogen_species(plant["species"])
            self.add_ecology(key, plant, citation_id, pathogens, "Ecology.PATHOGEN")

        # Return the updated data
        return key
