#!/usr/bin/env bash
# Data for part 01_Linux (modules 03-10). Needs only curl, gzip and md5sum (no conda), about 12 MB.
#   - E. coli K-12 MG1655 reference genome (FASTA) and annotation (GFF), RefSeq GCF_000005845.2, from the NCBI FTP site
#   - two small simulated gut metagenome samples (FASTQ), from nf-core/test-datasets (branch "mag")
#   - a 500 kb region of human chr21 (FASTA with N), for exercise 11
# Usage: bash download.sh   (run from anywhere)
set -euo pipefail
cd "$(dirname "$0")"

NCBI=https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2
if [ ! -s ecoli_k12.fna ]; then
  curl -sS "${NCBI}_genomic.fna.gz" | gunzip -c > ecoli_k12.fna
fi
if [ ! -s ecoli_k12.gff ]; then
  curl -sS "${NCBI}_genomic.gff.gz" | gunzip -c > ecoli_k12.gff
fi

NFCORE=https://raw.githubusercontent.com/nf-core/test-datasets/mag
mkdir -p fastq
for s in minigut minigut_sample2; do
  for r in R1 R2; do
    out="fastq/${s}_${r}.fastq.gz"
    [ -s "$out" ] || curl -sS -o "$out" "$NFCORE/test_data/test_${s}_${r}.fastq.gz"
  done
done
[ -s host_chr21_region.fa ] || curl -sS -o host_chr21_region.fa "$NFCORE/host_reference/genome.hg38.chr21_10000bp_region.fa"

md5sum ecoli_k12.fna ecoli_k12.gff fastq/*.fastq.gz host_chr21_region.fa
echo "Done. Files are in $(pwd)"
