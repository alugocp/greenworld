from typing import Optional
import re

class Taxon:
    family: Optional[str]
    genus: Optional[str]
    species: Optional[str]

    def parse_species(self, text: str):
        parts = text.lower().split(' ')
        self.genus = parts[0]
        self.species = parts[1]
        if self.species in ['sp.', 'spp.']:
            self.species = None
        return self

    def parse_family(self, text: str):
        match = re.search(r'[a-z]+eae', text, flags = re.I)
        if match:
            self.family = match.group().lower()
        return self
