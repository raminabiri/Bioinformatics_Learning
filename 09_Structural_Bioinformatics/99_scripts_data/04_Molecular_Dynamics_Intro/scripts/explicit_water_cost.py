#!/usr/bin/env python3
"""How much does explicit water cost? (part 09, module 04)

Builds the same protein in a periodic water box (TIP3P + 0.15 M ions), reports how many atoms
that adds, then runs 1 ps to measure the speed and extrapolate to 100 ps.
Compare the numbers with the implicit-solvent run of md_run.py.

Usage: python3 explicit_water_cost.py PROTEIN.pdb [PADDING_NM]
"""
import sys
import time
from openmm import LangevinMiddleIntegrator, Platform
from openmm.app import ForceField, HBonds, Modeller, PDBFile, PME, Simulation
from openmm.unit import molar, nanometer, kelvin, picosecond, picoseconds

pdb_path = sys.argv[1]
padding = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0

pdb = PDBFile(pdb_path)
ff = ForceField('amber14-all.xml', 'amber14/tip3p.xml')
mod = Modeller(pdb.topology, pdb.positions)
mod.addHydrogens(ff)
print('protein atoms:', mod.topology.getNumAtoms())

mod.addSolvent(ff, padding=padding * nanometer, ionicStrength=0.15 * molar)
waters = len([r for r in mod.topology.residues() if r.name == 'HOH'])
box = mod.topology.getUnitCellDimensions().value_in_unit(nanometer)
print(f'solvated atoms: {mod.topology.getNumAtoms()}  waters: {waters}  '
      f'box (nm): {[round(x, 2) for x in box]}')

system = ff.createSystem(mod.topology, nonbondedMethod=PME,
                         nonbondedCutoff=1.0 * nanometer, constraints=HBonds)
integrator = LangevinMiddleIntegrator(300 * kelvin, 1 / picosecond, 0.002 * picoseconds)
sim = Simulation(mod.topology, system, integrator, Platform.getPlatformByName('CPU'))
sim.context.setPositions(mod.positions)
sim.minimizeEnergy(maxIterations=200)

t0 = time.time()
sim.step(500)                      # 1 ps
dt = time.time() - t0
print(f'1 ps of explicit-solvent MD: {dt:.0f} s  ->  100 ps would take about {dt * 100 / 60:.0f} min')
