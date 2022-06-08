from typing import Iterator, List
from greenworld.database.species import SpeciesData
from greenworld.model.species import Species

"""
- Data to add for each crop -
habit: Growth habit enum
duration: Lifetime enum
sunlight: Preferred sunlight enum
drainage: Preferred soil drainage enum
kingdom: Taxonomic kingdom
water: Preferred water enum
height: height range
roots: roots length range
pH: Preferred soil pH range
"""

# This class represents an implementation SpeciesData for unit tests.
class TestSpeciesData(SpeciesData):
    species: List[Species]
    data: List[object] = [
        {
            'name': 'potato',
            'latin': 'solanum tuberosum',
            'habit': GrowthHabit.HERB,
            'duration': Duration.PERENNIAL,
            'sunlight': Sunlight.FULL_SUN,
            'drainage': Drainage.WELL_DRAINED,
            'kingdom': Kingdom.PLANT,
            'pH': (5.8, 6.5)
        },
        {
            'name': 'tomato',
            'latin': 'solanum lycopersicum'
        },
        {
            'name': 'onion',
            'latin': 'allium cepa'
        },
        {
            'name': 'corn',
            'latin': 'zea mays'
        },
        {
            'name': 'squash',
            'latin': 'cucurbita moschata'
        },
        {
            'name': 'beans',
            'latin': 'phaseolus vulgaris'
        },
        {
            'name': 'mint',
            'latin': 'mentha spicata'
        },
        {
            'name': 'watermelon',
            'latin': 'citrullus lanatus'
        },
        {
            'name': 'parsley',
            'latin': 'petroselinum crispum'
        },
        {
            'name': 'basil',
            'latin': 'ocimum basilicum'
        },
        {
            'name': 'garlic',
            'latin': 'allium sativum'
        },
        {
            'name': 'chives',
            'latin': 'allium schoenoprasum'
        },
        {
            'name': 'sunflower',
            'latin': 'helianthus annuus'
        },
        {
            'name': 'kohlrabi',
            'latin': 'brassica oleracea'
        },
        {
            'name': 'nasturtium',
            'latin': 'tropaeolum majus'
        },
        {
            'name': 'dill',
            'latin': 'anethum graveolens'
        },
        {
            'name': 'carrots',
            'latin': 'daucus carota'
        },
        {
            'name': 'peas',
            'latin': 'pisum sativum'
        },
        {
            'name': 'peppers',
            'latin': 'capsicum annuum'
        },
        {
            'name': 'marigold',
            'latin': 'calendula officinalis'
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
