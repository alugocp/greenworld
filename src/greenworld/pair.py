from typing import List
from .species import Species
from .factor import Factor

# This class represents a grouping of potential companion species.
class Pair:
    factors: List[Factor] = []
    s1: Species
    s2: Species

    def __repr__(self) -> str:
        return f'({self.s1}, {self.s2})'

    def reset(self, s1: Species, s2: Species) -> None:
        self.factors.clear()
        self.s1 = s1
        self.s2 = s2
