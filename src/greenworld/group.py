from typing import Dict, Iterator, List
from .types import Niche, Niches
from .species import Species
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

    # Returns an iterator for the species in this group
    def get_species_iterator(self) -> Iterator[Species]:
        return filter(lambda x: x is not None, self.species.values()).__iter__()