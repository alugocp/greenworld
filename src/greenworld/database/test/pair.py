from typing import List
from greenworld.model.pair import Pair
from greenworld.database.dev.pair_text import TextPairData

# This class represents an implementation PairData for unit tests.
class TestPairData(TextPairData):
    pairs: List[Pair] = []

    def __init__(self):
        super().__init__('output.txt')

    def write_pair(self, pair: Pair) -> None:
        super().write_pair(pair)
        self.pairs.append(pair)

    def get_pairs(self) -> List[Pair]:
        return self.pairs
