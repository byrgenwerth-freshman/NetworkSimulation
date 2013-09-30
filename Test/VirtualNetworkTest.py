import unittest
from networkModules.VirtualNetworkClass import *

class VirtualNetworkTest(unittest.TestCase):
    def test_init(self):
        new_vn = VirtualNetwork([1,2])
        self.assertEqual(new_vn.original_paths, [1,2])
        self.assertEqual(new_vn.added_paths, [])

    def test_add(self):
        add_vn = VirtualNetwork([1,2])
        add_vn.addPath(3)
        self.assertEqual(add_vn.added_paths, [3])
