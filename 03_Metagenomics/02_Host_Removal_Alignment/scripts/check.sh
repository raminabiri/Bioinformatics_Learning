#!/usr/bin/env bash
# Self-check for module 03/02. Run from 03_Metagenomics/ after run_host_removal.sh (all samples + minigut_spiked).
set -uo pipefail
ok=0; bad=0; pass(){ echo "  [OK]   $1"; ok=$((ok+1)); }; fail(){ echo "  [FAIL] $1"; bad=$((bad+1)); }
cnt(){ zcat "$1" 2>/dev/null | awk 'END{print NR/4}'; }
for s in minigut minigut_sample2; do
  a=$(cnt work/01_qc/trimmed/${s}_R1.fastq.gz); b=$(cnt work/02_host/clean/${s}_R1.fastq.gz); c=$(cnt work/02_host/clean/${s}_R2.fastq.gz)
  [ "$b" = "$c" ] && pass "$s: R1/R2 paired ($b)" || fail "$s: R1 $b != R2 $c"
  [ "$a" = "$b" ] && pass "$s: no bacterial pair removed ($b of $a kept)" || fail "$s: $((a-b)) pairs removed — expected 0 (no human reads in this sample)"
done
f=work/02_host/clean/minigut_spiked_R1.fastq.gz
if [ -s "$f" ]; then
  src=$(zcat $f | awk 'NR%4==1' | sed -E 's/^@?(HUMAN_chr[0-9]+|NC_[0-9.]+).*/\1/' | sort | uniq -c)
  h21=$(echo "$src" | awk '$2=="HUMAN_chr21"{print $1}'); h21=${h21:-0}
  bac=$(echo "$src" | awk '$2 ~ /^NC_/{s+=$1} END{print s+0}')
  [ "$h21" -le 10 ] && pass "spiked: chr21 human pairs left = $h21 (<=10)" || fail "spiked: $h21 chr21 human pairs left — did you use --un-conc?"
  [ "$bac" = 49845 ] && pass "spiked: all 49845 bacterial pairs kept" || fail "spiked: bacterial pairs kept = $bac (expected 49845)"
else fail "spiked sample not processed (make_spiked_sample.sh + run_host_removal.sh minigut_spiked)"; fi
for s in minigut minigut_sample2; do [ -s work/02_host/bam/$s.host.bam.bai ] && pass "$s BAM indexed" || fail "$s BAM index missing"; done
echo "Result: $ok passed, $bad failed"; [ $bad -eq 0 ]
