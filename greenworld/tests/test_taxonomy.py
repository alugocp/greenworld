import unittest
from greenworld.taxonomy import Taxon

class TaxonomyCase(unittest.TestCase):

    def test_parse_species(self):
        taxon = Taxon()
        self.assertEqual(taxon.parse_species('zea mays').pretty_species(), 'zea mays')
        self.assertEqual(taxon.parse_species('zea mays L.').pretty_species(), 'zea mays')
        self.assertEqual(taxon.parse_species('zea mays var. Oaxacan').pretty_species(), 'zea mays var. oaxacan')
        self.assertEqual(taxon.parse_species('zea mays var. Oaxacan cv. Green').pretty_species(), 'zea mays var. oaxacan cv. green')
        self.assertEqual(taxon.parse_species('zea mays var. Oaxacan L. cv. Green').pretty_species(), 'zea mays var. oaxacan cv. green')
        self.assertEqual(taxon.parse_species('zea mays nope. Oaxacan').pretty_species(), 'zea mays')

    def test_parse_family(self):
        taxon = Taxon()
        self.assertEqual(
            taxon.parse_family('Fabaceae').family,
            'fabaceae'
        )
        self.assertEqual(
            taxon.parse_family('asparagaceae').family,
            'asparagaceae'
        )
        self.assertEqual(
            taxon.parse_family('leguminosae').family,
            None
        )
