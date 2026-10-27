#!/usr/bin/env python3
"""Map human gene symbols to Ensembl IDs (and back to NCBI Gene IDs) with the Ensembl REST API.

Usage:
    python3 ens_ids.py SYMBOL [SYMBOL ...] > table.tsv

One POST request looks up all symbols at once; then one GET per gene asks for the
NCBI Gene (EntrezGene) cross-reference. Ensembl sometimes answers 500/503 when busy,
so every request is retried a few times. Messages about retries go to stderr.
"""
import sys
import time

import requests

SERVER = "https://rest.ensembl.org"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


def ask(method, path, **kwargs):
    """Send one request; retry on busy-server answers; return the JSON answer."""
    for attempt in range(1, 7):
        r = requests.request(method, SERVER + path, headers=HEADERS, timeout=90, **kwargs)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 429:                       # too many requests: wait as told
            wait = float(r.headers.get("Retry-After", 5))
        elif r.status_code in (500, 502, 503, 504):    # busy server: wait a bit longer each time
            wait = 3 * attempt
        else:                                          # 400 = bad request: retrying will not help
            sys.exit(f"{method} {path}: HTTP {r.status_code} {r.text[:200]}")
        print(f"  {path}: HTTP {r.status_code}, retry {attempt} in {wait:.0f} s", file=sys.stderr)
        time.sleep(wait)
    sys.exit(f"{method} {path}: gave up")


symbols = sys.argv[1:]
genes = ask("POST", "/lookup/symbol/homo_sapiens", json={"symbols": symbols})

print("symbol\tensembl_id\tchrom\tstart\tend\tstrand\tbiotype\tcanonical_transcript\tncbi_gene_id")
for s in symbols:
    g = genes.get(s)
    if g is None:                                      # not an official symbol in this release
        print(f"{s}\tNOT_FOUND" + "\t-" * 7)
        continue
    xrefs = ask("GET", f"/xrefs/id/{g['id']}", params={"external_db": "EntrezGene"})
    entrez = ",".join(x["primary_id"] for x in xrefs) or "-"
    print(f"{s}\t{g['id']}.{g['version']}\t{g['seq_region_name']}\t{g['start']}\t{g['end']}"
          f"\t{g['strand']}\t{g['biotype']}\t{g['canonical_transcript']}\t{entrez}")
    time.sleep(0.1)                                    # stay well below 15 requests per second
