import sys
import os
import re
#This will generate a csv
expirment_name = sys.argv[1]

print expirment_name

PATH = "/home/mattowens/Documents/gitRepos/NetworkSimulation/OUTPUT/"

output_path = PATH + expirment_name

if os.path.isdir(output_path):
  print "here"
  for demand_file in range(10):
    print "Demand File " + str(demand_file)
    for run in range(5):
      print "Run " + str(run)
      current_path = (output_path + "/" + str(demand_file) + "/"  +
                      str(run) + "/")
      print current_path
      for dynamic in range(2):
        for overbooking in range(2):
          for capacity in range(50, 205, 5):
            if overbooking == 1:
              f_name = ("output" + str(dynamic) + "-" + str(overbooking)
                        + "-" + str(capacity) + "-" + "10.txt")
              print current_path + f_name
              # fin = open(current_path + f_name, 'r')
              # print fin.readline()
            else:
              f_name = ("output" + str(dynamic) + "-" + str(overbooking)
                        + "-" + str(capacity) + "-" + "0.txt")
              print current_path + f_name
              fin = open(current_path + f_name, 'r')
              print fin.readline()


else:
  print "Not a directory"