import unittest
from greenworld.scripts import enter
from greenworld.lib import defs

class ScriptsEnterCase(unittest.TestCase):

    def test_convert_to_unit(self):
        self.assertEqual(enter.convert_to_unit('33.8 F'), 1)
        self.assertEqual(enter.convert_to_unit('1 lbs'), 453.592)
        self.assertEqual(enter.convert_to_unit('1 in'), 0.025)
        self.assertEqual(enter.convert_to_unit('1 ft'), 0.305)
        self.assertEqual(enter.convert_to_unit('33.8 f'), 1)
        self.assertEqual(enter.convert_to_unit('1 LBS'), 453.592)
        self.assertEqual(enter.convert_to_unit('1 iN'), 0.025)
        self.assertEqual(enter.convert_to_unit('1 Ft'), 0.305)

    def test_parse_enum(self):
        self.assertEqual(enter.parse_enum('Ecology.NEGATIVE_ALLELOPATHY'), defs.Ecology.NEGATIVE_ALLELOPATHY)
        self.assertEqual(enter.parse_enum('GrowthHabit.GRAMINOID'), defs.GrowthHabit.GRAMINOID)
        self.assertEqual(enter.parse_enum('Nitrogen.FIXER'), defs.Nitrogen.FIXER)
