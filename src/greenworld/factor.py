
# This class represents a factor to consider when growing some
# crops together as companions.
class Factor():
    GOOD: int = 1
    NEUTRAL: int = 0
    BAD: int = -1
    outcome: int
    label: str

    def __init__(self, outcome: int, label: str):
        self.outcome = outcome
        self.label = label