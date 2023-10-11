import json
import sys
from greenworld import Greenworld
from greenworld.collection.logic import collect

__collectors = []

def main(gw, args):
    outputs = collect(gw, args)
    for i, data in enumerate(outputs):
        with open(f"seed-data/tmp{i}.json", "w", encoding="utf-8") as file:
            pretty_json = json.dumps(data, indent=4)
            file.write(pretty_json)

if __name__ == "__main__":
    main(Greenworld(), sys.argv[1:])
