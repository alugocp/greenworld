import logging
import sys
import os
scripts = {}

# Caches the given script if it exists, or otherwise returns None
def get_script(name):
    if name in scripts:
        return scripts[name]
    try:
        imported = __import__(f'scripts.{name}')
        module = getattr(imported, name)
        scripts[name] = getattr(module, 'main')
        return scripts[name]
    except ModuleNotFoundError:
        return None

def main(args):
    os.environ['GREENWORLD_DB'] = 'sqlite:///greenworld.db'
    sys.path.append('./greenworld')
    logging.basicConfig(level=logging.NOTSET)
    a = 0

    while a < len(args):
        script = get_script(args[a])
        if script:
            if a + 1 < len(args) and not get_script(args[a + 1]):
                script(args[a + 1 : ])
                a = len(args)
            else:
                script()
                a += 1
            print("")
        else:
            logging.warning('\'%s\' is not a script', args[a])
            a = len(args)

if __name__ == '__main__':
    main(sys.argv[1:])
