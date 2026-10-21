#!/usr/bin/env bash
# build_practice_db.sh (part 06, module 03): build the PRACTICE Kraken2 + Bracken database.
#   45 bacterial/archaeal genomes listed in ../data/practice_db_genomes.tsv:
#     - 21 species present in the samples, but a DIFFERENT strain from the one the reads were simulated from
#     - 24 closely related "decoy" species (for example Shigella next to E. coli)
#   Candida albicans (present in minigut_sample2) is deliberately NOT included.
# !! FOR PRACTICE ONLY: real analyses need a full standard database (see the lesson). !!
# Download: about 48 MB of genomes + 80 MB of NCBI taxonomy.
# Run inside the project folder (cd ~/meta). Requires: datasets, kraken2, bracken (envs/metagenomics.yml).
# Output: profile/kraken2_practice_db/
set -euo pipefail
LIST="$(dirname "$0")/../data/practice_db_genomes.tsv"
B=profile/db_build
DB=profile/kraken2_practice_db
THREADS=${THREADS:-4}
mkdir -p $B/fna $B/taxonomy

echo "== 1. genomes, one by one (the NCBI API is unreliable for large batches)"
tail -n +2 "$LIST" | cut -f 3 | while read -r acc; do
  [ -s $B/fna/$acc.zip ] && continue
  for try in 1 2 3; do
    datasets download genome accession "$acc" --include genome --no-progressbar \
      --filename $B/fna/$acc.zip > /dev/null 2>&1 && break
    sleep 3
  done
done

echo "== 2. NCBI taxonomy (nodes.dmp, names.dmp)"
if [ ! -s $B/taxonomy/nodes.dmp ]; then
  curl -sL --retry 5 -o $B/taxonomy/taxdump.tar.gz https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
  tar -xzf $B/taxonomy/taxdump.tar.gz -C $B/taxonomy nodes.dmp names.dmp merged.dmp delnodes.dmp
fi

echo "== 3. one FASTA library; every header gets the taxid: >kraken:taxid|<taxid>|<old header>"
rm -f $B/library.fa
tail -n +2 "$LIST" | cut -f 3,6 | while read -r acc taxid; do
  unzip -p $B/fna/$acc.zip 'ncbi_dataset/data/*/*.fna' \
    | awk -v t="$taxid" '/^>/ {sub(/^>/, ">kraken:taxid|" t "|")} {print}' >> $B/library.fa
done

echo "== 4. Kraken2 database (no low-complexity masking: not needed for this practice DB)"
rm -rf $DB
mkdir -p $DB/taxonomy
cp $B/taxonomy/*.dmp $DB/taxonomy/
kraken2-build --add-to-library $B/library.fa --db $DB --no-masking
kraken2-build --build --db $DB --threads "$THREADS"

echo "== 5. Bracken models for the two read lengths of the course data"
for L in 125 150; do
  bracken-build -d $DB -t "$THREADS" -k 35 -l $L > $B/bracken_build_$L.log 2>&1
done
du -sh $DB/hash.k2d
echo "Practice database ready: $DB"
