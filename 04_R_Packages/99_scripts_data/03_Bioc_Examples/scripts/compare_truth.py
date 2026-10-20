# compare_truth.py: how many of the truly changed genes did DESeq2 find?
# Usage: python3 compare_truth.py deseq2_results.tsv truth.tsv [padj_cutoff]
# Prints: found (true positives), false alarms (false positives), missed (false negatives),
# and writes missed.tsv with the genes DESeq2 did not find.
import sys
import pandas as pd

results = pd.read_csv(sys.argv[1], sep="\t")
truth = pd.read_csv(sys.argv[2], sep="\t")
cutoff = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05

called = set(results[results["padj"] < cutoff]["gene_id"])
true = set(truth["gene_id"])

print(f"padj < {cutoff}: {len(called)} genes called changed; {len(true)} truly changed")
print(f"found (true positives):  {len(called & true)}")
print(f"false alarms:            {len(called - true)}")
print(f"missed:                  {len(true - called)}")

missed = truth[truth["gene_id"].isin(true - called)]
missed = missed.merge(results[["gene_id", "baseMean", "log2FoldChange", "padj"]], on="gene_id")
missed = missed.sort_values("padj").round(3)
missed.to_csv("missed.tsv", sep="\t", index=False)
print("wrote missed.tsv")
