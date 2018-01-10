# Tablemaking

The scripts here are used to count the mutation per individual.

The processing pipeline is as follows:
```
Raw Filtered Result
	|
	|	rawMutCount_condensor.py
	V
Mutation Count File (e.g. merge_file_transposed)
	|
	|	geneCol_merge.sh
	V
Summed Mutation Count for each unique gene
	|
	|	transpose_csv.sh
	V
Transposed Table with Summed Mutation Count
```

## Scripts Overview
**rawMutCount_condensor.py**
- Takes a _filtered_ .csv file as input 
- Optionally filters for genes one more time
- Condences each row of the file into just its gene and the mutation count for each individual in that row
	- Takes the text (e.g. Heterozygote) and translates it to a integer (e.g. "1")
- Outputs this condensed .csv file

**geneCol_merge.sh**
- Takes as input a .csv file with genes and mutation numbers for each individual for each gene
- Iterates over each row, for rows with identical genes, sum the two rows together into a single row
- Outputs a .csv file in the same format, but with unique genes, each with their summed mutation count for each individual
- Assumes that identical genes will always appear in consecutive rows

**transpose_csv.sh**
- Transposes a input .csv file


## Note
- The above pipeline can only sum integer mutation number, thus cannot perform the following function:
	- Compute logical assessment of handling strings such as "Missing", "Failed" and how the individual sum should be computed should these status appear in their mutation count



