# Filtering

The scripts here are used to filter tab-delimited genetic variant file(s) (typically with filename extension "_.output_") to generate a single output file containing only variants that meet the specified criteria.

**Dependencies**: runs using python 2

## Repository Overview
- The following scripts are used to do filtering for the various datasets. Note that I (Anthony) am not the original author of these scripts. I only uploaded the scripts here such that the entire pre-processing can be in one place.
  - `filtering_dbGaP_casecontrol_dataset.py`: used to filter the dbGaP_casecontrol dataset
  - `filtering_dbGaP_trios_dataset.py`: used to filter the dbGaP_trios dataset
  - `filtering_NDAR_dataset.py`: used to filter the NDAR dataset
- `singleFile_filtering.py`
  - This is written by me (Anthony) and used to generate a filtered output of a single file. This is sometimes used to validate that the filtered output from the above scripts are correct


## Running the Filtering Pipeline

1. Move the filtering script into the same directory as the unfiltered genetic variants (typically a directory which contains a number of "_.output_" files from various chromosomes)
    - The script should correspond with the dataset. For example, given a dbGaP_casecontrol dataset, we will using the `filtering_dbGaP_casecontrol_dataset.py` script
2. Set the wanted variables for what to filter (the below can either be set via changing values of variables within the script)
    - `APPLY_GENE_FILTER`: whether or not to filter only for genes specified by the list `genes`
    - The `coding_variant_types` variable specifies the coding variant types (e.g. "frameshift_deletion", "frameshift_insertion", etc.) to be included
    - `COVCRI_FILTER`: whether or not to apply coverage criteria filters. If an individual does not meet the coverage criteria (specified in the script to filter for number of variant reads, depth of sequencing and proportion of variant reads), his/her zygosity status in the filtered file will be changed (i.e. to say "Failed")
    - genotype quality: filter only for variants with a genotype quality higher than the one specified in the variable `genotypeQual`
    - coding variant type: filter only for variants with a specific coding type (e.g. "exonic", "intronic_splicing", etc.)
    - Minor allele frequency: the appropriate range of minor allele frequency that should be included
3. Run the script via executing the script using _Python_ in command line:

  `python filtering_script_for_corresponding_dataset.py`

4. After the script has finished running, it will generate an output file named "**resultsPASS.csv**" which contains all the filtered variants
    - For good practice, we typically rename the filtered result file to be something more specific, and move both the filtering script and the filtered result file  to a separate directory for the next step of analysis.
    - Note that we typically use a new copy of the filtering script for each analysis, since it allows us to keep track of the filtering criterias applied to each dataset.


## Validating the filtering pipeline
If needed, the filtered output file can be checked for validity as follows:

1. Configure the script `singleFile_filtering.py` such that its parameters are identical to the filtering criteria you want. The parameters include:
    - _Coding variant types_, denoted by variable `WANTED_CVTs`
    - _Variant functional types_, denoted by variable `WANTED_VFTs`
    - _Minor allele frequencies_, denoted by `MAF_lowerBound` and `MAF_upperBound`
    - \*Note that the column index (in the filtered variant file) to look for the above criteria can also be customized, as well as the delimiter (e.g. comma vs. tab-delimited)
2. Run the validation as follows:

  `python singleFile_filtering.py path_to_filtered_variant_file.csv output_file.csv`

3. Check that the output_file.csv from the current run has the same number of lines as the filtered variant file. The assumption is that if the filtered variant file only has variants that meet the criteria, running it through an additional filtering script with the same criteria should not result in any additional variants to be filtered.
    - Note that the line checking can be done via the bash `wc -l [filename]` command
