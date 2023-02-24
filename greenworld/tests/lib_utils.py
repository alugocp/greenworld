import unittest
from intervals import IntInterval
from greenworld.lib import utils

class LibUtilsCase(unittest.TestCase):

    def test_overlaps(self):
        self.assertTrue(utils.overlaps(IntInterval([0, 5]), IntInterval([1, 6])))
        self.assertTrue(utils.overlaps(IntInterval([0, 5]), IntInterval([5, 6])))
        self.assertTrue(utils.overlaps(IntInterval([0, 5]), IntInterval([-1, 6])))
        self.assertTrue(utils.overlaps(IntInterval([2, 5]), IntInterval([1, 6])))
        self.assertFalse(utils.overlaps(IntInterval([0, 5]), IntInterval([6, 10])))
        self.assertFalse(utils.overlaps(IntInterval([6, 10]), IntInterval([0, 5])))

    def test_reduce_intervals(self):
        self.assertEqual(utils.reduce_intervals({'spread': IntInterval([1, 2])}, {'spread': IntInterval([1, 2])}, 'spread', 'upper'), 4)
        self.assertEqual(utils.reduce_intervals({'spread': IntInterval([1, 2])}, {'spread': IntInterval([0, 1])}, 'spread', 'upper'), 3)
        self.assertEqual(utils.reduce_intervals({'spread': IntInterval([1, 2])}, {'spread': IntInterval([1, 2])}, 'spread', 'lower'), 2)
        self.assertEqual(utils.reduce_intervals({'spread': IntInterval([1, 2])}, {'spread': IntInterval([0, 1])}, 'spread', 'lower'), 1)
        self.assertEqual(utils.reduce_intervals({'spread': IntInterval([1, 2])}, {'spread': None}, 'spread', 'upper'), 2)
        self.assertEqual(utils.reduce_intervals({'spread': None}, {'spread': IntInterval([1, 2])}, 'spread', 'upper'), 2)
        self.assertEqual(utils.reduce_intervals({'spread': IntInterval([1, 2])}, {}, 'spread', 'upper'), 2)
        self.assertEqual(utils.reduce_intervals({}, {'spread': IntInterval([1, 2])}, 'spread', 'upper'), 2)
        self.assertEqual(utils.reduce_intervals({}, {}, 'spread', 'upper'), 0)

    def test_rule(self):
        utils.new_report()
        self.assertEqual(len(utils.get_report()), 0)
        self.assertEqual(len(utils.get_rules()), 0)
        utils.rule(lambda x, y: (None, x))(True, False)
        self.assertEqual(len(utils.get_report()), 1)
        self.assertEqual(len(utils.get_rules()), 1)
        utils.rule(lambda x, y: None)(True, False)
        self.assertEqual(len(utils.get_report()), 1)
        self.assertEqual(len(utils.get_rules()), 2)
