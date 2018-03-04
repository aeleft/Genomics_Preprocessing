#!/usr/bin/bash
###############################################################################
# Script which extracts a subset of genes from the filtered variant file (via
# grepping), and counts the number of 'Heterozygote', 'Homozygote' and 'Trizygote'
# occurances in each of the subfiles.
#
# Input: N/A (but change the initial variable parameters)
#
# Output: stdout for a report of the Heterozygote, Homozygote, etc. count for
#         each of the genes
#
# Note:
#   - Zygosity sub-files are generated in the current working directory
#   - Assumes genes are in column 10 (counting from 1)
###############################################################################

## Path of variant file ##
VAR_FILE=""

## Declare array of gene names to check for ##
declare -a arr=("GENE1"
                "GENE2"
                "GENE3"
                "GENE4"
                "GENE5"
                )


#Indicate variant file path
echo "Variant file relative to current directory: $VAR_FILE"
echo "Current date: `date`"
echo

#Iterate through each gene to generate report results
for g in "${arr[@]}"
do
  #Indicate to user:
  echo "========================================"
  date
  echo "Gene being extracted from variant file: $g"

  #Generate the name for the zygosity file
  zygoFile="$g""_zygosityFile_shGen.csv"

  #Grep the gene from the variant file into the zygosity file
  python getGeneSubfile.py $VAR_FILE $g $zygoFile

  #Look for the mixed list of genes in the zygosity file
  echo "Genes present in $zygoFile :"
  cut -d',' -f 10 $zygoFile | sort -u
  echo

  #Look for the types of mutations
  echo "Grep-ing for 'Heterozygote' count:"
  grep -o "Heterozygote" $zygoFile | wc -l
  echo "Grep-ing for 'Homozygote' count:"
  grep -o "Homozygote" $zygoFile | wc -l
  echo "Grep-ing for 'Trizygote' count:"
  grep -o "Trizygote" $zygoFile | wc -l

  #New line for separation
  echo
done
