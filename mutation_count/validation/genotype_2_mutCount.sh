#!/bin/bash
# ============================================================================
# Script that finds and replaces all word sequences in a given file. This is
#   used currently to replace zygosity with an integer representation of the
#   mutation count.
#
# Input   $1 - .output / .tsv / .csv file to be find-and-replaced-ed
#         $2 - path to the output file in the same format
#
# Output: .output file with the string sequences replaced
#
# Note that the `sed` function assumes GNU sed (i.e. Linux server). It will
# not work if run using OS/X. Also that the stdout is appended to the output
# stream but does not explicitly overwrites it.
# ============================================================================

#Set up path variables
VAR_FILE=$1
OUTPUT_PATH=$2


#Start sed script to replace various phenotypes
sed '
	s/Filtered Heterozygote/1/g;
	s/Heterozygote/1/g;

	s/Filtered Homozygote/2/g;
	s/Homozygote/2/g;
	
	s/Filtered Trizygote/3/g;
	s/Trizygote/3/g
' $VAR_FILE >> $OUTPUT_PATH


