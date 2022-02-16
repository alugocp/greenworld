from typing import Iterator, List
from .species import SpeciesData
from ..species import Species
from ..types import Kingdom

# This class represents a JSON-like implementation of SpeciesData.
class JsonSpeciesData(SpeciesData):
    species: List[Species]
    data: List[object] = [
        {
            'name': 'Corn',
            'latin': 'zea mays'
        },
        {
            'name': 'Beans',
            'latin': 'phaseolus lunatus'
        },
        {
            'name': 'Squash',
            'latin': 'cucurbita moschata'
        },
        {
            'name': 'Watermelon',
            'latin': 'citrullus lanatus'
        },
        {
            'name': 'Cucumber',
            'latin': 'cucumis sativus'
        },
        {
            'name': 'Winecap Mushroom',
            'latin': 'stropharia rugosa-annulata',
            'kingdom': Kingdom.FUNGI
        },
        {
            'name': 'Garlic',
            'latin': 'allium sativum'
        },
        {
            'name': 'Onion',
            'latin': 'allium cepa'
        },
        {
            'name': 'Cherry Tomato',
            'latin': 'solanum lycopersicum'
        },
        {
            'name': 'Basil',
            'latin': 'ocimum basilicum'
        },
        {
            'name': 'Parsley',
            'latin': 'petroselinum crispum'
        },
        {
            'name': 'Mango',
            'latin': 'mangifera indica'
        },
        {
            'name': 'Dragon Fruit',
            'latin': 'selenicereus megalanthus'
        },
        {
            'name': 'Potato',
            'latin': 'solanum tuberosum'
        },
        {
            'name': 'Plantain',
            'latin': 'musa x paradisiaca'
        },
        {
            'name': 'Banana',
            'latin': 'musa acuminata'
        },
        {
            'name': 'Cassava',
            'latin': 'manihot esculenta'
        },
        {
            'name': 'Sunflower',
            'latin': 'helianthus dissectifolius'
        },
        {
            'name': 'Dandelion',
            'latin': 'taraxacum officinale'
        },
        {
            'name': 'Cantaloupe',
            'latin': 'cucumis melo'
        },
        {
            'name': 'Winter Melon',
            'latin': 'benincasa hispida'
        }
    ]

    def __init__(self):
        self.species = list(map(lambda data: Species(**data), self.data))

    # Returns an iterator for every species in the data source.
    def get_species_iterator(self) -> Iterator[Species]:
        return self.species.__iter__()