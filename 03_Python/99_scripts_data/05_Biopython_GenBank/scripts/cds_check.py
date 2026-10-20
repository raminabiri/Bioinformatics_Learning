# cds_check.py: cut every protein-coding gene (CDS) out of the genome, translate it, and check it
# Usage: python3 cds_check.py ecoli_k12.fna ecoli_k12.gff
import sys
from Bio import SeqIO
from Bio.Seq import Seq

def get_attribute(attributes, key):
    for part in attributes.split(";"):
        if part.startswith(key + "="):
            return part[len(key) + 1:]
    return ""

genome = SeqIO.read(sys.argv[1], "fasta").seq

# 1. collect the CDS lines; a few genes have two CDS lines with the same ID (two pieces)
cds = {}
with open(sys.argv[2]) as f:
    for line in f:
        if line.startswith("#"):
            continue
        cols = line.rstrip("\n").split("\t")
        if cols[2] != "CDS" or "pseudo=true" in cols[8]:
            continue
        cds_id = get_attribute(cols[8], "ID")
        if cds_id not in cds:
            cds[cds_id] = {"gene": get_attribute(cols[8], "gene"), "strand": cols[6], "pieces": []}
        cds[cds_id]["pieces"].append((int(cols[3]), int(cols[4])))

# 2. cut, translate and check each CDS
starts = {}
stops = {}
broken = []
for cds_id in cds:
    c = cds[cds_id]
    dna = Seq("")
    for start, end in sorted(c["pieces"]):
        dna = dna + genome[start - 1:end]
    if c["strand"] == "-":
        dna = dna.reverse_complement()
    starts[str(dna[:3])] = starts.get(str(dna[:3]), 0) + 1
    stops[str(dna[-3:])] = stops.get(str(dna[-3:]), 0) + 1
    protein = dna.translate(table=11)
    if "*" in protein[:-1]:                    # a stop codon inside the gene
        broken.append(c["gene"])

print("CDS:", len(cds))
print("start codons:", starts)
print("stop codons:", stops)
print("CDS with an internal stop:", broken)
