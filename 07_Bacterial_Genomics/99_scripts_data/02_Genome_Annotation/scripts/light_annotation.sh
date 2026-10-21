#!/usr/bin/env bash
# part 07, module 02 — the fast parts of prokaryote annotation, on E. coli K-12 (genome from part 01), ~15 s total.
# Gene calling (Pyrodigal), rRNA (barrnap), tRNA (ARAGORN, tRNAscan-SE), then comparison with RefSeq.
# Run inside the project folder:  cd ~/genomes && bash <course>/07_Bacterial_Genomics/99_scripts_data/02_Genome_Annotation/scripts/light_annotation.sh
# Needs: pyrodigal, barrnap, aragorn, tRNAscan-SE (Bioconda); Python 3.
set -euo pipefail
HERE=$(dirname "$0")
G=${G:-$HERE/../../../../01_Linux/99_scripts_data/data}
OUT=annotation
[ -s $G/ecoli_k12.fna ] || { echo "Genome missing: bash $G/download.sh"; exit 1; }
mkdir -p $OUT

echo "== 1. Pyrodigal (single mode, translation table 11)"
pyrodigal -i $G/ecoli_k12.fna -g 11 -f gff -o $OUT/pyrodigal.gff -a $OUT/pyrodigal.faa
echo "predicted CDS: $(grep -vc '^#' $OUT/pyrodigal.gff)"

echo "== 2. Compare with RefSeq (same strand + same stop = same gene)"
python3 "$(dirname "$0")/compare_genecalls.py" $G/ecoli_k12.gff $OUT/pyrodigal.gff

echo "== 3. rRNA with barrnap"
barrnap --kingdom bac --threads 4 $G/ecoli_k12.fna > $OUT/barrnap.gff 2> $OUT/barrnap.log
grep -v '^#' $OUT/barrnap.gff | grep -oE 'Name=[^;]+' | sort | uniq -c

echo "== 4. tRNA with ARAGORN and tRNAscan-SE (bacterial model)"
aragorn -t -gc11 -w $G/ecoli_k12.fna -o $OUT/aragorn.txt
grep -m1 'genes found' $OUT/aragorn.txt
tRNAscan-SE -B --thread 4 -q --forceow -o $OUT/trnascan.txt $G/ecoli_k12.fna
echo "tRNAscan-SE: $(awk 'NR>3' $OUT/trnascan.txt | wc -l) tRNAs   RefSeq: $(awk -F'\t' '$3 == "tRNA"' $G/ecoli_k12.gff | wc -l)"
