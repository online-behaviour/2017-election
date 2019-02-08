#!/usr/bin/env python3
"""
    addHumanLabels.py: add human labels to data file
    usage: addHumanLabels.py labelFile < dataFile > outFile
    20190206 erikt(at)xs4all.nl
"""

import csv
import sys

COMMAND = sys.argv.pop(0)
USAGE = "usage: "+COMMAND+" labelFile < dataFile > outFile "
OFFSET = 1
SEPARATOR = ","
INDEXID = 2
LABELID = 3
FASTTEXTID = 0
DEEPLEARNINGID = 1
TWEETIDID = 4
DATEID = 5
USERNAMEID = 6
TWEETTEXTID = 7
TWEETID = "tweetid"
USERID = "userid"
USERNAME = "username"
PARTY1 = "party1"
PARTY2 = "party2"
TEXT = "text"
DATE = "date"
UNKNOWN1 = "unknown1"
UNKNOWN2 = "unknown2"
UNKNOWN3 = "unknown3"
LABEL = "label"
FASTTEXT = "fasttext"
DEEPLEARNING = "deeplearning"
OUTPUTFIELDS = [TWEETID,USERID,USERNAME,PARTY1,TEXT,UNKNOWN1,PARTY2,UNKNOWN2,UNKNOWN3,LABEL,DATE,FASTTEXT,DEEPLEARNING]
LABELIDS = {"":"0","ERROR":"0","C TRAIL":"1","PROMOTION":"2",
            "C ACTION":"3","VOTE CALL":"4","NEWS":"5","STANCE":"6",
            "CRITIQUE":"7", "INPUT":"8","ADVICE":"9","ACKNOWL":"10",
            "PERSONAL":"11","OTHER":"12" }

def processData(labels):
    lineCounter = 0
    csvreader = csv.reader(sys.stdin,delimiter=SEPARATOR)
    csvwriter = csv.DictWriter(sys.stdout,delimiter=SEPARATOR,fieldnames=OUTPUTFIELDS)
    for row in csvreader:
        lineCounter += 1
        index = str(lineCounter)
        if index in labels:
            data = {LABEL:labels[index],TEXT:row[TWEETTEXTID],TWEETID:row[TWEETIDID],USERNAME:row[USERNAMEID],DATE:row[DATEID],FASTTEXT:row[FASTTEXTID],DEEPLEARNING:row[DEEPLEARNINGID]}
            csvwriter.writerow(data)

def readLabels(labelFileName):
    try: labelFile = open(labelFileName,"r")
    except Exception as e: 
        sys.exit(COMMAND+": cannot read file "+labelFileName+": "+str(e))
    labels = {}
    for line in labelFile:
        tokens = line.split()
        index = str(int(tokens[INDEXID])+OFFSET)
        labelName = " ".join(tokens[LABELID:])
        labels[index] = LABELIDS[labelName]
    return(labels)

def main(argv):
    try: labelFileName = argv.pop(0)
    except Exception as e: sys.exit(USAGE+str(e))
    labels = readLabels(labelFileName)
    processData(labels)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
