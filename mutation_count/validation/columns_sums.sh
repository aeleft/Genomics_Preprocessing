#!/bin/bash
# ============================================================================
# Script takes in a .csv file and sum of each gene's mutation in the file.
#   The user decides the starting row and columns (see variables), after which
#   all ints are summed.
#
# Input   $1 - .csv file to sum
#
# Output: print-out of the sum of all mutations for each gene
# ============================================================================

#Command line variable - the input table file path
TABLE_FILE=$1

#The rows and columns to start summing from
START_ROW=2
START_COL=3


#Use awk to count and sum
awk -F, -v st_row="$START_ROW" -v st_col="$START_COL" '
    #Take the header information
    NR == 1{
      for (i=st_col; i<=NF; i++) h[i]=$i
    }

    # for every row, aggregate the sum of each gene mutation
    NR >= st_row{
      for (i=st_col; i<=NF; i++) m[i]+=$i
    }

    # print out the mutation sum of each gene
    END { for (key in h) { print h[key]","m[key]} }
' $TABLE_FILE
