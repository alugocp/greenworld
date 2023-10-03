import unittest
from greenworld.utils import CompanionAlgorithm
from greenworld.utils import Factor
from greenworld.utils import Report
from greenworld.utils import Rule

class DotDict(dict):
    __getattr__ = dict.get

class LibUtilsCase(unittest.TestCase):

    def test_factor_union(self):
        self.assertEqual(
            Factor.union([
                Factor(0.4, 'factor 1'),
                Factor(0.1, 'factor 2'),
                Factor(0.1, 'factor 3'),
            ]),
            Factor(0.2, 'factor 1 and factor 2 and factor 3')
        )

    def test_generate_report(self):
        p1 = DotDict({ 'species': 'plant1' })
        p2 = DotDict({ 'species': 'plant2' })
        p3 = DotDict({ 'species': 'plant3' })
        mock = MockAlgorithm()
        self.assertEqual(
            mock.generate_report(None, p1, p2),
            Report(0.0, [
                Factor(1.0, 'rule 1 is here'),
                Factor(-1.0, 'rule 2 is here'),
                Factor(0.0, 'rule 3 is here')
            ])
        )
        self.assertEqual(
            mock.generate_report(None, p1, p3),
            Report(-1.0, [
                Factor(-1.0, 'rule 2 is here')
            ])
        )
        self.assertEqual(
            mock.generate_report(None, p3, p2),
            Report(0.0, [
                Factor(0.0, 'rule 3 is here')
            ])
        )
        self.assertEqual(
            mock.generate_report(None, p3, p3),
            Report(None, [])
        )

class MockAlgorithm(CompanionAlgorithm):

    def __init__(self):
        super().__init__([
            Rule1(),
            Rule2(),
            Rule3(),
        ])

class Rule1(Rule):

    def generate_factor(self, _con, p1, p2):
        if p1.species == 'plant1' and p2.species == 'plant2':
            return Factor(1.0, 'rule 1 is here')
        return None

class Rule2(Rule):

    def generate_factor(self, _con, p1, p2):
        if p1.species == 'plant1':
            return Factor(-1.0, 'rule 2 is here')
        return None

class Rule3(Rule):

    def generate_factor(self, _con, p1, p2):
        if p2.species == 'plant2':
            return Factor(0.0, 'rule 3 is here')
        return None
