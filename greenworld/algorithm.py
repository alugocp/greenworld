import sqlalchemy
from greenworld.serial import deserialize_enum_list
from greenworld.orm import other_species_table
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


class GreenworldAlgorithm(CompanionAlgorithm):
    def __init__(self):
        super().__init__(
            [
                NitrogenRule(),
                EnvironmentRule(),
                SunlightRule(),
                AllelopathyRule(),
                EcologyRule(),
            ]
        )


# Returns true if the two intervals overlap or touch at all
def overlaps(a, b):
    return min(a.upper, b.upper) - max(a.lower, b.lower) >= 0


class NitrogenRule(Rule):
    def generate_factor(self, _con, p1, p2) -> Factor:
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
    def generate_factor(self, _con, p1, p2) -> Factor:
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
    HEIGHT_CLASSES = {
        GrowthHabit.LICHENOUS: 0,
        GrowthHabit.NONVASCULAR: 0,
        GrowthHabit.VINE: 0,
        GrowthHabit.FORB: 0,
        GrowthHabit.GRAMINOID: 0,
        GrowthHabit.SUBSHRUB: 2,
        GrowthHabit.SHRUB: 3,
        GrowthHabit.TREE: 4,
    }

    def generate_factor(self, _con, p1, p2) -> Factor:
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
    def generate_factor(self, con, p1, p2):
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
            Ecology.NO_ALLELOPATHY
            if p1_to_p2_relationship is None
            else p1_to_p2_relationship
        ][
            Ecology.NO_ALLELOPATHY
            if p2_to_p1_relationship is None
            else p2_to_p1_relationship
        ]


class EcologyRule(Rule):
    def generate_factor(self, con, p1, p2):
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
        return Factor(self.calculate_total(factors), union.label)

    def calculate_total(self, factors):
        x = sum(list(map(lambda x: x.value, factors)))
        coeff = -1 if x < 0 else 1
        return round(coeff * (1 - (1 / (((0.6 * x) ** 2) + 1))), 3)
