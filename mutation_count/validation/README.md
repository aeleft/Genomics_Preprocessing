# Validation
<span style="color:red">**The current repository is deprecated due to unknown bugs in the validation pipeline that produces discrepancies in the output mutation count. Use the _simpleValidation_ repository instead**</span>

The scripts here are used to validate that the mutation count is correct.

The validaiton pipeline from the original file is as follows:
```
Raw Filtered Result
	|
	|	funcGene_replacement.sh
	V
Raw Filtered Result with functional genes in the gene column
	|
	|	genotype_2_mutCount.sh
	V
Filtered Result with zygosities replaced with mutation integer numbers
	|
	|	sum_mutCount.sh
	V
File with mutation sum for each gene, and overall mutation quantity
```

The validation pipeline for the py-bash generated table is:
```
Generated table file
	|
	|	columns_sums.sh
	V
File with mutation sum for each gene
```

Finally, we compare the result from the two pipelines to check if we arrived at the same number of mutations per gene.



## Scripts Overview
**funcGene_replacement.sh**
- Takes in a .csv file and replaces the gene column (if there are multiple genes)
	- Replaced with the first gene in the detailed annotation column
- Outputs the same .csv file with the gene column replaced

**genotype_2_mutCount.sh**
- Simply does a search and replace on the file to convert zygosity to integer

**sum_mutCount.sh**
- Counts the mutation for each row (each row has only one gene) into a temp file
- Sum up the number of mutation for each unique gene from the temp file
- Get the total sum of all mutations from the temp file

**columns_sums.sh**
- Iterate over all rows and columns (after the user-specified indeces) to take the sum of each gene
