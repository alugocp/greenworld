"""
This module tests the enter script
"""
import unittest
from greenworld.scripts import enter
from greenworld.scripts import reset
from greenworld import Greenworld
from greenworld import defs
from greenworld import orm

def get_plants(db):
    """
    Return a list of plant objects from the database
    """
    with db.connect() as con:
        data = con.execute(
            orm.plants_table.select()
        )
        return list(data.mappings())

def get_others(db):
    """
    Return a list of non-plant species objects from the database
    """
    with db.connect() as con:
        data = con.execute(
            orm.other_species_table.select()
        )
        return list(data.mappings())

def get_ecology_others(db):
    """
    Return a list of plant / non-plant interaction objects from the database
    """
    with db.connect() as con:
        data = con.execute(
            orm.ecology_other_table.select()
        )
        return list(data.mappings())

class ScriptsEnterCase(unittest.TestCase):
    """
    unittest class
    """

    def test_parse_enum(self):
        """
        Tests the parse_enum function
        """
        self.assertEqual(
            enter.parse_enum("Ecology.NEGATIVE_ALLELOPATHY"),
            defs.Ecology.NEGATIVE_ALLELOPATHY,
        )
        self.assertEqual(
            enter.parse_enum("GrowthHabit.GRAMINOID"), defs.GrowthHabit.GRAMINOID
        )
        self.assertEqual(enter.parse_enum("Nitrogen.FIXER"), defs.Nitrogen.FIXER)

    def test_multiple_same_plants(self):
        """
        Tests when the same plant is added twice
        """
        gw = Greenworld()
        db = orm.init_db()
        reset.main(gw)
        def get_corn(color, species = "Zea mays", none = False):
            corn = {
                "id": 1,
                "name": f"{color} Corn",
                "species": species,
                "family": "Gramineae",
            }
            if none:
                corn["growth_habit"] = None
                corn["nitrogen"] = None
                corn["sun"] = None
                corn["soil"] = None
                corn["pH"] = None
                corn["drainage"] = None
            corn["citations"] = {}
            return corn

        # Enter initial species, ensure it was written to the database
        enter.enter_data(gw, db, {
            "plants": [get_corn("Turquoise")]
        })
        self.assertEqual(
            get_plants(db),
            [get_corn("Turquoise", "Zea mays", True)]
        )

        # Ensure the same species cannot be entered twice
        enter.enter_data(gw, db, {
            "plants": [get_corn("Red")]
        })
        self.assertEqual(
            get_plants(db),
            [get_corn("Red", "Zea mays", True)]
        )

        # Ensure the species name parsing logic does not betray the previous case
        enter.enter_data(gw, db, {
            "plants": [get_corn("Purple", "ZEA mays")]
        })
        self.assertEqual(
            get_plants(db),
            [get_corn("Purple", "Zea mays", True)]
        )

        # Make sure it works with duplicates in a single input
        enter.enter_data(gw, db, {
            "plants": [
                get_corn("Green", "ZEA mays"),
                get_corn("Giant", "zea mays")
            ]
        })
        self.assertEqual(
            get_plants(db),
            [get_corn("Giant", "Zea mays", True)]
        )

    def test_multiple_same_ecology(self):
        """
        Test when multiple plants have ecological interactions with the same species
        """
        gw = Greenworld()
        db = orm.init_db()
        reset.main(gw)
        enter.enter_data(gw, db, {
            "plants": [
                {
                    "id": 1,
                    "name": "White Oak",
                    "species": "Quercus alba",
                    "family": "Fagaceae",
                    "citations": {},
                    "ecology": [
                        {
                            "species": "Cyanocitta crystata",
                            "relationship": "Ecology.PREDATOR",
                            "citation": 1,
                        },
                        {
                            "species": "Cyanocitta crystata",
                            "relationship": "Ecology.PREDATOR",
                            "citation": 1,
                        },
                        {
                            "species": "Cyanocitta crystata",
                            "relationship": "Ecology.SEED_DISPERSER",
                            "citation": 1,
                        }
                    ]
                }
            ],
            "others": [
                {
                    "species": "Cyanocitta crystata",
                    "name": "Bluejay",
                    "family": "Corvidae"
                },
                {
                    "species": "Cyanocitta crystata",
                    "name": "Bluejay",
                    "family": "Corvidae"
                }
            ],
            "works_cited": [{
                "id": 1,
                "citation": "Trust me, bro"
            }]
        })

        # Check that nothing was duplicated
        self.assertEqual(
            get_plants(db),
            [{
                "id": 1,
                "name": "White Oak",
                "species": "Quercus alba",
                "family": "Fagaceae",
                "growth_habit": None,
                "nitrogen": None,
                "sun": None,
                "soil": None,
                "pH": None,
                "drainage": None,
                "citations": {}
            }]
        )
        self.assertEqual(
            get_others(db),
            [
                {
                    "id": 0,
                    "species": "Plantae",
                    "name": "Plant Kingdom",
                    "family": None
                },
                {
                    "id": 1,
                    "species": "Cyanocitta crystata",
                    "name": "Bluejay",
                    "family": "Corvidae"
                }
            ]
        )
        self.assertEqual(
            get_ecology_others(db),
            [
                {
                    "plant": 1,
                    "non_plant": 1,
                    "relationship": defs.Ecology.SEED_DISPERSER,
                    "citation": 1
                }
            ]
        )

    def test_missing_ecology(self):
        """
        Tests errors when required ecological fields are missing
        """
        gw = Greenworld()
        db = orm.init_db()
        reset.main(gw)

        # Check error when other species is unknown
        with self.assertRaises(Exception) as err:
            enter.enter_data(gw, db, {
                "plants": [
                    {
                        "id": 1,
                        "name": "White Oak",
                        "species": "Quercus alba",
                        "family": "Fagaceae",
                        "citations": {},
                        "ecology": [
                            {
                                "species": "Cyanocitta crystata",
                                "relationship": "Ecology.PREDATOR",
                                "citation": 1,
                            }
                        ]
                    }
                ]
            })
        self.assertEqual(str(err.exception), "Unknown interactive species 'Cyanocitta crystata'")

        # Check error when ecology citation is unknown
        with self.assertRaises(Exception) as err:
            enter.enter_data(gw, db, {
                "plants": [
                    {
                        "id": 1,
                        "name": "White Oak",
                        "species": "Quercus alba",
                        "family": "Fagaceae",
                        "citations": {},
                        "ecology": [
                            {
                                "species": "Cyanocitta crystata",
                                "relationship": "Ecology.PREDATOR",
                                "citation": 1,
                            }
                        ]
                    }
                ],
                "others": [
                    {
                        "species": "Cyanocitta crystata",
                        "name": "Bluejay",
                        "family": "Corvidae"
                    }
                ]
            })
        self.assertEqual(str(err.exception), "Unknown citation with ID '1'")
