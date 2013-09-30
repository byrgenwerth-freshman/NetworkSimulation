import random
import re
from VirtualNetworkClass import *

class VirtualNetworkMGMT:

    vn_container = []

    def __init__(self, virutal_networks):
       self.vn_container = virutal_networks

    def addTempPath(self, utilizationSet, demandManager):
        print self
        for i in range(len(demandManager.added_demands)):
            if len(utilizationSet.not_utilized) > 0:
                path = utilizationSet.not_utilized[random.randint(0,
                                                        len(utilizationSet.not_utilized) - 1)]
                utilizationSet.part_utilized.append(path)
                utilizationSet.not_utilized.remove(path)
                #Find out the Virtual Network and add the path
                vn_number = demandManager.added_demands[i].virtual_network_id
                #Add the path to that virtual network
                self.vn_container[vn_number].added_paths.append(path)
                #Change the path of the demand to new path
                location = demandManager.current_demands.index(demandManager.added_demands[i])
                demandManager.current_demands[location].demandPathId = path
                #print self
        # print "Virtual Network"
        # print self
        # print "Utilized Paths"
        # print utilizationSet.part_utilized
        # print "Not Utilzed Paths"
        # print utilizationSet.not_utilized
        # print demandManager.printAddedDemands()
        # print demandManager.printCurrentDemands()

    def __str__(self):
        string = ""
        for i in range(len(self.vn_container)):
            string = string + str(self.vn_container[i]) + "\n"
        return string
