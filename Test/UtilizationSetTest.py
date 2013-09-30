import unittest
from networkModules.utilizationMGMTModule import *
from networkModules.realNetworkMGMTModule import *
from networkModules.VirtualNetworkClass import *
from networkModules.virtualNetworkMGMTModule import *



class UtilizationSetTest(unittest.TestCase):
    def test_init(self):
        real_network = RealNetwork(3)
        tmp = []
        tmp.append(VirtualNetwork([1, 2]))
        tmp.append(VirtualNetwork([1, 2]))
        vn_manager = VirtualNetworkMGMT(tmp)

        utilization_set = UtilizationSet(real_network, vn_manager)
        self.assertEqual(utilization_set.full_utilized, [])
        self.assertEqual(utilization_set.part_utilized, [1, 2])
        self.assertEqual(utilization_set.not_utilized, [3])
