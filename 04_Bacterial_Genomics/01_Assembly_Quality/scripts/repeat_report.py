#!/usr/bin/env python3
"""Why short-read assemblies break: repeats in a finished genome, seen two ways.

1. k-mer view: for each k, the share of genome positions whose k-mer (either strand) occurs more than once.
   A de Bruijn assembler cannot resolve a repeat longer than k (or longer than the read/insert size).
2. Annotation view: cut the genome at every rRNA operon and insertion sequence (IS) from the GFF,
   and report the contigs an ideal short-read assembler would produce (count, N50, L50, largest).

Usage:
  python3 repeat_report.py genome.fna annotation.gff [--k 21 55 77 127]
"""
import argparse
from Bio import SeqIO


def repeated_fraction(seq, k):
    """Share of positions whose canonical k-mer is seen more than once in the genome."""
    rc = str(seq.reverse_complement())
    s, n = str(seq), len(seq)
    keys = [min(hash(s[i:i + k]), hash(rc[n - i - k:n - i])) for i in range(n - k + 1)]
    seen, dup = set(), set()
    for h in keys:
        (dup if h in seen else seen).add(h)
    return sum(h in dup for h in keys) / len(keys)


def repeat_intervals(gff):
    """rRNA genes and mobile elements from GFF3, merged when closer than 1 kb (one rrn operon = one block)."""
    iv = []
    with open(gff) as fh:
        for line in fh:
            f = line.split("\t")
            if len(f) > 4 and f[2] in ("rRNA", "mobile_genetic_element"):
                iv.append([int(f[3]), int(f[4])])
    iv.sort()
    merged = [iv[0]]
    for s, e in iv[1:]:
        if s - merged[-1][1] < 1000:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return merged


def n50_l50(lengths):
    total, run = sum(lengths), 0
    for i, x in enumerate(sorted(lengths, reverse=True), 1):
        run += x
        if run >= total / 2:
            return x, i


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fasta"); ap.add_argument("gff")
    ap.add_argument("--k", type=int, nargs="+", default=[21, 55, 77, 127])
    args = ap.parse_args()
    seq = next(SeqIO.parse(args.fasta, "fasta")).seq.upper()

    print("== k-mer view")
    print("k\tpositions_in_repeated_kmers_%")
    for k in args.k:
        print(f"{k}\t{100 * repeated_fraction(seq, k):.2f}")

    print("== annotation view (cut at rRNA operons + IS elements; genome treated as linear)")
    blocks = repeat_intervals(args.gff)
    contigs, prev = [], 1
    for s, e in blocks:
        if s > prev:
            contigs.append(s - prev)
        prev = e + 1
    contigs.append(len(seq) - prev + 1)
    n50, l50 = n50_l50(contigs)
    print(f"repeat blocks: {len(blocks)}  ({sum(e - s + 1 for s, e in blocks)} bp)")
    print(f"contigs: {len(contigs)}  total: {sum(contigs)}  largest: {max(contigs)}  N50: {n50}  L50: {l50}")


if __name__ == "__main__":
    main()
