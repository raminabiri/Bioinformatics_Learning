# gb_genes.py: list the genes of a GenBank file with their location and product
# Usage: python3 gb_genes.py rpo_region.gb
import sys
from Bio import SeqIO

def first(qualifiers, key):
    """Return the first value of a qualifier, or '-' if the feature does not have it."""
    if key in qualifiers:
        return qualifiers[key][0]
    return "-"

rec = SeqIO.read(sys.argv[1], "genbank")
print(rec.id, len(rec.seq), "bp")
for f in rec.features:
    if f.type == "source" or f.type == "gene":
        continue
    start = int(f.location.start) + 1          # back to 1-based, as in the GenBank file
    end = int(f.location.end)
    if f.location.strand == 1:
        strand = "+"
    else:
        strand = "-"
    gene = first(f.qualifiers, "gene")
    product = first(f.qualifiers, "product")
    if f.type == "CDS":
        length = len(first(f.qualifiers, "translation"))
        print(f"{f.type}\t{gene}\t{start}\t{end}\t{strand}\t{length} aa\t{product}")
    else:
        print(f"{f.type}\t{gene}\t{start}\t{end}\t{strand}\t-\t{product}")
