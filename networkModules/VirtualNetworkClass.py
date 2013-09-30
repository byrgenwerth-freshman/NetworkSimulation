class VirtualNetwork:
    original_paths = []
    added_paths = []

    def __init__(self, paths):
        self.original_paths = paths
        self.added_paths = []

    def addPath(self, path):
        self.added_paths.append(path)

    def __str__(self):
        return str(self.original_paths) + " " + str(self.added_paths)
