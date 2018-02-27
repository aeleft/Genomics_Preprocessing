# Tablemaking

The scripts here are used to generate a table specifying the mutation count for each gene for each individual.

The processing pipeline is as follows:
```
Raw Filtered Result (variant file); Subject Information File
	|
	|	indvMut_extract.py
	V
Mutation Count File
	|
	|	geneMut_uniqSum.py
	V
Summed Mutation Count for each unique gene, transposed
	|
	|	transpose_csv.sh
	V
Finalized Table with Summed Mutation Count
```

---

## Running the tablemaking pipeline

#### Before you start

Check that the `subject_information_file.csv` is in the below format

| Subject_ID | Subject_info_B | Subject_info_C | ... |
|------------|----------------|----------------|-----|
| subj_id_1  | subj_info_B_1  | subj_info_C_1  | ... |
| ...        | ...            | ...            | ... |
| subj_id_n  | subj_info_B_n  | subj_info_C_n  | ... |

- Currently, we have assumed that the **1st column** of the above file specifies the individual subject IDs

In the `variant_file.csv`, locate the column which contains the subject IDs for each row:

| ... | Subject_IDs_column               | ... |
|-----|----------------------------------|-----|
| ... | subj_id_1;subj_id_2;subj_id_3;...| ... |

- Note that the subject IDs in this column should be *identical* to the subject IDs from the 1st column of the `subject_information_file.csv`
  - They are what is used to match mutation to subject
- We have assumed that the subject IDs within the column is delimited by **";"**
- Traditionally, the subject IDs can be found in columns (counting from index 0):
  - 182 for *dbGaP_casecontrol*
  - 82 for *dbGaP_trios*
  - 85 for *NDAR*


#### Running the pipeline
- Download the files from this repository into the *same* directory:
  - `wrapper_tablemaking.sh`
  - `indvMut_extract.py`
  - `geneMut_uniqSum.py`
  - `transpose_csv.sh`
- In the `wrapper_tablemaking.sh` file, update the following:
  - Path of the input variant file
  - Path of the input subject information file
  - Path to the output table file
  - The subject ID column index variable (see above section)
  - Date that the script is ran (to document for future reference)
- Run the script as follows:
```
bash wrapper_tablemaking.sh
```


---

## Overview
### Environment overview
- The python scripts are developed to work in `python 2.6`
- The shell script runs under `bash`

### Scripts overview
`indvMut_extract.py`
- Scripts reads through a subject information file first to store a list of subject IDs
- Then, it reads through the variant file:
  - for each variant, it looks at the subject ID in which the mutation occurs to output a mutation for that subject in the output file

`geneMut_uniqSum.py`
- Script reads through a .csv file with a gene a row, and columns depicting individuals and their mutation count for that gene
- For consecutive rows with the same gene name, the script condenses it into a single row while summing up the mutation count for each and every individual
- **Note** We assume that identical gene names will appear *consecutively*

`transpose_csv.sh`
- Transposes an input .csv file

---

### Notes
- None for now!
