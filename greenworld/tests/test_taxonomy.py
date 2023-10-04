"""
This module tests code from the taxonomy module
"""
import unittest
from greenworld.taxonomy import Taxon


class TaxonomyCase(unittest.TestCase):
    """
    unittest class
    """

    def test_parse_species(self):
        """
        Tests the parse_species and pretty_species functions
        """
        taxon = Taxon()
        self.assertEqual(taxon.parse_species("zea mays").pretty_species(), "zea mays")
        self.assertEqual(
            taxon.parse_species("zea mays L.").pretty_species(), "zea mays"
        )
        self.assertEqual(
            taxon.parse_species("zea mays var. Oaxacan").pretty_species(),
            "zea mays var. oaxacan",
        )
        self.assertEqual(
            taxon.parse_species("zea mays var. Oaxacan cv. Green").pretty_species(),
            "zea mays var. oaxacan cv. green",
        )
        self.assertEqual(
            taxon.parse_species("zea mays var. Oaxacan L. cv. Green").pretty_species(),
            "zea mays var. oaxacan cv. green",
        )
        self.assertEqual(
            taxon.parse_species("zea mays nope. Oaxacan").pretty_species(), "zea mays"
        )
