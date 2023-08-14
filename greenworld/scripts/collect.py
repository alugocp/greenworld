import json
import sys
from greenworld import Greenworld
from greenworld.scripts.enter import json_schema
from greenworld.collection.iweb_xls import IwebXlsDataCollector
from greenworld.collection.usda_plants_local import UsdaPlantsLocalDataCollector
from greenworld.collection.insects_local import InsectsLocalDataCollector
from greenworld.collection.nitrogen_fixers import NitrogenFixersDataCollector

__collectors = []

# Grabs the appropriate data collector for the requested data
def get_data_collector(key):
    for collector in __collectors:
        if collector.matches_input(key):
            return collector
    return None

# Aggregates secondary missing data to output dicts
def fill_missing_path(data, missing):
    for collector in __collectors:
        if not collector.matches_input(missing):
            continue
        old = collector.get(data, missing)
        collected = collector.collect_data(old)
        if collected:
            collector.fill(data, missing, collected)
            break

def main(gw, args):
    # Initialize collectors
    __collectors.append(IwebXlsDataCollector(gw))
    __collectors.append(UsdaPlantsLocalDataCollector(gw))
    __collectors.append(InsectsLocalDataCollector(gw))
    __collectors.append(NitrogenFixersDataCollector(gw))

    # Collect data
    for arg in args:
        collector = get_data_collector(arg)
        if not collector:
            raise ValueError(f'No data collector for input \'{arg}\'')

        # Aggregate data from collectors
        data = collector.collect_data(arg)
        for missing in collector.get_missing_paths():
            fill_missing_path(data, missing)
        collector.clear_missing_paths()
        for other in __collectors:
            other.final_fill(data)

        # Assert and write to file
        assert json_schema.validate(data) == data
        pretty_json = json.dumps(data, indent = 4)
        with open('seed-data/tmp.json', 'w', encoding = 'utf-8') as file:
            file.write(pretty_json)

    for collector in __collectors:
        collector.destroy()

if __name__ == '__main__':
    main(Greenworld(), sys.argv[1:])
