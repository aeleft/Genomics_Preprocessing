#!/bin/bash
# ============================================================================
# Script that replaces all multi-gene sequence with a single functional gene
#   per variant row. This is done via splitting the genes and seeing which
#   gene is a substring of the first detailed annotation
#
# Input   $1 - .csv file to be find-and-replaced-ed
#         $2 - path to the output file in the same format
#
# Output: .csv file with the gene replaced to be functional
# ============================================================================

#Set command-line variables
VAR_FILE=$1
OUT_FILE=$2

#Set gene column variables - this is for the variant file column
GENE_COL=10
ANNO_COL=11

#Make two temporary files to store the genes and annotations, respectively
gene_list_file=`mktemp`
anno_list_file=`mktemp`

#Make a temporary file to store the actual functional gene name
func_gene_file=`mktemp`

#Get all of the genes into the raw gene file
sed -n '2,$p' <$VAR_FILE | cut -d',' -f $GENE_COL > $gene_list_file
#Get all of the detailed annotations into the raw annotation file
sed -n '2,$p' <$VAR_FILE | cut -d',' -f $ANNO_COL | cut -d'|' -f 1 > $anno_list_file

#Make the header for the functional gene file
head -1 $VAR_FILE | cut -d',' -f $GENE_COL > $func_gene_file

#Use awk to send the correct functional gene into the functional gene file
awk -F'|' '
{
  #Store the annotation (from the annotation file)
  if(NR==FNR) {
    a[NR]=$1;
  }
  #Check each gene and only take the one that is a substring of the annotation
  else {
    for(i=1; i<=NF; i++) {
      if(index(a[FNR],$i) != 0){
        print $i
      }
    }
  }
}
' $anno_list_file $gene_list_file >> $func_gene_file

#Use awk to send the correct functional gene into a copy of the variant file
awk -v col_num="$GENE_COL" '
  BEGIN{FS=OFS=","}
  FNR==NR{a[NR]=$1;next}{$col_num=a[FNR]}1
' $func_gene_file $VAR_FILE >> $OUT_FILE


#Remove the temporary files
rm $gene_list_file
rm $anno_list_file
rm $func_gene_file
