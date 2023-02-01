import logging
import sys
import os

def main(args):
    os.environ['GREENWORLD_DB'] = 'sqlite:///greenworld.db'
    sys.path.append('./greenworld')
    logging.basicConfig(level=logging.NOTSET)
    for arg in args:
        try:
            imported = __import__(f'scripts.{arg}')
            module = getattr(imported, arg)
            func = getattr(module, 'main')
            func()
            print("")
        except ModuleNotFoundError:
            logging.warning('\'%s\' is not a script', arg)

if __name__ == '__main__':
    main(sys.argv[1:])