from ..pair import Pair
from .data import Data

# This class represents an interface of pair data access. An implementation may
# connect this interface to a database or other source.
class PairData(Data):

    # Opens the output source connection
    def open(self) -> None:
        pass

    # Closes the output source connection
    def close(self) -> None:
        pass

    # Writes pair data to whatever source your implementation uses
    def write_pair(self, pair: Pair) -> None:
        pass
