#!/usr/bin/python2.6
"""
Script that converts a filtered output file into rows of genes with columns as individuals and their mutation count in that gene.

Input:  $1 - filtered input file from segregation
        $2 - sample information file
        $3 - affection status as seen in sample informaiton file

Output: condensed file containing just individuals, genes gender and mutation count

Note:
    - Run with Python 2
    - Adopted from Bill's script, originally created (Sun Dec 20 12:54:02 2015)
    - input file needs to be a comma-separated, NOT the excel utf8 encoding
        - The encoding type of the output and input file needs to be the same
        - It is safest to run both on the same system (i.e. same versino of Linux)
        - I've only chagned the SAMPLE_INFORMATION_FILE to read universal encoding
            (open file with 'rU'), but if problem persist you may wish to open all
            files with 'rU'

Author: Anthony Chen
May 2017
"""


import os, csv, sys
from sets import Set

#Path Variables
INPUT_FILE = sys.argv[1]
SAMPLE_INFORMATION_FILE = sys.argv[2]
AFFECTION_STATUS = sys.argv[3]

CONDENSED_OUTPUT_FILE = "merged_file_transposed.csv"

#Subject column variables
SUBJ_START_COL = 83
STEP_SIZE = 6


#Opens and stores information from the sample information file
with open(SAMPLE_INFORMATION_FILE,'rU') as sampleFile:
    #Initiate variables
    affectionStatus = AFFECTION_STATUS
    idList = []
    genderList = []
    idList.append("Family_ID")
    genderList.append("Gender")
    #Open file with correct dialect and skip first line
    sample_reader = csv.reader(sampleFile, delimiter=',')
    sample_reader.next()
    #Iterate through rows to get information
    for row in sample_reader:
        if affectionStatus in row[2]:
            idList.append(row[0])
            genderList.append(row[1])


#creates and writes ID and Gender into new merged file
outfile = open(CONDENSED_OUTPUT_FILE, "wb")
writer = csv.writer(outfile)
writer.writerow(idList)
writer.writerow(genderList)

#Filters input file row by row, ignoring the first row
mutationsList = []
geneList = []
with open(INPUT_FILE) as inFile:
    #Open and read the input file
    inFile_reader = csv.reader(inFile, delimiter=',')
    inFile_reader.next() #skip the first line (header)!
    #Iterate through each row of the input file
    for row in inFile_reader:
        #Look at the genes present in the current row
        current_genes = row[9].split("|")
        #Check only the first detailed variant annotation
        anno_parts = (row[10].split("|")[0]).split(":")
        #Check the variant has the correct functional type
        if not ( ('exonic' in anno_parts) or ('intronic_splicing' in anno_parts) or ('exonic_splicing' in anno_parts) ):
            continue
        #Iterate through the parts of the annotation to find gene match
        for anno_part in anno_parts:
            if anno_part in current_genes:
                print anno_part #Let user know
                geneList.append(anno_part)
                mutationsList.append(anno_part)
                break
        #Check for the mutation number for the current variant row
        if len(mutationsList) > 0:
            for j in range(SUBJ_START_COL,len(row),STEP_SIZE):
                mutationsNum = 0
                if "Wildtype" in row[j]:
                    mutationsNum = 0
                if "Heterozygote" in row[j]:
                    mutationsNum = 1
                if "Homozygote" in row[j]:
                    mutationsNum = 2
                if "Trizygote" in row[j]:
                    mutationsNum = 3
                if "Filtered Wildtype" in row[j]:
                    mutationsNum = 0
                if "Filtered Heterozygote" in row[j]:
                    mutationsNum = 1
                if "Filtered Homozygote" in row[j]:
                    mutationsNum = 2
                if "Filtered Trizygote" in row[j]:
                    mutationsNum = 3
                mutationsList.append(mutationsNum)
            writer.writerow(mutationsList)
        del mutationsList[:]

outfile.close()


print("DONE!")
