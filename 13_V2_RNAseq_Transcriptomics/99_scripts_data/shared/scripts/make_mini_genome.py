#!/usr/bin/env python3
"""Build the part-13 'mini-genome': 20 human gene loci from Ensembl, with annotation.

Usage:
    python3 make_mini_genome.py genes.tsv OUTDIR

genes.tsv has a header and the columns  symbol  ncbi_gene_id  ctrl_cpm  log2fc  (see the shared data folder).
For every gene the Ensembl REST server (release 116, GRCh38) gives the gene, its transcripts and exons.
Each gene locus (gene start-1000 .. gene end+1000, + strand of the chromosome) becomes one contig named
after the gene, so the mini-genome has 20 contigs. Writes into OUTDIR:
    mini_genome.fa            the 20 contigs
    mini_genes.gtf            all transcripts and exons, in contig coordinates (GTF is 1-based)
    transcripts_all.fa        spliced sequence of every transcript (for Salmon / kallisto)
    transcripts_canonical.fa  the Ensembl canonical transcript of each gene (reads are simulated from these)
    tx2gene.tsv               transcript -> gene table (for tximport)
Ensembl sometimes answers 500/503; every request is retried (same idea as 12/01 ens_ids.py).
"""
import os
import sys
import time

import requests

SERVER = "https://rest.ensembl.org"
FLANK = 1000
COMP = str.maketrans("ACGTNacgtn", "TGCANtgcan")


def ask(path, params=None):
    for attempt in range(1, 9):
        r = requests.get(SERVER + path, params=params, timeout=120,
                         headers={"Accept": "application/json"})
        if r.status_code == 200:
            return r.json()
        print(f"  {path}: HTTP {r.status_code}, retry {attempt}", file=sys.stderr)
        time.sleep(3 * attempt)
    sys.exit(f"{path}: gave up")


genes_file, outdir = sys.argv[1:3]
os.makedirs(outdir, exist_ok=True)
symbols = [line.split("\t")[0] for line in open(genes_file).read().splitlines()[1:] if line.strip()]

fa = open(os.path.join(outdir, "mini_genome.fa"), "w")
gtf = open(os.path.join(outdir, "mini_genes.gtf"), "w")
tx_all = open(os.path.join(outdir, "transcripts_all.fa"), "w")
tx_can = open(os.path.join(outdir, "transcripts_canonical.fa"), "w")
t2g = open(os.path.join(outdir, "tx2gene.tsv"), "w")
t2g.write("transcript_id\tgene_id\tgene_name\n")

for sym in symbols:
    g = ask(f"/lookup/symbol/homo_sapiens/{sym}", {"expand": 1})
    chrom, gstart, gend, gstrand = g["seq_region_name"], g["start"], g["end"], g["strand"]
    cstart = gstart - FLANK                                   # contig position 1 = chromosome position cstart
    seq = ask(f"/sequence/region/human/{chrom}:{cstart}..{gend + FLANK}:1")["seq"].upper()
    fa.write(f">{sym} {g['id']}.{g['version']} {chrom}:{cstart}-{gend + FLANK} Ensembl116\n")
    for i in range(0, len(seq), 60):
        fa.write(seq[i:i + 60] + "\n")
    strand = "+" if gstrand == 1 else "-"
    to_contig = lambda pos: pos - cstart + 1                  # chromosome -> contig coordinate (both 1-based)
    attr_g = f'gene_id "{g["id"]}"; gene_name "{sym}";'
    gtf.write(f"{sym}\tEnsembl116\tgene\t{to_contig(gstart)}\t{to_contig(gend)}\t.\t{strand}\t.\t{attr_g}\n")
    canonical = g["canonical_transcript"].split(".")[0]
    n_tx = 0
    for t in g["Transcript"]:
        exons = sorted(t["Exon"], key=lambda e: e["start"])
        attr_t = f'{attr_g} transcript_id "{t["id"]}"; transcript_biotype "{t["biotype"]}";'
        gtf.write(f"{sym}\tEnsembl116\ttranscript\t{to_contig(t['start'])}\t{to_contig(t['end'])}\t.\t{strand}\t.\t{attr_t}\n")
        parts = []
        for e in exons:
            s, e_ = to_contig(e["start"]), to_contig(e["end"])
            gtf.write(f"{sym}\tEnsembl116\texon\t{s}\t{e_}\t.\t{strand}\t.\t{attr_t}\n")
            parts.append(seq[s - 1:e_])                       # contig is 1-based, Python 0-based
        cdna = "".join(parts)
        if strand == "-":
            cdna = cdna.translate(COMP)[::-1]
        tx_all.write(f">{t['id']} {sym}\n{cdna}\n")
        t2g.write(f"{t['id']}\t{g['id']}\t{sym}\n")
        if t["id"] == canonical:
            tx_can.write(f">{t['id']} {sym}\n{cdna}\n")
        n_tx += 1
    print(f"{sym}\t{g['id']}\tchr{chrom}\t{strand}\t{len(seq)} bp\t{n_tx} transcripts\tcanonical {canonical}")
    time.sleep(0.2)

for fh in (fa, gtf, tx_all, tx_can, t2g):
    fh.close()
