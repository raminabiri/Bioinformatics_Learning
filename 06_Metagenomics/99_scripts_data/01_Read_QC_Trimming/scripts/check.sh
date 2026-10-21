#!/usr/bin/env bash
# check.sh (part 06, module 01): self-check of the QC outputs
# Run inside the project folder after run_qc.sh (or after your own commands):
#   cd ~/meta && bash ~/Bioinformatics_Learning-main/06_Metagenomics/99_scripts_data/01_Read_QC_Trimming/scripts/check.sh
set -uo pipefail
ok=0
bad=0
pass() { echo "  [OK]   $1"; ok=$((ok + 1)); }
fail() { echo "  [FAIL] $1"; bad=$((bad + 1)); }

for s in minigut minigut_sample2; do
  for r in R1 R2; do
    [ -s qc/fastqc_raw/${s}_${r}_fastqc.zip ]     && pass "FastQC raw $s $r"     || fail "FastQC raw $s $r missing"
    [ -s qc/trimmed/${s}_${r}.fastq.gz ]          && pass "trimmed $s $r"        || fail "trimmed $s $r missing"
    [ -s qc/fastqc_trimmed/${s}_${r}_fastqc.zip ] && pass "FastQC trimmed $s $r" || fail "FastQC trimmed $s $r missing"
  done
  if [ -s qc/trimmed/${s}_R1.fastq.gz ] && [ -s qc/trimmed/${s}_R2.fastq.gz ]; then
    raw=$(zcat raw/${s}_R1.fastq.gz | awk 'END {print NR/4}')
    n1=$(zcat qc/trimmed/${s}_R1.fastq.gz | awk 'END {print NR/4}')
    n2=$(zcat qc/trimmed/${s}_R2.fastq.gz | awk 'END {print NR/4}')
    [ "$n1" = "$n2" ] && pass "$s: R1 and R2 still paired ($n1 pairs)" || fail "$s: R1 ($n1) != R2 ($n2), pairs broken"
    pct=$(awk -v a="$n1" -v b="$raw" 'BEGIN {printf "%.2f", a / b * 100}')
    awk -v p="$pct" 'BEGIN {exit !(p >= 95)}' && pass "$s: $pct% pairs kept (>= 95% expected for this dataset)" \
                                              || fail "$s: only $pct% pairs kept; trimming too aggressive?"
  fi
done
for m in multiqc_raw multiqc_trimmed; do
  [ -s qc/$m/multiqc_report.html ] && pass "$m report" || fail "$m report missing"
done
echo "Result: $ok passed, $bad failed"
[ $bad -eq 0 ]
