class Demand:
    virtual_network_id = None
    demand_path_id = None
    demand = None
    original_demand = None
    duration = None
    startTime = None
    #alpha is a discount value for delayed demands
    alpha = None
    #delayed variable counts number of time periods a demand is delayed
    delayed = 0

    def __init__(self, virtual_network_id, demand_path_id, demand, duration,
                 startTime):
        self.virtual_network_id = virtual_network_id
        self.demand_path_id = demand_path_id
        self.demand = demand
        self.original_demand = demand
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
        return ("VNID: " + str(self.virtual_network_id) + "| DPathID: " +
                str(self.demand_path_id) + "| Demand: " + str(self.demand) +
                "| Original Demand: " + str(self.original_demand) +
                "| Duration: " + str(self.duration) + "| Start Time: " +
                str(self.startTime) + "| Delayed: " + str(self.delayed))
