#!/usr/bin/env python3
"""Extract every protein-coding gene (CDS) of a genome from FASTA + GFF3, translate it, and write a table.

Usage:
  python3 cds_table.py genome.fna annotation.gff [-o cds_table.tsv] [--table 11]

Output columns: gene, locus_tag, protein_id, start, end, strand, length_nt, length_aa, gc, gc3, ok
  gc3 = GC at third codon positions; ok = length is a multiple of 3, ends with a stop, no internal stop.
"""
import argparse
import csv
import sys
from Bio import SeqIO
from Bio.Seq import Seq


def parse_attributes(col9):
    """'ID=x;Name=y' -> {'ID': 'x', 'Name': 'y'}"""
    return dict(item.split("=", 1) for item in col9.strip().split(";") if "=" in item)


def read_cds(gff_path):
    """Yield one dict per CDS feature. Multi-segment CDS (same ID) are merged."""
    cds = {}
    with open(gff_path) as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            f = line.rstrip("\n").split("\t")
            if f[2] != "CDS":
                continue
            a = parse_attributes(f[8])
            if "pseudo" in a and a["pseudo"] == "true":
                continue
            key = a.get("ID")
            seg = (int(f[3]), int(f[4]))           # GFF: 1-based, inclusive
            if key in cds:
                cds[key]["segments"].append(seg)
            else:
                cds[key] = {"seqid": f[0], "strand": f[6], "segments": [seg],
                            "gene": a.get("gene", ""), "locus_tag": a.get("locus_tag", ""),
                            "protein_id": a.get("protein_id", "")}
    return cds.values()


def gc(s):
    return (s.count("G") + s.count("C")) / len(s) if s else 0.0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fasta"); ap.add_argument("gff")
    ap.add_argument("-o", "--out", default="-")
    ap.add_argument("--table", type=int, default=11, help="NCBI genetic code (11 = bacteria)")
    args = ap.parse_args()

    genome = {r.id: r.seq for r in SeqIO.parse(args.fasta, "fasta")}
    out = sys.stdout if args.out == "-" else open(args.out, "w", newline="")
    w = csv.writer(out, delimiter="\t", lineterminator="\n")
    w.writerow(["gene", "locus_tag", "protein_id", "start", "end", "strand",
                "length_nt", "length_aa", "gc", "gc3", "ok"])
    for c in read_cds(args.gff):
        segs = sorted(c["segments"])
        # GFF 1-based inclusive -> Python 0-based half-open: [start-1, end)
        nt = Seq("".join(str(genome[c["seqid"]][s - 1:e]) for s, e in segs))
        if c["strand"] == "-":
            nt = nt.reverse_complement()
        nt = str(nt).upper()
        prot = str(Seq(nt).translate(table=args.table))
        ok = (prot.endswith("*") and "*" not in prot[:-1] and len(nt) % 3 == 0)
        third = nt[2::3]
        w.writerow([c["gene"], c["locus_tag"], c["protein_id"], segs[0][0], segs[-1][1], c["strand"],
                    len(nt), len(prot.rstrip("*")), round(gc(nt), 4), round(gc(third), 4), ok])
    if out is not sys.stdout:
        out.close()


if __name__ == "__main__":
    main()
