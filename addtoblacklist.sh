#!/bin/bash 
#
# Blacklist the IP addresses from the file filteredheavyusers.txt in iptables
# Then empty out the filteredheavyusers.txt file so that we don't accidently get duplicates
#
 
cd /home/richb/src/kernlogscan

while read in; do

     /sbin/iptables -I INPUT 5 -p tcp --dport 12865 -j DROPPEDNETPERF --src "$in";

done < filteredheavyusers.txt

# shuffle filteredheavyusers.txt out of the way
mv filteredheavyusers.txt previousheavyusers.txt
touch filteredheavyusers.txt

# and save the iptables config over reboots...

su -c 'iptables-save  > /etc/iptables/rules.v4' # must be root...
su -c 'ip6tables-save > /etc/iptables/rules.v6'

# And commit the newest iptables.txt (but as user 'richb', not root)

# su richb -c 'git add iptables.txt'
# su richb -c 'git commit -m "Update iptables.txt"'
