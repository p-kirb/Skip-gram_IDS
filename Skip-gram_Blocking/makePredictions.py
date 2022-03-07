import pandas as pd
import math
import time

#import the observations dataset
#for every observation, calculate the cosine similarity of system and the connection type being used
#if the cosine similarity > 0, is anomoly

print("program start: makePredictions")


sentence = pd.read_csv("data/metadata.csv", header=None).to_numpy()

embeddings = pd.read_csv("data/embeddings_matrix.csv", header=None).to_numpy()

#observations is first 80% of clean samples + first 80% of malicious samples
cleanSamples = pd.read_csv("data/skipgram_training_honeypot.csv")
maliciousSamples = pd.read_csv("data/cleaned_honeypot-with_attacks.csv")
maliciousSamples = maliciousSamples[maliciousSamples["Label"] == 1]
maliciousSamples = maliciousSamples.head(round(0.8 * len(maliciousSamples.index)))

#code section for testing skip-gram on 20% of records
#cleanSamples = pd.read_csv("data/cleaned_honeypot-with_attacks.csv")
#maliciousSamples = cleanSamples[cleanSamples["Label"] == 1]
#maliciousSamples = maliciousSamples.tail(round(0.2 * len(maliciousSamples.index)))
#cleanSamples = cleanSamples[cleanSamples["Label"] == 0]
#cleanSamples = cleanSamples.tail(round(0.2 * len(cleanSamples.index)))

observations = pd.concat([cleanSamples, maliciousSamples])



connTypesStart = observations["IPIndex"].max() + 1          #connection types embeddings start immidiately after systems embeddings

print(connTypesStart)
print("Dataset length: ", len(observations.index))

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

start = time.time()
observations['Prediction'] = observations.apply(predict, axis=1)
end = time.time()
timeTaken = end - start

observations[['Label', 'Prediction']].to_csv("data/predictions.csv", index=False)



truths = observations['Label'].to_numpy()
predictions = observations['Prediction'].to_numpy()

correct = 0
attacks = 0
correctAttacks = 0
for i in range(len(truths)):
    if(truths[i] == 1):
        attacks = attacks + 1
    if(truths[i] == predictions[i]):
        correct = correct + 1
        if(truths[i] == 1):
            correctAttacks = correctAttacks+1

acc = "Accuracy: " + str(correct/len(truths))
prec = "\nPrecision: " + str(correctAttacks/attacks)
sens = "\nSensitivity: " + str((correct-correctAttacks)/(len(truths)-attacks))

print(acc)
print(prec)
print(sens)
print("Time taken: ", timeTaken)


f = open("data/skipgram_predictions_summary.txt", "w")
f.write(acc + prec + sens)
f.close
