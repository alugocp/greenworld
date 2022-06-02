from typing import Tuple
from enum import Enum

Range = Tuple[float, float]

# The preferred drainage level of a plant's soil
class Drainage(Enum):
    EXCESSIVELY_DRAINED          = 6
    SOMEWHAT_EXCESSIVELY_DRAINED = 5
    WELL_DRAINED                 = 4
    MODERATELY_WELL_DRAINED      = 3
    SOMEWHAT_POORLY_DRAINED      = 2
    POORLY_DRAINED               = 1
    VERY_POORLY_DRAINED          = 0

# How much sunlight a plant requires
class Sunlight(Enum):
    FULL_SUN      = 4
    LIGHT_SHADE   = 3
    PARTIAL_SHADE = 2
    FULL_SHADE    = 1
    DENSE_SHADE   = 0

# How much water a plant requires
class Water(Enum):
    HIGH     = 3    # Water
    MODERATE = 2    # Wet
    LOW      = 1    # Moist
    VERY_LOW = 0    # Dry

# Taxonomic level
class Kingdom(Enum):
    FUNGI = 'fungi'
    PLANT = 'plant'

# The growth habit displayed by a plant
class GrowthHabit(Enum):
    HERB        = 0
    GRAMINOID   = 1
    LICHENOUS   = 2
    NONVASCULAR = 3
    SHRUB       = 4
    SUBSHRUB    = 5
    TREE        = 6
    VINE        = 7

# The general lifespan duration of a plant
class Duration(Enum):
    ANNUAL    = 0
    BIENNIAL  = 1
    PERENNIAL = 2
