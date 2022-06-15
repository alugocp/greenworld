from typing import Callable, List
from greenworld.model.species import Species
from greenworld.model.factor import Factor
Engine = Callable[[List[Factor], Species, Species], None]

class Algorithm:
    engines: List[Engine]

    def __init__(self):
        self.engines = []

    def register(self, name: str) -> None:
        def wrapper(func: Engine):
            self.engines.append((name, func))
        return wrapper

    def run(self, s1: Species, s2: Species) -> List[Factor]:
        factors: List[Factor] = []
        for _, engine in self.engines:
            engine(factors, s1, s2)
        return factors

    def get_names(self) -> List[str]:
        return list(map(lambda x: x[0], self.engines))
