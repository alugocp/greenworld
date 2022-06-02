import os
import unittest
from typing import List, Tuple
from greenworld.model.pair import Pair
from greenworld.model.factor import Factor
from greenworld.database.test.pair import TestPairData
from greenworld.database.test.species import TestSpeciesData
from greenworld.greenworld import Greenworld
from greenworld.injector import Injector
from greenworld.printer import Printer

class ValidationTests(unittest.TestCase):
    bad_pairs: List[Tuple[str]]
    good_pairs: List[Tuple[str]]
    greenworld: Greenworld
    pairs: TestPairData

    def setUp(self):
        self.pairs = TestPairData()
        injector: Injector = Injector()
        injector.register_service('species-data', TestSpeciesData())
        injector.register_service('printer', Printer(False))
        injector.register_service('pair-data', self.pairs)
        self.greenworld = Greenworld(injector)
        source = lambda x: os.path.join(os.path.dirname(__file__), x)
        with open(source('companions.txt'), 'r', encoding = 'utf8') as file:
            self.good_pairs = list(map(lambda x: tuple(x.split(', ')), file.readlines()))
        with open(source('anticompanions.txt'), 'r', encoding = 'utf8') as file:
            self.bad_pairs = list(map(lambda x: tuple(x.split(', ')), file.readlines()))

    @classmethod
    def has_outcome(cls, factors: List[Factor], outcome: int) -> bool:
        for factor in factors:
            if factor.outcome == outcome:
                return True
        return False

    def get_expected(self, pair: Pair) -> int:
        found = lambda p, list: (p.s1.name, p.s2.name) in list or (p.s2.name, p.s1.name) in list
        if found(pair, self.good_pairs):
            return Factor.GOOD
        if found(pair, self.bad_pairs):
            return Factor.BAD
        return Factor.NEUTRAL

    def test(self):
        errors = []
        self.greenworld.calculate_compatibility_scores()
        for pair in self.pairs.get_pairs():
            expected = self.get_expected(pair)
            has_good = ValidationTests.has_outcome(pair.factors, Factor.GOOD)
            has_bad = ValidationTests.has_outcome(pair.factors, Factor.BAD)
            if expected == Factor.GOOD:
                if has_bad:
                    errors.append(f'{pair} should not have BAD') # False positive signal
                if not has_good:
                    errors.append(f'{pair} should have GOOD') # False negative signal
            elif expected == Factor.BAD:
                if has_good:
                    errors.append(f'{pair} should not have GOOD') # False positive signal
                if not has_bad:
                    errors.append(f'{pair} should have BAD') # False negative signal
        for e in errors:
            print(e)
        self.assertTrue(len(errors) == 0)
