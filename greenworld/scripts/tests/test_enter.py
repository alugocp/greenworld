"""
This module tests the enter script
"""
import unittest
from greenworld.scripts import enter
from greenworld import defs


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
