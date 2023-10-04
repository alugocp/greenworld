from typing import Set
import re
from greenworld.collection import BaseDataCollector
from greenworld import Greenworld


class NitrogenFixersDataCollector(BaseDataCollector):
    __genera: Set[str]

    def __init__(self, gw: Greenworld):
        super().__init__(gw)
        self.__genera = set()

        # Cache from main database
        with open(
            "referenced-data/leguminous_genera.txt", "r", encoding="utf-8"
        ) as file:
            for genus in file.readlines():
                self.__genera.add(genus.strip())

    def matches_input(self, key: str) -> bool:
        return re.match(r"^plants.[0-9]+.nitrogen$", key)

    def collect_data(self, key: dict) -> dict:
        genus = key["species"].split(" ")[0]
        if genus in self.__genera:
            print(f"{genus} is a nitrogen fixer!")
            return {"nitrogen": "Nitrogen.FIXER"}
        return None
