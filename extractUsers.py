#!/usr/bin/python3 -W all
"""
    extractUsers.py: extract tweets from selected users from json file
    usage: extractUsers.py user-file < tweet-file.json
    note: user-file contains one user name (tweet handle) per line
    20180219 erikt(at)xs4all.nl
"""

import json
import sys

COMMAND = sys.argv.pop(0)
USAGE = COMMAND+" user-file < tweet-file.json"

def readUserNames(userFileName):
    userNames = {}
    try: userFile = open(userFileName,"r")
    except: sys.exit(COMMAND+": cannot open file "+userFileName)
    for line in userFile:
        userName = line.rstrip().lower()
        userNames[userName] = True
    userFile.close()
    return(userNames)

def main(argv):
    if len(argv) < 1: sys.exit(USAGE)
    userFileName = argv.pop(0)
    userNames = readUserNames(userFileName)
    for line in sys.stdin:
        line = line.rstrip()
        jsonLine = json.loads(line)
        userName = jsonLine["user"]["screen_name"].lower()
        if userName in userNames: print(line)
    return(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
