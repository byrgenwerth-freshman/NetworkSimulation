import sets

class utilizationSet:

    #Three values
    notUtilized = []
    partUtilized = []
    fullUtilized = []

    def __init__(self, realNetwork, virtualNetworks):
        self.notUtilized = realNetwork
        for sets in virtualNetworks.vnContainer:
            self.notUtilized = list(set(sets.originalPaths) ^ set(self.notUtilized))
        self.partUtilized = list(set(self.notUtilized) ^ set(realNetwork))

    def __str__(self):
        return ("Not Utilized:\n" + str(self.notUtilized) + "\n" +
                "Part Utilized\n" + str(self.partUtilized) + "\n" +
                "Full Utilized\n" + str(self.fullUtilized)) 
        
        
 
