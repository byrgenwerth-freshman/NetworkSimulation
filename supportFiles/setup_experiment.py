import time
import os


#Make folders
PATH = "/home/mattowens/Documents/gitRepos/NetworkSimulation/"
outputFiles = PATH + "OUTPUT/"
inputFiles =  PATH + "inputFiles/"
lpFiles = PATH + "LP/"


folder = "experiment" + str(time.strftime("%m%d%Y")) + "/"
os.system("mkdir " + inputFiles + folder)
os.system("mkdir " + outputFiles + folder)
os.system("mkdir " + lpFiles + folder)


for i in range(10):
  # Make Path
  path = inputFiles + folder + str(i) + "/"
  outputPath = outputFiles + folder + str(i) + "/"
  lpPath = lpFiles + folder + str(i) + "/"

  os.system("mkdir " + path)
  os.system("mkdir " + outputPath)
  os.system("mkdir " + lpPath)


  # Generate Demand
  command = "python " + PATH + "supportFiles/demandVer1Network.py 5 0 100 64 30 25 4 "
  print command
  os.system(command)


  for j in range(5):
    print "\n\n"
    curr_path = path + str(j) + "/"
    curr_output_path = outputPath + str(j) + "/"
    curr_lp_path = lpPath + str(j) + "/"
    os.system("mkdir " + curr_path)
    os.system("mkdir " + curr_output_path)
    os.system("mkdir " + curr_lp_path)

    #Copy files
    os.system("cp " + inputFiles + "OriginalInput/IanProg"  + " " + curr_path)
    os.system("cp " + inputFiles + "OriginalInput/SampleFatTreeTopology.txt"  + " " + curr_path)
    os.system("cp " + inputFiles + "OriginalInput/pathsInfoFinal.txt"  + " " + curr_path)
    os.system("cp " + inputFiles + "OriginalInput/kshortestpaths.txt"  + " " + curr_path)
    os.system("cp " + PATH + "supportFiles/DemandFile.txt"  + " " + curr_path)
    os.system("cp " + PATH + "supportFiles/virtualNetworks.txt"  + " " + curr_path)

    #Write files
    for random in range(2):
      for over in range(2):
        for dcap in range(50, 205, 5):
          # Generate Filed
          if over == 1:
            file_name = ( curr_path +
                          "config_file-" +
                          str(random) + "-" +
                          str(over) + "-" +
                          str(dcap) + "-" +
                          str(10) +
                          ".txt")
            fout = open(file_name, 'w')
            demand_text = (curr_path + " IanProg DemandFile.txt " + folder +
                            str(i) + "/" + str(j) + "/output " +
                            "pathsInfoFinal.txt virtualNetworks.txt " +
                            str(random) + " " +
                            str(over) + " " +
                            str(dcap) + " " +
                            str(10))
            fout.write(demand_text)
            fout.close()
          else:
            file_name = ( curr_path +
                          "config_file-" +
                          str(random) + "-" +
                          str(over) + "-" +
                          str(dcap) + "-" +
                          str(0) +
                          ".txt")
            fout = open(file_name, 'w')
            demand_text = (curr_path + " IanProg DemandFile.txt " + folder +
                            str(i) + "/" + str(j) + "/output " +
                            "pathsInfoFinal.txt virtualNetworks.txt " +
                            str(random) + " " +
                            str(over) + " " +
                            str(dcap) + " " +
                            str(0))
            fout.write(demand_text)
            fout.close()


#Clean Up
os.system("rm " + PATH + "supportFiles/DemandFile.txt")
os.system("rm " + PATH + "supportFiles/virtualNetworks.txt")


