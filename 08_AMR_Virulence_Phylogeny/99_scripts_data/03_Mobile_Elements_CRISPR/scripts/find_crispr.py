#!/usr/bin/env python3
"""Find CRISPR arrays of a known repeat in a genome (part 08, module 03).

Scans both strands for copies of REPEAT with at most MAXMIS mismatches, groups copies that
are closer than 100 bp into arrays, and writes the spacers between neighbouring repeats.
This is a teaching tool for ONE known repeat; CRISPRCasFinder or MinCED find unknown ones.

Usage: python3 find_crispr.py GENOME.fna REPEAT [MAXMIS] > spacers.fna
       (array summary goes to stderr)
"""
import sys

genome_fna, repeat = sys.argv[1], sys.argv[2].upper()
maxmis = int(sys.argv[3]) if len(sys.argv) > 3 else 3
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


def hits(seq, rep):
    k = len(rep)
    for i in range(len(seq) - k + 1):
        mis = 0
        for a, b in zip(seq[i:i + k], rep):
            if a != b:
                mis += 1
                if mis > maxmis:
                    break
        if mis <= maxmis:
            yield i, mis


k = len(repeat)
for contig, seq in read_fasta(genome_fna).items():
    found = [(i, m, '+') for i, m in hits(seq, repeat)]
    found += [(i, m, '-') for i, m in hits(seq, repeat.translate(COMP)[::-1])]
    found.sort()
    arrays, cur = [], []
    for h in found:
        if cur and h[0] - (cur[-1][0] + k) > 100:
            arrays.append(cur)
            cur = []
        cur.append(h)
    if cur:
        arrays.append(cur)
    for n, arr in enumerate(arrays, 1):
        if len(arr) < 2:
            continue
        start, end = arr[0][0] + 1, arr[-1][0] + k
        exact = sum(1 for h in arr if h[1] == 0)
        print(f'{contig}\tarray{n}\t{start}-{end}\tstrand {arr[0][2]}\t'
              f'repeats {len(arr)} (exact {exact})\tspacers {len(arr) - 1}', file=sys.stderr)
        for j in range(len(arr) - 1):
            s = seq[arr[j][0] + k:arr[j + 1][0]]
            print(f'>{contig}_array{n}_spacer{j + 1} len={len(s)}\n{s}')
