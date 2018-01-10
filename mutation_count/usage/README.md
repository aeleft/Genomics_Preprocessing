# Tablemaking

The scripts here are used to count the mutation per individual.

The processing pipeline is as follows:
```flow
st=>start: Start
op=>operation: Your Operation
e=>end

raw_result=>start: Raw filtered result
cond_count=>operation: Mutation count (e.g. merge_file_transposed.csv)
uniq_count=>operation: Summed mutation count for each unique gene
table=>end: Transposed table with summed mutation for each unique gene

raw_result->cond_count->uniq_count->table
```


