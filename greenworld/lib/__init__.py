import logging
import os

def init_greenworld():
    os.environ['GREENWORLD_DB'] = 'sqlite:///greenworld.db'
    logging.basicConfig(level = logging.NOTSET)
