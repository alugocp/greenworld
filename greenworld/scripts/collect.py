import json
import sys
import re
from greenworld.scripts.enter import json_schema
from greenworld.collection.iweb_xls import IwebXlsDataCollector
from greenworld.collection.usda_plants_local import UsdaPlantsLocalDataCollector
from greenworld.collection.insects_local import InsectsLocalDataCollector

__collectors = [
    IwebXlsDataCollector(),
    UsdaPlantsLocalDataCollector(),
    InsectsLocalDataCollector()
]

# Grabs the appropriate data collector for the requested data
def get_data_collector(key):
    for collector in __collectors:
        if collector.matches_input(key):
            return collector
    return None

# Aggregates secondary missing data to output dicts
def fill_missing_path(data, missing):
    collector = get_data_collector(missing)
    if not collector:
        return
    keys = re.search(r'([a-z]+)\.([0-9]+)', missing).groups()
    old = data[keys[0]][int(keys[1])]
    collected = collector.collect_data(old)
    if collected:
        old.update(collected)

def main(args):
    for arg in args:
        collector = get_data_collector(arg)
        if not collector:
            raise Exception(f'No data collector for input \'{arg}\'')

        # Aggregate data from collectors
        data = collector.collect_data(arg)
        for missing in collector.get_missing_paths():
            fill_missing_path(data, missing)
        collector.clear_missing_paths()

        # Assert and write to file
        assert json_schema.validate(data) == data
        pretty_json = json.dumps(data, indent = 4)
        with open('seed-data/tmp.json', 'w', encoding = 'utf-8') as file:
            file.write(pretty_json)

if __name__ == '__main__':
    main(sys.argv[1:])
