#!/usr/bin/env bash
# Download the shared dataset for part 03 (Metagenomics).
# Source: nf-core/test-datasets, branch "mag" — subsampled human gut metagenome (2 samples, Illumina PE)
#         plus a 10 kb region of human chr21 (hg38) used as a toy host reference.
# Usage: bash 06_Metagenomics/data/download.sh   (run from anywhere)
set -euo pipefail
cd "$(dirname "$0")"
BASE=https://raw.githubusercontent.com/nf-core/test-datasets/mag
mkdir -p raw host

for s in test_minigut test_minigut_sample2; do
  for r in R1 R2; do
    out="raw/${s#test_}_${r}.fastq.gz"
    [ -s "$out" ] || wget -q --show-progress -O "$out" "$BASE/test_data/${s}_${r}.fastq.gz"
  done
done
[ -s host/host_chr21_region.fa ] || wget -q -O host/host_chr21_region.fa "$BASE/host_reference/genome.hg38.chr21_10000bp_region.fa"
# A second human region (GRCh38 chr1:100,000,001-100,300,000) that is NOT in the host index:
# used in module 02 to demonstrate what an incomplete host reference misses.
[ -s host/human_chr1_region.fa ] || curl -s -o host/human_chr1_region.fa \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000001.11&rettype=fasta&retmode=text&seq_start=100000001&seq_stop=100300000"

md5sum raw/*.fastq.gz host/*.fa
echo "Done. Files in $(pwd)/raw and $(pwd)/host"
