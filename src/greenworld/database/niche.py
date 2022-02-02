from typing import List

# This class represents an interface of niche data access. An implementation may
# connect this interface to a database or other source.
class NicheData:

    # Sets up a couple of lists for cataloging species by their niche.
    def initialize_niche_catalogs(self, niches: List[str]) -> None:
        pass

    # Records the given species as belonging to the given niche.
    def add_to_niche(self, niche: str, species: str) -> None:
        pass