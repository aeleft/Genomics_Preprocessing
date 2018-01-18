#!/bin/bash
# ============================================================================
# Filters an .output file using coding variant types
#
# Input   $1 - .output (tsv) file to be filtered
#         $2 - path to the output .output file
# Output: .output file with only rows with the filtered-for genes
#
# Note:
#	- If the coding variant type is blank, it passes the filter (is written)
# ============================================================================

#Set up variables
VAR_FILE=$1
CVT_FILE="helper_files/coding_var_types.txt"
OUTPUT_PATH=$2

#Iterate over the output list line by line from the second line
IFS=$'\n'       # make newlines the only separator
set -f          # disable globbing
for row in $(cat < "$VAR_FILE"); do
  #Skip the first row, if present
  if [ "`echo $row | cut -d$'\t' -f 1`" = "Family ID" ] ; then
    continue
  fi

  #Get the first coding variatn type (CVT)
  cur_cvt=`echo $row | cut -d$'\t' -f 9 | cut -d'|' -f 1`

  #Exception handling: if the CVT variable is blank, write row!
  if [ -z "$cur_cvt" ] ; then
    echo $row >> $OUTPUT_PATH ;
    continue
  fi

  #See if the current CVT is in the CVT file
  grep -q -x $cur_cvt $CVT_FILE
  grep_status=$?

  #If the CVT is present, save the line to the output file
  if [ $grep_status -eq 0 ] ; then
    echo $row >> $OUTPUT_PATH
  fi
done

echo "Done!"
