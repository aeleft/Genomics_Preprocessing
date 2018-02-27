#!/bin/bash
# ============================================================================
# Script that takes a .csv gene file and sums up the number of mutation for
# 	each gene of each individual.
#
# Assumption:
#	- The .csv file has the following format:
#		Fam_ID 	|	[indv_1]	| 	[indv_2]	|	...
#		--------|---------------|---------------|----------
#		Gender	|				|				|	...
#		--------|---------------|---------------|----------
#		Gene_1	|	[mut_count]	| 	[mut count]	|	...
#		--------|---------------|---------------|----------
#		Gene_1	|				|				|	
#			...
#
#	- That is to say, the gene & mutation count starts on the 3rd row
#	
# Input:	$1 - Filename of the input .csv file
# Output: 	print-out to stdout the .csv file with unique genes (summed mut)
# ============================================================================

VAR_FILE=$1

awk -F, '
	#Print the entire first line
	NR<=2{print $0}
	
	#For the first line of genes
	NR==3{
		gene=$1;
		for (i=2; i<=NF; i++) c[i]=$i;
	}

	#For the rest of the lines
	NR>3{
		#If the current row has the same gene as before
		if(gene==$1){
			#Add up counts
			for (i=2; i<=NF; i++) c[i]+=$i;
		}
		#If the current row has a new gene
		else{
			#print out the currently existing genes
			ORS="" ;
			print gene"," ;
			for (i=2; i<NF; i++) print c[i]"," ;
			
			#print out the last individual
			ORS="\n" ;
			print c[NF] ;
			
			#Reset the counter for new gene
			for (i=2; i<=NF; i++) c[i]=$i ;
			#Set up new gene
			gene=$1 ;
		}
	}
	#Finally, print out the last gene
	END{
		ORS="" ;
		print gene"," ;
		for (i=2; i<NF; i++) print c[i]"," ;
		ORS="\n" ;
		print c[NF] ;
	}
' $VAR_FILE
