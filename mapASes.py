#!/usr/bin/python
import sys
import pandas as pd
import pyasn
import collections
#use pip install pyasn


#writes IPs with slash notation and references as standard ips
def formatIP(seriesRow):
    unaltered = seriesRow.values[0]
    ipWithSources = unaltered.split(",")
    ipWithMask = ipWithSources[0].split("/")

    ip = ipWithMask[0]
    return ip

blacklistPath = str(sys.argv[1:][0])
date = blacklistPath[len(blacklistPath)-10:len(blacklistPath)]
asndb_name = "ipasnDBs/ipasn_" + date.replace('-', '') + ".dat"       #making file name


#ASN database used to map ips to ASNs
asndb = pyasn.pyasn(asndb_name)

blacklistIPsDF = pd.read_fwf(blacklistPath, header=None)              #dataframe
blacklistIPsSeries = blacklistIPsDF.squeeze(axis=0)     #series
#cleaning blacklist IPs
blacklistIPsSeries = blacklistIPsSeries.apply(formatIP, axis=1)
blacklistIPs = blacklistIPsSeries.tolist()

asnList = []
for ip in blacklistIPs:
    asnList.append(asndb.lookup(ip)[0])

asnFrequencies = collections.Counter(asnList)
sortedFreq = {}
sortedKeys = sorted(asnFrequencies, key=asnFrequencies.get)  # [1, 3, 2]

for w in sortedKeys:
    sortedFreq[w] = asnFrequencies[w]


with open("freq_of_ASNs_on_blacklists/ASN frequencies" + date + ".txt", "w") as file:
    file.write("ASN: Frequency\n")
    for key, value in sortedFreq.items():
        line = str(key) + ": " + str(value) + "\n"
        file.write(line)


#print(asnFrequencies)
#    print(asndb.lookup(ip))
#loop through each IP in cleaned list and call asndb.lookup(<ip string>) to get list of ASNs


