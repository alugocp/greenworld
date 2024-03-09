"""
Helper classes used by Greenworld as an interface to the core algorithm
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Factor:
    """
    Data class representing a factor
    """

    value: float
    label: str

    @staticmethod
    def union(factors, apply_filter=True):
        """
        Aggregate one or more factors
        """
        if len(factors) == 0:
            return None
        filtered = list(filter(lambda x: x is not None, factors))
        if len(filtered) == 0:
            return None
        if apply_filter:
            factors = filtered
        return Factor(
            round(
                sum(list(map(lambda x: 0.0 if x is None else x.value, factors)))
                / len(factors),
                3,
            ),
            " and ".join(list(map(lambda x: x.label, filtered))),
        )


@dataclass
class Report:
    """
    Data class representing a report
    """

    score: float
    factors: List[Factor]


class Rule:
    """
    The abstract class representing a rule in an algorithm
    """

    def generate_factor(self, con, p1, p2) -> Factor:
        """
        Abstract method for a rule to generate a factor
        """


class CompanionAlgorithm:
    """
    The abstract class for any core algorithm to be used in Greenworld
    """

    def __init__(self, rules=[]):
        self.__rules = rules

    def generate_report(self, con, p1, p2):
        """
        Runs every rule in this algorithm and combines the factors into a single report
        """
        # Gather a factor from each applicable rule
        factors = list(map(lambda x: x.generate_factor(con, p1, p2), self.__rules))

        # Calculate the score and return
        union = Factor.union(factors)
        return Report(
            None if union is None else union.value,
            list(filter(lambda x: x is not None, factors)),
        )
