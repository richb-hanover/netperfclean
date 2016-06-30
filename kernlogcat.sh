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
cat > junk.txt
rm kernlog.txt

