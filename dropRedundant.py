from numpy.core.numeric import NaN
import pandas as pd
import numpy as np


path = "../hornet7Dataset/hornet7-netflow-extended/Honeypot-Cloud-DigitalOcean-Geo-1/2021-04-23_honeypot-cloud-digitalocean-geo-1_netflow-extended.csv"

honeypotDF = pd.read_csv(path, error_bad_lines=False)          #dataframe
badIPsDF = pd.read_fwf("intersection.csv", header=None)
badIPs = badIPsDF.squeeze(axis=0)               #make series

#columnsToIgnore = ["SrcId", "Seq", "StartTime", "LastTime", "SrcStartTime", "SrcLastTime", "DstStartTime", "DstLastTime", "SRange", "Trans", "SrcAddr", "DstAddr"]

#print(badIPsDF)

labels = []
badcount = 0
goodcount = 0

#TODO: create label vector from each instance by checking its source address, if contained on the blacklist, label bad

#for instance in honeypotDF:
    #print(instance)
    #if badIPs.str.contains(instance.loc["SrcAddr"]):
    #    badcount += 1
    #else:
    #    goodcount += 1


#making correlation matrix of columns in honeypot dataset (absolute values for easier removal)
corrMat = honeypotDF.corr(method = "pearson").abs()
corrMat.to_csv("correlation.csv")
corrThresh = 0.95


# Select upper triangle of correlation matrix
upper = corrMat.where(np.triu(np.ones(corrMat.shape), k=1).astype(np.bool))

# Find features with correlation greater than 0.95
dropping = [column for column in upper.columns if (any(upper[column] > 0.95) or upper[column].isnull().values.all())]

#print(honeypotDF)

# Drop features 
honeypotDF.drop(dropping, axis=1, inplace=True)


#drops any non-numeric columns then fills missing values with 0(just for testing)
honeypotDF = honeypotDF.select_dtypes(include="number")
honeypotDF = honeypotDF.fillna(value=0)


print(honeypotDF)

honeypotDF.to_csv("honeypot-redundant-dropped.csv")




print("badcount: ", badcount)
print("goodcount: ", goodcount)