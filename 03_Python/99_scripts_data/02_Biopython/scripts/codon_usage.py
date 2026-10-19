#!/usr/bin/env python3
"""Codon usage (per thousand codons) of all CDS, or of a subset of genes selected by a gene-name regex.

Usage:
  python3 codon_usage.py genome.fna annotation.gff [--genes '^rp[lsm]'] [--top 5]
Reuses read_cds() from cds_table.py (same folder).
"""
import argparse
import re
from collections import Counter
from Bio import SeqIO
from Bio.Seq import Seq
from cds_table import read_cds


def cds_sequences(fasta, gff, pattern=None):
    genome = {r.id: r.seq for r in SeqIO.parse(fasta, "fasta")}
    for c in read_cds(gff):
        if pattern and not re.search(pattern, c["gene"]):
            continue
        nt = Seq("".join(str(genome[c["seqid"]][s - 1:e]) for s, e in sorted(c["segments"])))
        if c["strand"] == "-":
            nt = nt.reverse_complement()
        yield c["gene"], str(nt).upper()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fasta"); ap.add_argument("gff")
    ap.add_argument("--genes", help="regex on gene name, e.g. '^rp[lsm]' = ribosomal proteins")
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()

    codons, n_genes, gc3 = Counter(), 0, []
    for _, nt in cds_sequences(args.fasta, args.gff, args.genes):
        n_genes += 1
        cods = [nt[i:i + 3] for i in range(3, len(nt) - 3, 3)]   # skip start and stop codon
        codons.update(cods)
        third = nt[2::3]
        gc3.append((third.count("G") + third.count("C")) / len(third))
    total = sum(codons.values())
    print(f"genes: {n_genes}  codons (no start/stop): {total}  mean gc3: {sum(gc3) / len(gc3):.3f}")
    per_k = {c: 1000 * n / total for c, n in codons.items()}
    print("rarest:", ", ".join(f"{c} {per_k.get(c, 0):.2f}" for c in sorted(per_k, key=per_k.get)[:args.top]))
    print("commonest:", ", ".join(f"{c} {per_k[c]:.1f}" for c in sorted(per_k, key=per_k.get, reverse=True)[:args.top]))
    # Leucine / Arginine synonymous choices
    for aa, syn in {"Leu": ["CTG", "CTT", "CTC", "CTA", "TTA", "TTG"],
                    "Arg": ["CGT", "CGC", "CGA", "CGG", "AGA", "AGG"]}.items():
        n = sum(codons[c] for c in syn)
        print(aa, "  ".join(f"{c} {100 * codons[c] / n:.1f}%" for c in syn))


if __name__ == "__main__":
    main()
