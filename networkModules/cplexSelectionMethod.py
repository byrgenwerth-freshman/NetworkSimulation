#Put new method code in here
import cplex

#Constructor
def createSelectCPLEXmodel(network, PathDemands, capacityTable):
    model = cplex.Cplex()
    model.objective.set_sense(1)
    model.variables.add(names = network.equation, obj = network.coef)
    coef = []
    cplexDemandSel(model, network, coef, PathDemands)
    coef = []
    cplexCapacity(model, network, coef, capacityTable)
    return model


def cplexDemandSel()

def cplexCapacity(model, network, coef, capacityTable):
    for i in range(len(network.capacity)):
        for j in range(len(network.capacity[i][1])):
            print network.capacity[i][1][j]
            if network.capacity[i][1][j] == "Z":
                coef.append(- 1 * capacityTable.capacityTable[i].capacity)
            else:
                coef.append(1.0)
        addConstraint(model, network.capacity[i][1], coef,
                      "link{0}".format(network.capacity[i][0]), 0, "L")
        #Making the coeficient list empty for the next Equation                                                                                                                                                  
        coef = []

