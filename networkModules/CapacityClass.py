class Capacity:
    link = ""
    capacity = None
    list_of_paths = []

    def __init__(self, link, capacity, list_of_paths):
        self.link = link
        self.capacity = capacity
        self.list_of_paths = list_of_paths


    def printCap(self):
        print self
        print "The Link: " + str(self.link)
        print "The Capacity: " + str(self.capacity)
        print "List of Paths: " + str(self.list_of_paths)


