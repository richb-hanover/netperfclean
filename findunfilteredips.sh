#! /bin/bash
#
# This script scans kern.log files to count entries that are tagged with "Incoming"
# These entries are created by an iptables rule for each connection to port 12685
# The script then looks for addresses of "heavy users"  that have made more than 
# $NUM_ENTRIESconnections recently indicating they're abusing the netperf server.
# 
# The script has several outputs:
# - filteredheavyusers.txt - a list of IP addresses that are not already in iptables
# - countsofip.txt - counts of IP addresses > $NUM_ENTRIES
# 

# Scan the $INFILE for lines with specified entries
# and count their occurrence
count_lines_with() {
    cat $INFILE | \
    grep $1 | \
    grep "IN=venet0" | \
    sed -E 's/^.*SRC=//g' | \
    sed -E 's/DST=.*$//g' | \
    sort | uniq -c | sort -nr
}

NUM_ENTRIES=$1
if [ -z $NUM_ENTRIES ]
then
   NUM_ENTRIES=5000
fi

echo "Number of entries to scan for: $NUM_ENTRIES"

# combine all recent kern.log files into a local file
# zcat /var/log/kern.log.7.gz >  kernlog.txt
# zcat /var/log/kern.log.6.gz >> kernlog.txt
# zcat /var/log/kern.log.5.gz >> kernlog.txt
# zcat /var/log/kern.log.4.gz >> kernlog.txt
# zcat /var/log/kern.log.3.gz >> kernlog.txt
# zcat /var/log/kern.log.2.gz >> kernlog.txt
cat /var/log/kern.log.1     >> kernlog.txt
cat /var/log/kern.log       >> kernlog.txt

# Starting with kernlog.txt
INFILE='kernlog.txt'
# count the occurrences of "Incoming"
count_lines_with "Incoming" | \
# save that list in countsofip.txt
tee countsofip.txt | \
# only keep lines with counts > $NUM_ENTRIES
awk -v num_entries=$NUM_ENTRIES \
    'BEGIN { } \
    {
     if ($1 > num_entries) print $2;
    }
    END { } ' | \
sort | \
# save that list of IP addresses with high counts
cat > heavyusers.txt
# rm kernlog.txt

# Now dump the iptables to list the current set of drops
echo "Addresses with greater than $NUM_ENTRIES connections that aren't listed 
in iptables" 
# List all iptables rules
iptables -nL | \
# save that list in iptables.txt
tee iptables.txt | \
# only keep DROPPEDNETPERF lines
grep "DROPPEDNETPERF  tcp" | \
# isolate the source IP address of those DROPPEDNETPERF entries
sed -E 's/^.* --  //g' | \
sed -E 's/[ ].*$//g'  | \
sort | \
# save that list in iptables-addresses.txt
tee iptables-addresses.txt | \
# find the addresses in heavyusers.txt that *aren't* already in iptables
comm -13 - heavyusers.txt | \
# remove whitelist hosts from list to be added to iptables 
grep -vf whitelist.txt > filteredheavyusers.txt
# display addresses from countsofip.txt that aren't already in iptables
grep -f filteredheavyusers.txt countsofip.txt

# And finally scan the iptables for duplicate addresses
sh checkforiptablesdups.sh
