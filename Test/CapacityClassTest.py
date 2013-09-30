import unittest
from networkModules.CapacityClass import *

class CapacityClassTest(unittest.TestCase):
  def test_init(self):
    capacity = Capacity("1-3", 100, ["x1_2"])
    self.assertEqual(capacity.link, "1-3")
    self.assertEqual(capacity.capacity, 100)
    self.assertEqual(capacity.list_of_paths, ["x1_2"])