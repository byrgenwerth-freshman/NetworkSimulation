#Put new method code in here
import cplex

#Constructor
def createSelectCPLEXmodel(network, PathDemands, capacityTable, demandManager,
                            utilized):
    model = cplex.Cplex()
    network = convertToSelect(model, network, demandManager)
    #Need to update the equation to include the needed variables
    #Create 
    model.objective.set_sense(1)
    model.variables.add(names = network.equation, obj = network.coef)
    coef = []
    cplexDemandSel(model, network, coef, PathDemands)
    coef = []
    cplexCapacity(model, network, coef, capacityTable)
    return model

def convertToSelect(model, network, demandManager):
    #Create additional variables and set coeficient to 0
    print demandManager.currentDemands
    #for all the demand not met
        #create a variable y

    #Set all variables as binary
    #for all the new variables
    model.variables.set_types("variable", model.variables.type.binary)

def cplexDemandSel(model, network, coef, PathDemands, demandManager, utilized):
    #Add the demands to the open groups of paths
    pass

def cplexCapacity(model, network, coef, capacityTable):
    for i in range(len(network.capacity)):
        for j in range(len(network.capacity[i][1])):
            coef.append(1.0)
        addConstraint(model, network.capacity[i][1], coef,
                      "link{0}".format(network.capacity[i][0]), 0, "L")
        #Making the coeficient list empty for the next Equation                                                                                                                                                  
        coef = []

