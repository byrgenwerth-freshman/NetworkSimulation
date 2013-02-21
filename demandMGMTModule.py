#Also keep track of when demands are met and when they are not.
import re
from DemandClass import *

class DemandMGMT:
    waitingDemands = []
    currentDemands = []
    addedDemands = []

    def __init__(self, fin):
        for lines in fin:
            if lines[0] is not "#":
                getNumbers = re.compile("[\d]+")
                numbers = getNumbers.findall(lines)
                numbers = Demand(int(numbers[0]), int(numbers[1]),
                                 int(numbers[2]), int(numbers[3]),
                                 int(numbers[4]))
                self.waitingDemands.append(numbers)
        
    def demandCheckCurrent(self, time):
        for d in range(len(self.waitingDemands)):
            if time is self.waitingDemands[d].startTime:
                self.currentDemands.append(self.waitingDemands[d])
 
    def getAddedDemands(self, time):
        for d in range(len(self.waitingDemands)):
            if time is self.waitingDemands[d].startTime:
                self.addedDemands.append(self.waitingDemands[d])

    def demandCheckWaiting(self, time):
        rmList = []
        for d in range(len(self.waitingDemands)):
            if time is self.waitingDemands[d].startTime:
                rmList.append(self.waitingDemands[d])
        for a in range(len(rmList)):
                self.waitingDemands.remove(rmList[a])

    def decrementCurrentDemands(self):
        for i in range(len(self.currentDemands)):
            self.currentDemands[i].decrementDur(1)
        self.currentDemands = [x for x in self.currentDemands
                               if x.duration is not 0]

    def clearAddedDemands(self):
        self.addedDemands = []

    def printCurrentDemands(self):
        print "Current Demands"
        for demands in self.currentDemands:
            print str(demands)
    
    def printWaitingDemands(self):
        print "Waiting Demands"
        for demands in self.waitingDemands:
            print str(demands)

    def printAddedDemands(self):
        print "Added Demands"
        for demands in self.addedDemands:
            print str(demands)

    def __str__(self):
        string = "Current Demands:\n"
        for demands in self.currentDemands:
            string = string + str(demands) + "\n"
        string = string + "Added Demands:\n"
        for demands in self.addedDemands:
            string = string + str(demands) + "\n"
        string = string + "Waiting Demands:\n"
        for demands in self.waitingDemands:
            string = string + str(demands) + "\n"
        return string
