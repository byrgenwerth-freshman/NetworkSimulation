###############################################################################
import re
from CapacityClass import *

class CapacityTable:
    capacity_table = []
    links_to_remove = []
    remove_id = 0

    def __init__(self, capacities):
        self.capacity_table = capacities

    def capacityTableUpdate(self, results, secondLevelFlag,
                            demand_manager):
        #Checks to see if the solution failed
        if results is not "Failed":
            #Goes through all the results
            for i in range(len(results[0])):
                #Check to see if the results are greater than 0
                #If the result is more than 0
                if (float(results[1][i]) > float(0) and secondLevelFlag is False
                    and results[0][i] != 'z'):
                    #Grabs each capacity of information from the capacity table
                    for cap in self.capacity_table:
                        #Search for the index value of the link to remove
                        #capcity
                        try:
                            index = cap.list_of_paths.index(results[0][i])
                        except:
                            index = -1
                        #If it has that value
                        if index is not -1:
                            addList = []
                            #Subtract the results from capacity
                            cap.capacity = float(cap.capacity) - float(results[1][i])
                            #Add the link
                            addList.append(cap.link)
                            #Add the result
                            addList.append(results[0][i])
                            addList.append(results[1][i])
                            self.links_to_remove.append(addList)
            pathRe = re.compile("x\d+")
            not_dec = []
            for d in demand_manager.current_demands:
                if d.demand != 0:
                    not_dec.append(d)
            #Go through added demands
            for d in not_dec:
                demandP = d.demand_path_id + 1
                #Go through all the links to remove
                for i in range(len(self.links_to_remove)):
                    #Look at those without ids
                    if len(self.links_to_remove[i]) < 4:
                        match = pathRe.search(self.links_to_remove[i][1])
                        thePath = match.group()
                        #If it has the demand has the path
                        if str(thePath).strip() == str("x" + str(demandP)).strip():
                            #Then add the duration
                            self.links_to_remove[i].append(d.duration)
                            #Add an id
                            self.links_to_remove[i].append(self.remove_id)
                            self.remove_id += 1
                d.demand = 0
            for link in self.links_to_remove:
                if len(link) < 4:
                    exit()
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
                if line[0] == self.capacity_table[i].link:
                    self.capacity_table[i].capacity = (float(self.capacity_table[i].capacity)
                                                + float(line[2]))


        #Remove expired links
        for i in range(len(remove_list)):
            self.links_to_remove.remove(remove_list[i])

    def __str__(self):
        all_caps = ""
        for caps in self.capacity_table:
            all_caps += str(caps)
        return all_caps

    def addOverbooking(self, overbooking_value):
        for i in range(len(self.capacity_table)):
            self.capacity_table[i].capacity = self.capacity_table[i].capacity + overbooking_value

    def removeOverbooking(self, overbooking_value):
        for i in range(len(self.capacity_table)):
            self.capacity_table[i].capacity = self.capacity_table[i].capacity - overbooking_value

