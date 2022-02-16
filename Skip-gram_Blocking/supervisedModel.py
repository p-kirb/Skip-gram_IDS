
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

from sklearn import tree
from sklearn.metrics import precision_score

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

path = "../../UNSW-NB15 - CSV Files/UNSW-NB15_"

filenames = [path+"1.csv", path+"2.csv", path+"3.csv", path+"4.csv"]

print("reading data...")
dfs = []
for name in filenames:
    df = pd.read_csv(name, index_col=None)
    dfs.append(df)


honeypotDF = pd.concat(dfs, axis=0, ignore_index=True)



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

#print(honeypotDF)



groundTruths = honeypotDF["Label"]
honeypotDF = honeypotDF.drop(['Label'], axis=1)          #removing labels from features
honeypotDF = honeypotDF.drop(['attack_cat'], axis=1)          #removing labels from features




predictions = pd.read_csv("data/predictions.csv")
newLabels = predictions["Prediction"]


trainingCount = round(len(honeypotDF.index) * 0.85)    #85% is training data
testingCount = len(honeypotDF.index) - trainingCount


trainingMatrix = honeypotDF.head(trainingCount)
trainingLabels = newLabels.head(trainingCount)

print("observations: ", len(trainingMatrix))
print("labels: ", len(trainingLabels))

testingMatrix = honeypotDF.tail(testingCount)
testingLabels = groundTruths.tail(testingCount)


#training model
#model = KNeighborsClassifier(n_neighbors=10)
#model.fit(trainingMatrix, trainingLabels)
model = tree.DecisionTreeClassifier()
model.fit(trainingMatrix, trainingLabels)

#predicting
predictions = model.predict(testingMatrix)


#determining accuracy
correctPredictions = sum(predictions == testingLabels)
#correctPredictions = sum(predictions == "Background")           #accuracy if all observations were just labeled as background
print("correct: ", correctPredictions)
print("incorrect: ", testingCount-correctPredictions)

"""attacks = 0
correctAttacks = 0
for i in range(len(predictions)):
    if(testingLabels[i] == 1):
        attacks = attacks + 1
        if(testingLabels[i] == predictions[i]):
            correctAttacks = correctAttacks + 1"""



print("\naccuracy = ", correctPredictions/testingCount)
print("accuracy when assigning modal class: ", sum(testingLabels == 0)/testingCount)

#print("\ncorrect attacks: ", correctAttacks, " out of ", attacks)
print("precision: ", precision_score(testingLabels, predictions))

