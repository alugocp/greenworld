import unittest
from intervals import IntInterval
from greenworld.utils import Factor
from greenworld.algorithm import overlaps
from greenworld.algorithm import NitrogenRule
from greenworld.algorithm import EnvironmentRule
from greenworld.defs import Nitrogen

class DotDict(dict):
    __getattr__ = dict.get

class AlgorithmCase(unittest.TestCase):

    def test_overlaps(self):
        self.assertTrue(overlaps(IntInterval([0, 5]), IntInterval([1, 6])))
        self.assertTrue(overlaps(IntInterval([0, 5]), IntInterval([5, 6])))
        self.assertTrue(overlaps(IntInterval([0, 5]), IntInterval([-1, 6])))
        self.assertTrue(overlaps(IntInterval([0, 5]), IntInterval([1, 4])))
        self.assertTrue(overlaps(IntInterval([2, 5]), IntInterval([1, 6])))
        self.assertFalse(overlaps(IntInterval([0, 5]), IntInterval([6, 10])))
        self.assertFalse(overlaps(IntInterval([6, 10]), IntInterval([0, 5])))

    def test_nitrogen(self):
        self.assertEqual(
            NitrogenRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant1', 'nitrogen': Nitrogen.FIXER }),
                DotDict({ 'name': 'Plant2', 'nitrogen': Nitrogen.FIXER })
            ),
            None
        )
        self.assertEqual(
            NitrogenRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant1', 'nitrogen': Nitrogen.FIXER }),
                DotDict({ 'name': 'Plant2', 'nitrogen': Nitrogen.NEUTRAL })
            ),
            None
        )
        self.assertEqual(
            NitrogenRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant1', 'nitrogen': Nitrogen.FIXER }),
                DotDict({ 'name': 'Plant2', 'nitrogen': Nitrogen.HEAVY })
            ),
            Factor(1.0, 'Plant1 can fix nitrogen for Plant2')
        )
        self.assertEqual(
            NitrogenRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant1', 'nitrogen': Nitrogen.NEUTRAL }),
                DotDict({ 'name': 'Plant2', 'nitrogen': Nitrogen.FIXER })
            ),
            None
        )
        self.assertEqual(
            NitrogenRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant1', 'nitrogen': Nitrogen.NEUTRAL }),
                DotDict({ 'name': 'Plant2', 'nitrogen': Nitrogen.NEUTRAL })
            ),
            None
        )
        self.assertEqual(
            NitrogenRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant1', 'nitrogen': Nitrogen.NEUTRAL }),
                DotDict({ 'name': 'Plant2', 'nitrogen': Nitrogen.HEAVY })
            ),
            None
        )
        self.assertEqual(
            NitrogenRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant1', 'nitrogen': Nitrogen.HEAVY }),
                DotDict({ 'name': 'Plant2', 'nitrogen': Nitrogen.FIXER })
            ),
            Factor(1.0, 'Plant2 can fix nitrogen for Plant1')
        )
        self.assertEqual(
            NitrogenRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant1', 'nitrogen': Nitrogen.HEAVY }),
                DotDict({ 'name': 'Plant2', 'nitrogen': Nitrogen.NEUTRAL })
            ),
            None
        )
        self.assertEqual(
            NitrogenRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant1', 'nitrogen': Nitrogen.HEAVY }),
                DotDict({ 'name': 'Plant2', 'nitrogen': Nitrogen.HEAVY })
            ),
            Factor(-1.0, 'Plant1 and Plant2 are both heavy feeders')
        )

    def test_environment(self):
        self.assertEqual(
            EnvironmentRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant 1', 'pH': IntInterval([0, 7]), 'drainage': 3, 'soil': 3 }),
                DotDict({ 'name': 'Plant 2', 'pH': IntInterval([7, 14]), 'drainage': 1, 'soil': 1 })
            ),
            None
        )
        self.assertEqual(
            EnvironmentRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant 1', 'pH': IntInterval([0, 7]), 'drainage': 3, 'soil': 2 }),
                DotDict({ 'name': 'Plant 2', 'pH': IntInterval([7, 14]), 'drainage': 1, 'soil': 1 })
            ),
            Factor(-0.333, 'Plant 1 and Plant 2 require different soil')
        )
        self.assertEqual(
            EnvironmentRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant 1', 'pH': IntInterval([0, 7]), 'drainage': 2, 'soil': 3 }),
                DotDict({ 'name': 'Plant 2', 'pH': IntInterval([7, 14]), 'drainage': 1, 'soil': 1 })
            ),
            Factor(-0.333, 'Plant 1 and Plant 2 require different drainage')
        )
        self.assertEqual(
            EnvironmentRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant 1', 'pH': IntInterval([0, 6]), 'drainage': 3, 'soil': 3 }),
                DotDict({ 'name': 'Plant 2', 'pH': IntInterval([7, 14]), 'drainage': 1, 'soil': 1 })
            ),
            Factor(-0.333, 'Plant 1 and Plant 2 require different pH')
        )
        self.assertEqual(
            EnvironmentRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant 1', 'pH': IntInterval([0, 7]), 'drainage': 2, 'soil': 2 }),
                DotDict({ 'name': 'Plant 2', 'pH': IntInterval([7, 14]), 'drainage': 1, 'soil': 1 })
            ),
            Factor(-0.667, 'Plant 1 and Plant 2 require different soil and drainage')
        )
        self.assertEqual(
            EnvironmentRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant 1', 'pH': IntInterval([0, 6]), 'drainage': 2, 'soil': 3 }),
                DotDict({ 'name': 'Plant 2', 'pH': IntInterval([7, 14]), 'drainage': 1, 'soil': 1 })
            ),
            Factor(-0.667, 'Plant 1 and Plant 2 require different drainage and pH')
        )
        self.assertEqual(
            EnvironmentRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant 1', 'pH': IntInterval([0, 6]), 'drainage': 3, 'soil': 2 }),
                DotDict({ 'name': 'Plant 2', 'pH': IntInterval([7, 14]), 'drainage': 1, 'soil': 1 })
            ),
            Factor(-0.667, 'Plant 1 and Plant 2 require different soil and pH')
        )
        self.assertEqual(
            EnvironmentRule().generate_factor(
                None,
                DotDict({ 'name': 'Plant 1', 'pH': IntInterval([0, 6]), 'drainage': 2, 'soil': 2 }),
                DotDict({ 'name': 'Plant 2', 'pH': IntInterval([7, 14]), 'drainage': 1, 'soil': 1 })
            ),
            Factor(-1.0, 'Plant 1 and Plant 2 require different soil and drainage and pH')
        )
