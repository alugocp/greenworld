from typing import Iterable
from ..types import Niche, Niches
from ..species import Species

# This class represents an interface of niche data access. An implementation may
# connect this interface to a database or other source.
class NicheData:

    # Sets up a couple of lists for cataloging species by their niche.
    def initialize_niche_catalogs(self, niches: Niches) -> None:
        pass

    # Records the given species as belonging to the given niche.
    def add_to_niche(self, niche: Niche, species: Species) -> None:
        pass

    # Returns an iterator for every species in the given niche
    def get_niche_species_iterable(self, niche: Niche) -> Iterable[Species]:
        pass