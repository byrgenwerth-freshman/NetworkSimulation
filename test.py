###############################################################################
import unittest
from networkModules.CapacityClass import *
from networkModules.capacityMGMTModule import *
from networkModules.DemandClass import *
from networkModules.demandMGMTModule import *
from networkModules.networkMGMTModule import *
from networkModules.realNetworkMGMTModule import *
from networkModules.utilizationMGMTModule import *
from networkModules.virtualNetworkMGMTModule import *
from networkModules.VirtualNetworkClass import *
###############################################################################
# 1 *---* 3
#    \ /
#     * 2
# Base Graph
#
# Path
###############################################################################
class CapacityClassTest(unittest.TestCase):
  def test_init(self):
    capacity = Capacity("1-3", 100, ["x1_2"])
    self.assertEqual(capacity.link, "1-3")
    self.assertEqual(capacity.capacity, 100)
    self.assertEqual(capacity.list_of_paths, ["x1_2"])
###############################################################################

###############################################################################
class CapacityTableTest(unittest.TestCase):
  def test_init(self):
    raw_capacities = ([['1-2', ['x1_1']],['2-3', ['x1_1']],['1-3', ['x1_2']]])
    capacities = []
    for capacity in raw_capacities:
        capacity = Capacity(capacity[0], 100, capacity[1])
        capacities.append(capacity)
    capacity_table = CapacityTable(capacities)
    self.assertEqual(capacity_table.capacity_table, capacities)
###############################################################################

###############################################################################
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


###############################################################################

###############################################################################
class DemandTestMGMT(unittest.TestCase):
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






###############################################################################

###############################################################################
class NetworkTest(unittest.TestCase):
  def test_init(self):
    coefs = ([3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5,
                3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3,
                5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 4, 5, 4, 5, 4, 5, 4, 5,
                3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3,
                5, 3, 5, 4, 5, 4, 5, 4, 5, 4, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5,
                3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3,
                5])
    equation = (['x1_1', 'x1_2', 'x2_1', 'x2_2', 'x3_1', 'x3_2', 'x4_1',
                'x4_2', 'x5_1', 'x5_2', 'x6_1', 'x6_2', 'x7_1', 'x7_2', 'x8_1',
                'x8_2', 'x9_1', 'x9_2', 'x10_1', 'x10_2', 'x11_1', 'x11_2',
                'x12_1', 'x12_2', 'x13_1', 'x13_2', 'x14_1', 'x14_2', 'x15_1',
                'x15_2', 'x16_1', 'x16_2', 'x17_1', 'x17_2', 'x18_1', 'x18_2',
                'x19_1', 'x19_2', 'x20_1', 'x20_2', 'x21_1', 'x21_2', 'x22_1',
                'x22_2', 'x23_1', 'x23_2', 'x24_1', 'x24_2', 'x25_1', 'x25_2',
                'x26_1', 'x26_2', 'x27_1', 'x27_2', 'x28_1', 'x28_2', 'x29_1',
                'x29_2', 'x30_1', 'x30_2', 'x31_1', 'x31_2', 'x32_1', 'x32_2',
                'x33_1', 'x33_2', 'x34_1', 'x34_2', 'x35_1', 'x35_2', 'x36_1',
                'x36_2', 'x37_1', 'x37_2', 'x38_1', 'x38_2', 'x39_1', 'x39_2',
                'x40_1', 'x40_2', 'x41_1', 'x41_2', 'x42_1', 'x42_2', 'x43_1',
                'x43_2', 'x44_1', 'x44_2', 'x45_1', 'x45_2', 'x46_1', 'x46_2',
                'x47_1', 'x47_2', 'x48_1', 'x48_2', 'x49_1', 'x49_2', 'x50_1',
                'x50_2', 'x51_1', 'x51_2', 'x52_1', 'x52_2', 'x53_1', 'x53_2',
                'x54_1', 'x54_2', 'x55_1', 'x55_2', 'x56_1', 'x56_2', 'x57_1',
                'x57_2', 'x58_1', 'x58_2', 'x59_1', 'x59_2', 'x60_1', 'x60_2',
                'x61_1', 'x61_2', 'x62_1', 'x62_2', 'x63_1', 'x63_2', 'x64_1',
                'x64_2'])

    demandeq = ([['x1_1', 'x1_2'], ['x2_1', 'x2_2'], ['x3_1', 'x3_2'],
                ['x4_1', 'x4_2'], ['x5_1', 'x5_2'], ['x6_1', 'x6_2'],
                ['x7_1', 'x7_2'], ['x8_1', 'x8_2'], ['x9_1', 'x9_2'],
                ['x10_1', 'x10_2'], ['x11_1', 'x11_2'], ['x12_1', 'x12_2'],
                ['x13_1', 'x13_2'], ['x14_1', 'x14_2'], ['x15_1', 'x15_2'],
                ['x16_1', 'x16_2'], ['x17_1', 'x17_2'], ['x18_1', 'x18_2'],
                ['x19_1', 'x19_2'], ['x20_1', 'x20_2'], ['x21_1', 'x21_2'],
                ['x22_1', 'x22_2'], ['x23_1', 'x23_2'], ['x24_1', 'x24_2'],
                ['x25_1', 'x25_2'], ['x26_1', 'x26_2'], ['x27_1', 'x27_2'],
                ['x28_1', 'x28_2'], ['x29_1', 'x29_2'], ['x30_1', 'x30_2'],
                ['x31_1', 'x31_2'], ['x32_1', 'x32_2'], ['x33_1', 'x33_2'],
                ['x34_1', 'x34_2'], ['x35_1', 'x35_2'], ['x36_1', 'x36_2'],
                ['x37_1', 'x37_2'], ['x38_1', 'x38_2'], ['x39_1', 'x39_2'],
                ['x40_1', 'x40_2'], ['x41_1', 'x41_2'], ['x42_1', 'x42_2'],
                ['x43_1', 'x43_2'], ['x44_1', 'x44_2'], ['x45_1', 'x45_2'],
                ['x46_1', 'x46_2'], ['x47_1', 'x47_2'], ['x48_1', 'x48_2'],
                ['x49_1', 'x49_2'], ['x50_1', 'x50_2'], ['x51_1', 'x51_2'],
                ['x52_1', 'x52_2'], ['x53_1', 'x53_2'], ['x54_1', 'x54_2'],
                ['x55_1', 'x55_2'], ['x56_1', 'x56_2'], ['x57_1', 'x57_2'],
                ['x58_1', 'x58_2'], ['x59_1', 'x59_2'], ['x60_1', 'x60_2'],
                ['x61_1', 'x61_2'], ['x62_1', 'x62_2'], ['x63_1', 'x63_2'],
                ['x64_1', 'x64_2']])
    capacity = ([['1-5', ['x1_1', 'x2_1', 'x3_1', 'x4_1', 'x5_2', 'x6_2',
                'x7_2', 'x8_2', 'x17_2', 'x18_2', 'x19_2', 'x20_2', 'x29_2',
                'x30_2', 'x31_2', 'x32_2', 'x49_2', 'x50_2', 'x51_2',
                'x52_2']], ['5-13', ['x1_1', 'x1_2', 'x2_1', 'x2_2', 'x17_1',
                'x17_2', 'x18_1', 'x18_2', 'x33_2', 'x34_2', 'x49_2',
                'x50_2']], ['13-21', ['x1_1', 'x1_2', 'x17_1', 'x17_2',
                'x33_1', 'x33_2', 'x49_1', 'x49_2']], ['1-10', ['x1_2', 'x2_2',
                'x3_2', 'x4_2', 'x9_1', 'x10_1', 'x11_1', 'x12_1', 'x17_2',
                'x18_2', 'x19_2', 'x20_2']], ['2-10', ['x1_2', 'x2_2', 'x3_2',
                'x4_2', 'x17_2', 'x18_2', 'x19_2', 'x20_2', 'x25_1', 'x26_1',
                'x27_1', 'x28_1']], ['2-5', ['x1_2', 'x2_2', 'x3_2', 'x4_2',
                'x5_2', 'x6_2', 'x7_2', 'x8_2', 'x17_1', 'x18_1', 'x19_1',
                'x20_1', 'x29_2', 'x30_2', 'x31_2', 'x32_2', 'x33_2', 'x34_2',
                'x35_2', 'x36_2']], ['13-22', ['x2_1', 'x2_2', 'x18_1', 'x18_2',
                'x34_1', 'x34_2', 'x50_1', 'x50_2']], ['5-14', ['x3_1', 'x3_2',
                'x4_1', 'x4_2', 'x19_1', 'x19_2', 'x20_1', 'x20_2', 'x35_2',
                'x36_2', 'x51_2', 'x52_2']], ['14-23', ['x3_1', 'x3_2',
                'x19_1', 'x19_2', 'x35_1', 'x35_2', 'x51_1', 'x51_2']],
                ['14-24', ['x4_1', 'x4_2', 'x20_1', 'x20_2', 'x36_1', 'x36_2',
                'x52_1', 'x52_2']], ['1-8', ['x5_1', 'x6_1', 'x7_1', 'x8_1',
                'x9_2', 'x10_2', 'x11_2', 'x12_2', 'x13_2', 'x14_2', 'x15_2',
                'x16_2', 'x49_2', 'x50_2', 'x51_2', 'x52_2', 'x61_2', 'x62_2',
                'x63_2', 'x64_2']], ['8-15', ['x5_1', 'x6_1', 'x53_1',
                'x54_1']], ['15-25', ['x5_1', 'x5_2', 'x21_1', 'x21_2',
                'x37_1', 'x37_2', 'x53_1', 'x53_2']], ['2-7', ['x5_2', 'x6_2',
                'x7_2', 'x8_2', 'x21_1', 'x22_1', 'x23_1', 'x24_1', 'x25_2',
                'x26_2', 'x27_2', 'x28_2', 'x33_2', 'x34_2', 'x35_2', 'x36_2',
                'x37_2', 'x38_2', 'x39_2', 'x40_2']], ['7-15', ['x5_2', 'x6_2',
                'x21_1', 'x21_2', 'x22_1', 'x22_2', 'x37_1', 'x37_2', 'x38_1',
                'x38_2', 'x53_2', 'x54_2']], ['15-26', ['x6_1', 'x6_2',
                'x22_1', 'x22_2', 'x38_1', 'x38_2', 'x54_1', 'x54_2']],
                ['8-16', ['x7_1', 'x8_1', 'x55_1', 'x56_1']], ['16-27',
                ['x7_1', 'x7_2', 'x23_1', 'x23_2', 'x39_1', 'x39_2', 'x55_1',
                'x55_2']], ['7-16', ['x7_2', 'x8_2', 'x23_1', 'x23_2', 'x24_1',
                'x24_2', 'x39_1', 'x39_2', 'x40_1', 'x40_2', 'x55_2', 'x56_2']],
                ['16-28', ['x8_1', 'x8_2', 'x24_1', 'x24_2', 'x40_1', 'x40_2',
                'x56_1', 'x56_2']], ['10-17', ['x9_1', 'x10_1', 'x25_1',
                'x26_1']], ['17-29', ['x9_1', 'x9_2', 'x25_1', 'x25_2',
                'x41_1', 'x41_2', 'x57_1', 'x57_2']], ['4-8', ['x9_2', 'x10_2',
                'x11_2', 'x12_2', 'x13_2', 'x14_2', 'x15_2', 'x16_2', 'x49_2',
                'x50_2', 'x51_2', 'x52_2', 'x53_1', 'x54_1', 'x55_1', 'x56_1',
                'x61_2', 'x62_2', 'x63_2', 'x64_2']], ['4-9', ['x9_2', 'x10_2',
                'x11_2', 'x12_2', 'x41_2', 'x42_2', 'x43_2', 'x44_2', 'x57_1',
                'x58_1', 'x59_1', 'x60_1']], ['9-17', ['x9_2', 'x10_2',
                'x25_2', 'x26_2', 'x41_1', 'x41_2', 'x42_1', 'x42_2', 'x57_1',
                'x57_2', 'x58_1', 'x58_2']], ['17-30', ['x10_1', 'x10_2',
                'x26_1', 'x26_2', 'x42_1', 'x42_2', 'x58_1', 'x58_2']],
                ['10-18', ['x11_1', 'x12_1', 'x27_1', 'x28_1']], ['18-31',
                ['x11_1', 'x11_2', 'x27_1', 'x27_2', 'x43_1', 'x43_2', 'x59_1',
                'x59_2']], ['9-18', ['x11_2', 'x12_2', 'x27_2', 'x28_2',
                'x43_1', 'x43_2', 'x44_1', 'x44_2', 'x59_1', 'x59_2', 'x60_1',
                'x60_2']], ['18-32', ['x12_1', 'x12_2', 'x28_1', 'x28_2',
                'x44_1', 'x44_2', 'x60_1', 'x60_2']], ['1-11', ['x13_1',
                'x14_1', 'x15_1', 'x16_1', 'x29_2', 'x30_2', 'x31_2', 'x32_2',
                'x61_2', 'x62_2', 'x63_2', 'x64_2']], ['11-19', ['x13_1',
                'x13_2', 'x14_1', 'x14_2', 'x29_1', 'x29_2', 'x30_1', 'x30_2',
                'x45_1', 'x45_2', 'x46_1', 'x46_2', 'x61_1', 'x61_2', 'x62_1',
                'x62_2']], ['19-33', ['x13_1', 'x13_2', 'x29_1', 'x29_2',
                'x45_1', 'x45_2', 'x61_1', 'x61_2']], ['4-11', ['x13_2',
                'x14_2', 'x15_2', 'x16_2', 'x45_2', 'x46_2', 'x47_2', 'x48_2',
                'x61_1', 'x62_1', 'x63_1', 'x64_1']], ['19-34', ['x14_1',
                'x14_2', 'x30_1', 'x30_2', 'x46_1', 'x46_2', 'x62_1',
                'x62_2']], ['11-20', ['x15_1', 'x15_2', 'x16_1', 'x16_2',
                'x31_1', 'x31_2', 'x32_1', 'x32_2', 'x47_1', 'x47_2', 'x48_1',
                'x48_2', 'x63_1', 'x63_2', 'x64_1', 'x64_2']], ['20-35',
                ['x15_1', 'x15_2', 'x31_1', 'x31_2', 'x47_1', 'x47_2', 'x63_1',
                'x63_2']], ['20-36', ['x16_1', 'x16_2', 'x32_1', 'x32_2',
                'x48_1', 'x48_2', 'x64_1', 'x64_2']], ['2-12', ['x21_2',
                'x22_2', 'x23_2', 'x24_2', 'x29_1', 'x30_1', 'x31_1', 'x32_1',
                'x37_2', 'x38_2', 'x39_2', 'x40_2']], ['3-12', ['x21_2',
                'x22_2', 'x23_2', 'x24_2', 'x37_2', 'x38_2', 'x39_2', 'x40_2',
                'x45_1', 'x46_1', 'x47_1', 'x48_1']], ['3-7', ['x21_2',
                'x22_2', 'x23_2', 'x24_2', 'x25_2', 'x26_2', 'x27_2', 'x28_2',
                'x33_2', 'x34_2', 'x35_2', 'x36_2', 'x37_1', 'x38_1', 'x39_1',
                'x40_1', 'x53_2', 'x54_2', 'x55_2', 'x56_2']], ['3-9',
                ['x25_2', 'x26_2', 'x27_2', 'x28_2', 'x41_1', 'x42_1', 'x43_1',
                'x44_1', 'x57_2', 'x58_2', 'x59_2', 'x60_2']], ['11-12',
                ['x29_1', 'x30_1', 'x31_1', 'x32_1', 'x45_1', 'x46_1', 'x47_1',
                'x48_1']], ['3-6', ['x33_1', 'x34_1', 'x35_1', 'x36_1',
                'x41_2', 'x42_2', 'x43_2', 'x44_2', 'x45_2', 'x46_2', 'x47_2',
                'x48_2', 'x53_2', 'x54_2', 'x55_2', 'x56_2', 'x57_2', 'x58_2',
                'x59_2', 'x60_2']], ['6-13', ['x33_1', 'x34_1', 'x49_1',
                'x50_1']], ['6-14', ['x35_1', 'x36_1', 'x51_1', 'x52_1']],
                ['4-6', ['x41_2', 'x42_2', 'x43_2', 'x44_2', 'x45_2', 'x46_2',
                'x47_2', 'x48_2', 'x49_1', 'x50_1', 'x51_1', 'x52_1', 'x53_2',
                'x54_2', 'x55_2', 'x56_2', 'x57_2', 'x58_2', 'x59_2',
                'x60_2']]])
    output_file = ("/home/mattowens/Documents/gitRepos/NetworkSimulation/"
                    + "inputFiles/OriginalInput/kshortestpaths.txt")
    graph_file = ("/home/mattowens/Documents/gitRepos/NetworkSimulation/"
                    + "inputFiles/OriginalInput/SampleFatTreeTopology.txt")
    network = Network(output_file, graph_file)
    self.assertEqual(network.coef, coefs)
    self.assertEqual(network.equation, equation)
    self.assertEqual(network.demandeq, demandeq)
    self.assertEqual(network.capacity, capacity)
###############################################################################

###############################################################################
class RealNetworkTable(unittest.TestCase):
    def test_init(self):
        real_network = RealNetwork(3)
        self.assertEqual(real_network.group_path_names, [1, 2, 3])
        self.assertEqual(len(real_network.group_path_names), 3)
        real_network = RealNetwork(3)
        self.assertEqual(real_network.group_path_names, [1, 2, 3])
        self.assertEqual(len(real_network.group_path_names), 3)
###############################################################################

###############################################################################
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
###############################################################################

###############################################################################
class VirtualNetworkTest(unittest.TestCase):
    def test_init(self):

        new_vn = VirtualNetwork([1,2])
        self.assertEqual(new_vn.original_paths, [1,2])
        self.assertEqual(new_vn.added_paths, [])

    def test_add(self):
        add_vn = VirtualNetwork([1,2])
        add_vn.addPath(3)
        self.assertEqual(add_vn.added_paths, [3])

###############################################################################

###############################################################################
class VirtualNetworkMGMTTest(unittest.TestCase):
  def test_init(self):
    virtual_networks = []
    virtual_networks.append(VirtualNetwork([1,2]))
    virtual_networks.append(VirtualNetwork([3]))
    vn_manager = VirtualNetworkMGMT(virtual_networks)
    self.assertEqual(vn_manager.vn_container[0].original_paths, [1,2])
    self.assertEqual(vn_manager.vn_container[1].original_paths, [3])
    self.assertEqual(vn_manager.vn_container[0].added_paths, [])
    self.assertEqual(vn_manager.vn_container[1].added_paths, [])
###############################################################################

def main():
    unittest.main()

if __name__ == '__main__':
    main()
