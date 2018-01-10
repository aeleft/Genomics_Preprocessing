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
# ============================================================================

#Set up path variables
VAR_FILE=$1
OUTPUT_PATH=$2

echo "Initializing file $OUTPUT_PATH"
#Create a copy of the input file as the output file
cp $VAR_FILE $OUTPUT_PATH


### Carry out in-place replacement for the output file ###
#Note, the "Filtered [genotype]" conversion needs to be done first

#Filtering the heterozygote
sed -i '' 's/Filtered Heterozygote/1/g' $OUTPUT_PATH
sed -i '' 's/Heterozygote/1/g' $OUTPUT_PATH

#Filtering the Homozygote
sed -i '' 's/Filtered Homozygote/2/g' $OUTPUT_PATH
sed -i '' 's/Homozygote/2/g' $OUTPUT_PATH

#Filtering the trizygote
sed -i '' 's/Filtered Trizygote/3/g' $OUTPUT_PATH
sed -i '' 's/Trizygote/3/g' $OUTPUT_PATH


echo "Done!"
