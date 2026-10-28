#!/usr/bin/env python3
"""Simulate a small stranded paired-end RNA-seq experiment with a KNOWN answer (part 13).

Usage:
    python3 simulate_reads.py genes.tsv transcripts_canonical.fa OUTDIR [PAIRS_PER_SAMPLE]

Design: 6 samples, ctrl_1..3 (untreated) and dex_1..3 (dexamethasone), 100 000 read pairs EXPECTED per sample
by default (the real totals differ between samples, as library sizes do in real data).
For every gene, the expected share of reads = ctrl_cpm x transcript length (longer transcripts give more
fragments), times 2^log2fc in the dex samples (genes.tsv). The number of fragments per gene and sample is drawn
from a negative binomial (dispersion 0.05, typical of biological replicates), so replicates differ as in real data.
Fragments (mean 250 bp) are cut at random positions of the canonical transcript; reads are 2 x 100 bp.
Library type: stranded, dUTP / Illumina TruSeq ("reverse"): read 1 comes from the antisense strand.
Base qualities fall slowly along the read; sequencing errors follow the qualities (about 0.3% overall).
Writes OUTDIR/<sample>_R1.fastq.gz and _R2.fastq.gz, and OUTDIR/truth_counts.tsv (fragments per gene).
Random seed 13, so every run gives the same files.
"""
import gzip
import os
import sys

import numpy as np

genes_file, tx_fa, outdir = sys.argv[1:4]
pairs = int(sys.argv[4]) if len(sys.argv) > 4 else 100_000
os.makedirs(outdir, exist_ok=True)
rng = np.random.default_rng(13)
COMP = str.maketrans("ACGTN", "TGCAN")
READ_LEN, FRAG_MEAN, FRAG_SD, DISPERSION = 100, 250, 30, 0.05

# gene table and canonical transcripts (header: ">ENST... SYMBOL")
genes = [l.split("\t") for l in open(genes_file).read().splitlines()[1:] if l.strip()]
seqs, name = {}, None
for line in open(tx_fa):
    line = line.strip()
    if line.startswith(">"):
        name = line.split()[1]
        seqs[name] = []
    else:
        seqs[name].append(line)
seqs = {k: "".join(v) for k, v in seqs.items()}

symbols = [g[0] for g in genes]
base = np.array([float(g[2]) * len(seqs[g[0]]) for g in genes])
lfc = np.array([float(g[3]) for g in genes])
samples = [("ctrl_1", 0), ("ctrl_2", 0), ("ctrl_3", 0), ("dex_1", 1), ("dex_2", 1), ("dex_3", 1)]

# per-position quality: Q37 at the start, falling to ~Q25 at base 100 (Phred + 33)
qual = np.clip(np.round(37 - 12 * (np.arange(READ_LEN) / (READ_LEN - 1)) ** 2), 2, 41).astype(int)
qual_str = "".join(chr(q + 33) for q in qual)
err_p = 10 ** (-qual / 10)


def mutate(read):
    """Change bases where a random number falls below the error probability of that position."""
    hits = np.nonzero(rng.random(READ_LEN) < err_p)[0]
    if len(hits) == 0:
        return read
    r = list(read)
    for i in hits:
        r[i] = rng.choice([b for b in "ACGT" if b != r[i]])
    return "".join(r)


truth = {s: [] for s, _ in samples}
for sample, treated in samples:
    mean = base * (2 ** (lfc * treated))
    mean = mean / mean.sum() * pairs
    # negative binomial with mean m and dispersion d: n = 1/d, p = n / (n + m)
    n = 1 / DISPERSION
    counts = rng.negative_binomial(n, n / (n + mean))
    truth[sample] = counts
    with gzip.open(os.path.join(outdir, f"{sample}_R1.fastq.gz"), "wt", compresslevel=4) as f1, \
         gzip.open(os.path.join(outdir, f"{sample}_R2.fastq.gz"), "wt", compresslevel=4) as f2:
        k = 0
        for sym, c in zip(symbols, counts):
            tx = seqs[sym]
            for _ in range(c):
                flen = int(min(max(rng.normal(FRAG_MEAN, FRAG_SD), READ_LEN + 20), len(tx)))
                start = int(rng.integers(0, len(tx) - flen + 1))
                frag = tx[start:start + flen]
                # dUTP stranded: read 1 = reverse complement of the fragment end, read 2 = fragment start
                r1 = mutate(frag[-READ_LEN:].translate(COMP)[::-1])
                r2 = mutate(frag[:READ_LEN])
                k += 1
                f1.write(f"@{sample}.{k} {sym}/1\n{r1}\n+\n{qual_str}\n")
                f2.write(f"@{sample}.{k} {sym}/2\n{r2}\n+\n{qual_str}\n")
    print(f"{sample}\t{counts.sum()} pairs")

with open(os.path.join(outdir, "truth_counts.tsv"), "w") as out:
    out.write("symbol\tlog2fc_true\t" + "\t".join(s for s, _ in samples) + "\n")
    for i, sym in enumerate(symbols):
        out.write(f"{sym}\t{lfc[i]}\t" + "\t".join(str(truth[s][i]) for s, _ in samples) + "\n")
