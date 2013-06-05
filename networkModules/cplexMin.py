import cplex
from cplexSimModule import *

def createCPLEXmodel(network, PathDemands, capacityTable):
    model = cplex.Cplex()

    #Give it a name                                        
    model.set_problem_name("Topo1")
    #Setting it as minimiztion problem   
    model.objective.set_sense(1)
    #Give Cplex the minimization equation                                      
    model.variables.add(names = network.equation, obj = network.coef)
    #Give Cplex the demand equations                                           
    coef = []
    cplexDemand(model, network, coef, PathDemands)
    #Give Cplex the capacity equations                                         
    cplexCapacity(model, network, capacityTable)
    return model

def cplexDemand(model, network, coef, PathDemands):
    for i in range(len(network.demandeq)):
        for j in range(len(network.demandeq[i])):
            coef.append(1.0)
        addConstraint(model, network.demandeq[i], coef,
                      "demand{0}".format(i+1), PathDemands[i], "E")
            #Making the coeficient list empty for the next equation            
        coef = []