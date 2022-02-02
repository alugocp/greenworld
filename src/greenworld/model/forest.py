from typing import List
from .model import GardenModel

# This class represents the forest garden model.
class ForestGardenModel(GardenModel):

    def get_niches(self) -> List[str]:
        return ['canopy', 'subcanopy', 'shrub', 'herbaceous', 'rhizosphere', 'soil surface', 'vertical']

    def get_niche_of_species(self, species: str) -> str:
        return 'canopy'