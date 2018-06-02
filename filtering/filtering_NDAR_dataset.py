# coding: utf-8

"""
Adopted from the following script that was:
    Created on Mon Jul 20 15:24:04 2015
    @author: Bogdan Istrate

Specs:
    - Run with python 2.7

Anthony Chen
May 2017


*Note that the commented out code has been deleted for simplicity.
(Anthony Chen, January 13, 2018)

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

#Below are the genes you want to filter for

genes = ["ABCA12","ABCA13","ABCA3","ABI3BP","ADAM22","AFF4","AHNAK2","ANK3","AOC3","ARHGAP15","ASH1L","ASXL3","BICC1","BRD3","C10orf90","CACNA1E","CADPS","CDCA7L","CDKL3","CHD1","CHD2","CHST5","CREBBP","CUL3","CYTH4","DCAF4","DCTN5","DDX50","DICER1","DNAH7","DNAJC16","ECSIT","EEF1A2","EIF3G","ELK1","ENO3","EPAS1","EPHB6","ETFB","FAT1","FN1","FOXP1","GABRB3","GCN1L1","GPR139","GTF3C2","H2AFV","HERC1","HIVEP3","IL1R2","ITPR1","JAK2","JMJD1C","KIAA0226","KIAA1967","KIRREL3","KRTAP9-3","LPHN2","LRP1","LRP1B","MACC1","MANSC1","MCM2","MCPH1","MED13L","METTL2B","MKL2","MOV10","MPDZ","MUC4","MYCBP2","MYH10","MYH9","MYO1A","MYO5B","MYO9B","MYOF","MYOM2","MYT1L","NEB","NFASC","NISCH","OBSCN","PCDH15","PCDHB16","PCNX","PIAS1","PIWIL4","PLCD1","PLCD4","PLEKHA4","PLXNB1","POGZ","POLR1E","POLR2A","PTEN","RBMS3","RELN","RFX3","RTN4RL1","SBF1","SCN2A","SCRIB","SETD2","SETD5","SETD7","SLC30A5","SLC39A5","SLC6A1","SLC6A3","SMARCC2","SNAPC5","SNTG1","SPAST","STAT2","SVIL","SYNE1","SYNE2","SYNGAP1","TBL1XR1","TBR1","TCF3","TDRD5","TECTA","TGM3","TLK2","TRIO","TTN","TUBA1A","UBR4","UGT2B10","UNC79","USH2A","VAV3","WDR20","WDR66","XIRP1","XRCC5","XRN2","ZFC3H1","ZFHX3","ZFPM2","ZNF155","CALR3","FLNC","JPH2","MYH6","MYL2","MYL3","MYPN","NEXN","TCAP","TNNI3","TNNT2","TPM1","TTN","VCL","MTATP6","MTATP8"]

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
genInd = [87,93,99,105]

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

    #Open file and iterate through all rows
    inFile = open(file)
    for i, current in enumerate(csv.reader(inFile)):
        if i == 0:
            if not wroteHeader:
                writer.writerow(current)
                wroteHeader = True
            continue
        else:
            ############### Filter for individuals begin ###############
            fam_member_col = 85
            infinity = float('inf') #A positive infinity variable if needed for the upper bound

            #Iterate through all subjects on this row (from 1st to last subject)
            for subj_idx in range(86, 104+1, 6):
                #If no sibling present, but on the sibling column, skip current iteration
                if ('.s' not in current[85]) and (subj_idx == 104):
                    current[subj_idx] = 'NoSibling'
                    continue

                #Boolean variables to store this subject's presence status
                hasGenotypeQual = True
                hasCoverageCriteria = True

                #### Check if the subject zygosity is present (essential for sibling check)
                if isEmpty(current[subj_idx]):
                    current[subj_idx] = "Missing"
                    continue #No point checking other criterias if the subject isn't even present

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
                    elif not (10 <= float(current[subj_idx+4]) <= 184):
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
    inFile.close()
    print("Done with " + file)

print("Done filtering all files above. Results can be found in the file resultsPASS.csv")
outfile.close()


