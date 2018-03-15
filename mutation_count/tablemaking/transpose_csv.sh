#!/bin/bash
# ============================================================================
# Script that takes a .csv file and transposes it.
#
# Input:	$1 - .csv file
# Output:	$2 - transposed .csv file
# ============================================================================

IN_FILE=$1
OUT_FILE=$2

awk -F, '
{
    for (i=1; i<=NF; i++)  {
        a[NR,i] = $i
    }
}
NF>p { p = NF }
END {
    for(j=1; j<=p; j++) {
        str=a[1,j]
        for(i=2; i<=NR; i++){
            str=str","a[i,j];
        }
        print str
    }
}' $IN_FILE > $OUT_FILE
