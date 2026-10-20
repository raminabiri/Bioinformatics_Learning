# check_packages.R: is each R package installed? If yes, which version?
# Usage: Rscript check_packages.R DESeq2 vegan ggtree
# Without arguments it checks the packages used in part 04.

pkgs <- commandArgs(trailingOnly = TRUE)
if (length(pkgs) == 0) {
  pkgs <- c("BiocManager", "ggplot2", "vegan", "ape", "DESeq2", "ggtree")
}

cat("R:", R.version.string, "\n")
for (p in pkgs) {
  if (requireNamespace(p, quietly = TRUE)) {
    cat(sprintf("%-12s %s\n", p, as.character(packageVersion(p))))
  } else {
    cat(sprintf("%-12s NOT installed\n", p))
  }
}
