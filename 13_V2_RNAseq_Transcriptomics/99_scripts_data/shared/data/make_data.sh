#!/usr/bin/env bash
# Shared data of part 13: the mini-genome (20 human gene loci, Ensembl 116) and 6 simulated RNA-seq samples.
# Usage (inside conda activate rnaseq):   bash make_data.sh ~/rnaseq
# Needs internet for Ensembl REST (about 2-12 minutes; Ensembl sometimes answers 500/503 and the script retries).
# Output: ref/ (mini_genome.fa, mini_genes.gtf, transcripts_all.fa, transcripts_canonical.fa, tx2gene.tsv)
#         reads/ (ctrl_1..3, dex_1..3 _R1/_R2.fastq.gz, truth_counts.tsv)   -- about 27 MB
# The read simulation uses a fixed random seed (13), so everybody gets the same reads.
set -euo pipefail
OUT=${1:-$HOME/rnaseq}
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT" && cd "$OUT"
python3 "$HERE/../scripts/make_mini_genome.py" "$HERE/genes.tsv" ref
python3 "$HERE/../scripts/simulate_reads.py" "$HERE/genes.tsv" ref/transcripts_canonical.fa reads
md5sum ref/transcripts_canonical.fa reads/truth_counts.tsv
echo "Done: $OUT/ref and $OUT/reads"
