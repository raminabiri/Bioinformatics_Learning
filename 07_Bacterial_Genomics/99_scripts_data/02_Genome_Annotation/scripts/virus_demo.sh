#!/usr/bin/env bash
# part 07, module 02, lesson 2 — an ORF-based gene caller on a eukaryotic RNA virus (SARS-CoV-2 reference NC_045512.2).
# Downloads ~30 kb FASTA + ~15 kb GFF3 from NCBI, runs Pyrodigal in meta mode (code 1), compares with RefSeq. ~2 s.
# Run inside the project folder:  cd ~/genomes && bash <course>/07_Bacterial_Genomics/99_scripts_data/02_Genome_Annotation/scripts/virus_demo.sh
set -euo pipefail
OUT=annotation/sarscov2
mkdir -p $OUT
[ -s $OUT/sc2.fna ] || curl -s -o $OUT/sc2.fna \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_045512.2&rettype=fasta&retmode=text"
[ -s $OUT/sc2.gff3 ] || curl -s -o $OUT/sc2.gff3 \
  "https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?db=nuccore&report=gff3&id=NC_045512.2"

echo "== reference CDS (start end strand gene)"
awk -F'\t' '$3=="CDS"{match($9,/gene=[^;]+/); print $4, $5, $7, substr($9,RSTART+5,RLENGTH-5)}' $OUT/sc2.gff3
echo "mature peptides (nsp1-16 etc.): $(grep -c 'mature_protein_region_of_CDS' $OUT/sc2.gff3)"
grep -oE 'Note=[^;]*frameshift[^;]*' $OUT/sc2.gff3 | sort -u

echo "== Pyrodigal (meta mode, code 1)"
pyrodigal -i $OUT/sc2.fna -p meta -g 1 -f gff -o $OUT/pyrodigal.gff
grep -v '^#' $OUT/pyrodigal.gff | awk -F'\t' '{print $4, $5, $7, ($5-$4+1)/3-1 " aa"}'
python3 "$(dirname "$0")/compare_genecalls.py" $OUT/sc2.gff3 $OUT/pyrodigal.gff | head -8
