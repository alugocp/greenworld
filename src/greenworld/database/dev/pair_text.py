from greenworld.database.pair import PairData
from greenworld.model.pair import Pair

class TextPairData(PairData):
    path: str

    def __init__(self, path: str):
        self.path = path

    def open(self) -> None:
        with open(self.path, 'w', encoding = 'utf8') as file:
            file.write('')

    def close(self) -> None:
        pass

    def write_pair(self, pair: Pair) -> None:
        with open(self.path, 'a', encoding = 'utf8') as file:
            file.write(f'{pair}\n')
            for suggestion in pair.suggestions:
                file.write(f'{suggestion}\n')
            file.write('\n')
