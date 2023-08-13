# This module contains the core logic for the Greenworld algorithm.
import math
import sqlalchemy
from greenworld.lib.utils import AlgorithmUtils
from greenworld.lib.orm import (
    other_species_table,
    ecology_other_table,
    ecology_plant_table,
    MAX_PLANTING_RANGE
)
from greenworld.lib.defs import (
    PLANTAE,
    GrowthHabit,
    Nitrogen,
    Drainage,
    Ecology,
    Sun
)

# pylint: disable=inconsistent-return-statements

def build(utils: AlgorithmUtils) -> None:

    # Rules that will absolutely return a range value
    @utils.rule()
    @utils.mirrored()
    @utils.ensure(both = ['sun', 'growth_habit'], fields1 = ['length'], fields2 = ['height'])
    def can_vine_climb(plant1, plant2):
        dist = 6 * 0.0254 / math.sqrt(2) # 45 degree angle with 6 inch hypotenuse (based on three sisters)
        direct = f'{plant1.name} can climb up {plant2.name} for direct sunlight'
        indirect = f'{plant1.name} can climb up {plant2.name} for indirect sunlight'
        if plant1.growth_habit == GrowthHabit.VINE and plant1.length.lower <= plant2.height.upper:
            if (plant1.lightweight and plant2.growth_habit in [GrowthHabit.GRAMINOID, GrowthHabit.FORB]):
                if plant1.sun == Sun.FULL_SUN and plant2.sun == Sun.FULL_SUN:
                    return (0, dist), direct
                if plant1.sun == Sun.PARTIAL_SUN and plant2.sun == Sun.PARTIAL_SUN:
                    return (0, dist), indirect

            if (plant2.growth_habit == GrowthHabit.TREE and plant1.sun == Sun.PARTIAL_SUN and plant2.sun == Sun.FULL_SUN) or \
            (plant2.growth_habit in [GrowthHabit.SHRUB, GrowthHabit.SUBSHRUB] and plant1.sun == plant2.sun):
                close = float(plant1.spread.lower / 2 if plant1.spread else dist) + float(plant2.spread.upper / 2 if plant2.spread else dist) + dist
                far = float(plant1.spread.upper / 2 if plant1.spread else dist) + float(plant2.spread.upper / 2 if plant2.spread else dist) + dist
                return (close, far), indirect

    @utils.rule()
    @utils.taller_first()
    @utils.ensure(fields1 = ['height'], fields2 = ['sun'])
    def space_for_sunlight(plant1, plant2):
        if utils.is_rule_included('can_vine_climb'):
            return None
        if plant1.height.lower > 1/3:
            middle = float(plant1.spread.upper if plant1.spread else plant1.height.upper / 2)
            if plant2.sun == Sun.FULL_SUN:
                return (middle * 1.25, MAX_PLANTING_RANGE), f'{plant2.name} should be far enough away from {plant1.name} to get direct sunlight'
            if plant2.sun == Sun.PARTIAL_SUN:
                return (middle * 0.75, middle * 1.25), f'{plant2.name} should be just far enough from {plant1.name} to get partial sunlight'
            return (0, middle * 0.75), f'{plant2.name} should be close enough to {plant1.name} to get full shade'

    @utils.rule()
    @utils.ensure(both = ['growth_habit'])
    def vine_spacing(plant1, plant2):
        if plant1.growth_habit == GrowthHabit.VINE and plant2.growth_habit == GrowthHabit.VINE:
            close = math.sqrt(math.pow(24 / math.sqrt(2), 2) + math.pow(12, 2)) * 0.0254 # Distance between beans and squash in three sisters
            far = MAX_PLANTING_RANGE
            if plant1['spread'] and plant2['spread']:
                close = (plant1.spread.lower + plant2.spread.lower) / 2
                far = (plant1.spread.upper + plant2.spread.upper) / 2
            return (close, far), f'{plant1.name} should be placed far enough from {plant2.name} so both vines can spread'

    @utils.rule()
    @utils.ensure(both = ['spread', 'height'])
    def add_spread(plant1, plant2):
        if utils.overlaps(plant1.height, plant2.height):
            dist = ((plant1.spread.lower + plant2.spread.lower) / 2, MAX_PLANTING_RANGE)
            return dist, f'{plant1.name} and {plant2.name} should both have enough space to grow horizontally'

    # Rules that may return a range value
    @utils.rule()
    @utils.mirrored()
    @utils.ensure(both = ['nitrogen'])
    def nitrogen_relationship(plant1, plant2):
        if plant1.nitrogen == Nitrogen.FIXER and plant2.nitrogen == Nitrogen.HEAVY:
            dist = utils.reduce_intervals(plant1, plant2, 'root_spread', 'lower') / 4
            dist = None if dist == 0 else (0, dist)
            return dist, f'{plant1.name} can fix soil nitrogen for {plant2.name}'
        if plant1.nitrogen == Nitrogen.HEAVY and plant2.nitrogen == Nitrogen.HEAVY:
            dist = utils.reduce_intervals(plant1, plant2, 'root_spread', 'lower') / 4
            dist = None if dist == 0 else (dist, MAX_PLANTING_RANGE)
            return dist, f'{plant1.name} and {plant2.name} may compete for soil nitrogen'

    @utils.rule()
    def allelopathy_relationship(plant1, plant2):
        con = utils.get_connection()
        relationship = None

        # Hacked mirroring to get up to two results
        if plant1.id < plant2.id:
            # pylint: disable-next=arguments-out-of-order
            allelopathy_relationship(plant2, plant1)

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
            dist = utils.reduce_intervals(plant1, plant2, 'root_spread', 'lower') / 4
            dist = None if dist == 0 else (0, dist)
            return dist, f'{plant1.name} is a positive allelopath for {plant2.name}'
        if relationship == Ecology.NEGATIVE_ALLELOPATHY:
            dist = utils.reduce_intervals(plant1, plant2, 'root_spread', 'upper') / 4
            dist = None if dist == 0 else (dist, MAX_PLANTING_RANGE)
            return dist, f'{plant1.name} is a negative allelopath for {plant2.name}'

    @utils.rule()
    @utils.ensure(both = ['soil'])
    def match_soil(plant1, plant2):
        if plant1.soil != plant2.soil:
            dist = utils.reduce_intervals(plant1, plant2, 'root_spread', 'upper') / 2
            dist = None if dist == 0 else (dist, MAX_PLANTING_RANGE)
            return dist, f'{plant1.name} and {plant2.name} prefer different types of soil'

    @utils.rule()
    @utils.ensure(both = ['pH'])
    def match_ph(plant1, plant2):
        if not utils.overlaps(plant1.pH, plant2.pH):
            dist = utils.reduce_intervals(plant1, plant2, 'root_spread', 'upper') / 2
            dist = None if dist == 0 else (dist, MAX_PLANTING_RANGE)
            return dist, f'{plant1.name} and {plant2.name} prefer different pH ranges'

    @utils.rule()
    @utils.ensure(both = ['drainage'])
    def match_drainage(plant1, plant2):
        if plant1.drainage != plant2.drainage:
            dist = utils.reduce_intervals(plant1, plant2, 'root_spread', 'upper') / 2
            dist = None if dist == 0 else (dist, MAX_PLANTING_RANGE)
            return dist, f'{plant1.name} and {plant2.name} prefer different soil drainage'

    @utils.rule()
    @utils.mirrored()
    @utils.ensure(both = ['growth_habit'], fields1 = ['nitrogen'])
    def large_vines_shade_weeds(plant1, plant2):
        if plant1.nitrogen == Nitrogen.HEAVY and plant1.growth_habit == GrowthHabit.VINE and plant2.growth_habit != GrowthHabit.VINE:
            dist = None
            if plant1.length is not None and plant1.spread is not None:
                value1 = plant1.spread.lower
                value2 = plant1.length.lower / 4
                dist = (value1 if value1 < value2 else value2, value1 if value1 > value2 else value2)
            return dist, f'{plant1.name} can shade out weeds around {plant2.name}'

    @utils.rule()
    def ecological_intersection(plant1, plant2):
        if plant1.species == plant2.species:
            return None
        con = utils.get_connection()
        e1 = ecology_other_table.alias('e1')
        e2 = ecology_other_table.alias('e2')
        stmt = sqlalchemy.select(
            other_species_table.c['name'],
            e1.c['relationship'].label('r1'),
            e2.c['relationship'].label('r2')
        ).\
            join(e2, e1.c['non_plant'] == e2.c['non_plant']).\
            join(other_species_table, other_species_table.c['id'] == e1.c['non_plant']).\
            where(sqlalchemy.and_(e1.c['plant'] == plant1.id, e2.c['plant'] == plant2.id)).\
            distinct()
        for result in con.execute(stmt):
            non_plant, r1, r2 = result
            p1 = plant1.name
            p2 = plant2.name
            lower_bound = float(utils.reduce_intervals(plant1, plant2, 'spread', 'lower')) / 2
            upper_bound = float(utils.reduce_intervals(plant1, plant2, 'spread', 'upper')) / 2
            close = None if upper_bound == 0 else (lower_bound, upper_bound)
            far = None if upper_bound == 0 else (upper_bound * 2, MAX_PLANTING_RANGE)
            pair = {
                Ecology.NEGATIVE_ALLELOPATHY: {
                    Ecology.NEGATIVE_ALLELOPATHY: (None, f'{p1} and {p2} are both negative allelopaths for {non_plant}'),
                    Ecology.POSITIVE_ALLELOPATHY: (far, f'{p1} is a negative allelopath and {p2} is a positive allelopath for {non_plant}'),
                    Ecology.NO_ALLELOPATHY: None,
                    Ecology.PATHOGEN: (close, f'{p1} is a negative allelopath for {p2}\'s pathogenic species {non_plant}'),
                    Ecology.PREDATOR: (close, f'{p1} is a negative allelopath for {p2}\'s predator species {non_plant}'),
                    Ecology.SEED_DISPERSER: (far, f'{p1} is a negative allelopath for {p2}\'s seed disperser species {non_plant}'),
                    Ecology.POLLINATOR: (far, f'{p1} is a negative allelopath for {p2}\'s pollinator species {non_plant}')
                },
                Ecology.POSITIVE_ALLELOPATHY: {
                    Ecology.NEGATIVE_ALLELOPATHY: (far, f'{p1} is a positive allelopath and {p2} is a negative allelopath for {non_plant}'),
                    Ecology.POSITIVE_ALLELOPATHY: (close, f'{p1} and {p2} are both positive allelopaths for {non_plant}'),
                    Ecology.NO_ALLELOPATHY: None,
                    Ecology.PATHOGEN: (far, f'{p1} is a positive allelopath for {p2}\'s pathogenic species {non_plant}'),
                    Ecology.PREDATOR: (far, f'{p1} is a positive allelopath for {p2}\'s predator species {non_plant}'),
                    Ecology.SEED_DISPERSER: (close, f'{p1} is a positive allelopath for {p2}\'s seed disperser species {non_plant}'),
                    Ecology.POLLINATOR: (close, f'{p1} is a positive allelopath for {p2}\'s pollinator species {non_plant}')
                },
                Ecology.NO_ALLELOPATHY: {
                    Ecology.NEGATIVE_ALLELOPATHY: None,
                    Ecology.POSITIVE_ALLELOPATHY: None,
                    Ecology.NO_ALLELOPATHY: None,
                    Ecology.PATHOGEN: None,
                    Ecology.PREDATOR: None,
                    Ecology.SEED_DISPERSER: None,
                    Ecology.POLLINATOR: None
                },
                Ecology.PATHOGEN: {
                    Ecology.NEGATIVE_ALLELOPATHY: (close, f'{p2} is a negative allelopath for {p1}\'s pathogenic species {non_plant}'),
                    Ecology.POSITIVE_ALLELOPATHY: (far, f'{p2} is a positive allelopath for {p1}\'s pathogenic species {non_plant}'),
                    Ecology.NO_ALLELOPATHY: None,
                    Ecology.PATHOGEN: (far, f'{p1} and {p2} have a common pathogenic species {non_plant}'),
                    Ecology.PREDATOR: (far, f'{p1}\'s pathogenic species {non_plant} is a predator for {p2}'),
                    Ecology.SEED_DISPERSER: (far, f'{p1}\'s pathogenic species {non_plant} is a seed disperser for {p2}'),
                    Ecology.POLLINATOR: (far, f'{p1}\'s pathogenic species {non_plant} is a pollinator for {p2}')
                },
                Ecology.PREDATOR: {
                    Ecology.NEGATIVE_ALLELOPATHY: (close, f'{p2} is a negative allelopath for {p1}\'s predator species {non_plant}'),
                    Ecology.POSITIVE_ALLELOPATHY: (far, f'{p2} is a positive allelopath for {p1}\'s predator species {non_plant}'),
                    Ecology.NO_ALLELOPATHY: None,
                    Ecology.PATHOGEN: (far, f'{p1}\'s predator species {non_plant} is a pathogen for {p2}'),
                    Ecology.PREDATOR: (close, f'{p1} and {p2} have a common predator species {non_plant}'),
                    Ecology.SEED_DISPERSER: (close, f'{p1}\'s predator species {non_plant} is a seed disperser for {p2}'),
                    Ecology.POLLINATOR: (close, f'{p1}\'s predator species {non_plant} is a pollinator for {p2}')
                },
                Ecology.SEED_DISPERSER: {
                    Ecology.NEGATIVE_ALLELOPATHY: (far, f'{p2} is a negative allelopath for {p1}\'s seed disperser species {non_plant}'),
                    Ecology.POSITIVE_ALLELOPATHY: (close, f'{p2} is a positive allelopath for {p1}\'s seed disperser species {non_plant}'),
                    Ecology.NO_ALLELOPATHY: None,
                    Ecology.PATHOGEN: (far, f'{p1}\'s seed disperser species {non_plant} is a pathogen for {p2}'),
                    Ecology.PREDATOR: (close, f'{p1}\'s seed disperser species {non_plant} is a predator for {p2}'),
                    Ecology.SEED_DISPERSER: (close, f'{p1} and {p2} have a common seed disperser species {non_plant}'),
                    Ecology.POLLINATOR: (close, f'{p1}\'s seed disperser species {non_plant} is a pollinator for {p2}')
                },
                Ecology.POLLINATOR: {
                    Ecology.NEGATIVE_ALLELOPATHY: (far, f'{p2} is a negative allelopath for {p1}\'s pollinator species {non_plant}'),
                    Ecology.POSITIVE_ALLELOPATHY: (close, f'{p2} is a positive allelopath for {p1}\'s pollinator species {non_plant}'),
                    Ecology.NO_ALLELOPATHY: None,
                    Ecology.PATHOGEN: (far, f'{p1}\'s pollinator species {non_plant} is a pathogen for {p2}'),
                    Ecology.PREDATOR: (close, f'{p1}\'s pollinator species {non_plant} is a predator for {p2}'),
                    Ecology.SEED_DISPERSER: (close, f'{p1}\'s pollinator species {non_plant} is a seed disperser for {p2}'),
                    Ecology.POLLINATOR: (close, f'{p1} and {p2} have a common pollinator species {non_plant}')
                }
            }[r1][r2]
            if pair:
                utils.add_to_report(pair)

# pylint: enable=inconsistent-return-statements
