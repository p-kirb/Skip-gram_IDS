#!/bin/sh
pip install pyasn
cd ../../
mkdir week_of_blacklists
cd week_of_blacklists
#download zip lists
curl https://steel.isi.edu/projects/BLAG/data/2021/04/2021-04-23.zip -o "day1.zip"
curl https://steel.isi.edu/projects/BLAG/data/2021/04/2021-04-24.zip -o "day2.zip"
curl https://steel.isi.edu/projects/BLAG/data/2021/04/2021-04-25.zip -o "day3.zip"
curl https://steel.isi.edu/projects/BLAG/data/2021/04/2021-04-26.zip -o "day4.zip"
curl https://steel.isi.edu/projects/BLAG/data/2021/04/2021-04-27.zip -o "day5.zip"
curl https://steel.isi.edu/projects/BLAG/data/2021/04/2021-04-28.zip -o "day6.zip"
curl https://steel.isi.edu/projects/BLAG/data/2021/04/2021-04-29.zip -o "day7.zip"

unzip day1.zip
unzip day2.zip
unzip day3.zip
unzip day4.zip
unzip day5.zip
unzip day6.zip
unzip day7.zip

#move plaintext lists to lists folder
mkdir lists
mv 2021-04-23/2021-04-23    2021-04-24/2021-04-24   2021-04-25/2021-04-25   2021-04-26/2021-04-26   2021-04-27/2021-04-27   2021-04-28/2021-04-28   2021-04-29/2021-04-29 lists

#remove folders
rm -r 2021-04-23    2021-04-24    2021-04-25    2021-04-26    2021-04-27    2021-04-28    2021-04-29

#moving zips into their own folder
mkdir zips
mv *.zip zips

cd ../SCC300HoneypotProject/Mapping_IPs_to_Autonomous_Systems
#downloading RIB files (used to build database to map IPs to ASNs with pyasn module)
python3 ~/.local/bin/pyasn_util_download.py --dates-from-file dates.txt

#moving downloaded files to folder
mkdir bz2_files
mv *.bz2 bz2_files

#moving databases to folder
mkdir ipasnDBs
mv *.dat ipasnDBs

#converting .bz2 files to database ".dat" files
python3 ~/.local/bin/pyasn_util_convert.py --bulk 2021-04-23 2021-04-29

#making folder for output of python files
mkdir freq_of_ASNs_on_blacklists
python3 mapASes.py ../../week_of_blacklists/lists/2021-04-23
python3 mapASes.py ../../week_of_blacklists/lists/2021-04-24
python3 mapASes.py ../../week_of_blacklists/lists/2021-04-25
python3 mapASes.py ../../week_of_blacklists/lists/2021-04-26
python3 mapASes.py ../../week_of_blacklists/lists/2021-04-27
python3 mapASes.py ../../week_of_blacklists/lists/2021-04-28
python3 mapASes.py ../../week_of_blacklists/lists/2021-04-29




