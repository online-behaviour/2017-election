#!/usr/bin/bash
# fasttext10cv.bash: run 10cv experiment with fasttext
# usage: fasttext10cv.bash [ -w ]
# 20180116 erikt(at)xs4all.nl

FASTTEXTDIR=$HOME/software/fastText
FASTTEXT=$FASTTEXTDIR/fasttext
WIKIVEC=$FASTTEXTDIR/wiki.nl.vec
BASETRAIN=TRAIN.fasttext
TMPFILE=fasttext10cv.bash.$$.$RANDOM
EVAL=$HOME/projects/online-behaviour/machine-learning/eval.py
TRAIN=$TMPFILE.train
MODEL=$TMPFILE.model
DIM=300
MINCOUNT=5
USEWIKIVEC=""

while getopts ":T:t:w" opt; do
   case $opt in
   T) BASETRAIN=$OPTARG
      ;;
   w) USEWIKIVEC=1
      ;;
   \?) echo $COMMAND ": invalid option " $opt
      ;;
   esac
done

for I in 0 1 2 3 4 5 6 7 8 9
do
   echo -e "\c" > $TRAIN
   for J in 0 1 2 3 4 5 6 7 8 9
   do
      if [ $I != $J ]; then cat $BASETRAIN.$J >>$TRAIN; fi
   done
   TEST=$BASETRAIN.$I
   if [ "$USEWIKIVEC" != "" ]
   then
      $FASTTEXT supervised -input $TRAIN -output $MODEL -dim $DIM \
         -minCount $MINCOUNT -pretrainedVectors $WIKIVEC > /dev/null 2> /dev/null
   else
      $FASTTEXT supervised -input $TRAIN -output $MODEL -dim $DIM \
         -minCount $MINCOUNT > /dev/null 2> /dev/null
   fi
   $FASTTEXT predict $MODEL.bin $TEST > $TEST.labels
   rm -f $TRAIN $MODEL.bin
done
cut -f1 -d' ' $BASETRAIN > $TMPFILE.gold
cat $BASETRAIN.?.labels | cut -d' ' -f1 | paste -d' ' $TMPFILE.gold - | $EVAL
rm -f $TMPFILE.gold

exit 0
