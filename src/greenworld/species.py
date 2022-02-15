from .types import Sunlight, Drainage, PH

# This class represents a single species logged within this project.
# It contains information to help determine an organism's ideal growing
# environment.
class Species:
    pH: PH
    sunlight: Sunlight
    drainage: Drainage
    latin: str
    name: str

    def __init__(self, name: str, latin: str):
        self.latin = latin
        self.name = name

    def __repr__(self) -> str:
        return str(self.name)