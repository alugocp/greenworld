from .model.forest import ForestGardenModel
from .model.model import GardenModel
from .database.species_test import TestSpeciesData
from .database.niche_test import TestNicheData
from .database.species import SpeciesData
from .database.niche import NicheData
from typing import List

# This class is the main algorithm handler for calculating companionship groups.
# It ties all the business logic of this project together.
class Greenworld:

    # This function is what runs the core algorithm code.
    def calculate_groups(self) -> None:
        model: GardenModel = ForestGardenModel()
        species_data: SpeciesData = TestSpeciesData()
        niche_data: NicheData = TestNicheData()

        # Divide species into model niches
        niches: List[str] = model.get_niches()
        niche_data.initialize_niche_catalogs(niches)
        for species in species_data.get_species_iterator():
            niche: str = model.get_niche_of_species(species)
            niche_data.add_to_niche(niche, species)

        # Grab every combination of species within different niches
        # Calculate a companionship report for the group, perhaps using a previous group for some of the data