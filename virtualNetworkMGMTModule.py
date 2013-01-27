import random
import re
from VirtualNetworkClass import *

class VirtualNetworkMGMT:

    vnContainer = []

    def __str__(self):
        string = ""
        for i in range(len(self.vnContainer)):
            string = string + str(self.vnContainer[i]) + "\n" 
        return string

    def createVirtualNetwork(self, paths):
       vn = VirtualNetwork(paths)
       self.vnContainer.append(vn)
    
    def addTempPath(self, utilizationSet, demandManager):
        print self
        for i in range(len(demandManager.addedDemands)):
            if len(utilizationSet.notUtilized) > 0:   
                path = utilizationSet.notUtilized[random.randint(0,
                                                        len(utilizationSet.notUtilized) - 1)]
                utilizationSet.partUtilized.append(path) 
                utilizationSet.notUtilized.remove(path)
                #Find out the Virtual Network and add the path
                vnNumb = demandManager.addedDemands[i].virtualNetworkId
                #Add the path to that virtual network
                print self.vnContainer[vnNumb]
                self.vnContainer[vnNumb].addedPaths.append(path)
                #Change the path of the demand to new path
                location = demandManager.currentDemands.index(demandManager.addedDemands[i])
                demandManager.currentDemands[location].demandPathId = path
                #print self
        print "Virtual Network"
        print self
        print "Utilized Paths"
        print utilizationSet.partUtilized
        print "Not Utilzed Paths"
        print utilizationSet.notUtilized
        print demandManager.printAddedDemands()
        print demandManager.printCurrentDemands()
