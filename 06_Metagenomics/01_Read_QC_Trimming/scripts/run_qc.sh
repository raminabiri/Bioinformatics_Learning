#!/usr/bin/env bash
# Module 03/01 — Read QC & trimming for all samples of the part-03 dataset.
# Run from the part folder:   cd 06_Metagenomics && bash 01_Read_QC_Trimming/scripts/run_qc.sh
# Inputs : data/raw/<sample>_R1.fastq.gz, data/raw/<sample>_R2.fastq.gz   (bash data/download.sh)
# Outputs: work/01_qc/{fastqc_raw,multiqc_raw,trimmed,fastp_reports,fastqc_trimmed,multiqc_trimmed}
set -euo pipefail
THREADS=${THREADS:-4}
RAW=data/raw
OUT=work/01_qc
[ -d "$RAW" ] || { echo "Run from 06_Metagenomics/ (and run data/download.sh first)"; exit 1; }
mkdir -p $OUT/{fastqc_raw,multiqc_raw,trimmed,fastp_reports,fastqc_trimmed,multiqc_trimmed}

echo "== tool versions"; fastqc --version; fastp --version 2>&1; multiqc --version

echo "== 1. FastQC on raw reads"
fastqc -q -t "$THREADS" $RAW/*_R[12].fastq.gz -o $OUT/fastqc_raw
multiqc -q -f $OUT/fastqc_raw -o $OUT/multiqc_raw

echo "== 2. fastp: adapter + quality trimming (cut_front/cut_tail, Q20), min length 50"
for r1 in $RAW/*_R1.fastq.gz; do
  s=$(basename "$r1" _R1.fastq.gz)
  fastp \
    -i "$r1" -I "$RAW/${s}_R2.fastq.gz" \
    -o "$OUT/trimmed/${s}_R1.fastq.gz" -O "$OUT/trimmed/${s}_R2.fastq.gz" \
    --detect_adapter_for_pe \
    --cut_front --cut_tail --cut_mean_quality 20 \
    --length_required 50 \
    --thread "$THREADS" \
    --json "$OUT/fastp_reports/${s}.json" --html "$OUT/fastp_reports/${s}.html" \
    2> "$OUT/fastp_reports/${s}.log"
  echo "   $s done"
done

echo "== 3. FastQC on trimmed reads + combined MultiQC (FastQC + fastp)"
fastqc -q -t "$THREADS" $OUT/trimmed/*_R[12].fastq.gz -o $OUT/fastqc_trimmed
multiqc -q -f $OUT/fastqc_trimmed $OUT/fastp_reports/*.json -o $OUT/multiqc_trimmed

echo "== Done. Open $OUT/multiqc_raw/multiqc_report.html and $OUT/multiqc_trimmed/multiqc_report.html"
