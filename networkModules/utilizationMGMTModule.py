import sets

class UtilizationSet:

    #Three values
    not_utilized = []
    part_utilized = []
    full_utilized = []

    def __init__(self, realNetwork, virtualNetworks):
        #self.not_utilized = realNetwork.group_path_names
        for vn in virtualNetworks.vn_container:
            self.part_utilized = list(set(self.part_utilized) | set(vn.original_paths))
        self.not_utilized = list(set(realNetwork.group_path_names) - set(self.part_utilized))


    def __str__(self):
        return ("Not Utilized:\n" + str(self.not_utilized) + "\n" +
                "Part Utilized\n" + str(self.part_utilized) + "\n" +
                "Full Utilized\n" + str(self.full_utilized))



