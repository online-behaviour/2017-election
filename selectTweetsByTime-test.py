#!/usr/bin/python3
"""
    selectTweetsByTime-test.py: test file for selectTweetsByTime.py
    usage: selectTweetsByTime-test.py
    20180115 erikt(at)xs4all.nl
"""

import io
import unittest
import selectTweetsByTime
import sys

BEFORE = '{ "created_at":"Tue Feb 28 23:59:59 +0000 2017" }'
START = '{ "created_at":"Wed Mar 01 00:00:00 +0000 2017" }'
END = '{ "created_at":"Wed Mar 15 23:59:59 +0000 2017" }'
AFTER = '{ "created_at":"Thu Mar 16 00:00:00 +0000 2017" }'

DATAIN = [ BEFORE, START, END, AFTER ]
DATAOUT = [ [], [START], [END], [] ]

class myTest(unittest.TestCase):
    def testReadFile(self):
        for i in range(0,len(DATAIN)):
            sys.stdin = io.StringIO(DATAIN[i])
            results = selectTweetsByTime.filter()
            self.assertEqual(results,DATAOUT[i])

if __name__ == '__main__':
    unittest.main()
