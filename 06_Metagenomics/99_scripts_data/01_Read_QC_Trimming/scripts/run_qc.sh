#!/usr/bin/env bash
# run_qc.sh (part 06, module 01): read QC and trimming for every sample in raw/
# Run inside the project folder of part 06 (it must contain raw/<sample>_R1.fastq.gz and _R2):
#   cd ~/meta && bash ~/Bioinformatics_Learning-main/06_Metagenomics/99_scripts_data/01_Read_QC_Trimming/scripts/run_qc.sh
# Outputs: qc/{fastqc_raw,multiqc_raw,trimmed,fastp,fastqc_trimmed,multiqc_trimmed}
#          qc/trimmed/<sample>_R1.fastq.gz and _R2 are the input of module 02
set -euo pipefail
THREADS=${THREADS:-4}

if [ ! -d raw ]; then
  echo "No raw/ folder here. Run this script inside your project folder (cd ~/meta)."
  exit 1
fi
mkdir -p qc/fastqc_raw qc/multiqc_raw qc/trimmed qc/fastp qc/fastqc_trimmed qc/multiqc_trimmed

echo "== tool versions"
fastqc --version
fastp --version
multiqc --version

echo "== 1. FastQC + MultiQC on raw reads"
fastqc -q -t "$THREADS" -o qc/fastqc_raw raw/*.fastq.gz
multiqc -q -f qc/fastqc_raw -o qc/multiqc_raw

echo "== 2. fastp: adapters + trim both ends (Q20), keep reads >= 50 bp"
for r1 in raw/*_R1.fastq.gz; do
  s=$(basename "$r1" _R1.fastq.gz)
  fastp -i "$r1" -I "raw/${s}_R2.fastq.gz" \
        -o "qc/trimmed/${s}_R1.fastq.gz" -O "qc/trimmed/${s}_R2.fastq.gz" \
        --detect_adapter_for_pe --cut_front --cut_tail --cut_mean_quality 20 \
        --length_required 50 --thread "$THREADS" \
        -j "qc/fastp/${s}.json" -h "qc/fastp/${s}.html" 2> "qc/fastp/${s}.log"
  echo "   $s: $(grep 'reads passed filter' "qc/fastp/${s}.log")"
done

echo "== 3. FastQC on trimmed reads + MultiQC of FastQC and fastp"
fastqc -q -t "$THREADS" -o qc/fastqc_trimmed qc/trimmed/*.fastq.gz
multiqc -q -f qc/fastqc_trimmed qc/fastp -o qc/multiqc_trimmed

echo "== Done. Open qc/multiqc_raw/multiqc_report.html and qc/multiqc_trimmed/multiqc_report.html"
