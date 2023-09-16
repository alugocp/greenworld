from schema import Schema, Optional, And, Or
from greenworld import defs

def expand_enum(e):
    return Or(*[f'{e.__name__}.{name}' for name in e.__members__.keys()])

json_schema = Schema({

    # Plant species
    Optional('plants'): [
        {

            # Integer that's unique within your data file (will be remapped in the database)
            'id': int,

            # Common name
            'name': str,

            # Scientific name
            'species': str,

            # Taxonomic family
            'family': str,

            # Python enum value from greenworld/defs.py's GrowthHabit
            Optional('growth_habit'): expand_enum(defs.GrowthHabit),

            # Range of two values where each one is a string containing a decimal and a unit
            # Check greenworld/scripts/enter.py's _conversions for a list of supported units
            Optional('height'): And([str], lambda x: len(x) == 2),

            # Range of two values where each one is a string containing a decimal and a unit
            # Check greenworld/scripts/enter.py's _conversions for a list of supported units
            Optional('spread'): And([str], lambda x: len(x) == 2),

            # Range of two values where each one is a string containing a decimal and a unit
            # Check greenworld/scripts/enter.py's _conversions for a list of supported units
            Optional('length'): And([str], lambda x: len(x) == 2),

            # Set to true if the vine has fruit that's small enough to grow up forbs and graminoids (i.e. beans)
            Optional('lightweight'): bool,

            # Range of two values where each one is a string containing a decimal and a unit
            # Check greenworld/scripts/enter.py's _conversions for a list of supported units
            Optional('root_spread'): And([str], lambda x: len(x) == 2),

            # Python enum value from greenworld/defs.py's Nitrogen
            Optional('nitrogen'): expand_enum(defs.Nitrogen),

            # Python enum value from greenworld/defs.py's Sun
            Optional('sun'): expand_enum(defs.Sun),

            # Python enum value from greenworld/defs.py's Soil
            Optional('soil'): [expand_enum(defs.Soil)],

            # Range of two values where each one is a valid pH value (a decimal)
            Optional('pH'): And([float], lambda x: len(x) == 2 and x[0] >= 0 and x[1] <= 14 and x[0] <= x[1]),

            # Python enum value from greenworld/defs.py's Drainage
            Optional('drainage'): expand_enum(defs.Drainage),

            # Maps the works_cited list to data within this plant entry
            'citations': {

                # Maps ids from works_cited to a list of keys from this plant object
                Optional(str): [str]
            },

            # Ecological partnerships for this plant species
            Optional('ecology'): [
                {

                    # Scientific name
                    'species': str,

                    # Python enum value from greenworld/defs.py's Ecology
                    'relationship': expand_enum(defs.Ecology),

                    # An id in works_cited
                    'citation': int
                }
            ]
        }
    ],

    # Ecological partner species
    Optional('others'): [
        {

            # Scientific name
            'species': str,

            # Common name
            'name': str,

            # Taxonomic family
            Optional('family'): str
        }
    ],

    # Citations list
    Optional('works_cited'): [
        {

            # id unique to this file's citations list
            'id': int,

            # Link or citation text
            'citation': str
        }
    ]
})