import unittest
from greenworld.collection import iweb_xls


class CollectionIwebXlsxCase(unittest.TestCase):
    def test_parse_species_name(self):
        self.assertEqual(iweb_xls.parse_species_name(["zea mays"]), "zea mays")
        self.assertEqual(iweb_xls.parse_species_name(["ZEA MAYS"]), "zea mays")
        self.assertEqual(iweb_xls.parse_species_name(["ZEA", "MAYS"]), "zea mays")
        self.assertEqual(iweb_xls.parse_species_name(["ZEA", "mays"]), "zea mays")
        self.assertEqual(
            iweb_xls.parse_species_name(["ZEA", "MAYS (common corn)"]), "zea mays"
        )
        self.assertEqual(iweb_xls.parse_species_name(["ZEA", "SPP."]), "zea spp.")
        self.assertEqual(
            iweb_xls.parse_species_name(["ZEA", "spp. (common corn)"]), "zea spp."
        )
        self.assertEqual(
            iweb_xls.parse_species_name(["ZEA (gramineae)", "mays"]), "zea mays"
        )

    def test_parse_csv_line(self):
        self.assertEqual(
            iweb_xls.parse_csv_line("hello,1, 2,  bye"), ["hello", "1", "2", "bye"]
        )
        self.assertEqual(
            iweb_xls.parse_csv_line('"hello there",1,2,bye'),
            ["hello there", "1", "2", "bye"],
        )
        self.assertEqual(
            iweb_xls.parse_csv_line('"hello there"   ,"good bye"'),
            ["hello there", "good bye"],
        )
        self.assertEqual(iweb_xls.parse_csv_line('"hello, tester"'), ["hello, tester"])
        self.assertEqual(iweb_xls.parse_csv_line("\"'hello'\""), ["'hello'"])
        self.assertEqual(iweb_xls.parse_csv_line('"hello"'), ["hello"])
        self.assertEqual(iweb_xls.parse_csv_line("   hello  "), ["hello"])

    def test_parse_range(self):
        self.assertEqual(iweb_xls.parse_range("1:2,3:4"), [1, 2, 3, 4])
        self.assertEqual(iweb_xls.parse_range("100:20,13:14"), [100, 20, 13, 14])
        self.assertEqual(iweb_xls.parse_range("-100:20,13:14"), None)
        self.assertEqual(iweb_xls.parse_range("100:20,-13:14"), None)
        self.assertEqual(iweb_xls.parse_range("100:alex,13:14"), None)
        self.assertEqual(iweb_xls.parse_range("100:10"), None)
        self.assertEqual(iweb_xls.parse_range("100,100"), None)

    def test_transposed(self):
        self.assertEqual(iweb_xls.transposed([[1, 2], [3, 4]]), [[1, 3], [2, 4]])
        self.assertEqual(
            iweb_xls.transposed([[1, 2, 3], [4, 5, 6]]), [[1, 4], [2, 5], [3, 6]]
        )
