from .types import Sunlight, Drainage, Water, Range, Kingdom

# This class represents a single species logged within this project.
# It contains information to help determine an organism's ideal growing
# environment.
class Species:
    sunlight: Sunlight
    drainage: Drainage
    kingdom: Kingdom
    height: Range
    roots: Range
    water: Water
    latin: str
    name: str
    pH: Range

    def __init__(self, **kwargs):
        self.kingdom = kwargs['kingdom'] if 'kingdom' in kwargs else Kingdom.PLANT
        self.latin = kwargs['latin']
        self.name = kwargs['name']

    def __repr__(self) -> str:
        return f'{self.name} ({self.latin})'