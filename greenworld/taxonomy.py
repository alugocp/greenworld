from enum import IntEnum, unique
from typing import Optional
import re

@unique
class TaxonParseState(IntEnum):
    GENUS     = 0
    SPECIES   = 1
    EXTRA     = 2
    SEARCHING = 3

class Taxon:
    family: Optional[str]
    genus: Optional[str]
    species: Optional[str]
    extra: str

    def parse_species(self, text: str):
        parts = text.lower().split(' ')
        state = TaxonParseState.GENUS
        self.species = None
        self.genus = None
        self.extra = ''
        for part in text.lower().split(' '):

            # Add an extra identifier (variety or cultivar, etc)
            if state == TaxonParseState.EXTRA:
                self.extra = f'{self.extra} {part}'
                state = TaxonParseState.SEARCHING

            # Search for signifiers
            if state == TaxonParseState.SEARCHING:
                if part in ['c.', 'cv.', 'var.', 'v.']:
                    self.extra = f'{self.extra} {part}'
                    state = TaxonParseState.EXTRA

            # Parse the species name
            if state == TaxonParseState.SPECIES:
                if part not in ['sp.', 'spp.']:
                    self.species = part
                state = TaxonParseState.SEARCHING

            # Parse the genus name
            if state == TaxonParseState.GENUS:
                self.genus = part
                state = TaxonParseState.SPECIES

        self.extra = self.extra.strip()
        return self

    def pretty_species(self) -> str:
        return f'{self.genus} {self.species} {self.extra}'.strip()

    def parse_family(self, text: str):
        self.family = None
        match = re.search(r'[a-z]+eae', text, flags = re.I)
        if match:
            self.family = match.group().lower()
        return self
