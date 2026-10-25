#!/usr/bin/env python3
"""Drug-likeness and similarity of small molecules with RDKit (part 09, module 02).

Usage: python3 mol_props.py COMPOUNDS.csv REFERENCE_NAME [OUT.sdf]
  COMPOUNDS.csv  columns name,CID,SMILES,... (as written by the PubChem step of the lesson)
  REFERENCE_NAME the compound that the Tanimoto similarity is measured against
  OUT.sdf        optional: one 3D conformer per compound (ETKDG + MMFF), for docking later
Prints one row per compound: MW, cLogP, H-bond donors/acceptors, rotatable bonds, TPSA,
number of Lipinski rule-of-five violations, and Tanimoto similarity (Morgan radius 2, 2048 bits).
"""
import csv
import sys
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem, Crippen, Descriptors, Lipinski, rdMolDescriptors

csv_path, ref_name = sys.argv[1], sys.argv[2]
out_sdf = sys.argv[3] if len(sys.argv) > 3 else None

rows = list(csv.DictReader(open(csv_path)))
mols = {r['name']: Chem.MolFromSmiles(r['SMILES']) for r in rows}
fpgen = AllChem.GetMorganGenerator(radius=2, fpSize=2048)
fps = {n: fpgen.GetFingerprint(m) for n, m in mols.items()}

print('name\tMW\tcLogP\tHBD\tHBA\tRotB\tTPSA\tRo5_violations\tTanimoto_to_' + ref_name.replace(' ', '_'))
for name, m in mols.items():
    mw = Descriptors.MolWt(m)
    logp = Crippen.MolLogP(m)
    hbd = Lipinski.NumHDonors(m)
    hba = Lipinski.NumHAcceptors(m)
    rot = rdMolDescriptors.CalcNumRotatableBonds(m)
    tpsa = rdMolDescriptors.CalcTPSA(m)
    viol = sum([mw > 500, logp > 5, hbd > 5, hba > 10])
    sim = DataStructs.TanimotoSimilarity(fps[ref_name], fps[name])
    print(f'{name}\t{mw:.1f}\t{logp:.2f}\t{hbd}\t{hba}\t{rot}\t{tpsa:.1f}\t{viol}\t{sim:.2f}')

if out_sdf:
    w = Chem.SDWriter(out_sdf)
    for name, m in mols.items():
        mh = Chem.AddHs(m)
        if AllChem.EmbedMolecule(mh, randomSeed=42) == 0:
            AllChem.MMFFOptimizeMolecule(mh, maxIters=2000)
            mh.SetProp('_Name', name)
            w.write(mh)
        else:
            print('embedding failed:', name, file=sys.stderr)
    w.close()
