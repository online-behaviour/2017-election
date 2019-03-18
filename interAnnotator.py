#!/usr/bin/env python3
"""
    interAnnotator.py: get interannotator agreement data from annotations file
    usage: python interAnnotator.py < data/human-labels.txt
    20190318 erikt(at)xs4all.nl
"""

import csv
import re
import sys

COMMAND = sys.argv.pop(0)
FIRSTID = 0
LASTID = 299
NONE = "NONE"
TWEETID = "tweetid"
TWEETTEXT = "tweettext"
TWEETFILE = "data/2017-tweets.csv"
TWEETIDID = 4
TWEETTEXTID = 7

def readTweets(inFileName):
    inFile = open(inFileName,"r")
    csvreader = csv.reader(inFile)
    tweets = []
    for row in csvreader:
        try:
            tweets.append({TWEETID:row[TWEETIDID],TWEETTEXT:row[TWEETTEXTID]})
        except Exception as e:
            sys.exit(COMMAND+": problem with tweet file line: "+str(row)+": "+str(e))
    inFile.close()
    return(tweets)

def replaceSpaceInLabel(line):
    line = re.sub(" C "," C_",line)
    line = re.sub(" VOTE "," VOTE_",line)
    return(line)

def readData():
    data = {}
    for line in sys.stdin:
        try:
            line.strip()
            line = replaceSpaceInLabel(line)
            fields = line.split()
            if len(fields) == 3: fields.append("")
            user,date,corpusId,label = fields
            label.strip()
            corpusId = int(corpusId)
            if FIRSTID <= corpusId <= LASTID:
                if not corpusId in data: data[corpusId] = {}
                data[corpusId][user] = label
        except Exception as e:
            sys.exit(COMMAND+": problem with input line: "+line+": "+str(e))
    return(data)

def getAnnotators(data):
    annotators = []
    for tweetId in data: annotators.extend(list(data[tweetId].keys()))
    return(sorted(list(set(annotators))))

def printData(data,tweets):
    annotators = getAnnotators(data)
    fieldNames = annotators+[TWEETID,TWEETTEXT]
    csvwriter = csv.DictWriter(sys.stdout,fieldnames=fieldNames)
    csvwriter.writeheader()
    for corpusId in sorted(data.keys()):
        row = {TWEETID:tweets[corpusId][TWEETID],TWEETTEXT:tweets[corpusId][TWEETTEXT]}
        for annotator in annotators:
            if annotator in data[corpusId]: row[annotator] = data[corpusId][annotator]
            else: row[annotator] = NONE
        csvwriter.writerow(row)

def main(argv):
    tweets = readTweets(TWEETFILE)
    data = readData()
    printData(data,tweets)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
