def printResults(network, solutions, fout):
    vars = ""
    nums = ""
    printNums = ""
    varsList = []
    numsList = []
    for i in range(len(network.equation)):
        nums = nums + "%0.2f" %solutions[i] + "\t"
        vars = vars + network.equation[i] +"\t"
        numsList.append("%0.2f" %solutions[i])
        varsList.append(network.equation[i])
        printNums = printNums + "%0.2f" %solutions[i] + ", "
    print vars
    print nums
    fout.write(vars + "\n")
    fout.write(nums + "\n")
    results = [varsList, numsList]
    return results

def printBreak(fout):
    print "###########################################################################"
    fout.write("##############################################################"+ "\n")
