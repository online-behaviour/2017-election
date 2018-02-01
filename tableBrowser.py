#!/usr/bin/python2 -W all
# tableBrowser: browse csv table with labeled tweets
# usage: FLASK_APP=$PWD/tableBrowser.py; flask run
# 20180124 erikt(at)xs4all.nl

from flask import Flask
from flask import render_template
from flask import request
from wtforms import Form, StringField, SelectField, PasswordField, validators
import csv
import re
import sys

MAXSHOW = 10
DATAFILENAME = "data/2017-tweets.csv"
HUMANLABELFILE = "data/human-labels.txt"
LOGFILE = "data/logfile"
DATECOLUMN = 3
BORDERPAGES = 2
UNKNOWN = ""
labels = {"0":"ERROR","1":"C TRAIL","2":"PROMOTION","3":"C ACTION",
        "4":"VOTE CALL","5":"NEWS","6":"STANCE","7":"CRITIQUE",8:"INPUT",
        "9":"ADVICE", "10":"ACKNOWL","11":"PERSONAL","12":"OTHER","13":"ERROR" }
# human, fasttext, deeplearn, id, date, user, tweet
fieldsShow = [True,True,True,False,False,False,True]
fieldsNames = ["Human","FastText","DeepLearn","Id","Date","User","Tweet"]
nbrOfItems = 0

def readData(inFileName):
    data = []
    humanLabels = []
    inFile = open(inFileName,"r")
    csvreader = csv.reader(inFile,delimiter=',',quotechar='"')
    lineNbr = 0
    for row in csvreader:
        lineNbr += 1
        row[DATECOLUMN] = re.sub("^....","",row[DATECOLUMN])
        row[DATECOLUMN] = re.sub("...........$","",row[DATECOLUMN])
        data.append(row)
        humanLabels.append(UNKNOWN)
    inFile.close()
    return(data,humanLabels)

def readHumanLabels(humanLabels):
    inFile = open(HUMANLABELFILE,"r")
    for line in inFile:
        fields = line.split()
        index = int(fields.pop(0))
        label = " ".join(fields)
        humanLabels[index] = label
    return(humanLabels)

def storeHumanLabel(index,label):
    outFile = open(HUMANLABELFILE,"a")
    outFile.write(str(index)+" "+label+"\n")
    outFile.close()
    return()

def log(message):
    outFile = open(LOGFILE,"a")
    outFile.write(message+"\n")
    outFile.close()
    return()

def computePageBoundaries(nbrOfSelected,page):
    minPage = page-BORDERPAGES
    maxPage = page+BORDERPAGES
    lastPage = 1+int((nbrOfSelected-1)/MAXSHOW)
    if minPage < 1: 
        maxPage = maxPage+(1-minPage)
        minPage = 1
    if maxPage > lastPage:
        minPage = minPage-(maxPage-lastPage)
        maxPage = lastPage
    if minPage < 1 :
        minPage = 1
    return(minPage,maxPage)

app = Flask(__name__)
data, humanLabels = readData(DATAFILENAME)
humanLabels = readHumanLabels(humanLabels)

@app.route('/',methods=['GET','POST'])
def process():
    fasttext = ""
    deeplearn = ""
    human = ""
    page = 1
    selected = {}
    nbrOfSelected = 0
    form = request.form
    if request.method == "GET": # and form.validate():
        if "page" in request.args: page = int(request.args["page"])
        if "fasttext" in request.args: fasttext = request.args["fasttext"]
        if "deeplearn" in request.args: deeplearn = request.args["deeplearn"]
        if "human" in request.args: human = request.args["human"]
    if request.method == "POST": # and form.validate():
        if form["fasttext"] != "": fasttext = form["fasttext"]
        if form["deeplearn"] != "": deeplearn = form["deeplearn"]
        if form["human"] != "": human = form["human"]
        log("postcheck 1 "+fasttext)
        if form["fields"] != "":
            for i in range(0,len(fieldsNames)):
                if fieldsNames[i] == form["fields"]:
                    if fieldsShow[i]: fieldsShow[i] = False
                    else: fieldsShow[i] = True
        log("postcheck 2 "+fasttext)
        for i in range(1,MAXSHOW+1):
            key = "data"+str(i)
            if key in form and form[key] != "":
                fields = form[key].split()
                index = int(fields.pop(0))
                label = " ".join(fields)
                if humanLabels[index] != label:
                    humanLabels[index] = label
                    storeHumanLabel(index,label)
        log("postcheck 3 "+fasttext)
    for d in range(0,len(data)):
        if ((fasttext == "" or fasttext == labels[data[d][0]] or
             (fasttext == "SAMEDEEP" and labels[data[d][0]] == labels[data[d][1]]) or
             (fasttext == "DIFFDEEP" and labels[data[d][0]] != labels[data[d][1]])) and
             (deeplearn == "" or deeplearn == labels[data[d][1]] or
              (deeplearn == "SAMEFAST" and labels[data[d][1]] == labels[data[d][0]]) or
              (deeplearn == "DIFFFAST" and labels[data[d][1]] != labels[data[d][0]])) and
             (human == "" or human == humanLabels[d])):
            if nbrOfSelected >= MAXSHOW*(page-1) and \
               nbrOfSelected < MAXSHOW*page: selected[d] = True 
            nbrOfSelected += 1
    log("postcheck 4 "+fasttext)
    minPage, maxPage = computePageBoundaries(nbrOfSelected,page)
    log("postcheck 5 "+fasttext)
    return(render_template('template.html', data=data, labels=labels, fieldsShow=fieldsShow , fieldsNames=fieldsNames, fasttext=fasttext, deeplearn=deeplearn, human=human, selected=selected, nbrOfSelected=nbrOfSelected, humanLabels=humanLabels, page=page, minPage=minPage, maxPage=maxPage))

