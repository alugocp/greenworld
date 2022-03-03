from typing import Dict
from .types import Sunlight, Drainage, Water, Range, Kingdom

# This class represents a single species logged within this project. It contains
# information to help determine an organism's ideal growing environment.
class Species:
    sunlight: Sunlight
    drainage: Drainage
    kingdom: Kingdom
    height: Range # Meters
    roots: Range # Meters
    water: Water
    latin: str
    name: str
    pH: Range

    def __init__(self, **kwargs):
        defaults: Dict[str, object] = {
            'sunlight': Sunlight.LIGHT_SHADE,
            'drainage': Drainage.WELL_DRAINED,
            'kingdom': Kingdom.PLANT,
            'water': Water.MODERATE,
            'height': (1.0, 1.0),
            'roots': (0.2, 0.2),
            'pH': (7.0, 7.0)
        }
        for k, v in defaults.items():
            setattr(self, k, kwargs[k] if k in kwargs else v)
        self.latin = kwargs['latin']
        self.name = kwargs['name']

    def __repr__(self) -> str:
        return f'{self.name} ({self.latin})'