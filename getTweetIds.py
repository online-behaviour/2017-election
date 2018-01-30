#!/usr/bin/python3 -W all
# getTweetIds.py: extract tweet ids from json file with tweets
# usage: getTweetIds.py < file.json
# 20180130 erikt(at)xs4all.nl

import json
import sys

def main(argv):
    for line in sys.stdin:
        try:
            jsonLine = json.loads(line)
            tweetId = jsonLine["id_str"]
            print(tweetId)
        except: pass

if __name__ == "__main__":
    sys.exit(main(sys.argv))
