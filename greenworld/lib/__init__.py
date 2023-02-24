from typing import Callable
import logging
import os

class Greenworld:
    __log: Callable[[str], None]

    def __init__(self, log_func = logging.info):
        os.environ['GREENWORLD_DB'] = 'sqlite:///greenworld.db'
        logging.basicConfig(level = logging.NOTSET)
        self.__log = log_func

    def log(self, msg: str) -> None:
        self.__log(msg)
