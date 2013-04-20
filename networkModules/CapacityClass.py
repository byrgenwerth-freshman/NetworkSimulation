class Capacity:
    link = ""
    capacity = None
    listOfPaths = []

    def __init__(self, link, capacity, listOfPaths):
        self.link = link
        self.capacity = capacity
        self.listOfPaths = listOfPaths
    

    def printCap(self):
        print self
        print "The Link: " + str(self.link)
        print "The Capacity: " + str(self.capacity)
        print "List of Paths: " + str(self.listOfPaths)


