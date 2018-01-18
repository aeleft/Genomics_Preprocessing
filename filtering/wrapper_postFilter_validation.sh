#!/bin/bash
# ============================================================================
# (Example Script - delete this line)
# Wrapper script that runs a bash-faciliated pipeline on the python-filtered
# variant file.
#
# Date initiated: 
#
# ============================================================================


#File paths
INPUT_FILE="testFiles/resultAFF_small.csv"
OUTPUT_FILE="testFiles/re-filtered_resultAFF.tsv"

#Script Paths
CSV_2_TSV="csv2tsv.py"
CODING_VAR_TYPE_FILTER="codeVarType_filter.sh"
FUNCTIONAL_TYPE_FILTER="varFuncType_filter.sh"
MIN_ALLELE_FREQ_FILTER="minAlleleFreq_filter.sh"

# *** Remember *** #
# Change the absolute helper file paths inside of:
#   - CODING_VAR_TYPE_FILTER
#   - FUNCTIONAL_TYPE_FILTER


##### Write header of input file into output file #####
head -1 $INPUT_FILE > $OUTPUT_FILE


##### Convert the filtered file back into a .tsv file #####
filtered_tsv=`mktemp`
python $CSV_2_TSV < $INPUT_FILE > $filtered_tsv


##### Apply Filtering Criterias #####

#Filter for coding variant type
code_var_filtered=`mktemp`
bash $CODING_VAR_TYPE_FILTER $filtered_tsv $code_var_filtered
rm $filtered_tsv

#Filter for functional variant type
func_var_filtered=`mktemp`
bash $FUNCTIONAL_TYPE_FILTER $code_var_filtered $func_var_filtered
rm $code_var_filtered

#Filter for minimum allele frequency
bash $MIN_ALLELE_FREQ_FILTER $func_var_filtered $OUTPUT_FILE
rm $func_var_filtered


##### Print-out #####
echo "The output file can be found at: $OUTPUT_FILE"
echo "Input file line count:",
wc -l $INPUT_FILE
echo "Output file line count:",
wc -l $OUTPUT_FILE


