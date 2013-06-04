###############################################################################
#cplexSelection.py
#By Matthew Owens
#Email: mattowens11@gmail.com
###############################################################################
import cplex
from cplexSimModule import *
###############################################################################

###############################################################################
#Function: createSelectCPLEXmodel
#Pre:
#Post:
###############################################################################
def createSelectCPLEXmodel(network, PathDemands, capacityTable, demandManager,
                            utilized):
    #Creating the model
    model = cplex.Cplex()
    #Setting equation as minimization
    model.objective.set_sense(1)
    #Adding the additional variables to the selection model.
    convertToSelect(model, network, demandManager, utilized)
    #Making those variables binary balues
    addBinary(model, demandManager)
    #Creating the demands
    cplexDemandSel(model, network, PathDemands, demandManager, utilized)
    #Adding the capacity
    cplexCapacity(model, network, capacityTable)
    selectionEquations(model, demandManager, utilized)

    return model
###############################################################################

###############################################################################
#Function: convertToSelect
#Pre:
#Post:
###############################################################################
def convertToSelect(model, network, demandManager, utilized):
    #Create additional variables and set coeficient to 0
    print len(demandManager.currentDemands) * len(utilized.notUtilized)
    for i in range(len(demandManager.currentDemands) 
                    * len(utilized.notUtilized)):
        cvar = "y" + str(i + 1)
        network.equation.append(cvar)
        network.coef.append(0)
    print network.equation
    model.variables.add(names = network.equation, obj = network.coef)
    #Clean up the equation
    for i in range(len(demandManager.currentDemands) 
                    * len(utilized.notUtilized)):
        network.equation.pop()
        network.coef.pop()
###############################################################################


###############################################################################
#Function: addBinary
#Pre:
#Post:
###############################################################################
def addBinary(model, demandManager):
    for i in range(len(demandManager.currentDemands)):
        cvar = "y" + str(i + 1)
        model.variables.set_types(cvar, model.variables.type.binary)
###############################################################################

###############################################################################
#Function: cplexDemandSel
#Pre:
#Post:
###############################################################################
def cplexDemandSel(model, network, PathDemands, demandManager, utilized):
    #Add the demands to the open groups of paths
    varMul = 1
    coef = []
    for i in range(len(network.demandeq)):
        for j in range(len(network.demandeq[i])):
            coef.append(1)
        try:
            if utilized.notUtilized.index(i) is not -1:
                for k in range(len(demandManager.currentDemands)):
                    coef.append(demandManager.currentDemands[k].demand * -1)
                    cvar = "y" + str(varMul)
                    network.demandeq[i].append(cvar)
                    varMul += 1
        except ValueError:
            pass
        print network.demandeq[i]
        addConstraint(model, network.demandeq[i], coef,
                      "demand{0}".format(i+1), PathDemands[i], "E")
        
        #Clean up equation
        try:
            if utilized.notUtilized.index(i) is not -1:
                for k in range(len(demandManager.currentDemands)): 
                    network.demandeq[i].pop()
        except ValueError:
            pass

        coef = []
###############################################################################

###############################################################################
#Function: selectionEquations
#Pre:
#Post:
###############################################################################
def selectionEquations(model, demandManager, utilized):
    coef = []
    equation = []
    for i in range(len(demandManager.currentDemands)):
        for j in range(len(utilized.notUtilized)):
            coef.append(1)
            equation.append("y" + str(len(demandManager.currentDemands) * j + i +  1))
        print coef
        print equation
        addConstraint(model, equation, coef,
                      "seleq{0}".format(i+1), 1, "E")

        coef = []
        equation = []

###############################################################################

