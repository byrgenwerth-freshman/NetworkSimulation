import cplex

def setStream(model, name_for_logs):
    model.set_log_stream(name_for_logs + ".log")
    model.set_error_stream(name_for_logs + ".err")
    model.set_results_stream(name_for_logs + ".res")

def addConstraint(model, varList, coefList, constrName, trhs, operator):
    eq = cplex.SparsePair(ind = varList, val = coefList)
    model.linear_constraints.add(names = [constrName], lin_expr = [eq],
                                 rhs = [trhs], senses = [operator])
    
def cplexDemand(model, network, coef, PathDemands):
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
            coef.append(1.0)
        addConstraint(model, network.capacity[i][1], coef,
                      "link{0}".format(network.capacity[i][0]),
                      capacityTable.capacityTable[i].capacity, "L")
        #Making the coeficient list empty for the next Equation                
        coef = []


#Rename so it reflects this relates to minimization.
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
    coef = []
    cplexCapacity(model, network, coef, capacityTable)
    return model

#Create cplex model for new format

#Create cplex model for load balancing

def addUpDemands(currentDemands, Paths):
    PathDemands = []
    demand = 0
    for i in range(len(Paths)):
        for j in range(len(currentDemands)):
            if currentDemands[j].demandPathId == i:
                demand = demand + currentDemands[j].demand
        PathDemands.append(demand)
        demand = 0
    return PathDemands
