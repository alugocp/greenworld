from typing import Callable, List
from greenworld.model.species import Species
from greenworld.model.types import SuggestionSet

# Engine type for decorators
Engine = Callable[[SuggestionSet, Species, Species], None]

# Class that defines the compatibility calculation algorithm
class Algorithm:
    engines: List[Engine]

    def __init__(self):
        self.engines = []

    def register(self, name: str) -> None:
        def wrapper(func: Engine):
            self.engines.append((name, func))
        return wrapper

    def run(self, s1: Species, s2: Species) -> SuggestionSet:
        suggestions: SuggestionSet = []
        for _, engine in self.engines:
            engine(suggestions, s1, s2)
        return list(filter(lambda x: x is not None, suggestions))

    def get_names(self) -> List[str]:
        return list(map(lambda x: x[0], self.engines))
