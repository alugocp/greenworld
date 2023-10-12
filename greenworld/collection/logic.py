from greenworld import Greenworld
from greenworld.scripts.enter import json_schema
from greenworld.collection.collectors import get_collectors


# Grabs the appropriate data collector for the requested data
def get_data_collector(collectors, key):
    for collector in collectors:
        if collector.matches_input(key):
            return collector
    return None


# Aggregates secondary missing data to output dicts
def fill_missing_path(collectors, data, missing):
    for collector in collectors:
        if not collector.matches_input(missing):
            continue
        old = collector.get(data, missing)
        collected = collector.collect_data(old)
        if collected:
            collector.fill(data, missing, collected)
            break


def collect(gw: Greenworld, args):
    # Initialize collectors
    collectors = get_collectors(gw, False)

    # Collect data
    outputs = []
    for arg in args:
        collector = get_data_collector(collectors, arg)
        if not collector:
            raise ValueError(f"No data collector for input '{arg}'")

        # Aggregate data from collectors
        data = collector.collect_data(arg)
        for missing in collector.get_missing_paths():
            fill_missing_path(collectors, data, missing)
        collector.clear_missing_paths()
        for other in collectors:
            other.final_fill(data)

        # Assert and write to file
        assert json_schema.validate(data) == data
        outputs.append(data)

    # Cleanup the collectors
    for collector in collectors:
        collector.destroy()

    # Return results
    return outputs
