# python2.6
# ============================================================================
# Turns comma-separated file (.csv) into tab-separated file (.tsv)
#
# Input: stdin of the .csv file
#
# Output: stdout of the .tsv file
# ============================================================================

import csv, sys
csv.writer(sys.stdout, dialect='excel-tab').writerows(csv.reader(sys.stdin))

