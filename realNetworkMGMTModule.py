#This is a place holder
class realNetwork:
    
    #Group of paths name
    gPathName = []

    def __init__(self, lines):
        networkPaths = int(lines.strip())
        for i in range(networkPaths):
            self.gPathName.append(i)
