#!/usr/bin/env bash
# Module 03/02 — remove host (human) reads with Bowtie2 + samtools.
# Run from 06_Metagenomics/ after module 01.
# Usage: bash 02_Host_Removal_Alignment/scripts/run_host_removal.sh [sample ...]
#        (default: all samples in $IN = work/01_qc/trimmed)
# Keeps a read pair ONLY if BOTH mates are unaligned to the host (samtools -f 12 -F 256).
# (Bowtie2's --un-conc would also keep discordant pairs whose mates DID align to host.)
# Outputs: work/02_host/clean/<sample>_R{1,2}.fastq.gz
#          work/02_host/bam/<sample>.host.bam (+ .bai)   sorted, for inspection
#          work/02_host/logs/<sample>.bowtie2.log, <sample>.flagstat
set -euo pipefail
THREADS=${THREADS:-4}
IN=${IN:-work/01_qc/trimmed}
REF=${REF:-data/host/host_chr21_region.fa}
IDX=${IDX:-work/02_host/index/host}
mkdir -p "$(dirname "$IDX")" work/02_host/{clean,bam,logs}

if [ ! -s "${IDX}.1.bt2" ]; then
  echo "== building Bowtie2 index from $REF"
  bowtie2-build --threads "$THREADS" -q "$REF" "$IDX"
fi

samples=("$@")
[ ${#samples[@]} -gt 0 ] || samples=($(ls $IN/*_R1.fastq.gz | xargs -n1 basename | sed 's/_R1.fastq.gz//'))

for s in "${samples[@]}"; do
  echo "== $s"
  tmp=work/02_host/bam/${s}.unsorted.bam
  # 1) align; Bowtie2 writes both mates of a pair next to each other (input order)
  bowtie2 -p "$THREADS" --very-sensitive -x "$IDX" \
      -1 "$IN/${s}_R1.fastq.gz" -2 "$IN/${s}_R2.fastq.gz" \
      2> "work/02_host/logs/${s}.bowtie2.log" \
    | samtools view -b -o "$tmp" -
  # 2) keep pairs where read AND mate are unmapped (-f 12), no secondary (-F 256)
  samtools view -b -f 12 -F 256 "$tmp" \
    | samtools fastq -1 "work/02_host/clean/${s}_R1.fastq.gz" -2 "work/02_host/clean/${s}_R2.fastq.gz" \
                     -0 /dev/null -s /dev/null -n - 2> /dev/null
  # 3) sorted, indexed BAM + flagstat for inspection
  samtools sort -@ 2 -o "work/02_host/bam/${s}.host.bam" "$tmp" 2> /dev/null && rm "$tmp"
  samtools index "work/02_host/bam/${s}.host.bam"
  samtools flagstat "work/02_host/bam/${s}.host.bam" > "work/02_host/logs/${s}.flagstat"
  printf "   %s   clean pairs: %s\n" "$(tail -n 1 work/02_host/logs/${s}.bowtie2.log)" \
         "$(zcat work/02_host/clean/${s}_R1.fastq.gz | awk 'END{print NR/4}')"
done
