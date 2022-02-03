from .types import Niche, Niches, Species
from typing import Dict, List

# This class represents a grouping of potential companion species.
class Group:
    species: Dict[Niche, Species] = {}

    def __init__(self, niches: Niches):
        for niche in niches:
            self.species[niche] = None

    def __repr__(self) -> str:
        return str(self.species)

    # This function sets the species for the given niche within this group
    def fill_niche(self, niche: Niche, species: Species) -> None:
        self.species[niche] = species