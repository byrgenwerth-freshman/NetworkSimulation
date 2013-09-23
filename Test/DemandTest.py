import unittest
from networkModules.DemandClass import *

class DemandTest(unittest.TestCase):
    def test_init(self):
        new_demand = Demand(2, 23, 50, 25, 3)
        self.assertEqual(new_demand.virtual_network_id, 2)
        self.assertEqual(new_demand.demand_path_id, 23)
        self.assertEqual(new_demand.demand, 50)
        self.assertEqual(new_demand.duration, 25)
        self.assertEqual(new_demand.startTime, 3)

    def test_decrementDur(self):
        new_demand = Demand(2, 23, 50, 25, 3)
        new_demand.decrementDur(1)
        self.assertEqual(new_demand.duration, 24)
