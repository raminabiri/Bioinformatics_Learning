#!/usr/bin/env bash
# Data for module 01/01 (Bash): E. coli K-12 MG1655 reference genome + annotation (~3 MB download).
# Same genome as part 00 (gene tour). Run: bash 01_Computing_Foundations/01_Bash_Linux/data/download.sh
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -s ecoli_k12.fna ]; then
  datasets download genome accession GCF_000005845.2 --include genome,gff3 --no-progressbar --filename ecoli_k12.zip
  unzip -oq ecoli_k12.zip
  mv ncbi_dataset/data/GCF_000005845.2/GCF_000005845.2_ASM584v2_genomic.fna ecoli_k12.fna
  mv ncbi_dataset/data/GCF_000005845.2/genomic.gff ecoli_k12.gff
  rm -rf ncbi_dataset ecoli_k12.zip README.md md5sum.txt
fi
md5sum ecoli_k12.fna ecoli_k12.gff
