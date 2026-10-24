#!/usr/bin/env python3
"""List mobile elements near each resistance gene (part 08, module 03).

Inputs:
  GENBANK  a GenBank record of the plasmid (its mobile_element features are read)
  AMR_TSV  an AMRFinderPlus table run with --name (column 3 = contig, 4-5 = start-stop)
  CONTIG   the contig name in AMR_TSV that holds this plasmid
  DIST     distance in bp (default 5000)
Output (tab-separated): gene, gene start-stop, element, element start-stop, distance
(distance 0 = overlapping)

Usage: python3 gene_context.py pEK499.gb isoF.amr.tsv isoF_pEK499 [5000]
"""
import re
import sys

gb, amr_tsv, contig = sys.argv[1:4]
dist = int(sys.argv[4]) if len(sys.argv) > 4 else 5000

elements, loc = [], None
for line in open(gb):
    if line.startswith('     mobile_element'):
        loc = line.split()[1]
    elif loc and '/mobile_element_type=' in line:
        name = line.split('=', 1)[1].strip().strip('"').split(':')[-1]
        start, end = map(int, re.findall(r'\d+', loc)[:2])
        elements.append((start, end, name))
        loc = None

print('gene\tgene_pos\telement\telement_pos\tdistance')
for line in open(amr_tsv):
    f = line.rstrip('\n').split('\t')
    if f[0] == 'Name' or f[2] != contig or f[8] != 'core':
        continue
    g_start, g_end, gene = int(f[3]), int(f[4]), f[6]
    for e_start, e_end, name in elements:
        d = max(0, e_start - g_end, g_start - e_end)
        if d <= dist:
            print(f'{gene}\t{g_start}-{g_end}\t{name}\t{e_start}-{e_end}\t{d}')
