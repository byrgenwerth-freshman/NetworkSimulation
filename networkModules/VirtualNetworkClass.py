class VirtualNetwork:
    originalPaths = []
    addedPaths = []

    def __init__(self, paths):
        self.originalPaths = paths
        self.addedPaths = []
	
    def __str__(self):
        return str(self.originalPaths) + "" + str(self.addedPaths)
