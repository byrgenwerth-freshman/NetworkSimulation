import unittest
from networkModules.realNetworkMGMTModule import *

class RealNetworkTableTest(unittest.TestCase):
    def test_init(self):
        real_network = RealNetwork(3)
        self.assertEqual(real_network.group_path_names, [1, 2, 3])
        self.assertEqual(len(real_network.group_path_names), 3)
        real_network = RealNetwork(3)
        self.assertEqual(real_network.group_path_names, [1, 2, 3])
        self.assertEqual(len(real_network.group_path_names), 3)
