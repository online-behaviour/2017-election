#!/usr/bin/bash
# run.bash: run experiments
# usage: ./run.bash
# 20180115 erikt(at)xs4all.nl

FASTTEXT=$HOME/software/fastText/fasttext
TRAIN=TRAIN.fasttext
TEST=selected.fasttext
DIM=300
MINCOUNT=5
TMPFILE=run.$$.$RANDOM
MODEL=$TMPFILE.model
VECTORS=$TMPFILE.vectors

$FASTTEXT supervised -input $TRAIN -output $MODEL -dim $DIM \
    -minCount $MINCOUNT > /dev/null 2> /dev/null
$FASTTEXT predict $MODEL.bin $TEST > $TEST.labels
rm -f $MODEL.bin

exit 0
