from typing import List
from greenworld.model.suggestion import Suggestion
from greenworld.model.species import Species

# This class represents a grouping of potential companion species.
class Pair:
    suggestions: List[Suggestion] = []
    s1: Species
    s2: Species

    def __init__(self, s1: Species, s2: Species):
        self.s1 = s1
        self.s2 = s2

    def __repr__(self) -> str:
        return f'({self.s1.name}, {self.s2.name})'
