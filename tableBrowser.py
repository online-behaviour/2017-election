#!/usr/bin/python3 -W all
# tableBrowser: browse csv table with labeled tweets
# usage: FLASK_APP=$PWD/tableBrowser.py; flask run
# 20180124 erikt(at)xs4all.nl

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from wtforms import Form, StringField, SelectField, PasswordField, validators
import csv
import datetime
import hashlib
import re
import sys

# start site-dependent variables
URL = "http://145.100.58.119/cgi-bin/newsgac/"
BASEDIR = "/home/cloud/projects/online-behaviour/2017-election"
# end site-dependent variables
DATAFILENAME = BASEDIR+"/data/2017-tweets.csv"
HUMANLABELFILE = BASEDIR+"/data/human-labels.txt"
USERFILE = BASEDIR+"/data/users.txt"
LOGFILE = BASEDIR+"/data/logfile"
DATECOLUMN = 5
BORDERPAGES = 2
UNKNOWN = ""
labels = {"0":"ERROR","1":"C TRAIL","2":"PROMOTION","3":"C ACTION",
          "4":"VOTE CALL","5":"NEWS","6":"STANCE","7":"CRITIQUE",
          "8":"INPUT","9":"ADVICE", "10":"ACKNOWL","11":"PERSONAL",
          "12":"OTHER","13":"ERROR" }
fieldLabels = [ "Date", "DeepLearn", "DeepLearn+", "FastText", "FastText+", "Human", "Id", "Tweet", "User" ]
fieldsShow = { "Date":False, "DeepLearn":True, "DeepLearn+":False, "FastText":True, "FastText+":False, "Human":True, "Id":False, "Tweet":True, "User":False }
nbrOfItems = 0

def useFieldsStatus(fieldsStatus):
    fieldsShow = {}
    fieldsStatusInt = int(fieldsStatus)
    for label in reversed(fieldLabels):
        newFieldsStatusInt = int(fieldsStatusInt/2)
        if fieldsStatusInt > 2*newFieldsStatusInt: fieldsShow[label] = True
        else: fieldsShow[label] = False
        fieldsStatusInt = newFieldsStatusInt
    return(fieldsShow)

def getFieldsStatus(fieldsShow):
    fieldsStatus = 0
    for label in fieldLabels:
        fieldsStatus *= 2
        if fieldsShow[label]: fieldsStatus += 1
    return(fieldsStatus)

def readData(inFileName):
    data = []
    humanLabels = []
    inFile = open(inFileName,"r",encoding="utf-8")
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
    inFile = open(HUMANLABELFILE,"r",encoding="utf-8")
    for line in inFile:
        fields = line.rstrip().split()
        username = fields.pop(0)
        date = fields.pop(0)
        index = int(fields.pop(0))
        label = " ".join(fields)
        if "username" in session and username == session["username"]:
            humanLabels[index] = label
    inFile.close()
    return(humanLabels)

def readUsers():
    users = {}
    inFile = open(USERFILE,"r",encoding="utf-8")
    for line in inFile:
        fields = line.rstrip().split(":")
        username = fields.pop(0)
        password = fields.pop(0)
        users[username] = password
    inFile.close()
    return(users)

def storeHumanLabel(index,label,username):
    date = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
    outFile = open(HUMANLABELFILE,"a",encoding="utf-8")
    outFile.write(username+" "+date+" "+str(index)+" "+label+"\n")
    outFile.close()
    return()

def log(message):
    outFile = open(LOGFILE,"a",encoding="utf-8")
    outFile.write(message+"\n")
    outFile.close()
    return()

def computePageBoundaries(nbrOfSelected,page,pageSize):
    minPage = page-BORDERPAGES
    maxPage = page+BORDERPAGES
    lastPage = 1+int((nbrOfSelected-1)/pageSize)
    if minPage < 1: 
        maxPage = maxPage+(1-minPage)
        minPage = 1
    if maxPage > lastPage:
        minPage = minPage-(maxPage-lastPage)
        maxPage = lastPage
    if minPage < 1 :
        minPage = 1
    if page > lastPage: page = lastPage
    return(page,minPage,maxPage)

app = Flask(__name__)
data, humanLabels = readData(DATAFILENAME)

def encode(password):
    import random
    algorithm = "sh1"
    encoded = hashlib.sha1(password.encode("utf-8")).hexdigest()
    return(encoded)

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        formdata = request.form
        username = formdata["username"]
        password = formdata["password"]
        users = readUsers()
        if username in users and users[username] == encode(password):
            session["username"] = username
            return(redirect(URL))
        else: return(render_template("login.html", message="Incorrect user name or password"))
    else:
        return(render_template('login.html', message=""))

def select(fasttext,deeplearn,human,labelF,labelD,labelH):
    if ((fasttext == "" or fasttext == labelF or
         (fasttext == "SAMEDEEP" and labelF == labelD) or
         (fasttext == "DIFFDEEP" and labelF != labelD)) and
         (deeplearn == "" or deeplearn == labelD or
          (deeplearn == "SAMEFAST" and labelD == labelF) or
          (deeplearn == "DIFFFAST" and labelD != labelF)) and
         (human == "" or human == labelH)): return(True)
    else: return(False)

@app.route('/',methods=['GET','POST'])
def process():
    global fieldsShow,humanLabels

    if not "username" in session: return(redirect(URL+"login"))
    username = session["username"]
    fasttext = ""
    deeplearn = ""
    human = ""
    page = 1
    selected = {}
    nbrOfSelected = 0
    pageSize = 10
    formdata = {}
    changeFieldsStatus = ""
    humanLabels = readHumanLabels(humanLabels)
    fieldsStatus = getFieldsStatus(fieldsShow)
    if request.method == "GET": formdata = request.args
    elif request.method == "POST": formdata = request.form
    for key in formdata:
        if key == "fasttext": fasttext = formdata["fasttext"]
        elif key == "deeplearn": deeplearn = formdata["deeplearn"]
        elif key == "human": human = formdata["human"]
        elif key == "page" and formdata["page"] != "": 
            page = int(formdata["page"])
        elif key == "fields" and formdata["fields"] != "": 
            changeFieldsStatus = formdata["fields"]
        elif key == "fieldsStatus" and formdata["fieldsStatus"] != "": 
            fieldsStatus = formdata["fieldsStatus"]
            fieldsShow = useFieldsStatus(fieldsStatus)
        elif key == "size": pageSize = int(formdata["size"])
        elif key == "pageSize" and formdata["pageSize"] != "": pageSize = int(formdata["pageSize"])
        elif key == "logout":
            session.pop("username")
            return(redirect(URL))
        elif re.match("^data",key):
            if formdata[key] != "":
                fields = formdata[key].split()
                index = int(fields.pop(0))
                label = " ".join(fields)
                if humanLabels[index] != label:
                    humanLabels[index] = label
                    storeHumanLabel(index,label,username)
        else: pass # unknown key in formdata!
    if changeFieldsStatus != "":
        fieldsShow[changeFieldsStatus] = not fieldsShow[changeFieldsStatus]
        fieldsStatus = getFieldsStatus(fieldsShow)
    for d in range(0,len(data)):
        if select(fasttext,deeplearn,human,labels[data[d][0]],labels[data[d][1]],humanLabels[d]):
            nbrOfSelected += 1
    page, minPage, maxPage = computePageBoundaries(nbrOfSelected,page,pageSize)
    counter = 0
    for d in range(0,len(data)):
        if select(fasttext,deeplearn,human,labels[data[d][0]],labels[data[d][1]],humanLabels[d]):
            if counter >= pageSize*(page-1) and \
               counter < pageSize*page: selected[d] = True 
            counter += 1
    return(render_template('template.html', data=data, labels=labels, fieldsShow=fieldsShow , fasttext=fasttext, deeplearn=deeplearn, human=human, selected=selected, nbrOfSelected=nbrOfSelected, humanLabels=humanLabels, page=page, minPage=minPage, maxPage=maxPage, pageSize=pageSize, URL=URL, username=username, fieldsStatus=fieldsStatus))

app.secret_key = "PLEASEREPLACETHIS"
