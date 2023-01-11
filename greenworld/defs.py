from enum import IntEnum, unique

@unique
class GrowthHabit(IntEnum):
    HERB        = 0 # non woody and non grass-like
    GRAMINOID   = 1 # Grass or grass-like
    LICHENOUS   = 2 # Actually two organisms living together
    NONVASCULAR = 3 # Terrestrial, like a moss or something
    SHRUB       = 4 # Perennial woody plant below 5 meters
    SUBSHRUB    = 5 # Smaller shrub under 1 meter
    TREE        = 6 # Perennial woody plant, over 5 meters
    VINE        = 7 # Plant with long stems, woody or herbaceous

@unique
class Sun(IntEnum):
    FULL_SHADE  = 0
    PARTIAL_SUN = 1
    FULL_SUN    = 2 # 6 - 8 hours a day

@unique
class Soil(IntEnum):
    SAND = 0
    CLAY = 1
    SILT = 2
    LOAM = 3

@unique
class Drainage(IntEnum):
    EXCESSIVELY_DRAINED          = 6 # Water removed very rapidly, soil has a coarse texture
    SOMEWHAT_EXCESSIVELY_DRAINED = 5 # Water removed rapidly, internal water is very deep in the soil
    WELL_DRAINED                 = 4 # Water removed readily, internal water is deep in the soil
    MODERATELY_WELL_DRAINED      = 3 # Water removed somewhat slowly during parts of the year, internal water moderately deep
    SOMEWHAT_POORLY_DRAINED      = 2 # Water removed slowly, soil is wet at shallow depth for large portions of the season
    POORLY_DRAINED               = 1 # Water removed slowly, soil remains wet for long periods
    VERY_POORLY_DRAINED          = 0 # Water removed so slowly that free water remains at or near surface for most of the season