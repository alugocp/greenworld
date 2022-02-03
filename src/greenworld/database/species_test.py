from typing import Iterator, List

# This class represents a test implementation of SpeciesData.
class TestSpeciesData:

    # Returns an iterator for every species in the data source.
    def get_species_iterator(self) -> Iterator[str]:
        return TestSpeciesIterator()

# This class is an iterator to be used by TestSpeciesData.
class TestSpeciesIterator:
    num: int = 0
    data: List[str] = [
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
        'Cassava'
    ]

    def __iter__(self):
        return self

    def __next__(self):
        if self.num < len(self.data):
            self.num += 1
            return self.data[self.num - 1]
        raise StopIteration