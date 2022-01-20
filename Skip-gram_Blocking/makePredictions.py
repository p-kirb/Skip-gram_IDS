import pandas as pd
import math

#import the observations dataset
#for every observation, calculate the cosine similarity of system and the connection type being used
#if the cosine similarity > 0, is anomoly

sentence = pd.read_csv("metadata.csv", header=None).to_numpy()

embeddings = pd.read_csv("embeddings_matrix.csv", header=None).to_numpy()

observations = pd.read_csv("cleaned_honeypot-with_attacks.csv")

connTypesStart = observations["IPIndex"].max() + 1          #connection types embeddings start immidiately after systems embeddings

print(connTypesStart)

def predict(row):
    similarity = computeSimilarity(embeddings[row["IPIndex"]], embeddings[connTypesStart + row["connectionType"]])

    return similarity

def computeSimilarity(srcAddr, connectionType):
    numerator = 0
    d1 = 0
    d2 = 0
    for i in range(4):
        numerator = numerator + (srcAddr[i] * connectionType[i])
        d1 = d1 + (srcAddr[i] ** 2)
        d2 = d2 + (connectionType[i] ** 2)
    denominator = math.sqrt(d1) * math.sqrt(d2)
    if((numerator/denominator) < 0):
        return 1
    return 0
    


print("count: ",len(observations.index))


print("cleaning data...")

#keeping only the relevant columns
labels = observations['Label']
observations = observations[['SrcAddr', 'connectionType', 'IPIndex', 'Label']]

observations['Prediction'] = observations.apply(predict, axis=1)

observations[['Label', 'Prediction']].to_csv("predictions.csv", index=False)



truths = observations['Label'].to_numpy()
predictions = observations['Prediction'].to_numpy()

correct = 0
for i in range(len(truths)):
    if(truths[i] == predictions[i]):
        correct = correct + 1

print("Accuracy: ", correct/len(truths))


