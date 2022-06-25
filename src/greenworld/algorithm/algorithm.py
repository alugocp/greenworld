from typing import List
from greenworld.model.species import Species
from greenworld.model.suggestion import Engine, SuggestionSet

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
        return suggestions

    def get_names(self) -> List[str]:
        return list(map(lambda x: x[0], self.engines))
