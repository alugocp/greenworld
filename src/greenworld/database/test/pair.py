from typing import List
from greenworld.database.pair import PairData
from greenworld.model.pair import Pair

# This class represents an implementation PairData for unit tests.
class TestPairData(PairData):
    pairs: List[Pair] = []

    def write_pair(self, pair: Pair) -> None:
        self.pairs.append(pair)

    def get_pairs(self) -> List[Pair]:
        return self.pairs
