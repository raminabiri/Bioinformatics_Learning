# diversity.R: how diverse is each microbial sample, and how different are the samples? (vegan)
# Usage: Rscript diversity.R ground_truth.tsv diversity [organism|genus]
#   input: long table with columns sample, read_pairs, organism (one row per organism per sample)
#   organism (default): every organism name counts separately; genus: first word of the name
# Writes: <prefix>_alpha.tsv, <prefix>_bray.tsv, <prefix>_rarecurve.png

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  cat("Usage: Rscript diversity.R <table.tsv> <out_prefix> [organism|genus]\n")
  quit(status = 1)
}
table_file <- args[1]
prefix <- args[2]
level <- if (length(args) >= 3) args[3] else "organism"

suppressPackageStartupMessages(library(vegan))

long <- read.delim(table_file)
if (level == "genus") long$organism <- sub(" .*", "", long$organism)
# vegan wants a "community matrix": one row per sample, one column per organism
comm <- xtabs(read_pairs ~ sample + organism, data = long)
comm <- as.data.frame.matrix(comm)
cat("level:", level, " samples:", nrow(comm), " taxa:", ncol(comm), "\n")

alpha <- data.frame(
  sample   = rownames(comm),
  reads    = rowSums(comm),
  richness = specnumber(comm),
  shannon  = round(diversity(comm, index = "shannon"), 3),
  simpson  = round(diversity(comm, index = "simpson"), 3)
)
alpha$evenness <- round(alpha$shannon / log(alpha$richness), 3)
print(alpha, row.names = FALSE)
write.table(alpha, paste0(prefix, "_alpha.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)

bray <- vegdist(comm, method = "bray")
cat("\nBray-Curtis dissimilarity (0 = same, 1 = nothing shared):\n")
print(round(bray, 3))
write.table(round(as.matrix(bray), 3), paste0(prefix, "_bray.tsv"), sep = "\t", quote = FALSE)

png(paste0(prefix, "_rarecurve.png"), width = 800, height = 600, res = 120)
rarecurve(as.matrix(comm), step = 100, xlab = "read pairs sampled",
          ylab = "organisms found", label = TRUE)
invisible(dev.off())
cat("saved", paste0(prefix, c("_alpha.tsv", "_bray.tsv", "_rarecurve.png")), "\n")
