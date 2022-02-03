from typing import Dict, Iterable, List

# This class represents a test implementation of NicheData.
class TestNicheData:
    catalogs: Dict[str, List[str]] = {}

    def initialize_niche_catalogs(self, niches: List[str]) -> None:
        for niche in niches:
            self.catalogs[niche] = []

    def add_to_niche(self, niche: str, species: str) -> None:
        self.catalogs[niche].append(species)

    def get_niche_species_iterable(self, niche: str) -> Iterable[str]:
        return self.catalogs[niche]