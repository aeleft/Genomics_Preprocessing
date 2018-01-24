#!/bin/bash
# ============================================================================
# Script that validates the output .csv file from tablemaking via comparing 
# it with a bash-generated table file that also counts the mutations.
#
# Date initiated:
# 
# ============================================================================

#File paths
VAR_FILE="?"
TABL_FILE="?"
SUMMARY_FILE="?"

#Variant file counting: defining the starting col for individual phenotype
START_PHENO_COL=184
#dbGaP_casecontrol:184; dbGaP_trios:84; NDAR:87 ; CONFIRM ON FILE EACH TIME


#Actual table counting: defining starting col and row
TABL_START_ROW=2
TABL_START_COL=3
#for dbGaP_casecontrol: row=2, col=3
#for dbGaP_trios: row=2, col=6
#for NDAR: row=2, col=6


##### BASH GENERATION PIPELINE #####

#Change the multiple genes in variant file to the single functional gene
echo "Isolating functional genes in variant file (`date`)"
funcGene_temp=`mktemp`
bash funcGene_replacement.sh $VAR_FILE $funcGene_temp

#Convert the genotypes to integer mutation counts
echo "Converting genotypes to integer mutation counts (`date`)"
intMut_temp=`mktemp`
bash genotype_2_mutCount.sh $funcGene_temp $intMut_temp
rm $funcGene_temp

#Count the number of mutations for each gene 
echo "Counting mutation sum from variant file (`date`)"
shGen_mutCount=`mktemp`
bash sum_mutCount.sh $intMut_temp $START_PHENO_COL > $shGen_mutCount
rm $intMut_temp

#Isolate only the gene & mutation count and sort
echo "Sorting genes and mutation count from variant file (`date`)"
shGen_mutCount_sorted=`mktemp`
head -n -2 $shGen_mutCount | sort > $shGen_mutCount_sorted 
rm $shGen_mutCount


##### ACTUAL TABLE VALIDATION #####
echo "Counting mutation sum in table file (`date`)"
tabl_mutCount_sorted=`mktemp`
bash columns_sums.sh $TABL_FILE $TABL_START_ROW $TABL_START_COL | sort > $tabl_mutCount_sorted



##### COMBINE INTO SUMMARY FILE #####
echo "Validation summary file generated on: `date`" > $SUMMARY_FILE
echo "" >> $SUMMARY_FILE

echo "==============================" >> $SUMMARY_FILE
echo "" >> $SUMMARY_FILE
echo "Genes exclusive to single file (bash generated, python generated):" >> $SUMMARY_FILE
comm -3 $shGen_mutCount_sorted $tabl_mutCount_sorted >> $SUMMARY_FILE
echo "" >> $SUMMARY_FILE

echo "==============================" >> $SUMMARY_FILE
echo "" >> $SUMMARY_FILE
echo "Genes & mutation count present in both files:" >> $SUMMARY_FILE
comm -12 $shGen_mutCount_sorted $tabl_mutCount_sorted >> $SUMMARY_FILE
echo "" >> $SUMMARY_FILE




