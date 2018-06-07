# Simple Validation for Tablemaking

The script here help automate a simple validation step to check the validity of the tablemaking pipeline's output.


## Usage Instruction

#### Taking the mutation sum for each gene in the table
- After running the tablemaking pipeline, we can find the *total* number of mutation present within each gene by taking the sum of each of the columns in the output table file
- The specifics of the `columns_sums` script is described in the script header (i.e. the first few lines of the actual `columns_sums.sh` script file), but in short the summation is done via running:

  `bash columns_sums.sh table.csv rowIdx colIdx > column_sum_file.txt`

#### Re-Generate mutation counts for a subset of genes from variant file
- As a method of comparison, we will count, using an alternative method, mutation count for a subset of genes which we can compare with the table-generated mutation count to make sure both ways reach the same total mutation counts
- This is done very simply by using the `grep` shell function. It has been automated in the script `generateGrepReport.sh`, which is used as follows:
  1. Before running the script, the user must set the following variables:
    - `VAR_FILE`: a string describing the path to the filtered variant file from which the table was made
    - `arr`: an array of genes that the user wants to check mutation counts for. One could look at the output file from `columns_sums.sh` to randomly select a list of genes
  2. The user than runs the script as follows:

    `bash generateGrepReport.sh > grep_report.txt`

- After the output summary file (*"grep_report.txt"*) has been generated, the user can compare the occurrences of the string sequences for *"Heterozygote"*, *"Homozygote"* and *"Trizygote"* for each of the specified genes with the total mutation count of the table file.


#### Comparing mutation sum and re-generated mutation count
- If we follow the above two steps, the `generateGrepReport.sh` script will produce a file named `grep_report.txt`, which contains a list of genes and the number of *"Heterozygote"*, *"Homozygote"* and *"Trizygote"* for each of those genes
  - Compute the total number of mutation count for a given gene based on its number of *"Heterozygote"*, *"Homozygote"* and *"Trizygote"*
    - As an example, if we assume *"Heterozygote"*, *"Homozygote"* and *"Trizygote"* maps to 1, 2 and 3 mutation counts, respectively, a gene with 1 *"Heterozygote"*, 1 *"Homozygote"* and 1 *"Trizygote"* mutations will have a total mutation count of `1*1 + 1*2 + 1*3 = 6`
  - After this step, we will have a "ground-truth" total mutation count for each of the genes we specified
- For each of the genes we selected, we can then check for their overall mutation count in the `column_sum_file.txt` file (the file produced by the `columns_sums.sh` script)
    - To look at the mutation count for a specific gene (e.g. "*GENE1*"), we enter the following into the command line:

    `grep GENE1 column_sum_file.txt`

    - The above command generates a output indicating the total mutation count of that gene (e.g. "*GENE1*") that was counted by our tablemaking pipeline
- If the tablemaking pipeline is functioning correctly, the output of the two methods above should match in terms of total mutation counts



## Note
- For each of the specified gene (e.g. in `arr`), the `generateGrepReport.sh` script does the following:
  - Takes a sub-section of the filtered variant file via the `getGeneSubfile.py` script, the subfile only contains variants with the current gene of interest
  - Perform `grep -o` on the sub-sectioned file for the terms *"Heterozygote"*, *"Homozygote"* and *"Trizygote"* , counting the occurrences of each of the terms in the sub-sectioned file.
