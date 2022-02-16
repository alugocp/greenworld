from typing import Iterator, List
from ..species import Species

# This class represents a test implementation of SpeciesData.
class TestSpeciesData:
    data: List[Species] = [
        Species('Corn', 'zea mays'),
        Species('Beans', 'phaseolus lunatus'),
        Species('Squash', 'cucurbita moschata'),
        Species('Watermelon', 'citrullus lanatus'),
        Species('Cucumber', 'cucumis sativus'),
        Species('Mushroom', 'stropharia rugosa-annulata'),
        Species('Garlic', 'allium sativum'),
        Species('Onion', 'allium cepa'),
        Species('Cherry Tomato', 'solanum lycopersicum'),
        Species('Basil', 'ocimum basilicum'),
        Species('Parsley', 'petroselinum crispum'),
        Species('Mango', 'mangifera indica'),
        Species('Dragon Fruit', 'selenicereus megalanthus'),
        Species('Potato', 'solanum tuberosum'),
        Species('Plantain', 'musa x paradisiaca'),
        Species('Banana', 'musa acuminata'),
        Species('Cassava', 'manihot esculenta'),
        Species('Sunflower', 'helianthus dissectifolius'),
        Species('Dandelion', 'taraxacum officinale'),
        Species('Cantaloupe', 'cucumis melo'),
        Species('Winter Melon', 'benincasa hispida')
    ]

    # Returns an iterator for every species in the data source.
    def get_species_iterator(self) -> Iterator[Species]:
        return self.data.__iter__()