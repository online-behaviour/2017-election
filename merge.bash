#!/usr/bin/bash
# merge.bash: merge category labels
# usage: merge.bash < file.fasttext
# 20180122 erikt(at)xs4all.nl

# keep labels 5, 11 and 12
sed 's/__label__[123] /__label__1+2+3 /' |\
   sed 's/__label__[67] /__label__6+7 /' |\
   sed 's/__label__[489] /__label__4+8+9+10 /' |\
   sed 's/__label__10 /__label__4+8+9+10 /' 

exit 0
