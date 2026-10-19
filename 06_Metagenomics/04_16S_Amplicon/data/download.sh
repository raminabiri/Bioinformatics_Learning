#!/usr/bin/env bash
# Download the data for module 03/04 (16S amplicon).
# Reads: QIIME 2 "Atacama soil microbiome" tutorial, 1% subsample (EMP paired-end protocol, 16S V4, 515F/806R,
#        Illumina MiSeq 2x151). Neilson et al. 2017, mSystems, doi:10.1128/mSystems.00195-16.
# Reference: SILVA 138 (99%), trimmed to the 515F/806R region, prepared by the QIIME 2 team (Robeson et al. 2021).
# Total ~53 MB. Usage: bash 06_Metagenomics/04_16S_Amplicon/data/download.sh   (run from anywhere)
set -euo pipefail
cd "$(dirname "$0")"
Q=https://data.qiime2.org/2024.10
mkdir -p raw db

for f in forward reverse barcodes; do
  [ -s raw/$f.fastq.gz ] || curl -sSL -o raw/$f.fastq.gz "$Q/tutorials/atacama-soils/1p/$f.fastq.gz"
done
[ -s sample_metadata.tsv ] || curl -sSL -o sample_metadata.tsv "$Q/tutorials/atacama-soils/sample_metadata.tsv"
for f in seqs tax; do
  [ -s db/silva-138-99-$f-515-806.qza ] || curl -sSL -o db/silva-138-99-$f-515-806.qza "$Q/common/silva-138-99-$f-515-806.qza"
done

md5sum -c - <<'EOF'
b5ee4718605158e5db91ef906fb61f62  raw/forward.fastq.gz
2ac4ca47f39ebc9f517396c051257342  raw/reverse.fastq.gz
df32df8dc627319d7bc1d9ce49b89849  raw/barcodes.fastq.gz
380b04ad294f043b283ada11f42c011f  sample_metadata.tsv
a914837bc3f8964b156a9653e2420d22  db/silva-138-99-seqs-515-806.qza
e2c40ae4c60cbf75e24312bb24652f2c  db/silva-138-99-tax-515-806.qza
EOF
echo "Done. Next, from 06_Metagenomics/: bash 04_16S_Amplicon/scripts/train_classifier.sh (once), then bash 04_16S_Amplicon/scripts/run_16s.sh"
