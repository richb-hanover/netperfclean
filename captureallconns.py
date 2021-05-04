'''
Capture All Connections

Scan a day's /var/log/kern.log file and create a file of the form:

yyyy-mm-dd hh:mm:ss \t IP-address

This will go into a SQLite database for further analysis.

Run this once per day shortly after midnight on /var/log/kern.log.1
    to process yesterday's log file
'''

import sys
import argparse
import re
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

    stat = os.stat(fi)

    print (stat)

    logfile = KernLogFile(fi)
    # adrsDict = dict()

    # while True:
    #     # line = f.readline()
    #     measurements = logfile.readTodayLine()
    #     if measurements == [] :       # EOF
    #         break
    #
    #     connTime = measurements[0]
    #     ipAdrs = measurements[1]
    #     # print connTime, ipAdrs, type(ipAdrs)
    #     if adrsDict.has_key(ipAdrs):
    #         interval = connTime - adrsDict[ipAdrs]["prevTime"]
    #         adrsDict[ipAdrs]["prevTime"] = connTime
    #         adrsDict[ipAdrs]["duration"] = connTime - adrsDict[ipAdrs]["firstTime"]
    #         if interval > adrsDict[ipAdrs]["maxIdle"]:
    #             adrsDict[ipAdrs]["maxIdle"] = interval
    #         adrsDict[ipAdrs]["count"] += 1
    #
    #     else:
    #         adrsDict[ipAdrs] = {
    #             "firstTime":connTime,
    #             "prevTime": connTime,
    #             "maxIdle":0,
    #             "count": 1,
    #             "duration":0
    #             }
    #     # print adrsDict[ipAdrs]
    #
    # # Thanks SO: https://stackoverflow.com/questions/16412563/python-sorting-dictionary-of-dictionaries
    # abusers = sorted(adrsDict.items(), key=lambda x: x[1]['maxIdle'], reverse=True)
    # print >> fe, "IP Address\tCount\tFirst\tMax Idle\tTotal Duration\tDurOfTests\tRate\tReason"
    #
    # blacklistCount = 0
    # for item in abusers:
    #     theIP = item[0]
    #     first = item[1]["firstTime"]
    #     count = item[1]["count"]
    #     dur = item[1]["duration"]
    #     maxIdle = item[1]["maxIdle"]
    #     durOfTests = max (1,dur-maxIdle)
    #     rate = count / float(durOfTests)
    #
    #     report = "%s\t%d\t%s\t%s\t%s\t%d\t%1.2f\t" % (theIP, count, hhmm(first), hhmm(maxIdle), hhmm(dur), durOfTests, rate)
    #     print >> fe, report,
    #
    #     reason = "BLACKLIST"
    #     if count == 14:          # Many bots make 14 tests/day
    #         print >> fo, "%s" % theIP
    #         print >> fe, "BLACKLIST: 14 tests"
    #         blacklistCount += 1
    #         continue
    #     if count <= 20:         # skip addresses making <= 20 tests
    #         print >> fe, "ignore: < 20 tests"
    #         continue
    #     if rate > 0.5:          # blacklist addresses making connections too fast
    #         print >> fo, "%s" % theIP
    #         print >> fe, "BLACKLIST: high rate"
    #         blacklistCount += 1
    #         continue
    #     if dur <= 21*60*60:     # skip addresses whose tests span fewer than 21 hours
    #         print >> fe, "ignore: < 21 hours"
    #         continue
    #     if maxIdle > 7*60*60:   # skip addresses where there's > 7 hours between the test
    #         print >> fe, "ignore: break > 7 hours"
    #         continue
    #     else:                   # blacklist the remainder
    #         print >> fo, "%s" % theIP
    #         print >> fe, reason
    #         blacklistCount += 1
    #
    # print >> fe, "Total addresses blacklisted: %d" % blacklistCount

if __name__ == "__main__":
    sys.exit(main())


