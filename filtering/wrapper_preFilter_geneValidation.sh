#!/bin/bash
# ============================================================================
# (Example Script - delete this line)
# Wrapper script that runs a bash-faciliated pipeline on a directory of .output
# files for 5 specific genes.
#
# Date initiated: 
#
# ============================================================================


#File paths
FILTERED_FILE="???"

#Genes to select for
GENE_1="DEFB12"
GENE_2="DUXAP"
GENE_3="OR4F"
GENE_4="SAMD11"
GENE_5="TUBB8"


#Script Paths
CSV_2_TSV="csv2tsv.py"
CODING_VAR_TYPE_FILTER="codeVarType_filter.sh"
FUNCTIONAL_TYPE_FILTER="varFuncType_filter.sh"
MIN_ALLELE_FREQ_FILTER="minAlleleFreq_filter.sh"

# *** Remember *** #
# Change the absolute helper file paths inside of:
#   - CODING_VAR_TYPE_FILTER
#   - FUNCTIONAL_TYPE_FILTER



##### Get variants with correct genes and merge

#Create temp file to merge all the unfiltered variants with desired genes
start_file=`mktemp`

#Grep for all gene patterns (surpress file name output) from .output files
grep -h -e $GENE_1 -e $GENE_2 -e $GENE_3 -e $GENE_4 -e $GENE_5 *.output > $start_file



##### Filter the chosen variants #####

#Filter for coding variant type
code_var_filtered=`mktemp`
bash $CODING_VAR_TYPE_FILTER $start_file  $code_var_filtered
rm $start_file

#Filter for functional variant type
func_var_filtered=`mktemp`
bash $FUNCTIONAL_TYPE_FILTER $code_var_filtered $func_var_filtered
rm $code_var_filtered

#Filter for minimum allele frequency
sh_filtered_subset=`mktemp`
bash $MIN_ALLELE_FREQ_FILTER $func_var_filtered $sh_filtered_subset
rm $func_var_filtered


#(potential) Additional filter to isolate functional genes?



##### Grep the same genes from the py-filtered file #####
py_filtered_subset=`mktemp`
grep -h -e $GENE_1 -e $GENE_2 -e $GENE_3 -e $GENE_4 -e $GENE_5 $FILTERED_FILE > $py_filtered_subset


##### Print-out #####
echo "Python filtered subset file line count:",
wc -l $py_filtered_subset
echo "Original filtered subset file line count:",
wc -l $sh_filtered_subset

rm $py_filtered_subset
rm $sh_filtered_subset


