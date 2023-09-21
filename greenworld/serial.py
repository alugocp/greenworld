import math
from typing import List
from greenworld.factor import Factor

# Converts a sum value from the database into a list of integers (corresponds to some enum class)
def deserialize_enum_list(val):
    values = []
    check = math.pow(2, math.floor(math.log(val) / math.log(2)))
    while check >= 1:
        if val >= check:
            values.append(int(check))
            val -= check
        check /= 2
    return values

# Converts a report (list of dataclass instances) into a nested list (JSON for the database)
def serialize_report(report: List[Factor]) -> list:
    def serialize_factor(factor: Factor) -> List:
        if factor.interval:
            x, y = factor.interval
            return [[x, y], factor.reason]
        return [None, factor.reason]
    return list(map(serialize_factor, report))
