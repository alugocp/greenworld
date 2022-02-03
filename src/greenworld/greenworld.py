from .model.forest import ForestGardenModel
from .model.model import GardenModel
from .types import Niche, Niches, Species
from .math.combinatorics import Combinatorics
from .database.species_test import TestSpeciesData
from .database.niche_test import TestNicheData
from .database.species import SpeciesData
from .database.niche import NicheData
from .printer import Printer
from .group import Group
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
        niches: Niches = self.model.get_niches()
        self.niche_data.initialize_niche_catalogs(niches)
        niche_numbers: Dict[Niche, int] = {}
        total_species = 0
        for niche in niches:
            niche_numbers[niche] = 0
            self.printer.add_line(f'{niche}: 0')
        self.printer.add_line('-----')
        self.printer.add_line('total: 0')
        for species in self.species_data.get_species_iterator():
            niche: Niche = self.model.get_niche_of_species(species)
            self.niche_data.add_to_niche(niche, species)
            niche_numbers[niche] += 1
            total_species += 1
            self.printer.update_line(niches.index(niche), f'{niche}: {niche_numbers[niche]}')
            self.printer.update_line(len(niches) + 1, f'total: {total_species}')
        self.printer.close_stack()
        self.printer.print_line()

        # Grab every combination of species within different niches
        group: Group = Group(niches)
        combos = Combinatorics(niches, niche_numbers)
        groups_visited = 0
        niches_visited = 0
        num_total_groups = combos.get_number_total_groups()
        num_niche_combos = combos.get_number_niche_combinations()
        self.printer.print_line('Iterating through companion groups...')
        self.printer.add_line(f'0/{num_niche_combos} niche combinations')
        self.printer.add_line(f'0/{num_total_groups} companion groups')
        for niche in niches:
            self.printer.add_line(f'{niche}: ---')
        # For every possible number of niches in a submodel
        for n in range(2, len(niches) + 1):
            # For every combination of niches in the submodel
            for subniches in combos.iterate_subset_combinations(n, niches):
                niches_visited += 1
                # Ignore incomplete submodels
                if 0 in list(map(lambda x: niche_numbers[x], subniches)):
                    continue
                # For every combination of species to fill this submodel
                niche_iterables = list(map(lambda x: self.niche_data.get_niche_species_iterable(x), subniches))
                for grouping in combos.iterate_combinations(niche_iterables):
                    for a in range(len(niches)):
                        if niches[a] in subniches:
                            i = subniches.index(niches[a])
                            group.fill_niche(subniches[i], grouping[i])
                            self.printer.update_line(2 + a, f'{niches[a]}: {grouping[i]}')
                        else:
                            group.fill_niche(subniches[i], None)
                            self.printer.update_line(2 + a, f'{niches[a]}: ---')
                    groups_visited += 1
                    self.printer.update_line(0, f'{niches_visited}/{num_niche_combos} niche combinations')
                    self.printer.update_line(1, f'{groups_visited}/{num_total_groups} companion groups')
                    # Calculate a companionship report for the group, perhaps using a previous group for some of the data
        self.printer.update_line(0, f'{niches_visited}/{num_niche_combos} niche combinations')
        self.printer.close_stack()
