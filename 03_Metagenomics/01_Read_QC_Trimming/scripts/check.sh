#!/usr/bin/env bash
# Self-check for module 03/01. Run from 03_Metagenomics/ after run_qc.sh (or your own commands).
set -uo pipefail
OUT=work/01_qc; ok=0; bad=0
pass(){ echo "  [OK]   $1"; ok=$((ok+1)); }
fail(){ echo "  [FAIL] $1"; bad=$((bad+1)); }
for s in minigut minigut_sample2; do
  for r in R1 R2; do
    [ -s $OUT/fastqc_raw/${s}_${r}_fastqc.zip ]     && pass "FastQC raw $s $r"     || fail "FastQC raw $s $r missing"
    [ -s $OUT/trimmed/${s}_${r}.fastq.gz ]          && pass "trimmed $s $r"        || fail "trimmed $s $r missing"
    [ -s $OUT/fastqc_trimmed/${s}_${r}_fastqc.zip ] && pass "FastQC trimmed $s $r" || fail "FastQC trimmed $s $r missing"
  done
  j=$OUT/fastp_reports/$s.json
  if [ -s "$j" ]; then
    n1=$(zcat $OUT/trimmed/${s}_R1.fastq.gz | awk 'END{print NR/4}')
    n2=$(zcat $OUT/trimmed/${s}_R2.fastq.gz | awk 'END{print NR/4}')
    [ "$n1" = "$n2" ] && pass "$s: R1 and R2 still paired ($n1 reads each)" || fail "$s: R1 ($n1) != R2 ($n2) — pairs broken"
    kept=$(jq '.summary.after_filtering.total_reads / .summary.before_filtering.total_reads * 100' "$j")
    awk -v k="$kept" 'BEGIN{exit !(k>=95)}' && pass "$s: $(printf %.2f "$kept")% reads kept (>=95% expected for this dataset)" \
                                            || fail "$s: only $(printf %.2f "$kept")% reads kept — trimming too aggressive?"
  else fail "fastp report $j missing"; fi
done
for m in multiqc_raw multiqc_trimmed; do [ -s $OUT/$m/multiqc_report.html ] && pass "$m report" || fail "$m report missing"; done
echo "Result: $ok passed, $bad failed"; [ $bad -eq 0 ]
