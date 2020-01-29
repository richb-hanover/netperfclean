#! /bin/bash
#
# Concatenate all the kern.log files from last week into a single file
#

# Scan the log file for specified entries
scan_for() {
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

zcat /var/log/kern.log.7.gz >  kernlog.txt
zcat /var/log/kern.log.6.gz >> kernlog.txt
zcat /var/log/kern.log.5.gz >> kernlog.txt
zcat /var/log/kern.log.4.gz >> kernlog.txt
zcat /var/log/kern.log.3.gz >> kernlog.txt
zcat /var/log/kern.log.2.gz >> kernlog.txt
cat /var/log/kern.log.1     >> kernlog.txt
cat /var/log/kern.log       >> kernlog.txt

INFILE='kernlog.txt'
scan_for "Incoming" | \
tee countsofip.txt | \
# split off the count, and output lines with high counts
awk -v num_entries=$NUM_ENTRIES \
    'BEGIN { print num_entries } \
    {
     if ($1 > num_entries) print $2;
    }
    END { } ' | \
sort | \
# heavyusers.txt has IP addresses with high counts
cat > heavyusers.txt
# rm kernlog.txt

# Now dump the iptables to list the current set of drops
echo "Addresses with greater than $NUM_ENTRIES connections that aren't listed 
in iptables" 
iptables -nL | \
tee iptables.txt | \
grep "DROPPEDNETPERF  tcp" | \
sed -E 's/^.* --  //g' | \
sed -E 's/[ ].*$//g'  | \
sort | \
# iptables-addresses.txt has the list of DROPPEDNETPERF addresses in iptables
tee iptables-addresses.txt | \
comm -13 - heavyusers.txt > filteredheavyusers.txt
grep -f filteredheavyusers.txt countsofip.txt

# And finally scan the iptables for duplicate addresses
sh checkforiptablesdups.sh
