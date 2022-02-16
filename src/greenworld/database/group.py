from ..group import Group
from .data import Data

# This class represents an interface of group data access. An implementation may
# connect this interface to a database or other source.
class GroupData(Data):

    # Opens the output source connection
    def open(self) -> None:
        pass

    # Closes the output source connection
    def close(self) -> None:
        pass

    # Writes group data to whatever source your implementation uses
    def write_group(self, group: Group) -> None:
        pass