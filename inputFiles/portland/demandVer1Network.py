import sys
import random
import math

lamb = 2.7
#The number of virtualized networks
networks = int(sys.argv[1])
#The time when each virtual network is initialized
newNetworksInterval = int(sys.argv[2])
#How long a network is in use
networkDuration = int(sys.argv[3])
#The number of paths in the network
path = sys.argv[4]
#The Demand
demand = sys.argv[5]
#How long the demand last
duration = sys.argv[6]
#Interval Arrival time
interArrivalTime = sys.argv[7]
#Initial time of zero
start = 0
#List that holds the topology
topo = []
#Puts lists for the individual networks
for i in range(networks):
    topo.append([])
print topo

#
for i in range(len(topo)):
    while len(topo[i]) is not 4:
        test = True 
        number = random.randint(0, int(path) - 1)
        for j in range(len(topo)):
            for k in range(len(topo[j])):
                if topo[j][k] is number:
                    test = False
        if test is True:
            topo[i].append(number)
print topo
fout = open("virtualNetworks.txt", "w")
fout.write(path)
fout.write("\n")

for network in topo:
    for numb in network:
        fout.write(str(numb))
        fout.write(" ")
    fout.write("\n")

fout.close()

#
fout = open("DemandFile.txt", "w")

#
for i in range(int(networks)):
    while(start < int(networkDuration)):
        #(VN Path Demand Duration Start_Time)
        demandString = str(i)
        demandString = demandString + " " + str(topo[i][random.randint(0, len(topo[i]) - 1)])
        demandString = demandString + " " + str(int(int(demand) *  (-1 * (1/float(lamb)) * math.log(random.random()))) + 1 )
        demandString = demandString + " " + str(int(math.ceil((int(-1 * int(duration) * math.log(random.random()))))) + 1 )
        start = start + int(math.ceil((int(-1 * int(interArrivalTime) * math.log(random.random())))))
        demandString = demandString + " " + str(start)
        print demandString
        fout.write(demandString + "\n")
    start = (i + 1) * newNetworksInterval
    networkDuration = networkDuration + start

fout.close()
