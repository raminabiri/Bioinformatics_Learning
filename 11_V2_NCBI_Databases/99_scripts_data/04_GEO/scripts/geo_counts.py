#!/usr/bin/env python3
"""Quick look at a GEO RNA-seq series: sample table from the series matrix + NCBI raw counts.

Usage:
    python3 geo_counts.py SERIES_MATRIX.txt.gz COUNTS.tsv.gz TREATED CONTROL [GENEID ...]

TREATED / CONTROL are values of the "treatment:" characteristic (e.g. Dexamethasone Untreated).
Prints the sample table, library sizes, then a paired log2 fold change (treated vs control,
same cell line) for the given Gene IDs, and the 10 genes with the largest mean change.
This is a first look only: no statistics (that is DESeq2, part 13).
"""
import gzip
import sys

import numpy as np
import pandas as pd

matrix, counts_file, treated, control = sys.argv[1:5]
genes = [int(g) for g in sys.argv[5:]]

# 1. sample table from the "!Sample_..." lines of the series matrix
rows = {}
with gzip.open(matrix, "rt") as fh:
    for line in fh:
        if not line.startswith("!Sample_"):
            continue
        key, *values = line.rstrip("\n").split("\t")
        values = [v.strip('"') for v in values]
        if key == "!Sample_geo_accession":
            rows["gsm"] = values
        elif key == "!Sample_characteristics_ch1":
            name = values[0].split(":")[0]             # e.g. "treatment"
            rows[name] = [v.split(": ", 1)[1] for v in values]
samples = pd.DataFrame(rows).set_index("gsm")[["cell line", "treatment"]]
print(samples.to_string(), "\n")

# 2. counts: rows = NCBI Gene ID, columns = GSM
counts = pd.read_csv(counts_file, sep="\t", index_col=0)
lib = counts.sum()
print("library size (million reads):")
print((lib / 1e6).round(1).to_string(), "\n")

# 3. CPM and paired log2 fold change (pseudocount 1 avoids log of zero)
cpm = counts / lib * 1e6
t = samples[samples.treatment == treated].reset_index().set_index("cell line")["gsm"]
c = samples[samples.treatment == control].reset_index().set_index("cell line")["gsm"]
lfc = pd.DataFrame({line: np.log2(cpm[t[line]] + 1) - np.log2(cpm[c[line]] + 1) for line in t.index})
summary = pd.DataFrame({"mean_cpm_" + control: cpm[c.values].mean(axis=1).round(1),
                        "mean_cpm_" + treated: cpm[t.values].mean(axis=1).round(1),
                        "mean_log2FC": lfc.mean(axis=1).round(2),
                        "lines_up": (lfc > 0).sum(axis=1)})

if genes:
    print(f"selected genes ({treated} vs {control}):")
    print(summary.loc[genes].to_string(), "\n")

expressed = summary[summary["mean_cpm_" + control] >= 5]          # ignore near-zero genes
print(f"top 10 up among {len(expressed)} genes with control CPM >= 5:")
print(expressed.sort_values("mean_log2FC", ascending=False).head(10).to_string())
