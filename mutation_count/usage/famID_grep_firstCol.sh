#!/bin/bash
# ============================================================================
# Extract specific rows with matching first (family ID) column
#
# Input   $1 - file to be filtered
#         $2 - the keyword to be matched in the first column
#         $3 - path to the output file
#
# Output: filtered file that is a subset of the input
# ============================================================================

#Set up argument variables
IN_FILE=$1
WORD_2_MATCH=$2
OUT_PATH=$3


#Preserve the first row of the input file (assume it is the header)
echo "Writing new file: $OUT_PATH"
head -1 $IN_FILE > $OUT_PATH

#Grep for specific first column word
echo "Filtering..."
grep -E "^$WORD_2_MATCH" $IN_FILE >> $OUT_PATH

echo "Done!"
