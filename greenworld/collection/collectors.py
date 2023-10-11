"""
This module lists all of the active collectors used in Greenworld
"""
from greenworld import Greenworld
from greenworld.collection.primary.seed_data import SeedDataCollector
from greenworld.collection.primary.iweb_xls import IwebXlsDataCollector
from greenworld.collection.secondary.usda_plants_local import UsdaPlantsLocalDataCollector
from greenworld.collection.secondary.insects_local import InsectsLocalDataCollector
from greenworld.collection.secondary.nitrogen_fixers import NitrogenFixersDataCollector

def get_collectors(gw: Greenworld):
    """
    Returns a list of all active collectors
    """
    return [
        SeedDataCollector(gw),
        IwebXlsDataCollector(gw),
        UsdaPlantsLocalDataCollector(gw),
        InsectsLocalDataCollector(gw),
        NitrogenFixersDataCollector(gw),
    ]
