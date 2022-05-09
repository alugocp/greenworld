import unittest
from greenworld.database.test.pair import TestPairData
from greenworld.database.test.species import TestSpeciesData
from greenworld.greenworld import Greenworld
from greenworld.injector import Injector
from greenworld.printer import Printer

class ValidationTests(unittest.TestCase):
    greenworld: Greenworld
    pairs: TestPairData

    def __init__(self):
        self.pairs = TestPairData()
        injector: Injector = Injector()
        injector.register_service('species-data', TestSpeciesData())
        injector.register_service('printer', Printer(False))
        injector.register_service('pair-data', self.pairs)
        self.greenworld = Greenworld(injector)

    def companion_validation_tests(self):
        self.greenworld.calculate_compatibility_scores()
        print(self.pairs.get_pairs())
