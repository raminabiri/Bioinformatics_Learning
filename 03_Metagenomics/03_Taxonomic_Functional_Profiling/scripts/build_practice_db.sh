#!/usr/bin/env bash
# Build the PRACTICE Kraken2 + Bracken database used in module 03/03.
#   45 bacterial/archaeal genomes listed in practice_db_genomes.tsv:
#     - 21 species present in the samples, but a DIFFERENT strain from the one the reads were simulated from
#     - 24 closely related "decoy" species (e.g. Shigella vs E. coli)
#   Candida albicans (present in minigut_sample2) is deliberately NOT included.
# !! FOR PRACTICE ONLY — real analyses need a full standard database (see lesson). !!
# Download: ~48 MB genomes + ~80 MB NCBI taxonomy (asks nothing; run only when you decide to).
# Run from 03_Metagenomics/.  Requires: datasets, jq, kraken2, bracken.
set -euo pipefail
LIST=03_Taxonomic_Functional_Profiling/practice_db_genomes.tsv
B=work/03_profile/db_build; DB=work/03_profile/kraken2_practice_db
THREADS=${THREADS:-8}
mkdir -p $B/fna $B/taxonomy

echo "== 1. genomes (one by one; the NCBI API is unreliable for large batches)"
tail -n +2 $LIST | cut -f3 | while read -r a; do
  [ -s $B/fna/$a.zip ] && unzip -tq $B/fna/$a.zip >/dev/null 2>&1 && continue
  for i in 1 2 3; do
    timeout 300 datasets download genome accession "$a" --include genome --no-progressbar --filename $B/fna/$a.zip >/dev/null 2>&1 \
      && unzip -tq $B/fna/$a.zip >/dev/null 2>&1 && break
    sleep 3
  done
done

echo "== 2. NCBI taxonomy (nodes/names)"
if [ ! -s $B/taxonomy/nodes.dmp ]; then
  curl -sL -C - --retry 5 -o $B/taxonomy/taxdump.tar.gz https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
  tar -xzf $B/taxonomy/taxdump.tar.gz -C $B/taxonomy nodes.dmp names.dmp merged.dmp delnodes.dmp
fi

echo "== 3. library with kraken:taxid headers"
rm -f $B/library.fa
for z in $B/fna/*.zip; do
  t=$(unzip -p $z ncbi_dataset/data/assembly_data_report.jsonl | jq -r '.organism.taxId')
  unzip -p $z 'ncbi_dataset/data/*/*.fna' | awk -v t="$t" '/^>/{sub(/^>/, ">kraken:taxid|" t "|")} {print}' >> $B/library.fa
done

echo "== 4. Kraken2 build (no low-complexity masking: dustmasker not required for this practice DB)"
rm -rf $DB; mkdir -p $DB/taxonomy; cp $B/taxonomy/*.dmp $DB/taxonomy/
kraken2-build --add-to-library $B/library.fa --db $DB --no-masking
kraken2-build --build --db $DB --threads "$THREADS"

echo "== 5. Bracken k-mer distributions for the two read lengths of the course data"
for L in 125 150; do bracken-build -d $DB -t "$THREADS" -k 35 -l $L > $B/bracken_build_$L.log 2>&1; done
du -sh $DB/hash.k2d; echo "Practice database ready: $DB"
