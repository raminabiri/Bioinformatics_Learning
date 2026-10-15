#!/usr/bin/env bash
# Module 03/04 — train a genus-level Naive Bayes classifier on SILVA 138 (99%) trimmed to 515F/806R (V4).
# Run once, from the part folder:  cd 03_Metagenomics && bash 04_16S_Amplicon/scripts/train_classifier.sh
# Why train locally: a classifier only works with the scikit-learn version it was trained with
#   (QIIME 2 2026.7 has sklearn 1.7.1; older downloaded classifiers were made with 1.4.2 and are refused).
# Why genus level: species-level SILVA V4 has 67,689 taxonomy classes and training needed >12 GB RAM;
#   genus level has 8,415 classes (5.5 GB RAM, 8 min on the course server). A 250-bp V4 read rarely resolves species anyway.
# PRACTICE ONLY: for research use the full SILVA/GTDB/Greengenes2 references (see lesson, section 5).
set -euo pipefail
DB=04_16S_Amplicon/data/db
[ -s $DB/silva-138-99-seqs-515-806.qza ] || { echo "Run from 03_Metagenomics/ after 04_16S_Amplicon/data/download.sh"; exit 1; }
qiime --version | head -1

if [ ! -s $DB/silva-138-99-tax-515-806-genus.qza ]; then
  echo "== 1. Drop the species rank from the taxonomy"
  tmp=$(mktemp -d)
  qiime tools export --input-path $DB/silva-138-99-tax-515-806.qza --output-path "$tmp" >/dev/null
  sed 's/; s__[^\t]*$//' "$tmp/taxonomy.tsv" > "$tmp/genus.tsv"
  qiime tools import --type 'FeatureData[Taxonomy]' --input-path "$tmp/genus.tsv" \
    --output-path $DB/silva-138-99-tax-515-806-genus.qza
  rm -r "$tmp"
fi

echo "== 2. Train (chunk size 10000 keeps memory lower)"
qiime feature-classifier fit-classifier-naive-bayes \
  --i-reference-reads $DB/silva-138-99-seqs-515-806.qza \
  --i-reference-taxonomy $DB/silva-138-99-tax-515-806-genus.qza \
  --p-classify--chunk-size 10000 \
  --o-classifier $DB/silva-138-99-515-806-genus-nb.qza
