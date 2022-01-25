
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier


#read in whole dataset.
#read in the skipgram predicted labels.
#replace real labels with skipgram predictions.
#train model
#make predictions on test data
#compare real labels of test data with predictions


path = "../../UNSW-NB15 - CSV Files/UNSW-NB15_"

filenames = [path+"1.csv", path+"2.csv", path+"3.csv", path+"4.csv"]

print("reading data...")
dfs = []
for name in filenames:
    df = pd.read_csv(name, index_col=None)
    dfs.append(df)


honeypotDF = pd.concat(dfs, axis=0, ignore_index=True)

groundTruths = honeypotDF["Label"]
honeypotDF = honeypotDF.drop(['Label'], axis=1)          #removing labels from features


predictions = pd.read_csv("data/predictions.csv")
newLabels = predictions["Prediction"]


trainingCount = round(len(honeypotDF.index) * 0.85)    #85% is training data
testingCount = len(honeypotDF.index) - trainingCount


trainingMatrix = honeypotDF.head(trainingCount)
trainingLabels = newLabels.head(trainingCount)

testingMatrix = honeypotDF.tail(testingCount)
testingLabels = groundTruths.tail(testingCount)


#training model
model = KNeighborsClassifier(n_neighbors=10)
model.fit(trainingMatrix, trainingLabels)

#predicting
predictions = model.predict(testingMatrix)


#determining accuracy
correctPredictions = sum(predictions == testingLabels)
#correctPredictions = sum(predictions == "Background")           #accuracy if all observations were just labeled as background
print("correct: ", correctPredictions)
print("incorrect: ", testingCount-correctPredictions)

print("accuracy = ", correctPredictions/testingCount)
