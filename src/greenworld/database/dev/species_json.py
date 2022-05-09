from typing import Iterator, List
from greenworld.model.types import Kingdom, Sunlight, Drainage, Water
from greenworld.database.species import SpeciesData
from greenworld.model.species import Species

# This class represents a JSON-like implementation of SpeciesData.
class JsonSpeciesData(SpeciesData):
    species: List[Species]
    data: List[object] = [
        {
            'name': 'Corn',
            'latin': 'zea mays',
            'pH': (6.0, 6.5),
            'water': Water.LOW,
            'drainage': Drainage.SOMEWHAT_POORLY_DRAINED,
            'sunlight': Sunlight.FULL_SUN,
            'height': (2.0, 2.0)
        },
        {
            'name': 'Lima Bean',
            'latin': 'phaseolus lunatus',
            'pH': (6.0, 6.8),
            'water': Water.LOW,
            'sunlight': Sunlight.FULL_SUN,
            'height': (6.0, 6.0)
        },
        {
            'name': 'Butternut Squash',
            'latin': 'cucurbita moschata',
            'pH': (6.0, 6.5),
            'water': Water.LOW,
            'sunlight': Sunlight.FULL_SUN,
            'height': (0.6, 0.6)
        },
        {
            'name': 'Watermelon',
            'latin': 'citrullus lanatus',
            'pH': (6.0, 6.8),
            'water': Water.VERY_LOW,
            'sunlight': Sunlight.FULL_SUN,
            'height': (0.5, 0.5)
        },
        {
            'name': 'Cucumber',
            'latin': 'cucumis sativus',
            'pH': (6.0, 7.0),
            'water': Water.LOW,
            'sunlight': Sunlight.FULL_SUN,
            'height': (2.0, 2.0)
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
            'name': 'Yellow Dragon Fruit',
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
            'latin': 'cucumis melo',
            'pH': (6.0, 6.5),
            'water': Water.VERY_LOW,
            'sunlight': Sunlight.FULL_SUN,
            'height': (1.5, 1.5)
        },
        {
            'name': 'Winter Melon',
            'latin': 'benincasa hispida',
            'pH': (5.8, 6.8),
            'water': Water.VERY_LOW,
            'sunlight': Sunlight.FULL_SUN,
            'height': (6.0, 6.0)
        },
        {
            'name': 'Annabelle Hydrangea',
            'latin': 'hydrangea aborescens',
            'pH': (6.0, 6.5),
            'water': Water.LOW,
            'drainage': Drainage.WELL_DRAINED,
            'sunlight': Sunlight.LIGHT_SHADE,
            'height': (3.0, 3.0)
        },
        {
            'name': 'Asparagus',
            'latin': 'asparagus officinalis'
        },
        {
            'name': 'Parsley',
            'latin': 'petroselinum crispum'
        },
        {
            'name': 'Basil',
            'latin': 'ocimum basilicum'
        },
        {
            'name': 'Beetroot',
            'latin': 'beta vulgaris'
        },
        {
            'name': 'Lettuce',
            'latin': 'lactuca sativa'
        },
        {
            'name': 'Broccoli',
            'latin': 'brassica oleracea'
        },
        {
            'name': 'Sweet Cherry',
            'latin': 'prunus avium'
        },
        {
            'name': 'Spinach',
            'latin': 'spinacia oleracea'
        },
        {
            'name': 'Rosemary',
            'latin': 'salvia rosmarinus'
        },
        {
            'name': 'Bottle Gourd',
            'latin': 'lagenaria siceraria'
        },
        {
            'name': 'Radish',
            'latin': 'raphanus raphanistrum'
        },
        {
            'name': 'Marigold',
            'latin': 'calendula officinalis'
        },
        {
            'name': 'Pumpkin',
            'latin': 'cucurbita maxima'
        },
        {
            'name': 'Pinto Bean',
            'latin': 'phaseolus vulgaris'
        }
    ]

    def __init__(self):
        self.species = list(map(lambda data: Species(**data), self.data))

    # Returns an iterator for every species in the data source.
    # If 'species' is provided, then return an iterator for every
    # species after the provided one.
    def get_species_iterator(self, species: Species = None) -> Iterator[Species]:
        if species:
            return self.species[self.species.index(species) + 1:].__iter__()
        return self.species.__iter__()

    # Returns the number of species in this data set
    def get_species_count(self) -> int:
        return len(self.species)
