#1) clean data
#   a) set non-common ports to 9999 (look for "non-common" criteria in paper)
#   b) appropriately fill NA values.
#   c) make system-connection type table.
#2) train neural network
#3) output vectorized systems and connection types

import pandas as pd
import numpy as np

def cleanHex(dataItem):
    if("0x" in dataItem):
        return int(dataItem[2:], 16)
    return dataItem

print("program start")
path = "../../CTU-43_bidirectional-sample/capture20110811.binetflow"


print("reading data...")
honeypotDF = pd.read_csv(path)#, nrows=500)


print("cleaning data...")

#keeping only the relevant columns
honeypotDF = honeypotDF[['SrcAddr', 'DstAddr', 'Dport', 'Proto']]

#TODO: decide what to do with this
#removing all background observations
#honeypotDF = honeypotDF[~honeypotDF.Label.str.contains("Background")]


#TODO: align this with papers handling of NA values
#fills all missing data with 0 currently
honeypotDF.fillna("0", axis=0, inplace=True)


#Sport gets any hex strings to standard ints
honeypotDF['Dport'] = honeypotDF['Dport'].apply(cleanHex)



print("getting unique connection types")
#goes through every communication instance in the log and adds a connectionType entry to the corresponding SrcAddr in the wordsTable
honeypotDF['connectionType'] = pd.factorize(pd._libs.lib.fast_zip([honeypotDF.DstAddr.values, honeypotDF.Dport.values, honeypotDF.Proto.values]))[0] #enumerates the DstAddr, Dport, and Proto columns to give each unique row a unique value

#Getting the indeces of where to find the sourceIP in the wordsTable list for faster lookup
honeypotDF['IPIndex'] = honeypotDF['SrcAddr'].factorize()[0]


honeypotDF.to_csv("cleaned_honeypot.csv", index=False)


#getting unique SrcAddr values in 2d array
wordsTable =  honeypotDF[['SrcAddr']].drop_duplicates().values.tolist()


#TODO: optimise maybe? takes a while
#loops over honeypotDF, adds the current rows connectionType to the array at the index specified by IPIndex
#(builds the table used to feed data into network)
for index, row in honeypotDF.iterrows():
    wordsTable[row['IPIndex']].append(row['connectionType'])

print(wordsTable)




