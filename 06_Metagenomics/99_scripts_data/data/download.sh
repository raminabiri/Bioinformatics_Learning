#!/usr/bin/env bash
# download.sh (part 06): fetch the shared data of part 06 into the current project folder.
# You only need this if you do NOT have the course copy of the reads
# (01_Linux/99_scripts_data/data/fastq, the same four files, identical md5).
# Usage: mkdir -p ~/meta && cd ~/meta && bash <course>/06_Metagenomics/99_scripts_data/data/download.sh
# Source: nf-core/test-datasets, branch "mag" (simulated gut metagenome, 2 samples, Illumina PE)
#         + two small regions of the human genome as a toy host reference (module 02).
set -euo pipefail
BASE=https://raw.githubusercontent.com/nf-core/test-datasets/mag
mkdir -p raw host/ref

for s in minigut minigut_sample2; do
  for r in R1 R2; do
    out=raw/${s}_${r}.fastq.gz
    [ -s "$out" ] || curl -sL -o "$out" "$BASE/test_data/test_${s}_${r}.fastq.gz"
  done
done

[ -s host/ref/host_chr21_region.fa ] || curl -sL -o host/ref/host_chr21_region.fa \
  "$BASE/host_reference/genome.hg38.chr21_10000bp_region.fa"
# GRCh38 chr1:100,000,001-100,300,000: NOT in the host index; shows what an incomplete reference misses
[ -s host/ref/human_chr1_region.fa ] || curl -s -o host/ref/human_chr1_region.fa \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000001.11&rettype=fasta&retmode=text&seq_start=100000001&seq_stop=100300000"

md5sum raw/*.fastq.gz host/ref/host_chr21_region.fa
echo "Expected md5: see README.md next to this script."
