from typing import Dict, List

# This class represents a grouping of potential companion species.
class Group:
    species: Dict[str, str]

    def __init__(self, niches: List[str]):
        for niche in niches:
            self.species[niche] = None