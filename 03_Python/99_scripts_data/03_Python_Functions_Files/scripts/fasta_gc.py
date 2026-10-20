# fasta_gc.py: read a FASTA file (one or more sequences, multi-line) and report length and GC
# Usage: python3 fasta_gc.py file1.fa [file2.fa ...]
import sys


def read_fasta(path):
    """Return a dictionary {sequence id: sequence} for a FASTA file."""
    seqs = {}
    name = None
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith(">"):
                name = line[1:].split()[0]    # the identifier: first word after '>'
                seqs[name] = []
            else:
                seqs[name].append(line)
    result = {}
    for name in seqs:
        result[name] = "".join(seqs[name])   # glue the lines of each sequence together
    return result


def gc_content(seq):
    """Fraction of G and C among the known bases (A, C, G, T; any case)."""
    seq = seq.upper()
    gc = seq.count("G") + seq.count("C")
    acgt = gc + seq.count("A") + seq.count("T")
    return gc / acgt


for path in sys.argv[1:]:
    for name, seq in read_fasta(path).items():
        print(f"{path}\t{name}\t{len(seq)}\t{gc_content(seq) * 100:.2f}")
