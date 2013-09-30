###############################################################################
import re
from CapacityClass import *

class CapacityTable:
    capacity_table = []
    links_to_remove = []

    def __init__(self, capacities):
        self.capacity_table = capacities

    def capacityTableUpdate(self, results, secondLevelFlag, linkReList,
                            id, currentDemands):
        if results is not "Failed":
            for i in range(len(results[0])):
                print results[0][i] + ": " + results[1][i]
                #Check to see if the results are greater than 0
                if float(results[1][i]) > float(0) and secondLevelFlag is False:
                    #Grabs each line of information from the capacity table
                    for lists in self.capacity_table:
                        #Search for the index value
                        try:
                            index = lists[2].index(results[0][i])
                        except:
                            index = -1
                        #If it has that value
                        if index is not -1:
                            addList = []
                            #Subtract the results from capacity
                            lists[1] = float(lists[1]) - float(results[1][i])
                            addList.append(lists[0])
                            addList.append(results[0][i])
                            addList.append(results[1][i])
                            linkReList.append(addList)
            pathRe = re.compile("x\d+")

            for d in currentDemands:
                print d
                demandP = d.demand_path_id + 1
                for i in range(len(linkReList)):
                    if len(linkReList[i]) < 4:
                        match = pathRe.search(linkReList[i][1])
                        thePath = match.group()
                        if str(thePath).strip() == str("x" + str(demandP)).strip():
                            linkReList[i].append(d[3])
                            linkReList[i].append(id)
                            id = id + 1
        else:
            pass

    def restoreCapacity(self):
        #Decrement Links to remove
        for i in range(len(self.links_to_remove)):
            #Decrease the duration of capacity changes.
                if len(self.links_to_remove[i]) > 3:
                    self.links_to_remove[i][3] = self.links_to_remove[i][3] - 1

        #Create Remove List
        remove_list = []
        for i in range(len(self.links_to_remove)):
            if len(self.links_to_remove[i]) > 3:
                if self.links_to_remove[i][3] <= 0:
                    remove_list.append(self.links_to_remove[i])


        #Restore Capacities
        for line in remove_list:
            for i in range(len(self.capacity_table)):
                if line[0] == self.capacity_table[i][0]:
                    self.capacity_table[i][1] = (float(self.capacity_table[i][1])
                                                + float(line[2]))


        #Remove expired links
        for i in range(len(remove_list)):
            self.links_to_remove.remove(remove_list[i])

    def printCapList(self):
        print self.capacity_table
        for caps in self.capacity_table:
            caps.printCap()
