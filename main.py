###############################################################################
#main.py by Matt Owens
#email: mattowens11@gmail.com
###############################################################################
import cplex
import os
#Check to see if "import re" can be taken out
import re
import sys
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

#GLOBALS
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
elif len(sys.argv) is 2:
    configFile = sys.argv[1]
    cfs = open(configFile, 'r')
    content = []
    for line in cfs:
    #throw out comment lines
        if line.startswith('#'):
            pass
    #throw out blank lines or incomplete lines
        elif(len(line.split()) != 10):
            pass
        else:
            content.append(line.split())
    filePath = content[0][0]
    binary = content[0][1]
    demandFile = content[0][2]
    fin = open(filePath + demandFile, "r")
    outputFile = content[0][3]
    pathFile = content[0][4]
    finPaths = open(filePath + pathFile, "r")
    virtualNetworkFile = content[0][5]
    finNetwork = open(filePath + virtualNetworkFile , "r")
    dynamic = int(content[0][6])
    overbooking = int(content[0][7])
    capacity = int(content[0][8])
    overBookingValue = int(content[0][9])
    fout = open("OUTPUT/" + outputFile + str(dynamic) + "-" + str(overbooking) +
                "-" + str(capacity) + "-" +str(overBookingValue) + ".txt", "w")
    pathFiles = filePath + "kshortestpaths.txt"
    topologyFile = filePath + "SampleFatTreeTopology.txt"

elif len(sys.argv) is 9:
    demandFile = sys.argv[1]
    fin = open(demandFile, "r")
    outputFile = sys.argv[2]
    pathFile = sys.argv[3]
    finPaths = open(pathFile, "r")
    virtualNetworkFile = sys.argv[4]
    finNetwork = open(virtualNetworkFile , "r")
    dynamic = int(sys.argv[5])
    overbooking = int(sys.argv[6])
    capacity = int(sys.argv[7])
    overBookingValue = int(sys.argv[8])
    fout = open("OUTPUT/" + outputFile + str(dynamic) + "-" + str(overbooking) +
                "-" + str(capacity) + "-" +str(overBookingValue) + ".txt", "w")

else:
    wrongInputErrorMessage()
    exit(2)

originalMain(filePath, binary, fin, fout, pathFile, topologyFile, finPaths, finNetwork, capacity, flag, timesFlagged, secondLevelFlag, secondTimesFlagged, dynamic, overbooking, overBookingValue, outputFile)






