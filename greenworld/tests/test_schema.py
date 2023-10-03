import unittest
from schema import SchemaError
from greenworld.schema import json_schema
from greenworld.schema import expand_enum
from greenworld.defs import GrowthHabit

class SchemaCase(unittest.TestCase):

    def test_expand_enum(self):
        schema = expand_enum(GrowthHabit)
        self.assertEqual(schema.validate('GrowthHabit.FORB'), 'GrowthHabit.FORB')
        self.assertEqual(schema.validate('GrowthHabit.GRAMINOID'), 'GrowthHabit.GRAMINOID')
        self.assertEqual(schema.validate('GrowthHabit.LICHENOUS'), 'GrowthHabit.LICHENOUS')
        self.assertEqual(schema.validate('GrowthHabit.NONVASCULAR'), 'GrowthHabit.NONVASCULAR')
        self.assertEqual(schema.validate('GrowthHabit.SHRUB'), 'GrowthHabit.SHRUB')
        self.assertEqual(schema.validate('GrowthHabit.SUBSHRUB'), 'GrowthHabit.SUBSHRUB')
        self.assertEqual(schema.validate('GrowthHabit.TREE'), 'GrowthHabit.TREE')
        self.assertEqual(schema.validate('GrowthHabit.VINE'), 'GrowthHabit.VINE')

    def test_expand_enum_exceptions(self):
        schema = expand_enum(GrowthHabit)
        with self.assertRaises(SchemaError) as _:
            schema.validate('GrowthHabit.HELLO')

    def test_json_schema_empty(self):
        self.assertEqual(json_schema.validate({}), {})

    def test_json_schema(self):
        data = {
            'plants': [
                {
                    'id': 1,
                    'name': 'Plant name',
                    'species': 'plantus species',
                    'family': 'planteae',
                    'growth_habit': 'GrowthHabit.FORB',
                    'height': ['', ''],
                    'spread': ['', ''],
                    'length': ['', ''],
                    'lightweight': True,
                    'root_spread': ['', ''],
                    'nitrogen': 'Nitrogen.FIXER',
                    'sun': 'Sun.FULL_SUN',
                    'soil': ['Soil.SAND', 'Soil.LOAM'],
                    'pH': [7.0, 8.0],
                    'drainage': ['Drainage.WELL_DRAINED', 'Drainage.MODERATELY_WELL_DRAINED'],
                    'citations': {
                        '1': ['', '', ''],
                        '2': ['', '', '']
                    },
                    'ecology': [
                        {
                            'species': 'thing 1',
                            'relationship': 'Ecology.POSITIVE_ALLELOPATHY',
                            'citation': 1
                        },
                        {
                            'species': 'thing 2',
                            'relationship': 'Ecology.POSITIVE_ALLELOPATHY',
                            'citation': 1
                        }
                    ]
                }
            ],
            'others': [
                {
                    'species': 'thing 1',
                    'name': 'Thing 1 name',
                    'family': 'thing family'
                }
            ],
            'works_cited': [
                {
                    'id': 1,
                    'citation': 'work is cited lol'
                }
            ]
        }
        self.assertEqual(json_schema.validate(data), data)

    def test_json_schema_without_options(self):
        data = {
            'plants': [
                {
                    'id': 1,
                    'name': 'Plant name',
                    'species': 'plantus species',
                    'family': 'planteae',
                    'citations': {
                        '1': ['', '', ''],
                        '2': ['', '', '']
                    }
                }
            ]
        }
        self.assertEqual(json_schema.validate(data), data)

    def test_json_schema_without_citations(self):
        data = {
            'plants': [
                {
                    'id': 1,
                    'name': 'Plant name',
                    'species': 'plantus species',
                    'family': 'planteae'
                }
            ]
        }
        with self.assertRaises(SchemaError) as _:
            json_schema.validate(data)
