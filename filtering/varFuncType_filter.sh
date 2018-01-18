#!/bin/bash
# ============================================================================
# Filters an .output file using variant function types (VFT)
#
# Input   $1 - .output (tsv) file to be filtered
#         $2 - path to the output .output file
# Output: .output file with only rows with the filtered-for genes
# ============================================================================

#Set up variables
VAR_FILE=$1
VFT_FILE="helper_files/var_func_types.txt"
OUTPUT_PATH=$2

#Iterate over the output list line by line from the second line
IFS=$'\n'       # make newlines the only separator
set -f          # disable globbing
for row in $(cat < "$VAR_FILE"); do
  #Skip the first row, if present
  if [ "`echo $row | cut -d$'\t' -f 1`" = "Family ID" ] ; then
    continue
  fi

  #Get the first variant function type (VFT)
  cur_vft=`echo $row | cut -d$'\t' -f 8 | cut -d'|' -f 1`

  #Exception handing: in case the VFT cell is blank, skip row
  if [ -z "$cur_vft" ] ; then
    continue
  fi

  #See if the current VFT is in the VFT file
  grep -q -x $cur_vft $VFT_FILE
  grep_status=$?

  #If the VFT is present, save the line to the output file
  if [ $grep_status -eq 0 ] ; then
    echo $row >> $OUTPUT_PATH
  fi

done

echo "Done!"
