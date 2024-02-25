from typing import Dict, List
import re
import csv
from greenworld.collection.base import BaseDataCollector
from greenworld import Greenworld

growth_habits_map = {
    "Forb/herb": "GrowthHabit.FORB",
    "Graminoid": "GrowthHabit.GRAMINOID",
    "Lichenous": "GrowthHabit.LICHENOUS",
    "Nonvascular": "GrowthHabit.NONVASCULAR",
    "Shrub": "GrowthHabit.SHRUB",
    "Subshrub": "GrowthHabit.SUBSHRUB",
    "Tree": "GrowthHabit.TREE",
    "Vine": "GrowthHabit.VINE",
}


class UsdaPlantsLocalDataCollector(BaseDataCollector):
    __genera: Dict[str, List[str]] = {}
    __families: Dict[str, str] = {}

    def __init__(self, gw: Greenworld):
        super().__init__(gw)

        # Cache from main database
        with open(
            "referenced-data/usda_plants_database.csv", "r", encoding="utf-8"
        ) as file:
            next(file)
            for line in file.readlines():
                sanitized = list(csv.reader([line]))[0]
                common = sanitized[3]
                if len(common) > 0:
                    genus = sanitized[2].lower().split(" ")[0]
                    family = sanitized[4].lower()
                    if genus not in self.__families:
                        self.__families[genus] = family
                    if genus not in self.__genera:
                        self.__genera[genus] = []
                    self.__genera[genus].append([sanitized[2].lower(), common])

        # Cache from growth habit database
        # Search type: Growth Habit
        # Forb/herb|Graminoid|Lichenous|Nonvascular|Shrub|Subshrub|Tree|Vine
        with open(
            "referenced-data/usda_plants_database_growth_habit.csv",
            "r",
            encoding="utf-8",
        ) as file:
            next(file)
            for line in file.readlines():
                sanitized = list(csv.reader([line]))[0]
                scientific = sanitized[2].lower().split(" ")
                if scientific[0] in self.__genera:
                    for entry in self.__genera[scientific[0]]:
                        if scientific[1] in entry[0]:
                            entry.append(sanitized[4])
                            break

    def find_match(self, species: str, needs: List[str]) -> dict:
        genus = species.split(" ")[0].lower()
        if genus in self.__genera:
            suffix = " ".join(species.split(" ")[1:])
            for entry in self.__genera[genus]:
                if suffix in entry[0]:
                    result = {}
                    if "name" in needs:
                        result["name"] = entry[1]
                    if "family" in needs:
                        result["family"] = self.__families[genus]
                    if len(entry) == 3 and "growth_habit" in needs:
                        result["growth_habit"] = growth_habits_map[entry[2]]
                    return result
        return None

    def matches_input(self, key: str) -> bool:
        return re.match(r"^plants.[0-9]+$", key)

    def collect_data(self, key: dict) -> dict:
        species = key["species"]
        needs = []
        if "name" not in key:
            needs.append("name")
        if "family" not in key:
            needs.append("family")
        if "growth_habit" not in key:
            needs.append("growth_habit")

        # Query cached USDA plants database
        if len(needs) == 0:
            self.gw.log(f"Nothing is needed for {species}")
            return None
        self.gw.log(f"Searching cached USDA Plants Database for {species}...")
        return self.find_match(species, needs)
