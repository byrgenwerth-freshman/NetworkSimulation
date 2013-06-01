#Put new method code in here
import cplex
from cplexSimModule import *

#Constructor
def createSelectCPLEXmodel(network, PathDemands, capacityTable, demandManager,
                            utilized):
    model = cplex.Cplex()
    model.objective.set_sense(1)
    convertToSelect(model, network, demandManager)
    #Need to update the equation to include the needed variables
    #Create 
    model.variables.add(names = network.equation, obj = network.coef)
    addBinary(model, demandManager)
    cplexDemandSel(model, network, PathDemands, demandManager, utilized)
    coef = []
    cplexCapacity(model, network, coef, capacityTable)
    
    return model

def convertToSelect(model, network, demandManager):
    print network.equation
    #Create additional variables and set coeficient to 0
    for i in range(len(demandManager.currentDemands)):
        print demandManager.currentDemands[i]
        cvar = "y" + str(i + 1)
        network.equation.append(cvar)
        network.coef.append(0)

    model.variables.add(names = network.equation, obj = network.coef)
    #Clean up the equation
    for i in range(len(demandManager.currentDemands)):
        network.equation.pop()
        network.coef.pop()
    print network.equation 

def addBinary(model, demandManager):
    for i in range(len(demandManager.currentDemands)):
        cvar = "y" + str(i + 1)
        model.variables.set_types(cvar, model.variables.type.binary)

def cplexDemandSel(model, network, PathDemands, demandManager, utilized):
    #Add the demands to the open groups of paths
    coef = []
    for i in range(len(network.demandeq)):
        for j in range(len(network.demandeq[i])):
            coef.append(1)
        try:
            if utilized.notUtilized.index(i) is not -1:
                for k in range(len(demandManager.currentDemands)):
                    coef.append(demandManager.currentDemands[k].demand * -1)
                    cvar = "y" + str(k + 1) 
                    network.demandeq[i].append(cvar)
        except ValueError:
            pass
        addConstraint(model, network.demandeq[i], coef,
                      "demand{0}".format(i+1), PathDemands[i], "E")
        print "Start"
        print network.demandeq[i]
        #Clean
        sentinal = True
        try:
            if utilized.notUtilized.index(i) is not -1:
                for k in range(len(demandManager.currentDemands)): 
                    network.demandeq[i].pop()
        except ValueError:
            pass

        print "End"
        print network.demandeq[i]

        coef = []


