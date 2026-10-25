# PyMOL script: rifampicin pocket of E. coli RNA polymerase (part 09, module 01).
# Run in the folder that holds 5UAC.cif.gz:   pymol -cq rif_pocket.pml
# Output: rif_pocket.png
load 5UAC.cif.gz, wt
remove solvent
hide everything
bg_color white
set ray_opaque_background, 1

# beta subunit (chain C) as cartoon, rifampicin as sticks
show cartoon, wt and chain C
color grey80, wt and chain C
set cartoon_transparency, 0.6
select rif, wt and resn RFP
show sticks, rif
color yellow, rif and elem C

# the three resistance positions of module 08/01 (E. coli numbering)
select rrdr, wt and chain C and resi 516+526+531
show sticks, rrdr and not name N+C+O
color salmon, rrdr and elem C
set label_size, 22
label rrdr and name CA, "%s%s" % (resn, resi)
set label_color, black
set float_labels, on
set label_position, (0, 2, 2)

# residues within 4 A of rifampicin
select pocket, byres (wt and chain C and polymer) within 4 of rif
show lines, pocket and not rrdr
util.cnc("rif or rrdr or pocket")   # oxygen red, nitrogen blue (rifampicin is in chain C too)

orient rif
zoom rif, 9
set ray_shadows, 0
png rif_pocket.png, width=1200, height=900, dpi=150, ray=1
