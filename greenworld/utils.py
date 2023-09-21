from typing import Optional, List
from greenworld.factor import Factor

class AlgorithmUtils:
    __report: List[Factor] = []
    __included_rules = None
    __connection = None
    __rules = []

    # Sets up a new report instance
    def new_report(self):
        self.__included_rules = []
        self.__report = []

    # Returns the current report to another module
    def get_report(self) -> List[Factor]:
        return self.__report

    # Adds a pair to the current report
    def add_to_report(self, factor: Factor, rule_name: Optional[str] = None) -> None:
        if rule_name:
            self.__included_rules.append(rule_name)
        self.__report.append(factor)

    # Returns true if the given rule has been hit
    def is_rule_included(self, rule_name: str) -> bool:
        return rule_name in self.__included_rules

    # Sets the current SQLAlchemy connection
    def set_connection(self, con):
        # pylint: disable-next=global-statement
        self.__connection = con

    # Returns the current SQLAlchemy connection
    def get_connection(self):
        return self.__connection

    # Returns the list of rules to another module
    def get_rules(self):
        return self.__rules

    # Returns true if the two intervals overlap or touch at all
    def overlaps(self, a, b):
        return min(a.upper, b.upper) - max(a.lower, b.lower) >= 0

    def reduce_intervals(self, plant1, plant2, field1, field2):
        return (getattr(plant1[field1], field2) if field1 in plant1 and plant1[field1] else 0) + (getattr(plant2[field1], field2) if field1 in plant2 and plant2[field1] else 0)

    # Adds any valid information to the current report
    def rule(self):
        def decorate_wrapper(func):
            def func_wrapper(plant1, plant2):
                factor = func(plant1, plant2)
                if factor:
                    if factor.interval:
                        dist1, dist2 = factor.interval
                        factor.interval = (round(float(min(dist1, dist2)), 3), round(float(max(dist1, dist2)), 3))
                    self.add_to_report(factor, func.__name__)
            self.__rules.append(func_wrapper)
            func_wrapper.__name__ = func.__name__
            return func_wrapper
        return decorate_wrapper

    # Repeats the decorated function with the tested plants reversed (if nothing was returned the first time)
    def mirrored(self):
        def decorate_wrapper(func):
            def func_wrapper(plant1, plant2):
                return func(plant1, plant2) or func(plant2, plant1)
            func_wrapper.__name__ = func.__name__
            return func_wrapper
        return decorate_wrapper

    # Does not run the decorated function if the tested plants do not have certain fields
    def ensure(self, both = [], fields1 = [], fields2 = []):
        def decorate_wrapper(func):
            def func_wrapper(plant1, plant2):
                for k in both + fields1:
                    if plant1[k] is None:
                        return None
                for k in both + fields2:
                    if plant2[k] is None:
                        return None
                return func(plant1, plant2)
            func_wrapper.__name__ = func.__name__
            return func_wrapper
        return decorate_wrapper

    # Runs the decorated function with the taller of the tested plants first
    def taller_first(self):
        def decorate_wrapper(func):
            def func_wrapper(plant1, plant2):
                if plant1.height and ((not plant2.height) or plant1.height > plant2.height):
                    return func(plant1, plant2)
                if plant2.height and ((not plant1.height) or plant2.height > plant1.height):
                    return func(plant2, plant1)
                return None
            func_wrapper.__name__ = func.__name__
            return func_wrapper
        return decorate_wrapper
