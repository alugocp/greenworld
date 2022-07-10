import os
import sys
import unittest
from typing import List
from testing.data import generate_validation_data
from greenworld.model.types import Suggestion, stringify_suggestion
from greenworld.algorithm.logic import algorithm
from greenworld.database.test.pair import TestPairData
from greenworld.database.test.species import TestSpeciesData
from greenworld.greenworld import Greenworld
from greenworld.injector import Injector
from greenworld.printer import Printer

class ValidationTests(unittest.TestCase):
    greenworld: Greenworld
    pairs: TestPairData
    data: dict

    def setUp(self):
        self.pairs = TestPairData()
        injector: Injector = Injector()
        injector.register_service('species-data', TestSpeciesData())
        injector.register_service('printer', Printer(False))
        injector.register_service('pair-data', self.pairs)
        injector.register_service('algorithm', algorithm)
        self.greenworld = Greenworld(injector)
        self.data = generate_validation_data()

        # Validate that all plants are listed in plants.txt
        nonexistent = []
        source = lambda x: os.path.join(os.path.dirname(__file__), x)
        with open(source('plants.txt'), 'r', encoding = 'utf8') as file:
            plants = list(map(lambda x: x.strip(), file.readlines()))
            for k, v in self.data.items():
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
    def get_expected(self, s1: str, s2: str) -> List[Suggestion]:
        ls1 = self.data[s1][s2] if s1 in self.data and s2 in self.data[s1] else []
        ls2 = self.data[s2][s1] if s2 in self.data and s1 in self.data[s2] else []
        return ls1 + ls2

    # Runs the validation test
    def test(self):
        errors = 0
        self.greenworld.calculate_compatibility_scores()
        for pair in self.pairs.get_pairs():
            local = []
            expected = list(map(lambda x: x[0], self.get_expected(pair.s1.name, pair.s2.name)))
            actual = list(map(lambda x: x[0], pair.suggestions))
            for s in expected:
                if s in actual:
                     # Ignore calculated suggestions that were expected
                    actual.remove(s)
                else:
                    # Raise expected suggestions that were not calculated
                    local.append(f'• Missing {stringify_suggestion(s)}')
            for s in actual:
                # Raise calculated suggestions that were not expected
                local.append(f'• Unexpected {stringify_suggestion(s)}')
            if len(local) > 0:
                print(f'{pair.s1.name}, {pair.s2.name}:')
                print('\n'.join(local) + '\n')
                errors += len(local)
        self.assertEqual(errors, 0)
