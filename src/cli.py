from greenworld.greenworld import Greenworld
from greenworld.printer import Printer
import sys
printer = Printer(True)

# Displays helpful information
def help():
    printer.print_line('OVERVIEW: LugoCorp\'s Greenworld algorithm')
    printer.print_line()
    printer.print_line('USAGE: gw [options]')
    printer.print_line()
    printer.print_line('OPTIONS:')
    printer.print_line('\trun\t\tRuns the Greenworld algorithm')
    printer.print_line('\t--help\t\tDisplays helpful information')
    printer.print_line('\t--version\tDisplays version information')

# Displays version info
def version():
    printer.print_line('Greenworld algorithm v1.0 (alpha)')
    printer.print_line('Designed by LugoCorp')

# Runs the core algorithm
def run():
    gw = Greenworld()
    gw.calculate_groups()

# Parse arguments
args = sys.argv[1:]
if len(args) == 0:
    help()
while len(args):
    arg = args[0]
    if arg == '--help':
        help()
    elif arg == '--version':
        version()
    elif arg == 'run':
        run()
    else:
        help()
    args.pop(0)