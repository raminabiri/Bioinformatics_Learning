#!/usr/bin/env bash
# Build small real example files for each format from course data (run from the module folder).
# Needs: part 01/01 data (ecoli_k12.*), part 03 modules 01–02 outputs, samtools, bcftools, curl.
# Downloads only one small GenBank record (~12 KB).
set -euo pipefail
D=data; B=../01_Bash_Linux/data; M=../../03_Metagenomics
mkdir -p $D
# FASTA: first 10 kb of E. coli K-12, 60 bp per line
awk 'NR==1{print ">NC_000913.3:1-10000"; next} {s=s $0} END{print substr(s,1,10000)}' $B/ecoli_k12.fna | fold -w 60 > $D/ecoli_10kb.fa
# FASTQ: first 3 read pairs of minigut (R1)
zcat $M/data/raw/minigut_R1.fastq.gz | head -n 12 > $D/minigut_3reads.fastq || true
# GFF3: header + features overlapping rpoB
{ grep '^##' $B/ecoli_k12.gff | head -n 3; awk -F'\t' '$1=="NC_000913.3" && $4<=4185273 && $5>=4181245' $B/ecoli_k12.gff; } > $D/rpoB.gff3
# GenBank: rpoB region from NCBI
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000913.3&rettype=gbwithparts&retmode=text&seq_start=4181245&seq_stop=4185273" > $D/rpoB.gb
# SAM: a few chr21 read pairs from the module 03/02 host BAM
samtools view -h $M/work/02_host/bam/minigut_spiked.host.bam chr21part:100000-100400 | head -n 8 > $D/example.sam
# BAM -> VCF: call the SNPs that wgsim introduced into the simulated human reads
bcftools mpileup -Ou -f $M/data/host/host_chr21_region.fa $M/work/02_host/bam/minigut_spiked.host.bam 2>/dev/null \
  | bcftools call -mv -Oz -o $D/chr21_spiked.vcf.gz 2>/dev/null
bcftools index -t $D/chr21_spiked.vcf.gz
# Truth: the mutations wgsim introduced (same parameters and seed as 03/02 make_spiked_sample.sh)
wgsim -N 5000 -1 126 -2 126 -d 350 -s 50 -e 0.002 -r 0.001 -R 0.1 -S 42 \
      $M/data/host/host_chr21_region.fa /dev/null /dev/null 2>/dev/null > $D/chr21_true_mutations.txt
# BED: rpoB gene as BED (0-based, half-open)
awk -F'\t' 'BEGIN{OFS="\t"} $3=="gene" && $9 ~ /Name=rpoB;/ {print $1, $4-1, $5, "rpoB", 0, $7}' $B/ecoli_k12.gff > $D/rpoB.bed
ls -la $D
