###############################################################################
import unittest
from Test.CapacityClassTest import *
from Test.CapacityTableTest import *
from Test.DemandMGMTTest import *
from Test.DemandTest import *
from Test.LoadBalancingModelTest import *
from Test.NetworkTest import *
from Test.RealNetworkTableTest import *
from Test.UtilizationSetTest import *
from Test.VirtualNetworkMGMTTest import *
from Test.VirtualNetworkTest import *

###############################################################################
# 1 *---* 3
#    \ /
#     * 2
# Base Graph
#
# Path
###############################################################################

def main():
    unittest.main()

if __name__ == '__main__':
    main()
