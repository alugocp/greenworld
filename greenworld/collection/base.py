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
            elif len(keys) == 1:
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
