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
DATECOLUMN = 3
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

class myForm(Form):
    fasttext = StringField("fasttext",[validators.Length(min=0,max=100)])
    deeplearn = StringField("deeplearn",[validators.Length(min=0,max=100)])
    human = StringField("deeplearn",[validators.Length(min=0,max=100)])
    fields= StringField("fields",[validators.Length(min=0,max=100)])
    data = StringField("data",[validators.Length(min=0,max=100)])

app = Flask(__name__)
data, humanLabels = readData(DATAFILENAME)
humanLabels = readHumanLabels(humanLabels)

@app.route('/',methods=['GET','POST'])
def process():
    fasttext = ""
    deeplearn = ""
    human = ""
    selected = {}
    nbrOfSelected = 0
    form = myForm(request.form)
    if request.method == "POST" and form.validate():
        if form.fasttext.data != "": fasttext = form.fasttext.data
        if form.deeplearn.data != "": deeplearn = form.deeplearn.data
        if form.human.data != "": human = form.human.data
        if form.fields.data != "":
            for i in range(0,len(fieldsNames)):
                if fieldsNames[i] == form.fields.data:
                    if fieldsShow[i]: fieldsShow[i] = False
                    else: fieldsShow[i] = True
        if form.data.data != "":
            fields = form.data.data.split()
            index = int(fields.pop(0))
            label = " ".join(fields)
            humanLabels[index] = label
            storeHumanLabel(index,form.data.data)
    for d in range(0,len(data)):
        if ((fasttext == "" or fasttext == labels[data[d][0]] or
             (fasttext == "SAMEDEEP" and labels[data[d][0]] == labels[data[d][1]]) or
             (fasttext == "DIFFDEEP" and labels[data[d][0]] != labels[data[d][1]])) and
             (deeplearn == "" or deeplearn == labels[data[d][1]] or
              (deeplearn == "SAMEFAST" and labels[data[d][1]] == labels[data[d][0]]) or
              (deeplearn == "DIFFFAST" and labels[data[d][1]] != labels[data[d][0]])) and
             (human == "" or human == labels[data[d][2]])):
            if nbrOfSelected < MAXSHOW: selected[d] = True 
            nbrOfSelected += 1
    return(render_template('template.html', data=data, labels=labels, fieldsShow=fieldsShow , fieldsNames=fieldsNames, fasttext=fasttext, deeplearn=deeplearn, human=human, selected=selected, nbrOfSelected=nbrOfSelected, humanLabels=humanLabels))

