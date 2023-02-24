from typing import Optional

class Taxon:
    genus: Optional[str]
    species: Optional[str]

    def __init__(self, text: str):
        parts = text.lower().split(' ')
        self.genus = parts[0]
        self.species = parts[1]
        if self.species in ['sp.', 'spp.']:
            self.species = None

    def full_species(self):
        return f'{self.genus} {self.species}'
