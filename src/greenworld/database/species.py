from ..types import Species
from typing import Iterator

# This class represents an interface of species data access. An implementation
# may connect this interface to a database or other source.
class SpeciesData:

    # Returns an iterator for every species in the data source.
    def get_species_iterator(self) -> Iterator[Species]:
        pass