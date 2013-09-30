#Also keep track of when demands are met and when they are not.
import re
import copy

from DemandClass import *

class DemandMGMT:
    waiting_demands = []
    current_demands = []
    added_demands = []

    def __init__(self, init_demands):
        self.waiting_demands = []
        self.current_demands = []
        self.added_demands = []

        self.waiting_demands = copy.deepcopy(init_demands)

    def checkDemands(self, time):
        self.added_demands = []
        for d in range(len(self.waiting_demands)):
            if time >= self.waiting_demands[d].startTime:
                self.current_demands.append(self.waiting_demands[d])
        rmList = []
        for d in range(len(self.waiting_demands)):
            if time >= self.waiting_demands[d].startTime:
                rmList.append(self.waiting_demands[d])
        for a in range(len(rmList)):
            self.waiting_demands.remove(rmList[a])
        for d in range(len(self.current_demands)):
            if time is self.current_demands[d].startTime:
                self.added_demands.append(self.current_demands[d])

    def addUpDemands(self, path):
        path_demands = []
        demand = 0
        for i in range(len(path)):
            for j in range(len(self.current_demands)):
                if self.current_demands[j].demand_path_id == i:
                    demand = demand + self.current_demands[j].demand
            path_demands.append(demand)
            demand = 0
        return path_demands

    def decrementCurrentDemands(self):
        for i in range(len(self.current_demands)):
            self.current_demands[i].decrementDur(1)
        self.current_demands = [x for x in self.current_demands
                               if x.duration is not 0]

    def clearAddedDemands(self):
        self.added_demands = []

    def printCurrentDemands(self):
        print "Current Demands"
        for demands in self.current_demands:
            print str(demands)

    def printWaitingDemands(self):
        print "Waiting Demands"
        for demands in self.waiting_demands:
            print str(demands)

    def printAddedDemands(self):
        print "Added Demands"
        for demands in self.added_demands:
            print str(demands)

    def __str__(self):
        string = "Current Demands:\n"
        for demands in self.current_demands:
            string = string + str(demands) + "\n"
        string = string + "Added Demands:\n"
        for demands in self.added_demands:
            string = string + str(demands) + "\n"
        string = string + "Waiting Demands:\n"
        for demands in self.waiting_demands:
            string = string + str(demands) + "\n"
        return string
