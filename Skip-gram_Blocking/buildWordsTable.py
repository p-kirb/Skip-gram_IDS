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
    if(isinstance(dataItem, str)):
        if("0x" in dataItem):
            return int(dataItem[2:], 16)
        else:
            return 9999                         #rows with missing values get returned as 9999
    return dataItem

#filters the destination ports so only the most popular ports (popPorts) are included - if not popular port then set to 9999
def filterPort(dataItem):
    if(int(dataItem) in popPorts):
        return dataItem
    return 9999


def ip2int(numip):
    binIP = ""
    for x in numip.split('.'):
        x = bin(int(x)+256)[3:]         #adds 256 to number (to make them all 9 bits) then removes unnecessary first 3 characters ("0b1")
        binIP+=x
    return int(binIP, 2)

###########################
#PROGRAM CODE
###########################

print("program start: buildWordsTable")
path = "../../UNSW-NB15 - CSV Files/UNSW-NB15_"

filenames = [path+"1.csv", path+"2.csv", path+"3.csv", path+"4.csv"]

print("reading data...")
dfs = []
for name in filenames:
    df = pd.read_csv(name, index_col=None)
    dfs.append(df)


honeypotDF = pd.concat(dfs, axis=0, ignore_index=True)

print("count: ",len(honeypotDF.index))


print("cleaning data...")

#keeping only the relevant columns
honeypotDF = honeypotDF[['SrcAddr', 'DstAddr', 'Dport', 'Proto', 'Label']]

#fills all missing data with 0
honeypotDF.fillna("0", axis=0, inplace=True)

#drops any observations with an IPv6 SrcAddr
honeypotDF = honeypotDF[~honeypotDF.SrcAddr.str.contains(":")]


#Sport gets any hex strings to standard ints
honeypotDF['Dport'] = honeypotDF['Dport'].apply(cleanHex)

#filtering the uncommon ports (may be removed as there are too many unpopular ports being used that arent bad traffic)
honeypotDF['Dport'] = honeypotDF['Dport'].apply(filterPort)

#converting all SrcAddr values to ints (for easier feeding into NN)
honeypotDF['SrcAddr'] = honeypotDF['SrcAddr'].apply(ip2int)


print("getting unique connection types...")
#goes through every communication instance in the log and adds a connectionType entry to the corresponding SrcAddr in the wordsTable
honeypotDF['connectionType'] = pd.factorize(pd._libs.lib.fast_zip([honeypotDF.DstAddr.values, honeypotDF.Dport.values, honeypotDF.Proto.values]))[0] #enumerates the DstAddr, Dport, and Proto columns to give each unique row a unique value


#writing just the connection types and their number to a file
connectionTypesDF = honeypotDF.drop_duplicates('connectionType')
connectionTypesDF = connectionTypesDF[['connectionType','DstAddr', 'Dport', 'Proto']]
connectionTypesDF.to_csv("data/connection_types.csv", index=False)

#Getting the indeces of where to find the sourceIP in the wordsTable list for faster lookup
honeypotDF['IPIndex'] = honeypotDF['SrcAddr'].factorize()[0]

honeypotDF.to_csv("data/cleaned_honeypot-with_attacks.csv", index = False)

#dropping rows with attacks (for training)
honeypotDF = honeypotDF[honeypotDF["Label"] == 0]
#getting first 80%
honeypotDF = honeypotDF.head(round(0.8 * len(honeypotDF.index)))
honeypotDF.to_csv("data/skipgram_training_honeypot.csv", index=False)





print("Building words table...")

#getting unique SrcAddr values in 2d array
wordsTable =  honeypotDF[['SrcAddr']].drop_duplicates().values.tolist()


for index, row in honeypotDF.iterrows():
    wordsTable[row['IPIndex']].append(row['connectionType'])

with open("data/words_table.csv", "w") as file:
    w = csv.writer(file)
    w.writerows(wordsTable)

#print(wordsTable)

