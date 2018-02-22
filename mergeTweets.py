#!/usr/bin/python3 -W all
# mergeTweets.py: remove duplicate tweets from csv files
# usage: cat file1.csv file2.csv ... | ./mergeTweets.py
# note: expects sentence-initial tweet id
# 20180222 erikt(at)xs4all.nl

import re
import sys

seen = {}

lineNbr = 0
for line in sys.stdin:
    lineNbr += 1
    line = line.rstrip()
    id = re.sub(",.*","",line)
    if not re.match("^[0-9]+$",id): 
        sys.exit(COMMAND+": unknown id on line "+str(lineNbr)+": "+id)
    if not id in seen:
        print(line)
        seen[id] = True
