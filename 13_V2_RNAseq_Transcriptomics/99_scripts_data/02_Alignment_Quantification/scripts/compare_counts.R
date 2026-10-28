# Compare gene counts from Salmon (via tximport) and featureCounts with the known truth (part 13, module 02).
# Usage (in ~/rnaseq):   Rscript compare_counts.R salmon_isr counts/fc_s2.txt ref/tx2gene.tsv reads/truth_counts.tsv
# Works the same in R/RStudio on Windows (set the working directory to the rnaseq folder first).
# Writes gene_counts_salmon.tsv (rounded gene-level Salmon counts, input of module 13/03).
suppressMessages(library(tximport))

args <- commandArgs(trailingOnly = TRUE)
salmon_dir <- args[1]; fc_file <- args[2]; t2g_file <- args[3]; truth_file <- args[4]
samples <- c("ctrl_1", "ctrl_2", "ctrl_3", "dex_1", "dex_2", "dex_3")

# 1. Salmon transcript counts -> gene counts (sum over the transcripts of each gene)
t2g <- read.delim(t2g_file)[, c("transcript_id", "gene_name")]
files <- file.path(salmon_dir, samples, "quant.sf")
names(files) <- samples
tx <- tximport(files, type = "salmon", tx2gene = t2g, dropInfReps = TRUE)

# 2. featureCounts table: Geneid (row names), 5 annotation columns, then one column per BAM
fc <- read.delim(fc_file, comment.char = "#", row.names = 1)[, 6:11]
colnames(fc) <- samples

# 3. truth and comparison for one sample
truth <- read.delim(truth_file, row.names = 1)
genes <- rownames(truth)
out <- data.frame(truth = truth[genes, "ctrl_1"],
                  salmon = round(tx$counts[genes, "ctrl_1"], 1),
                  featureCounts = fc[genes, "ctrl_1"], row.names = genes)
print(out[order(out$truth), ])
cat("sum over all samples: truth", sum(truth[, samples]), " salmon", round(sum(tx$counts)),
    " featureCounts", sum(fc), "\n")
cat("largest |salmon - truth|:", max(abs(tx$counts[genes, samples] - as.matrix(truth[genes, samples]))), "\n")
cat("featureCounts / truth, all samples:", round(sum(fc) / sum(truth[, samples]), 4), "\n")

write.table(round(tx$counts[genes, samples]), "gene_counts_salmon.tsv", sep = "\t", quote = FALSE)
