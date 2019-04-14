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
#
# Format of kernlog.txt
#
# Sep  1 03:10:57 netperf kernel: [3582360.450529] Dropped netperf  ...
#
# - First remove everything from 'netperf kernel' to the end of the line
# - then remove the last six characters (the :mm:ss) leaving only the hours
# - summarize the hours

cat kernlog.txt | \
grep "Incoming netperf" | \
grep SRC=$1 | \
sed -E 's/atl kernel.*//g' | \
tee temp.txt | \
sed -E 's/......$//g' | \
uniq -c
echo "$1 `wc -l < temp.txt` lines"
