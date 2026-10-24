#!/usr/bin/env python3
"""Build three simulated E. coli isolates with a KNOWN resistance content (part 08, module 01).

Each isolate = the K-12 MG1655 chromosome (part 01 data), optionally with
  - one point mutation in gyrA or parC (quinolone resistance), and
  - one extra "plasmid" contig carrying acquired genes from acquired_genes.fna.

  isoA: gyrA S83L  + plasmid pA: blaCTX-M-15
  isoB: parC S80I  + plasmid pB: blaNDM-1 and a truncated tet(A) (first 600 of 1200 bp)
  isoC: unchanged K-12 (negative control)

Usage: python3 make_mock_isolates.py K12.fna K12.gff acquired_genes.fna OUTDIR
Writes OUTDIR/isoA.fna, isoB.fna, isoC.fna and OUTDIR/ground_truth_amr.tsv
"""
import os
import random
import sys

k12_fna, k12_gff, genes_fna, outdir = sys.argv[1:5]
os.makedirs(outdir, exist_ok=True)
random.seed(42)

CODON = {}
bases = 'TCAG'
aas = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
for i, a in enumerate(aas):
    CODON[bases[i // 16] + bases[i // 4 % 4] + bases[i % 4]] = a
COMP = str.maketrans('ACGT', 'TGCA')


def read_fasta(path):
    seqs, name = {}, None
    for line in open(path):
        line = line.strip()
        if line.startswith('>'):
            name = line[1:].split()[0]
            seqs[name] = []
        elif name:
            seqs[name].append(line.upper())
    return {n: ''.join(s) for n, s in seqs.items()}


def gene_coords(gff, name):
    for line in open(gff):
        f = line.rstrip('\n').split('\t')
        if len(f) == 9 and f[2] == 'gene' and f'Name={name};' in f[8]:
            return int(f[3]), int(f[4]), f[6]
    sys.exit(f'gene {name} not found in {gff}')


def mutate(chrom, gff, gene, pos, ref_aa, new_codon):
    """Change codon `pos` of `gene` to `new_codon`; check the old amino acid first."""
    start, end, strand = gene_coords(gff, gene)
    cds = chrom[start - 1:end]
    if strand == '-':
        cds = cds.translate(COMP)[::-1]
    old = cds[3 * (pos - 1):3 * pos]
    if CODON[old] != ref_aa:
        sys.exit(f'{gene} codon {pos} is {old} ({CODON[old]}), expected {ref_aa}')
    cds = cds[:3 * (pos - 1)] + new_codon + cds[3 * pos:]
    if strand == '-':
        cds = cds.translate(COMP)[::-1]
    print(f'{gene} {ref_aa}{pos}{CODON[new_codon]}: {old} -> {new_codon}')
    return chrom[:start - 1] + cds + chrom[end:]


def spacer(n):
    return ''.join(random.choice('ACGT') for _ in range(n))


def write(path, records):
    with open(path, 'w') as out:
        for name, seq in records:
            out.write(f'>{name}\n')
            for i in range(0, len(seq), 80):
                out.write(seq[i:i + 80] + '\n')


chrom = read_fasta(k12_fna)['NC_000913.3']
genes = read_fasta(genes_fna)

isoA_chrom = mutate(chrom, k12_gff, 'gyrA', 83, 'S', 'TTG')
pA = spacer(2000) + genes['blaCTX-M-15'] + spacer(2000)
write(f'{outdir}/isoA.fna', [('isoA_chromosome', isoA_chrom), ('isoA_pA', pA)])

isoB_chrom = mutate(chrom, k12_gff, 'parC', 80, 'S', 'ATC')
pB = spacer(2000) + genes['blaNDM-1'] + spacer(1500) + genes['tet(A)'][:600] + spacer(2000)
write(f'{outdir}/isoB.fna', [('isoB_chromosome', isoB_chrom), ('isoB_pB', pB)])

write(f'{outdir}/isoC.fna', [('isoC_chromosome', chrom)])

with open(f'{outdir}/ground_truth_amr.tsv', 'w') as out:
    out.write('isolate\tcontig\tfeature\tkind\n')
    out.write('isoA\tisoA_chromosome\tgyrA_S83L\tpoint mutation\n')
    out.write('isoA\tisoA_pA\tblaCTX-M-15\tacquired gene (complete)\n')
    out.write('isoB\tisoB_chromosome\tparC_S80I\tpoint mutation\n')
    out.write('isoB\tisoB_pB\tblaNDM-1\tacquired gene (complete)\n')
    out.write('isoB\tisoB_pB\ttet(A)\tacquired gene (first 600 of 1200 bp)\n')
    out.write('isoC\t-\t-\tnone (K-12 only)\n')
print('Done:', outdir)
