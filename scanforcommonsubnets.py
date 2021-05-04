'''
Scan For Common Subnets:

Read a sorted list of IP addresses currently being blocked by iptables.
Output a list of subnets containing more than N consecutive addresses in a /16 or /24 subnet.

'''

import sys
import argparse
import re
from string import atoi
import os
# from collections import OrderedDict

"""
readTodayLine(f)

Reads a line from the input file and returns the IP address and its connection time (in seconds)
Only returns lines from "today" where the connection time is >= previous connection time.
(Otherwise, it returns "" to signal EOF)

"""
class KernLogFile:

    def __init__(self, file):
        self.prevConnTime = 0
        self.theFile = file

    def readTodayLine(self):
        line = self.theFile.readline()
        if line == "":
            return []
        secString = re.findall("[ ]\d\d:\d\d:\d\d[ ]",line)[0]
        ipAdrs = re.findall("SRC=(.*?)[ ]" ,line)[0]

        [hh,mm,ss] = secString.split(":")

        connTime = 3600*int(hh) + 60*int(mm) + int(ss)
        if connTime < self.prevConnTime:
            return []                       # got into next day's data - treat as EOF
        self.prevConnTime = connTime

        return [connTime,ipAdrs]
        
'''
hhmm - format number of seconds as "hh:mm"
'''
def hhmm(secs):
    roundedsecs = secs+30
    hh = int(roundedsecs/3600)
    return '%02d:%02d' % (hh, (roundedsecs-hh*3600)/60 )


'''
Main Function

Parse arguments
Scan through file
Build up dictionary for each IP address
Uses argparse for variables (https://docs.python.org/3/library/argparse.html)
   and https://docs.python.org/3/howto/argparse.html#id1

'''
def main(argv=None):

    try:
        parser = argparse.ArgumentParser(description=__doc__) # print the global document string
        parser.add_argument("-i", '--infile', nargs='?', type=argparse.FileType('rU'), default=sys.stdin)
        parser.add_argument("-o", '--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
        parser.add_argument("-e", '--errfile', nargs='?', type=argparse.FileType('w'), default=sys.stderr)
        parser.add_argument("-t", "--threshold", nargs='?', type=int, default=4, help="Threshold for consecutive addresses")
        theArgs = parser.parse_args()
    except Exception, err:
        return str(err)

    fi = theArgs.infile                      # the argument parsing returns open file objects
    fo = theArgs.outfile
    fe = theArgs.errfile

    # stat = os.stat(fi)

    print ("Threshold: %d"%(theArgs.threshold))
    
    subnetMasks = [
        0x0ffffffff,  # 0
        0x0ffffffff,  # 1
        0x0ffffffff,  # 2
        0x0ffffffff,  # 3
        0x0ffffffff,  # 4
        0x0ffffffff,  # 5
        0x0ffffffff,  # 6
        0x0ffffffff,  # 7
        0x0ffffffff,  # 8
        0x0ffffffff,  # 9
        0x0ffffffff,  # 10
        0x0ffffffff,  # 11
        0x0ffffffff,  # 12
        0x0ffffffff,  # 13
        0x0ffffffff,  # 14
        0x0ffffffff,  # 15
        0x00000ffff,  # 16
        0x000007fff,  # 17
        0x000003fff,  # 18
        0x000001fff,  # 19
        0x000000fff,  # 20
        0x0000007ff,  # 21
        0x0000003ff,  # 22
        0x0000001ff,  # 23
        0x0000000ff,  # 24
    ]

    count = 0
    sn8 = 0
    sn16 = 0
    sn24 = 0
    prev0 = ""
    prev1 = ""
    prev2 = ""
    previp = 0
    while True:
        line = fi.readline().strip()
        if line == "":
            break

        quads = line.split(".")

        ip = ((atoi(quads[0])*256 + atoi(quads[1]))*256+atoi(quads[2]))*256+atoi(quads[3])

        print >> fo, "%s: %d %d" % (quads, ip, ip-previp)
        previp = ip

        # if count == 0:
        #     prev0 = quads[0]
        #     prev1 = quads[1]
        #     prev2 = quads[2]
        #
        # if (prev0 == quads[0] and prev1 == quads[1] and prev2 == quads[2]):
        #     sn24 += 1
        # else:
        #     if sn24 >= theArgs.threshold:
        #         print >> fo, "%s.%s.%s.0 %d" % (prev0,prev1,prev2, sn24)
        #     prev0 = quads[0]
        #     prev1 = quads[1]
        #     prev2 = quads[2]
        #     sn24 = 0

        count += 1

    # if sn24 > theArgs.threshold:
    #     print >> fo, "%s.%s.%s.0 %d" % (prev0, prev1, prev2, sn24)

    print >> fo, "Count: %d" % count


if __name__ == "__main__":
    sys.exit(main())


