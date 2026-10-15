#!/usr/bin/env python3
"""Find CDS with unusual GC content (z-score) in a cds_table.tsv made by cds_table.py.

Usage:
  python3 gc_outliers.py cds_table.tsv [--min-aa 100] [--z 2] [--top 10]
"""
import argparse
import csv
import statistics as st
from collections import Counter


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("table")
    ap.add_argument("--min-aa", type=int, default=100, help="ignore short CDS (GC is noisy)")
    ap.add_argument("--z", type=float, default=2.0)
    ap.add_argument("--top", type=int, default=10)
    args = ap.parse_args()

    with open(args.table) as fh:
        rows = [r for r in csv.DictReader(fh, delimiter="\t") if int(r["length_aa"]) >= args.min_aa]
    gcs = [float(r["gc"]) for r in rows]
    mu, sd = st.mean(gcs), st.stdev(gcs)
    for r in rows:
        r["z"] = (float(r["gc"]) - mu) / sd
    low = sorted((r for r in rows if r["z"] < -args.z), key=lambda r: r["z"])
    high = [r for r in rows if r["z"] > args.z]
    print(f"CDS >= {args.min_aa} aa: {len(rows)}  mean GC = {mu:.4f}  sd = {sd:.4f}")
    print(f"low-GC outliers (z < -{args.z}): {len(low)}   high-GC outliers (z > {args.z}): {len(high)}")
    print(f"\n{args.top} lowest-GC genes:")
    print("gene\tlocus_tag\tstart\tlength_aa\tgc\tz")
    for r in low[:args.top]:
        print(f"{r['gene']}\t{r['locus_tag']}\t{r['start']}\t{r['length_aa']}\t{r['gc']}\t{r['z']:.2f}")
    # gene-name prefix (first 3 letters) = rough "operon family"
    fam = Counter(r["gene"][:3] for r in low)
    print("\nmost common gene prefixes among low-GC outliers:", fam.most_common(6))


if __name__ == "__main__":
    main()
