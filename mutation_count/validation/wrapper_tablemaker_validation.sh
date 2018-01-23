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
bash sum_mutCount.sh $intMut_temp > $shGen_mutCount
rm $intMut_temp

#Isolate only the gene & mutation count and sort
echo "Sorting genes and mutation count from variant file (`date`)"
shGen_mutCount_sorted=`mktemp`
head -n -2 $shGen_mutCount | sort > $shGen_mutCount_sorted 
rm $shGen_mutCount


##### ACTUAL TABLE VALIDATION #####
echo "Counting mutation sum in table file (`date`)"
tabl_mutCount=`mktemp`
bash columns_sums.sh $TABL_FILE | sort > $tabl_mutCount_sorted



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




