#This is a place holder
class RealNetwork:

    #Group of paths name
    group_path_names = []

    def __init__(self, paths):
        network_paths = paths
        self.group_path_names = []

        for i in range(network_paths):
            self.group_path_names.append(i + 1)
