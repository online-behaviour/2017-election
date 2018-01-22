#!/usr/bin/bash
# fasttext.bash: run experiment with fasttext
# usage: fasttext.bash [ -w ]
# 20180118 erikt(at)xs4all.nl

FASTTEXTDIR=$HOME/software/fastText
FASTTEXT=$FASTTEXTDIR/fasttext
WIKIVEC=$FASTTEXTDIR/wiki.nl.vec
EVAL=$HOME/projects/online-behaviour/machine-learning/eval.py
TRAIN=TRAIN-TEST.fasttext
TEST=TEST.fasttext
TMPFILE=fasttext.bash.$$.$RANDOM
MODEL=$TMPFILE.model
DIM=300
MINCOUNT=5
USEWIKIVEC=""

while getopts ":T:t:w" opt; do
   case $opt in
   T) TRAIN=$OPTARG
      ;;
   t) TEST=$OPTARG
      ;;
   w) USEWIKIVEC=1
      ;;
   \?) echo $COMMAND ": invalid option " $opt
      ;;
   esac
done

if [ "$USEWIKIVEC" != "" ]
then
   $FASTTEXT supervised -input $TRAIN -output $MODEL -dim $DIM \
      -minCount $MINCOUNT -pretrainedVectors $WIKIVEC > /dev/null 2> /dev/null
else
   $FASTTEXT supervised -input $TRAIN -output $MODEL -dim $DIM \
      -minCount $MINCOUNT > /dev/null 2> /dev/null
fi
$FASTTEXT predict $MODEL.bin $TEST | tee $TEST.labels |\
   paste -d' ' - $TEST | cut -d' ' -f1,2 |\
   sed 's/^\(.*\) \(.*\)$/\2 \1/' | $EVAL
rm -f $MODEL.bin

exit 0
