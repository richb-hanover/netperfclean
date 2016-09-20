Using these files:

# Get a list of IP addresses that used > 20K sessions
# Output files:
#  - countsofip.txt - file that shows IP address counts in the form: ### 192.168.1.1
#  - heavyusers.txt - IPs of devices with > 20K sessions from log files
#  - filteredheavyusers.txt - heavy users not present in iptables
#  - iptables-addresses.txt - DROPPEDNETPERF addresses found in iptables
#  - iptables.txt - raw output of 'iptables -nL'
#  - kernlog.txt - concatenated output of all log files

     sudo sh findunfiltered.sh

# See if an address is still testing too hard
     sh checkdistrib.sh <ipaddress>

# Blacklist in iptables if necessary
# Adds all items in filteredheavyusers.txt into iptables using these commands:
#     sudo iptables -I INPUT 3 -p tcp --dport 12865 -j DROPPEDNETPERF --src ip-address
#     sudo su -c 'iptables-save  > /etc/iptables/rules.v4' # must be root...
#     sudo su -c 'ip6tables-save > /etc/iptables/rules.v6'

     sudo addtoblacklist.sh

# distrib.sh - scan the log files for the distribution of access of files in heavyusers.txt



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
