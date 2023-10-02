import unittest
from greenworld.scripts import report
from greenworld.scripts import reset
from greenworld.scripts import enter
from greenworld.factor import Factor
from greenworld import Greenworld

class ScriptsReportCase(unittest.TestCase):

    def test_get_range_union(self):
        self.assertEqual(report.get_range_union([Factor((0, 1), None), Factor((9, 10), None)]), (9, 10))
        self.assertEqual(report.get_range_union([Factor((0, 1), None), Factor((0, 2), None)]), (0, 1))
        self.assertEqual(report.get_range_union([Factor((0, 2), None), Factor((1, 2), None)]), (1, 2))
        self.assertEqual(report.get_range_union([Factor((0, 1), None), Factor((1, 2), None)]), (1, 2))
        self.assertEqual(report.get_range_union([Factor((1, 4), None), Factor((2, 3), None)]), (2, 3))
        self.assertEqual(report.get_range_union([Factor((1, 2), None), Factor((3, 4), None), Factor((5, 6), None)]), (5, 6))
        self.assertEqual(report.get_range_union([Factor((1, 6), None), Factor((5, 7), None)]), (5, 6))

    def test_get_analysis_total(self):
        self.assertEqual(report.get_analysis_total(3, 0), 6)
        self.assertEqual(report.get_analysis_total(4, 0), 10)
        self.assertEqual(report.get_analysis_total(5, 0), 15)
        self.assertEqual(report.get_analysis_total(108, 0), 5886)
        self.assertEqual(report.get_analysis_total(3, 3), 15)
        self.assertEqual(report.get_analysis_total(3, 5), 21)
        self.assertEqual(report.get_analysis_total(0, 0), 0)
        self.assertEqual(report.get_analysis_total(0, 10), 0)

    def test_three_sisters(self):
        logs = []
        gw = Greenworld(log_func = logs.append)
        reset.main(gw, seed_data = False)
        enter.main(gw, [
            'seed-data/pests.json',
            'seed-data/pathogens.json',
            'seed-data/three-sisters.json'
        ])
        logs.clear()
        report.main(gw)
        self.assertEqual(logs, [
            '1/6: Hopi Turquoise Corn (zea mays) x Hopi Turquoise Corn (zea mays)',
            '2/6: Hopi Turquoise Corn (zea mays) x Hopi Orange Squash (cucurbita maxima)',
            '3/6: Hopi Orange Squash (cucurbita maxima) x Hopi Orange Squash (cucurbita maxima)',
            '4/6: Hopi Turquoise Corn (zea mays) x Hopi Purple String Bean (phaseolus vulgaris)',
            '5/6: Hopi Orange Squash (cucurbita maxima) x Hopi Purple String Bean (phaseolus vulgaris)',
            '6/6: Hopi Purple String Bean (phaseolus vulgaris) x Hopi Purple String Bean (phaseolus vulgaris)'
        ])
