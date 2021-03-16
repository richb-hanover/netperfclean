#!/bin/bash
#
# listandblacklist.sh - find abusing ip addresses and blacklist them in iptables
# Run this periodically to keep the number of abusers down
# Current process is to scan the last two days' of kern.log files, and 
#   blacklist any addresses that appear more than the specified number of tests.
# This will check a 24 to 48 hour period assuming five up and five down streams per test.
#

/home/deploy/src/netperfclean/findunfilteredips.sh 350

/home/deploy/src/netperfclean/addtoblacklist.sh
