from typing import Dict, List

# This class represents a grouping of potential companion species.
class Group:
    species: Dict[str, str] = {}

    def __init__(self, niches: List[str]):
        for niche in niches:
            self.species[niche] = None

    def __repr__(self):
        return str(self.species)

    # This function sets the species for the given niche within this group
    def fill_niche(self, niche: str, species: str) -> None:
        self.species[niche] = species