#!/usr/bin/env bash
# Self-check for module 03/04. Run from 06_Metagenomics/ after run_16s.sh (or your own commands, same file names).
set -uo pipefail
OUT=work/04_16s; E=$OUT/exports; ok=0; bad=0
pass(){ echo "  [OK]   $1"; ok=$((ok+1)); }
fail(){ echo "  [FAIL] $1"; bad=$((bad+1)); }
for f in demux.qza table.qza rep-seqs.qza denoising-stats.qza taxonomy.qza rooted-tree.qza \
         core-metrics-results/unweighted_unifrac_distance_matrix.qza core-metrics-results/faith_pd_vector.qza; do
  [ -s $OUT/$f ] && pass "$f" || fail "$f missing"
done
if [ -s $E/stats/stats.tsv ]; then
  read -r inp merged < <(awk -F'\t' 'NR>2{i+=$2; m+=$6} END{print i, m}' $E/stats/stats.tsv)
  [ "$inp" = 46712 ] && pass "demultiplexed reads entering DADA2 = 46712" || fail "reads entering DADA2 = $inp (expected 46712: check --p-rev-comp-mapping-barcodes)"
  [ "$merged" = 16438 ] && pass "merged reads = 16438" || fail "merged reads = $merged (expected 16438 with trim 13 / trunc 150)"
else fail "$E/stats/stats.tsv missing (run step 7 of run_16s.sh)"; fi
if [ -s $E/rep-seqs/dna-sequences.fasta ]; then
  n=$(grep -c '>' $E/rep-seqs/dna-sequences.fasta)
  [ "$n" = 414 ] && pass "414 ASVs" || fail "$n ASVs (expected 414)"
  l=$(awk '!/^>/{print length($0)}' $E/rep-seqs/dna-sequences.fasta | sort | uniq -c | sort -nr | awk 'NR==1{print $2}')
  [ "$l" = 227 ] && pass "modal ASV length 227 (= 253-bp amplicon - 2 x 13 trimmed)" || fail "modal ASV length $l (expected 227)"
fi
if [ -s $E/taxonomy/taxonomy.tsv ]; then
  g=$(awk -F'\t' 'NR>1 && $2 ~ /g__/' $E/taxonomy/taxonomy.tsv | wc -l)
  [ "$g" -ge 200 ] && pass "$g ASVs classified to genus" || fail "only $g ASVs classified to genus — wrong classifier?"
fi
if [ -s $E/adonis/adonis.tsv ]; then
  awk -F'\t' '$1=="elevation"{exit !($6<=0.01)}' $E/adonis/adonis.tsv && pass "adonis: elevation significant (p <= 0.01)" || fail "adonis: elevation not significant?"
fi
echo "Result: $ok passed, $bad failed"; [ $bad -eq 0 ]
