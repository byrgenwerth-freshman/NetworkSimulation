class Demand:
    virtualNetworkId = None
    demandPathId = None
    demand = None
    duration = None
    startTime = None
    #alpha is a discount value for delayed demands
    alpha = None
    #delayed variable counts number of time periods a demand is delayed
    delayed = 0

    def __init__(self, virtualNetworkId, demandPathId, demand, duration,
                 startTime):
        self.virtualNetworkId = virtualNetworkId
        self.demandPathId = demandPathId
        self.demand = demand
        self.duration = duration
        self.startTime = startTime
	#self.alpha = alpha

    def decrementDur(self, amount):
        self.duration = int(self.duration - amount)

    def discountDemand(self):
	#discounts demand when demand is delayed 1 time period
	self.demand = int(self.demand - self.alpha)
	#increment delayed variable to signify additional time delay
	self.delayed = int(self.delayed + 1)

    def __str__(self):
        return ("VNID: " + str(self.virtualNetworkId) + " |DPathID: " +
                str(self.demandPathId) + " |Demand: " + str(self.demand) +
                " |Duration: " + str(self.duration) + " |Start Time: " +
                str(self.startTime) + "|Alpha: " + str(self.alpha) +
		str(self.alpha) + " |Delayed: " + str(self.delayed))
