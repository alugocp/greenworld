from typing import Tuple, List
from enum import Enum, unique
from math import floor

# The preferred drainage level of a plant's soil
@unique
class Drainage(Enum):
    EXCESSIVELY_DRAINED          = 6
    SOMEWHAT_EXCESSIVELY_DRAINED = 5
    WELL_DRAINED                 = 4
    MODERATELY_WELL_DRAINED      = 3
    SOMEWHAT_POORLY_DRAINED      = 2
    POORLY_DRAINED               = 1
    VERY_POORLY_DRAINED          = 0

# How much sunlight a plant requires
@unique
class Sunlight(Enum):
    FULL_SUN      = 4 # 6 - 8 hours a day
    LIGHT_SHADE   = 3
    PARTIAL_SHADE = 2
    FULL_SHADE    = 1
    DENSE_SHADE   = 0

# How much water a plant requires
@unique
class Water(Enum):
    HIGH     = 3 # Water
    MODERATE = 2 # Wet
    LOW      = 1 # Moist
    VERY_LOW = 0 # Dry

# Taxonomic level
@unique
class Kingdom(Enum):
    FUNGI = 'fungi'
    PLANT = 'plant'

# The growth habit displayed by a plant
@unique
class GrowthHabit(Enum):
    HERB        = 0 # non woody and non grass-like
    GRAMINOID   = 1 # Grass or grass-like
    LICHENOUS   = 2 # Actually two organisms living together
    NONVASCULAR = 3 # Terrestrial, like a moss or something
    SHRUB       = 4 # Perennial woody plant below 5 meters
    SUBSHRUB    = 5 # Smaller shrub under 1 meter
    TREE        = 6 # Perennial woody plant, over 5 meters
    VINE        = 7 # Plant with long stems, woody or herbaceous

# The general lifespan duration of a plant
@unique
class Duration(Enum):
    ANNUAL    = 0 # Lifecycle lasts 1 year
    BIENNIAL  = 1 # Lifecycle lasts 2 years
    PERENNIAL = 2 # Can get older than just 2 years

# The type of recommended distance between two plants
@unique
class SuggestionType(Enum):
    SPATIAL  = 0 # Defines how far apart you should plant these crops
    TEMPORAL = 1 # Defines how long you should wait in between planting these crops

# Simple typedefs
Range = Tuple[float, float]
Suggestion = Tuple[SuggestionType, str]
SuggestedRange = Tuple[Suggestion, Range]
SuggestionSet = List[SuggestedRange]

# String conversion methods
def stringify_suggestion(s: Suggestion) -> str:
    dimension = 'temporal' if s[0] == SuggestionType.TEMPORAL else 'spatial'
    return f'{s[1]} ({dimension})'

def stringify_suggested_range(r: SuggestedRange) -> str:
    bot = floor(r[1][0] * 100) / 100
    top = floor(r[1][1] * 100) / 100
    return f'{stringify_suggestion(r[0])}: {bot} - {top}'
