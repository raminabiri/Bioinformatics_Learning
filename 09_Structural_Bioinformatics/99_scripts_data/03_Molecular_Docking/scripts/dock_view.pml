# PyMOL script: crystal pose (yellow) vs best docked pose (cyan) of rifampicin (part 09, module 03).
# Run in the folder that holds 5UAC_rec_H.pdb, 5UAC_lig.mol and 5UAC_docked.pdbqt:
#   pymol -cq dock_view.pml
# Output: dock_view.png
load 5UAC_rec_H.pdb, rec
load 5UAC_lig.mol, xtal
load 5UAC_docked.pdbqt, docked
hide everything
bg_color white
set ray_opaque_background, 1

show cartoon, rec
color grey80, rec
set cartoon_transparency, 0.7
show sticks, xtal and not elem H
show sticks, docked and state 1 and not elem H
set all_states, 0
frame 1
color yellow, xtal and elem C
color cyan, docked and elem C
util.cnc("xtal or docked")

select rrdr, rec and resi 516+526+531
show sticks, rrdr and not name N+C+O and not elem H
color salmon, rrdr and elem C
util.cnc("rrdr")
set float_labels, on
set label_size, 22
label rrdr and name CA, "%s%s" % (resn, resi)

orient xtal
zoom xtal, 7
set ray_shadows, 0
png dock_view.png, width=1200, height=900, dpi=150, ray=1
