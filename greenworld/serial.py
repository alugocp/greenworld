"""
Logic for serializing/deserializing to/from the database
"""
import math


# Converts a sum value from the database into a list of integers (corresponds to some enum class)
def deserialize_enum_list(val):
    """
    Deserialize a bitwise unioned database value into a list of enum values
    """
    values = []
    check = math.pow(2, math.floor(math.log(val) / math.log(2)))
    while check >= 1:
        if val >= check:
            values.append(int(check))
            val -= check
        check /= 2
    return values


def serialize_factors(factors):
    """
    Strip a list of factors into just their labels for database storage
    """
    return list(map(lambda x: x.label, factors))
