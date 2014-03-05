for i in range(10):
    for random in range(2):
        for over in range(2):
            for dcap in range(50, 205, 5):
                if random == 1:
                    for time in range(10):
                        print ("/home/mattowens/Documents/"
                               +"gitRepos/NetworkSimulation/"
                               + "inputFiles/experiment20140304/"
                               + str(i) + " IanProg DemandFile.txt output"
                               + str(time)
                               + str(random)
                               + str(over) + str(dcap) 
                               + "10 pathsInfoFinal.txt "
                               + "virtualNetworks.txt "
                               + str(random) + " "
                               + str(over) + " " + str(dcap) + " 10")
                else:
                    print ("/home/mattowens/Documents/"
                           +"gitRepos/NetworkSimulation/"
                           + "inputFiles/experiment20140304/"
                           + str(i) + " IanProg DemandFile.txt output" 
                           + str(random) 
                           + str(over) + str(dcap) + "10 pathsInfoFinal.txt " 
                           + "virtualNetworks.txt "
                           + str(random) + " "
                           + str(over) + " " + str(dcap) + " 10")
