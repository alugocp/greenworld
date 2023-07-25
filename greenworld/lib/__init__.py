from typing import Callable, Dict
import logging
import os
import re

# Imports key-value pairs from .env file
def read_env() -> Dict[str, str]:
    env = {}
    with open('.env', 'r', encoding = 'utf-8') as file:
        lines = file.readlines()
    for line in lines:
        match = re.match(r'^(\w+)=(\w+)$', line)
        if match:
            env[match.groups()[0]] = match.groups()[1]
    return env

# Top-level class for the Greenworld companion planting algorithm
class Greenworld:
    __log: Callable[[str], None]

    def __init__(self, filename = None, log_func = logging.info):
        env = read_env()
        if 'DRIVER' in env and env['DRIVER'] == 'sqlite':
            os.environ['GREENWORLD_DB'] = 'sqlite:///greenworld.db'
        else:
            password = env['PASSWORD']
            host = 'database' if os.environ['PYTHONPATH'] == '/srv' else 'localhost'
            os.environ['GREENWORLD_DB'] = f'postgresql://postgres:{password}@{host}:5432/greenworld'
        logging.basicConfig(
            filename = filename,
            encoding = 'utf-8',
            level = logging.NOTSET
        )
        self.__log = log_func
        self.log('Greenworld script initialized')

    def log(self, msg: str) -> None:
        self.__log(msg)
