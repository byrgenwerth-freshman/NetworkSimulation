import cplex
from cplexSimModule import *

def createLBCPLEXmodel(network, PathDemands, capacityTable):
    
    #Need to have a test to see if this has been initiated
    if network.equation[-1] is not "Z":
        network = convertToLB(network)

    model = cplex.Cplex()
    #Give it a name                                        
    model.set_problem_name("Topo1")
    #Setting it as minimiztion problem   
    model.objective.set_sense(1)
    #Give Cplex the minimization equation                                      
    model.variables.add(names = network.equation, obj = network.coef)
    #Give Cplex the demand equations                                           
    coef = []
    cplexDemandLB(model, network, coef, PathDemands)
    #Give Cplex the capacity equations                                         
    coef = []
    cplexCapacity(model, network, coef, capacityTable)
    return model

def convertToLB(network):
    networkLB = network
    networkLB.equation = network.equation
    networkLB.coef = []
    for i in range(len(networkLB.equation)):
        networkLB.coef.append(0)
    networkLB.coef.append(1)
    networkLB.equation.append("Z")
    networkLB.demandeq = network.demandeq
    networkLB.capacity = network.capacity
    for i in range(len(networkLB.capacity)):
        networkLB.capacity[i][1].append("Z")
    return networkLB

#This is the same as the other Demand equations
def cplexDemandLB(model, network, coef, PathDemands):
    for i in range(len(network.demandeq)):
        for j in range(len(network.demandeq[i])):
            coef.append(1.0)
        addConstraint(model, network.demandeq[i], coef,
                      "demand{0}".format(i+1), PathDemands[i], "E")
            #Making the coeficient list empty for the next equation            
        coef = []


def cplexCapacity(model, network, coef, capacityTable):
    for i in range(len(network.capacity)):
        for j in range(len(network.capacity[i][1])):
            if network.capacity[i][1][j] == "Z":
                coef.append(- 1 * capacityTable.capacityTable[i].capacity)
            else:
                coef.append(1.0)
        addConstraint(model, network.capacity[i][1], coef,
                      "link{0}".format(network.capacity[i][0]), 0, "L")
        #Making the coeficient list empty for the next Equation                
        coef = []
    #
    addConstraint(model, ["Z"], [1], "ZCont", 1, "L")


