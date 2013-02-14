import cplex
from cplexSimModule import *

def createLBCPLEXmodel(network, PathDemands, capacityTable):
    model = cplex.Cplex()

    #Give it a name                                        
    model.set_problem_name("Topo1")
    #Setting it as minimiztion problem   
    model.objective.set_sense(-1)
    #Give Cplex the minimization equation                                      
    model.variables.add(names = network.equation, obj = network.coef)
    #Give Cplex the demand equations                                           
    coef = []
    cplexDemandLB(model, network, coef, PathDemands)
    #Give Cplex the capacity equations                                         
    coef = []
    cplexCapacity(model, network, coef, capacityTable)
    return model

def cplexDemandLB(model, network, coef, PathDemands):
    for i in range(len(network.demandeq)):
        for j in range(len(network.demandeq[i])):
        	if network.demandeq[i][j] == "Z":
        		coef.append(- 1 * PathDemands[i])
        	else:
        		coef.append(1.0)
        addConstraint(model, network.demandeq[i], coef,
                      "demand{0}".format(i+1), 0, "E")
            #Making the coeficient list empty for the next equation            
        coef = []
