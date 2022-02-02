from .model.forest import ForestGardenModel
from .model.model import GardenModel
from .database.species_test import TestSpeciesData
from .database.niche_test import TestNicheData
from .database.species import SpeciesData
from .database.niche import NicheData
from .printer import Printer
from typing import Dict, List

# This class is the main algorithm handler for calculating companionship groups.
# It ties all the business logic of this project together.
class Greenworld:
    printer: Printer = Printer(True)
    model: GardenModel = ForestGardenModel()
    species_data: SpeciesData = TestSpeciesData()
    niche_data: NicheData = TestNicheData()

    # This function is what runs the core algorithm code.
    def calculate_groups(self) -> None:

        # Startup information
        self.printer.print_line('Initializing Greenworld algorithm...')
        self.printer.print_line(f'Using model \'{self.model.__class__.__name__}\'')
        self.printer.print_line()

        # Divide species into model niches
        self.printer.print_line('Cataloging species into niches...')
        niches: List[str] = self.model.get_niches()
        self.niche_data.initialize_niche_catalogs(niches)
        niche_numbers: Dict[str, int] = {}
        total = 0
        for niche in niches:
            niche_numbers[niche] = 0
            self.printer.add_line(f'{niche}: 0')
        self.printer.add_line('-----')
        self.printer.add_line('total: 0')
        for species in self.species_data.get_species_iterator():
            niche: str = self.model.get_niche_of_species(species)
            self.niche_data.add_to_niche(niche, species)
            niche_numbers[niche] += 1
            total += 1
            self.printer.update_line(niches.index(niche), f'{niche}: {niche_numbers[niche]}')
            self.printer.update_line(len(niches) + 1, f'total: {total}')
        self.printer.close_stack()
        self.printer.print_line()

        # Grab every combination of species within different niches
        # Calculate a companionship report for the group, perhaps using a previous group for some of the data