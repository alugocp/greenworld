from enum import Enum, unique

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
