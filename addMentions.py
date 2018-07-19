#!/usr/bin/python3
# addMentions.py: count mentions of known users in tweets
# usage: addMentions < 2017-tweets.csv
# 20180719 erikt(at)xs4all.nl

import csv
import nltk
import re
import sys

COMMAND = sys.argv[0]
ATSIGN = "@"
RETWEETTOKEN = "RT"
OUTPUTFIELDS = ["id","date","user","retweetUser","mentionCount","mentions","tweet"]
SEPARATOR = ","

def readFile():
    tweets = []
    users = {}
    csvreader = csv.reader(sys.stdin,delimiter=SEPARATOR)
    for row in csvreader:
        tweetId,date,user,tweet = row[4:8]
        tweets.append({"id":tweetId,"date":date,"user":user,"tweet":tweet})
        users[user.lower()] = True
    return(tweets,users)

def findMentions(tweets,users):
    mentions = []
    for tweet in tweets:
        mentionCount = 0
        mentioned = ""
        retweet = ""
        retweetSeen = False
        tokens = nltk.word_tokenize(tweet["tweet"])
        for i in range(0,len(tokens)):
            if tokens[i] == RETWEETTOKEN and not retweetSeen:
                retweetSeen = True
                if i < len(tokens)-2 and tokens[i+1] == ATSIGN \
                   and tokens[i+2].lower() in users:
                    retweet = tokens[i+2]
            if tokens[i] == ATSIGN and \
               (i < len(tokens)-1 and tokens[i+1].lower() in users):
                   if mentioned == "": mentioned = tokens[i+1]
                   else: mentioned += " "+tokens[i+1]
                   mentionCount += 1
        mentions.append({"retweetUser":retweet,"mentionCount":mentionCount,"mentions":mentioned})
    return(mentions)

def printData(tweets,mentions):
    csvwriter = csv.DictWriter(sys.stdout,delimiter=SEPARATOR,fieldnames=OUTPUTFIELDS)
    csvwriter.writeheader()
    for i in range(0,len(mentions)):
        data = dict(tweets[i])
        data.update(mentions[i])
        csvwriter.writerow(data)
    return()

def main(argv):
    tweets,users = readFile()
    mentions = findMentions(tweets,users)
    printData(tweets,mentions)

if __name__ == "__main__":
    sys.exit(main(sys.argv))

