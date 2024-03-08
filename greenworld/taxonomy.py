"""
Scientific species name parsing logic
"""
from enum import IntEnum, unique
from typing import Optional, Self


@unique
class TaxonParseState(IntEnum):
    """
    States used in the Taxon parsing algorithm
    """

    GENUS = 0
    SPECIES = 1
    EXTRA = 2
    SEARCHING = 3


class Taxon:
    """
    Class that can parse and pretty print scientific names
    """

    genus: Optional[str]
    species: Optional[str]
    extra: str

    def parse(self, text: str) -> Self:
        """
        Parses a raw string species name so Greenworld knows what it's dealing with.
        Will throw an error if the argument is an invalid species name.
        """
        state = TaxonParseState.GENUS
        self.species = None
        self.genus = None
        self.extra = ""
        for part in text.lower().split(" "):
            if part == "":
                break

            # Add an extra identifier (variety or cultivar, etc)
            if state == TaxonParseState.EXTRA:
                self.extra = f"{self.extra} {part}"
                state = TaxonParseState.SEARCHING

            # Search for signifiers
            if state == TaxonParseState.SEARCHING:
                if part in ["c.", "cv.", "var.", "v."]:
                    self.extra = f"{self.extra} {part}"
                    state = TaxonParseState.EXTRA

            # Parse the species name
            if state == TaxonParseState.SPECIES:
                if part in ["sp.", "spp."]:
                    self.species = "spp."
                else:
                    self.species = part
                state = TaxonParseState.SEARCHING

            # Parse the genus name
            if state == TaxonParseState.GENUS:
                self.genus = part.capitalize()
                state = TaxonParseState.SPECIES

        # Clean up the extra field and check for invalid arguments
        self.extra = self.extra.strip()
        if self.genus is None:
            raise ValueError(f"Species name '{text}' is invalid")
        return self

    def format(self) -> str:
        """
        Return the parsed species name in the Greenworld standard format
        """
        return " ".join(
            list(
                filter(
                    lambda x: x is not None and len(x) > 0,
                    [
                        self.genus,
                        self.species,
                        self.extra,
                    ],
                )
            )
        )

    @staticmethod
    def family(family: str) -> str:
        """
        Properly format a taxonomic family
        """
        return family.lower().capitalize()
