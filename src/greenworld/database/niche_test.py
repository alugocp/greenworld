from typing import Dict, Iterable, List
from ..types import Niche, Niches, Species

# This class represents a test implementation of NicheData.
class TestNicheData:
    catalogs: Dict[Niche, List[Species]] = {}

    def initialize_niche_catalogs(self, niches: Niches) -> None:
        for niche in niches:
            self.catalogs[niche] = []

    def add_to_niche(self, niche: Niche, species: Species) -> None:
        self.catalogs[niche].append(species)

    def get_niche_species_iterable(self, niche: Niche) -> Iterable[Species]:
        return self.catalogs[niche]