from typing import TextIO
from ..printer import Printer
from .group import GroupData
from ..group import Group

class TextGroupData(GroupData):
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

    def write_group(self, group: Group) -> None:
        for k, v in group.species.items():
            self.printer.print_line(f'{k}: {v}')
        for factor in group.global_factors:
            self.printer.print_line(str(factor))
        self.printer.print_line()