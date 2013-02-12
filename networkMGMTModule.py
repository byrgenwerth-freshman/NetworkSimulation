############################################################################## 
#networkMGMTModule.py by Matt Owens
#Updated: 1/9/2013
#This is a file that contains the code for my function that takes a graph and
#converts it into a different list that can be used by cplex. I've broken the 
#function in to other functions to make the code easier to read.
###############################################################################
import re

class Network:
###############################################################################
#This function takes the output file of Ian Ramsey's shortest path program
#and the graph file used in that program and makes them so that cplex
#can use that information.
#This is for min cost
###############################################################################
	coef = []
	equation = []
	demandeq = []
	capacity = []
	def __init__(self, outputfile, graphfile):
		#This function takes the output file and puts the three outputs
		#of the variables names, the minimization equations, and the
		#demand equations
		both = self.getbteq(outputfile)
		#This is the list with both variablies, compact and explicit
		btvar = both[0]
		#This is the the minimization equation
		self.equation = both[1]
		#This is the demand equations
		self.demandeq = both[2]

		#This function gets the capacity equations
		self.capacity = self.getCapacityEq(graphfile, btvar)

		#This functions gets the demand equations
		self.coef = self.getCoefEq(self.equation, self.capacity)
###############################################################################

###############################################################################
#This function takes the output file of Ian Ramsey's shortest path program 
#and the graph file used in that program and makes them so that cplex
#can use that information.
#This is for load balancing
###############################################################################
#Updated on 2/12/2013
#This function needs to be fixed
	def convertToLB(self):
		networkLB = Network
		networkLB.equation = self.equation
		for i in range(len(networkLB.equation)):
			networkLB.coef.append(0)
		networkLB.coef.append(1)
		networkLB.equation.append("Z")
		networkLB.demandeq = self.demandeq
		networkLB.capacity = self.capacity
		for equations in networkLB.demandeq:
			equations.append("Z")


		return networkLB
###############################################################################

############################################################################## 
#This function takes the makes the variable name, the minimization function,
# and the demand equations.
###############################################################################
	def getbteq(self, outputfile):
		file = open(outputfile,"r")
		equation = []
		demandeq = [[]]
		bteq = [[]]
		i = 1

		for line in file.readlines():
			if line[0] != "#":
				#Breaks the sections up to parts
				first = line.find("|")
				part1 = line[:first]
				second = line.find("|",first + 1)
				part2 = line[first+2:second]
				part3 = line[second + 2:]
				#Gets the first and last element
				getbeg_end = re.compile("\d*\s\d*")
				results = getbeg_end.match(part1)
				begend = results.group()
				#Creating minimizing function
				#Initial run though
				if i is 1:
					check = begend
					smdest = 1
					p = 1
					var = "x{0}_{1}".format(smdest, p)
					equation.append(var)
					demandeq[smdest - 1].append(var)
					bteq[i - 1].append(var)
				#The rest of the run through
				else:
					#If it is in the same
					if check == begend:
						p = p + 1
						var = "x{0}_{1}".format(smdest,
									p)
						equation.append(var)
						demandeq[smdest - 1].append(var
									    )
						bteq[i - 1].append(var)
					else:
						smdest = smdest + 1
						p = 1
						var = "x{0}_{1}".format(smdest,
									p)
						equation.append(var)
						demandeq.append([])
						demandeq[smdest - 1].append(var
									    )
						bteq[i - 1].append(var)
						check = begend
				#Get path
				get_allnumbers = re.compile("(\d+\s)+")
				results = get_allnumbers.match(part2)
				path =  results.group()
				ex = "x " + path
				bteq[i - 1].append(ex)
				bteq.append([])
				i = i + 1
		file.close()
		bteq.remove([])
		both = [bteq, equation, demandeq]
		return both
###############################################################################

###############################################################################
#This function takes the graph file and the and the explicit variable names and
#creates the capacity equations.
#This is returned in a list [(capacity equation name)[(varibles)]
###############################################################################
	def getCapacityEq(self, graphfile,bteq):
		file = open(graphfile,"r")
		all_links = file.readlines()
		#List for the capacity links    
		capacity = [[]]
		#Variable to check if the
		inthere = -1
		#Varialble for number of equations in the list
		numcapeq = 0
		#Create capacity equations
		for i in range(len(bteq)):
			links = bteq[i][1][2:]
			get_link = re.compile("\d+")
			#Seperating out the
			results = get_link.findall(links)
			#Get each path
			for j in range(len(results) - 1):
				var = results[j]
				var1 = results[j+1]
				if int(var) > int(var1):
					swap = var
					var = var1
					var1 = swap
				totvar = var + "-" + var1
				inthere = -1
				#See if the link is in the list 
				for k in range(len(capacity) - 1):
					if (capacity[k][0].find(totvar)
					    is not -1):
						inthere = k
				#If the in the list
				if inthere is not -1:
					capacity[inthere][1].append(bteq[i][0])
				#If it is not in the list
				else:
					capacity[numcapeq].append([])
					#Putting the link name for the list
					capacity[numcapeq][0] = totvar
					capacity[numcapeq].append([])
					capacity[numcapeq][1] = []
					#Putting the variavle in the list    
					capacity[numcapeq][1].append(bteq[i][0]
								     )
					numcapeq = numcapeq + 1
					capacity.append([])
		capacity.remove([])
		file.close()
		return capacity
###############################################################################

###############################################################################
#This returns the coefficients of the minimization equations
###############################################################################
	def getCoefEq(self, equation, capacity):
		coef = []
		for i in range(len(equation)):
			coef.append(0)
		for i in range(len(capacity)):
			for j in range(len(capacity[i][1])):
				for k in range(len(equation)):
					if (equation[k].find(capacity[i][1][j])
					    is not -1):
						theco = k
				coef[theco] = coef[theco] + 1
		return coef
###############################################################################
#Print Network file 
#This needs to be fixed 2/12/2013
	def printNetwork(self):
	    for i in range(len(network)):
		if i is 0:
		    print "Coefficient and Variable"
		    for k in range(len(network[i])):
			print str(network[i][k]) + " " + str(network[i + 1][k])
		elif i is 2:
		    print "Groups of Paths"
		    for k in range(len(network[i])):
			print network[i][k]
		elif i is 3:
		    print "Link with Associated Paths"
		    for k in range(len(network[i])):
			paths = ""
			for nums in network[i][k][1]:
			    paths = paths + str(nums) + ", "
			print "Link " + str(network[i][k][0]) + ": " + paths
