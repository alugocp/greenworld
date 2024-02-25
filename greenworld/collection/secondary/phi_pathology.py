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
        works_cited = key["works_cited"] if "works_cited" in key else []
        citation_id = max(list(map(lambda x: x["id"], works_cited))) + 1 if len(works_cited) > 0 else 1
        works_cited.append(
            {
                "id": citation_id,
                "citation": "http://www.phi-base.org/searchFacet.htm?queryTerm=",
            }
        )
        key["works_cited"] = works_cited

        # Grab pathogens for each plant species
        other_species = key["others"] if "others" in key else []
        for plant in key["plants"] if "plants" in key else []:
            pathogens = self.get_pathogen_species(plant["species"])

            # Add the pathogen if they're not already listed for this plant species
            ecology = plant["ecology"] if "ecology" in key else []
            for pathogen in pathogens:
                if not any(pathogen == partner["species"] for partner in ecology):
                    ecology.append(
                        {
                            "species": pathogen,
                            "relationship": "Ecology.PATHOGEN",
                            "citation": citation_id,
                        }
                    )
                if not any(pathogen == species["species"] for species in other_species):
                    other_species.append({"species": pathogen, "name": "???"})
            if len(ecology) > 0:
                plant["ecology"] = ecology
        key["others"] = other_species

        # Return the updated data
        return key
