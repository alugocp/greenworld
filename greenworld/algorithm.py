# This module contains the core logic for the Greenworld algorithm.
import math
from greenworld.defs import (
    GrowthHabit,
    Nitrogen,
    Drainage,
    Sun
)
from greenworld.utils import (
    reduce_intervals,
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
    dist1 = 3 * 0.0254 / math.sqrt(2) # 45 degree angle with 3 inch hypotenuse
    dist2 = 6 * 0.0254 / math.sqrt(2) # 45 degree angle with 6 inch hypotenuse
    if plant1.sun == Sun.FULL_SUN and plant1.growth_habit == GrowthHabit.VINE and plant1.fruit_weight < threshold and plant2.sun == Sun.FULL_SUN and plant2.growth_habit in [GrowthHabit.GRAMINOID, GrowthHabit.FORB]:
        return (dist1, dist2), f'{plant1.name} can climb up {plant2.name} for direct sunlight'

@rule
@taller_first
@ensure(both = ['spread'], fields1=['height'], fields2 = ['sun'])
def space_for_sunlight(plant1, plant2):
    if plant2.sun == Sun.FULL_SUN:
        dist1 = plant1.height.upper
        dist2 = (plant1.spread.upper + plant2.spread.upper) / 2
        return (dist1, dist2), f'{plant2.name} should be far enough away from {plant1.name} to get direct sunlight'
    if plant2.sun == Sun.PARTIAL_SUN:
        dist1 = (plant1.spread.lower + plant1.spread.upper) / 2
        dist2 = (plant1.spread.lower + plant1.spread.upper + plant2.spread.lower + plant2.spread.upper) / 4
        return (dist1, dist2), f'{plant2.name} should be just far enough from {plant1.name} to get partial sunlight'
    dist1 = plant2.spread.upper / 2
    dist2 = (plant1.spread.lower - plant2.spread.upper) / 2
    return (dist1, dist2), f'{plant2.name} should be close enough to {plant1.name} to get full shade'

@rule
@ensure(both = ['growth_habit'])
def vine_spacing(plant1, plant2):
    if plant1.growth_habit == GrowthHabit.VINE and plant2.growth_habit == GrowthHabit.VINE:
        dist = math.sqrt(math.pow(24 / math.sqrt(2), 2) + math.pow(12, 2)) * 0.0254 # Distance between beans and squash in three sisters
        if plant1['spread'] and plant2['spread']:
            dist = (plant1.spread.upper + plant2.spread.upper) / 2
        return (dist, dist * 2), f'{plant1.name} should be placed far enough from {plant2.name} so both vines can spread'

@rule
@mirrored
@ensure(both = ['nitrogen', 'root_spread'])
def nitrogen_relationship(plant1, plant2):
    if plant1.nitrogen == Nitrogen.FIXER and plant2.nitrogen == Nitrogen.HEAVY:
        dist1 = reduce_intervals(plant1, plant2, 'spread', 'upper') / 2
        dist2 = plant1.root_spread.lower + plant2.root_spread.lower
        return (dist1, dist2), f'{plant1.name} can fix soil nitrogen for {plant2.name}'
    if plant1.nitrogen == Nitrogen.HEAVY and plant2.nitrogen == Nitrogen.HEAVY:
        dist = plant1.root_spread.upper + plant2.root_spread.upper
        return (dist, dist * 2), f'{plant1.name} and {plant2.name} may compete for soil nitrogen'

@rule
@ensure(both = ['temperature'])
def match_temperature(plant1, plant2):
    if not overlaps(plant1.temperature, plant2.temperature):
        return None, f'{plant1.name} and {plant2.name} prefer different temperature ranges'

@rule
@ensure(both = ['soil'])
def match_soil(plant1, plant2):
    if plant1.soil != plant2.soil:
        return None, f'{plant1.name} and {plant2.name} prefer different types of soil'

@rule
@ensure(both = ['pH'])
def match_ph(plant1, plant2):
    if not overlaps(plant1.pH, plant2.pH):
        return None, f'{plant1.name} and {plant2.name} prefer different pH ranges'

@rule
@ensure(both = ['drainage'])
def match_drainage(plant1, plant2):
    if plant1.drainage != plant2.drainage:
        return None, f'{plant1.name} and {plant2.name} prefer different soil drainage'

@rule
@mirrored
@ensure(fields1 = ['nitrogen', 'growth_habit'])
def large_vines_shade_weeds(plant1, plant2):
    if plant1.nitrogen == Nitrogen.HEAVY and plant1.growth_habit == GrowthHabit.VINE:
        return None, f'{plant1.name} can shade out weeds around {plant2.name}'

@rule
@mirrored
@ensure(both = ['root_depth'], fields2 = ['drainage'])
def roots_break_up_soil(plant1, plant2):
    if plant1.root_depth > plant2.root_depth and plant2.drainage >= Drainage.WELL_DRAINED:
        dist1 = reduce_intervals(plant1, plant2, 'spread', 'upper') / 2
        dist2 = reduce_intervals(plant1, plant2, 'root_spread', 'lower')
        dist = None if dist1 == 0 and dist2 == 0 else (dist1, dist2)
        return dist, f'{plant1.name} can break up the soil for {plant2.name} to get better drainage'

# pylint: enable=inconsistent-return-statements
