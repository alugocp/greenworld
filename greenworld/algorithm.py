# This module contains the core logic for the Greenworld algorithm.
import math
from greenworld.schema import (
    other_species_table,
    ecology_other_table,
    ecology_plant_table
)
from greenworld.defs import (
    PLANTAE,
    GrowthHabit,
    Nitrogen,
    Drainage,
    Ecology,
    Sun
)
from greenworld.utils import (
    reduce_intervals,
    get_connection,
    overlaps,
    taller_first,
    mirrored,
    ensure,
    rule
)

# pylint: disable=inconsistent-return-statements

# Rules that will absolutely return a range value
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
@ensure(fields1=['height'], fields2 = ['sun'])
def space_for_sunlight(plant1, plant2):
    middle = float(plant1.spread.upper if plant1.spread else plant1.height.upper / 2)
    if plant2.sun == Sun.FULL_SUN:
        return (middle * 1.25, middle * 2), f'{plant2.name} should be far enough away from {plant1.name} to get direct sunlight'
    if plant2.sun == Sun.PARTIAL_SUN:
        return (middle * 0.75, middle * 1.25), f'{plant2.name} should be just far enough from {plant1.name} to get partial sunlight'
    return (0, middle * 0.75), f'{plant2.name} should be close enough to {plant1.name} to get full shade'

@rule
@ensure(both = ['growth_habit'])
def vine_spacing(plant1, plant2):
    if plant1.growth_habit == GrowthHabit.VINE and plant2.growth_habit == GrowthHabit.VINE:
        dist = math.sqrt(math.pow(24 / math.sqrt(2), 2) + math.pow(12, 2)) * 0.0254 # Distance between beans and squash in three sisters
        if plant1['spread'] and plant2['spread']:
            dist = (plant1.spread.upper + plant2.spread.upper) / 2
        return (dist, dist * 2), f'{plant1.name} should be placed far enough from {plant2.name} so both vines can spread'

@rule
@ensure(both = ['spread'])
def add_spread(plant1, plant2):
    dist = (plant1.spread.lower + plant2.spread.lower, plant1.spread.upper + plant2.spread.upper)
    return dist, f'{plant1.name} and {plant2.name} should both have enough space to grow horizontally'

# Rules that may return a range value
@rule
@mirrored
@ensure(both = ['nitrogen'])
def nitrogen_relationship(plant1, plant2):
    if plant1.nitrogen == Nitrogen.FIXER and plant2.nitrogen == Nitrogen.HEAVY:
        dist1 = reduce_intervals(plant1, plant2, 'spread', 'upper') / 2
        dist2 = reduce_intervals(plant1, plant2, 'root_spread', 'lower')
        dist = None if dist1 == 0 and dist2 == 0 else (dist1, dist2)
        return dist, f'{plant1.name} can fix soil nitrogen for {plant2.name}'
    if plant1.nitrogen == Nitrogen.HEAVY and plant2.nitrogen == Nitrogen.HEAVY:
        dist = reduce_intervals(plant1, plant2, 'root_spread', 'upper')
        dist = None if dist == 0 else (dist, dist * 2)
        return dist, f'{plant1.name} and {plant2.name} may compete for soil nitrogen'

@rule
@mirrored
def allelopathy_relationship(plant1, plant2):
    con = get_connection()
    relationship = None

    # Grab plant2's family's ID (if it exists)
    stmt = other_species_table.select().where(other_species_table.c['species'] == plant2.family)
    plant2_family_id = con.execute(stmt).fetchone()
    plant2_family_id = plant2_family_id[0] if plant2_family_id else None

    # Calculate exact relationship dynamic
    stmt = ecology_other_table.select().where(ecology_other_table.c['plant'] == plant1.id)
    for row in con.execute(stmt).mappings():
        if (relationship is None and row['non_plant'] == PLANTAE) or row['non_plant'] == plant2_family_id:
            relationship = row['relationship']
    stmt = ecology_plant_table.select().where(ecology_plant_table.c['plant'] == plant1.id)
    for row in con.execute(stmt).mappings():
        if row['target'] == plant2.id:
            relationship = row['relationship']

    # Return based on uncovered relationship
    if relationship == Ecology.POSITIVE_ALLELOPATHY:
        dist1 = reduce_intervals(plant1, plant2, 'spread', 'upper') / 2
        dist2 = reduce_intervals(plant1, plant2, 'root_spread', 'lower')
        dist = None if dist1 == 0 and dist2 == 0 else (dist1, dist2)
        return dist, f'{plant1.name} is a positive allelopath for {plant2.name}'
    if relationship == Ecology.NEGATIVE_ALLELOPATHY:
        dist = reduce_intervals(plant1, plant2, 'root_spread', 'upper')
        dist = None if dist == 0 else (dist, dist * 2)
        return dist, f'{plant1.name} is a negative allelopath for {plant2.name}'

@rule
@mirrored
@ensure(both = ['root_depth'], fields2 = ['drainage'])
def roots_break_up_soil(plant1, plant2):
    if plant1.root_depth > plant2.root_depth and plant2.drainage >= Drainage.WELL_DRAINED:
        dist1 = reduce_intervals(plant1, plant2, 'spread', 'upper') / 2
        dist2 = reduce_intervals(plant1, plant2, 'root_spread', 'lower')
        dist = None if dist1 == 0 and dist2 == 0 else (dist1, dist2)
        return dist, f'{plant1.name} can break up the soil for {plant2.name} to get better drainage'

# Rules that will absolutely not return a range value
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

# pylint: enable=inconsistent-return-statements
