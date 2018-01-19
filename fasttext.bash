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
if [ "$1" == "-s" ]
then
   TEST=selected.fasttext
   shift
fi
TMPFILE=fasttext.bash.$$.$RANDOM
MODEL=$TMPFILE.model
DIM=300
MINCOUNT=5

if [ "$1" == "-w" ]
then
   $FASTTEXT supervised -input $TRAIN -output $MODEL -dim $DIM \
      -minCount $MINCOUNT -pretrainedVectors $WIKIVEC > /dev/null 2> /dev/null
else
   $FASTTEXT supervised -input $TRAIN -output $MODEL -dim $DIM \
      -minCount $MINCOUNT > /dev/null 2> /dev/null
fi
$FASTTEXT predict $MODEL.bin $TEST | tee $TEST.labels |\
   paste -d' ' - $TEST | cut -d' ' -f1,2 | rev | $EVAL
rm -f $MODEL.bin

exit 0
