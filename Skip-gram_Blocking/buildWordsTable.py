#Script to read data from a network traffic log, and output the table of target/context words used to train the model.
#format of the words table is a unique IP address in column 1 and the following columns containing the connection
#types that that system performed in order.

#1) clean data
#   a) set non-common ports to 9999
#   b) appropriately fill NA values.
#   c) make system-connection type table.


import pandas as pd
import csv

popPorts = {20,21,22,23,25,53,67,68,69,80,110,119,123,135,136,137,138,139,143,161,162,179,389,443,500,636,989,990}

###########################
#FUNCTIONS
###########################
def cleanHex(dataItem):
    if("0x" in dataItem):
        return int(dataItem[2:], 16)
    return dataItem

#filters the destination ports so only the most popular ports (popPorts) are included - if not popular port then set to 9999
def filterPort(dataItem):
    if(int(dataItem) in popPorts):
        return dataItem
    return 9999

###########################
#PROGRAM CODE
###########################

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

#filtering the uncommon ports (may be removed as there are too many unpopular ports being used that arent bad traffic)
honeypotDF['Dport'] = honeypotDF['Dport'].apply(filterPort)



print("getting unique connection types...")
#goes through every communication instance in the log and adds a connectionType entry to the corresponding SrcAddr in the wordsTable
honeypotDF['connectionType'] = pd.factorize(pd._libs.lib.fast_zip([honeypotDF.DstAddr.values, honeypotDF.Dport.values, honeypotDF.Proto.values]))[0] #enumerates the DstAddr, Dport, and Proto columns to give each unique row a unique value

#Getting the indeces of where to find the sourceIP in the wordsTable list for faster lookup
honeypotDF['IPIndex'] = honeypotDF['SrcAddr'].factorize()[0]


honeypotDF.to_csv("cleaned_honeypot.csv", index=False)



print("Building words table...")

#getting unique SrcAddr values in 2d array
wordsTable =  honeypotDF[['SrcAddr']].drop_duplicates().values.tolist()

#TODO: optimise maybe? takes a long time
#loops over honeypotDF, adds the current rows connectionType to the array at the index specified by IPIndex
#(builds the table used to feed data into network)
for index, row in honeypotDF.iterrows():
    wordsTable[row['IPIndex']].append(row['connectionType'])

with open("words_table.csv", "w") as file:
    w = csv.writer(file)
    w.writerows(wordsTable)

#print(wordsTable)

