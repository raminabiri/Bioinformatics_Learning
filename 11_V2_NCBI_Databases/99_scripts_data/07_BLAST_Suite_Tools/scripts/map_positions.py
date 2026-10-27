#!/usr/bin/env python3
"""Map residue numbers from the query to the subject through one BLAST alignment.

Make the input with:
    blastp -query Q.faa -db DB -max_hsps 1 -max_target_seqs 1 -outfmt "6 qstart sstart qseq sseq" > hsp.tsv
Usage:
    python3 map_positions.py hsp.tsv 435 445 450
Prints "query residue+number <-> subject residue+number"; a gap in the subject is shown as "-".
"""
import sys

qstart, sstart, qseq, sseq = open(sys.argv[1]).read().split()[:4]
wanted = {int(p) for p in sys.argv[2:]}

q, s = int(qstart), int(sstart)
for a, b in zip(qseq, sseq):
    if a != "-" and q in wanted:
        print(f"query {a}{q}  <->  subject {b}{s if b != '-' else ''}")
    if a != "-":          # a gap in the query does not use up a query residue
        q += 1
    if b != "-":
        s += 1
