# composition.py: percentage of reads from each organism in one sample, as a table and a bar chart
# Usage: python3 composition.py ground_truth.tsv minigut_sample2 composition.png
import sys
import pandas as pd
import matplotlib.pyplot as plt

table_file = sys.argv[1]
sample = sys.argv[2]
png_file = sys.argv[3]

gt = pd.read_csv(table_file, sep="\t")
gt = gt[gt["sample"] == sample]
gt["percent"] = gt["read_pairs"] / gt["read_pairs"].sum() * 100
gt["genus"] = gt["organism"].str.split().str[0]
by_genus = gt.groupby("genus")["percent"].sum().sort_values()

print(by_genus.round(2))
by_genus.round(2).to_csv(f"{sample}_genus.tsv", sep="\t")

fig, ax = plt.subplots(figsize=(7, 6))
ax.barh(by_genus.index, by_genus.values, color="seagreen")
ax.set_xlabel("percent of read pairs")
ax.set_title(f"{sample}: composition by genus")
fig.tight_layout()
fig.savefig(png_file, dpi=120)
print("saved", png_file)
