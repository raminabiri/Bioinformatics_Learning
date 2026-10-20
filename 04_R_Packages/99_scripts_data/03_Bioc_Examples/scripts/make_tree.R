# make_tree.R: build a small practice tree (Newick file) from a DNA alignment that ships with ape
# Data: 'woodmouse' = 15 mitochondrial cytochrome b sequences of wood mice (Apodemus sylvaticus).
# Method: distances between sequences (dist.dna, K80 model) -> neighbour-joining tree (nj).
# (How trees are really built is taught in part 08; here we only need a tree file to draw.)
# Usage: Rscript make_tree.R woodmouse.nwk

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) {
  cat("Usage: Rscript make_tree.R <output.nwk>\n")
  quit(status = 1)
}
suppressPackageStartupMessages(library(ape))

data(woodmouse)
cat("alignment:", nrow(woodmouse), "sequences x", ncol(woodmouse), "bp\n")
tree <- nj(dist.dna(woodmouse, model = "K80"))
tree <- root(tree, outgroup = "No305", resolve.root = TRUE)
tree$edge.length[tree$edge.length < 0] <- 0   # NJ can give tiny negative branches; set them to 0
write.tree(tree, args[1])
cat("saved", args[1], "\n")
