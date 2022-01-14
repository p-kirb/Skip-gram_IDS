#2) train neural network
#3) output vectorized systems and connection types

#Skip-gram model

#read words table csv
#initialise embeddings matrix



import csv
import pandas as pd
import numpy as np
import random as rnd

#tensorflow 2.6.0
import tensorflow as tf
from tensorflow import keras

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

def makeOneHot(index, sentenceLength):
    vec = np.zeros(sentenceLength, int)
    vec[index] = 1
    return vec.tolist()


#############
#PROGRAM CODE
#############

batchSize = 8                   #optimum from paper
numSkips = 2                    #optimum from paper
embeddingSize = 4

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
sentenceLength = len(sentence)



print("\nInitialising matrices:")

#making embedding matrix - dimensions: sentence length * embeddingSize
#each row is the corresponding system/connectionType vector
print("embedding matrix...")
embeddings = np.zeros((len(sentence), embeddingSize))
for i in range(len(sentence)):
    for j in range(4):
        embeddings[i][j] = rnd.uniform(-1,1)






print("training matrix...")
#generating training data

trainingTargets = []                        #will be a 2d array (each target word by its one hot vector)
trainingContexts = []                       #will be a 3d array (each target word by the numskips by the one hot vectors)
for i in range(uniqueSystems):              #for every unique system...
    for c in range(numSkips):
        if(rnd.random() < 0.2):
            #add one hot encoding of random connection type from this row
            connType1 = rnd.randint(1, len(wordsTable[i]) - 1)
            trainingTargets.append(makeOneHot(i+connType1, sentenceLength))
        else:
            #add one hot encoding of that system (hot index is just the current i value)
            trainingTargets.append(makeOneHot(i, sentenceLength))
        
        #adding the context word (randomly chosen from current rows avaiable connection types)
        connType2 = rnd.randint(1, len(wordsTable[i]) - 1)
        trainingContexts.append(makeOneHot(i+connType2, sentenceLength))

#trainingDataset = tf.data.Dataset.from_tensor_slices((trainingTargets, trainingContexts)).batch(batchSize)
trainingTargets = np.array(trainingTargets)
trainingContexts = np.array(trainingContexts)
print("made dataset")
        



print("\nTraining model...")

model = keras.Sequential([
    keras.layers.Input(shape=(len(sentence),), batch_size=batchSize, sparse=True),          #input layer (arguments may need changing)
    keras.layers.Dense(units=embeddingSize),                                                #hidden layer (arguments may need changing)
    keras.layers.Dense(units=len(sentence), activation="softmax")                           #softmax output layer (arguments may need changing)
])

#loss is categorical cross entropy so provide training labels as one hot vectors
model.compile(optimizer='Adagrad', loss=tf.keras.losses.CategoricalCrossentropy(), metrics=['categorical_accuracy'])

data = model.fit(x=trainingTargets, y=trainingContexts, batch_size = batchSize, epochs = 10)

print(data)

#TODO:
#set the pre-initialised embedding matrix to the weights of layer 1
#initialise bias and weights matrix
#   biases set to 0
#   weights initialised with values taken from normal distribution
