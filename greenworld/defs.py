"""
This module houses the constant values used throughout Greenworld
"""

from enum import IntEnum, unique

# Constant representing the entire plant kingdom
PLANTAE = 0


@unique
class GrowthHabit(IntEnum):
    """
    All the different morphologies a plant can take
    """

    # non woody and non grass-like
    FORB = 0
    # Grass or grass-like
    GRAMINOID = 1
    # Actually two organisms living together
    LICHENOUS = 2
    # Terrestrial, like a moss or something
    NONVASCULAR = 3
    # Perennial woody plant below 5 meters
    SHRUB = 4
    # Smaller shrub under 1 meter
    SUBSHRUB = 5
    # Perennial woody plant, over 5 meters
    TREE = 6
    # Plant with long stems, woody or herbaceous
    VINE = 7


@unique
class Sun(IntEnum):
    """
    A plant's preferred levels of sunlight
    """

    # 0 - 2 hours a day
    FULL_SHADE = 0
    # 2 - 6 hours a day
    PARTIAL_SUN = 1
    # 6 - 8 hours a day
    FULL_SUN = 2


@unique
class Soil(IntEnum):
    """
    A plant's preferred soil type
    """

    SAND = 1
    CLAY = 2
    SILT = 4
    LOAM = 8


@unique
class Drainage(IntEnum):
    """
    A plant's preferred soil drainage
    """

    # Water removed very rapidly, soil has a coarse texture
    EXCESSIVELY_DRAINED = 6
    # Water removed rapidly, internal water is very deep in the soil
    SOMEWHAT_EXCESSIVELY_DRAINED = 5
    # Water removed readily, internal water is deep in the soil
    WELL_DRAINED = 4
    # Water removed somewhat slowly during parts of the year, internal water moderately deep
    MODERATELY_WELL_DRAINED = 3
    # Water removed slowly, soil is wet at shallow depth for large portions of the season
    SOMEWHAT_POORLY_DRAINED = 2
    # Water removed slowly, soil remains wet for long periods
    POORLY_DRAINED = 1
    # Water removed so slowly that free water remains at or near surface for most of the season
    VERY_POORLY_DRAINED = 0


@unique
class Nitrogen(IntEnum):
    """
    A plant's interaction with nitrogen
    """

    # Adds nitrogen to the soil
    FIXER = 0
    # Has no remarkable relationship to soil nitrogen
    NEUTRAL = 1
    # Requires relatively high levels of nitrogen
    HEAVY = 2


@unique
class Ecology(IntEnum):
    """
    All the ways Greenworld models ecological relationships
    """

    # The plant species thwarts the target plant or non-plant species
    NEGATIVE_ALLELOPATHY = 0
    # The plant species benefits the target plant or non-plant species
    POSITIVE_ALLELOPATHY = 1
    # The plant species does not poison nor benefit the target plant or non-plant species
    NO_ALLELOPATHY = 2
    # The non-plant species causes some disease in the plant species
    PATHOGEN = 3
    # The non-plant species preys upon the plant species
    PREDATOR = 4
    # The non-plant species spreads the seeds of the plant species
    SEED_DISPERSER = 5
    # The non-plant species pollinates the plant species
    POLLINATOR = 6
