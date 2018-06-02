
# coding: utf-8

"""
Adopted from the following script that was:
    Created on Mon Jul 20 15:24:04 2015
    @author: Bogdan Istrate

Specs:
    - Run with python 2.7

Anthony Chen
May 2017

*Note that I deleted the old commented out script lines for clarity
(Anthony Chen, January 12, 2018)
"""

import os, csv, sys
fileType = "text" #change to "excel" to only consider excel files

"""""""""""""""""""""
Utility method to check for empty positions which should not be considered 0
and should also not give errors.
"""""""""""""""""""""

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def isEmpty(value):
    return True if value == "" else False

def findMatch(list1, list2):
    for item in list1:
        if item in list2:
            return True
    return False


"""""""""""""""""""""
Utility method to convert .output files to csv files, replacing any extraneous
commas (which do not delineate columns) with semicolons
"""""""""""""""""""""

def output_to_csv(outputFile):
    with open(outputFile) as inFile:
        converted = outputFile.split('.')[0]+'.csv'
        if os.path.isfile(converted):
            print("File " + converted + " already exists, skipping")
            return
        #csvFile = open(converted,'w', newline='')
        csvFile = open(converted,'w')
        writer = csv.writer(csvFile, quotechar='', escapechar='', quoting=csv.QUOTE_NONE)

        for line in inFile:
            item = line.split('\t')
            for i in range(0,len(item)):
                if not isfloat(item[i]):
                    item[i] = item[i].replace(',',';').strip()
            try:
                writer.writerow(item)
            except:
                print("Failed on file: " + outputFile +". Please remove this file" +
                    " from the folder and run the script again.")
                sys.exit(4)

        print(outputFile + " converted successfully\n")
        csvFile.close()

"""""""""""""""""""""
Converts specified files in the directory to .csv using the method
above (def xls_to_csv)
"""""""""""""""""""""
outputFileList = []
extension = '.output' if 'text' in fileType else '.xls'
for infile in [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(extension)]:
    print("Converting: " + infile + " to csv")
    outputFileList.append(infile.split('.')[0]+'.csv')
    if 'text' in fileType:
        output_to_csv(infile)
#    elif 'excel' in fileType:
#        xls_to_csv(infile)
    else:
        print("Something in the code went wrong. Please contact the developer\n")
        sys.exit(0)

outputFileList.sort(key=lambda item: (len(item), item))

"""""""""""""""""""""
Creates the filters to be applied when reading in the data files
"""""""""""""""""""""

#Set to 'True' if you want to filter for genes, 'False' to include all genes
APPLY_GENE_FILTER = False
#Set to 'True' if you want to apply the coverage criteria filters
COVCRI_FILTER = True

#List of genes to be filtered below
genes = ["A2M","AHDC1","ANKRD11","ATP2A2","BCKDHA","CACNA1A","CHD4","CHRNG","CP","CPNE7","CPOX","DICER1","DMPK","DNAH12","ECM1","FGFR2","GAL","GLUD2","GPR153","KCNN4","LRP1","MACF1","MAN2B1","MAP3K8","MED12","MMACHC","MPO","NAGS","NPC1","NT5DC3","PAK3","PDGFB","PINK1","PITPNM1","PLAU","PPP1R12B","PPT1","PRDM8","PTPN22","RGS12","ROGDI","RYR2","SETD1A","STAC2","TP53","TPH2","ZBTB20","ZFYVE26"]

#List of coding variant types below
coding_variant_types = ["frameshift_deletion", "frameshift_insertion", "frameshift_substitution","nonsynonymous_SNV", "stopgain", "stoploss"]

#SIFT = 0.05 #<=.05
#Index of SIFT value
#SiftInd = 24

#PolyPhen = 0.95 #>=.95
#Index of PolyPhen value
#PPInd = 26

#ExCon = 10 #<=10
#Indices at which to check external controls
#ExConInd1 = 74
#ExConInd2 = 76

genotypeQual = 90 #>=20
#Indices at which to evaluate genotype quality (CJ,CP,CV,DB)
genInd = [84,90,96] #TODO: unused variable

"""""""""""""""""""""
Reads in the files in the current directory and applies the filters from above,
writing the results to the file specified by "outfile".
The directory can be changed by using a different path in the round brackets of
os.listdir(), for example os.listdir('/Users/bogdan/Desktop/').
"""""""""""""""""""""


outfile = open("resultsPASS.csv", "a")
writer = csv.writer(outfile)
print("Make sure only the appropriate files are filtered:")
wroteHeader = False

for file in outputFileList:

    print("Filtering file: " + file)

    filtered = []

    #Open file and iterate through rows
    inFile = open(file)
    for i, current in enumerate(csv.reader(inFile)):
        if i == 0:
            if not wroteHeader:
                writer.writerow(current)
                wroteHeader = True
            continue
        else:
            ############### Filter for individuals begin ###############
            starting_col = 83 #First subject column (should be the zygosity)
            step_size = 6
            infinity = float('inf') #A positive infinity variable if needed for the upper bound

            #Iterate through all subjects on this row
            for subj_idx in range(starting_col, len(current)-1, step_size):
                #Boolean variables to store this subject's presence status
                hasGenotypeQual = True
                hasCoverageCriteria = True

                ###### Check Genotype Qualtiy (GQ) ######
                #Check if the GQ column is blank
                if not isfloat(current[subj_idx+1]):
                    hasGenotypeQual = False
                #If not blank, check if it passes the criteria
                elif float(current[subj_idx+1]) < genotypeQual:
                    current[subj_idx] = "Failed"

                ###### (Optional) for coverage criteria ######
                if COVCRI_FILTER == True:
                    #Checks for number of variant reads
                    if isEmpty(current[subj_idx+3]): #If it is empty
                        hasCoverageCriteria = False
                    elif (float(current[subj_idx+3]) < 4.0 ): #If it passes criteria
                        current[subj_idx] = 'Failed'
                    #Checks for depth of sequencing
                    if isEmpty(current[subj_idx+4]):
                        hasCoverageCriteria = False
                    elif not (10 <= float(current[subj_idx+4]) <= infinity):
                        current[subj_idx] = 'Failed'
                    #Checks for proportion of variant reads
                    if isEmpty(current[subj_idx+5]):
                        hasCoverageCriteria = False
                    elif (float(current[subj_idx+5]) < 0.20 ):
                        current[subj_idx] = 'Failed'

                ## If any of the above is missing, set subject to Missing
                if not (hasGenotypeQual and hasCoverageCriteria):
                    current[subj_idx] = "Missing"
            ############### Filter for individuals end ###############


            ###### Filter for functional type and gene begins ######
            #Filter for VFT and gene (gene is optional) in the detailed annotation column
            detailedAnnotations = current[10].split("|")
            found_VFT = False
            found_gene = False
            #Look at only the first detailed anotation
            anno_parts = detailedAnnotations[0].split(":")
            #Check for correct variant types
            if ("exonic" in anno_parts) or ("exonic_splicing" in anno_parts) or ("intronic_splicing" in anno_parts):
                found_VFT = True
            #Check for gene of interest
            if APPLY_GENE_FILTER == True:
                if findMatch(anno_parts, genes):
                    found_gene = True
            else:
                found_gene = True
            #Variant only pass if both VFT and (optional) genes are filtered
            if not (found_VFT and found_gene):
                continue
            ###### Filter for functional type and gene ends ######


            ###### Filter for coding variant type begins ######
            has_VT = False
            #Check for empty coding variant type box
            if isEmpty(current[8]):
                has_VT = True
            else:
                #Split by pipe just in case there are multiple coding variant types per input row
                for row_vt in current[8].split('|'):
                    #Check for membership (exact match) in coding_variant_type list
                    if row_vt in coding_variant_types:
                        has_VT = True
                        break #If one is found, row passes
            #Skip current row if no VT matches are found
            if has_VT == False:
                continue
            ###### Filter for coding variant type ends ######

            ######## Checking minor allele frequency <= 0.01 ########
            if not ( isfloat(current[19]) and (float(current[19]) >= 0.0 ) and (float(current[19]) <= 0.01) ):
                continue


            #The only way to get here is if ALL criteria are met, so that row is added to the list that will be written to file later
            writer.writerow(current)
    #Close file and let user know
    inFile.close()
    print("Done with " + file)

print("Done filtering all files above. Results can be found in the file resultsPASS.csv")
outfile.close()
