#!/usr/bin/python2.6

###############################################################################
# Script to extract the subject mutation information and match with a refere-
# nce subject information file.
#
# The script writes out a transpose of the subject information file such that
#   the subject ID's and associated information are written to the first few
#   rows. It then reads through the variant file and matches the mutation from
#   each gene to the correct subject.
#
#
# Input:    $1 - Path to variant file containing mutations from exome sequencing
#           $2 - Path to subject information file
#           $3 - Path to output the resulting file
#           $4 - The column index at which the subject IDs (fam_ID) is
#
# Output:   $3 - Output file
#           Stdout - single integer denoting the number of header rows
#
#
# Note:
#   Format of subject information file:
#   - The file must only have a single line of header information, the subject
#       information must start on the second row
#   - This is because the script skips the first row and reads from the second
#       row to initialize the subject arrays
#
#   Format of the variant file
#   - Assume the funcitonal gene is always in the first detailed annotation
#   - Assumes
#   - Assumes that the zygosity status jumps by 6 columns each time
##############################################################################

import os, sys, csv

VAR_FILE = sys.argv[1]
SUBJ_INFO_FILE = sys.argv[2]
OUTPUT_FILE = sys.argv[3]

#Which column in the sample info file contains the subject key for matching?
SUBJ_KEY_COL = 0

#Which column in variant file has the genes
GENE_COL = 9
#Which column in variant file has the detailed annotation
ANNO_COL = 10
#Which column in variant file has the subject IDs
SUBJ_IDS_COL = int(sys.argv[4])
#What is the delimiter used to separate the individuals in the above column?
SUBJ_IDS_DELIM = ';'
#First column in variant file has zygosity statuses
ZYGOSITY_START_COL = SUBJ_IDS_COL + 1



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


#Function to convert a zygosity into a mutation count
def zygo2mutCount(zygosity):
    #Mapping between zygosity and mutation count
    zygosity_mapping = {\
        'Filtered Wildtype':0, 'Wildtype':0,\
        'Filtered Heterozygote':1, 'Heterozygote':1,\
        'Filtered Homozygote':2,'Homozygote':2,\
        'Filtered Trizygote':3, 'Trizygote':3,\
        'Missing':0,'Failed':0,'':0, ' ':0
    }

    return zygosity_mapping[zygosity]


#Initialize a hashmap to store subject ID --> subject column index
HashMap_Id2Col = {}


############# READING INFORMATION FROM SUBJECT INFORMATION FILE #############

#Open the subject information file and the output file streams
infoFile = open(SUBJ_INFO_FILE,'rb')
infoFile_reader = csv.reader(infoFile, delimiter=',')
outFile = open(OUTPUT_FILE,'wb')
outFile_writer = csv.writer(outFile, delimiter=',', lineterminator='\n')

#Save the header (always 1st row) from the subject information file
infoFile_header = infoFile_reader.next()
#Output how many header rows there are to skip
print len(infoFile_header)

#Iterate over each column to write to output
for infoFile_colIdx in range(0,len(infoFile_header)):
    #Reset the reader's row position to the second row
    infoFile.seek(0)
    infoFile_reader.next()

    #Initialize an array to contain this specific type of subject information
    subjInfo = [ infoFile_header[infoFile_colIdx] ]

    #Iterate over the subject information file to get all subjects' info
    for rowIdx, rowContent in enumerate(infoFile_reader):
        subjInfo.append( rowContent[infoFile_colIdx] )
        #If this column contains the subject key, store in hashmap
        if infoFile_colIdx == SUBJ_KEY_COL:
            #rowIdx + 1 because we skipped the first row but it still counts
            HashMap_Id2Col[rowContent[infoFile_colIdx]] = rowIdx + 1

    #Write out the information to the output file
    outFile_writer.writerow(subjInfo)

#Close the input stream from the subject information file
infoFile.close()

## Note on carrying over: ##
# The output stream for outFile is still open, and we need the hashmap variable
# from above to establish which column to write out the mutation count to
###



################### READING INFORMATION FROM VARIANT FILE ###################
#Open the variant file input stream
varFile = open(VAR_FILE,'rb')
varFile_reader = csv.reader(varFile, delimiter=',')

#Offset the first header row
varFile_reader.next()
#Read through the variant file, starting from the second row
for varRow in varFile_reader:
    #Extract the functional gene for this row
    funcGene = extract_funcGene(varRow[GENE_COL], varRow[ANNO_COL])

    #Initialize the output list for this row with n-subject + 1 columns
    outRow = [0] * ( len(HashMap_Id2Col) + 1 ) #TODO: make this more robust?
    #The first column of the output row is the functional gene name
    outRow[0] = funcGene

    #Get the subject IDs
    subject_IDs = varRow[SUBJ_IDS_COL].split(SUBJ_IDS_DELIM)

    #Iterate through each subject's zygosity to get mutation count
    zygosity_col = ZYGOSITY_START_COL
    for subj_id in subject_IDs:
        #Convert the zygosity to a mutation count
        mutCount = zygo2mutCount(varRow[zygosity_col])

        #Add the mutation count to the correct subject column
        current_subj_col = HashMap_Id2Col[subj_id]
        outRow[current_subj_col] = mutCount

        #Increment the column index to the next subject's zygosity
        zygosity_col += 6

    #Write out the current row to the output file
    outFile_writer.writerow(outRow)


#Close the variant file and output file streams
varFile.close()
outFile.close()
