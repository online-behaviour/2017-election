#!/usr/bin/bash
# fasttext10cv.bash: run 10cv experiment with fasttext
# usage: fasttext10cv.bash
# 20180116 erikt(at)xs4all.nl

FASTTEXT=$HOME/software/fastText/fasttext
BASETRAIN=TRAIN.fasttext
TMPFILE=fasttext10cv.bash.$$.$RANDOM
TRAIN=$TMPFILE.train
MODEL=$TMPFILE.model
DIM=300
MINCOUNT=5

for I in 0 1 2 3 4 5 6 7 8 9
do
   echo -e "\c" > $TRAIN
   for J in 0 1 2 3 4 5 6 7 8 9
   do
      if [ $I != $J ]; then cat $BASETRAIN.$J >>$TRAIN; fi
   done
   TEST=$BASETRAIN.$I
   $FASTTEXT supervised -input $TRAIN -output $MODEL -dim $DIM \
      -minCount $MINCOUNT > /dev/null 2> /dev/null
   $FASTTEXT predict $MODEL.bin $TEST > $TEST.labels
   rm -f $TRAIN $MODEL.bin
done

exit 0
