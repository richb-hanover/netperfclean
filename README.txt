findunfilteredips.sh scans the /var/log/kern.log* files for lines marked with "Incoming" (netperf) connections.

It finds the top source addresses (appearing more often than the THRESHOLD), 
then compares those addresses to the set of IPs already filtered by iptables.

It then prints those addresses as candidates for updating the iptables rules.

------
logscan.sh is a precursor to findunfilteredips.sh. It scans the kern.log* files, and
shows counts for "Incoming" and "Dropped" netperf connections.
