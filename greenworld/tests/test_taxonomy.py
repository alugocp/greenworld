"""
This module tests code from the taxonomy module
"""
import unittest
from greenworld.taxonomy import Taxon


class TaxonomyCase(unittest.TestCase):
    """
    unittest class
    """

    def test_parse_and_format(self):
        """
        Tests the parse and format functions
        """
        taxon = Taxon()
        self.assertEqual(taxon.parse("zea mays").format(), "Zea mays")
        self.assertEqual(taxon.parse("ZEA MAYS").format(), "Zea mays")
        self.assertEqual(
            taxon.parse("zea mays L.").format(), "Zea mays"
        )
        self.assertEqual(
            taxon.parse("zea mays var. Oaxacan").format(),
            "Zea mays var. oaxacan",
        )
        self.assertEqual(
            taxon.parse("zea mays var. Oaxacan cv. Green").format(),
            "Zea mays var. oaxacan cv. green",
        )
        self.assertEqual(
            taxon.parse("zea mays var. Oaxacan L. cv. Green").format(),
            "Zea mays var. oaxacan cv. green",
        )
        self.assertEqual(
            taxon.parse("zea mays nope. Oaxacan").format(), "Zea mays"
        )
        self.assertEqual(
            taxon.parse("zea").format(), "Zea"
        )
        self.assertEqual(
            taxon.parse("zea sp.").format(), "Zea spp."
        )
        self.assertEqual(
            taxon.parse("zea spp.").format(), "Zea spp."
        )

    def test_invalid_parse(self):
        """
        Tests invalid species name cases
        """
        taxon = Taxon()

        with self.assertRaises(Exception) as err:
            taxon.parse('')
        self.assertEqual(str(err.exception), "Species name '' is invalid")
