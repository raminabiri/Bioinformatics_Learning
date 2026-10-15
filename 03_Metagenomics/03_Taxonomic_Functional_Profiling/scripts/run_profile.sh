#!/usr/bin/env bash
# Module 03/03 — taxonomic profiling with Kraken2 + Bracken (practice database).
# Run from 03_Metagenomics/ after module 02 and build_practice_db.sh.
# Usage: CONF=0.1 bash 03_Taxonomic_Functional_Profiling/scripts/run_profile.sh [sample ...]
set -euo pipefail
DB=${DB:-work/03_profile/kraken2_practice_db}
CONF=${CONF:-0}
IN=work/02_host/clean; K=work/03_profile/kraken; BR=work/03_profile/bracken
mkdir -p $K $BR
samples=("$@"); [ ${#samples[@]} -gt 0 ] || samples=(minigut minigut_sample2)
for s in "${samples[@]}"; do
  # Bracken needs the read length the k-mer distribution was built for
  L=$(set +o pipefail; zcat $IN/${s}_R1.fastq.gz | head -n 4000 | awk 'NR%4==2{n++; t+=length($0)} END{print (t/n>137)?150:125}')
  kraken2 --db "$DB" --threads 8 --paired --confidence "$CONF" \
          --report $K/${s}_c$CONF.kreport --output $K/${s}_c$CONF.kraken \
          $IN/${s}_R1.fastq.gz $IN/${s}_R2.fastq.gz 2> $K/${s}_c$CONF.log
  bracken -d "$DB" -i $K/${s}_c$CONF.kreport -o $BR/${s}_c$CONF.bracken -w $BR/${s}_c$CONF.breport \
          -r "$L" -l S -t 10 > $BR/${s}_c$CONF.log 2>&1
  printf "== %s (confidence %s, Bracken -r %s): %s\n" "$s" "$CONF" "$L" "$(grep -m1 ' classified' $K/${s}_c$CONF.log | sed 's/^ *//')"
done
