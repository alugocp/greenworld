
# This class represents any abstract data I/O connection. It is extended for
# specific data use cases.
class Data:

    # Opens the output source connection
    def open(self) -> None:
        pass

    # Closes the output source connection
    def close(self) -> None:
        pass