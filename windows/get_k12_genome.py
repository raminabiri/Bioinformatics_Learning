#!/usr/bin/env python3
"""Download the E. coli K-12 MG1655 genome (FASTA) and annotation (GFF) and unpack them.

The same two files that 01_Linux/99_scripts_data/data/download.sh makes with curl and gunzip,
but with Python only, so it works on Windows without Linux tools.

Usage (in the folder where you want the files):
    python get_k12_genome.py
Writes ecoli_k12.fna and ecoli_k12.gff and prints their MD5 checksums.
"""
import gzip
import hashlib
import os
import urllib.request

NCBI = ("https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/"
        "GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2")

for suffix, out in [("_genomic.fna.gz", "ecoli_k12.fna"), ("_genomic.gff.gz", "ecoli_k12.gff")]:
    if not os.path.exists(out) or os.path.getsize(out) == 0:
        print(f"downloading {out} ...")
        with urllib.request.urlopen(NCBI + suffix, timeout=300) as response:
            data = gzip.decompress(response.read())
        with open(out, "wb") as fh:
            fh.write(data)
    md5 = hashlib.md5(open(out, "rb").read()).hexdigest()
    print(f"{md5}  {out}  ({os.path.getsize(out):,} bytes)")
