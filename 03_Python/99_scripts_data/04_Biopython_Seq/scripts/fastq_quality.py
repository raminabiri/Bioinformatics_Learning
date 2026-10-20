# fastq_quality.py: summarise a (gzipped) FASTQ file and keep the good reads
# Usage: python3 fastq_quality.py reads.fastq.gz good.fastq 30
import sys
import gzip
from Bio import SeqIO

in_file = sys.argv[1]
out_file = sys.argv[2]
min_mean_q = int(sys.argv[3])

def mean_quality(record):
    """Arithmetic mean of the Phred scores of one read."""
    q = record.letter_annotations["phred_quality"]
    return sum(q) / len(q)

n_reads = 0
n_bases = 0
good = []
with gzip.open(in_file, "rt") as f:
    for rec in SeqIO.parse(f, "fastq"):
        n_reads = n_reads + 1
        n_bases = n_bases + len(rec.seq)
        if mean_quality(rec) >= min_mean_q:
            good.append(rec)

n_written = SeqIO.write(good, out_file, "fastq")
print("reads:", n_reads)
print("bases:", n_bases)
print(f"mean read length: {n_bases / n_reads:.1f}")
print(f"reads with mean Q >= {min_mean_q}: {n_written} ({n_written / n_reads * 100:.1f}%)")
