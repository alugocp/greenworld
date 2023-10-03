from dataclasses import dataclass
from typing import List

@dataclass
class Factor:
    value: float
    label: str

    @staticmethod
    def union(factors, apply_filter = True):
        if len(factors) == 0:
            return None
        filtered = list(filter(lambda x: x is not None, factors))
        if len(filtered) == 0:
            return None
        if apply_filter:
            factors = filtered
        return Factor(
            round(sum(list(map(lambda x: 0.0 if x is None else x.value, factors))) / len(factors), 3),
            ' and '.join(list(map(lambda x: x.label, filtered)))
        )

@dataclass
class Report:
    score: float
    factors: List[Factor]

class Rule:
    def generate_factor(self, con, p1, p2) -> Factor:
        pass

class CompanionAlgorithm:

    def __init__(self, rules = []):
        self.__rules = rules

    def generate_report(self, con, p1, p2):
        # Gather a factor from each applicable rule
        factors = list(map(lambda x: x.generate_factor(con, p1, p2), self.__rules))

        # Calculate the score and return
        union = Factor.union(factors)
        return Report(
            None if union is None else union.value,
            list(filter(lambda x: x is not None, factors))
        )
