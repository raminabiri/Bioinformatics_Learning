#!/usr/bin/env python3
"""Python version of parts of gene_tour.sh (section 00): NCBI Taxonomy, Nucleotide, Gene and PubMed via Bio.Entrez.

Usage:
  python3 entrez_tour.py --email you@uni.edu [--gene rpoB] [--term "rifampicin resistance"]
NCBI rule: max 3 requests/s without an API key (10/s with Entrez.api_key).
"""
import argparse
import socket
import time
from Bio import Entrez

socket.setdefaulttimeout(30)   # a stalled connection fails after 30 s instead of hanging forever

TAXID = "511145"   # E. coli K-12 MG1655
GENOME_QUERY = ('"Escherichia coli str. K-12 substr. MG1655"[Organism] '
                'AND refseq[filter] AND "complete genome"[Title]')
Entrez.max_tries = 5            # Biopython retries failed requests (default 3)


def call(func, **kw):
    """One E-utilities call, parsed, followed by a pause (rate limit)."""
    with func(**kw) as h:
        out = Entrez.read(h)
    time.sleep(0.4)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--email", required=True)
    ap.add_argument("--gene", default="rpoB")
    ap.add_argument("--term", default="rifampicin resistance")
    args = ap.parse_args()
    Entrez.email = args.email

    print("== 1. Taxonomy")
    tax = call(Entrez.efetch, db="taxonomy", id=TAXID)[0]
    print(f"taxid={tax['TaxId']}  name={tax['ScientificName']}  rank={tax['Rank']}")

    print("== 2. Nucleotide (RefSeq complete genome)")
    ids = call(Entrez.esearch, db="nuccore", term=GENOME_QUERY, retmax=100)["IdList"]
    docs = call(Entrez.esummary, db="nuccore", id=",".join(ids))
    # NC_ = curated reference; NZ_ = RefSeq copy of a GenBank submission (other labs' resequencing)
    print(f"records: {len(docs)}  (NC_: {sum(s['AccessionVersion'].startswith('NC_') for s in docs)})")
    for s in docs:
        if s["AccessionVersion"].startswith("NC_"):
            print(f"{s['AccessionVersion']}  length={int(s['Length'])}  {s['Title']}")

    print("== 3. Gene")
    q = f"{args.gene}[Gene Name] AND {TAXID}[Taxonomy ID]"
    gid = call(Entrez.esearch, db="gene", term=q)["IdList"]
    doc = call(Entrez.esummary, db="gene", id=gid[0])["DocumentSummarySet"]["DocumentSummary"][0]
    loc = doc["GenomicInfo"][0]
    print(f"GeneID={gid[0]}  symbol={doc['Name']}  {doc['Description']}  "
          f"{loc['ChrAccVer']}:{int(loc['ChrStart']) + 1}-{int(loc['ChrStop']) + 1}")

    print("== 4. PubMed")
    n = call(Entrez.esearch, db="pubmed", term=f"{args.gene} AND {args.term}", retmax=0)["Count"]
    print(f'PubMed hits for "{args.gene} AND {args.term}": {n}')


if __name__ == "__main__":
    main()
