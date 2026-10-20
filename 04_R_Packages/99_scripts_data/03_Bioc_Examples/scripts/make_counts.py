# make_counts.py: SIMULATED RNA-seq read counts for E. coli genes, with a known answer
# 3 wild-type (WT) and 3 rifampicin-resistant (RifR) samples. 100 genes, picked at random,
# truly change between the groups; truth.tsv lists them. This is not real biology:
# it is practice data, so you can check whether DESeq2 finds the right genes.
# Usage: python3 make_counts.py ecoli_k12.gff
# Writes: counts.tsv, samples.tsv, truth.tsv (in the current folder)
import sys
import numpy as np
import pandas as pd

gff_file = sys.argv[1]
rng = np.random.default_rng(42)

# 1. protein-coding genes from the GFF: locus tag (b0001...), name, length
rows = []
with open(gff_file) as f:
    for line in f:
        if line.startswith("#"):
            continue
        cols = line.rstrip("\n").split("\t")
        if cols[2] != "gene" or "gene_biotype=protein_coding" not in cols[8]:
            continue
        attrs = dict(part.split("=", 1) for part in cols[8].split(";"))
        rows.append((attrs["locus_tag"], attrs["Name"], int(cols[4]) - int(cols[3]) + 1))
genes = pd.DataFrame(rows, columns=["gene_id", "name", "length"])

# 2. baseline expression of each gene: very different from gene to gene (log-normal)
base = np.exp(rng.normal(5.0, 1.5, len(genes))) * genes["length"] / 1000

# 3. pick 100 genes that change: 50 up, 50 down, by 2x to 8x (log2 fold change 1 to 3)
changed = rng.choice(len(genes), 100, replace=False)
log2fc = np.zeros(len(genes))
log2fc[changed[:50]] = rng.uniform(1, 3, 50)
log2fc[changed[50:]] = -rng.uniform(1, 3, 50)

# 4. counts = negative binomial noise around the mean; each sample has its own depth
samples = ["WT_1", "WT_2", "WT_3", "RifR_1", "RifR_2", "RifR_3"]
depth = [0.8, 1.0, 1.2, 0.9, 1.1, 1.0]
dispersion = 0.05
counts = pd.DataFrame({"gene_id": genes["gene_id"]})
for s, d in zip(samples, depth):
    mean = base * d * (2 ** log2fc if s.startswith("RifR") else 1)
    n = 1 / dispersion
    counts[s] = rng.negative_binomial(n, n / (n + mean))

counts.to_csv("counts.tsv", sep="\t", index=False)
pd.DataFrame({"sample": samples, "condition": ["WT"] * 3 + ["RifR"] * 3}).to_csv(
    "samples.tsv", sep="\t", index=False)
truth = genes.loc[changed, ["gene_id", "name"]].assign(true_log2FC=log2fc[changed].round(2))
truth.to_csv("truth.tsv", sep="\t", index=False)
print(f"wrote counts.tsv ({len(genes)} genes x {len(samples)} samples), samples.tsv, truth.tsv ({len(truth)} changed genes)")
