import sys
from greenworld.greenworld import Greenworld
from greenworld.printer import Printer
printer = Printer(True)

def help_cmd():
    printer.print_line('OVERVIEW: LugoCorp\'s Greenworld algorithm')
    printer.print_line()
    printer.print_line('USAGE: gw [options]')
    printer.print_line()
    printer.print_line('OPTIONS:')
    printer.print_line('\trun\t\tRuns the Greenworld algorithm')
    printer.print_line('\t--help\t\tDisplays helpful information')
    printer.print_line('\t--version\tDisplays version information')

# Displays version info
def version_cmd():
    printer.print_line('Greenworld algorithm v1.0 (alpha)')
    printer.print_line('Designed by LugoCorp')

# Runs the core algorithm
def run_cmd():
    gw = Greenworld()
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
    else:
        help_cmd()
    args.pop(0)