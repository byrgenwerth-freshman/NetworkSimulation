###############################################################################
import unittest
from networkModules.virtualNetworkMGMTModule import *
from networkModules.demandMGMTModule import *
from networkModules.utilizationMGMTModule import *
from networkModules.realNetworkMGMTModule import *
from networkModules.VirtualNetworkClass import *
from networkModules.virtualNetworkMGMTModule import *
###############################################################################

class VirtualNetworkMGMTTest(unittest.TestCase):
    def setUp(self):
        #Virtual Network Manager
        test_virtual_networks = []
        test_virtual_networks.append(VirtualNetwork([1,2]))
        test_virtual_networks.append(VirtualNetwork([3]))
        self.vn_manager = VirtualNetworkMGMT(test_virtual_networks)

        #Utilization Set
        real_network = RealNetwork(20)
        tmp = []
        tmp.append(VirtualNetwork([7, 9]))
        tmp.append(VirtualNetwork([15, 16]))
        vn_manager = VirtualNetworkMGMT(tmp)
        self.utilization_set = UtilizationSet(real_network, vn_manager)

        #Demand Mangager
        new_demands = []
        new_demands.append(Demand(1, 7, 50, 25, 3))
        new_demands.append(Demand(1, 7, 50, 25, 2))
        new_demands.append(Demand(1, 7, 50, 25, 1))
        new_demands.append(Demand(1, 9, 50, 25, 0))
        self.demand_mgmt_model = DemandMGMT(new_demands)

    def test_init(self):
        virtual_networks = []
        virtual_networks.append(VirtualNetwork([1,2]))
        virtual_networks.append(VirtualNetwork([3]))
        vn_manager = VirtualNetworkMGMT(virtual_networks)
        self.assertEqual(vn_manager.vn_container[0].original_paths, [1,2])
        self.assertEqual(vn_manager.vn_container[1].original_paths, [3])
        self.assertEqual(vn_manager.vn_container[0].added_paths, [])
        self.assertEqual(vn_manager.vn_container[1].added_paths, [])

    def test_addTempPath(self):
        print self.vn_manager
        before = 0
        for i in range(len(self.vn_manager.vn_container)):
            before += len(self.vn_manager.vn_container[i].added_paths)
        self.demand_mgmt_model.checkDemands(0)
        self.vn_manager.addTempPath(self.utilization_set,
                                    self.demand_mgmt_model)
        print self.vn_manager
        after = 0
        for i in range(len(self.vn_manager.vn_container)):
            after += len(self.vn_manager.vn_container[i].added_paths)
        self.assertNotEqual(before, after)