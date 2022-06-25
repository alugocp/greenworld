import os
import sys
import unittest
from typing import List
from greenworld.model.suggestion import Suggestion
from greenworld.algorithm.init import algorithm
from greenworld.database.test.pair import TestPairData
from greenworld.database.test.species import TestSpeciesData
from greenworld.greenworld import Greenworld
from greenworld.injector import Injector
from greenworld.printer import Printer
from testing.data import data

class ValidationTests(unittest.TestCase):
    greenworld: Greenworld
    pairs: TestPairData

    def setUp(self):
        self.pairs = TestPairData()
        injector: Injector = Injector()
        injector.register_service('species-data', TestSpeciesData())
        injector.register_service('printer', Printer(False))
        injector.register_service('pair-data', self.pairs)
        injector.register_service('algorithm', algorithm)
        self.greenworld = Greenworld(injector)

        # Validate that all plants are listed in plants.txt
        nonexistent = []
        source = lambda x: os.path.join(os.path.dirname(__file__), x)
        with open(source('plants.txt'), 'r', encoding = 'utf8') as file:
            plants = list(map(lambda x: x.strip(), file.readlines()))
            for k, v in data.items():
                if not k in plants:
                    nonexistent.append(k)
                for k1, _ in v.items():
                    if not k1 in plants:
                        nonexistent.append(k1)
        if len(nonexistent) > 0:
            formatted = ', '.join(nonexistent)
            print(f'Invalid referenced plants: {formatted}')
            sys.exit(1)

    # Grabs the expected suggestions from our validation data
    @classmethod
    def get_expected(cls, s1: str, s2: str) -> List[Suggestion]:
        if s1 in data and s2 in data[s1]:
            return data[s1][s2]
        if s2 in data and s1 in data[s2]:
            return data[s2][s1]
        return []

    # Runs the validation test
    def test(self):
        errors = 0
        self.greenworld.calculate_compatibility_scores()
        for pair in self.pairs.get_pairs():
            local = []
            expected = self.get_expected(pair.s1.name, pair.s2.name)
            actual = list(map(lambda x: x[0], pair.suggestions))
            for s in expected:
                if s in actual:
                    actual.remove(s)
                else:
                    local.append(f'• Missing {s}')
            for s in actual:
                local.append(f'• Unexpected {s}')
            if len(local) > 0:
                print(f'{pair.s1.name}, {pair.s2.name}:')
                print('\n'.join(local))
                errors += len(local)
        self.assertEqual(errors, 0)
