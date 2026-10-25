#!/usr/bin/env python3
"""Split a protein-ligand crystal structure into receptor and ligand files (part 09, module 03).

Usage: python3 prep_complex.py STRUCTURE.cif[.gz] CHAIN LIGAND_NAME SMILES OUT_PREFIX
Writes:
  OUT_PREFIX_rec.pdb      protein atoms of CHAIN only (no ligand, no water, no ions)
  OUT_PREFIX_lig.mol      the ligand with correct bond orders (taken from SMILES) and hydrogens,
                          at its crystal position (this is the reference pose for redocking)
Prints the ligand centre (for the docking box) and its size.
Crystal structures have no bond orders and usually no hydrogens; RDKit copies the bond orders
from the SMILES template onto the crystal atoms, then adds hydrogens with coordinates.
"""
import sys
import gemmi
from rdkit import Chem
from rdkit.Chem import AllChem

path, chain_name, lig_name, smiles, prefix = sys.argv[1:6]

st = gemmi.read_structure(path)
st.remove_hydrogens()
model = st[0]

rec = gemmi.Structure()
rec.cell = st.cell
rec_model = gemmi.Model('1')
rec_chain = gemmi.Chain(chain_name)
lig = gemmi.Structure()
lig_model = gemmi.Model('1')
lig_chain = gemmi.Chain(chain_name)
for res in model[chain_name]:
    if res.name == lig_name and len(lig_chain) == 0:
        lig_chain.add_residue(res)
    elif res.het_flag != 'H':
        rec_chain.add_residue(res)
if len(lig_chain) == 0:
    sys.exit(f'{lig_name} not found in chain {chain_name}')
rec_model.add_chain(rec_chain)
rec.add_model(rec_model)
rec.setup_entities()
rec.write_pdb(f'{prefix}_rec.pdb')
lig_model.add_chain(lig_chain)
lig.add_model(lig_model)
lig.write_pdb(f'{prefix}_lig_noH.pdb')

template = Chem.MolFromSmiles(smiles)
xtal = Chem.MolFromPDBFile(f'{prefix}_lig_noH.pdb', removeHs=True)
mol = AllChem.AssignBondOrdersFromTemplate(template, xtal)
Chem.AssignStereochemistryFrom3D(mol)
same = Chem.MolToSmiles(mol) == Chem.MolToSmiles(template)
molH = Chem.AddHs(mol, addCoords=True)
Chem.MolToMolFile(molH, f'{prefix}_lig.mol')

pos = molH.GetConformer().GetPositions()
heavy = [p for p, a in zip(pos, molH.GetAtoms()) if a.GetAtomicNum() > 1]
centre = [sum(c) / len(heavy) for c in zip(*heavy)]
span = [max(c) - min(c) for c in zip(*heavy)]
print(f'receptor residues: {len(rec_chain)}  ligand heavy atoms: {mol.GetNumAtoms()}  with H: {molH.GetNumAtoms()}')
print(f'crystal stereochemistry matches SMILES: {same}')
print('ligand centre: {:.3f} {:.3f} {:.3f}'.format(*centre))
print('ligand size (A): {:.1f} {:.1f} {:.1f}'.format(*span))
print(f'written: {prefix}_rec.pdb {prefix}_lig.mol')
