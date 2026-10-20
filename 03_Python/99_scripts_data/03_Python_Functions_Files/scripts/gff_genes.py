# gff_genes.py: read a GFF file line by line and summarise its genes
# Usage: python3 gff_genes.py ecoli_k12.gff
import sys

gff_file = sys.argv[1]

n_genes = 0
strands = {}
total_length = 0
rpo_genes = []

with open(gff_file) as f:
    for line in f:
        if line.startswith("#"):          # skip comment lines
            continue
        cols = line.rstrip("\n").split("\t")
        if cols[2] != "gene":             # keep only gene lines
            continue
        start = int(cols[3])
        end = int(cols[4])
        strand = cols[6]
        n_genes = n_genes + 1
        total_length = total_length + (end - start + 1)
        strands[strand] = strands.get(strand, 0) + 1
        if "Name=rpo" in cols[8]:
            rpo_genes.append(start)

print("genes:", n_genes)
print("strands:", strands)
print(f"mean length: {total_length / n_genes:.1f}")
print("rpo genes start at:", rpo_genes)
