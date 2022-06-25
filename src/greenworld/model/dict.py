from typing import List, Tuple
from greenworld.model.suggestion import Suggestion, SuggestedRange
from greenworld.model.types import SuggestionType, Range

class SuggestionDict:
	# A list of canonical Suggestions
	factors: List[Tuple[SuggestionType, str]] = [
		(SuggestionType.SPATIAL,  'disease'),
		(SuggestionType.SPATIAL,  'root disruption'),
		(SuggestionType.SPATIAL,  'pH mismatch'),
		(SuggestionType.SPATIAL,  'water mismatch'),
		(SuggestionType.SPATIAL,  'drainage mismatch'),
		(SuggestionType.TEMPORAL, 'soil loosener')
	]

	# Initializes the Suggestion dictionary
	def init(self) -> None:
		for factor in self.factors:
			self.add_method(factor[1], factor[0])

	# Adds a method to Suggestion that returns a SuggestedRange with a given Suggestion
	def add_method(self, label: str, dimension: Range) -> None:
		def inner(x: float, y: float) -> SuggestedRange:
				return (Suggestion(label, dimension), (x, y))
		inner.__doc__ = f'Returns a SuggestedRange with the label \'{label}\''
		inner.__name__ = label.lower().replace(' ', '_')
		setattr(Suggestion, inner.__name__, inner)