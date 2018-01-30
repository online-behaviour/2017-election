#!/usr/bin/python3 -W all
# removeUsers.py: remove user information from json file with tweets
# usage: removeUsers.py < infile.json > outfile.json
# 20180130 erikt(at)xs4all.nl

import json
import re
import sys

def main(argv):
    patternHttp = re.compile("http\S+",flags=re.IGNORECASE)
    patternMail = re.compile("\S+@\S+")
    patternUser = re.compile("@\S+")

    for line in sys.stdin:
        try:
            jsonLine = json.loads(line)
            jsonLine["user"] = None
            jsonLine["text"] = patternHttp.sub("HTTP",jsonLine["text"])
            jsonLine["text"] = patternMail.sub("MAIL",jsonLine["text"])
            jsonLine["text"] = patternUser.sub("USER",jsonLine["text"])
            if "entities" in jsonLine: 
                jsonLine["entities"]["user_mentions"] = None
            print(json.dumps(jsonLine,sort_keys=True))
        except: pass

if __name__ == "__main__":
    sys.exit(main(sys.argv))
