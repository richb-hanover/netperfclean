# scan the iptables addresses for duplicates

uniq -c iptables-addresses.txt | sort -nr | \
tee junk.txt | \
# split off the count, and output lines with counts > 20000
awk 'BEGIN {
      result="";
    } \
    {
     if ($1 > 1) result=result$2"\n";
    }
    END {
     if (length(result) != 0) {
       print "Duplicate addresses found in iptables";
       print result;
       print "Use iptables -nL --line-numbers to find line numbers";
       print "Use iptables -D NETPERF # to remove";
       }
     } '

