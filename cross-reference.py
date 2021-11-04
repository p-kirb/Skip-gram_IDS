import pandas as pd

#install pandas with "pip install pandas"


#TODO: read IPs from traffic CSV
#TODO: download latest list from firehol
#TODO: clean firehol IP list
#TODO: find intersection of datasets



#trafficData = open("../hornet7-netflow-extended/Honeypot-Cloud-DigitalOcean-Geo-1")

my_csv = pd.read_csv("../hornet7-netflow-extended/Honeypot-Cloud-DigitalOcean-Geo-1/2021-04-23_honeypot-cloud-digitalocean-geo-1_netflow-extended.csv")
column = my_csv.SrcAddr

print(column)
