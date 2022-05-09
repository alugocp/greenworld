from typing import Tuple
from enum import Enum

Range = Tuple[float, float]

class Drainage(Enum):
    EXCESSIVELY_DRAINED          = 6
    SOMEWHAT_EXCESSIVELY_DRAINED = 5
    WELL_DRAINED                 = 4
    MODERATELY_WELL_DRAINED      = 3
    SOMEWHAT_POORLY_DRAINED      = 2
    POORLY_DRAINED               = 1
    VERY_POORLY_DRAINED          = 0

class Sunlight(Enum):
    FULL_SUN      = 4
    LIGHT_SHADE   = 3
    PARTIAL_SHADE = 2
    FULL_SHADE    = 1
    DENSE_SHADE   = 0

class Water(Enum):
    HIGH     = 3    # Water
    MODERATE = 2    # Wet
    LOW      = 1    # Moist
    VERY_LOW = 0    # Dry

class Kingdom(Enum):
    FUNGI = 'fungi'
    PLANT = 'plant'