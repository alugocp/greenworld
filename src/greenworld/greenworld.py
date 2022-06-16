from greenworld.math.combinatorics import combination
from greenworld.algorithm.algorithm import Algorithm
from greenworld.database.species import SpeciesData
from greenworld.database.pair import PairData
from greenworld.injector import Injector
from greenworld.model.pair import Pair
from greenworld.printer import Printer

# This class is the main algorithm handler for calculating companionship pairs.
# It ties all the business logic of this project together.
class Greenworld:
    species_data: SpeciesData
    pair_data: PairData
    algorithm: Algorithm
    printer: Printer

    def __init__(self, injector: Injector):
        self.species_data = injector.get_service('species-data')
        self.algorithm = injector.get_service('algorithm')
        self.pair_data = injector.get_service('pair-data')
        self.printer = injector.get_service('printer')

    # This function is what runs the core algorithm code.
    def calculate_compatibility_scores(self) -> None:
        self.printer.print_line('Initializing Greenworld algorithm...')
        for engine in self.algorithm.get_names():
            self.printer.print_line(f'Loaded engine: \033[32m{engine}\033[0m')
        self.species_data.open()
        self.pair_data.open()
        self.process_pairs()
        self.printer.print_line('Closing algorithm resources...')
        self.pair_data.close()
        self.species_data.close()
        self.printer.print_line('\033[32mDone\033[0m')

    # This function iterates through every pair of species.
    def process_pairs(self) -> None:
        total = combination(self.species_data.get_species_count(), 2)
        self.printer.add_lines(3)
        iteration = 1
        for s1 in self.species_data.get_species_iterator():
            for s2 in self.species_data.get_species_iterator(s1):
                msg = f'Calculating pair \033[32m{iteration}\033[0m/\033[32m{total}\033[0m...'
                self.printer.update_line(0, msg)
                self.printer.update_line(1, f'• \033[32m{s1}\033[0m')
                self.printer.update_line(2, f'• \033[32m{s2}\033[0m')
                pair = Pair(s1, s2)
                pair.suggestions = self.algorithm.run(s1, s2)
                self.pair_data.write_pair(pair)
                iteration += 1
        self.printer.close_stack()
