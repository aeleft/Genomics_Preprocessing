#!/usr/bin/python2.6

"""
Adopted from Bill's script
- Originally created on Sun Dec 20 12:54:02 2015

Note:
    - Run with Python 2
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
import copy

INPUT_FILE = sys.argv[1]
SAMPLE_INFORMATION_FILE = "dbGAP.swedish.sampleinfo.csv"
APPLY_GENE_FILTER = True

BLANKS_2_MISSING=False


######################## Gene filter below ########################
if APPLY_GENE_FILTER == True:
    genes = ["ACE","ACKR2","ACR","ACY1","ADA","ADAM2","ADAMDEC1","ADAMTS14","ADCY9","ADGRF3","ADGRF5","AIP","AKAP1","ANKRD2","ANKRD24","ANKRD30A","ANXA1","ANXA11","APC2","AR","ARC","ARHGAP1","ARHGAP11A","ARL1","ARL11","ARL13B","ARNT","ASIP","ASTN1","ATAD2","ATF6B","BMP1","BOD1","BPI","BRAT1","BSX","BTAF1","BZRAP1","C1D","C1orf116","C1R","C2","C21orf33","C2orf71","C3","C3orf20","C5","C9","CAD","CALD1","CAMK1","CAMK1D","CAP1","CAPN12","CARD11","CAT","CCDC102B","CCDC114","CCDC13","CCDC155","CCDC17","CCDC3","CCDC78","CCK","CCKAR","CDCA8","CDH10","CDH12","CDH3","CDK1","CEP164","CFAP58","CFAP61","CHM","CIC","CKAP4","CMYA5","CNDP1","CP","CREB3","CRYBG3","CS","CSRP2","CSRP2BP","CTSO","CXCL1","DBN1","DCHS2","DCLRE1A","DDX20","DDX58","DEC1","DENND3","DHH","DNAH3","DNAJB1","DNAJC5","DOCK1","DPP6","DSC2","EAF1","EDN1","EIF3A","ELK3","ENAM","EPB41L4B","ERBB2","ERG","F10","F12","F2","F3","F5","FAM129B","FAM63A","FANCA","FAT2","FBXO24","FERMT3","FH","FLG","FLNC","FNDC1","FSD1","FUK","GABRR2","GAL","GJA1","GPAM","GPATCH8","GPRIN2","GRAP","GRAP2","GRB14","GRIK3","GRM2","GRP","GSN","HAPLN1","HAPLN3","HCN3","HECTD4","HERC1","HNRNPU","HPSE","HR","HSPA14","HTR6","ICA1","ID1","IGDCC4","IK","IL21","IL21R","IL3","IL32","IL4R","INF2","IRAK3","IRX6","ISG20L2","ITGB7","KCNE5","KCTD1","KDR","KIAA0754","KIDINS220","KIF18A","KIF27","KL","KLK1","KLKB1","KMT2D","KNTC1","KRT34","KRT7","KRT71","LARS","LBP","LRP11","LRRC31","LRRC56","MAGEA1","MAGI1","MAP3K1","MAP3K15","MAP4","MARCO","MCC","MDC1","MDP1","MERTK","METTL4","MGA","MGAM","MICALCL","MKX","MPG","MPO","MPP3","MRFAP1","MROH5","MRPL3","MRPS9","MSLN","MTNR1A","MTOR","MUC1","MUC3A","MUC6","MUC7","MX2","MYC","MYCBP","MYCBP2","MYCBPAP","MYCT1","MYH1","MYLK3","MYO9B","MYOM2","NAT1","NBAS","NCAPD3","NDP","NDUFS1","NEDD8","NEDD8.MDP1","NEFM","NF2","NLRP14","NPL","NRDE2","NUP93","OR2T3","OR2T33","OR5K3","ORC1","OSTN","PAPLN","PC","PCLO","PCNXL3","PDE4A","PDE4DIP","PDE6B","PDK4","PER1","PEX2","PF4","PFAS","PIDD1","PIP","PKD1L2","PKHD1L1","PLN","POLL","POSTN","PPL","PRAME","PRB4","PRR21","PSEN2","PSMD5","PTPN13","PTPN22","PTS","RAB40A","RABEP1","RAD54L2","RAN","RASGRP2","RASGRP3","RASGRP4","RASIP1","RBBP8","RC3H1","RECQL","REXO1","RFX1","RGS2","RIN2","RP2","RPL3L","RPS6","RPS9","RSPH1","RTTN","SARS","SCAF1","SCAP","SEPN1","SET","SF1","SGIP1","SH3TC1","SI","SLC25A2","SLC25A4","SLC25A40","SLC25A41","SLC25A46","SLC25A47","SLC2A11","SLC2A9","SLC39A5","SLC6A17","SLN","SMC1B","SNCAIP","SNTB1","SOS2","SOX3","SPEF2","SPN","SQRDL","SRRM3","STAR","STEAP3","STX17","SULT1C4","SYP","SYTL2","TAF6","TANC1","TBC1D14","TBC1D16","TBC1D2","TBP","TG","TMEM128","TMEM52B","TNFRSF10C","TNFSF18","TNXB","TOMM20","TOMM20L","TPCN2","TPR","TRIM23","TSSC4","TTC16","TTC37","U2AF1","UBQLN3","UCN","USP1","USP4","USP6","UTY","VCX","VPS13B","VWA3A","WIPI2","WNT9B","WWP2","ZBTB2","ZBTB39","ZCCHC14","ZNF2","ZNF20","ZNF22","ZNF273","ZNF284","ZNF3","ZNF407","ZNF44","ZNF568","ZNF587","ZNF600","ZNF77","ZNF780B"]
else:
    print "Gene filter disabled; initializing all exonic & intronic_splicing genes..."
    #Initialize a set for unique item collection (don't want repeated genes)
    exome_gene_set = Set([])
    #Open input stream from the input file
    geneRef_inStream = open(INPUT_FILE)
    geneRef_reader = csv.reader(geneRef_inStream, delimiter=',')
    geneRef_reader.next() #skip the first line (header)!
    #Iterate through the rows to get information
    for row in geneRef_reader:
        #Split the gene and annotation columns
        gene_list = [g for g in row[9].split("|")]
        anno_list = [a for a in row[10].split("|")]
        #Iterate through each gene and annotation combinations
        for gene, anno in [(g,a) for g in gene_list for a in anno_list]:
            #Split the annotation into parts for exact matching
            annoParts = anno.split(":")
            if (gene in annoParts) and ( ('exonic' in annoParts) or ('intronic_splicing' in annoParts) or ('exonic_splicing' in annoParts) ):
                exome_gene_set.add(gene) #If so, add gene to set!

    #Close input stream
    geneRef_inStream.close()
    genes = list(exome_gene_set)
####################################################################

#Print-line to let user know the genes initiated
print "======== Genes of interested initiated: ========"
print genes
print "================================================\n"


#Opens and stores information from the sample information file
with open(SAMPLE_INFORMATION_FILE,'rU') as sampleFile:
    #Initiate variables
    affectionStatus = "case"
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
outfile = open("merged_file_transposed.csv", "wb")
writer = csv.writer(outfile)
writer.writerow(idList)
writer.writerow(genderList)

#filters "dbGaP_results_PASS_cases.xls" row by row, if gene is in the gene list
#then codes mutations in to numbers and writes into merged file
mutationsList = []
geneList = []
with open(INPUT_FILE) as inFile:
    #Open and read the input file
    inFile_reader = csv.reader(inFile, delimiter=',')
    inFile_reader.next() #skip the first line (header)!
    #Iterate through each row of the input file
    for row in inFile_reader:
        #Check only the first detailed variant annotation
        anno_parts = (row[10].split("|")[0]).split(":")
        #Check the variant has the correct functional type
        if not ( ('exonic' in anno_parts) or ('intronic_splicing' in anno_parts) or ('exonic_splicing' in anno_parts) ):
            continue
        #Iterate through the parts of the annotation to find gene match
        for anno_part in anno_parts:
            if anno_part in genes:
                print anno_part #Let user know
                geneList.append(anno_part)
                mutationsList.append(anno_part)
                break
        #Check for the mutation number for the current variant row
        if len(mutationsList) > 0:
            for j in range(183,len(row),6):
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
                #Carry forward strings?
                if CARRY_FORWARD_MISSING and ( "Missing" in row[j] ):
                    mutationsNum = 'Missing'
                if CARRY_FORWARD_MISSING and ( "Grey-Fail" in row[j] ):
                    mutationsNum = 'Grey-Fail'
                mutationsList.append(mutationsNum)
            writer.writerow(mutationsList)
        del mutationsList[:]

outfile.close()



#os.remove('merged_columns.csv')
#os.remove('merged_file.csv')
#os.remove('merged_file_semifinal.csv')
#os.remove('merged_file_transposed.csv')

print("DONE!")
