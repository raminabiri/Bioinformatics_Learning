#!/usr/bin/env bash
# Build a controlled test sample for host removal:
#   minigut (trimmed, 49,845 pairs, 0% human)
# + 5,000 simulated human pairs from chr21 region  (present in the host index)
# + 5,000 simulated human pairs from chr1 region   (ABSENT from the host index)
# Read names start with the source, so every read's true origin is known.
# Run from 06_Metagenomics/ after module 01.  Requires: wgsim (samtools package), seqkit.
set -euo pipefail
OUT=work/02_host/spiked; mkdir -p $OUT
TR=work/01_qc/trimmed
[ -s $TR/minigut_R1.fastq.gz ] || { echo "Run module 01 first"; exit 1; }

# wgsim: -N pairs, -1/-2 read lengths, -d insert size, -e base error rate,
#        -r mutation rate, -R indel fraction, -S seed (fixed => identical result for everyone)
for region in chr21 chr1; do
  ref=data/host/$( [ $region = chr21 ] && echo host_chr21_region.fa || echo human_chr1_region.fa )
  wgsim -N 5000 -1 126 -2 126 -d 350 -s 50 -e 0.002 -r 0.001 -R 0.1 -S 42 \
        "$ref" $OUT/human_${region}_R1.fq $OUT/human_${region}_R2.fq > /dev/null
  # prefix read names with the true source
  for r in R1 R2; do sed -i "1~4s/^@/@HUMAN_${region}_/" $OUT/human_${region}_${r}.fq; done
done

for r in R1 R2; do
  { zcat $TR/minigut_${r}.fastq.gz; cat $OUT/human_chr21_${r}.fq $OUT/human_chr1_${r}.fq; } | gzip > $OUT/minigut_spiked_${r}.fastq.gz
done
rm $OUT/human_*.fq
seqkit stats -T $OUT/minigut_spiked_R1.fastq.gz $OUT/minigut_spiked_R2.fastq.gz | cut -f1,4
