from typing import Iterator, List
from .species import SpeciesData
from ..species import Species
from ..types import Kingdom

# This class represents a test implementation of SpeciesData.
class TestSpeciesData(SpeciesData):
    data: List[Species] = [
        Species(name = 'Corn', latin = 'zea mays'),
        Species(name = 'Beans', latin = 'phaseolus lunatus'),
        Species(name = 'Squash', latin = 'cucurbita moschata'),
        Species(name = 'Watermelon', latin = 'citrullus lanatus'),
        Species(name = 'Cucumber', latin = 'cucumis sativus'),
        Species(
            name = 'Winecap Mushroom',
            latin = 'stropharia rugosa-annulata',
            kingdom = Kingdom.FUNGI
        ),
        Species(name = 'Garlic', latin = 'allium sativum'),
        Species(name = 'Onion', latin = 'allium cepa'),
        Species(name = 'Cherry Tomato', latin = 'solanum lycopersicum'),
        Species(name = 'Basil', latin = 'ocimum basilicum'),
        Species(name = 'Parsley', latin = 'petroselinum crispum'),
        Species(name = 'Mango', latin = 'mangifera indica'),
        Species(name = 'Dragon Fruit', latin = 'selenicereus megalanthus'),
        Species(name = 'Potato', latin = 'solanum tuberosum'),
        Species(name = 'Plantain', latin = 'musa x paradisiaca'),
        Species(name = 'Banana', latin = 'musa acuminata'),
        Species(name = 'Cassava', latin = 'manihot esculenta'),
        Species(name = 'Sunflower', latin = 'helianthus dissectifolius'),
        Species(name = 'Dandelion', latin = 'taraxacum officinale'),
        Species(name = 'Cantaloupe', latin = 'cucumis melo'),
        Species(name = 'Winter Melon', latin = 'benincasa hispida')
    ]

    # Returns an iterator for every species in the data source.
    def get_species_iterator(self) -> Iterator[Species]:
        return self.data.__iter__()