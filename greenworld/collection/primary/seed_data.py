"""
This module adds support for seed data files in the collection system
"""
import re
import json
from greenworld.collection.base import BaseDataCollector

class SeedDataCollector(BaseDataCollector):
    """
    Tells the collection process to grab all potential data for any incoming plant species data
    """

    def matches_input(self, key: str) -> bool:
        """
        Match seed data JSON filenames
        """
        return re.match(r"^seed-data/[\w\-]+\.json$", key)

    def collect_data(self, key: str) -> dict:
        """
        Request data for every plant in the file
        """
        with open(key, "r", encoding = "utf-8") as file:
            data = json.loads(file.read())
            for i, _ in enumerate(data["plants"] if "plants" in data else []):
                self.request_data(f"plants.{i}")
                self.request_data(f"plants.{i}.nitrogen")
            self.request_data("(pathogens)")
            self.request_data("(pests)")
            return data
