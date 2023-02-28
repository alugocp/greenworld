import re
import json
import requests
from greenworld.collection import BaseDataCollector
from greenworld.lib.taxonomy import Taxon

habits_map = {
    'Lichenous': 'GrowthHabit.LICHENOUS',
    'Nonvascular': 'GrowthHabit.NONVASCULAR',
    'Tree': 'GrowthHabit.TREE',
    'Shrub': 'GrowthHabit.SHRUB',
    'Subshrub': 'GrowthHabit.SUBSHRUB',
    'Vine': 'GrowthHabit.VINE',
    'Graminoid': 'GrowthHabit.GRAMINOID',
    'Forb/herb': 'GrowthHabit.FORB'
}

def grab_growth_habit(data):
    for habit, mapped in habits_map.items():
        if habit in data['GrowthHabits']:
            return mapped
    return None

def grab_family(data):
    for ancestor in data['Ancestors']:
        if ancestor['Rank'] == 'Family':
            t = Taxon()
            t.parse_family(ancestor['ScientificName'])
            return t.family
    return None

class UsdaPlantsLookupDataCollector(BaseDataCollector):

    def matches_input(self, key: str) -> bool:
        return re.match(r'^plants.[0-9]+$', key)

    def collect_data(self, key: dict) -> dict:
        species = key['species']

        # Make initial query to USDA (search by scientific name)
        self.gw.log(f'Querying USDA Plants Database for {species}...')
        r1 = requests.post(
            url = 'https://plantsservices.sc.egov.usda.gov/api/PlantSearch',
            data = {
                'Text': species,
                'Field': 'Scientific Name',
                'Locations': None,
                'Groups': None,
                'Durations': None,
                'GrowthHabits': None,
                'WetlandRegions': None,
                'NoxiousLocations': None,
                'InvasiveLocations': None,
                'Countries': None,
                'Provinces': None,
                'Counties': None,
                'Cities': None,
                'Localities': None,
                'ArtistFirstLetters': None,
                'ImageLocations': None,
                'Artists': None,
                'CopyrightStatuses': None,
                'ImageTypes': None,
                'SortBy': 'sortSciName',
                'Offset': -1,
                'FilterOptions': None,
                'UnfilteredPlantIds': None,
                'Type': None,
                'TaxonSearchCriteria': None,
                'MasterId': -1
            }
        )
        result1 = json.loads(r1.text)
        if len(result1['PlantResults']) == 0:
            return {}
        match = result1['PlantResults'][0]
        symbol = match['Symbol']

        # Make second query to USDA (grab family name and growth habit)
        self.gw.log(f'Querying USDA Plants Database for {symbol}...')
        r2 = requests.get(
            url = f'https://plantsservices.sc.egov.usda.gov/api/PlantProfile?symbol={symbol}'
        )
        result2 = json.loads(r2.text)

        # Return aggregated data
        output = {
            'name': match['CommonName'].title(),
            'family': grab_family(result2),
            'growth_habit': grab_growth_habit(result2)
        }
        if not output['growth_habit']:
            del output['growth_habit']
            habit = output['growth_habit']
            self.gw.log(f'Encountered unknown growth habit \'{habit}\'')
        return output
