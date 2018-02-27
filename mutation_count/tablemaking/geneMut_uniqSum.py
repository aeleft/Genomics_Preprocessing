#!/usr/bin/python2.6

###############################################################################
# Script that takes a gene mutation count file and sums over (consecutive) rows
# that have the same gene.
#
# Input:    $1 - Input file path of the file I want to take uniq gene sums from
#           $2 - Output file path
#           $3 - The number of header rows in the input file
#
# Output:   $2 - Output file path containng unique genes
#
#
# Note:
#   Formatting of input mutation count file:
#       - Assumes that all identical genes would be in consecutive rows
###############################################################################

#Import modules
import os, sys, csv
from operator import add


#Specify path of input and output files
INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

#How many rows from the input file are header rows?
HEADER_OFFSET = int(sys.argv[3])


#Open the input and output read / write streams
inFile = open(INPUT_FILE,'rb')
inFile_reader = csv.reader(inFile, delimiter=',')
outFile = open(OUTPUT_FILE,'wb')
outFile_writer = csv.writer(outFile, delimiter=',')


### Write the header from the input file to the output file ###
for i in range(0,HEADER_OFFSET):
    outFile_writer.writerow( inFile_reader.next() )

### Set up variables and read the first gene line ###
#Read the first line of mutation count and store the gene associated
curLine = inFile_reader.next()
curGene = curLine[0]
#Get just the mutation counts in integer format
curMuts = map(int, curLine[1:])


### Iterate through the rest of the input file ###
for rowIdx, rowContent in enumerate(inFile_reader):
    #Get just the mutation count in integer format for the current row
    newMuts = map(int, rowContent[1:])

    #If there is a new gene, format and write out to output file
    if (rowContent[0] != curGene):
        #Make a new list with the previous gene and summed mutation count
        outRow = [curGene] + curMuts
        #Write to output
        outFile_writer.writerow(outRow)

        #Update the current gene variable
        curGene = rowContent[0]
        curMuts = newMuts

    #If the gene is the same, aggregate the mutation count
    else:
        #NOTE: check if outputting to the same list is good practice?
        curMuts = map(add, curMuts, newMuts)

#Write the last gene to the output file
outRow = [curGene] + curMuts
outFile_writer.writerow(outRow)


#Close the input and output streams
inFile.close()
outFile.close()
