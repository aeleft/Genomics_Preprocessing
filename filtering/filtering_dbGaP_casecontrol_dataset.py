#!/usr/bin/env python2
"""
Adopted from original author:
    - Bogdan Istrate
    - Created on Mon Jul 20 15:24:04 2015


Anthony's to self:
    - Run with python2
    - Commented out sections that uses the xlrd packages as it is non-default.
        May renable later if a clean compatible solution can be found to use
        this package both locally and on the database server
        - (Update) Does not seem necessary - script is working
    - Check the "TODO's" to find temp changes that should be changed / deleted
    - Note that the script formatting has been altered from the original for
        clealiness
    - Note that the coverage criteria filters assumes:
        - The first subject will have his/her zygosity column at col 89 (counting starting from index 0)


Anthony Chen
May 2017
"""
# (Anthony's note) xlrd import has been commented out as it is a non-default
#   package.
#import xlrd

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


#"""""""""""""""""""""
#Utility method to convert excel files to csv files, replacing any extraneous
#commas (which do not delineate columns) with semicolons
#"""""""""""""""""""""
#
#def xls_to_csv(excelFile):
#    with xlrd.open_workbook(excelFile) as inFile:
#        xlSheet = inFile.sheet_by_index(0)
#        csvFile = open(excelFile.split('.')[0]+'.csv','w')
#        writer = csv.writer(csvFile, quotechar='', escapechar='', quoting=csv.QUOTE_NONE)
#
#        for rowNum in range(xlSheet.nrows):
#            item = xlSheet.row_values(rowNum)
#            for i in range(0,len(item)):
#                if not isfloat(item[i]):
#                    item[i] = item[i].replace(',',';').strip()
#            try:
#                writer.writerow(item)
#            except:
#                print("Failed on file: " + excelFile +". Please remove this file" +
#                    " from the folder and run the script again.")
#                sys.exit(4)
#
#        print(excelFile + " converted successfully\n")
#        csvFile.close()


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

#List of genes to filter below

genes = ["ACE","ACKR2","ACR","ACY1","ADA","ADAM2","ADAMDEC1","ADAMTS14","ADCY9","ADGRF3","ADGRF5","AIP","AKAP1","ANKRD2","ANKRD24","ANKRD30A","ANXA1","ANXA11","APC2","AR","ARC","ARHGAP1","ARHGAP11A","ARL1","ARL11","ARL13B","ARNT","ASIP","ASTN1","ATAD2","ATF6B","BMP1","BOD1","BPI","BRAT1","BSX","BTAF1","BZRAP1","C1D","C1orf116","C1R","C2","C21orf33","C2orf71","C3","C3orf20","C5","C9","CAD","CALD1","CAMK1","CAMK1D","CAP1","CAPN12","CARD11","CAT","CCDC102B","CCDC114","CCDC13","CCDC155","CCDC17","CCDC3","CCDC78","CCK","CCKAR","CDCA8","CDH10","CDH12","CDH3","CDK1","CEP164","CFAP58","CFAP61","CHM","CIC","CKAP4","CMYA5","CNDP1","CP","CREB3","CRYBG3","CS","CSRP2","CSRP2BP","CTSO","CXCL1","DBN1","DCHS2","DCLRE1A","DDX20","DDX58","DEC1","DENND3","DHH","DNAH3","DNAJB1","DNAJC5","DOCK1","DPP6","DSC2","EAF1","EDN1","EIF3A","ELK3","ENAM","EPB41L4B","ERBB2","ERG","F10","F12","F2","F3","F5","FAM129B","FAM63A","FANCA","FAT2","FBXO24","FERMT3","FH","FLG","FLNC","FNDC1","FSD1","FUK","GABRR2","GAL","GJA1","GPAM","GPATCH8","GPRIN2","GRAP","GRAP2","GRB14","GRIK3","GRM2","GRP","GSN","HAPLN1","HAPLN3","HCN3","HECTD4","HERC1","HNRNPU","HPSE","HR","HSPA14","HTR6","ICA1","ID1","IGDCC4","IK","IL21","IL21R","IL3","IL32","IL4R","INF2","IRAK3","IRX6","ISG20L2","ITGB7","KCNE5","KCTD1","KDR","KIAA0754","KIDINS220","KIF18A","KIF27","KL","KLK1","KLKB1","KMT2D","KNTC1","KRT34","KRT7","KRT71","LARS","LBP","LRP11","LRRC31","LRRC56","MAGEA1","MAGI1","MAP3K1","MAP3K15","MAP4","MARCO","MCC","MDC1","MDP1","MERTK","METTL4","MGA","MGAM","MICALCL","MKX","MPG","MPO","MPP3","MRFAP1","MROH5","MRPL3","MRPS9","MSLN","MTNR1A","MTOR","MUC1","MUC3A","MUC6","MUC7","MX2","MYC","MYCBP","MYCBP2","MYCBPAP","MYCT1","MYH1","MYLK3","MYO9B","MYOM2","NAT1","NBAS","NCAPD3","NDP","NDUFS1","NEDD8","NEDD8.MDP1","NEFM","NF2","NLRP14","NPL","NRDE2","NUP93","OR2T3","OR2T33","OR5K3","ORC1","OSTN","PAPLN","PC","PCLO","PCNXL3","PDE4A","PDE4DIP","PDE6B","PDK4","PER1","PEX2","PF4","PFAS","PIDD1","PIP","PKD1L2","PKHD1L1","PLN","POLL","POSTN","PPL","PRAME","PRB4","PRR21","PSEN2","PSMD5","PTPN13","PTPN22","PTS","RAB40A","RABEP1","RAD54L2","RAN","RASGRP2","RASGRP3","RASGRP4","RASIP1","RBBP8","RC3H1","RECQL","REXO1","RFX1","RGS2","RIN2","RP2","RPL3L","RPS6","RPS9","RSPH1","RTTN","SARS","SCAF1","SCAP","SEPN1","SET","SF1","SGIP1","SH3TC1","SI","SLC25A2","SLC25A4","SLC25A40","SLC25A41","SLC25A46","SLC25A47","SLC2A11","SLC2A9","SLC39A5","SLC6A17","SLN","SMC1B","SNCAIP","SNTB1","SOS2","SOX3","SPEF2","SPN","SQRDL","SRRM3","STAR","STEAP3","STX17","SULT1C4","SYP","SYTL2","TAF6","TANC1","TBC1D14","TBC1D16","TBC1D2","TBP","TG","TMEM128","TMEM52B","TNFRSF10C","TNFSF18","TNXB","TOMM20","TOMM20L","TPCN2","TPR","TRIM23","TSSC4","TTC16","TTC37","U2AF1","UBQLN3","UCN","USP1","USP4","USP6","UTY","VCX","VPS13B","VWA3A","WIPI2","WNT9B","WWP2","ZBTB2","ZBTB39","ZCCHC14","ZNF2","ZNF20","ZNF22","ZNF273","ZNF284","ZNF3","ZNF407","ZNF44","ZNF568","ZNF587","ZNF600","ZNF77","ZNF780B"]

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
#genInd = [87,93,99,105]

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

    #Open input stream
    inFile = open(file)
    for i, current in enumerate(csv.reader(inFile)):
        if i == 0:
            if not wroteHeader:
                writer.writerow(current)
                wroteHeader = True
            continue
        else:

            ############### Filter for individuals begin ###############
            starting_col = 183 #First subject column (should be the zygosity)
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

            #Checking minor allele frequency <= 0.01
            if not ( isfloat(current[19]) and (float(current[19]) >= 0.0 ) and (float(current[19]) <= 0.01) ):
                continue


            """(Anthony's note:) Below was originally commented out, it is kept in its original form
            #Tags all rows with "Filtered " as "Missing"
            #colInd = [86, 92 ,98, 104]
            #for j in colInd:
                #if j <= len(current):
                    #if current[j].find("Filtered ") != -1:
                        #current[j] = "Missing"
            """
            """(Anthony's record keeping) - do no disable since this is only for record keeping, I cannot guarantee its indentation is appropriate
            #Checking coding variant type
            #if "nonframeshift" not in current[8] or "synonymous" not in current[8] or "frameshift" in current[8] or "nonsynonymous" in current[8] or "splicing" in current[8] or "stopgain" in current[8] or "stoploss" in current[8] or "startloss" in current[8] or isEmpty(current[8]):

            #Checking SIFT <=0.25 OR PolyPhen >=0.95
            #if (isEmpty(current[SiftInd]) and isEmpty(current[PPInd])) or (isfloat(current[SiftInd]) and float(current[SiftInd]) <= SIFT) or (isfloat(current[PPInd]) and float(current[PPInd]) >= PolyPhen) or (isEmpty(current[SiftInd]) and (isfloat(current[PPInd]) and float(current[PPInd]) >= PolyPhen)) or (isEmpty(current[PPInd]) and (isfloat(current[SiftInd]) and float(current[SiftInd]) <= SIFT)):

            #Checking BW <= 10
            #if (isfloat(current[ExConInd1]) and float(current[ExConInd1]) <= ExCon) or isEmpty(current[ExConInd1]):

                #Checking BY <= 10
                #if isEmpty(current[ExConInd2]) or  (isfloat(current[ExConInd2]) and float(current[ExConInd2]) <= ExCon):

            """

            #The only way to get here is if ALL criteria are met, so that row is added to the list that will be written to file later
            writer.writerow(current)
    #Close input stream and indicate to User
    inFile.close()
    print("Done with " + file)

print("Done filtering all files above. Results can be found in the file resultsPASS.csv")
outfile.close()
