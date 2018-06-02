# Simple Validation for Tablemaking

The script here help automate a simple validation step to check the validity of the tablemaking pipeline's output.

## Usage Instruction

#### Taking the mutation sum for each gene in the table
- After running the tablemaking pipeline, we can find the *total* number of mutation present within each gene by taking the sum of each of the columns in the output table file
- The specifics of the `columns_sums` script is described in its header, but in short the summation is done via running:

  `bash columns_sums.sh table.csv rowIdx colIdx > column_sum_file.txt`

#### Re-Generate mutation counts for a subset of genes from variant file
- As a method of comparison, we will count, using an alternative method, mutation count for a subset of genes which we can compare with the table-generated mutation count to make sure both ways reach the same total mutation counts
- This is done very simply by using the `grep` shell function. It has been automated in the script `generateGrepReport.sh`, which is used as follows:
  1. Before running the script, the user must set the following variables:
    - `VAR_FILE`: path to the filtered variant file from which the table was made
    - `arr`: an array of genes that the user wants to check mutation counts for. One could look at the output file from `columns_sums.sh` to randomly select a list of genes
  2. The user than runs the script as follows:

    `bash generateGrepReport.sh > grep_report.txt`
- After the output summary file (*"grep_report.txt"*) has been generated, the user can compare the occurrences of the string sequences for *"Heterozygote"*, *"Homozygote"* and *"Trizygote"* for each of the specified genes with the total mutation count of the table file.

## Note
- For each of the specified gene (e.g. in `arr`), the `generateGrepReport.sh` script does the following:
  - Takes a sub-section of the variant file via `grep` that just contains the current gene of interest
  - Perform `grep -o` on the sub-sectioned file for the terms *"Heterozygote"*, *"Homozygote"* and *"Trizygote"* , counting the occurrences of each of the terms in the sub-sectioned file.
- Sometimes, since there can be multiple genes per row, but the table only takes into account the functional gene (unique per row), `grep` causes multiple genes to be included in the sub-sectioned file for a particular gene. In this case, one would look at the mutation count (in the table file) of the other gene(s) as well to see if the total count makes sense.
