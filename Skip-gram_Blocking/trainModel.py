#2) train neural network
#3) output vectorized systems and connection types

#Skip-gram model

#read words table csv
#initialise embeddings matrix



import csv
import pandas as pd
import numpy as np
import random as rnd

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

print("Reading data...")
#reading in wordsTable to 2d list (not dataframe because varying number of columns per row)
with open("words_table.csv", newline='') as file:
    r = csv.reader(file)
    wordsTable = list(r)

wordsTable = [list(map(int, i)) for i in wordsTable]

#reading connectionTypes into dataframe
connectionTypes = pd.read_csv("connection_types.csv")

uniqueSystems = len(wordsTable)
uniqueConnectionTypes = len(connectionTypes.index)

#making "sentence" for 1 hot encoding reference
sentence = [row[0] for row in wordsTable]
sentence = sentence + connectionTypes["connectionType"].to_list()



print("\nInitialising matrices:")

#making one hot encoding
print("one hot encoding matrix...")
oneHot = np.zeros((len(sentence), len(sentence)), int)
np.fill_diagonal(oneHot, 1)

#making embedding matrix - dimensions: (addresses + connection types) * connection types
print("embedding matrix...")
embeddings = np.zeros((uniqueSystems, uniqueSystems + uniqueConnectionTypes))
for i in range(uniqueSystems):
    for j in range(uniqueSystems + uniqueConnectionTypes):
        embeddings[i][j] = rnd.uniform(-1,1)






print("Training...")
#generating training data
batchSize = 10                  #arbitrarily chosen for now
numSkips = 2                    #arbitrarily chosen for now
batchStart = 0

#initialise empty trainingBatch
trainingBatch = np.zeros((batchSize, numSkips+1), int)

for index in range(batchSize):
    if(rnd.random() < 0.2):
        #sets a random valid connection type as the target word
        trainingBatch[index][0] = wordsTable[index+batchStart][rnd.randint(1, len(wordsTable[index+batchStart]) - 1)]

    else:
        #sets the system IP address as the target word
        trainingBatch[index][0] = wordsTable[index+batchStart][0]
    
    #randomly selects the context words (from the connection types) for the selected target word
    for c in range(numSkips):
        trainingBatch[index][c + 1] = wordsTable[index+batchStart][rnd.randint(1, len(wordsTable[index+batchStart]) - 1)]
batchStart = batchStart + batchSize

print(trainingBatch)



#TODO:
#initialise bias and weights matrix
#   biases set to 0
#   weights initialised with values taken from normal distribution

