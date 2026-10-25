import sys, numpy as np
from rdkit import Chem
ref_mol, pose_pdb = sys.argv[1], sys.argv[2]
def skeleton(m):
    q = Chem.RWMol(m)
    for b in q.GetBonds(): b.SetBondType(Chem.BondType.SINGLE); b.SetIsAromatic(False)
    for a in q.GetAtoms(): a.SetIsAromatic(False); a.SetFormalCharge(0); a.SetNoImplicit(True)
    return q
x = Chem.RemoveHs(Chem.MolFromMolFile(ref_mol))
d = Chem.MolFromPDBFile(pose_pdb, removeHs=True, sanitize=False, proximityBonding=True)
ms = skeleton(d).GetSubstructMatches(skeleton(x), uniquify=False, useChirality=False, maxMatches=1000)
X = x.GetConformer().GetPositions(); D = d.GetConformer().GetPositions()
print(round(min(np.sqrt(((X - D[list(m)])**2).sum(1).mean()) for m in ms), 2))
