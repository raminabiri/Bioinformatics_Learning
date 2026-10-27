#!/usr/bin/env python3
"""Summarise one AMR gene across all isolates of an NCBI Pathogen Detection *.amr.metadata.tsv file.

Usage:
    python3 amr_summary.py PDGxxx.amr.metadata.tsv GENE [CLUSTER_LIST.tsv]
Example:
    python3 amr_summary.py PDG000000004.6392.amr.metadata.tsv blaCTX-M-15 PDG000000004.6392.reference_target.cluster_list.tsv

Reads the file line by line (it is ~0.5 GB for E. coli; never loaded whole), so memory stays small.
GENE must match one element of AMR_genotypes exactly (blaCTX-M-15 does not match blaCTX-M-150).
"""
import csv
import sys
from collections import Counter

csv.field_size_limit(10**7)
meta, gene = sys.argv[1], sys.argv[2]

total = 0
species = Counter()
carriers = []                     # (target_acc, country, year, genotypes) of isolates with GENE
with open(meta, newline="") as fh:
    rows = csv.DictReader(fh, delimiter="\t")
    for r in rows:
        total += 1
        species[r["species_taxid"]] += 1          # scientific_name holds strain names; the taxid does not
        genotypes = r["AMR_genotypes"].strip('"').split(",")
        if gene in genotypes:
            country = r["geo_loc_name"].split(":")[0] if r["geo_loc_name"] != "NULL" else "NULL"
            year = r["collection_date"][:4]
            if not (year.isdigit() and 1901 <= int(year) <= 2026):    # "missing", "NULL", placeholder 1900
                year = "NULL"
            carriers.append((r["target_acc"], country, year, set(genotypes)))

print(f"isolates: {total}")
print("top species_taxid:", ", ".join(f"{s} {n}" for s, n in species.most_common(4)))
print(f"with {gene}: {len(carriers)} ({100 * len(carriers) / total:.1f}%)\n")

print("top countries:")
for c, n in Counter(c for _, c, _, _ in carriers).most_common(8):
    print(f"  {c}\t{n}")
iran = sum(1 for _, c, _, _ in carriers if c == "Iran")
print(f"  Iran\t{iran}\n")

decades = Counter(y[:3] + "0s" for _, _, y, _ in carriers if y != "NULL")
no_year = sum(1 for _, _, y, _ in carriers if y == "NULL")
print("by decade:", ", ".join(f"{d} {n}" for d, n in sorted(decades.items())), f"| no usable year: {no_year}")

print(f"\nmost frequent companions of {gene}:")
companions = Counter(g for _, _, _, gs in carriers for g in gs if g != gene)
for g, n in companions.most_common(10):
    print(f"  {g}\t{100 * n / len(carriers):.1f}%")

if len(sys.argv) > 3:                               # which SNP clusters hold the carriers?
    in_cluster = {}
    with open(sys.argv[3]) as fh:
        next(fh)
        for line in fh:
            pds, target = line.split("\t")[:2]
            in_cluster[target] = pds
    clusters = Counter(in_cluster.get(t, "none") for t, _, _, _ in carriers)
    print(f"\ncarriers in a SNP cluster: {len(carriers) - clusters['none']} of {len(carriers)}")
    print("largest clusters:", ", ".join(f"{c} {n}" for c, n in clusters.most_common(4) if c != "none"))
