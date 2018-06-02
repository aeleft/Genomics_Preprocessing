#!/usr/bin/python2.6

###############################################################################
# Script to check for the validation validitity of the filtering script.
# Specifically, the script checks for the following:
#   - Coding variant type
#   - Variant functional type
#   - Minor allele frequencies
#
# Input:    $1 - Path of input variant file to be filtered
#           $2 - Path of the output, filtered file
#
# Output:   $2 - Output, filtered file, written as a .csv with the unwated row
#                excluded
#
# Assumptions:
#   - First row and only the first row is the header row
#
# Author: Anthony Chen
###############################################################################

import os, sys, csv


### Define paths and file reading delimiter ###
INPUT_FILE = sys.argv[1]
INFILE_DELIM = ','
OUTPUT_FILE = sys.argv[2]


### WRITE_HEADER ###
WRITE_HEADER = True


### Specific filtering criterias ###
## Coding variant type (CVT) ##
CVT_colIdx = 8
WANTED_CVTs = set(["","frameshift_deletion", "frameshift_insertion", "frameshift_substitution", "nonsynonymous_SNV", "stopgain", "stoploss"])
# Note: if I want to include empty cells, include "" in the above set

## Variant function types (VFT) ##
ANNOTATION_colIdx = 10
WANTED_VFTs = set(["exonic", "exonic_splicing", "intronic_splicing"])

## Minor allele frequencies (MAF) (note that range is inclusive) ##
MAF_colIdx = 19
MAF_lowerBound = 0.0
MAF_upperBound = 0.01



### Opening Streams ###
#Open the input stream and read
inFile = open(INPUT_FILE, 'rb')
inFile_reader = csv.reader(inFile, delimiter=INFILE_DELIM)
#Open the output and writing stream
outFile = open(OUTPUT_FILE,'wb')
outFile_writer = csv.writer(outFile, delimiter=',', lineterminator='\n')

### Taking care of header ###
inFile_header = inFile_reader.next()
if WRITE_HEADER:
    outFile_writer.writerow( inFile_header )

### Iterate through the rest of the infile and filter ###
for rowIdx, rowContent in enumerate(inFile_reader):

    ## Filter for coding variant type (CVT) ##
    row_CVTs = set(rowContent[CVT_colIdx].split('|'))
    if not bool(row_CVTs & WANTED_CVTs):
        continue


    ## Filter for variant functional type (VFT) ##
    firstAnno_parts = set(rowContent[ANNOTATION_colIdx].split('|')[0].split(':'))
    #Check for set intersection between parts of the first annotation and wanted VFT
    if not bool(firstAnno_parts & WANTED_VFTs):
        continue


    ## Filter for minor allele frequencies (MAF)##
    #If it is convertable to a float but not within range, skip row
    try:
        if not MAF_lowerBound <= float(rowContent[MAF_colIdx]) <= MAF_upperBound:
            continue
    #If it is not convertable to a float, also skip row
    except ValueError:
        continue


    ## After passing all criterias, we can write-out the row to output file ##
    outFile_writer.writerow( rowContent )


#Close the input stream and exit
inFile.close()
outFile.close()
