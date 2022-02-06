import unittest
import greenworld.math.combinatorics as combos

class TestCombinatoricsIterators(unittest.TestCase):
    def test_iterate_subset_combinations(self):
        iterator = combos.iterate_subset_combinations(3, [1, 2, 3, 4, 5])
        self.assertTrue(next(iterator) == [1, 2, 3])
        self.assertTrue(next(iterator) == [1, 2, 4])
        self.assertTrue(next(iterator) == [1, 2, 5])
        self.assertTrue(next(iterator) == [1, 3, 4])
        self.assertTrue(next(iterator) == [1, 3, 5])
        self.assertTrue(next(iterator) == [1, 4, 5])
        self.assertTrue(next(iterator) == [2, 3, 4])
        self.assertTrue(next(iterator) == [2, 3, 5])
        self.assertTrue(next(iterator) == [2, 4, 5])
        self.assertTrue(next(iterator) == [3, 4, 5])
        self.assertRaises(StopIteration, lambda: next(iterator))

if __name__ == '__main__':
    unittest.main()