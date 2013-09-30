import unittest
from networkModules.capacityMGMTModule import *

class CapacityTableTest(unittest.TestCase):
  def test_init(self):
    raw_capacities = ([['1-2', ['x1_1']],['2-3', ['x1_1']],['1-3', ['x1_2']]])
    capacities = []
    for capacity in raw_capacities:
        capacity = Capacity(capacity[0], 100, capacity[1])
        capacities.append(capacity)
    capacity_table = CapacityTable(capacities)
    self.assertEqual(capacity_table.capacity_table, capacities)

  def test_restoreCapacity(self):
    assert False
