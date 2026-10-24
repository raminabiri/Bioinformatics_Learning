# Presence/absence heatmap of resistance (core) and virulence genes (part 08, module 02).
# Input : one AMRFinderPlus table per isolate, run with --plus --name (column 1 = isolate)
# Output: a PNG heatmap and a TSV matrix (1 = present, 0 = absent)
# Usage : Rscript amr_vir_heatmap.R OUT_PREFIX iso1.amr.tsv iso2.amr.tsv ...
suppressPackageStartupMessages(library(ggplot2))

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) stop("usage: Rscript amr_vir_heatmap.R OUT_PREFIX FILE.tsv ...")
prefix <- args[1]
files <- args[-1]

tabs <- lapply(files, read.delim, check.names = FALSE, quote = "")
amr <- do.call(rbind, tabs)

# keep clinical resistance (Scope core) and all virulence genes; drop K-12 background (plus AMR/STRESS)
keep <- amr[amr$Scope == "core" | amr$Type == "VIRULENCE", ]
keep <- keep[keep$Subtype != "STX_TYPE", ]          # the operon line repeats stxA2/stxB2
keep$group <- ifelse(keep$Type == "VIRULENCE", "virulence", "resistance")

isolates <- sapply(tabs, function(t) t$Name[1])
genes <- unique(keep[order(keep$group, keep$`Element symbol`), c("Element symbol", "group")])

grid <- expand.grid(isolate = isolates, gene = genes$`Element symbol`, stringsAsFactors = FALSE)
grid$present <- as.integer(paste(grid$isolate, grid$gene) %in%
                           paste(keep$Name, keep$`Element symbol`))
grid$group <- genes$group[match(grid$gene, genes$`Element symbol`)]
grid$gene <- factor(grid$gene, levels = rev(genes$`Element symbol`))

wide <- reshape(grid[, c("gene", "isolate", "present")], idvar = "gene",
                timevar = "isolate", direction = "wide")
names(wide) <- sub("present.", "", names(wide), fixed = TRUE)
write.table(wide, paste0(prefix, "_matrix.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)

p <- ggplot(grid, aes(x = isolate, y = gene, fill = factor(present))) +
  geom_tile(colour = "white") +
  facet_grid(group ~ ., scales = "free_y", space = "free_y") +
  scale_fill_manual(values = c("0" = "grey90", "1" = "firebrick"),
                    labels = c("absent", "present"), name = NULL) +
  labs(x = NULL, y = NULL, title = "Resistance (core) and virulence genes") +
  theme_minimal(base_size = 11)
ggsave(paste0(prefix, "_heatmap.png"), p, width = 5, height = 5, dpi = 150)
cat("isolates:", length(isolates), " genes:", nrow(genes), "\n")
cat("written:", paste0(prefix, "_matrix.tsv"), paste0(prefix, "_heatmap.png"), "\n")
