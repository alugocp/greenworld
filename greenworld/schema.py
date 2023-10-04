"""
Schema validation for Greenworld seed data
"""
from schema import Schema, Optional, And, Or
from greenworld import defs


def expand_enum(e):
    """
    Returns a validation rule that matches any value in a given enum
    """
    return Or(*[f"{e.__name__}.{name}" for name in e.__members__.keys()])


json_schema = Schema(
    {
        # Plant species
        Optional("plants"): [
            {
                # Integer that's unique within your data file (will be remapped in the database)
                "id": int,
                # Common name
                "name": str,
                # Scientific name
                "species": str,
                # Taxonomic family
                "family": str,
                # Python enum value from greenworld/defs.py's GrowthHabit
                Optional("growth_habit"): expand_enum(defs.GrowthHabit),
                # Python enum value from greenworld/defs.py's Nitrogen
                Optional("nitrogen"): expand_enum(defs.Nitrogen),
                # Python enum value from greenworld/defs.py's Sun
                Optional("sun"): expand_enum(defs.Sun),
                # Python enum value from greenworld/defs.py's Soil
                Optional("soil"): [expand_enum(defs.Soil)],
                # Range of two values where each one is a valid pH value (a decimal)
                Optional("pH"): And(
                    [float],
                    lambda x: len(x) == 2 and x[0] >= 0 and x[1] <= 14 and x[0] <= x[1],
                ),
                # Python enum value from greenworld/defs.py's Drainage
                Optional("drainage"): [expand_enum(defs.Drainage)],
                # Maps the works_cited list to data within this plant entry
                "citations": {
                    # Maps ids from works_cited to a list of keys from this plant object
                    Optional(str): [str]
                },
                # Ecological partnerships for this plant species
                Optional("ecology"): [
                    {
                        # Scientific name
                        "species": str,
                        # Python enum value from greenworld/defs.py's Ecology
                        "relationship": expand_enum(defs.Ecology),
                        # An id in works_cited
                        "citation": int,
                    }
                ],
            }
        ],
        # Ecological partner species
        Optional("others"): [
            {
                # Scientific name
                "species": str,
                # Common name
                "name": str,
                # Taxonomic family
                Optional("family"): str,
            }
        ],
        # Citations list
        Optional("works_cited"): [
            {
                # id unique to this file's citations list
                "id": int,
                # Link or citation text
                "citation": str,
            }
        ],
    }
)
