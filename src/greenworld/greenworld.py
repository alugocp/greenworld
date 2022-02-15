from typing import Dict, List
from .model.forest import ForestGardenModel
from .model.model import GardenModel
from .types import Niche, Niches
from .species import Species
from .math.combinatorics import NicheCombinatorics
from .math.combinatorics import iterate_combinations
from .math.combinatorics import iterate_subset_combinations
from .database.species_test import TestSpeciesData
from .database.niche_test import TestNicheData
from .database.species import SpeciesData
from .database.niche import NicheData
from .printer import Printer
from .group import Group

# This class is the main algorithm handler for calculating companionship groups.
# It ties all the business logic of this project together.
class Greenworld:
    printer: Printer = Printer(True)
    model: GardenModel = ForestGardenModel()
    species_data: SpeciesData = TestSpeciesData()
    niche_data: NicheData = TestNicheData()
    niche_numbers: Dict[Niche, int]
    niches: Niches

    # This function is what runs the core algorithm code.
    def calculate_compatibility_scores(self) -> None:
        self.printer.print_line('Initializing Greenworld algorithm...')
        self.printer.print_line(f'Using model \'{self.model.__class__.__name__}\'')
        self.printer.print_line()
        self.niches = self.model.get_niches()
        self.niche_numbers = self.catalog_into_niches()
        self.process_groups()
        self.printer.print_line('Done.')

    # This function divides the species data into niches.
    def catalog_into_niches(self) -> Dict[Niche, int]:
        self.printer.print_line('Cataloging species into niches...')
        self.niche_data.initialize_niche_catalogs(self.niches)
        niche_numbers: Dict[Niche, int] = {}
        total_species = 0
        for niche in self.niches:
            niche_numbers[niche] = 0
            self.printer.add_line(f'{niche}: 0')
        self.printer.add_line('-----')
        self.printer.add_line('total: 0')
        for species in self.species_data.get_species_iterator():
            niche: Niche = self.model.get_niche_of_species(species)
            if niche:
                self.niche_data.add_to_niche(niche, species)
                niche_numbers[niche] += 1
                total_species += 1
                self.printer.update_line(
                    self.niches.index(niche),
                    f'{niche}: {niche_numbers[niche]}'
                )
                self.printer.update_line(len(self.niches) + 1, f'total: {total_species}')
        self.printer.close_stack()
        self.printer.print_line()
        return niche_numbers

    # This function iterates through every group of species from different niches.
    def process_groups(self) -> None:
        groups_visited = 0
        niches_visited = 0
        group: Group = Group(self.niches)
        combos = NicheCombinatorics(self.niches, self.niche_numbers)
        num_niche_combos = combos.get_number_niche_combinations()
        num_total_groups = combos.get_number_total_groups()
        self.printer.print_line('Calculating companion groups...')
        self.printer.add_line(f'0/{num_niche_combos} niche combinations')
        self.printer.add_line(f'0/{num_total_groups} companion groups')
        for niche in self.niches:
            self.printer.add_line(f'{niche}: ---')
        # For every possible number of niches in a submodel
        for n in range(2, len(self.niches) + 1):
            # For every combination of niches in the submodel
            for subniches in iterate_subset_combinations(n, self.niches):
                niches_visited += 1
                # Ignore incomplete submodels
                if 0 in list(map(lambda x: self.niche_numbers[x], subniches)):
                    continue
                # For every combination of species to fill this submodel
                niche_iterables = list(map(self.niche_data.get_niche_species_iterable, subniches))
                for grouping in iterate_combinations(niche_iterables):
                    groups_visited += 1
                    self.printer.update_line(
                        0, f'{niches_visited}/{num_niche_combos} niche combinations')
                    self.printer.update_line(
                        1, f'{groups_visited}/{num_total_groups} companion groups')
                    self.update_group(group, subniches, grouping)
                    self.calculate_global_compatibility(group)
                    self.model.calculate_model_compatibility(group)
                    # Write the group to the database
        self.printer.update_line(0, f'{niches_visited}/{num_niche_combos} niche combinations')
        self.printer.close_stack()
        self.printer.print_line()

    # Updates the niches and species of the given group.
    def update_group(self, group: Group, subniches: Niches, grouping: List[Species]) -> None:
        group.model_factors = []
        group.global_factors = []
        for a, niche in enumerate(self.niches):
            if niche in subniches:
                i = subniches.index(niche)
                group.fill_niche(niche, grouping[i])
                self.printer.update_line(2 + a, f'{niche}: {grouping[i]}')
            else:
                group.fill_niche(niche, None)
                self.printer.update_line(2 + a, f'{niche}: ---')

    # This function calculates compatibility data for the given group.
    def calculate_global_compatibility(self, group: Group) -> None:
        # Calculate a companionship report for the group, perhaps using a previous group for some of
        # the data.
        pass