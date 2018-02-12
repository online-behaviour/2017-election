#!/usr/bin/python3 -W all
# to-encode.py: replace words by marking token
# usage: to-encode.py < file
# note: input file should be tokenized
# 20180205 erikt(at)xs4all.nl

import sys

words = { "to":True, "too":True, "two":True }
mask = "TO-MASK"
sameTag = "SAME"
contextSize = 5
filler = "FILLER"
labelPrefix = "__label__"

for line in sys.stdin:
    tokens = line.split()
    for i in range(0,len(tokens)):
        if tokens[i].lower() in words:
            if tokens[i].lower() in words: 
                outLine = labelPrefix+tokens[i].lower()
            else: outLine = labelPrefix+sameTag
            for j in range(contextSize,0,-1):
                if i-j < 0: outLine += " "+filler
                else: outLine += " "+tokens[i-j]
            if tokens[i].lower() in words: outLine += " "+mask
            else: outLine += " "+tokens[i].lower()
            for j in range(0,contextSize):
                if i+j+1 >= len(tokens): outLine += " "+filler
                else: outLine += " "+tokens[i+j+1]
            print(outLine)

sys.exit(0)
