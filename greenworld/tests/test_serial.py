import unittest
from greenworld.serial import deserialize_enum_list

class SerialCase(unittest.TestCase):

    def test_deserialize_enum_list(self):
        self.assertEqual(deserialize_enum_list(8), [8])
        self.assertEqual(deserialize_enum_list(7), [4, 2, 1])
        self.assertEqual(deserialize_enum_list(6), [4, 2])
        self.assertEqual(deserialize_enum_list(5), [4, 1])
        self.assertEqual(deserialize_enum_list(4), [4])
        self.assertEqual(deserialize_enum_list(3), [2, 1])
        self.assertEqual(deserialize_enum_list(2), [2])
        self.assertEqual(deserialize_enum_list(1), [1])