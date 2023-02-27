import json
# import sys
from greenworld.scripts.enter import json_schema
from greenworld.collection.iweb_xls import IwebXlsDataCollector

__collectors = [
    IwebXlsDataCollector()
]

def get_data_collector(filename):
    for collector in __collectors:
        if collector.matches_input(filename):
            return collector
    return None

def main(args):
    for arg in args:
        collector = get_data_collector(arg)
        if not collector:
            raise Exception(f'No data collector for input \'{arg}\'')
        data = collector.collect_data(arg)
        assert json_schema.validate(data) == data
        pretty_json = json.dumps(data, indent = 4)
        with open('seed-data/tmp.json', 'w', encoding = 'utf-8') as file:
            file.write(pretty_json)

if __name__ == '__main__':
    # main(sys.argv[1:])
    main(['referenced-data/clements_1923.xls'])
