from typing import List
from .species import Species
from .math.comparisons import overlaps
from .math.combinatorics import combination
from .database.species import SpeciesData
from .database.pair import PairData
from .injector import Injector
from .printer import Printer
from .factor import Factor
from .pair import Pair

# This class is the main algorithm handler for calculating companionship pairs.
# It ties all the business logic of this project together.
class Greenworld:
    species_data: SpeciesData
    pair_data: PairData
    printer: Printer

    def __init__(self, injector: Injector):
        self.species_data = injector.get_service('species-data')
        self.pair_data = injector.get_service('pair-data')
        self.printer = injector.get_service('printer')

    # This function is what runs the core algorithm code.
    def calculate_compatibility_scores(self) -> None:
        self.printer.print_line('Initializing Greenworld algorithm...')
        self.species_data.open()
        self.pair_data.open()
        self.process_pairs()
        self.printer.print_line('Closing algorithm resources...')
        self.pair_data.close()
        self.species_data.close()
        self.printer.print_line('\033[32mDone.\033[0m')

    # This function iterates through every pair of species.
    def process_pairs(self) -> None:
        pair = Pair()
        total = combination(self.species_data.get_species_count(), 2)
        self.printer.add_lines(3)
        iteration = 1
        for s1 in self.species_data.get_species_iterator():
            for s2 in self.species_data.get_species_iterator(s1):
                msg = f'Calculating pair \033[32m{iteration}\033[0m/\033[32m{total}\033[0m...'
                self.printer.update_line(0, msg)
                self.printer.update_line(1, f'• \033[32m{s1}\033[0m')
                self.printer.update_line(2, f'• \033[32m{s2}\033[0m')
                pair.reset(s1, s2)
                pair.factors = calculate_compatibility(s1, s2)
                self.pair_data.write_pair(pair)
                iteration += 1
        self.printer.close_stack()

# This function calculates a compatibility report for the given pair of species.
def calculate_compatibility(s1: Species, s2: Species) -> List[Factor]:
    factors = []
    if not overlaps(s1.pH, s2.pH):
        factors.append(Factor(Factor.BAD,
            f'{s1} and {s2} require different soil pH levels'
        ))
    if s1.drainage != s2.drainage:
        factors.append(Factor(Factor.BAD,
            f'{s1} and {s2} require different soil drainage levels'
        ))
    if s1.water != s2.water:
        factors.append(Factor(Factor.NEUTRAL,
            f'{s1} and {s2} will need different levels of water'
        ))
    return factors
