'''
Look for constant users

Scan a day's /var/log/kern.log file and measure timing for each connection received

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
from collections import OrderedDict

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
hhmm - return "hh:mm" from a number of seconds
'''
def hhmm(secs):
    hh = int(secs/3600)
    return '%02d:%02d' % (hh, (secs-hh*3600)/60 )


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
        parser.add_argument("-e", '--errfile', nargs='?', type=argparse.FileType('w'), default=sys.stderr)
        # parser.add_argument("--notables", action="store_false", help="Don't print the tables")
        theArgs = parser.parse_args()
    except Exception, err:
        return str(err)

    fi = theArgs.infile                      # the argument parsing returns open file objects
    fo = theArgs.outfile
    fe = theArgs.errfile

    logfile = KernLogFile(fi)
    adrsDict = dict()

    while True:
        # line = f.readline()
        measurements = logfile.readTodayLine()
        if measurements == [] :       # EOF
            break

        connTime = measurements[0]
        ipAdrs = measurements[1]
        # print connTime, ipAdrs, type(ipAdrs)
        if adrsDict.has_key(ipAdrs):
            interval = connTime - adrsDict[ipAdrs]["prevTime"]
            adrsDict[ipAdrs]["prevTime"] = connTime
            adrsDict[ipAdrs]["duration"] = connTime - adrsDict[ipAdrs]["firstTime"]
            if interval > adrsDict[ipAdrs]["maxInterval"]:
                adrsDict[ipAdrs]["maxInterval"] = interval
            adrsDict[ipAdrs]["count"] += 1

        else:
            adrsDict[ipAdrs] = {
                "firstTime":connTime,
                "prevTime": connTime,
                "maxInterval":0,
                "count": 1,
                "duration":0
                }
        # print adrsDict[ipAdrs]

    # Thanks SO: https://stackoverflow.com/questions/16412563/python-sorting-dictionary-of-dictionaries
    abusers = sorted(adrsDict.items(), key=lambda x: x[1]['maxInterval'], reverse=True)
    print >> fe, "IP Address\tCount\tMax Interval\tTotal Duration"


    # print abusers[0][0]
    # print abusers[0][1]

    count = 0
    for item in abusers:
        if item[1]["count"] <= 20:          # skip addresses making <= 20 tests
            continue
        if item[1]["duration"] <= 21*60*60: # skip addresses whose tests span fewer than 21 hours
            continue
        if item[1]["maxInterval"] > 7*60*60: # skip addresses where there's > 7 hours between the test
            continue
        print >> fo, "%s" % item[0]
        print >> fe, "%s\t%d\t%s\t%s" % (item[0],item[1]["count"],hhmm(item[1]["maxInterval"]),hhmm(item[1]["duration"]))
        count += 1

    print >> fe, "Total addresses listed: %d" % count

if __name__ == "__main__":
    sys.exit(main())


