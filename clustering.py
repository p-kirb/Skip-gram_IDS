import pandas as pd


path = "../hornet7Dataset/hornet7-netflow-extended/Honeypot-Cloud-DigitalOcean-Geo-1/2021-04-23_honeypot-cloud-digitalocean-geo-1_netflow-extended.csv"

honeypotDF = pd.read_csv(path, error_bad_lines=False)          #dataframe
badIPsDF = pd.read_fwf("intersection.csv", header=None)
badIPs = badIPsDF.squeeze(axis=0)               #make series

#columnsToIgnore = ["SrcId", "Seq", "StartTime", "LastTime", "SrcStartTime", "SrcLastTime", "DstStartTime", "DstLastTime", "SRange", "Trans", "SrcAddr", "DstAddr"]

print(badIPsDF)

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


print("badcount: ", badcount)
print("goodcount: ", goodcount)