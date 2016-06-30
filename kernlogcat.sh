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
tee junk.txt | \
awk 'BEGIN { } \
    {
     if ($1 > 3000) print $2;
    }
    END { } ' | \
sort | \
cat > badboys.txt
rm kernlog.txt

# Now dump the iptables to list the current set of drops
iptables -nL | \
tee iptables.txt | \
grep "DROPPEDNETPERF  tcp" | \
sed -E 's/^.* --  //g' | \
sed -E 's/[ ].*$//g'  | \
sort | \
tee junk.txt | \
comm -13 - badboys.txt
