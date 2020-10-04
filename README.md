# README for running a netperf server

It's easy to run a netperf server.
Just stand up a VPS,
[read the installation instructions and download the zip from https://github.com/HewlettPackard/netperf](https://github.com/HewlettPackard/netperf),
`make; make install`,
open port 12865 on the firewall,
and you're on the air.
BUT...

A netperf server (for example, at [netperf.bufferbloat.net](http://netperf.bufferbloat.net)) is an attractive nuisance.
A garden-variety VPS can easily handle the load generated by a handful of network researchers.
But it has grown popular with people who want to test their network connection every five minutes, 24x7.
This rapidly exhausts the bandwidth caps of (low-cost) hosting plans, leading to increased expense or suspension of the server.

This repository contains a number of tools for identifying and shutting down "abusers" who run bandwidth tests continually.
It does this by using `iptables` rules to identify traffic to port 12865 (the default netperf port), counting the connections, and blocking addresses that cross a threshold.

The current threshold is set at 5000 connections per 24-48 hour time 
interval.
This ballpark number was computed using the following factors: a normal "speed test" typically uses five simultaneous connections to "fill the pipe": first in the download phase then the upload phase.
Thus, a single speed test session creates 10 connections.
If the count exceeds the threshold (1000, or about 50 speed tests over a 
day or two), we stop accepting connections for that address.

## The Details

`iptables` is configured to log a message with a prefix of "Incoming netperf" each time a connection to port 12865 arrives.
Those log entries (written to `/var/log/kern.log`) have the form:

```
Feb 11 03:11:45 atl kernel: [9353834.165208] Incoming netperf IN=lo OUT= MAC=00:00:00:00:00:00:00:00:00:00:00:00:08:00 
SRC=23.x.x.x DST=23.x.x.x LEN=60 TOS=0x00 PREC=0x00 TTL=64 ID=38423 DF PROTO=TCP SPT=56374 DPT=12865 WINDOW=65535 RES=0x00 SYN 
URGP=0
```

The important scripts in this repo are:

* **listandblacklist.sh** runs via cron on a regular basis (several times per hour).
This script calls each of the following scripts in sequence:

* **findunfiltered.sh ###** scans the `/var/log/kern.log*` files for those "Incoming 
netperf" lines,
isolates the SRC=... addresses, and creates a frequency count of those addresses. It writes a list of IP addresses
that occur more than the threshold  
to the `heavyusers.txt` file.

   The script then compares those new addresses (in `heavyusers.txt`) to the list of IP addresses that are already present in iptables with a DROPPEDNETPERF target
and writes new addresses to `filteredheavyusers.txt`

* **addtoblacklist.sh** reads `filteredheavyusers.txt` to update the `iptables` rules by adding each address to the INPUT chain with a -j DROPPEDNETPERF target.
The DROPPEDNETPERF chain drops the packet (and thus the connection.) 

## iptables setup   

First, add a rule to the INPUT chain to log each arriving netperf connection.
The command below appends (-A) to the INPUT chain a rule so that a TCP packet on port 12865 jumps to the LOG chain with the prefix "Incoming netperf "

```
sudo iptables -A INPUT -p tcp --dport 12865 -j LOG --log-prefix "Incoming netperf "
```
Second, create a DROPPEDNETPERF chain to process packets that exceed the threshold.
Originally, this chain would log a "Dropped netperf" message (the second rule below), but it no longer does this.
That's because, under load, the logging messages for the high volume of dropped packets placed too much load on the server.
The commands to create the chain are:

```
sudo iptables -N DROPPEDNETPERF
# sudo iptables -A DROPPEDNETPERF -j LOG --log-prefix "Dropped netperf "
sudo iptables -A DROPPEDNETPERF -j DROP
```

Finally, the `addtoblacklist.sh` script adds an `iptables` rule to drop connections for the listed address:
insert (-I) a rule in the INPUT chain at position 3, with criteria for tcp and port 12865 and the specified source address.
A matching packet "jumps to" the DROPPEDNETPERF chain that subsequently drops the packet.
This prevents the connection from becoming established.

```
sudo iptables -I INPUT 3 -p tcp --dport 12865 -j DROPPEDNETPERF --src <ip-address>
```

The command above takes effect immediately.
If you wish the command to persist across reboots, you must use `iptables-save`, like this.
These commands must be run as root.

   ```
sudo su -c 'iptables-save  > /etc/iptables/rules.v4' 
sudo su -c 'ip6tables-save > /etc/iptables/rules.v6'
   ```
 
`iptables -nvL` displays counts of the number of packets and bytes processed by each of the `iptables` rules.

## Old info - not necessarily up-to-date

Description of other files:

   * `countsofip.txt` - file that shows IP address counts in the form: ### 192.168.1.1
   * `heavyusers.txt` - IPs of devices with > *threshold* connections from log files
   * `whitelist.txt` - a file of IP addresses never to blacklist
   * `filteredheavyusers.txt` - heavy users not present in iptables
   * `iptables-addresses.txt` - addresses with DROPPEDNETPERF as the target in iptables
   * `iptables.txt` - raw output of 'iptables -nL'
   * `kernlog.txt` - concatenated output of all log files
   * `sh checkdistrib.sh <ipaddress>` - a script to display the number of tests for each one-hour interval for a specified address.
This indicates whether the device was continually testing, or tested for a while, then stopped, then started again.
   * `logscan.sh` precursor to findunfilteredips.sh. It scans the kern.log* files, and
shows counts for "Incoming" and "Dropped" netperf connections.

