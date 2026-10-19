#!/usr/bin/env bash
# Count reads and mean read length in one or more FASTQ(.gz) files.
# Usage: bash count_reads.sh file1.fastq.gz [file2.fastq.gz ...]
set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: bash count_reads.sh file1.fastq.gz [file2 ...]" >&2
  exit 1
fi

printf "sample\treads\tmean_length\n"
for f in "$@"; do
  if [ ! -s "$f" ]; then
    echo "Error: file '$f' not found or empty" >&2
    exit 1
  fi
  name=$(basename "$f" .fastq.gz)
  zcat "$f" | awk -v s="$name" 'NR%4==2 {n++; L+=length($0)} END{printf "%s\t%d\t%.1f\n", s, n, L/n}'
done
