class Demand:
    virtualNetworkId = None
    demandPathId = None
    demand = None
    duration = None
    startTime = None


    def __init__(self, virtualNetworkId, demandPathId, demand, duration,
                 startTime):
        self.virtualNetworkId = virtualNetworkId
        self.demandPathId = demandPathId
        self.demand = demand
        self.duration = duration
        self.startTime = startTime

    def decrementDur(self, amount):
        self.duration = int(self.duration - amount)

    def __str__(self):
        return ("VNID: " + str(self.virtualNetworkId) + " |DPathID: " +
                str(self.demandPathId) + " |Demand: " + str(self.demand) +
                " |Duration: " + str(self.duration) + " |Start Time: " +
                str(self.startTime))
