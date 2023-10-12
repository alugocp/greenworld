

"""
This module tests the report script
"""
import unittest
import sqlalchemy
from greenworld import Greenworld
from greenworld.scripts import report
from greenworld.scripts import reset
from greenworld.scripts import enter
from greenworld.orm import reports_table
from greenworld.orm import init_db

def count_reports(db):
    """
    Return the number of reports in the database
    """
    with db.connect() as con:
        return con.execute(sqlalchemy.select(sqlalchemy.func.count()).select_from(
            reports_table
        )).fetchone()[0]

class ScriptsReportCase(unittest.TestCase):
    """
    unittest class
    """

    def test_continued_reporting(self):
        """
        Tests when plant data is entered, reported on, then more plants come in
        """
        gw = Greenworld()
        db = init_db()
        reset.main(gw)

        # Enter, report, and count initial Three Sisters data
        enter.enter_data(gw, db, {
            "plants": [
                {
                    "id": 1,
                    "name": "Corn",
                    "species": "Zea mays",
                    "family": "Gramineae",
                    "citations": {},
                },
                {
                    "id": 2,
                    "name": "Squash",
                    "species": "Cucurbita moschata",
                    "family": "Cucurbitaceae",
                    "citations": {},
                },
                {
                    "id": 3,
                    "name": "Beans",
                    "species": "Phaseolus vulgaris",
                    "family": "Fabaceae",
                    "citations": {},
                }
            ]
        })
        report.main(gw)
        self.assertEqual(count_reports(db), 6)

        # Enter, report, and count the full Seven Sisters data
        enter.enter_data(gw, db, {
            "plants": [
                {
                    "id": 1,
                    "name": "Sunflower",
                    "species": "Helianthus annuus",
                    "family": "Asteraceae",
                    "citations": {},
                },
                {
                    "id": 2,
                    "name": "Sunchoke",
                    "species": "Helianthus tuberosus",
                    "family": "Asteraceae",
                    "citations": {},
                },
                {
                    "id": 3,
                    "name": "Ground Cherry",
                    "species": "Physalis peruviana",
                    "family": "Solanaceae",
                    "citations": {},
                },
                {
                    "id": 4,
                    "name": "Tobacco",
                    "species": "Nicotiana tabacum",
                    "family": "Solanaceae",
                    "citations": {},
                }
            ]
        })
        report.main(gw)
        self.assertEqual(count_reports(db), 28)
