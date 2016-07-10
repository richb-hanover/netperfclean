#! /bin/sh
#
# checkdistrib.sh
#
# Check the (time) distribution of a particular IP address' presence in the kernlog.txt file
# Helps distinguish brief heavy testing from continuous users
#
# To use:
# sudo sh findunfilteredips.sh # to create the updated kernlog.txt file
# sh checkdistrib.sh <ip-address>


cat kernlog.txt | \
grep "Incoming netperf" | \
grep $1 | \
tee temp.txt | \
sed -E 's/netperf kernel.*//g' | \
sed -E 's/......$//g' | \
uniq -c
echo "$1 `wc -l < temp.txt` lines"
