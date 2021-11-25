import pandas as pd


#path = "../../labeled_honeypot_dataset.csv"

#what this program needs to do:
#read honeypot csv file
#seperate last column (labels) from the data
#enumerate any non-numerical data
#train knn model with a portion of the data

#for evaluation: test the model with the rest of the data.
#calculate accuracy, sensitivity, and specificity by comparing predictions to actual labels



honeypotDF = pd.read_csv(path)
labels = honeypotDF[['Label']]              #extracting label vector
honeypotDF.drop(['Label'], axis=1)          #removing labels from features

#enumerating non-numerical data
#use pythons enumerate() and maybe remove dupes? *depending on how enumerate() works*

