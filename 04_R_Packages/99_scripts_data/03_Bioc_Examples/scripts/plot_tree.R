# plot_tree.R: draw a phylogenetic tree from a Newick file (ggtree)
# Usage: Rscript plot_tree.R woodmouse.nwk woodmouse_tree.png [rectangular|circular]

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  cat("Usage: Rscript plot_tree.R <tree.nwk> <output.png> [rectangular|circular]\n")
  quit(status = 1)
}
tree_file <- args[1]
png_file <- args[2]
layout <- if (length(args) >= 3) args[3] else "rectangular"

suppressPackageStartupMessages({
  library(ggtree)
  library(ggplot2)
})

tree <- read.tree(tree_file)
cat("tips (leaves):", length(tree$tip.label), "\n")
cat("first tips:", head(tree$tip.label, 5), "\n")

p <- ggtree(tree, layout = layout) +
  geom_tiplab(size = 3) +
  geom_treescale()
if (layout == "rectangular") p <- p + xlim(0, max(ape::node.depth.edgelength(tree)) * 1.3)
ggsave(png_file, p, width = 6, height = 6, dpi = 120)
cat("saved", png_file, "\n")
