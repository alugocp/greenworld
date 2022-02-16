from typing import List
from ..types import Niches, Niche
from ..species import Species
from .model import GardenModel
from ..factor import Factor
from ..group import Group

# This class represents the forest garden model.
class ForestGardenModel(GardenModel):
    latest_niche: int = 0

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
        # This is a placeholder even spread algorithm for now
        niches = self.get_niches()
        result = niches[self.latest_niche]
        self.latest_niche += 1
        if self.latest_niche == len(niches):
            self.latest_niche = 0
        return result

    def calculate_model_compatibility(self, group: Group) -> List[Factor]:
        return []