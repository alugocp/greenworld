from dataclasses import dataclass
from typing import List

@dataclass
class Factor:
    value: float
    label: str

    @staticmethod
    def union(factors):
        if len(factors) == 0:
            return None
        return Factor(
            sum(list(map(lambda x: x.value, factors))) / len(factors),
            ' and '.join(list(map(lambda x: x.label, factors)))
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
        factors = []
        for rule in self.__rules:
            factor = rule.generate_factor(con, p1, p2)
            if factor is not None:
                factors.append(factor)

        # Calculate the score and return
        union = Factor.union(factors)
        return Report(
            None if union is None else union.value,
            factors
        )
