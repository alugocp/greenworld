from typing import List
from greenworld.model.species import Species
from greenworld.model.factor import Factor

# This class represents a grouping of potential companion species.
class Pair:
    factors: List[Factor] = []
    s1: Species
    s2: Species

    def __init__(self, s1: Species, s2: Species):
        self.s1 = s1
        self.s2 = s2

    def __repr__(self) -> str:
        return f'({self.s1}, {self.s2})'
