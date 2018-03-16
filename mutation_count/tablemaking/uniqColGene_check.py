#!/usr/bin/python2.6
###############################################################################
# Script that checks the uniqueness of the genes in a tablemaker output. If the
# header contains non-unique genes, it will attempt to sum them and output a
# similar file with only unique genes.
#
#
# Input:    $1 - Input file path to the table mutation count file
#           $2 - Output file path (unique-gene table file)
#           $3 - The number of columns for subject information
#
# Output:   $2 - Output file path containing unique gene table
#
# Note
#   - Assumes the subject information is always the first few columns
#
###############################################################################

#Import modules
import sys, os, csv
from collections import OrderedDict


#Specify path of input and output files
INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

#How many columns from the input file are for subject information?
SUBJ_INFO_COLS = int(sys.argv[3])

### Check the first row to see if there are non-unique genes ###

#Open the input file stream
inFile = open(INPUT_FILE,'rb')
reader = csv.reader(inFile, delimiter=',')

#Read the header genes and check to see if it is unique
raw_header_genes = reader.next()[SUBJ_INFO_COLS:]
header_gene_set = set(raw_header_genes)

#If the header already contain all unique genes, terminate program
if len(raw_header_genes) == len(header_gene_set):
    print "All genes already unique. Updating filename and terminating program."
    inFile.close()
    os.rename(INPUT_FILE, OUTPUT_FILE)
    sys.exit()


### Re-setup if the input file does not contain only unique gene columns ###
inFile.seek(0)
#Keeping track of # subject info column + # unique gene column
M_cols = len(header_gene_set) + SUBJ_INFO_COLS

#Open output file
outFile = open(OUTPUT_FILE,'wb')
writer = csv.writer(outFile, delimiter=',', lineterminator='\n')


### Read the first row of input file again to get dict of unique genes ###

#Read the header and initialize the output list for the new header
in_header = reader.next()
out_header = [''] * M_cols
#Store subject information cells
out_header[0:SUBJ_INFO_COLS] = in_header[0:SUBJ_INFO_COLS]

#Initialize a sorted dictionary for the indeces of each gene
geneIdxs_dict = OrderedDict()

#Iterate and initialize the gene --> column indeces mappings
for colIdx, geneName in enumerate(in_header):
    #Skip the subject information columns
    if colIdx < SUBJ_INFO_COLS:
        continue

    #If the current column gene name is not in the dictionary
    if geneName not in geneIdxs_dict:
        geneIdxs_dict[geneName] = [colIdx]
    #If the gene name is in the dictionary, append the second column idx
    else:
        geneIdxs_dict[geneName].append(colIdx)

#Add the genes to the output list and writeout
out_header[SUBJ_INFO_COLS:] = [k for k in geneIdxs_dict]
writer.writerow(out_header)


#### Iterate through the rest of the rows which contain individual subjects ####
for in_row in reader:
    #Initialize output list and subject information
    out_row = [''] * M_cols
    out_row[0:SUBJ_INFO_COLS] = in_row[0:SUBJ_INFO_COLS]
    #Iterate through each gene in the OrderedDict
    for geneIdx, geneName in enumerate(geneIdxs_dict):
        #Take the sum of all the (column) cells containins this gene
        geneMutSum = 0
        for colIdx in geneIdxs_dict[geneName]:
            geneMutSum += int(in_row[colIdx])
        #Store the gene in the output array
        out_row[SUBJ_INFO_COLS+geneIdx] = geneMutSum

    #After iteration, print current row
    writer.writerow(out_row)


#Close the input and output streams
inFile.close()
outFile.close()
