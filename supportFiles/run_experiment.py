import time
import os

PATH = "/home/mattowens/Documents/gitRepos/NetworkSimulation/"
inputFiles =  PATH + "inputFiles/"

folder = "experiment" + str(time.strftime("%m%d%Y")) + "/"



for i in range(10):
  path = inputFiles + folder + str(i) + "/"
  for j in range(5):
    curr_path = path + str(j) + "/"
    for random in range(2):
      for over in range(2):
        for dcap in range(50, 205, 5):
          if over == 1:

            file_name = (   curr_path +
                            "config_file-" +
                            str(random) + "-" +
                            str(over) + "-" +
                            str(dcap) + "-" +
                            str(10) +
                            ".txt")
            print file_name
            os.system("python main.py " + file_name)
          else:
            file_name = (   curr_path +
                            "config_file-" +
                            str(random) + "-" +
                            str(over) + "-" +
                            str(dcap) + "-" +
                            str(0) +
                            ".txt")
            print file_name
            os.system("python " + PATH + "main.py " + file_name)

