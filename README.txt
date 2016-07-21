Using these files:

# Get a list of IP addresses that used > 20K sessions
     sudo sh findunfiltered.sh

# See if an address is still testing too hard
     sh checkdistrib.sh <ipaddress>

# Blacklist in iptables if necessary
     sudo iptables -I INPUT 3 -p tcp --dport 12865 -j DROPPEDNETPERF --src ip-address
     sudo su -c 'iptables-save  > /etc/iptables/rules.v4' # must be root...
     sudo su -c 'ip6tables-save > /etc/iptables/rules.v6'

-----
findunfilteredips.sh scans the /var/log/kern.log* files for lines marked with 
"Incoming" (netperf) connections.

It finds the top source addresses (appearing more often than the THRESHOLD), 
then compares those addresses to the set of IPs already filtered by iptables.

It then prints those addresses as candidates for updating the iptables rules.

Threshold: If a device shows > 20,000 hits in the last 7 days, print the address
Then use checkdistrib.sh to see how bad they've been, and whether they're still
doing it.

------
checkdistrib.sh checks the time distribution of suspect IP addresses. It prints
a list of the hours during which that address used the server, plus the number
of hits in that hour. Requires a recent run of findunfilteredips.sh.

Threshold: >500 hits/hour for a continued period. Points off if they are still
using at that rate now. Maybe give a pass for heavy use for a day or so, then stopping. 

------
logscan.sh is a precursor to findunfilteredips.sh. It scans the kern.log* files, and
shows counts for "Incoming" and "Dropped" netperf connections.
