import math
from typing import List
from greenworld.model.types import SuggestionType, Range

# This class represents a suggested distance between your crops,
# be it spatial or temporal
class Suggestion:
    dimension: SuggestionType
    span: Range
    key: str

    def __init__(self, key: str, span: Range, dimension: SuggestionType):
        self.dimension = dimension
        self.span = span
        self.key = key

    def __repr__(self):
        dimension = 'temporal' if self.dimension == SuggestionType.TEMPORAL else 'spatial'
        floor = math.floor(self.span[0] * 100) / 100
        ceil = math.floor(self.span[1] * 100) / 100
        return f'{self.key} ({dimension}): {floor} - {ceil}'

# A special set class for the suggestion type
class SuggestionSet:
    list: List[Suggestion]

    def __init__(self):
        self.list = []

    def add(self, key: str, span: Range, dimension: SuggestionType = SuggestionType.SPATIAL):
        if len(span) != 2:
            raise f'Invalid range length for {span}'
        self.list.append(Suggestion(key, span, dimension))
