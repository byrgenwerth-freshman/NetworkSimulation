def createRemoveList(linkReList):
    removeList = []
    for i in range(len(linkReList)):
        if len(linkReList[i]) > 3:
            if linkReList[i][3] <= 0:
                removeList.append(linkReList[i])
    return removeList

def createDemandRemoveList(currentDemands):
    removeList = []
    for i in range(len(currentDemands)):
        if currentDemands[i][3] <= 0:
            removeList.append(currentDemands[i])
    return removeList
