import sys
from greenworld.greenworld import Greenworld
from greenworld.database.dev.pair_text import TextPairData
from greenworld.database.dev.species_json import JsonSpeciesData
from greenworld.algorithm.init import algorithm
from greenworld.injector import Injector
from greenworld.printer import Printer
printer = Printer(True)

def help_cmd():
    printer.print_line('OVERVIEW: LugoCorp\'s Greenworld algorithm')
    printer.print_line()
    printer.print_line('USAGE: gw [options]')
    printer.print_line()
    printer.print_line('OPTIONS:')
    printer.print_line('\trun\t\tRuns the core algorithm')
    printer.print_line('\t--help\t\tDisplays helpful information')
    printer.print_line('\t--version\tDisplays version information')

# Displays version info
def version_cmd():
    printer.print_line('Greenworld algorithm v1.0 (alpha)')
    printer.print_line('Designed by LugoCorp')

# Runs the core algorithm
def run_cmd():
    injector = Injector()
    injector.register_service('printer', printer)
    injector.register_service('species-data', JsonSpeciesData())
    injector.register_service('pair-data', TextPairData('output.txt'))
    injector.register_service('algorithm', algorithm)
    gw = Greenworld(injector)
    gw.calculate_compatibility_scores()

# Parse arguments
args = sys.argv[1:]
if len(args) == 0:
    help_cmd()
while len(args) > 0:
    arg = args[0]
    if arg == '--version':
        version_cmd()
    elif arg == 'run':
        run_cmd()
    else:
        help_cmd()
    args.clear()
