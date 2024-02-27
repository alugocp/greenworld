import re
from typing import List, Union
from greenworld import Greenworld


class BaseDataCollector:
    __missing_paths: List[str] = []
    gw: Greenworld

    def __init__(self, gw: Greenworld):
        self.gw = gw

    # Should return True if this subclass is designed to handle the given input
    def matches_input(self, key: str) -> bool:
        raise NotImplementedError()

    # Returns some data to fill out the requested input
    def collect_data(self, key: Union[str, dict]) -> dict:
        raise NotImplementedError()

    # De-initialize, if necessary
    def destroy(self):
        pass

    # Gets a value from the data at the given path
    def get(self, data, path):
        queries = [
            r"^([a-z]+)\.([0-9]+)",
            r"^([a-z]+)",
        ]
        for regex in queries:
            results = re.search(regex, path)
            if results is None:
                continue
            keys = results.groups()
            if len(keys) == 2:
                return data[keys[0]][int(keys[1])]
            if len(keys) == 1:
                return data[keys[0]]
        return data

    # Updates some missing data at the given path
    def fill(self, data, path, value):
        self.get(data, path).update(value)

    # Last call for missing data
    def final_fill(self, data):
        pass

    # Requests some missing data
    def request_data(self, path: str):
        self.__missing_paths.append(path)

    # Returns secondary data to request
    def get_missing_paths(self) -> List[str]:
        return self.__missing_paths

    # Clears the list of secondary data to request
    def clear_missing_paths(self):
        self.__missing_paths.clear()

    # Grabs the ID of a citation in the works_cited and adds one if none such exists
    def populate_works_cited(self, key: dict, citation: str) -> int:
        works_cited = key["works_cited"] if "works_cited" in key else []
        candidates = list(filter(lambda x: x["citation"] == citation, works_cited))
        if len(candidates) > 0:
            return candidates[0]["id"]
        citation_id = max(list(map(lambda x: x["id"], works_cited))) + 1 if len(works_cited) > 0 else 1
        works_cited.append(
            {
                "id": citation_id,
                "citation": citation,
            }
        )
        key["works_cited"] = works_cited
        return citation_id

    # Populates plant data with some ecological partner
    def add_ecology(self, key: dict, plant: dict, citation_id: int, partners: List[str], relationship: str) -> ():
        other_species = key["others"] if "others" in key else []

        # Add the partner if they're not already listed for this plant species
        ecology = plant["ecology"] if "ecology" in plant else []
        for partner in partners:
            if not any(partner == species["species"] for species in ecology):
                ecology.append(
                    {
                        "species": partner,
                        "relationship": relationship,
                        "citation": citation_id,
                    }
                )
            if not any(partner == species["species"] for species in other_species):
                other_species.append({"species": partner, "name": "???"})
        if len(ecology) > 0:
            plant["ecology"] = ecology
        key["others"] = other_species
