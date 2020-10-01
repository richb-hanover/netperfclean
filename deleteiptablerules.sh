#!/bin/bash
# 
# Delete a set of rules from an iptables chain
#
# Usage: sudo bash deleteiptablesrules.sh <chain> <first_rule> <last_rule>
#  e.g.: sudo bash deleteiptablesrules.sh INPUT 5 10 # deletes rules 5 through 10 from INPUT chain
#
# Stole idea from: https://forums.centos.org/viewtopic.php?t=9202
#

if [[  $# -ne 3 ]]; then
   echo "Usage: deleteiptablesrules.sh {CHAIN} {starting rule number} {ending rule number}";
   exit 1;
fi;

for (( i=$3; i>=$2; i-- ))
do
  #  echo $1 $i
  sudo iptables -D $1 $i;
done

# and save the iptables config over reboots...
sudo su -c 'iptables-save  > /etc/iptables/rules.v4' # must be root...
sudo su -c 'ip6tables-save > /etc/iptables/rules.v6'
