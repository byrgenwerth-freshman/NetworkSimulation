def getFiles(introMessage):
    control = True
    while control is True:
        value = raw_input(introMessage)
        try:
            fin = open(value, "r")
            control = False
        except IOError:
            print "That is not a valid file."
            control = True
    return fin

def get1or0(introMessage):
    control = True
    while control is True:
        print "Please enter a 1 or a 0."
        value = input(introMessage)
        try:
            value = int(input(introMessage))
            if value is 1 or value is 0:
                control = False
            else:
                print "That is not a valid input. Try again"
        except NameError:
            print "That is not a valid input. Try again"
    return value

def getInt(introMessage):
    control = True
    while control is True:
        print "Please enter an integer."
        try:
            value = int(input(introMessage))
            
            control = False
        except NameError:
            print "That is not a valid integer. Please try again."

def wrongInputErrorMessage():
    print "This program requires no arguments or three argument."
    print "The first is the demand file."
    print "The second is the output file."
    print "The third is path info."
    print "The fourth is the virtual network file."
    print "The fifth is 0 for not dynamic, 1 for dynamic."
    print "The sixth is 0 for no overbooking, 1 for overbooking."
    print "The seventh is for how much the capacity is."
    print "The eight is for the value of overbooking(This is required)"
