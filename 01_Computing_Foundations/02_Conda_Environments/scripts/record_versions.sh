#!/usr/bin/env bash
# Record versions of selected tools installed in a conda environment (for Methods / supplementary).
# Usage: bash record_versions.sh <env_name> [tool ...]   > versions.tsv
set -euo pipefail
ENV=${1:?Usage: record_versions.sh <env_name> [tool ...]}; shift
tools=("$@"); [ ${#tools[@]} -gt 0 ] || tools=(fastqc fastp multiqc bowtie2 samtools seqkit)
conda env list | awk '{print $1}' | grep -qx "$ENV" || { echo "Error: environment '$ENV' not found" >&2; exit 1; }
listing=$(conda list -n "$ENV")
printf "tool\tversion\tchannel\n"
for t in "${tools[@]}"; do
  echo "$listing" | awk -v t="$t" '$1==t {print $1"\t"$2"\t"($4==""?"conda-forge":$4); f=1} END{if(!f) print t"\tNOT_INSTALLED\t-"}'
done
printf "# environment=%s  conda=%s  date=%s\n" "$ENV" "$(conda --version | cut -d' ' -f2)" "$(date +%F)"
