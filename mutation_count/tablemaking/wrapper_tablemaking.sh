#!/usr/bin/bash

###############################################################################
# Wrapper script for the tablemaking processing pipeline from variant files.
#
# Pipeline initialied on date:
#
###############################################################################

### File paths ###
#Post-filtered variant file
VAR_FILE=""
#Subject information file
SUBJ_INFO_FILE=""
#Final output table file
OUT_TABLE_FILE=""

### Dataset-specific variables ###
#The column index (from idx=0) containing subject ID in the variant file
SUBJ_ID_COL=82
#dbGaP_casecontrol:182; dbGaP_trios:82; NDAR:85 ; CONFIRM ON FILE EACH TIME


## Extract the mutation count from the variant file ##
echo "Extracting mutation count from variant file: `date`"
#Make temp file for mutation extraction output
mutExtracted_file=`mktemp`
#Make temp file for the header offhset
header_offset_file=`mktemp`
#Run mutation count extraction script, save the header offset
python indvMut_extract.py $VAR_FILE $SUBJ_INFO_FILE $mutExtracted_file $SUBJ_ID_COL > $header_offset_file

#Save header offset to local variable and indicate to user
header_rows=`cat $header_offset_file`
echo "Number of rows to offset for header: $header_rows"
rm $header_offset_file


## Condense the extrated mut-count file such that it has unique genes ##
echo "Summing mutations for unique genes: `date`"
#Make a temp file for the transposed table output
table_transposed=`mktemp`
#Run the file to condense the mutation count file into only unique genes
python geneMut_uniqSum.py $mutExtracted_file $table_transposed $header_rows

#Remove the mutation extraction temp file
rm $mutExtracted_file


## Transpose the transposed table file to generate the final table ##
echo "Transposing to create finalized table file: `date`"
bash transpose_csv.sh $table_transposed $OUT_TABLE_FILE

#Remove the intermediate table file
rm $table_transposed

echo "Done! On `date`"
