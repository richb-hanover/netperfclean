# To-Do's

- Switch to new iptables scheme 
	- port 12865 -> NETPERF chain so that other connections aren't slowed by search
	- NETPERF chain has default "Incoming netperf" log rule
	- NETPERF gets blacklisted addresses that -J LIMITEDNETPERF
	- LIMITEDNETPERF rejects packets, maybe allows only 2pkts/sec for each connections

- Factor findfilteredips.sh into:
	- findheavyips.sh - scans kern.log files to find heavy users --> heavyusers.txt
	- findnewips.sh - scan heavyusers.txt and find addresses not already in iptables
		write to newheavyusers.txt
	- (addtoblacklist.sh) reads newheavyusers.txt to add to the right place in iptables