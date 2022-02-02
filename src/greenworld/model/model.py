from typing import List
from ..group import Group

# This class represents an interface for any gardening model. Garden models are
# sets of particular niches that companion species can hold in relation ot one
# another.
class GardenModel:

    # Returns the niches that exist within this model.
    def get_niches(self) -> List[str]:
        pass

    # Returns the niche that a given species would fill in this model.
    def get_niche_of_species(self, species: str) -> str:
        pass

    # Populates a group's model compatibility based on this garden model.
    def calculate_model_compatibility(self, group: Group) -> None:
        pass