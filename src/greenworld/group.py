from typing import Dict, List
from .types import Niche, Niches, Species
from .factor import Factor

# This class represents a grouping of potential companion species.
class Group:
    species: Dict[Niche, Species] = {}
    global_factors: List[Factor]
    model_factors: List[Factor]

    def __init__(self, niches: Niches):
        for niche in niches:
            self.species[niche] = None

    def __repr__(self) -> str:
        return str(self.species)

    # This function sets the species for the given niche within this group
    def fill_niche(self, niche: Niche, species: Species) -> None:
        self.species[niche] = species