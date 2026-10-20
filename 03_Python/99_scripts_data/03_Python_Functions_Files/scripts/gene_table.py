# gene_table.py: write a table (TSV) of all genes in a GFF file: name, start, end, strand, length
# Usage: python3 gene_table.py ecoli_k12.gff genes.tsv
import sys


def get_attribute(attributes, key):
    """From a GFF column 9 like 'ID=x;Name=rpoB;...' return the value of key, or '' if absent."""
    for part in attributes.split(";"):
        if part.startswith(key + "="):
            return part[len(key) + 1:]
    return ""


gff_file = sys.argv[1]
out_file = sys.argv[2]

n = 0
with open(gff_file) as f, open(out_file, "w") as out:
    out.write("name\tstart\tend\tstrand\tlength\n")
    for line in f:
        if line.startswith("#"):
            continue
        cols = line.rstrip("\n").split("\t")
        if cols[2] != "gene":
            continue
        start = int(cols[3])
        end = int(cols[4])
        name = get_attribute(cols[8], "Name")
        out.write(f"{name}\t{start}\t{end}\t{cols[6]}\t{end - start + 1}\n")
        n = n + 1

print(f"wrote {n} genes to {out_file}")
