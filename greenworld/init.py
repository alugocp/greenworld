import logging
import os

def init():
    os.environ['GREENWORLD_DB'] = 'sqlite:///greenworld.db'
    logging.basicConfig(level = logging.NOTSET)