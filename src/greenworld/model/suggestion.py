import math
from typing import Callable, List, Tuple
from greenworld.model.species import Species
from greenworld.model.types import SuggestionType, Range

# This class represents a suggestion to attach to a planting range
class Suggestion:
    dimension: SuggestionType
    label: str

    def __init__(self, label: str, dimension: SuggestionType):
        self.dimension = dimension
        self.label = label

    def __repr__(self) -> str:
        dimension = 'temporal' if self.dimension == SuggestionType.TEMPORAL else 'spatial'
        return f'{self.label} ({dimension})'

    def __eq__(self, other) -> bool:
        return self.label == other.label and self.dimension == other.dimension

    # Returns a string representation of this suggestion with a range attached to it
    def display(self, span: Range) -> str:
        floor = math.floor(span[0] * 100) / 100
        ceil = math.floor(span[1] * 100) / 100
        return f'{self}: {floor} - {ceil}'

    #
    # List of constructors for special suggestions
    #

    @classmethod
    def DISEASE(cls):
        return cls('disease', SuggestionType.SPATIAL)

# Suggestion-related typedefs
SuggestedRange = Tuple[Suggestion, Range]
SuggestionSet = List[SuggestedRange]
Engine = Callable[[SuggestionSet, Species, Species], None]