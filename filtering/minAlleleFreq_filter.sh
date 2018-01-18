#!/bin/bash
# ============================================================================
# Filters for minor allele frequency to be in a certain range
#
# Input   $1 - .output (tsv) file to be filtered
#         $2 - path to the output .output file
#
# Output: .output file with only rows with the filtered-for genes
# ============================================================================

#Set up path variables
VAR_FILE=$1
OUTPUT_PATH=$2

#Set up range variables
LOWER_RANGE=0.00
UPPER_RANGE=0.01


#Iterate over the output list line by line from the second line
IFS=$'\n'       # make newlines the only separator
set -f          # disable globbing
for row in $(cat < "$VAR_FILE"); do
  #Skip the first row, if present
  if [ "`echo $row | cut -d$'\t' -f 1`" = "Family ID" ] ; then
    continue
  fi
  
  #Get the current minor allele frequency (MAF)
  cur_maf=`echo $row | cut -d$'\t' -f 20`

  #Exception handing: in case the cur_maf is empty, skip row!
  if [ -z "$cur_maf" ] ; then
    continue
  fi

  #Convert scientific notation to decimals
  semi_proper_maf=${cur_maf//e/E}
  printf -v proper_maf "%f" "$semi_proper_maf"

  #Check lower range and upper range
  lower_range_good=`(echo "$proper_maf >= $LOWER_RANGE" |bc -l)`
  upper_range_good=`(echo "$proper_maf <= $UPPER_RANGE" |bc -l)`

  #Check if both the lower and upper bound are good
  if (( $lower_range_good && $upper_range_good )); then
    #If so, write the whole row to an output file
    echo $row >> $OUTPUT_PATH
  fi

done

echo "Done!"
