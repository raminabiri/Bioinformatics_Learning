# Outbreak tree from a core-genome alignment, with metadata (part 08, module 04).
# Steps: keep only variable sites (SNPs) -> pairwise SNP distance matrix -> NJ tree on SNP counts
#        -> 100 bootstrap replicates -> root on the outgroup -> ggtree plot with metadata columns.
# Usage : Rscript outbreak_tree.R CORE.aln METADATA.tsv OUTGROUP OUT_PREFIX
# Output: OUT_PREFIX_snps.fasta, OUT_PREFIX_snp_dist.tsv, OUT_PREFIX.nwk, OUT_PREFIX.png
suppressPackageStartupMessages({
  library(ape)
  library(ggplot2)
  library(ggtree)
})

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 4) stop("usage: Rscript outbreak_tree.R CORE.aln METADATA.tsv OUTGROUP OUT_PREFIX")
aln_file <- args[1]; meta_file <- args[2]; outgroup <- args[3]; prefix <- args[4]

aln <- read.dna(aln_file, format = "fasta")
snps <- aln[, seg.sites(aln)]
cat("isolates:", nrow(aln), " alignment length:", ncol(aln), " SNP sites:", ncol(snps), "\n")
write.dna(snps, paste0(prefix, "_snps.fasta"), format = "fasta", colsep = "")

d <- dist.dna(snps, model = "N")                       # N = number of differing sites
write.table(as.matrix(d), paste0(prefix, "_snp_dist.tsv"), sep = "\t", quote = FALSE, col.names = NA)

make_tree <- function(x) nj(dist.dna(x, model = "N"))
tree <- make_tree(snps)
set.seed(1)
boot <- boot.phylo(tree, snps, make_tree, B = 100, quiet = TRUE)
tree$node.label <- boot
tree <- root(tree, outgroup = outgroup, resolve.root = TRUE, edgelabel = TRUE)
tree$node.label[tree$node.label %in% c("Root", NA)] <- ""
write.tree(tree, paste0(prefix, ".nwk"))

meta <- read.delim(meta_file, stringsAsFactors = FALSE)
rownames(meta) <- meta$isolate
plot_tree <- drop.tip(tree, outgroup)                  # the 1500-SNP outgroup branch would squash the plot
p <- ggtree(plot_tree) %<+% meta +
  geom_tiplab(aes(colour = hospital, label = paste0(label, "  ", ST)), size = 3, offset = 5) +
  geom_nodelab(aes(label = label), size = 2.3, hjust = 1.3, vjust = -0.5, colour = "grey30") +
  geom_treescale(width = 100) +
  scale_colour_manual(values = c(H1 = "#1b9e77", H2 = "#d95f02", H3 = "#7570b3")) +
  theme(legend.position = "left")
heat <- meta[plot_tree$tip.label, c("blaKPC", "iuc")]
p <- suppressMessages(
  gheatmap(p, heat, offset = 230, width = 0.3, colnames_angle = 0, font.size = 3, colnames_position = "top") +
    scale_fill_manual(values = c(yes = "firebrick", no = "grey90"), name = "gene"))
ggsave(paste0(prefix, ".png"), p, width = 9, height = 6, dpi = 130)
cat("written:", paste0(prefix, c("_snps.fasta", "_snp_dist.tsv", ".nwk", ".png")), "\n")
