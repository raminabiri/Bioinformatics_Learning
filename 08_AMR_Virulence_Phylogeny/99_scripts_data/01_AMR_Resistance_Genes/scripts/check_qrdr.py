#!/usr/bin/env python3
"""Check the quinolone-resistance positions gyrA 83/87 and parC 80/84 in E. coli genomes.

Works the same on Windows, macOS and Linux (only Python + Biopython).

Usage:
    python check_qrdr.py ecoli_k12.gff GENOME.fna [GENOME.fna ...]

The gene coordinates come from the K-12 GFF (the simulated isolates keep the K-12
chromosome, part 08/01), so the chromosome must be the first record of each FASTA.
For each genome the script prints the codon and amino acid at each position and
whether it differs from the wild type (S83 and D87 in GyrA, S80 and E84 in ParC).
"""
import sys

from Bio import SeqIO
from Bio.Seq import Seq

POSITIONS = {"gyrA": {83: "S", 87: "D"}, "parC": {80: "S", 84: "E"}}

gff_file, genomes = sys.argv[1], sys.argv[2:]

# 1. start, end and strand of each gene's CDS in the K-12 GFF (column 3 = CDS)
cds = {}
for line in open(gff_file):
    if line.startswith("#"):
        continue
    col = line.rstrip("\n").split("\t")
    if len(col) < 9 or col[2] != "CDS":
        continue
    for gene in POSITIONS:
        if f"gene={gene};" in col[8]:
            cds[gene] = (int(col[3]), int(col[4]), col[6])

print("genome\tgene\tposition\tcodon\taa\twild_type\tstatus")
for path in genomes:
    chrom = next(SeqIO.parse(path, "fasta")).seq        # first record = chromosome
    name = path.replace("\\", "/").split("/")[-1].replace(".fna", "")
    for gene, (start, end, strand) in cds.items():
        dna = chrom[start - 1:end]                       # GFF is 1-based, Python is 0-based
        if strand == "-":
            dna = dna.reverse_complement()
        for pos, wild in POSITIONS[gene].items():
            codon = str(dna[(pos - 1) * 3:pos * 3])
            aa = str(Seq(codon).translate())
            status = "wild type" if aa == wild else f"MUTANT {wild}{pos}{aa}"
            print(f"{name}\t{gene}\t{pos}\t{codon}\t{aa}\t{wild}\t{status}")
