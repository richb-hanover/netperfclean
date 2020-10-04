#!/bin/bash
#
# listandblacklist.sh - find abusing ip addresses and blacklist them in iptables
# Run this periodically to keep the number of abusers down
# Current process is to scan the last two days' of kern.log files, and 
#   blacklist any addresses that appear more than 1000 times.
# This will detect devices doing 500 tests in a 24 to 48 hour period 
#   assuming five up and five down streams per test.
#

/home/richb/src/kernlogscan/findunfilteredips.sh 500

/home/richb/src/kernlogscan/addtoblacklist.sh
