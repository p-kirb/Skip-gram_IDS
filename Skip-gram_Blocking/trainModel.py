#2) train neural network
#3) output vectorized systems and connection types

#Skip-gram model

#read words table csv
#embedding matrix needs to be randomly initialised with values between 0 and 1 from a normal distribution.


#WHAT I WAS DOING:
#wordsTable is read as strings so need to convert it to ints for NN input
#need ot figure out what to do with IPv6 addresses? maybe still just convert to ints?


import csv

##########
#FUNCTIONS
##########

def ip2int(numip):
    if(":" in numip):                   #currently just sets any IPv6 addresses to 0
        return 0
    binIP = ""
    for x in numip.split('.'):
        x = bin(int(x)+256)[3:]         #adds 256 to number (to make them all 9 bits) then removes unnecessary first 3 characters ("0b1")
        binIP+=x
    return int(binIP, 2)


#############
#PROGRAM CODE
#############


with open("words_table.csv", newline='') as file:
    r = csv.reader(file)
    wordsTable = list(r)

wordsTable = [list(map(int, i)) for i in wordsTable]

print(wordsTable[:1])

#initialise embedding matrix - dimensions: number of addresses * number of connection types?
#   numbers between -1 and 1 taken from uniform distribution

#initialise bias and weights matrix
#   biases set to 0
#   weights initialised with values taken from normal distribution

#also need one hot encoding of words? maybe do this step in the buildWordsTable script