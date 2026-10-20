# run_deseq2.R: which genes change between two groups of RNA-seq samples? (DESeq2)
# Usage: Rscript run_deseq2.R counts.tsv samples.tsv WT deseq2
#   counts.tsv  : first column gene_id, then one column of read counts per sample
#   samples.tsv : columns sample and condition; sample names = column names of counts.tsv
#   WT          : the reference (control) group; log2FoldChange = other group vs this one
#   deseq2      : prefix of the output files
# Writes: <prefix>_results.tsv, <prefix>_MA.png, <prefix>_PCA.png

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 4) {
  cat("Usage: Rscript run_deseq2.R <counts.tsv> <samples.tsv> <reference_group> <out_prefix>\n")
  quit(status = 1)
}
counts_file <- args[1]
samples_file <- args[2]
reference <- args[3]
prefix <- args[4]

# ---- settings you may change ----
padj_cutoff <- 0.05   # false discovery rate for calling a gene "changed"
# ----------------------------------

suppressPackageStartupMessages({
  library(DESeq2)
  library(ggplot2)
})

counts <- read.delim(counts_file, row.names = 1, check.names = FALSE)
samples <- read.delim(samples_file)
if (!all(samples$sample %in% colnames(counts))) {
  cat("These samples are in", samples_file, "but not in", counts_file, ":",
      setdiff(samples$sample, colnames(counts)), "\n")
  quit(status = 1)
}
counts <- counts[, samples$sample]
samples$condition <- relevel(factor(samples$condition), ref = reference)
cat("genes:", nrow(counts), " samples:", ncol(counts), "\n")
print(table(samples$condition))

dds <- DESeqDataSetFromMatrix(countData = as.matrix(counts),
                              colData = samples, design = ~ condition)
dds <- DESeq(dds)
res <- results(dds, alpha = padj_cutoff)
summary(res)

out <- as.data.frame(res)
out <- cbind(gene_id = rownames(out), out)
out <- out[order(out$padj), ]
write.table(out, paste0(prefix, "_results.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)

png(paste0(prefix, "_MA.png"), width = 800, height = 600, res = 120)
plotMA(res, alpha = padj_cutoff, main = "DESeq2: MA plot")
invisible(dev.off())

vsd <- vst(dds, blind = TRUE)
p <- plotPCA(vsd, intgroup = "condition") + theme_bw()
ggsave(paste0(prefix, "_PCA.png"), p, width = 6, height = 4.5, dpi = 120)

cat("saved", paste0(prefix, c("_results.tsv", "_MA.png", "_PCA.png")), "\n")
