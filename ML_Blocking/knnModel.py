import pandas as pd
#Decimal used for large decimal numbers
from decimal import Decimal
from scipy.sparse import data
from sklearn.neighbors import KNeighborsClassifier

##########
#Functions
##########

def parseDate(dateString):
    cleanDate = dateString.replace('/', '')
    cleanDate = cleanDate.replace(' ', '')
    cleanDate = cleanDate.replace(':','')
    return Decimal(cleanDate)


def ip2int(numip):
    if(":" in numip):                   #currently just sets any IPv6 addresses to 0
        return 0
    binIP = ""
    for x in numip.split('.'):
        x = bin(int(x)+256)[3:]         #adds 256 to number (to make them all 9 bits) then removes unnecessary first 3 characters ("0b1")
        binIP+=x
    return int(binIP, 2)

def cleanLabel(row):
    label = row["Label"]
    if "Background" in label:
        return "Background"
    if "Normal" in label:
        return "Normal"
    if "Botnet" in label:
        return "Botnet"
    else:
        return "unclassified"

def cleanHex(dataItem):
    if("0x" in dataItem):
        return int(dataItem[2:], 16)
    return dataItem


#######
#Code
#######
path = "../../CTU-43_bidirectional-sample/capture20110811.binetflow"

#what this program needs to do:
#read honeypot csv file
#seperate last column (labels) from the data
#enumerate any non-numerical data
#train knn model with a portion of the data

#for evaluation: test the model with the rest of the data.
#calculate accuracy, sensitivity, and specificity by comparing predictions to actual labels


print("program start")

print("reading data...")
honeypotDF = pd.read_csv(path)#, nrows=500)

print("cleaning data...")

#removing all background observations
honeypotDF = honeypotDF[~honeypotDF.Label.str.contains("Background")]

labels = honeypotDF[['Label']]              #extracting label vector
honeypotDF = honeypotDF.drop(['Label'], axis=1)          #removing labels from features


#fills all missing data with 0 currently
honeypotDF.fillna("0", axis=0, inplace=True)

#enumerating non-numerical data
#date column just gets converted into one long number
honeypotDF['StartTime'] = honeypotDF['StartTime'].apply(parseDate)
#ip addresses get converted to single numbers
honeypotDF['SrcAddr'] = honeypotDF['SrcAddr'].apply(ip2int)
honeypotDF['DstAddr'] = honeypotDF['DstAddr'].apply(ip2int)
#Dport and Sport get any hex strings to standard ints
honeypotDF['Sport'] = honeypotDF['Sport'].apply(cleanHex)
honeypotDF['Dport'] = honeypotDF['Dport'].apply(cleanHex)


#non-numeric data that is one of multiple options is assigned a number from 0 to however many classes there are.
#using factorize() gives each unique entry a new number (quickly assigning a number to each possible protocol type)
honeypotDF['Proto'] = honeypotDF['Proto'].factorize()[0]
honeypotDF['Dir'] = honeypotDF['Dir'].factorize()[0]
honeypotDF['State'] = honeypotDF['State'].factorize()[0]

#cleaning labels
labels = labels.apply(cleanLabel, axis=1)



#splitting data into training and testing
totalObservations = len(honeypotDF)
trainingCount = round(totalObservations * 0.9)
testingCount = totalObservations - trainingCount

trainingMatrix = honeypotDF.head(trainingCount)
trainingLabels = labels.head(trainingCount)

testingMatrix = honeypotDF.tail(testingCount)
testingLabels = labels.tail(testingCount)


#trainingMatrix.to_csv("trainingMatrix.csv", index=False)
#trainingLabels.to_csv("trainingLabels.csv", index=False)
#testingMatrix.to_csv("testingMatrix.csv", index=False)
#testingLabels.to_csv("testingLabels.csv", index=False)
#honeypotDF.to_csv("cleaned_honeypot.csv", index=False)
#print(honeypotDF)


#model by default uses minowski distance with power (p) of 2 which is the same as using euclidean distance
print("training model...")
model = KNeighborsClassifier(n_neighbors=10)
model.fit(trainingMatrix, trainingLabels)

print("predicting...")
predictions = model.predict(testingMatrix)

#determining accuracy
correctPredictions = sum(predictions == testingLabels)
#correctPredictions = sum(predictions == "Background")           #accuracy if all observations were just labeled as background
print("correct: ", correctPredictions)
print("incorrect: ", testingCount-correctPredictions)

print("accuracy = ", correctPredictions/testingCount)
print("accuracy when assigning modal class: ", sum(predictions == "Botnet")/testingCount)