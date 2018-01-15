#!/usr/bin/python3
"""
    selectTweetsByTime.py: select tweets in a certain time interval
    usage: selectTweetsByTime.py < out.txt
    20180115 erikt(at)xs4all.nl
"""

from dateutil import parser
import json
import sys

STARTDATE = "2017-03-01 00:00:00+00:00"
ENDDATE = "2017-03-15 23:59:59+00:00"

def filter():
    startDate =  parser.parse(STARTDATE)
    endDate =  parser.parse(ENDDATE)
    lines = []
    for line in sys.stdin:
        line = line.rstrip()
        jsonLine = json.loads(line)
        date = parser.parse(jsonLine["created_at"])
        if date >= startDate and date <= endDate: lines.append(line)
    return(lines)

def main(argv):
    lines = filter()
    for l in range(0,len(lines)): print(lines[l])
    return(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
