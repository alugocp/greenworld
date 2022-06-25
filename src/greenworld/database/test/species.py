from typing import Iterator, List
from greenworld.database.species import SpeciesData
from greenworld.model.species import Species
from greenworld.model.types import GrowthHabit
from greenworld.model.types import Duration
from greenworld.model.types import Sunlight
from greenworld.model.types import Drainage
from greenworld.model.types import Kingdom
from greenworld.model.types import Water

# Data to add for each crop
# habit: Growth habit enum
# duration: Lifetime enum
# sunlight: Preferred sunlight enum
# drainage: Preferred soil drainage enum
# kingdom: Taxonomic kingdom
# water: Preferred water enum
# height: height range
# roots: roots length range
# pH: Preferred soil pH range

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
            'water': Water.MODERATE,
            'height': (1.0, 1.0),
            'roots': (0.6, 0.6),
            'pH': (5.8, 6.5)
        },
        {
            'name': 'tomato',
            'latin': 'solanum lycopersicum',
            'habit': GrowthHabit.VINE,
            'duration': Duration.ANNUAL,
            'sunlight': Sunlight.FULL_SUN,
            'drainage': Drainage.WELL_DRAINED,
            'kingdom': Kingdom.PLANT,
            'water': Water.MODERATE,
            'height': (0.91, 1.22),
            'roots': (0.3, 0.3),
            'pH': (6.2, 6.8)
        },
        {
            'name': 'onion',
            'latin': 'allium cepa',
            'habit': GrowthHabit.HERB,
            'duration': Duration.BIENNIAL,
            'sunlight': Sunlight.FULL_SUN,
            'drainage': Drainage.SOMEWHAT_EXCESSIVELY_DRAINED,
            'kingdom': Kingdom.PLANT,
            'water': Water.MODERATE,
            'height': (0.75, 1.8),
            'roots': (0.3, 0.76),
            'pH': (6.0, 7.0)
        },
        {
            'name': 'corn',
            'latin': 'zea mays',
            'habit': GrowthHabit.GRAMINOID,
            'duration': Duration.ANNUAL,
            'sunlight': Sunlight.FULL_SUN,
            'drainage': Drainage.WELL_DRAINED,
            'kingdom': Kingdom.PLANT,
            'water': Water.MODERATE,
            'height': (1.52, 3.66),
            'roots': (0.15, 0.75),
            'pH': (5.8, 6.2)
        },
        {
            'name': 'squash',
            'latin': 'cucurbita moschata',
            'habit': GrowthHabit.VINE,
            'duration': Duration.ANNUAL,
            'sunlight': Sunlight.FULL_SUN,
            'drainage': Drainage.WELL_DRAINED,
            'kingdom': Kingdom.PLANT,
            'water': Water.MODERATE,
            'height': (1.52, 2.44),
            'roots': (0.3, 0.6),
            'pH': (6.0, 6.5)
        },
        {
            'name': 'beans',
            'latin': 'phaseolus vulgaris',
            'habit': GrowthHabit.VINE,
            'duration': Duration.ANNUAL,
            'sunlight': Sunlight.FULL_SUN,
            'drainage': Drainage.WELL_DRAINED,
            'kingdom': Kingdom.PLANT,
            'water': Water.MODERATE,
            'height': (1.5, 3.0),
            'roots': (0.46, 0.61),
            'pH': (6.0, 7.0)
        },
        {
            'name': 'mint',
            'latin': 'mentha spicata',
            'habit': GrowthHabit.HERB,
            'duration': Duration.PERENNIAL,
            'sunlight': Sunlight.PARTIAL_SHADE,
            'drainage': Drainage.WELL_DRAINED,
            'kingdom': Kingdom.PLANT,
            'water': Water.LOW,
            'height': (0.025, 0.152),
            'roots': (0.05, 0.61),
            'pH': (6.0, 7.5)
        },
        {
            'name': 'watermelon',
            'latin': 'citrullus lanatus',
            'habit': GrowthHabit.VINE,
            'duration': Duration.ANNUAL,
            'sunlight': Sunlight.FULL_SUN,
            'drainage': Drainage.WELL_DRAINED,
            'kingdom': Kingdom.PLANT,
            'water': Water.HIGH,
            'height': (1.829, 2.438),
            'roots': (0.203, 0.254),
            'pH': (6.0, 6.8)
        }
    ]
    """
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
    """

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
