from math import factorial
from typing import Dict, Iterable, Iterator, List
from ..types import Niches, Niche

# This function returns the number combinations (n choose k)
def combination(n: int, k: int) -> int:
    return (int)(factorial(n) / (factorial(k) * factorial(n - k)))

# This class represents combinatoric algorithms for estimating runtime and
# iterating through combinations of data.
class NicheCombinatorics:
    niche_numbers: Dict[Niche, int]
    niches: Niches

    def __init__(self, niches: Niches, niche_numbers: Dict[Niche, int]):
        self.niche_numbers = niche_numbers
        self.niches = niches

    # This function returns the number of combinations of niches
    def get_number_niche_combinations(self) -> int:
        result: int = 0
        for n in range(2, len(self.niches) + 1):
            result += combination(len(self.niches), n)
        return result

    # This function returns the number of combinations between species from the
    # given niches.
    def get_number_groups_from_subniches(self, subniches: Niches) -> int:
        if len(subniches) == 0:
            return 0
        result: int = 1
        for niche in subniches:
            result *= self.niche_numbers[niche]
        return result

    # This function returns the total number of companionship groups you can
    # have with the number of niches and species in each niche.
    def get_number_total_groups(self) -> int:
        result = 0
        for n in range(2, len(self.niches) + 1):
            for subniches in iterate_subset_combinations(n, self.niches):
                result += self.get_number_groups_from_subniches(subniches)
        return result

# This function allows you to iterate through every combination of k
# elements in this set
def iterate_subset_combinations(k: int, items: List) -> Iterator:
    return CombinationsSubsetIterator(k, items)

# This function allows you to iterate through every combination of a group
# of iterables.
def iterate_combinations(*args: Iterable) -> Iterator:
    return CombinationsIterator(*args)

# This helper class is sued to iterate through every combination of k items from
# a set of n items.
class CombinationsSubsetIterator:
    first: bool = True
    current: List
    items: List
    k: int

    def __init__(self, k: int, items: List):
        self.current = list(range(k))
        self.items = items
        self.k = k

    def __iter__(self):
        return self

    def __next__(self):
        if self.first:
            self.first = False
        else:
            i = self.k - 1
            while i >= 0 and self.current[i] == len(self.items) - self.k + i:
                i -= 1
            if i < 0:
                raise StopIteration
            self.current[i] += 1
            for a in range(i + 1, self.k):
                self.current[a] = self.current[a - 1] + 1
        return list(map(lambda x: self.items[x], self.current))

# This helper class is sued to iterate through every combination of k items from
# a set of n items.
class CombinationsIterator:
    iterables: List[Iterable]
    iterators: List[Iterator]
    first: bool = True
    current: List

    def __init__(self, iterables: List[Iterable]):
        def next_or_none(x: Iterator):
            try:
                return next(x)
            except StopIteration:
                return None
        self.iterators = list(map(lambda x: x.__iter__(), iterables))
        self.current = list(map(next_or_none, self.iterators))
        self.iterables = iterables

    def __iter__(self):
        return self

    def __next__(self):
        if self.first:
            self.first = False
        else:
            i = len(self.iterators) - 1
            while True:
                try:
                    self.current[i] = next(self.iterators[i])
                except StopIteration as stop:
                    self.iterators[i] = self.iterables[i].__iter__()
                    self.current[i] = next(self.iterators[i])
                    i -= 1
                    if i < 0:
                        raise stop
                    continue
                break
        return self.current
