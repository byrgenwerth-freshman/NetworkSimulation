###############################################################################
#main.py by Matt Owens
#email: mattowens11@gmail.com
###############################################################################
import cplex
import os
import re
import sys
from cplexSimModule import *
from demandMGMTModule import *
from startModule import *
from visualizationModule import *
from capacityMGMTModule import *
from virtualNetworkMGMTModule import *
from networkMGMTModule import *
from realNetworkMGMTModule import *
from utilizationMGMTModule import *
from linkReListMGMTModule import *
from removeListMGMTModule import *
from cplexLB import *
###############################################################################
#GLOBALS
#Figure out what id is?
id = 0
flag = False 
timesFlagged = []
secondLevelFlag = False
secondTimesFlagged = []
###############################################################################
#Argument contols
###############################################################################
if len(sys.argv) is 1:
    fin = getFiles("What is the name of the demand file?")
    outputFile = raw_input("What would you like to name the output file?")
    fout = open(outputFile, "w")
    finPaths = getFiles("What is the name of the path info file?")
    #Virtual Network
    finNetwork = getFiles("What is the name of the virtual network info file?")
    #Dynamic or Static
    dynamic = get1or0("Do you want dynamic flows or static flows?")
    #Overbooking
    overbooking = get1or0("Do you want overbooking?")
    #Capacity
    capacity = getInt("What value do you want your capacity to be?")
    #Overbooking value
    overBookingValue = getInt("What value do you want for overbooking?")
elif len(sys.argv) is 9:
    demandFile = sys.argv[1]
    fin = open(demandFile, "r")
    outputFile = sys.argv[2]
    fout = open(outputFile, "w")
    pathFile = sys.argv[3]
    finPaths = open(pathFile, "r")
    virtualNetworkFile = sys.argv[4]
    finNetwork = open(virtualNetworkFile , "r")
    dynamic = int(sys.argv[5])
    overbooking = int(sys.argv[6])
    capacity = int(sys.argv[7])
    overBookingValue = int(sys.argv[8])
else:
    wrongInputErrorMessage()
    exit(2)
##############################################################################
#Seting up networks(Real Network and Virtual Networks)
##############################################################################
counter = 0
getNumbers = re.compile("[\d]+")
virtualNetworks = VirtualNetworkMGMT()
for lines in finNetwork:
    ###########################################################################
    #Setting up real network set
    ###########################################################################
    if counter is 0:
        physNet = realNetwork(lines)
    else:
        getNumbers = re.compile("[\d]+")
        numbers = getNumbers.findall(lines)
        numbers = map(int, numbers)
        virtualNetworks.createVirtualNetwork(numbers)
    counter = counter + 1
print virtualNetworks
print physNet.gPathName
print "This is the real network"
print physNet.gPathName
print "This is the virtual network."
print virtualNetworks
###############################################################################
#Setting up utilization sets
###############################################################################
#Put in utilization MGMT module
utilized = utilizationSet(physNet.gPathName, virtualNetworks)
print str(utilized)
#Must come after setting up the utilization sets are set up.
#This is because the additional list messes up the set utilization.
printBreak(fout)
###############################################################################
#Generating k shortest path for the network, if there is no file
###############################################################################
if os.path.isfile("kshortestpaths.txt") is False:
    for lines in finPaths:
        if lines[0] is not "#":
            getNumbers = re.compile("[\d]+")
            numbers = getNumbers.findall(lines)
            numbers = map(int, numbers)
            os.system("./IanProg {0} {1} {2}".format(numbers[0], numbers[1],
                                                     numbers[2]))
finPaths.close()
#Setting demand to 0
demand = 0
###############################################################################
#Creating the network attributes object
###############################################################################
network = Network("kshortestpaths.txt", "SampleFatTreeTopology.txt" )
print network.coef
print network.equation
print network.demandeq
print network.capacity
#This is a test of convertToLb
LBnetwork = network.convertToLB()
print LBnetwork.coef
print LBnetwork.equation
print LBnetwork.demandeq
print LBnetwork.capacity
###############################################################################
#Creating the  Capacity Table
###############################################################################
capacityTable = CapacityTable(network.capacity, capacity)
###############################################################################
#Creating the demand manager
###############################################################################
#The demand list is [demand location, demand, duration, start]
demandManager = DemandMGMT(fin)
fin.close()
print str(demandManager)
###############################################################################
#Initialization finished
###############################################################################
#Link removal list
linkReList = []
time = 0
###############################################################################
while (len(demandManager.currentDemands) is not 0
       or len(demandManager.waitingDemands) is not 0):
    print "This is time " + str(time)
    fout.write("This is time " + str(time) + "\n" )
    ###########################################################################
    #Checking to see if there are any new demands for this time
    ###########################################################################
    demandManager.demandCheckCurrent(time)
    demandManager.getAddedDemands(time)
    demandManager.demandCheckWaiting(time)
    #Printing Demands
    print str(demandManager)
    PathDemands = addUpDemands(demandManager.currentDemands, network.demandeq)
    print PathDemands
    ###########################################################################
    #Creating the CPLEX file
    ###########################################################################
    model = createLBCPLEXmodel(LBnetwork, PathDemands, capacityTable)
    #Sets up output streams
    setStream(model, "output")
    model.get_problem_type()
    ###########################################################################
    #Solve equation
    ###########################################################################
    #Print problem using write(filename, filetype='mps,lp,sav')
    model.write("file.lp", filetype="lp")
    exit()
    model.solve()
    ###########################################################################
    #Inspect Information
    ###########################################################################
    solutions = []
    while True:
        try:
            solutions = model.solution.get_values()
            results = printResults(network, solutions, fout)
            break
        #######################################################################
        #Find new equation if solution failed
        #######################################################################
        except cplex.exceptions.CplexSolverError:
            #If you are doing dynamic allocation of paths
            if dynamic:
                virtualNetworks.addTempPath(utilized, demandManager)
            #If you are doing any overbooking
            if overbooking:
                capacity = capacity + overbooking
            print "This solution failed."
            print "Trying alternate capacities."
            flag = True
            fout.write("This solution failed\n")
            fout.write("Trying alternate solution\n")
            PathDemands = addUpDemands(demandManager.currentDemands,
                                       network.demandeq)
            model = createCPLEXmodel(network, PathDemands, capacityTable)
            setStream(model, "output")
            model.get_problem_type()
            model.solve()
            #Setting the demand back to what it was if overbooking
            if overbooking:
                capacity = capacity - overbooking
            try:
                solutions = model.solution.get_values()
                reults = printResults(network, solutions, fout)
                break
            #Falied with new solution, block
            except cplex.exceptions.CplexSolverError:
                print "Failed with new rerouting"
                secondLevelFlag = True
            break
    #Print the virtual network information to see if there is a change
    print virtualNetworks
    fout.write(str(virtualNetworks) + "\n")
    ###########################################################################
    #Update the capacity table with current dataflow
    ###########################################################################
    capacityTable.capacityTableUpdate(results, secondLevelFlag, linkReList, id,
                                      demandManager.currentDemands)
    ###########################################################################
    #Keeping track of the amount of time the network is blocked
    ###########################################################################
    if flag is True:
        flag = False
        metric = []
        metric.append(time)
        metric.append(list(demandManager.currentDemands))
        timesFlagged.append(metric)
    if secondLevelFlag is True:
        secondLevelFlag = False
        metric1 = []    
        metric1.append(time)
        metric1.append(list(demandManager.currentDemands))
        secondTimesFlagged.append(metric1)
    ###########################################################################
    #Decrease the duration
    ###########################################################################
    #This checks to decrease the duration of the of the capacity changes.
    linkReList = decrementLinkReList(linkReList)
    removeList = createRemoveList(linkReList) 
    #Add the capacity decreases back
    capacityTable.restoreCapacity(removeList)
    #Remove the items in the remove list
    linkReList = removeExpiredLinkReList(linkReList, removeList)
    print linkReList
    #In the demands
    demandManager.decrementCurrentDemands()
    #Clear out the added demands for this time period
    demandManager.clearAddedDemands()
    #Increase the time period
    time = time + 1
    printBreak(fout)
###############################################################################
print virtualNetworks
numAdded = 0
for i in range(len(virtualNetworks.vnContainer)):
    numAdded = numAdded + len(virtualNetworks.vnContainer[i].addedPaths)
print numAdded
print "Initial Blocks Times"
print timesFlagged
print "Initial Number of Blocks"
print len(timesFlagged)
demandsBlocked = 0
for i in range(len(timesFlagged)):
    demandsBlocked = demandsBlocked + len(timesFlagged[i][1])
print demandsBlocked
fout.write(str(timesFlagged) + "\n")
fout.write(str(len(timesFlagged)) + "\n")
print "Secondary Block Times"
print secondTimesFlagged
print "Secondary Number of Blocks"
print len(secondTimesFlagged)
demandsBlocked = 0
for i in range(len(secondTimesFlagged)):
    demandsBlocked = demandsBlocked+ len(secondTimesFlagged[i][1])
print demandsBlocked
fout.write(str(secondTimesFlagged) + "\n")
fout.write(str(len(secondTimesFlagged)) + "\n")
for line in capacityTable.capacityTable:
    print line.capacity
