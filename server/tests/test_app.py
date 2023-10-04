import subprocess
import unittest
import time
import requests
from greenworld import Greenworld
from greenworld.scripts import reset
from greenworld.scripts import enter
from greenworld.scripts import report

BASE = "http://127.0.0.1:2017"
SERVER = None


class ServerAppCase(unittest.TestCase):
    # Infinite diff length in the logs
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        # pylint: disable-next=global-statement
        global SERVER
        # pylint: disable-next=consider-using-with

        # Seed consistent test data
        gw = Greenworld()
        reset.main(gw)
        enter.main(gw, ["seed-data/three-sisters.json"])
        report.main(gw)

        # Start up the Greenworld server
        SERVER = subprocess.Popen(["make", "serve"])

        # Wait for server to come online
        pings = 0
        while True:
            time.sleep(1)
            try:
                print("Pinging server process...")
                requests.get(BASE, timeout = 5)
                return
            except ConnectionError:
                pings += 1
                if pings == 10:
                    return

    @classmethod
    def tearDownClass(cls):
        # Tear down the Greenworld server
        SERVER.terminate()

    def test_search(self):
        self.assertEqual(
            requests.get(url=f"{BASE}/search/zea", timeout=5).json(),
            [{"id": 1, "name": "Hopi Turquoise Corn", "species": "zea mays"}],
        )
        self.assertEqual(requests.get(url=f"{BASE}/search/z", timeout=5).json(), [])

    def test_neighbors(self):
        self.assertEqual(
            requests.get(url=f"{BASE}/neighbors/1", timeout=5).json(),
            [[3, 0.367], [1, -1.0], [2, -1.0]],
        )

    def test_handlers(self):
        self.assertEqual(
            requests.get(url=f"{BASE}/handlers?ids=1,2", timeout=5).json(),
            [
                {"id": 1, "name": "Hopi Turquoise Corn", "species": "zea mays"},
                {"id": 2, "name": "Hopi Orange Squash", "species": "cucurbita maxima"},
            ],
        )
