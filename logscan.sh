# Scan /var/log/kern.log to summarize netperf invocations
# Default is to scan /var/log/kern.log
# Pass a filename to scan as first parameter if desired
#
# Invoke with sudo sh logscan.sh
#

if [$1 -eq ""]
then 
	INFILE="/var/log/kern.log"
else
	INFILE=$1
fi
cat $INFILE | \
grep "Incoming netperf" | \
grep "IN=venet0" | \
sed -E 's/^.*SRC=//g' | \
sed -E 's/DST=.*$//g' | \
sort | uniq -c | sort -nr
