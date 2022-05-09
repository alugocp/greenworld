from typing import Iterable, Iterator, List
from math import factorial

# This function returns the number combinations (n choose k)
def combination(n: int, k: int) -> int:
    return (int)(factorial(n) / (factorial(k) * factorial(n - k)))
