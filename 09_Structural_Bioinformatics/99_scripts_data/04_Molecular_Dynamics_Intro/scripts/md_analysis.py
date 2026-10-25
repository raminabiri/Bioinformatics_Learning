#!/usr/bin/env python3
"""Analyse a short MD trajectory with mdtraj (part 09, module 04).

Usage: python3 md_analysis.py START.pdb TRAJ.dcd LOG.csv OUT_PREFIX
Computes, for the C-alpha atoms:
  RMSD to the start structure (after superposition) per frame, RMSF per residue over the run,
  radius of gyration per frame; and reads temperature/energy from the OpenMM log.
Prints a short summary and writes OUT_PREFIX_analysis.png (4 panels) and OUT_PREFIX_rmsf.tsv.
"""
import csv
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mdtraj as md
import numpy as np

start_pdb, dcd, log_csv, prefix = sys.argv[1:5]
ref = md.load(start_pdb)
traj = md.load(dcd, top=start_pdb)
ca = traj.topology.select('name CA')
time_ps = np.arange(1, traj.n_frames + 1) * 1.0          # one frame per ps (md_run.py)

rmsd = md.rmsd(traj, ref, atom_indices=ca) * 10           # nm -> A
traj.superpose(ref, atom_indices=ca)
xyz = traj.xyz[:, ca, :] * 10
rmsf = np.sqrt(((xyz - xyz.mean(axis=0)) ** 2).sum(axis=2).mean(axis=0))
rg = md.compute_rg(traj.atom_slice(ca)) * 10

rows = list(csv.DictReader(open(log_csv)))
temp = np.array([float(r['Temperature (K)']) for r in rows])
epot = np.array([float(r['Potential Energy (kJ/mole)']) for r in rows])

residues = [traj.topology.atom(i).residue for i in ca]
with open(f'{prefix}_rmsf.tsv', 'w') as out:
    out.write('residue\tRMSF_A\n')
    for r, v in zip(residues, rmsf):
        out.write(f'{r.name}{r.resSeq}\t{v:.2f}\n')

half = traj.n_frames // 2
print(f'frames: {traj.n_frames}  C-alpha atoms: {len(ca)}')
print(f'temperature: mean {temp.mean():.1f} K (sd {temp.std():.1f})')
print(f'RMSD to start: mean of 2nd half {rmsd[half:].mean():.2f} A, max {rmsd.max():.2f} A')
print(f'radius of gyration: mean {rg.mean():.2f} A (sd {rg.std():.2f})')
top = np.argsort(rmsf)[::-1][:3]
print('most mobile residues (RMSF): ' + ', '.join(f'{residues[i].name}{residues[i].resSeq} {rmsf[i]:.2f} A' for i in top))

fig, ax = plt.subplots(2, 2, figsize=(10, 7))
ax[0, 0].plot(time_ps, rmsd); ax[0, 0].set(xlabel='time (ps)', ylabel='C-alpha RMSD (A)', title='RMSD to start')
ax[0, 1].bar([f'{r.resSeq}' for r in residues], rmsf); ax[0, 1].set(xlabel='residue', ylabel='RMSF (A)', title='RMSF per residue')
ax[0, 1].tick_params(axis='x', labelsize=7)
ax[1, 0].plot(time_ps, rg); ax[1, 0].set(xlabel='time (ps)', ylabel='Rg (A)', title='Radius of gyration')
ax[1, 1].plot(time_ps[:len(temp)], temp); ax[1, 1].axhline(300, color='grey', ls='--')
ax[1, 1].set(xlabel='time (ps)', ylabel='temperature (K)', title='Temperature')
fig.tight_layout()
fig.savefig(f'{prefix}_analysis.png', dpi=120)
print(f'written: {prefix}_analysis.png {prefix}_rmsf.tsv')
