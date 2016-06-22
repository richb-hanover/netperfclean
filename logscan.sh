# Scan /var/log/kern.log to summarize netperf invocations
# Default is to scan /var/log/kern.log
# Pass a filename to scan as first parameter if desired
#
# Invoke with sudo sh logscan.sh
#

date
if [$1 -eq ""]
then 
	INFILE="/var/log/kern.log"
else
	INFILE=$1
fi

head -2 $INFILE
tail -1 $INFILE

# Scan the log file for specified entries
scan_for() {
	cat $INFILE | \
	grep $1 | \
	grep "IN=venet0" | \
	sed -E 's/^.*SRC=//g' | \
	sed -E 's/DST=.*$//g' | \
	sort | uniq -c | sort -nr
}

echo " "
echo "Incoming Netperf Connections"
scan_for "Incoming"

echo " "
echo "Dropped Netperf Connections"
scan_for "Dropped"
