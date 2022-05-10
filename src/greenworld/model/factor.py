
# This class represents a factor to consider when growing some
# crops together as companions.
class Factor():
    GOOD: int = 2
    NEUTRAL: int = 1
    BAD: int = 0
    outcome: int
    label: str

    def __init__(self, outcome: int, label: str):
        self.outcome = outcome
        self.label = label

    def __repr__(self):
        outcome = self.outcome_str(self.outcome)
        return f'({outcome}) {self.label}'

    @classmethod
    def outcome_str(cls, outcome: int) -> str:
        return ['BAD', 'NEUTRAL', 'GOOD'][outcome]
