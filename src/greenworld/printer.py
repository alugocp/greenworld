from io import TextIOWrapper
from typing import List
from sys import stdout

# This class handles advanced console output. It uses a stack-based model to
# print to multiple lines at a time. ANSII terminal codes are used to get the
# desired effects.
class Printer:
    active: bool
    stack: List[str]
    out: TextIOWrapper

    def __init__(self, active: bool, out: TextIOWrapper = stdout):
        self.active = active
        self.stack = []
        self.out = out

    # This function wraps the buffer output method
    def print(self, msg: str) -> None:
        self.out.write(msg)
        self.out.flush()

    # Just prints a line without any advanced stack features
    def print_line(self, msg: str = '') -> None:
        if self.active:
            if len(self.stack) > 0:
                raise RuntimeError('Cannot use Printer.print_line in a print stack')
            self.print(f'{msg}\n')

    # This function closes the current dynamic print stack
    def close_stack(self) -> None:
        self.stack = []

    # This function adds a line to the stack
    def add_line(self, msg: str) -> None:
        if self.active:
            self.stack.append(msg)
            self.print(f'{msg}\n')

    def add_lines(self, n: int) -> None:
        for a in range(n):
            self.add_line('')

    # This function updates the line at index i on the stack
    def update_line(self, i: int, msg: str) -> None:
        if self.active:
            diff = len(self.stack) - i
            clear = ''.join([' ' * len(self.stack[i])])
            down = ''.join(['\033[B' * diff])
            up = ''.join(['\033[A' * diff])
            self.print(f'{up}\r{clear}\r{msg}\r{down}')
            self.stack[i] = msg