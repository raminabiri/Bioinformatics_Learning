# make_table.py: turn "count accession" lines into a table with organism names
# Usage: python3 make_table.py counts/minigut.tsv names.tsv minigut tables/minigut.tsv
# Output columns (same as ground_truth.tsv): sample, read_pairs, accession, organism
import sys

counts_file, names_file, sample, out_file = sys.argv[1:5]

# accession -> organism name, from the lookup table
names = {}
with open(names_file) as f:
    next(f)                                   # skip the header line
    for line in f:
        accession, organism = line.rstrip("\n").split("\t")
        names[accession] = organism

with open(counts_file) as f, open(out_file, "w") as out:
    out.write("sample\tread_pairs\taccession\torganism\n")
    for line in f:
        count, accession = line.split()       # e.g. "  28912 NC_006347.1"
        organism = names.get(accession, "unknown")
        out.write(f"{sample}\t{count}\t{accession}\t{organism}\n")
