#!/usr/bin/env python3
"""Search NCBI Gene and print one row per gene: id, symbol, chromosome accession, start, stop, strand, length.

Usage:
    python3 gene_table.py "rpoB[preferred symbol] AND txid511145[Organism:noexp]"

Contact email comes from $ENTREZ_EMAIL (NCBI asks for one); the API key, if any, from $NCBI_API_KEY.
Neither is ever printed.
"""
import os
import sys

from Bio import Entrez

Entrez.email = os.environ.get("ENTREZ_EMAIL", "your.name@example.org")
Entrez.api_key = os.environ.get("NCBI_API_KEY")      # None = no key: at most 3 requests per second

query = sys.argv[1]

# 1. esearch: query -> list of Gene UIDs
found = Entrez.read(Entrez.esearch(db="gene", term=query, retmax=100))
ids = found["IdList"]
print(f"# query: {query}")
print(f"# hits: {found['Count']}")
if not ids:
    sys.exit(0)

# 2. esummary: UIDs -> one DocumentSummary per gene (one request for all IDs)
summary = Entrez.read(Entrez.esummary(db="gene", id=",".join(ids)))
print("id\tsymbol\tchr_acc\tstart\tstop\tstrand\tlength")
for doc in summary["DocumentSummarySet"]["DocumentSummary"]:
    gid = doc.attributes["uid"]
    # GenomicInfo is the place on the current assembly; it is empty for some old records
    if not doc["GenomicInfo"]:
        print(f"{gid}\t{doc['Name']}\t-\t-\t-\t-\t-")
        continue
    info = doc["GenomicInfo"][0]
    start, stop = int(info["ChrStart"]), int(info["ChrStop"])
    strand = "-" if start > stop else "+"
    length = abs(stop - start) + 1
    print(f"{gid}\t{doc['Name']}\t{info['ChrAccVer']}\t{start}\t{stop}\t{strand}\t{length}")
