from typing import List, Union
from greenworld.lib import Greenworld

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

    # Requests some missing data
    def request_data(self, path: str):
        self.__missing_paths.append(path)

    # Returns secondary data to request
    def get_missing_paths(self) -> List[str]:
        return self.__missing_paths

    # Clears the list of secondary data to request
    def clear_missing_paths(self):
        self.__missing_paths.clear()
