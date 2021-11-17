#!/usr/bin/python
import sys

import pyasn
#use pip install pyasn

blacklistPath = str(sys.argv[1:][0])
print("argument: ", blacklistPath)

#ASN database used to map ips to ASNs
#asndb = pyasn.pyasn(<created database name>)


#loop through each IP in cleaned list and call asndb.lookup(<ip string>) to get list of ASNs


