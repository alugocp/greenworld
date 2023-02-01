# This module contains the core logic for the Greenworld algorithm.
from defs import (
    GrowthHabit,
    Nitrogen,
    Drainage,
    Sun
)
from utils import (
    overlaps,
    taller_first,
    mirrored,
    ensure,
    rule
)

# pylint: disable=inconsistent-return-statements

@rule
@mirrored
@ensure(both = ['sun', 'growth_habit'], fields1 = ['fruit_weight'])
def can_vine_climb(plant1, plant2):
    threshold = 45.359237 # 0.1 lbs
    if plant1.sun == Sun.FULL_SUN and plant1.growth_habit == GrowthHabit.VINE and plant1.fruit_weight < threshold and plant2.sun == Sun.FULL_SUN and plant2.growth_habit in [GrowthHabit.GRAMINOID, GrowthHabit.FORB]:
        return f'{plant1.name} can climb up {plant2.name} for direct sunlight'

@rule
@taller_first
@ensure(fields2 = ['sun'])
def space_for_sunlight(plant1, plant2):
    if plant2.sun == Sun.FULL_SUN:
        return f'{plant2.name} should be far enough away from {plant1.name} to get direct sunlight'
    if plant2.sun == Sun.PARTIAL_SUN:
        return f'{plant2.name} should be just far enough from {plant1.name} to get partial sunlight'
    return f'{plant2.name} should be close enough to {plant1.name} to get full shade'

@rule
@ensure(both = ['growth_habit'])
def vine_spacing(plant1, plant2):
    if plant1.growth_habit == GrowthHabit.VINE and plant2.growth_habit == GrowthHabit.VINE:
        return f'{plant1.name} should be placed far enough from {plant2.name} so both vines can spread'

@rule
@mirrored
@ensure(both = ['nitrogen'])
def nitrogen_relationship(plant1, plant2):
    if plant1.nitrogen == Nitrogen.FIXER and plant2.nitrogen == Nitrogen.HEAVY:
        return f'{plant1.name} can fix soil nitrogen for {plant2.name}'
    if plant1.nitrogen == Nitrogen.HEAVY and plant2.nitrogen == Nitrogen.HEAVY:
        return f'{plant1.name} and {plant2.name} may compete for soil nitrogen'

@rule
@ensure(both = ['temperature'])
def match_temperature(plant1, plant2):
    if not overlaps(plant1.temperature, plant2.temperature):
        return f'{plant1.name} and {plant2.name} prefer different temperature ranges'

@rule
@ensure(both = ['soil'])
def match_soil(plant1, plant2):
    if plant1.soil != plant2.soil:
        return f'{plant1.name} and {plant2.name} prefer different types of soil'

@rule
@ensure(both = ['pH'])
def match_ph(plant1, plant2):
    if not overlaps(plant1.pH, plant2.pH):
        return f'{plant1.name} and {plant2.name} prefer different pH ranges'

@rule
@ensure(both = ['drainage'])
def match_drainage(plant1, plant2):
    if plant1.drainage != plant2.drainage:
        return f'{plant1.name} and {plant2.name} prefer different soil drainage'

@rule
@mirrored
@ensure(fields1 = ['nitrogen', 'growth_habit'])
def large_vines_shade_weeds(plant1, plant2):
    if plant1.nitrogen == Nitrogen.HEAVY and plant1.growth_habit == GrowthHabit.VINE:
        return f'{plant1.name} can shade out weeds around {plant2.name}'

@rule
@mirrored
@ensure(both = ['root_depth'], fields2 = ['drainage'])
def roots_break_up_soil(plant1, plant2):
    if plant1.root_depth > plant2.root_depth and plant2.drainage >= Drainage.WELL_DRAINED:
        return f'{plant1.name} can break up the soil for {plant2.name} to get better drainage'

# pylint: enable=inconsistent-return-statements
