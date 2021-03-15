'''
Look for constant users

Scan a day's /var/log/kern.log file and measure timing for each connection

Real humans running real experiments take breaks.
Bots/automated tests don't

If there's a long break between bursts of tests, then it's probably a human

Procedure:

Scan the input file for IP address and time stamp (in seconds since start of day)
  Sample data: Mar 13 00:01:00 atl kernel: [39595063.153866] iptables: Incoming netperf IN=venet0 OUT= MAC= SRC=123.45.67.89 ...
Keep a dictionary of IP addresses recording for each:
- Count of that device's connections
- Time from that device's previous connection
- Max time between that device's connections

'''

import sys
import argparse
import re

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
            return []                       # EOF - got into next day's data
        self.prevConnTime = connTime

        return [connTime,ipAdrs]

'''
Main Function

Parse arguments
Scan through file
Build up dictionary for each IP address

'''
def main(argv=None):

    try:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("-i", '--infile', nargs='?', type=argparse.FileType('rU'), default=sys.stdin)
        parser.add_argument("-o", '--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
        # parser.add_argument("--notables", action="store_false", help="Don't print the tables")
        theArgs = parser.parse_args()
    except Exception, err:
        return str(err)

    f = theArgs.infile                      # the argument parsing returns open file objects
    fo = theArgs.outfile

    logfile = KernLogFile(f)
    colA = ""
    colC = ""
    count = 0
    while True:
        # line = f.readline()
        measurements = logfile.readTodayLine()
        if measurements == [] :       # EOF
            break
        else:
            count = count+1
            print measurements

    print ("Count: %s" % count)

if __name__ == "__main__":
    sys.exit(main())


