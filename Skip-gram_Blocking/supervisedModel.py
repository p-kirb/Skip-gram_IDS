
from socketserver import ThreadingMixIn
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn import svm

import gc
import sys

#read in whole dataset.
#read in the skipgram predicted labels.
#replace real labels with skipgram predictions.
#train model
#make predictions on test data
#compare real labels of test data with predictions

def ip2int(numip):
    if(":" in numip):                   #currently just sets any IPv6 addresses to 0
        return 0
    binIP = ""
    for x in numip.split('.'):
        x = bin(int(x)+256)[3:]         #adds 256 to number (to make them all 9 bits) then removes unnecessary first 3 characters ("0b1")
        binIP+=x
    return int(binIP, 2)


#sorts out hex values (return as ints) and also sets any invalid (-) entrys to 9999
def cleanHex(dataItem):
    if(isinstance(dataItem, str)):
        if("0x" in dataItem):
            return int(dataItem[2:], 16)
        else:
            return 9999
    return dataItem




print("program start: supervisedModel")

path = "../../UNSW-NB15 - CSV Files/UNSW-NB15_"                             #reding in raw, unprocessed data

filenames = [path+"1.csv", path+"2.csv", path+"3.csv", path+"4.csv"]

print("reading data...")
dfs = []
for name in filenames:
    df = pd.read_csv(name, index_col=None)
    dfs.append(df)


honeypotDF = pd.concat(dfs, axis=0, ignore_index=True)

for i in dfs:
    del i
del dfs
del df
gc.collect()


print("cleaning data...")

honeypotDF['SrcAddr'] = honeypotDF['SrcAddr'].apply(ip2int)
honeypotDF['DstAddr'] = honeypotDF['DstAddr'].apply(ip2int)

honeypotDF['sport'] = honeypotDF['sport'].apply(cleanHex)
honeypotDF['Dport'] = honeypotDF['Dport'].apply(cleanHex)


#enumerating text fields
honeypotDF['Proto'] = honeypotDF['Proto'].factorize()[0]
honeypotDF['state'] = honeypotDF['state'].factorize()[0]
honeypotDF['service'] = honeypotDF['service'].factorize()[0]

honeypotDF = honeypotDF.replace(r"^$", np.NaN, regex=True)        #replace empty strings with 0
for column in honeypotDF:
    honeypotDF[column] = pd.to_numeric(honeypotDF[column], errors='coerce')

honeypotDF = honeypotDF.fillna("0", axis=0)

#print("total samples: ", len(honeypotDF.index))


groundTruths = honeypotDF["Label"].tolist()
honeypotDF = honeypotDF.drop(['attack_cat'], axis=1)          #removing attact types (information relates to label)


#splitting into training and testing
goodSamples = honeypotDF[honeypotDF["Label"] == 0]     #isolating benign samples to get dataset to line up with labels produced
malSamples = honeypotDF[honeypotDF["Label"] == 1]

del honeypotDF
gc.collect()


goodSplitIndex = round(0.8 * len(goodSamples.index))
malSplitIndex = round(0.8 * len(malSamples.index))


trainingGood = goodSamples.head(goodSplitIndex)
testingGood = goodSamples.tail(len(goodSamples.index) - goodSplitIndex)


del goodSamples                 #cleanup

trainingMal = malSamples.head(malSplitIndex)
testingMal = malSamples.tail(len(malSamples.index) - malSplitIndex)


del malSamples                  #cleanup
gc.collect()

trainingMatrix = pd.concat([trainingGood, trainingMal])      #combines the 2 matrices

del trainingGood, trainingMal
gc.collect()


testingMatrix = pd.concat([testingGood, testingMal]).sample(frac=1) #builds and shuffles testing matrix

del testingGood, testingMal
gc.collect()


trainingMatrix = trainingMatrix.drop(['Label'], axis=1)          #removing labels from training matrix



#fetching labels
predictions = pd.read_csv("data/predictions.csv")               #the predictions made by the skip gram model, to be used here as labels for training
trainingLabels = predictions["Prediction"].tolist()

del predictions
gc.collect()


print("training observations: ", len(trainingMatrix.index))
print("training labels: ", len(trainingLabels))
#print("labels: ", len(trainingLabels))


testingLabels = testingMatrix["Label"].tolist()
testingMatrix = testingMatrix.drop(["Label"], axis=1)

print("testing observations: ", len(testingMatrix.index))
print("testing labels: ", len(testingLabels))

#name, obj = None, None
#for name, obj in locals().items():
#    print(name, ":\t\t\t", sys.getsizeof(obj))

#training model
print("training model")
#model = KNeighborsClassifier(n_neighbors=10)

#model = tree.DecisionTreeClassifier()

model = GaussianNB()

#model = svm.SVC()
model.fit(trainingMatrix, trainingLabels)


print("predicting")
#predicting
predictions = model.predict(testingMatrix)


#determining accuracy
correctPredictions = sum(predictions == testingLabels)
#correctPredictions = sum(predictions == "Background")           #accuracy if all observations were just labeled as background
print("correct: ", correctPredictions)
print("incorrect: ", len(testingMatrix.index)-correctPredictions)

attacks = 0
correctAttacks = 0
for i in range(len(predictions)):
    if(testingLabels[i] == 1):
        attacks = attacks + 1
        if(testingLabels[i] == predictions[i]):
            correctAttacks = correctAttacks + 1



print("\naccuracy = ", correctPredictions/len(testingMatrix.index))
#print("accuracy when assigning modal class: ", sum(testingLabels == 0)/len(testingMatrix.index))

#print("\ncorrect attacks: ", correctAttacks, " out of ", attacks)
print("precision: ", correctAttacks/attacks)
print("sensitivity: ", (correctPredictions - correctAttacks) / (len(testingMatrix.index) - attacks))

