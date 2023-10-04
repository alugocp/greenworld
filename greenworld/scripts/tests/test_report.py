import unittest
import sqlalchemy
from greenworld import Greenworld
from greenworld.scripts import report
from greenworld.scripts import reset
from greenworld.defs import Nitrogen
from greenworld.defs import Ecology
from greenworld.defs import PLANTAE
from greenworld.orm import other_species_table
from greenworld.orm import ecology_other_table
from greenworld.orm import ecology_plant_table
from greenworld.orm import works_cited_table
from greenworld.orm import reports_table
from greenworld.orm import plants_table
from greenworld.orm import init_db
gw = Greenworld()
db = init_db()

def get_report(id1, id2):
    with db.connect() as con:
        data = con.execute(reports_table.select().where(
            sqlalchemy.and_(
                reports_table.c['plant1'] == id1,
                reports_table.c['plant2'] == id2
            )
        )).mappings()
    return next(data).report

class ScriptsReportCase(unittest.TestCase):

    @classmethod
    def setUpClass(_cls):
        reset.main(gw)

        # Manually enter plant data
        with db.connect() as con:
            con.execute(works_cited_table.insert().values([
                {
                    'id': 1,
                    'citation': 'Trust me, bro'
                }
            ]))
            con.execute(other_species_table.insert().values([
                {
                    'id': 1,
                    'species': 'fabaceae',
                    'name': 'Bean Family'
                },
                {
                    'id': 2,
                    'species': 'bee species',
                    'name': 'Bee'
                },
                {
                    'id': 3,
                    'species': 'butterfly species',
                    'name': 'Butterfly'
                },
                {
                    'id': 4,
                    'species': 'fungus species',
                    'name': 'Mushroom'
                }
            ]))
            con.execute(plants_table.insert().values([
                {
                    'id': 1,
                    'name': 'Bean',
                    'species': 'bean species',
                    'family': 'fabaceae',
                    'nitrogen': Nitrogen.FIXER,
                    'citations': {}
                },
                {
                    'id': 2,
                    'name': 'Pumpkin',
                    'species': 'pumpkin species',
                    'family': 'cucurbitaceae',
                    'nitrogen': Nitrogen.HEAVY,
                    'citations': {}
                },
                {
                    'id': 3,
                    'name': 'Onion',
                    'species': 'onion species',
                    'family': 'amaryllidaceae',
                    'nitrogen': Nitrogen.NEUTRAL,
                    'citations': {}
                },
                {
                    'id': 4,
                    'name': 'Anti-Onion Bean',
                    'species': 'anti-onion bean species',
                    'family': 'fabaceae',
                    'nitrogen': Nitrogen.FIXER,
                    'citations': {}
                },
                {
                    'id': 5,
                    'name': 'Walnut That Likes Beans And Onions',
                    'species': 'walnut that likes beans and onions species',
                    'family': 'juglandaceae',
                    'nitrogen': Nitrogen.NEUTRAL,
                    'citations': {}
                },
                {
                    'id': 6,
                    'name': 'Aster 1',
                    'species': 'aster 1 species',
                    'family': 'asteraceae',
                    'nitrogen': Nitrogen.NEUTRAL,
                    'citations': {}
                },
                {
                    'id': 7,
                    'name': 'Aster 2',
                    'species': 'aster 2 species',
                    'family': 'asteraceae',
                    'nitrogen': Nitrogen.NEUTRAL,
                    'citations': {}
                },
                {
                    'id': 8,
                    'name': 'Aster 3',
                    'species': 'aster 3 species',
                    'family': 'asteraceae',
                    'nitrogen': Nitrogen.NEUTRAL,
                    'citations': {}
                }
            ]))
            con.execute(ecology_other_table.insert().values([
                {
                    'plant': 3,
                    'non_plant': 1,
                    'relationship': Ecology.NEGATIVE_ALLELOPATHY,
                    'citation': 1
                },
                {
                    'plant': 5,
                    'non_plant': PLANTAE,
                    'relationship': Ecology.NEGATIVE_ALLELOPATHY,
                    'citation': 1
                },
                {
                    'plant': 5,
                    'non_plant': 1,
                    'relationship': Ecology.POSITIVE_ALLELOPATHY,
                    'citation': 1
                },
                {
                    'plant': 6,
                    'non_plant': 2,
                    'relationship': Ecology.POLLINATOR,
                    'citation': 1
                },
                {
                    'plant': 6,
                    'non_plant': 3,
                    'relationship': Ecology.POLLINATOR,
                    'citation': 1
                },
                {
                    'plant': 6,
                    'non_plant': 4,
                    'relationship': Ecology.PATHOGEN,
                    'citation': 1
                },
                {
                    'plant': 7,
                    'non_plant': 2,
                    'relationship': Ecology.PREDATOR,
                    'citation': 1
                },
                {
                    'plant': 7,
                    'non_plant': 3,
                    'relationship': Ecology.POLLINATOR,
                    'citation': 1
                },
                {
                    'plant': 7,
                    'non_plant': 4,
                    'relationship': Ecology.PATHOGEN,
                    'citation': 1
                },
                {
                    'plant': 8,
                    'non_plant': 2,
                    'relationship': Ecology.NEGATIVE_ALLELOPATHY,
                    'citation': 1
                },
                {
                    'plant': 8,
                    'non_plant': 3,
                    'relationship': Ecology.POSITIVE_ALLELOPATHY,
                    'citation': 1
                },
            ]))
            con.execute(ecology_plant_table.insert().values([
                {
                    'plant': 4,
                    'target': 3,
                    'relationship': Ecology.NEGATIVE_ALLELOPATHY,
                    'citation': 1
                },
                {
                    'plant': 5,
                    'target': 3,
                    'relationship': Ecology.NO_ALLELOPATHY,
                    'citation': 1
                }
            ]))
            con.commit()

        # Run report code
        report.main(gw)

    # Test interaction between nitrogen values
    def test_nitrogen(self):
        self.assertEqual(
            get_report(1, 2),
            ['Bean can fix nitrogen for Pumpkin']
        )

        self.assertEqual(
            get_report(2, 2),
            ['Pumpkin and Pumpkin are both heavy feeders']
        )

        self.assertEqual(
            get_report(2, 3),
            []
        )

        self.assertEqual(
            get_report(3, 3),
            []
        )

    # Test allelopathy logic paths
    def test_allelopathy(self):
        self.assertEqual(
            get_report(1, 3),
            ['Onion is a negative allelopath for Bean']
        )

        self.assertEqual(
            get_report(3, 4),
            ['Anti-Onion Bean and Onion are negative allelopaths for each other']
        )

        self.assertEqual(
            get_report(1, 5),
            ['Walnut That Likes Beans And Onions is a positive allelopath for Bean']
        )

        self.assertEqual(
            get_report(2, 5),
            ['Walnut That Likes Beans And Onions is a negative allelopath for Pumpkin']
        )

        self.assertEqual(
            get_report(3, 5),
            ['Walnut That Likes Beans And Onions is a positive allelopath and Onion is a negative allelopath for Bean Family']
        )

    # Test ecology logic paths
    def test_ecology(self):
        self.assertEqual(
            get_report(6, 7),
            ['Aster 2\'s predator species Bee is a pollinator for Aster 1 and Aster 2 and Aster 1 have a common pollinator species Butterfly and Aster 2 and Aster 1 have a common pathogenic species Mushroom']
        )

        self.assertEqual(
            get_report(7, 8),
            ['Aster 3 is a negative allelopath for Aster 2\'s predator species Bee and Aster 3 is a positive allelopath for Aster 2\'s pollinator species Butterfly']
        )

        self.assertEqual(
            get_report(6, 8),
            ['Aster 3 is a negative allelopath for Aster 1\'s pollinator species Bee and Aster 3 is a positive allelopath for Aster 1\'s pollinator species Butterfly']
        )
