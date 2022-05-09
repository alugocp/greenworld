from typing import TextIO
from ..printer import Printer
from .pair import PairData
from ..pair import Pair

class TextPairData(PairData):
    printer: Printer
    file: TextIO
    path: str

    def __init__(self, path: str):
        self.path = path

    def open(self) -> None:
        self.file = open(self.path, 'w', encoding = 'utf8')
        self.printer = Printer(True, self.file)

    def close(self) -> None:
        self.file.close()

    def write_pair(self, pair: Pair) -> None:
        self.printer.print_line(str(pair))
        for factor in pair.factors:
            self.printer.print_line(str(factor))
        self.printer.print_line()