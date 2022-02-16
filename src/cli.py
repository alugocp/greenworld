import sys
from greenworld.greenworld import Greenworld
from greenworld.database.species_json import JsonSpeciesData
from greenworld.database.niche_test import TestNicheData
from greenworld.database.group_text import TextGroupData
from greenworld.model.mycorrhizal import MycorrhizalModel
from greenworld.model.forest import ForestGardenModel
from greenworld.model.model import GardenModel
from greenworld.injector import Injector
from greenworld.printer import Printer
printer = Printer(True)

def help_cmd():
    printer.print_line('OVERVIEW: LugoCorp\'s Greenworld algorithm')
    printer.print_line()
    printer.print_line('USAGE: gw [options]')
    printer.print_line()
    printer.print_line('OPTIONS:')
    printer.print_line('\trun [model]\tRuns the Greenworld algorithm with a given model')
    printer.print_line('\t\t\tmodels: forest (default), mycorrhizal')
    printer.print_line('\t--help\t\tDisplays helpful information')
    printer.print_line('\t--version\tDisplays version information')

# Displays version info
def version_cmd():
    printer.print_line('Greenworld algorithm v1.0 (alpha)')
    printer.print_line('Designed by LugoCorp')

# Runs the core algorithm
def run_cmd():
    model = args[1] if len(args) > 1 else 'forest'
    garden_model: GardenModel = ForestGardenModel()
    if model == 'mycorrhizal':
        garden_model = MycorrhizalModel()
    injector = Injector()
    injector.register_service('printer', printer)
    injector.register_service('garden-model', garden_model)
    injector.register_service('species-data', JsonSpeciesData())
    injector.register_service('niche-data', TestNicheData())
    injector.register_service('group-data', TextGroupData('output.txt'))
    gw = Greenworld(injector)
    gw.calculate_compatibility_scores()

# Parse arguments
args = sys.argv[1:]
if len(args) == 0:
    help_cmd()
while len(args) > 0:
    arg = args[0]
    if arg == '--help':
        help_cmd()
    elif arg == '--version':
        version_cmd()
    elif arg == 'run':
        run_cmd()
        if len(args) > 1:
            args.pop(0)
    else:
        help_cmd()
    args.pop(0)