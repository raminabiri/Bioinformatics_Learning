#!/usr/bin/env python3
"""How much of each gene's Salmon count went to the transcript the reads really came from? (part 13, module 02)

All simulated reads come from the Ensembl canonical transcript (transcripts_canonical.fa), so a perfect
quantifier would give 100% to it. Prints the genes with the lowest share.

Usage (in ~/rnaseq):   python3 isoform_share.py salmon_isr/ctrl_1/quant.sf ref/tx2gene.tsv ref/transcripts_canonical.fa
Works the same on Windows (py instead of python3).
"""
import sys

import pandas as pd

quant_file, t2g_file, canonical_fa = sys.argv[1:4]
q = pd.read_csv(quant_file, sep="\t", index_col=0)
t2g = pd.read_csv(t2g_file, sep="\t", index_col=0)
canonical = {line[1:].split()[0] for line in open(canonical_fa) if line.startswith(">")}

q["gene"] = t2g.loc[q.index, "gene_name"]
q["is_canonical"] = q.index.isin(canonical)
rows = []
for gene, d in q.groupby("gene"):
    reads = d["NumReads"].sum()
    to_canonical = d.loc[d["is_canonical"], "NumReads"].sum()
    rows.append({"gene": gene, "transcripts": len(d), "reads": round(reads, 1),
                 "to_canonical": round(to_canonical, 1),
                 "pct_canonical": round(100 * to_canonical / reads, 1)})
table = pd.DataFrame(rows).sort_values("pct_canonical")
print(table.head(6).to_string(index=False))
print("all genes: % of reads given to the canonical transcript =",
      round(100 * table["to_canonical"].sum() / table["reads"].sum(), 1))
