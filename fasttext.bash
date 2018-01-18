#!/usr/bin/bash
# fasttext.bash: run experiment with fasttext
# usage: fasttext.bash
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

$FASTTEXT supervised -input $TRAIN -output $MODEL -dim $DIM \
   -minCount $MINCOUNT -pretrainedVectors $WIKIVEC > /dev/null 2> /dev/null
$FASTTEXT predict $MODEL.bin $TEST | paste -d' ' - $TEST |\
   cut -d' ' -f1,2 | rev | $EVAL
rm -f $MODEL.bin

exit 0
