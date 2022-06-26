from typing import List, Tuple
from greenworld.model.types import SuggestedRange, SuggestionType, Range

class CanonicalSuggestions:

    # A list of canonical Suggestions
    factors: List[Tuple[SuggestionType, str]] = [
        (SuggestionType.SPATIAL,  'root disruption'),
        (SuggestionType.SPATIAL,  'pH mismatch'),
        (SuggestionType.SPATIAL,  'water mismatch'),
        (SuggestionType.SPATIAL,  'drainage mismatch'),
        (SuggestionType.SPATIAL,  'repels pests'),
        (SuggestionType.SPATIAL,  'nitrogen fixer'), # Both dimensions
        (SuggestionType.SPATIAL,  'provides shade'),
        (SuggestionType.SPATIAL,  'sacrificial crop'),
        (SuggestionType.SPATIAL,  'resource competition'), # Both dimensions
        (SuggestionType.SPATIAL,  'similar diseases'), # Both dimensions
        (SuggestionType.SPATIAL,  'bad allelopathy'), # Both dimensions
        (SuggestionType.SPATIAL,  'good allelopathy'), # Both dimensions
        (SuggestionType.SPATIAL,  'same pests'), # Both dimensions
        (SuggestionType.SPATIAL,  'vine competition'),
        (SuggestionType.SPATIAL,  'sunlight competition'),
        (SuggestionType.SPATIAL,  'overgrowth competition'),
        (SuggestionType.SPATIAL,  'supress weeds'),
        (SuggestionType.SPATIAL,  'attracts friends'),
        (SuggestionType.TEMPORAL, 'soil loosener')
    ]

    # Initializes the Suggestion dictionary
    def populate(self) -> None:
        for factor in self.factors:
            self.add_method(factor[0], factor[1])

    # Adds a method to Suggestion that returns a SuggestedRange with a given Suggestion
    @classmethod
    def add_method(cls, dimension: Range, label: str) -> None:
        def inner(x: float = -1, y: float = -1) -> SuggestedRange:
            return ((dimension, label), (x, y))
        inner.__doc__ = f'Returns a SuggestedRange with the label \'{label}\''
        inner.__name__ = label.lower().replace(' ', '_')
        setattr(cls, inner.__name__, inner)
