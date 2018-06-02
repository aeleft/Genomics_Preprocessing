# Genomics_Preprocessing
This repository contains script used to build a pre-processing pipeline for large genomics datasets.

## Processing Pipeline
In short, the pre-processing pipeline has two main steps:
1. **Filtering**: Filtering of annotated genetic variant data
2. **Tablemaking**: Conversion of the variant data into a mutation count table, where the number of mutations per gene of each individual is specified

Both steps also have their corresponding validation pipelines, which heuristically checks for potential errors.

## Repository Description
- For the **Filtering** step, refer to the directory "_filtering_"
  - This directory contains both the filtering scripts and script used to validate the filtered output
- For the **Tablemaking** step, refer to the directory "*mutation_count*"
  - The "*mutation\_count/tablemaking*" directory contains the scripts to set up the tablemaking pipeline
  - The "*mutation_count/simpleValidation*" directory contains the script to set up a pipeline which attempts to validate the output of the tablemaking process
- Each sub-directory contains its own README's which instructs you on how to set up and run the pipelines.
