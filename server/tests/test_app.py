import subprocess
import unittest
import time
import requests
BASE = 'http://localhost:2017'
SERVER = None

class ServerAppCase(unittest.TestCase):

    @staticmethod
    def setUpClass():
        # pylint: disable-next=global-statement
        global SERVER
        # pylint: disable-next=consider-using-with
        SERVER = subprocess.Popen(['python3','greenworld/server/app.py'])
        time.sleep(5)

    @staticmethod
    def tearDownClass():
        SERVER.terminate()

    def test_reports(self):
        self.assertEqual(
            requests.get(url = f'{BASE}/reports?species_list=[0,1,2]', timeout = 5).json(),
            [{"plant1":1,"plant2":1,"range_union_max":"10000.0000000000","range_union_min":"2.4380000000","report":[[[0.305,10000.0],"Hopi Turquoise Corn and Hopi Turquoise Corn should both have enough space to grow horizontally"],[[2.438,10000.0],"Hopi Turquoise Corn and Hopi Turquoise Corn may compete for soil nitrogen"]],"score":"11.0098522167"},{"plant1":1,"plant2":2,"range_union_max":"3.0480000000","range_union_min":"1.5240000000","report":[[[0.381,10000.0],"Hopi Orange Squash should be far enough away from Hopi Turquoise Corn to get direct sunlight"],[[1.219,10000.0],"Hopi Turquoise Corn and Hopi Orange Squash may compete for soil nitrogen"],[[1.524,3.048],"Hopi Orange Squash can shade out weeds around Hopi Turquoise Corn"]],"score":None},{"plant1":1,"plant2":3,"range_union_max":"0.1080000000","range_union_min":"0E-10","report":[[[0.0,0.108],"Hopi Purple String Bean can climb up Hopi Turquoise Corn for direct sunlight"],[[0.0,0.914],"Hopi Purple String Bean can fix soil nitrogen for Hopi Turquoise Corn"]],"score":None}]
        )

    def test_search(self):
        self.assertEqual(
            requests.get(url = f'{BASE}/search/zea', timeout = 5).json(),
            [{'id':1,'name':'Hopi Turquoise Corn','species':'zea mays'}]
        )
        self.assertEqual(
            requests.get(url = f'{BASE}/search/z', timeout = 5).json(),
            []
        )
