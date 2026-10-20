#!/usr/bin/env bash
# run_all.sh: run the R scripts of part 04 one after another, like a small pipeline.
# For every sample in ground_truth.tsv: composition table + bar chart (composition.R).
# Then: diversity of all samples (diversity.R). Every R run writes a log file.
# Usage: bash run_all.sh <ground_truth.tsv> <output_folder>
set -euo pipefail

if [ $# -ne 2 ]; then
    echo "Usage: bash run_all.sh <ground_truth.tsv> <output_folder>" >&2
    exit 1
fi
table=$(realpath "$1")
out=$2

# folder of this script -> the R scripts of modules 02 and 03 sit next to it
here=$(dirname "$(realpath "$0")")
R02=$here/../../02_Run_Rscript/scripts
R03=$here/../../03_Bioc_Examples/scripts

mkdir -p "$out/logs"
cd "$out"

# 1. record the R and package versions used for this run
Rscript "$here/../../01_Install_Packages/scripts/check_packages.R" ggplot2 vegan > versions.txt

# 2. one composition chart per sample
for sample in $(cut -f1 "$table" | tail -n +2 | sort -u); do
    echo "composition: $sample"
    Rscript --vanilla "$R02/composition.R" "$table" "$sample" "${sample}_composition.png" \
        > "logs/${sample}_composition.log" 2>&1
done

# 3. diversity of all samples together (genus level)
echo "diversity: all samples"
Rscript --vanilla "$R03/diversity.R" "$table" diversity genus > logs/diversity.log 2>&1

echo "done; outputs in $out"
