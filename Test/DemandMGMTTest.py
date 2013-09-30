import unittest
from networkModules.demandMGMTModule import *


class DemandMGMTTest(unittest.TestCase):
    def test_init(self):
        new_demands = []
        new_demands.append(Demand(2, 23, 50, 25, 3))
        new_demands.append(Demand(2, 23, 50, 25, 2))
        new_demands.append(Demand(2, 23, 50, 25, 1))
        new_demands.append(Demand(2, 23, 50, 25, 0))

        demand_mgmt_model = DemandMGMT(new_demands)


    def test_check_for_current_demands(self):
        new_demands = []
        new_demands.append(Demand(2, 23, 50, 25, 3))
        new_demands.append(Demand(2, 23, 50, 25, 2))
        new_demands.append(Demand(2, 23, 50, 25, 1))
        new_demands.append(Demand(2, 23, 50, 25, 0))
        demand_mgmt_model = DemandMGMT(new_demands)
        demand_mgmt_model.checkDemands(3)
        self.assertEqual(demand_mgmt_model.waiting_demands, [])
        for i in range(len(demand_mgmt_model.current_demands)):
            self.assertEqual(demand_mgmt_model.current_demands[i].virtual_network_id,
                                new_demands[i].virtual_network_id)
            self.assertEqual(demand_mgmt_model.current_demands[i].demand_path_id,
                                new_demands[i].demand_path_id)
            self.assertEqual(demand_mgmt_model.current_demands[i].demand,
                                new_demands[i].demand)
            self.assertEqual(demand_mgmt_model.current_demands[i].duration,
                                new_demands[i].duration)
            self.assertEqual(demand_mgmt_model.current_demands[i].startTime,
                                new_demands[i].startTime)
        self.assertEqual(demand_mgmt_model.added_demands[0].virtual_network_id,
                            new_demands[0].virtual_network_id)
        self.assertEqual(demand_mgmt_model.added_demands[0].demand_path_id,
                            new_demands[0].demand_path_id)
        self.assertEqual(demand_mgmt_model.added_demands[0].demand,
                            new_demands[0].demand)
        self.assertEqual(demand_mgmt_model.added_demands[0].duration,
                            new_demands[0].duration)
        self.assertEqual(demand_mgmt_model.added_demands[0].startTime,
                            new_demands[0].startTime)


