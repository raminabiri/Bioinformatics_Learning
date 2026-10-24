# Neighbour-joining tree with bootstrap support from a DNA alignment (part 08, module 04).
# Usage : Rscript nj_tree.R ALIGNMENT.fasta OUTGROUP OUT_PREFIX [MODEL] [N_BOOT]
#         MODEL  = substitution model of ape::dist.dna, e.g. TN93 (default), K80, JC69, N (= SNP counts)
#         N_BOOT = number of bootstrap replicates (default 100)
# Output: OUT_PREFIX.nwk (rooted tree, bootstrap % as node labels) and OUT_PREFIX.png
suppressPackageStartupMessages(library(ape))

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 3) stop("usage: Rscript nj_tree.R ALIGNMENT.fasta OUTGROUP OUT_PREFIX [MODEL] [N_BOOT]")
aln_file <- args[1]
outgroup <- args[2]
prefix <- args[3]
model <- if (length(args) >= 4) args[4] else "TN93"
nboot <- if (length(args) >= 5) as.integer(args[5]) else 100

aln <- read.dna(aln_file, format = "fasta")
rownames(aln) <- sub(" .*", "", rownames(aln))          # keep the first word of each name
cat("sequences:", nrow(aln), " alignment length:", ncol(aln), "\n")

make_tree <- function(x) nj(dist.dna(x, model = model, pairwise.deletion = TRUE))
tree <- make_tree(aln)

set.seed(1)
boot <- boot.phylo(tree, aln, make_tree, B = nboot, quiet = TRUE)
tree$node.label <- round(100 * boot / nboot)

tree <- root(tree, outgroup = outgroup, resolve.root = TRUE, edgelabel = TRUE)
tree$node.label[tree$node.label %in% c("Root", NA)] <- ""   # the new root node has no support value
write.tree(tree, paste0(prefix, ".nwk"))

png(paste0(prefix, ".png"), width = 900, height = 650, res = 120)
plot(tree, cex = 0.8, no.margin = TRUE)
nodelabels(tree$node.label, frame = "none", adj = c(1.2, -0.4), cex = 0.6, col = "firebrick")
add.scale.bar(x = 0.6 * max(node.depth.edgelength(tree)), y = 1)
invisible(dev.off())
cat("model:", model, " bootstrap replicates:", nboot, "\n")
cat("written:", paste0(prefix, ".nwk"), paste0(prefix, ".png"), "\n")
