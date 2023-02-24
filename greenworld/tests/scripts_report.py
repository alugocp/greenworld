import unittest
from greenworld.scripts import report
from greenworld.scripts import reset
from greenworld.scripts import enter
from greenworld.lib import Greenworld

class ScriptsReportCase(unittest.TestCase):

    def test_get_range_union(self):
        self.assertEqual(report.get_range_union([((0, 1), None), ((9, 10), None)]), (0, 10))
        self.assertEqual(report.get_range_union([((0, 1), None), ((0, 2), None)]), (0, 2))
        self.assertEqual(report.get_range_union([((0, 2), None), ((1, 2), None)]), (0, 2))
        self.assertEqual(report.get_range_union([((0, 1), None), ((1, 2), None)]), (0, 2))
        self.assertEqual(report.get_range_union([((1, 4), None), ((2, 3), None)]), (1, 4))
        self.assertEqual(report.get_range_union([((1, 2), None), ((3, 4), None), ((5, 6), None)]), (1, 6))

    def test_three_sisters(self):
        logs = []
        gw = Greenworld(log_func = logs.append)
        reset.main(gw, seed_data = False)
        enter.main(gw, ['seed-data/three-sisters.json'])
        logs.clear()
        report.main(gw)
        self.assertEqual(logs, [
            'Analyzing Hopi Turquoise Corn x Hopi Orange Squash...',
            'Analyzing Hopi Turquoise Corn x Hopi Purple String Bean...',
            'Analyzing Hopi Orange Squash x Hopi Purple String Bean...'
        ])
