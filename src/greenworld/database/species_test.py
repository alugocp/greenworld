from typing import Iterator, List
from ..types import Species

# This class represents a test implementation of SpeciesData.
class TestSpeciesData:
    data: List[Species] = [
        'Corn',
        'Beans',
        'Squash',
        'Watermelon',
        'Cucumber',
        'Mushroom',
        'Garlic',
        'Onion',
        'Tomato',
        'Basil',
        'Parsley',
        'Mango',
        'Dragon Fruit',
        'Potato',
        'Plantain',
        'Banana',
        'Cassava',
        'Sunflower',
        'Dandelion',
        'Cantaloupe',
        'Honeydew'
    ]

    # Returns an iterator for every species in the data source.
    def get_species_iterator(self) -> Iterator[Species]:
        return self.data.__iter__()