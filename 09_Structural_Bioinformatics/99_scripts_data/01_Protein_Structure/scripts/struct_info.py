#!/usr/bin/env python3
"""Summarise a structure file and list the residues around a ligand (part 09, module 01).

Usage: python3 struct_info.py STRUCTURE.cif[.gz] [LIGAND_NAME] [DISTANCE_A]
  - prints title-like facts (method, resolution), each chain with its length and first residue
  - lists every non-water ligand (het group) with its chain and residue number
  - with LIGAND_NAME: lists protein residues that have any atom within DISTANCE_A (default 4.0 A)
    of any atom of the first copy of that ligand
"""
import sys
import gemmi

path = sys.argv[1]
lig_name = sys.argv[2] if len(sys.argv) > 2 else None
cutoff = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0

st = gemmi.read_structure(path)
st.setup_entities()
model = st[0]
method = st.info['_exptl.method'] if '_exptl.method' in st.info else '?'
print(f'entry: {st.name}  method: {method}  resolution: {st.resolution} A  models: {len(st)}')

for ch in model:
    poly = ch.get_polymer()
    if len(poly):
        print(f'chain {ch.name}: {len(poly)} residues  first: {poly[0].name}{poly[0].seqid.num}')

ligands = [(ch.name, r.name, r.seqid.num, len(r)) for ch in model for r in ch
           if r.het_flag == 'H' and not r.is_water()]
print('ligands (chain, name, number, atoms):', ligands)

if lig_name:
    copies = [(ch, r) for ch in model for r in ch if r.name == lig_name]
    if not copies:
        sys.exit(f'ligand {lig_name} not found')
    lig_chain, lig = copies[0]
    ns = gemmi.NeighborSearch(model, st.cell, 6).populate()
    near = {}
    for atom in lig:
        for mark in ns.find_atoms(atom.pos, '\0', radius=cutoff):
            cra = mark.to_cra(model)
            if cra.residue.het_flag == 'H':
                continue
            key = (cra.chain.name, cra.residue.seqid.num, cra.residue.name)
            d = atom.pos.dist(cra.atom.pos)
            near[key] = min(d, near.get(key, 99))
    print(f'residues within {cutoff} A of {lig_name} (chain {lig_chain.name}):')
    for (c, n, name), d in sorted(near.items()):
        print(f'  {c} {name}{n}  closest {d:.1f} A')
