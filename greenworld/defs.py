from enum import IntEnum, unique

@unique
class GrowthHabit(IntEnum):
    # non woody and non grass-like
    FORB        = 0
    # Grass or grass-like
    GRAMINOID   = 1
    # Actually two organisms living together
    LICHENOUS   = 2
    # Terrestrial, like a moss or something
    NONVASCULAR = 3
    # Perennial woody plant below 5 meters
    SHRUB       = 4
    # Smaller shrub under 1 meter
    SUBSHRUB    = 5
    # Perennial woody plant, over 5 meters
    TREE        = 6
    # Plant with long stems, woody or herbaceous
    VINE        = 7

@unique
class Sun(IntEnum):
    FULL_SHADE  = 0
    PARTIAL_SUN = 1
    # 6 - 8 hours a day
    FULL_SUN    = 2

@unique
class Soil(IntEnum):
    SAND = 0
    CLAY = 1
    SILT = 2
    LOAM = 3

@unique
class Drainage(IntEnum):
    # Water removed very rapidly, soil has a coarse texture
    EXCESSIVELY_DRAINED          = 6
    # Water removed rapidly, internal water is very deep in the soil
    SOMEWHAT_EXCESSIVELY_DRAINED = 5
    # Water removed readily, internal water is deep in the soil
    WELL_DRAINED                 = 4
    # Water removed somewhat slowly during parts of the year, internal water moderately deep
    MODERATELY_WELL_DRAINED      = 3
    # Water removed slowly, soil is wet at shallow depth for large portions of the season
    SOMEWHAT_POORLY_DRAINED      = 2
    # Water removed slowly, soil remains wet for long periods
    POORLY_DRAINED               = 1
    # Water removed so slowly that free water remains at or near surface for most of the season
    VERY_POORLY_DRAINED          = 0

@unique
class Nitrogen(IntEnum):
    # Adds nitrogen to the soil
    FIXER   = 0
    # Has no remarkable relationship to soil nitrogen
    NEUTRAL = 1
    # Requires relatively high levels of nitrogen
    HEAVY   = 2

@unique
class SpeciesRelation(IntEnum):
    # The non-plant species causes some disease in the plant species
    PATHOGEN       = 0
    # The non-plant species preys upon the plant species
    PREDATOR       = 1
    # The non-plant species spreads the seeds of the plant species
    SEED_DISPERSER = 2
    # The non-plant species pollinates the plant species
    POLLINATOR     = 3

@unique
class AlleloRelation(IntEnum):
    # The plant secretes this allelochemical into the rhizosphere
    SECRETES = 0
    # The plant is negatively affected by this allelochemical
    NEGATIVE = 1
    # The plant is positively affected by this allelochemical
    POSITIVE = 2
