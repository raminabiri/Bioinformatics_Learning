#!/usr/bin/env bash
# run_profile.sh (part 06, module 03): taxonomic profiling with Kraken2 + Bracken (practice database).
# Run inside the project folder (cd ~/meta) after module 02 and build_practice_db.sh.
# Usage: bash run_profile.sh [sample ...]            (default: minigut minigut_sample2)
#        CONF=0.1 bash run_profile.sh                 (Kraken2 --confidence 0.1)
# Outputs: profile/kraken/<sample>_c<CONF>.{kreport,kraken,log}
#          profile/bracken/<sample>_c<CONF>.{bracken,breport,log}
set -euo pipefail
DB=${DB:-profile/kraken2_practice_db}
CONF=${CONF:-0}
IN=host/clean
K=profile/kraken
BR=profile/bracken
mkdir -p $K $BR

samples=("$@")
[ ${#samples[@]} -gt 0 ] || samples=(minigut minigut_sample2)

for s in "${samples[@]}"; do
  # Bracken needs the read length its model was built for (125 or 150): estimate it from 1000 reads
  L=$(set +o pipefail; zcat $IN/${s}_R1.fastq.gz | head -n 4000 \
      | awk 'NR%4==2 {n++; t+=length($0)} END {print (t/n > 137) ? 150 : 125}')
  kraken2 --db "$DB" --threads 4 --paired --confidence "$CONF" \
          --report $K/${s}_c$CONF.kreport --output $K/${s}_c$CONF.kraken \
          $IN/${s}_R1.fastq.gz $IN/${s}_R2.fastq.gz 2> $K/${s}_c$CONF.log
  bracken -d "$DB" -i $K/${s}_c$CONF.kreport -o $BR/${s}_c$CONF.bracken -w $BR/${s}_c$CONF.breport \
          -r "$L" -l S -t 10 > $BR/${s}_c$CONF.log 2>&1
  printf "== %s (confidence %s, Bracken -r %s): %s\n" "$s" "$CONF" "$L" \
         "$(grep -m 1 ' classified' $K/${s}_c$CONF.log | sed 's/^ *//')"
done
