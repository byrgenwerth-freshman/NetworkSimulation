def decrementLinkReList(linkReList):
    for i in range(len(linkReList)):
    #Decrease the duration of capacity changes.                             
        if len(linkReList[i]) > 3:
            linkReList[i][3] = linkReList[i][3] - 1
    return linkReList

def removeExpiredLinkReList(linkReList, removeList):
    for i in range(len(removeList)):
        linkReList.remove(removeList[i])
    
    return linkReList
