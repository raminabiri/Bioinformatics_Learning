# composition.R: percentage of reads from each genus in one sample, as a table and a bar chart
# Same job as composition.py (part 03, module 06), written in R with ggplot2.
# Usage: Rscript composition.R ground_truth.tsv minigut_sample2 composition_R.png

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) {
  cat("Usage: Rscript composition.R <ground_truth.tsv> <sample> <output.png>\n")
  quit(status = 1)
}
table_file <- args[1]
sample     <- args[2]
png_file   <- args[3]

suppressPackageStartupMessages(library(ggplot2))

gt <- read.delim(table_file)
gt <- gt[gt$sample == sample, ]
if (nrow(gt) == 0) {
  cat("No rows for sample:", sample, "\n")
  quit(status = 1)
}
gt$percent <- gt$read_pairs / sum(gt$read_pairs) * 100
gt$genus   <- sub(" .*", "", gt$organism)

by_genus <- aggregate(percent ~ genus, data = gt, FUN = sum)
by_genus <- by_genus[order(by_genus$percent), ]
by_genus$percent <- round(by_genus$percent, 2)

print(by_genus, row.names = FALSE)
out_tsv <- paste0(sample, "_genus_R.tsv")
write.table(by_genus, out_tsv, sep = "\t", quote = FALSE, row.names = FALSE)

by_genus$genus <- factor(by_genus$genus, levels = by_genus$genus)
p <- ggplot(by_genus, aes(x = percent, y = genus)) +
  geom_col(fill = "seagreen") +
  labs(x = "percent of read pairs", y = NULL,
       title = paste0(sample, ": composition by genus")) +
  theme_bw()
ggsave(png_file, p, width = 7, height = 6, dpi = 120)
cat("saved", out_tsv, "and", png_file, "\n")
