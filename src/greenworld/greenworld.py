from typing import Dict, List
from .model.model import GardenModel
from .types import Niche, Niches
from .species import Species
from .math.comparisons import overlaps
from .math.combinatorics import NicheCombinatorics
from .math.combinatorics import iterate_combinations
from .math.combinatorics import iterate_subset_combinations
from .database.species import SpeciesData
from .database.niche import NicheData
from .database.group import GroupData
from .injector import Injector
from .printer import Printer
from .factor import Factor
from .group import Group

# This class is the main algorithm handler for calculating companionship groups.
# It ties all the business logic of this project together.
class Greenworld:
    niche_numbers: Dict[Niche, int]
    species_data: SpeciesData
    niche_data: NicheData
    group_data: GroupData
    model: GardenModel
    printer: Printer
    niches: Niches

    def __init__(self, injector: Injector):
        self.species_data = injector.get_service('species-data')
        self.niche_data = injector.get_service('niche-data')
        self.group_data = injector.get_service('group-data')
        self.model = injector.get_service('garden-model')
        self.printer = injector.get_service('printer')

    # This function is what runs the core algorithm code.
    def calculate_compatibility_scores(self) -> None:
        self.printer.print_line('Initializing Greenworld algorithm...')
        self.species_data.open()
        self.niche_data.open()
        self.group_data.open()
        self.printer.print_line(f'Using model \033[32m\'{self.model.__class__.__name__}\'\033[0m')
        self.printer.print_line()
        self.niches = self.model.get_niches()
        self.niche_numbers = self.catalog_into_niches()
        self.process_groups()
        self.printer.print_line('Closing algorithm resources...')
        self.group_data.close()
        self.niche_data.close()
        self.species_data.close()
        self.printer.print_line('\033[32mDone.\033[0m')

    # This function divides the species data into niches.
    def catalog_into_niches(self) -> Dict[Niche, int]:
        self.printer.print_line('Cataloging species into niches...')
        self.niche_data.initialize_niche_catalogs(self.niches)
        niche_numbers: Dict[Niche, int] = {}
        total_species = 0
        for niche in self.niches:
            niche_numbers[niche] = 0
            self.printer.add_line(f'\033[1m{niche}:\033[0m \033[32m0\033[0m')
        self.printer.add_line('-----')
        self.printer.add_line('\033[1mtotal:\033[0m \033[32m0\033[0m')
        for species in self.species_data.get_species_iterator():
            niche: Niche = self.model.get_niche_of_species(species)
            if niche:
                self.niche_data.add_to_niche(niche, species)
                niche_numbers[niche] += 1
                total_species += 1
                self.printer.update_line(
                    self.niches.index(niche),
                    f'\033[1m{niche}:\033[0m \033[32m{niche_numbers[niche]}\033[0m'
                )
                self.printer.update_line(len(self.niches) + 1,
                    f'\033[1mtotal:\033[0m \033[32m{total_species}\033[0m'
                )
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
        self.printer.add_line(f'\033[32m0/{num_niche_combos}\033[0m niche combinations')
        self.printer.add_line(f'\033[32m0/{num_total_groups}\033[0m companion groups')
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
                        0, f'\033[32m{niches_visited}/{num_niche_combos}\033[0m niche combinations')
                    self.printer.update_line(
                        1, f'\033[32m{groups_visited}/{num_total_groups}\033[0m companion groups')
                    self.update_group(group, subniches, grouping)
                    group.global_factors = calculate_global_compatibility(group)
                    group.model_factors = self.model.calculate_model_compatibility(group)
                    self.group_data.write_group(group)
        self.printer.update_line(0,
            f'\033[32m{niches_visited}/{num_niche_combos}\033[0m niche combinations'
        )
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
                self.printer.update_line(2 + a,
                    f'\033[1m{niche}:\033[0m \033[32m{grouping[i]}\033[0m'
                )
            else:
                group.fill_niche(niche, None)
                self.printer.update_line(2 + a, f'\033[1m{niche}:\033[0m ---')

# This function calculates compatibility data for the given group.
def calculate_global_compatibility(group: Group) -> List[Factor]:
    factors = []
    species = list(filter(lambda x: x is not None, group.species.values()))
    for i1 in range(0, len(species) - 1):
        for i2 in range(i1, len(species)):
            species1 = species[i1]
            species2 = species[i2]
            if not overlaps(species1.pH, species2.pH):
                factors.append(Factor(Factor.BAD,
                    f'{species1} and {species2} require different soil pH levels'
                ))
            if species1.drainage != species2.drainage:
                factors.append(Factor(Factor.BAD,
                    f'{species1} and {species2} require different soil drainage levels'
                ))
            if species1.water != species2.water:
                factors.append(Factor(Factor.NEUTRAL,
                    f'{species1} and {species2} will need different levels of water'
                ))
    return factors