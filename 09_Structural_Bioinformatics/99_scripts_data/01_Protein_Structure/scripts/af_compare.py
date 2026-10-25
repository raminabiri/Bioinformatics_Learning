#!/usr/bin/env python3
"""Compare an AlphaFold model with an experimental structure (part 09, module 01).

Usage: python3 af_compare.py MODEL.pdb|cif EXPERIMENT.cif[.gz] CHAIN [RESIDUES]
  MODEL      AlphaFold model (pLDDT is stored in the B-factor column)
  EXPERIMENT experimental structure; CHAIN = its chain for the same protein
  RESIDUES   optional comma-separated residue numbers to report (e.g. a binding pocket)
Prints: pLDDT classes, CA RMSD after superposition on all common residues,
        and pLDDT + per-residue CA distance for the chosen residues.
Residues are matched by number, so the model and the experiment must use the same numbering.
"""
import sys
import gemmi

model_path, exp_path, chain_name = sys.argv[1:4]
chosen = [int(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else []

model = gemmi.read_structure(model_path)[0][0]           # AlphaFold: one model, one chain
exp = gemmi.read_structure(exp_path)[0][chain_name]

plddt = {r.seqid.num: r['CA'][0].b_iso for r in model if r.find_atom('CA', '*')}
bins = [('very high (>90)', 90, 101), ('confident (70-90)', 70, 90),
        ('low (50-70)', 50, 70), ('very low (<50)', 0, 50)]
print(f'model residues: {len(plddt)}  mean pLDDT: {sum(plddt.values()) / len(plddt):.1f}')
for label, lo, hi in bins:
    n = sum(1 for v in plddt.values() if lo <= v < hi)
    print(f'  {label:18s} {n:5d}  ({100 * n / len(plddt):.1f}%)')

m_ca = {r.seqid.num: r['CA'][0].pos for r in model if r.find_atom('CA', '*')}
e_ca = {r.seqid.num: r['CA'][0].pos for r in exp.get_polymer() if r.find_atom('CA', '*')}
common = sorted(set(m_ca) & set(e_ca))
sup = gemmi.superpose_positions([e_ca[n] for n in common], [m_ca[n] for n in common])
print(f'common residues: {len(common)}  CA RMSD after superposition: {sup.rmsd:.2f} A')

if chosen:
    print('residue  pLDDT  CA distance after superposition (A)')
    for n in chosen:
        if n in m_ca and n in e_ca:
            moved = gemmi.Position(sup.transform.apply(m_ca[n]))
            print(f'{n:7d}  {plddt[n]:5.1f}  {moved.dist(e_ca[n]):.2f}')
        else:
            print(f'{n:7d}  missing in model or experiment')
