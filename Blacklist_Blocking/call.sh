#!/bin/sh
curl https://raw.githubusercontent.com/ktsaou/blocklist-ipsets/master/firehol_level1.netset -o "firehol_iplist.txt"
python3 cross-reference.py
