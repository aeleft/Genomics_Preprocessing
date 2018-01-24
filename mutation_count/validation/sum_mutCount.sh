#! /bin/bash
# ============================================================================
# Script that takes a variant file and outputs the number of variants per gene
#   (see below for assumptions made on formatting), as well as the total
#   number of variants for the entire file
#
# Input   $1 - .csv variant file with integer mutations
#	  $2 - the phenotype column to start counting from
# Output: Printed each gene and the mutation sum for it
#
# Notes on assumptions:
#   - The input file has:
#       - individuals variants starting on column 184 with 6 col step size
#       - The gene column is column 10
#       - The detailed annotation column is column 11
# ============================================================================

#Variable for the input variant file
VAR_FILE=$1

#The column to start counting for individual phenotyes
START_PHENO_COL=$2


#Create a temporary file to store the genes and the mutation count per row
temp_file=`mktemp`

#Use awk to count the mutations
awk -F, -v st_pheno_col="$START_PHENO_COL" '
    # for every row, calculate the sum
    {sum = 0; for (i=st_pheno_col; i<=NF; i+=6) sum += $i}

    # print out the mutation sum with the gene and annotation
    {print $10","$11","sum}
' $VAR_FILE > $temp_file

#Use awk to count the number of mutations
awk -F, '
  {a[$1]+=$3}
  END{for(i in a) print i","a[i]}
' $temp_file

echo
awk -F, '
  {sum+=$3}
  END{print "Overall Mutation Sum =",sum}
' $temp_file

#Remove the temp file
rm $temp_file
