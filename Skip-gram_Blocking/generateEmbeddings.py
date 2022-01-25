#2) train neural network
#3) output vectorized systems and connection types

#Skip-gram model

#read words table csv
#initialise embeddings matrix



import csv
from locale import normalize
import pandas as pd
import numpy as np
import random as rnd

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
embedding_dim = 4
numNegSamples = 4


print("Reading data...")
#reading in wordsTable to 2d list (not dataframe because varying number of columns per row)
with open("data/words_table.csv", newline='') as file:
    r = csv.reader(file)
    wordsTable = list(r)

wordsTable = [list(map(int, i)) for i in wordsTable]


#reading connectionTypes into dataframe
connectionTypes = pd.read_csv("data/connection_types.csv")

systemsCount = len(wordsTable)
connectionTypesCount = len(connectionTypes.index)
print("connection types: ", connectionTypesCount)

#making "sentence" for 1 hot encoding reference
sentence = [row[0] for row in wordsTable]
sentence = sentence + connectionTypes["connectionType"].to_list()
pd.DataFrame(sentence).to_csv("data/metadata.csv", index=False, header=False)


sentenceLength = len(sentence)

print("sentence length: ", sentenceLength)



print("generating negative samples")
negativeSamples = []
for s in range(systemsCount):
    negativeSamples.append([])
    for c in range(connectionTypesCount):
        if(not c in wordsTable[s]):
            negativeSamples[s].append(c)


print("\nTraining model...")

embeddingsInitializer = keras.initializers.RandomUniform(minval=-1, maxval=1)
denseInitializer = keras.initializers.RandomNormal()

class Word2Vec(tf.keras.Model):
  def __init__(self, vocab_size, embedding_dim):
    super(Word2Vec, self).__init__()
    self.target_embedding = keras.layers.Embedding(vocab_size,
                                      embedding_dim,
                                      name="w2v_embedding",
                                      embeddings_initializer="uniform",
                                      input_length=numNegSamples+1)


    self.context_embedding = keras.layers.Embedding(vocab_size,
                                       embedding_dim,
                                       input_length=numNegSamples+1)

  def call(self, pair):
    target, context = pair
    word_emb = self.target_embedding(target)
    context_emb = self.target_embedding(context)
    dots = tf.einsum('ikm, ikm-> ik', word_emb, context_emb)
    cos = tf.math.l2_normalize(dots)
    #tf.print(dots)
    return cos

def custom_loss(x_logit, y_true):
    x_logit = tf.cast(x_logit, tf.float32)
    return tf.nn.sigmoid_cross_entropy_with_logits(logits=x_logit, labels=y_true)

model = Word2Vec(sentenceLength, embedding_dim)
#loss is categorical cross entropy so provide training labels as one hot vectors
model.compile(optimizer='Adagrad', loss=keras.losses.LogCosh())#, metrics=['categorical_accuracy', 'accuracy'])


#test start
recordNo=0

for e in range(180000):
    print("epoch: ", e)
    trainingTargets = []                        #each row is a target word represented as its integer index in "sentence"
    trainingContexts = []                       #each row is a list of context words (connection type) represented as their integer indeces in "sentence"
    labels = []
    counter = 0

    for i in range(batchSize):              #loops through 
        for c in range(numSkips):
            trainingTargets.append([])
            if(rnd.random() < 0.2):
                #add one hot encoding of random connection type from this row
                connType1 = wordsTable[recordNo][rnd.randint(1, len(wordsTable[recordNo]) - 1)]                 #gets the number of a random connection type from that row
                #trainingTargets.append(makeOneHot(recordNo+connType1, sentenceLength))
                for f in range(numNegSamples+1):
                    trainingTargets[counter].append(systemsCount+connType1)
            else:
                #add one hot encoding of that system (hot index is just the current i value)
                #trainingTargets.append(makeOneHot(recordNo, sentenceLength))
                for f in range(numNegSamples+1):
                    trainingTargets[counter].append(recordNo)

            #adding a positive sample
            trainingContexts.append([])         #make contexts list 2d
            labels.append([])
            #adding the context word (randomly chosen from current rows avaiable connection types)
            connType2 = wordsTable[recordNo][rnd.randint(1, len(wordsTable[recordNo]) - 1)]
            trainingContexts[counter].append(systemsCount+connType2)
            labels[counter].append(1)

            #adding negative samples
            for n in range(numNegSamples):
                negCon = negativeSamples[recordNo][rnd.randint(0, len(negativeSamples[recordNo])-1)]
                trainingContexts[counter].append(systemsCount+negCon)
                labels[counter].append(-1)

            counter = counter + 1
        recordNo = (recordNo + 1) % systemsCount
            


    #print("labels: ", labels)
    trainingTargets = np.array(trainingTargets)
    #print("targets shape: ", trainingTargets.shape)
    trainingContexts = np.array(trainingContexts)
    #print("Training targets: ", trainingTargets)
    #print("contexts shape: ", trainingContexts.shape)
    labels = np.array(labels)
    BUFFER_SIZE = 10000
    dataset = tf.data.Dataset.from_tensor_slices(((trainingTargets, trainingContexts), labels))
    dataset = dataset.shuffle(BUFFER_SIZE).batch(batchSize*2, drop_remainder=False)
    #print("dataset: ", dataset)
    data = model.fit(dataset, epochs = 1)#batch_size = 16)

#test end

#data = model.fit(x=trainingTargets, y=trainingContexts, batch_size = batchSize, epochs = 1)


#predictions = model(trainingTargets, training=False)

wordEmbeddings = model.get_layer("w2v_embedding").get_weights()[0]           #get_weights returns array containing 2 arrays - 1st one is kernel matrix, second is bias vector (i.e. bias of each node)

pd.DataFrame(wordEmbeddings).to_csv("data/embeddings_matrix.csv", index=False, header=False)


#hiddenEmbeddings = model.get_layer("hid").get_weights()[0]

#pd.DataFrame(wordEmbeddings).to_csv("hiddenEmbeddings_matrix.csv", index=False, header=False)


#print(predictions)

print(model.summary())
