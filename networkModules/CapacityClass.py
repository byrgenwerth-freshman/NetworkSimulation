class Capacity:
    link = ""
    capacity = None
    list_of_paths = []

    def __init__(self, link, capacity, list_of_paths):
        self.link = link
        self.capacity = capacity
        self.list_of_paths = list_of_paths


    def __str__(self):
        total = ""
        total += "The Link: " + str(self.link) + "\n"
        total += "The Capacity: " + str(self.capacity) + "\n"
        total += "List of Paths: " + str(self.list_of_paths) + "\n\n"
        return total


