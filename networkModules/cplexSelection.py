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
                            utilized, virtualNetworks):
    #Creating the model
    model = cplex.Cplex()
    #Setting equation as minimization
    model.objective.set_sense(1)
    #Adding the additional variables to the selection model.
    convertToSelect(model, network, demandManager, utilized)
    #Making those variables binary balues
    addBinary(model, network)
    setupvn(model, virtualNetworks)
    setUpVNPath(model, network)

    #Creating the demands
    cplexDemandSel(model, network, PathDemands, demandManager, utilized)
    #Adding the capacity
    cplexCapacitySel(model, network, capacityTable)
    #selectionEquations(model, demandManager, utilized)

    return model
###############################################################################

###############################################################################
#Function: convertToSelect
#Pre:
#Post:
###############################################################################
def convertToSelect(model, network, demandManager, utilized):
    #New pseudo code
    #Create z's
    coef =[]
    equation = []
    for link in network.capacity:
        var = "z" + str(link[0]) 
        print var
        coef.append(1)
        equation.append(var)
    for vars in network.equation:
        equation.append(vars)
        coef.append(0)
    #The 2 is a temp fix
    for i in range(len(network.equation)/2):
        coef.append(0)
        equation.append("y" + str(i + 1))
    print coef
    print equation
    model.variables.add(names = equation, obj = coef)
    #Clean up equation
    #The 2 is a temp fix
    for i in range(len(network.equation)/2):
        coef.pop()
        equation.pop()
    for i in range(len(network.equation)):
        coef.pop()
        equation.pop()
    print coef
    print equation
###############################################################################


###############################################################################
#Function: addBinary
#Pre:
#Post:
###############################################################################
def addBinary(model, network):
    print network.equation
    for i in range(len(network.equation)):
        vars = network.equation[i]
        if ((i + 1) % 2) is 0:
            otherVar = "y" + str((i/2) + 1)
            model.variables.set_types(otherVar, model.variables.type.binary)
        model.variables.set_types(vars, model.variables.type.binary)
###############################################################################

###############################################################################
#Function: Set Up VN
#Pre:
#Post:
###############################################################################
def setupvn(model, virtualNetworks):
    for i in range(len(virtualNetworks.vnContainer)):
        print virtualNetworks.vnContainer[i].originalPaths
        coef = []
        equation = []
        for path in virtualNetworks.vnContainer[i].originalPaths:
            coef.append(1)
            equation.append("y" + str(path))
        print equation
        addConstraint(model, equation, coef, "vn{0}".format(i+1), 1, "E")
###############################################################################

###############################################################################
#Function: Set Up VN Path Constraints
#Pre:
#Post:
###############################################################################
def setUpVNPath(model, network):
    equation = []
    coef = []
    for i in range(len(network.equation)):
        print network.equation[i]
        coef.append(1)
        equation.append(network.equation[i])
        if ((i + 1) % 2) is 0:
            coef.append(-1)
            equation.append("y" + str((i/2) + 1))
            addConstraint(model, equation, coef, "VNPath{0}".format((i+1)/2), 0, 
                            "E")
            print coef
            print equation
            coef = []
            equation = []

###############################################################################

###############################################################################
#Function: cplexDemandSel
#Pre:
#Post:
###############################################################################
def cplexDemandSel(model, network, PathDemands, demandManager, utilized):
    tmp_id = []
    tmp_demand = []
    for i in range(len(demandManager.currentDemands)):
        print demandManager.currentDemands[i]
        tmp_id.append(demandManager.currentDemands[i].demandPathId)
        tmp_demand.append(demandManager.currentDemands[i].demand)
    id = []
    demand = []
    for i in range(len(tmp_id)):
        for j in range(2):
            id.append("x" + str(tmp_id[i]) + "_" + str(j + 1))
            demand.append(tmp_id[i])


    for i in range(len(network.capacity)):
        print network.capacity[i][1]
        coef = []
        equation = []
        for j in range(len(network.capacity[i][1])):
            equation.append(network.capacity[i][1][j])
            try:
                value = id.index(network.capacity[i][1][j])
                coef.append(demand[value])
            except ValueError:
                coef.append(0)
        coef.append(-1)
        equation.append("z" + str(network.capacity[i][0]))
        addConstraint(model, equation, coef,
                      "demand{0}".format(i+1), 0, "E")      
###############################################################################

###############################################################################
#Function: cplexDemandSel
#Pre:
#Post:
###############################################################################
def cplexCapacitySel(model, network, capacityTable):
    print network.capacity
    for i in range(len(capacityTable.capacityTable)):
        coef = []
        equation = []
        capacity = []
        coef.append(1)
        equation.append("z" + str(capacityTable.capacityTable[i].link))
        addConstraint(model, equation, coef, "capacity{0}".format(i+1),
                        capacityTable.capacityTable[i].capacity, "L")
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
            equation.append("y" + str(len(demandManager.currentDemands) 
                            * j + i +  1))
        print coef
        print equation
        addConstraint(model, equation, coef,
                      "seleq{0}".format(i+1), 1, "L")

        coef = []
        equation = []

###############################################################################

