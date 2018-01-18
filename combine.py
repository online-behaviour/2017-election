#!/usr/bin/python3 -W all
"""
    combine: combine results of different machine learners
    usage: combine -T train-file [ -t test-file] [-m]
    note: expected input line format: gold-label label-1 label-2 ...
    20180118 erikt(at)xs4all.nl
"""

import getopt
import sys

COMMAND = sys.argv[0]
USAGE = "usage: "+COMMAND+" -T train-file [ -t test-file ]"

def processOpts(argv):
    argv.pop(0)
    try: options = getopt.getopt(argv,"mT:t:",[])
    except: sys.exit(USAGE)
    printModel = ""
    trainFile = ""
    testFile = ""
    for option in options[0]:
        if option[0] == "-T": trainFile = option[1]
        elif option[0] == "-t": testFile = option[1]
        elif option[0] == "-m": printModel = True
    if trainFile == "": sys.exit(USAGE)
    return(trainFile,testFile,printModel)

def applyModel(inFileName,model):
    try: inFile = open(inFileName,"r")
    except: sys.exit(COMMAND+": cannot open file "+inFileName)
    nbrOfFields = -1
    lineCount = 0
    correctCount = []
    correct = 0
    for line in inFile:
        lineCount += 1
        line = line.rstrip()
        fields = line.split()
        if nbrOfFields < 0: nbrOfFields = len(fields)
        if len(fields) != nbrOfFields:
            sys.exit(COMMAND+": unexpected line "+line)
        goldLabel = fields.pop(0)
        for i in range(0,len(fields)):
            while len(correctCount) < i+1: correctCount.append(0)
            if fields[i] == goldLabel: correctCount[i] += 1
            bestSystem = ""
        bestCount = -1
        for i in range(0,len(correctCount)):
            if correctCount[i] > bestCount:
                bestCount = correctCount[i]
                bestSystem = i
        dataWithoutLabel = " ".join(fields)
        bestLabel = ""
        if dataWithoutLabel in model["exceptions"]: 
            bestLabel = model["exceptions"][dataWithoutLabel]
        else: bestLabel = fields[model["best system"]]
        if bestLabel == goldLabel: correct += 1
    print("# correct: {0:0.1f}%; best individual system: {1:0.1f}% (system {2})".format(100*correct/lineCount,100*bestCount/lineCount,bestSystem+1))
    inFile.close()
    return(0)

def makeModel(inFileName,printModel):
    nbrOfFields = -1
    correctCount = []
    dataWithLabels = {}
    dataWithoutLabels = {}
    labels = {}
    lineCount = 0
    try: inFile = open(inFileName,"r")
    except: sys.exit(COMMAND+": cannot open file "+inFileName)
    for line in inFile:
        lineCount += 1
        line = line.rstrip()
        fields = line.split()
        if nbrOfFields < 0: nbrOfFields = len(fields)
        if len(fields) != nbrOfFields: 
            sys.exit(COMMAND+": unexpected line "+line)
        goldLabel = fields.pop(0)
        for i in range(0,len(fields)):
            while len(correctCount) < i+1: correctCount.append(0)
            if fields[i] == goldLabel: correctCount[i] += 1
        if not line in dataWithLabels: dataWithLabels[line] = 1
        else: dataWithLabels[line] += 1 
        dataWithoutLabel = " ".join(fields)
        dataWithoutLabels[dataWithoutLabel] = 1
        labels[goldLabel] = 1
    inFile.close()
    bestSystem = ""
    bestCount = -1
    for i in range(0,len(correctCount)):
        if correctCount[i] > bestCount:
            bestCount = correctCount[i]
            bestSystem = i
    print("# best system: {0} ({1:0.1f}%)".format(bestSystem+1,100*bestCount/lineCount))
    exceptions = {}
    for dataWithoutLabel in dataWithoutLabels:
        bestLabel = "???"
        bestCount = -1
        for label in labels:
            key = label+" "+dataWithoutLabel
            if key in dataWithLabels and dataWithLabels[key] > bestCount:
                bestCount = dataWithLabels[key]
                bestLabel = label
        systemLabels = dataWithoutLabel.split()
        if systemLabels[bestSystem] != bestLabel and bestCount >= 5:
            exceptions[dataWithoutLabel] = bestLabel
            if printModel: print("{0} {1} {2}".format(bestCount,bestLabel,dataWithoutLabel))
    return({"best system":bestSystem,"exceptions":exceptions})

def main(argv):
    trainFile, testFile, printModel = processOpts(argv)
    model = makeModel(trainFile,printModel)
    if testFile != "": applyModel(testFile,model) 
    return(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))

