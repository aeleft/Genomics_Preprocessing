#!/usr/bin/python2.6

###############################################################################
# Script to extract a subset of a file based on a functional gene of interest
#
# Input:    $1 - Path to the filtered variant file
#           $2 - String sequence for the gene of interest
#           $3 - Path to the output file containing just rows for that gene
#
# Output:   $3 - Output file
#
# Note:
#   - Assume the funcitonal gene is always in the first detailed annotation
#   - Assumes the gene and detailed annotation columns are 9 and 10 (counting
#       from index 0), respectively
##############################################################################

import os, sys, csv

VAR_FILE = sys.argv[1]
GENE_OF_INTEREST = sys.argv[2]
OUTPUT_FILE = sys.argv[3]


############# FUNCTION DEFINITIONS #############
#Function to get the functional gene using the gene and annotation columns
def extract_funcGene(genesCol, annosCol):
    #Split the genes asnd annotations into part
    genes = genesCol.split('|')
    anno_parts = annosCol.split('|')[0].split(':')
    #Iterate over the parts of the annotation to find functional gene
    for part in anno_parts:
        if part in genes:
            return part

################ Script starts ################
#Open the variant file and the output file streams
varFile = open(VAR_FILE,'rb')
reader = csv.reader(varFile, delimiter=',')
outFile = open(OUTPUT_FILE,'wb')
writer = csv.writer(outFile, delimiter=',')

#Iterate the entire variant file
for row in reader:
    #Get the variant's functional gene
    funcGene = extract_funcGene(row[9],row[10])
    #Write out this row if it contains the correct functional gene
    if funcGene == GENE_OF_INTEREST:
        writer.writerow(row)


#Close the input and output streams
varFile.close()
outFile.close()
