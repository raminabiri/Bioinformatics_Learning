#!/usr/bin/env bash
# Summarise an ENA/SRA project per sample: number of runs, layouts, total reads.
# Usage: bash project_summary.sh PRJEB7774 > samples.tsv
# Note: ENA always puts run_accession first, whatever order you request,
#       so columns are looked up by header name, not by position.
set -euo pipefail
PROJECT=${1:?Usage: project_summary.sh <BioProject accession>}
curl -s "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=${PROJECT}&result=read_run&fields=sample_accession,library_layout,read_count&format=tsv" \
| awk -F'\t' '
  NR==1 { for (i=1; i<=NF; i++) col[$i]=i; next }
  {
    s=$col["sample_accession"]
    n[s]++; reads[s]+=$col["read_count"]
    lay[s] = (lay[s]=="" ? $col["library_layout"] : lay[s] "," $col["library_layout"])
  }
  END { for (s in n) print s"\t"n[s]"\t"lay[s]"\t"reads[s] }' \
| sort -k1,1 | { printf "sample\tn_runs\tlayouts\ttotal_reads\n"; cat; }
