# gene_lengths.py: summarise the gene table and draw a histogram of gene lengths
# Usage: python3 gene_lengths.py genes.tsv gene_lengths.png
import sys
import pandas as pd
import matplotlib.pyplot as plt

table_file = sys.argv[1]
png_file = sys.argv[2]

df = pd.read_csv(table_file, sep="\t")
print(df["length"].describe())

fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(df["length"], bins=60, color="steelblue")
ax.axvline(df["length"].median(), color="black", linestyle="--", label="median")
ax.set_xlabel("gene length (bp)")
ax.set_ylabel("number of genes")
ax.set_title(f"E. coli K-12 MG1655: {len(df)} genes")
ax.legend()
fig.tight_layout()
fig.savefig(png_file, dpi=120)
print("saved", png_file)
