"""
This module defines the Greenworld core algorithm and its rules
"""

from typing import List
import sqlalchemy
from greenworld.serial import deserialize_enum_list
from greenworld.orm import other_species_table
from greenworld.orm import ecology_predator_table
from greenworld.orm import ecology_other_table
from greenworld.orm import ecology_plant_table
from greenworld.utils import CompanionAlgorithm
from greenworld.utils import Factor
from greenworld.utils import Rule
from greenworld.defs import PLANTAE
from greenworld.defs import GrowthHabit
from greenworld.defs import Nitrogen
from greenworld.defs import Ecology
from greenworld.defs import Sun


def asymptotic_total(factors: List[Factor]) -> float:
    """
    Uses an asymptotic function to calculate the value of a factor from the ecology rule
    """
    x = sum(list(map(lambda x: x.value, factors)))
    coeff = -1 if x < 0 else 1
    return round(coeff * (1 - (1 / (((0.6 * x) ** 2) + 1))), 3)


class GreenworldAlgorithm(CompanionAlgorithm):
    """
    Implementation for the official Greenworld core algorithm
    """

    def __init__(self):
        """
        Include the five rules defined in this file
        """
        super().__init__(
            [
                NitrogenRule(),
                EnvironmentRule(),
                SunlightRule(),
                AllelopathyRule(),
                FirstClassEcologyRule(),
                SecondClassEcologyRule(),
            ]
        )


def overlaps(a, b):
    """
    Returns true if the two intervals overlap or touch at all
    """
    return min(a.upper, b.upper) - max(a.lower, b.lower) >= 0


class NitrogenRule(Rule):
    """
    Accounts for interactions in two input plants' relationship to soil nitrogen
    """

    def generate_factor(self, _con, p1, p2) -> Factor:
        """
        Generates a factor for the nitrogen rule
        """
        # p1 is a nitrogen fixer and p2 is a heavy feeder
        if p1.nitrogen == Nitrogen.FIXER and p2.nitrogen == Nitrogen.HEAVY:
            return Factor(1.0, f"{p1.name} can fix nitrogen for {p2.name}")

        # p2 is a nitrogen fixer and p1 is a heavy feeder
        if p2.nitrogen == Nitrogen.FIXER and p1.nitrogen == Nitrogen.HEAVY:
            return Factor(1.0, f"{p2.name} can fix nitrogen for {p1.name}")

        # Both p1 and p2 are heavy feeders
        if p1.nitrogen == Nitrogen.HEAVY and p2.nitrogen == Nitrogen.HEAVY:
            return Factor(-1.0, f"{p1.name} and {p2.name} are both heavy feeders")
        return None


class EnvironmentRule(Rule):
    """
    Accounts for mismatches between two input plants' preferred soil environment
    """

    def generate_factor(self, _con, p1, p2) -> Factor:
        """
        Generates a factor for the environment rule
        """
        factors = []

        # Check soil mismatch
        if p1.soil is not None and p2.soil is not None:
            soils1 = deserialize_enum_list(p1.soil)
            soils2 = deserialize_enum_list(p2.soil)
            if not any(s1 in soils2 for s1 in soils1):
                factors.append(Factor(-1.0, "mismatched soil type"))

        # Check drainage mismatch
        if p1.drainage is not None and p2.drainage is not None:
            drainages1 = deserialize_enum_list(p1.drainage)
            drainages2 = deserialize_enum_list(p2.drainage)
            if not any(d1 in drainages2 for d1 in drainages1):
                factors.append(Factor(-1.0, "mismatched soil drainage"))

        # Check pH mismatch
        if p1.pH is not None and p2.pH is not None:
            if not overlaps(p1.pH, p2.pH):
                factors.append(Factor(-1.0, "mismatched soil pH"))

        while len(factors) < 3:
            factors.append(None)
        return Factor.union(factors, False)


class SunlightRule(Rule):
    """
    Accounts for the interaction between two input plants' growth habit and desired sunlight
    """

    HEIGHT_CLASSES = {
        GrowthHabit.LICHENOUS: 0,
        GrowthHabit.NONVASCULAR: 0,
        GrowthHabit.VINE: 0,
        GrowthHabit.FORB: 0,
        GrowthHabit.GRAMINOID: 0,
        GrowthHabit.SUBSHRUB: 1,
        GrowthHabit.SHRUB: 2,
        GrowthHabit.TREE: 3,
    }

    def generate_factor(self, _con, p1, p2) -> Factor:
        """
        Generates a factor for the sunlight rule
        """
        # Check that required attributes exist
        if (
            p1.growth_habit is None
            or p2.growth_habit is None
            or p1.sun is None
            or p2.sun is None
        ):
            return None

        # Lookup height classes
        h1 = self.HEIGHT_CLASSES[p1.growth_habit]
        h2 = self.HEIGHT_CLASSES[p2.growth_habit]
        if h1 == h2:
            return None

        # Check the dynamics between a taller and shorter plant
        taller = p2 if h2 > h1 else p1
        shorter = p1 if h2 > h1 else p2
        if shorter.sun == Sun.FULL_SUN:
            return Factor(-1.0, f"{taller.name} may shade out {shorter.name}")
        return Factor(1.0, f"{taller.name} can provide shade for {shorter.name}")


class AllelopathyRule(Rule):
    """
    Accounts for allelochemicals shared between two input plants
    """

    def generate_factor(self, con, p1, p2):
        """
        Generates a factor for the allelopathy rule
        """
        if p1.species == p2.species:
            return None
        p1_to_p2_relationship = None
        p2_to_p1_relationship = None

        # Grab both plant families' IDs (if they exist in the other species table)
        family_ids = {p1.family: -1, p2.family: -1}
        stmt = other_species_table.select().where(
            sqlalchemy.or_(
                other_species_table.c["species"] == p1.family,
                other_species_table.c["species"] == p2.family,
            )
        )
        for row in con.execute(stmt).mappings():
            family_ids[row["species"]] = row["id"]

        # Check non-species level allelopathy
        stmt = ecology_other_table.select().where(
            sqlalchemy.or_(
                ecology_other_table.c["plant"] == p1.id,
                ecology_other_table.c["plant"] == p2.id,
            )
        )
        for row in con.execute(stmt).mappings():
            # Plant1 has some relationship to Plantae or plant2's family
            if row["plant"] == p1.id and (
                (row["non_plant"] == PLANTAE and p1_to_p2_relationship is None)
                or row["non_plant"] == family_ids[p2.family]
            ):
                p1_to_p2_relationship = row["relationship"]

            # Plant2 has some relationship to Plantae or plant1's family
            if row["plant"] == p2.id and (
                (row["non_plant"] == PLANTAE and p2_to_p1_relationship is None)
                or row["non_plant"] == family_ids[p1.family]
            ):
                p2_to_p1_relationship = row["relationship"]

        # Check on species-level allelopathy
        stmt = ecology_plant_table.select().where(
            sqlalchemy.or_(
                ecology_plant_table.c["plant"] == p1.id,
                ecology_plant_table.c["plant"] == p2.id,
            )
        )
        for row in con.execute(stmt).mappings():
            # Plant1 has some relationship to plant2
            if row["plant"] == p1.id and row["target"] == p2.id:
                p1_to_p2_relationship = row["relationship"]

            # Plant2 has some relationship to plant1
            if row["plant"] == p2.id and row["target"] == p1.id:
                p2_to_p1_relationship = row["relationship"]

        # Convert the relationship pair into a Factor
        return {
            Ecology.POSITIVE_ALLELOPATHY: {
                Ecology.POSITIVE_ALLELOPATHY: Factor(
                    1.0,
                    f"{p1.name} and {p2.name} are positive allelopaths for each other",
                ),
                Ecology.NEGATIVE_ALLELOPATHY: Factor(
                    0.0,
                    f"{p1.name} is a positive allelopath for {p2.name} but {p2.name} is a negative allelopath for {p1.name}",
                ),
                Ecology.NO_ALLELOPATHY: Factor(
                    1.0, f"{p1.name} is a positive allelopath for {p2.name}"
                ),
            },
            Ecology.NEGATIVE_ALLELOPATHY: {
                Ecology.POSITIVE_ALLELOPATHY: Factor(
                    0.0,
                    f"{p2.name} is a positive allelopath for {p1.name} but {p1.name} is a negative allelopath for {p2.name}",
                ),
                Ecology.NEGATIVE_ALLELOPATHY: Factor(
                    -1.0,
                    f"{p1.name} and {p2.name} are negative allelopaths for each other",
                ),
                Ecology.NO_ALLELOPATHY: Factor(
                    -1.0, f"{p1.name} is a negative allelopath for {p2.name}"
                ),
            },
            Ecology.NO_ALLELOPATHY: {
                Ecology.POSITIVE_ALLELOPATHY: Factor(
                    1.0, f"{p2.name} is a positive allelopath for {p1.name}"
                ),
                Ecology.NEGATIVE_ALLELOPATHY: Factor(
                    -1.0, f"{p2.name} is a negative allelopath for {p1.name}"
                ),
                Ecology.NO_ALLELOPATHY: None,
            },
        }[
            (
                Ecology.NO_ALLELOPATHY
                if p1_to_p2_relationship is None
                else p1_to_p2_relationship
            )
        ][
            (
                Ecology.NO_ALLELOPATHY
                if p2_to_p1_relationship is None
                else p2_to_p1_relationship
            )
        ]


class FirstClassEcologyRule(Rule):
    """
    Accounts for ecological bisections between two input plants
    """

    def generate_factor(self, con, p1, p2):
        """
        Generates a factor for the first-class ecology rule
        """
        if p1.species == p2.species:
            return None
        e1 = ecology_other_table.alias("e1")
        e2 = ecology_other_table.alias("e2")
        stmt = (
            sqlalchemy.select(
                other_species_table.c["name"],
                e1.c["relationship"].label("r1"),
                e2.c["relationship"].label("r2"),
            )
            .join(e2, e1.c["non_plant"] == e2.c["non_plant"])
            .join(other_species_table, other_species_table.c["id"] == e1.c["non_plant"])
            .where(sqlalchemy.and_(e1.c["plant"] == p1.id, e2.c["plant"] == p2.id))
            .distinct()
        )
        factors = []
        for result in con.execute(stmt):
            non_plant, r1, r2 = result
            factors.append(
                {
                    Ecology.NEGATIVE_ALLELOPATHY: {
                        Ecology.NEGATIVE_ALLELOPATHY: Factor(
                            1.0,
                            f"{p1.name} and {p2.name} are both negative allelopaths for {non_plant}",
                        ),
                        Ecology.POSITIVE_ALLELOPATHY: Factor(
                            -1.0,
                            f"{p1.name} is a negative allelopath and {p2.name} is a positive allelopath for {non_plant}",
                        ),
                        Ecology.NO_ALLELOPATHY: None,
                        Ecology.PATHOGEN: Factor(
                            1.0,
                            f"{p1.name} is a negative allelopath for {p2.name}'s pathogenic species {non_plant}",
                        ),
                        Ecology.PREDATOR: Factor(
                            1.0,
                            f"{p1.name} is a negative allelopath for {p2.name}'s predator species {non_plant}",
                        ),
                        Ecology.SEED_DISPERSER: Factor(
                            -1.0,
                            f"{p1.name} is a negative allelopath for {p2.name}'s seed disperser species {non_plant}",
                        ),
                        Ecology.POLLINATOR: Factor(
                            -1.0,
                            f"{p1.name} is a negative allelopath for {p2.name}'s pollinator species {non_plant}",
                        ),
                    },
                    Ecology.POSITIVE_ALLELOPATHY: {
                        Ecology.NEGATIVE_ALLELOPATHY: Factor(
                            -1.0,
                            f"{p1.name} is a positive allelopath and {p2.name} is a negative allelopath for {non_plant}",
                        ),
                        Ecology.POSITIVE_ALLELOPATHY: Factor(
                            1.0,
                            f"{p1.name} and {p2.name} are both positive allelopaths for {non_plant}",
                        ),
                        Ecology.NO_ALLELOPATHY: None,
                        Ecology.PATHOGEN: Factor(
                            -1.0,
                            f"{p1.name} is a positive allelopath for {p2.name}'s pathogenic species {non_plant}",
                        ),
                        Ecology.PREDATOR: Factor(
                            -1.0,
                            f"{p1.name} is a positive allelopath for {p2.name}'s predator species {non_plant}",
                        ),
                        Ecology.SEED_DISPERSER: Factor(
                            1.0,
                            f"{p1.name} is a positive allelopath for {p2.name}'s seed disperser species {non_plant}",
                        ),
                        Ecology.POLLINATOR: Factor(
                            1.0,
                            f"{p1.name} is a positive allelopath for {p2.name}'s pollinator species {non_plant}",
                        ),
                    },
                    Ecology.NO_ALLELOPATHY: {
                        Ecology.NEGATIVE_ALLELOPATHY: None,
                        Ecology.POSITIVE_ALLELOPATHY: None,
                        Ecology.NO_ALLELOPATHY: None,
                        Ecology.PATHOGEN: None,
                        Ecology.PREDATOR: None,
                        Ecology.SEED_DISPERSER: None,
                        Ecology.POLLINATOR: None,
                    },
                    Ecology.PATHOGEN: {
                        Ecology.NEGATIVE_ALLELOPATHY: Factor(
                            1.0,
                            f"{p2.name} is a negative allelopath for {p1.name}'s pathogenic species {non_plant}",
                        ),
                        Ecology.POSITIVE_ALLELOPATHY: Factor(
                            -1.0,
                            f"{p2.name} is a positive allelopath for {p1.name}'s pathogenic species {non_plant}",
                        ),
                        Ecology.NO_ALLELOPATHY: None,
                        Ecology.PATHOGEN: Factor(
                            -1.0,
                            f"{p1.name} and {p2.name} have a common pathogenic species {non_plant}",
                        ),
                        Ecology.PREDATOR: Factor(
                            -1.0,
                            f"{p1.name}'s pathogenic species {non_plant} is a predator for {p2.name}",
                        ),
                        Ecology.SEED_DISPERSER: Factor(
                            -1.0,
                            f"{p1.name}'s pathogenic species {non_plant} is a seed disperser for {p2.name}",
                        ),
                        Ecology.POLLINATOR: Factor(
                            -1.0,
                            f"{p1.name}'s pathogenic species {non_plant} is a pollinator for {p2.name}",
                        ),
                    },
                    Ecology.PREDATOR: {
                        Ecology.NEGATIVE_ALLELOPATHY: Factor(
                            1.0,
                            f"{p2.name} is a negative allelopath for {p1.name}'s predator species {non_plant}",
                        ),
                        Ecology.POSITIVE_ALLELOPATHY: Factor(
                            -1.0,
                            f"{p2.name} is a positive allelopath for {p1.name}'s predator species {non_plant}",
                        ),
                        Ecology.NO_ALLELOPATHY: None,
                        Ecology.PATHOGEN: Factor(
                            -1.0,
                            f"{p1.name}'s predator species {non_plant} is a pathogen for {p2.name}",
                        ),
                        Ecology.PREDATOR: Factor(
                            1.0,
                            f"{p1.name} and {p2.name} have a common predator species {non_plant}",
                        ),
                        Ecology.SEED_DISPERSER: Factor(
                            1.0,
                            f"{p1.name}'s predator species {non_plant} is a seed disperser for {p2.name}",
                        ),
                        Ecology.POLLINATOR: Factor(
                            1.0,
                            f"{p1.name}'s predator species {non_plant} is a pollinator for {p2.name}",
                        ),
                    },
                    Ecology.SEED_DISPERSER: {
                        Ecology.NEGATIVE_ALLELOPATHY: Factor(
                            -1.0,
                            f"{p2.name} is a negative allelopath for {p1.name}'s seed disperser species {non_plant}",
                        ),
                        Ecology.POSITIVE_ALLELOPATHY: Factor(
                            1.0,
                            f"{p2.name} is a positive allelopath for {p1.name}'s seed disperser species {non_plant}",
                        ),
                        Ecology.NO_ALLELOPATHY: None,
                        Ecology.PATHOGEN: Factor(
                            -1.0,
                            f"{p1.name}'s seed disperser species {non_plant} is a pathogen for {p2.name}",
                        ),
                        Ecology.PREDATOR: Factor(
                            1.0,
                            f"{p1.name}'s seed disperser species {non_plant} is a predator for {p2.name}",
                        ),
                        Ecology.SEED_DISPERSER: Factor(
                            1.0,
                            f"{p1.name} and {p2.name} have a common seed disperser species {non_plant}",
                        ),
                        Ecology.POLLINATOR: Factor(
                            1.0,
                            f"{p1.name}'s seed disperser species {non_plant} is a pollinator for {p2.name}",
                        ),
                    },
                    Ecology.POLLINATOR: {
                        Ecology.NEGATIVE_ALLELOPATHY: Factor(
                            -1.0,
                            f"{p2.name} is a negative allelopath for {p1.name}'s pollinator species {non_plant}",
                        ),
                        Ecology.POSITIVE_ALLELOPATHY: Factor(
                            1.0,
                            f"{p2.name} is a positive allelopath for {p1.name}'s pollinator species {non_plant}",
                        ),
                        Ecology.NO_ALLELOPATHY: None,
                        Ecology.PATHOGEN: Factor(
                            -1.0,
                            f"{p1.name}'s pollinator species {non_plant} is a pathogen for {p2.name}",
                        ),
                        Ecology.PREDATOR: Factor(
                            -1.0,
                            f"{p1.name}'s pollinator species {non_plant} is a predator for {p2.name}",
                        ),
                        Ecology.SEED_DISPERSER: Factor(
                            1.0,
                            f"{p1.name}'s pollinator species {non_plant} is a seed disperser for {p2.name}",
                        ),
                        Ecology.POLLINATOR: Factor(
                            1.0,
                            f"{p1.name} and {p2.name} have a common pollinator species {non_plant}",
                        ),
                    },
                }[r1][r2]
            )
        union = Factor.union(factors)
        if union is None:
            return None
        return Factor(asymptotic_total(factors), union.label)


class SecondClassEcologyRule(Rule):
    """
    Accounts for indirect ecological interactions that two input plants experience via nonplant partners
    """

    def generate_factor(self, con, p1, p2):
        """
        Generates a factor for the second-class ecology rule

        Query logic as raw SQL:
        select i1.plant, i1.non_plant, i1.species, i1.relationship, i2.plant, i2.non_plant, i2.species, i2.relationship, ecology_predator.predator from
        (select ecology_other.plant, ecology_other.non_plant, ecology_other.relationship, other_species.species from ecology_other join other_species on other_species.id = ecology_other.non_plant where ecology_other.plant = 47) as i1
        join ecology_predator
        on ecology_predator.predator = i1.non_plant or ecology_predator.prey = i1.non_plant join
        (select ecology_other.plant, ecology_other.non_plant, ecology_other.relationship, other_species.species from ecology_other join other_species on other_species.id = ecology_other.non_plant where ecology_other.plant = 58) as i2
        on ecology_predator.predator = i2.non_plant or ecology_predator.prey = i2.non_plant
        """
        if p1.species == p2.species:
            return None

        # Grab relevant non-plant ecological partner species for P1
        i1 = (
            sqlalchemy.select(
                ecology_other_table.c["non_plant"],
                ecology_other_table.c["relationship"],
                other_species_table.c["species"],
            )
            .join(
                other_species_table,
                ecology_other_table.c["non_plant"] == other_species_table.c["id"],
            )
            .where(ecology_other_table.c["plant"] == p1.id)
        ).alias("i1")

        # Grab relevant non-plant ecological partner species for P2
        i2 = (
            sqlalchemy.select(
                ecology_other_table.c["non_plant"],
                ecology_other_table.c["relationship"],
                other_species_table.c["species"],
            )
            .join(
                other_species_table,
                ecology_other_table.c["non_plant"] == other_species_table.c["id"],
            )
            .where(ecology_other_table.c["plant"] == p2.id)
        ).alias("i2")

        # Join I1 and I2 using the ecological predators table
        stmt = (
            sqlalchemy.select(
                i1.c["non_plant"],
                i1.c["species"],
                i1.c["relationship"],
                i2.c["non_plant"],
                i2.c["species"],
                i2.c["relationship"],
                ecology_predator_table.c["predator"],
            )
            .join(
                ecology_predator_table,
                sqlalchemy.or_(
                    i1.c["non_plant"] == ecology_predator_table.c["predator"],
                    i1.c["non_plant"] == ecology_predator_table.c["prey"],
                ),
            )
            .join(
                i2,
                sqlalchemy.or_(
                    i2.c["non_plant"] == ecology_predator_table.c["predator"],
                    i2.c["non_plant"] == ecology_predator_table.c["prey"],
                ),
            )
            .where(i1.c["non_plant"] != i2.c["non_plant"])
        )

        factors = []
        for result in con.execute(stmt):
            # Determine which data is for the predator and which is for the prey
            if result[0] == result[6]:
                plant_with_predator = p1
                plant_with_prey = p2
                predator_species = result[1]
                prey_species = result[4]
                prey_relation = result[5]
            else:
                plant_with_predator = p2
                plant_with_prey = p1
                predator_species = result[4]
                prey_species = result[1]
                prey_relation = result[2]

            # Logic matrix based on the second-class ecological interaction
            if prey_relation == Ecology.PREDATOR:
                factors.append(
                    Factor(
                        1.0,
                        f"{plant_with_predator.name} attracts {predator_species}, which predates upon {plant_with_prey.name}'s predator species {prey_species}",
                    )
                )

            if prey_relation == Ecology.POLLINATOR:
                factors.append(
                    Factor(
                        -1.0,
                        f"{plant_with_predator.name} attracts {predator_species}, which predates upon {plant_with_prey.name}'s pollinator species {prey_species}",
                    )
                )

        union = Factor.union(factors)
        if union is None:
            return None
        return Factor(asymptotic_total(factors), union.label)
