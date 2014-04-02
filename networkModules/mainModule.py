import cplex
import re
import os
from networkModules.cplexSimModule import *
from networkModules.demandMGMTModule import *
from networkModules.startModule import *
from networkModules.visualizationModule import *
from networkModules.capacityMGMTModule import *
from networkModules.virtualNetworkMGMTModule import *
from networkModules.networkMGMTModule import *
from networkModules.realNetworkMGMTModule import *
from networkModules.utilizationMGMTModule import *
from networkModules.cplexLB import *
from networkModules.cplexMin import *
from networkModules.cplexSelection import *
from networkModules.mainModule import *
###############################################################################
def originalMain(filePath, binary, fin, fout, pathFile, topologyFile, finPaths,
				    finNetwork, capacity, flag, timesFlagged, secondLevelFlag,
				    secondTimesFlagged, dynamic, overbooking, overBookingValue,
                    outputFile):
    ###########################################################################
    #Setting up networks(Real Network and Virtual Networks)
    ###########################################################################
    counter = 0
    agent_numbers = re.compile("[\d]+")
    tmp_virtual_network = []
    for lines in finNetwork:
        #######################################################################
        #Setting up real network set
        #######################################################################
        if counter is 0:
            phys_net = RealNetwork(int(str(lines).strip()))
        else:
            getNumbers = re.compile("[\d]+")
            numbers = getNumbers.findall(lines)
            numbers = map(int, numbers)
            tmp_virtual_network.append(VirtualNetwork(numbers))
            #virtual_networks.createVirtualNetwork(numbers)
        counter = counter + 1
    virtual_networks = VirtualNetworkMGMT(tmp_virtual_network)
    ###########################################################################
    #Setting up utilization sets
    ###########################################################################
    #Put in utilization MGMT module
    utilized = UtilizationSet(phys_net, virtual_networks)
    #Must come after setting up the utilization sets are set up.
    #This is because the additional list messes up the set utilization.
    printBreak(fout)
    ###########################################################################
    #Generating k shortest path for the network, if there is no file
    ###########################################################################
    pathFile = filePath + pathFile
    if os.path.isfile(pathFile) is False:
        for lines in finPaths:
            if lines[0] is not "#":
                getNumbers = re.compile("[\d]+")
                numbers = getNumbers.findall(lines)
                numbers = map(int, numbers)
                os.system(filePath + binary + " {0} {1} {2}".format(numbers[0],
                                                                    numbers[1],
                                                                    numbers[2]))
    finPaths.close()
    #Setting demand to 0
    #Is this needed?
    demand = 0
    ###########################################################################
    #Creating the network attributes object
    ###########################################################################
    network = Network(filePath + "kshortestpaths.txt", topologyFile)
    ###########################################################################
    #Creating the  Capacity Table
    ###########################################################################
    raw_capacities = network.capacity
    capacities = []
    for raw_capacity in raw_capacities:
        raw_capacity = Capacity(raw_capacity[0], capacity, raw_capacity[1])
        capacities.append(raw_capacity)
    capacity_table = CapacityTable(capacities)
    ###########################################################################
    #Creating the demand manager
    ###########################################################################
    #The demand list is [demand location, demand, duration, start]
    #Processing the data
    demands = []
    for lines in fin:
        if lines[0] is not "#":
            getNumbers = re.compile("[\d]+")
            numbers = getNumbers.findall(lines)
            numbers = Demand(int(numbers[0]), int(numbers[1]),
                                int(numbers[2]), int(numbers[3]),
                                int(numbers[4]))
            demands.append(numbers)
    demand_manager = DemandMGMT(demands)
    fin.close()
    ###########################################################################
    #Initialization finished
    ###########################################################################
    #Link removal list
    linkReList = []
    time = 0
    ###########################################################################
    while (len(demand_manager.current_demands) is not 0
           or len(demand_manager.waiting_demands) is not 0):
        print "This is time " + str(time)
        fout.write("This is time " + str(time) + "\n" )
        #######################################################################
        #Checking to see if there are any new demands for this time
        #######################################################################
        demand_manager.checkDemands(time)
        #Printing Demands
        path_demands = demand_manager.addUpDemands(network.demandeq)
        #######################################################################
        #Creating the CPLEX file
        #######################################################################
        load_balance_eq = LoadBalancingModel(network, path_demands,
                                                capacity_table)

        #######################################################################
        #Solve equation
        #######################################################################
        print "Solving Problem"
        load_balance_eq.solve(outputFile, dynamic, overbooking, capacity,
                                        overBookingValue, time, fout)

        #######################################################################
        #Inspect Information
        #######################################################################
        if load_balance_eq.has_solution is False:
            ###################################################################
            #Find new equation if solution failed
            ###################################################################
            #If you are doing dynamic allocation of paths
            if dynamic == 1:
                virtual_networks.addTempPath(utilized, demand_manager)
            #If you are doing any overbooking
            if overbooking == 1:
                #capacity = capacity + overBookingValue
                capacity_table.addOverbooking(overBookingValue)
            print "This solution failed."
            print "Trying alternate capacities."
            flag = True
            fout.write("This solution failed\n")
            fout.write("Trying alternate solution\n")
            path_demands = demand_manager.addUpDemands(network.demandeq)
            load_balance_eq = LoadBalancingModel(network, path_demands,
                                                    capacity_table)
            setStream(load_balance_eq.model, "output")
            load_balance_eq.solve(outputFile, dynamic, overbooking, capacity,
                                        overBookingValue, time, fout)
            if load_balance_eq.has_solution is False:
                secondLevelFlag = True
            #Setting the demand back to what it was if overbooking
            if overbooking == 1:
                capacity_table.removeOverbooking(overBookingValue)
        fout.write(str(virtual_networks) + "\n")
        #######################################################################
        #Update the capacity table with current dataflow
        #######################################################################
        capacity_table.capacityTableUpdate(load_balance_eq.results,
                                            secondLevelFlag,
                                            demand_manager)
        #######################################################################
        #Keeping track of the amount of time the network is blocked
        #######################################################################
        if flag is True:
            flag = False
            metric = []
            metric.append(time)
            metric.append(list(demand_manager.current_demands))
            timesFlagged.append(metric)
        if secondLevelFlag is True:
            secondLevelFlag = False
            metric1 = []
            metric1.append(time)
            metric1.append(list(demand_manager.current_demands))
            secondTimesFlagged.append(metric1)
        #######################################################################
        #Decrease the duration
        #######################################################################
        capacity_table.restoreCapacity()
        demand_manager.decrementCurrentDemands()
        #Clear out the added demands for this time period
        #Increase the time period
        time = time + 1
        printBreak(fout)
    ###########################################################################
    print virtual_networks
    numAdded = 0
    for i in range(len(virtual_networks.vn_container)):
        numAdded = numAdded + len(virtual_networks.vn_container[i].added_paths)
    print numAdded
    #print "Initial Blocks Times"
    #print timesFlagged
    print "Initial Number of Blocks"
    print len(timesFlagged)
    demandsBlocked = 0
    for i in range(len(timesFlagged)):
        demandsBlocked = demandsBlocked + len(timesFlagged[i][1])
    print demandsBlocked
    #fout.write(str(timesFlagged) + "\n")
    fout.write(str(len(timesFlagged)) + "\n")
    #print "Secondary Block Times"
    #print secondTimesFlagged
    print "Secondary Number of Blocks"
    print len(secondTimesFlagged)
    demandsBlocked = 0
    for i in range(len(secondTimesFlagged)):
        demandsBlocked = demandsBlocked+ len(secondTimesFlagged[i][1])
    print demandsBlocked
    #fout.write(str(secondTimesFlagged) + "\n")
    fout.write(str(len(secondTimesFlagged)) + "\n")
    for line in capacity_table.capacity_table:
        print line.capacity
###############################################################################
