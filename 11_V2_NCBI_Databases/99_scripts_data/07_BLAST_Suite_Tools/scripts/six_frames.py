#!/usr/bin/env python3
"""Longest ORF (ATG ... stop) in each of the six reading frames of the first sequence in a FASTA file.

Usage:
    python3 six_frames.py seq.fna [MIN_AA]
Frames +1..+3 read the given strand from base 1, 2, 3; frames -1..-3 read the reverse complement.
This is what ORFfinder does on the NCBI web site, in its simplest form (standard genetic code, ATG start only).
"""
import sys

from Bio import SeqIO

record = next(SeqIO.parse(sys.argv[1], "fasta"))
min_aa = int(sys.argv[2]) if len(sys.argv) > 2 else 30
print(f"{record.id}: {len(record.seq)} bp")

for strand, seq in (("+", record.seq), ("-", record.seq.reverse_complement())):
    for offset in range(3):
        frame = seq[offset:]
        frame = frame[: len(frame) // 3 * 3]          # whole codons only
        protein = str(frame.translate())
        best = ""
        for piece in protein.split("*"):             # stretches between stop codons
            start = piece.find("M")
            if start != -1 and len(piece) - start > len(best):
                best = piece[start:]
        if len(best) >= min_aa:
            print(f"frame {strand}{offset + 1}: longest ORF {len(best)} aa  {best[:12]}...")
        else:
            print(f"frame {strand}{offset + 1}: no ORF >= {min_aa} aa")
