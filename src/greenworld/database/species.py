from typing import Iterator
from ..species import Species
from .data import Data

# This class represents an interface of species data access. An implementation
# may connect this interface to a database or other source.
class SpeciesData(Data):

    # Returns the number of species in this data set
    def get_species_count(self) -> int:
        pass

    # Returns an iterator for every species in the data source.
    def get_species_iterator(self, species: Species = None) -> Iterator[Species]:
        pass
