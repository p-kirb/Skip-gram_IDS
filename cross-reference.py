import pandas as pd

#install pandas with "pip install pandas"


#TODO: read IPs from traffic CSV
#TODO: download latest list from firehol from https://raw.githubusercontent.com/ktsaou/blocklist-ipsets/master/firehol_level1.netset
#TODO: clean firehol IP list
#TODO: find intersection of datasets



#trafficData = open("../hornet7-netflow-extended/Honeypot-Cloud-DigitalOcean-Geo-1")

path = "../hornet7Dataset/hornet7-netflow-extended/Honeypot-Cloud-DigitalOcean-Geo-1/2021-04-24_honeypot-cloud-digitalocean-geo-1_netflow-extended.csv"

honeypotIPs = pd.read_csv(path, usecols=["SrcAddr"])

blacklistIPfile = open("iplist.txt", "r")
blacklistIPs = blacklistIPfile.read()

#loop through file and remove info after slashes, also remove lines starting with #
print(blacklistIPs)

print(honeypotIPs)
