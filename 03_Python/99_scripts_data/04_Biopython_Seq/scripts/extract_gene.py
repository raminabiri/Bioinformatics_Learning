# extract_gene.py: cut one gene out of a genome, translate it, and write DNA + protein FASTA
# Usage: python3 extract_gene.py genome.fna name start end strand
# Example: python3 extract_gene.py ecoli_k12.fna rpoB 4181245 4185273 +
import sys
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

genome_file = sys.argv[1]
name = sys.argv[2]
start = int(sys.argv[3])
end = int(sys.argv[4])
strand = sys.argv[5]

genome = SeqIO.read(genome_file, "fasta")
dna = genome.seq[start - 1:end]           # GFF coordinates -> Python slice
if strand == "-":
    dna = dna.reverse_complement()
protein = dna.translate(table=11, cds=True)

dna_rec = SeqRecord(dna, id=name, description=f"{genome.id}:{start}-{end}({strand})")
prot_rec = SeqRecord(protein, id=name, description=f"translated with table 11, {len(protein)} aa")
SeqIO.write(dna_rec, f"{name}.fna", "fasta")
SeqIO.write(prot_rec, f"{name}.faa", "fasta")
print(f"{name}: {len(dna)} nt, {len(protein)} aa, starts with {protein[:10]}")
