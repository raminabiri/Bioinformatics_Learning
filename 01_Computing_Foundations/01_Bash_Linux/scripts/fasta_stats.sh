#!/usr/bin/env bash
# Summary statistics for a (multi-line, optionally gzipped) FASTA file.
# Usage: bash fasta_stats.sh file.fa[.gz]
# Prints: file, number of sequences, total length, shortest, longest, GC% (over A/C/G/T; NA for protein)
set -euo pipefail
[ $# -eq 1 ] || { echo "Usage: $(basename "$0") file.fa[.gz]" >&2; exit 1; }
f=$1
[ -s "$f" ] || { echo "Error: '$f' not found or empty" >&2; exit 1; }
case "$f" in *.gz) reader="zcat";; *) reader="cat";; esac

$reader "$f" | awk -v file="$(basename "$f")" '
  /^>/ { if (len != "") lens[n] = len; n++; len = 0; next }
       { gsub(/[ \t\r]/, ""); len += length($0); tot += length($0)
         gc += gsub(/[GCgc]/, ""); at += gsub(/[ATat]/, ""); nn += gsub(/[Nn]/, "") }
  END  { if (n == 0) { print "Error: no FASTA header found" > "/dev/stderr"; exit 1 }
         lens[n] = len; min = max = lens[1]
         for (i = 2; i <= n; i++) { if (lens[i] < min) min = lens[i]; if (lens[i] > max) max = lens[i] }
         # GC% only makes sense for nucleotides; computed over A/C/G/T (N excluded)
         gcp = ((gc + at + nn) / tot > 0.9 && gc + at > 0) ? sprintf("%.2f", gc / (gc + at) * 100) : "NA(protein?)"
         printf "file\tn_seqs\ttotal_len\tmin_len\tmax_len\tGC%%\n%s\t%d\t%d\t%d\t%d\t%s\n", file, n, tot, min, max, gcp }'
