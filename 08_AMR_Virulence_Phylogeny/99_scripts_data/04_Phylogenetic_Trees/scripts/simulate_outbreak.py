#!/usr/bin/env python3
"""Simulate a core-genome alignment of 20 hospital isolates on a KNOWN tree (part 08, module 04).

A random 100 kb "core genome" evolves down a fixed tree. Branch lengths are numbers of SNPs,
and every SNP hits a new site (infinite sites), so the SNP distance between two isolates is
exactly the sum of branch lengths between them in the true tree.

True story hidden in the data (the learner has to find it):
  clone A  (STa, blaKPC): H1-01 H1-02 H1-03 H2-01 H2-02 H2-03; the H2 isolates sit INSIDE the
           H1 diversity = transmission from hospital 1 to hospital 2
  clone B  (STb, iuc):    H3-01 .. H3-05, only in hospital 3 = local outbreak
  sporadic: 9 unrelated isolates; one of them (H2-05) also carries blaKPC (plasmid, not clone)
  Ref     : outgroup

Usage: python3 simulate_outbreak.py OUTDIR
Writes OUTDIR/core_full.aln, OUTDIR/metadata.tsv, OUTDIR/true_tree.nwk
"""
import os
import random
import sys

outdir = sys.argv[1]
os.makedirs(outdir, exist_ok=True)
random.seed(2026)
L = 100_000

# (name, branch length in SNPs, children)
clone_a = ('A', 350, [('H1-01', 1, []), ('H1-02', 2, []),
                      ('a1', 1, [('H1-03', 1, []),
                                 ('a2', 2, [('H2-01', 1, []), ('H2-02', 0, []), ('H2-03', 2, [])])])])
clone_b = ('B', 420, [('H3-01', 2, []), ('H3-02', 1, []),
                      ('b1', 3, [('H3-03', 3, []), ('H3-04', 1, [])]), ('H3-05', 4, [])])
sporadic = ['H1-04', 'H2-04', 'H3-06', 'H1-05', 'H2-05', 'H3-07', 'H1-06', 'H2-06', 'H3-08']


def backbone(names, lengths):
    """Caterpillar backbone: each step 60 SNPs deeper, one sporadic isolate per step."""
    if len(names) == 1:
        return (names[0], lengths[0], [])
    return ('s' + names[0], 60, [(names[0], lengths[0], []), backbone(names[1:], lengths[1:])])


spor_len = [random.randint(450, 900) for _ in sporadic]
ingroup = ('ING', 0, [clone_a, ('BS', 80, [clone_b, backbone(sporadic, spor_len)])])
tree = ('root', 0, [('Ref', 1500, []), ingroup])

base = [random.choice('ACGT') for _ in range(L)]
free_sites = list(range(L))
random.shuffle(free_sites)
seqs = {}


def evolve(node, seq):
    name, length, children = node
    seq = seq[:]
    for _ in range(length):
        site = free_sites.pop()
        seq[site] = random.choice([b for b in 'ACGT' if b != seq[site]])
    if not children:
        seqs[name] = ''.join(seq)
    for child in children:
        evolve(child, seq)


def newick(node):
    name, length, children = node
    if not children:
        return f'{name}:{length}'
    inner = ','.join(newick(c) for c in children)
    return f'({inner}):{length}' if name != 'root' else f'({inner});'


evolve(tree, base)

with open(f'{outdir}/core_full.aln', 'w') as out:
    for name in sorted(seqs):
        out.write(f'>{name}\n')
        s = seqs[name]
        for i in range(0, L, 80):
            out.write(s[i:i + 80] + '\n')
with open(f'{outdir}/true_tree.nwk', 'w') as out:
    out.write(newick(tree) + '\n')

clone_a_tips = {'H1-01', 'H1-02', 'H1-03', 'H2-01', 'H2-02', 'H2-03'}
clone_b_tips = {'H3-01', 'H3-02', 'H3-03', 'H3-04', 'H3-05'}
st_other = iter('cdefghijk')
# clone A appears in H1 first, then in H2; clone B within a few weeks in H3
MONTH = {'H1-01': 2, 'H1-02': 3, 'H1-03': 4, 'H2-01': 5, 'H2-02': 5, 'H2-03': 6,
         'H3-01': 3, 'H3-02': 3, 'H3-03': 4, 'H3-04': 4, 'H3-05': 5}
with open(f'{outdir}/metadata.tsv', 'w') as out:
    out.write('isolate\thospital\tmonth\tST\tblaKPC\tiuc\n')
    for name in sorted(seqs):
        if name == 'Ref':
            out.write('Ref\treference\tNA\tSTref\tno\tno\n')
            continue
        hosp = 'H' + name[1]
        month = MONTH.get(name, 3 + int(name[3:]) % 4)
        if name in clone_a_tips:
            st, kpc, iuc = 'STa', 'yes', 'no'
        elif name in clone_b_tips:
            st, kpc, iuc = 'STb', 'no', 'yes'
        else:
            st, kpc, iuc = 'ST' + next(st_other), 'yes' if name == 'H2-05' else 'no', 'no'
        out.write(f'{name}\t{hosp}\t2026-{month:02d}\t{st}\t{kpc}\t{iuc}\n')
print(f'isolates: {len(seqs)}  alignment length: {L}  SNP sites used: {L - len(free_sites)}')
print('Done:', outdir)
