from intervals import IntInterval
import unittest
import utils

class AlgorithmUtilCase(unittest.TestCase):

    def test_overlaps(self):
        self.assertTrue(utils.overlaps(IntInterval([0, 5]), IntInterval([1, 6])))
        self.assertTrue(utils.overlaps(IntInterval([0, 5]), IntInterval([5, 6])))
        self.assertTrue(utils.overlaps(IntInterval([0, 5]), IntInterval([-1, 6])))
        self.assertTrue(utils.overlaps(IntInterval([2, 5]), IntInterval([1, 6])))
        self.assertFalse(utils.overlaps(IntInterval([0, 5]), IntInterval([6, 10])))
        self.assertFalse(utils.overlaps(IntInterval([6, 10]), IntInterval([0, 5])))

    def test_rule(self):
        utils.new_report()
        self.assertEqual(len(utils.get_report()), 0)
        self.assertEqual(len(utils.get_rules()), 0)
        utils.rule(lambda x, y: x)(True, False)
        self.assertEqual(len(utils.get_report()), 1)
        self.assertEqual(len(utils.get_rules()), 1)
        utils.rule(lambda x, y: y)(True, False)
        self.assertEqual(len(utils.get_report()), 1)
        self.assertEqual(len(utils.get_rules()), 2)