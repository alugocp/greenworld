# This module contains the core logic for the Greenworld algorithm.
from defs import (
    GrowthHabit,
    Sun
)
from utils import (
    new_report,
    get_report,
    taller_first,
    mirrored,
    ensure,
    rule
)

@rule
@mirrored
@ensure(both = ['sun', 'growth_habit'], fields1 = ['fruit_weight'])
def can_vine_climb(plant1, plant2):
    if plant1.sun == Sun.FULL_SUN and plant1.growth_habit == GrowthHabit.VINE and plant1.fruit_weight < 0.1 and plant2.sun == Sun.FULL_SUN and plant2.growth_habit in [GrowthHabit.GRAMINOID, GrowthHabit.FORB]:
        return f'{plant1.name} can climb up {plant2.name} for direct sunlight'

@rule
@taller_first
@ensure(fields2 = ['sun'])
def space_for_sunlight(plant1, plant2):
    if plant2.sun == Sun.FULL_SUN:
        return f'{plant2.name} should be far enough away from {plant1.name} to get direct sunlight'
    elif plant2.sun == Sun.PARTIAL_SUN:
        return f'{plant2.name} should be just far enough from {plant1.name} to get partial sunlight'
    return f'{plant2.name} should be close enough to {plant1.name} to get full shade'

@rule
@ensure(both = ['growth_habit'])
def vine_spacing(plant1, plant2):
    if plant1.growth_habit == GrowthHabit.VINE and plant2.growth_habit == GrowthHabit.VINE:
        return f'{plant1.name} should be placed far enough from {plant2.name} so both vines can spread'