#!/usr/bin/env python3
"""A short molecular dynamics run with OpenMM, in implicit solvent (part 09, module 04).

Usage: python3 md_run.py PROTEIN.pdb OUT_PREFIX [PICOSECONDS] [SEED]
Steps: take the first model -> add missing hydrogens -> force field Amber14 + implicit water (OBC2)
       -> energy minimisation -> 300 K Langevin dynamics, 2 fs time step, H-bonds constrained
       -> a frame and a line of energy/temperature every 1 ps.
Writes OUT_PREFIX_start.pdb (minimised structure), OUT_PREFIX.dcd (trajectory), OUT_PREFIX_log.csv.
Implicit solvent keeps the system tiny (a few hundred atoms) so it runs on a laptop CPU; real
studies use explicit water (thousands of water molecules), see the GROMACS section of the lesson.
"""
import sys
import time
from openmm import LangevinMiddleIntegrator, Platform
from openmm.app import (DCDReporter, ForceField, HBonds, Modeller, NoCutoff, PDBFile,
                        Simulation, StateDataReporter)
from openmm.unit import kelvin, picosecond, picoseconds

pdb_path, prefix = sys.argv[1], sys.argv[2]
ps = float(sys.argv[3]) if len(sys.argv) > 3 else 100
seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1

pdb = PDBFile(pdb_path)                       # NMR files: OpenMM reads the first model
ff = ForceField('amber14-all.xml', 'implicit/obc2.xml')
mod = Modeller(pdb.topology, pdb.positions)
mod.addHydrogens(ff)
system = ff.createSystem(mod.topology, nonbondedMethod=NoCutoff, constraints=HBonds)
integrator = LangevinMiddleIntegrator(300 * kelvin, 1 / picosecond, 0.002 * picoseconds)
integrator.setRandomNumberSeed(seed)
sim = Simulation(mod.topology, system, integrator, Platform.getPlatformByName('CPU'))
sim.context.setPositions(mod.positions)
print(f'atoms: {mod.topology.getNumAtoms()}  residues: {mod.topology.getNumResidues()}')

e0 = sim.context.getState(getEnergy=True).getPotentialEnergy()
sim.minimizeEnergy()
state = sim.context.getState(getEnergy=True, getPositions=True)
print(f'potential energy before / after minimisation: {e0._value:.1f} / {state.getPotentialEnergy()._value:.1f} kJ/mol')
PDBFile.writeFile(sim.topology, state.getPositions(), open(f'{prefix}_start.pdb', 'w'))

sim.context.setVelocitiesToTemperature(300 * kelvin, seed)
steps = int(ps / 0.002)
sim.reporters.append(DCDReporter(f'{prefix}.dcd', 500))
sim.reporters.append(StateDataReporter(f'{prefix}_log.csv', 500, step=True, time=True,
                                       potentialEnergy=True, temperature=True))
t0 = time.time()
sim.step(steps)
print(f'{ps:g} ps ({steps} steps) in {time.time() - t0:.0f} s')
print(f'written: {prefix}_start.pdb {prefix}.dcd {prefix}_log.csv')
