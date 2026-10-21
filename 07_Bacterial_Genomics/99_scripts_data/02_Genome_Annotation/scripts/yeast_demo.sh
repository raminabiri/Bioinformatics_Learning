#!/usr/bin/env bash
# part 07, module 02, lesson 3 — what a prokaryote gene caller does to a eukaryote chromosome.
# Downloads S. cerevisiae S288C chromosome I (NC_001133.9, ~230 kb FASTA + ~200 kb GFF3) from NCBI,
# runs Pyrodigal (standard code 1) and compares with the reference annotation. ~5 s after download.
# Run inside the project folder:  cd ~/genomes && bash <course>/07_Bacterial_Genomics/99_scripts_data/02_Genome_Annotation/scripts/yeast_demo.sh
set -euo pipefail
OUT=annotation/yeast
mkdir -p $OUT
[ -s $OUT/chrI.fna ] || curl -s -o $OUT/chrI.fna \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_001133.9&rettype=fasta&retmode=text"
[ -s $OUT/chrI.gff3 ] || curl -s -o $OUT/chrI.gff3 \
  "https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?db=nuccore&report=gff3&id=NC_001133.9"

echo "== reference: feature types"
grep -v '^#' $OUT/chrI.gff3 | cut -f3 | sort | uniq -c | sort -nr | head -8
echo "== genes with more than one CDS segment (= introns)"
awk -F'\t' '$3=="CDS"{split($9,a,";"); c[a[1]]++; if (match($9,/gene=[^;]+/)) g[a[1]]=substr($9,RSTART+5,RLENGTH-5)} END{for(k in c) if(c[k]>1) print g[k], c[k]" exons"}' $OUT/chrI.gff3

echo "== Pyrodigal (single mode, genetic code 1) vs reference"
pyrodigal -i $OUT/chrI.fna -g 1 -f gff -o $OUT/pyrodigal.gff
python3 "$(dirname "$0")/compare_genecalls.py" $OUT/chrI.gff3 $OUT/pyrodigal.gff | head -9

echo "== the three intron-containing genes: reference CDS segments vs Pyrodigal"
for g in EFB1 SNC1 TFC3; do
  read -r s e st < <(awk -F'\t' -v g="gene=$g;" '$3=="CDS" && index($9,g){print $4, $5, $7}' $OUT/chrI.gff3 \
                     | awk 'NR==1{s=$1; e=$2} {if($1<s)s=$1; if($2>e)e=$2; st=$3} END{print s, e, st}')
  ref_aa=$(awk -F'\t' -v g="gene=$g;" '$3=="CDS" && index($9,g){n+=$5-$4+1} END{print n/3-1}' $OUT/chrI.gff3)
  pred=$(awk -F'\t' -v s=$s -v e=$e -v st=$st '!/^#/ && $7==st && $4<=e && $5>=s {printf "%s-%s (%d aa) ", $4, $5, ($5-$4+1)/3-1}' $OUT/pyrodigal.gff)
  echo "$g  reference ${s}-${e} ${st} (${ref_aa} aa)   Pyrodigal: ${pred:-none}"
done
