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


