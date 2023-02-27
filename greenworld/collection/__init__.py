
class BaseDataCollector:

    # Should return True if this subclass is designed to handle the given input
    def matches_input(self, filename: str) -> bool:
        raise NotImplementedError()

    # Returns some data to fill out the requested input
    def collect_data(self, filename: str) -> dict:
        raise NotImplementedError()
