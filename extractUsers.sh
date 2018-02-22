#!/bin/bash
# run.sh: get tweet files from hadoop and extract tweets from certain users
# usage: run.sh
# 20180219 erikt(at)xs4all.nl

TMPFILE=run.sh.$$.$RANDOM

Y=2017
M=03
for D in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15
do
   for H in 00 01 02 03 04 05 06 07 08 09 \
            10 11 12 13 14 15 16 17 18 19 \
            20 21 22 23
   do
      hadoop fs -cat twitter/$Y/$M/$D/$Y$M$D-$H.out.gz | gunzip -c > $TMPFILE
      ./extractUsers.py users.txt < $TMPFILE
      rm -f $TMPFILE
   done
done

M=02
for D in 15 16 17 18 19 20 21 22 23 24 25 26 27 28
do
   for H in 00 01 02 03 04 05 06 07 08 09 \
            10 11 12 13 14 15 16 17 18 19 \
            20 21 22 23
   do
      hadoop fs -cat twitter/$Y/$M/$D/$Y$M$D-$H.out.gz | gunzip -c > $TMPFILE
      ./extractUsers.py users.txt < $TMPFILE
      rm -f $TMPFILE
   done
done

exit 0
