import pandas as pd

#install pandas with "pip install pandas"


#TODO: get submask2regex function to work when applied to blacklistIPSeries
#TODO: find intersection of datasets

##########
#FUNCTIONS
##########

#writes IPs as regular expressions (subnets represented by *s)
def submask2regex(seriesRow):
    unaltered = seriesRow.values[0]
    ipWithSources = unaltered.split(",")
    ipWithMask = ipWithSources[0].split("/")

    ip = ipWithMask[0]#ip2bin(ipWithMask[0])

    #trims subnet mask off and replaces with *s (if subnet mask stated)
    #if(len(ipWithMask) == 2):
    #    ip = ip[:len(ip) - int(ipWithMask[1])]
        #for i in range(int(ipWithMask[1])):
        #    ip+="*"
    return ip




#converts ip addresses into single binary number
def ip2bin(numip):
    binIP = ""
    for x in numip.split('.'):
        x = bin(int(x)+256)[3:]         #adds 256 to number (to make them all 9 bits) then removes unnecessary first 3 characters ("0b1")
        binIP+=x
    return binIP



########
#PROGRAM
########

#honeypot data
path = "../hornet7Dataset/hornet7-netflow-extended/Honeypot-Cloud-DigitalOcean-Geo-1/2021-04-23_honeypot-cloud-digitalocean-geo-1_netflow-extended.csv"

honeypotIPsDF = pd.read_csv(path, usecols=["SrcAddr"])          #dataframe

honeypotIPsDF = honeypotIPsDF.drop_duplicates()                 #remove duplicates
honeypotIPsSeries = honeypotIPsDF.squeeze(axis=0)               #make series

#cleaning honeypot IPs
honeypotIPsSeries = honeypotIPsSeries.apply(submask2regex, axis=1)
print("honeypot cleaned.")





#reading blacklist
blacklistIPsDF = pd.read_fwf("../2021-04-23/2021-04-23")              #dataframe
blacklistIPsSeries = blacklistIPsDF.squeeze(axis=0)     #series

#removes lines containing "#"
blacklistIPsSeries = blacklistIPsSeries[blacklistIPsSeries.iloc[:,0].str.contains("#") == False]

#transforms each IP to binary version with subnet as *s
blacklistIPsSeries = blacklistIPsSeries.apply(submask2regex, axis=1)
print("blacklist cleaned.")

#converting to sets
blacklistSet = set(blacklistIPsSeries)
honeypotSet = set(honeypotIPsSeries)


intersection = blacklistSet.intersection(honeypotSet)
#print(intersection)
#print(len(intersection))
print("unique honeypot addresses length:",len(honeypotSet))
print("blacklist length:",len(blacklistSet))
print("intersection length: ", len(intersection))