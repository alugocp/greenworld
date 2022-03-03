from typing import List
from ..types import Niches, Niche
from ..species import Species
from .model import GardenModel
from ..factor import Factor
from ..group import Group

# This class represents the forest garden model.
class ForestGardenModel(GardenModel):

    def get_niches(self) -> Niches:
        return [
            'canopy',
            'subcanopy',
            'shrub',
            'herbaceous',
            'rhizosphere',
            'soil surface',
            'vertical'
        ]

    def get_niche_of_species(self, species: Species) -> Niche:
        if species.height[0] >= 9.0:
            return 'canopy'
        if species.height[0] >= 3.0:
            return 'subcanopy'
        return 'shrub'

    def calculate_model_compatibility(self, group: Group) -> List[Factor]:
        return []