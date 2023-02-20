import unittest
from greenworld.scripts import enter

class ScriptsEnterCase(unittest.TestCase):

    def test_parse_species_name(self):
        self.assertEqual(enter.parse_species_name(['zea mays']), 'zea mays')
        self.assertEqual(enter.parse_species_name(['ZEA MAYS']), 'zea mays')
        self.assertEqual(enter.parse_species_name(['ZEA', 'MAYS']), 'zea mays')
        self.assertEqual(enter.parse_species_name(['ZEA', 'mays']), 'zea mays')
        self.assertEqual(enter.parse_species_name(['ZEA', 'MAYS (common corn)']), 'zea mays')
        self.assertEqual(enter.parse_species_name(['ZEA', 'SPP.']), 'zea spp.')
        self.assertEqual(enter.parse_species_name(['ZEA', 'spp. (common corn)']), 'zea spp.')
        self.assertEqual(enter.parse_species_name(['ZEA (gramineae)', 'mays']), 'zea mays')
