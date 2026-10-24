#!/usr/bin/env python3
"""Build two simulated E. coli isolates with a KNOWN virulence content (part 08, module 02).

Each isolate = the K-12 MG1655 chromosome (part 01 data) + extra contigs that carry
virulence genes from virulence_genes.fna (and one resistance gene from module 01):

  isoD (STEC-like, as E. coli O157:H7):
       isoD_island : eae (intimin gamma)
       isoD_phage  : stx2a operon (stxA2 + stxB2) of phage 933W
       isoD_pO157  : ehxA (enterohemolysin)
  isoE (ExPEC-like, resistant):
       isoE_PAI    : papC, sat, cnf1
       isoE_pE     : iutA (aerobactin receptor) + blaCTX-M-15

Usage: python3 make_virulence_isolates.py K12.fna virulence_genes.fna acquired_genes.fna OUTDIR
Writes OUTDIR/isoD.fna, isoE.fna and OUTDIR/ground_truth_vir.tsv
"""
import os
import random
import sys

k12_fna, vir_fna, amr_fna, outdir = sys.argv[1:5]
os.makedirs(outdir, exist_ok=True)
random.seed(7)


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


def spacer(n):
    return ''.join(random.choice('ACGT') for _ in range(n))


def contig(*genes):
    """Random DNA - gene - random DNA - gene ... - random DNA."""
    parts = [spacer(2000)]
    for g in genes:
        parts += [g, spacer(1500)]
    parts[-1] = spacer(2000)
    return ''.join(parts)


def write(path, records):
    with open(path, 'w') as out:
        for name, seq in records:
            out.write(f'>{name}\n')
            for i in range(0, len(seq), 80):
                out.write(seq[i:i + 80] + '\n')


chrom = read_fasta(k12_fna)['NC_000913.3']
vir = read_fasta(vir_fna)
amr = read_fasta(amr_fna)

write(f'{outdir}/isoD.fna', [
    ('isoD_chromosome', chrom),
    ('isoD_island', contig(vir['eae_gamma'])),
    ('isoD_phage', contig(vir['stx2a_operon'])),
    ('isoD_pO157', contig(vir['ehxA'])),
])
write(f'{outdir}/isoE.fna', [
    ('isoE_chromosome', chrom),
    ('isoE_PAI', contig(vir['papC'], vir['sat'], vir['cnf1'])),
    ('isoE_pE', contig(vir['iutA'], amr['blaCTX-M-15'])),
])

with open(f'{outdir}/ground_truth_vir.tsv', 'w') as out:
    out.write('isolate\tcontig\tgene\tfunction\n')
    for row in [('isoD', 'isoD_island', 'eae', 'intimin (attaching and effacing)'),
                ('isoD', 'isoD_phage', 'stxA2+stxB2', 'Shiga toxin 2a'),
                ('isoD', 'isoD_pO157', 'ehxA', 'enterohemolysin'),
                ('isoE', 'isoE_PAI', 'papC', 'P fimbriae usher'),
                ('isoE', 'isoE_PAI', 'sat', 'secreted autotransporter toxin'),
                ('isoE', 'isoE_PAI', 'cnf1', 'cytotoxic necrotizing factor 1'),
                ('isoE', 'isoE_pE', 'iutA', 'aerobactin receptor'),
                ('isoE', 'isoE_pE', 'blaCTX-M-15', 'ESBL (resistance, module 01)')]:
        out.write('\t'.join(row) + '\n')
print('Done:', outdir)
