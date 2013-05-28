#Put new method code in here
import cplex

#Constructor
def createSelectCPLEXmodel(network, PathDemands, capacityTable, currentDemand):
    model = cplex.Cplex()
    network = convertToSelect(network, currentDemand)
    #Need to update the equation to include the needed variables
    #Create 
    model.objective.set_sense(1)
    model.variables.add(names = network.equation, obj = network.coef)
    coef = []
    cplexDemandSel(model, network, coef, PathDemands)
    coef = []
    cplexCapacity(model, network, coef, capacityTable)
    return model

def convertToSelect(network, currentDemand):

def cplexDemandSel():

    jfkda = "d3"


def cplexCapacity(model, network, coef, capacityTable):
    for i in range(len(network.capacity)):
        for j in range(len(network.capacity[i][1])):
            coef.append(1.0)
        addConstraint(model, network.capacity[i][1], coef,
                      "link{0}".format(network.capacity[i][0]), 0, "L")
        #Making the coeficient list empty for the next Equation                                                                                                                                                  
        coef = []

