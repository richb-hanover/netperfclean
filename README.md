## README for cleaning up iptables files

iptables is configured to log "undropped" netperf connections (to port 12865) with "Incoming netperf" in /var/log/kern.log 
They have the form:

```
Feb 11 03:11:45 atl kernel: [9353834.165208] Incoming netperf IN=lo OUT= MAC=00:00:00:00:00:00:00:00:00:00:00:00:08:00 
SRC=23.226.232.80 DST=23.226.232.80 LEN=60 TOS=0x00 PREC=0x00 TTL=64 ID=38423 DF PROTO=TCP SPT=56374 DPT=12865 WINDOW=65535 RES=0x00 SYN 
URGP=0
```

`sudo sh findunfiltered.sh ###` scans the last week's /var/log/kern.log* files for those "Incoming 
netperf" lines,
isolates the SRC=... addresses, and creates a frequency count of those addresses. It writes a list of IP addresses
that occur more than ### lines (default = 5000) in the seven days to a file heavyusers.txt.

It then compares it to the list of IP addresses that are already filtered in iptables (into the DROPPEDNETPERF chain)
and writes that (shorter list) to filteredheavyusers.txt

`sudo sh addtoblacklist.sh` takes the list of filteredheavyusers.txt and adds those addresses to the DROPPEDNETPERF chain 

## Old info - no longer up-to-date

Using these files:

 `sudo sh findunfiltered.sh ###` Get a list of IP addresses that used > 20K sessions

   * countsofip.txt - file that shows IP address counts in the form: ### 192.168.1.1
   * heavyusers.txt - IPs of devices with > 20K sessions from log files
   * filteredheavyusers.txt - heavy users not present in iptables
   * iptables-addresses.txt - DROPPEDNETPERF addresses found in iptables
   * iptables.txt - raw output of 'iptables -nL'
   * kernlog.txt - concatenated output of all log files


`sh checkdistrib.sh <ipaddress>` See if an address is still testing too hard
     

* Blacklist in iptables if necessary
* Adds all items in filteredheavyusers.txt into iptables using these commands:

* sudo iptables -I INPUT 3 -p tcp --dport 12865 -j DROPPEDNETPERF --src ip-address
 
* sudo su -c 'iptables-save  > /etc/iptables/rules.v4' # must be root...
* sudo su -c 'ip6tables-save > /etc/iptables/rules.v6'

     sudo addtoblacklist.sh

* distrib.sh - scan the log files for the distribution of access of files in heavyusers.txt



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
