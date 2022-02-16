from typing import List
from ..types import Niches, Niche, Kingdom
from ..species import Species
from .model import GardenModel
from ..factor import Factor
from ..group import Group

# This class represents a companion group with a mycorrhizal fungus and some
# plant root (perhaps an onion, cassava or strawberry).
class MycorrhizalModel(GardenModel):

    def get_niches(self) -> Niches:
        return [
            'fungus',
            'root'
        ]

    def get_niche_of_species(self, species: Species) -> Niche:
        if species.kingdom == Kingdom.FUNGI:
            return 'fungus'
        return 'root'

    def calculate_model_compatibility(self, group: Group) -> List[Factor]:
        return []