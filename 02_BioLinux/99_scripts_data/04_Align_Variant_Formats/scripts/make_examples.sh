#!/usr/bin/env bash
# How the example BAM and VCF of module 02_BioLinux/04_Align_Variant_Formats were made.
# Students do NOT need to run this: the results are already in ../data/.
# It uses tools taught later in the course (wgsim, bowtie2, bcftools mpileup/call; part 06).
#
# Story: a rifampicin-resistant E. coli K-12 "patient isolate" with the rpoB H526Y mutation
# (CAC->TAC at genome position 4,182,820), two other SNPs and a 1-bp deletion.
# Reads are simulated only from a 30 kb region around rpoB and aligned to the full reference genome.
set -euo pipefail
cd "$(dirname "$0")/../data"
REF=../../../../01_Linux/99_scripts_data/data/ecoli_k12.fna   # downloaded in part 01
W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT

# 1. mutant region 4,170,001-4,200,000 (30 kb); positions below are genome coordinates
samtools faidx "$REF" NC_000913.3:4170001-4200000 | grep -v '^>' | tr -d '\n' > "$W/region.txt"
python3 - "$W/region.txt" "$W/mutant.fa" <<'PY'
import sys
seq = list(open(sys.argv[1]).read().strip())
off = 4170001                       # genome position of seq[0]
edits = {4182820: ('C', 'T'),       # rpoB H526Y  (CAC -> TAC)
         4175500: ('C', 'T'),       # SNP 2
         4193210: ('G', 'A')}       # SNP 3
for pos, (ref, alt) in edits.items():
    assert seq[pos - off].upper() == ref, (pos, seq[pos - off])
    seq[pos - off] = alt
del seq[4189000 - off]              # 1-bp deletion at genome position 4,189,000
open(sys.argv[2], 'w').write('>resistant_region\n' + ''.join(seq) + '\n')
PY

# 2. simulate 3,000 read pairs (2 x 150 bp, fragment ~300 bp, ~30x), no extra random mutations
wgsim -S 42 -N 3000 -1 150 -2 150 -d 300 -s 30 -e 0.002 -r 0 -R 0 "$W/mutant.fa" "$W/r1.fq" "$W/r2.fq" > /dev/null

# 3. align to the full reference genome, sort, index
bowtie2-build -q "$REF" "$W/ref"
bowtie2 -p 4 -x "$W/ref" -1 "$W/r1.fq" -2 "$W/r2.fq" --rg-id resistant --rg SM:resistant 2> bowtie2.log \
  | samtools sort -o resistant.bam -
samtools index resistant.bam

# 4. call variants (bacteria are haploid)
bcftools mpileup -f "$REF" resistant.bam 2>/dev/null \
  | bcftools call -mv --ploidy 1 -Oz -o resistant.vcf.gz 2>/dev/null
bcftools index -t resistant.vcf.gz
ls -lh resistant.bam resistant.bam.bai resistant.vcf.gz resistant.vcf.gz.tbi bowtie2.log
