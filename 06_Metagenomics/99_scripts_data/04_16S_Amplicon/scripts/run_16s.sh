#!/usr/bin/env bash
# run_16s.sh (part 06, module 04): 16S V4 amplicon analysis with QIIME 2 (Atacama soils, 1% subsample).
# Run inside the project folder:  cd ~/amplicon && bash <this script>
# Needs: data/download.sh, then scripts/train_classifier.sh (once).
# Outputs: the current folder (*.qza artifacts, *.qzv visualizations, exports/ with plain tables)
set -euo pipefail
THREADS=${THREADS:-4}
DEPTH=${DEPTH:-150}                 # rarefaction depth (lesson 2, section 4.2)
D=data
M=$D/sample_metadata.tsv
CLF=$D/db/silva-138-99-515-806-genus-nb.qza
OUT=.
export UNIFRAC_USE_GPU=N            # the unifrac binary is GPU-built; without a GPU it aborts
[ -s $D/raw/forward.fastq.gz ] || { echo "Run inside ~/amplicon (and run data/download.sh first)"; exit 1; }
[ -s $CLF ] || { echo "Classifier missing: run scripts/train_classifier.sh first"; exit 1; }
mkdir -p $OUT/emp $OUT/exports
qiime --version | head -1

echo "== 1. Import (EMP paired-end: forward, reverse, barcodes)"
cp $D/raw/forward.fastq.gz $D/raw/reverse.fastq.gz $D/raw/barcodes.fastq.gz $OUT/emp/
qiime tools import --type EMPPairedEndSequences --input-path $OUT/emp --output-path $OUT/emp-paired-end-sequences.qza

echo "== 2. Demultiplex (Golay barcodes; the mapping file lists them reverse-complemented)"
qiime demux emp-paired --i-seqs $OUT/emp-paired-end-sequences.qza \
  --m-barcodes-file $M --m-barcodes-column barcode-sequence --p-rev-comp-mapping-barcodes \
  --o-per-sample-sequences $OUT/demux.qza --o-error-correction-details $OUT/demux-details.qza
qiime demux summarize --i-data $OUT/demux.qza --o-visualization $OUT/demux.qzv

echo "== 3. DADA2: trim 13 nt from 5' ends, truncate both reads at 150"
qiime dada2 denoise-paired --i-demultiplexed-seqs $OUT/demux.qza \
  --p-trim-left-f 13 --p-trim-left-r 13 --p-trunc-len-f 150 --p-trunc-len-r 150 --p-n-threads "$THREADS" \
  --o-table $OUT/table.qza --o-representative-sequences $OUT/rep-seqs.qza \
  --o-denoising-stats $OUT/denoising-stats.qza --o-base-transition-stats $OUT/base-transition-stats.qza
qiime metadata tabulate --m-input-file $OUT/denoising-stats.qza --o-visualization $OUT/denoising-stats.qzv
qiime feature-table summarize --i-table $OUT/table.qza --m-metadata-file $M \
  --o-feature-frequencies $OUT/feature-frequencies.qza --o-sample-frequencies $OUT/sample-frequencies.qza \
  --o-summary $OUT/table.qzv

echo "== 4. Taxonomy (Naive Bayes, SILVA 138 V4, genus level) + bar plot"
qiime feature-classifier classify-sklearn --i-classifier $CLF --i-reads $OUT/rep-seqs.qza \
  --p-n-jobs 1 --o-classification $OUT/taxonomy.qza
qiime taxa barplot --i-table $OUT/table.qza --i-taxonomy $OUT/taxonomy.qza --m-metadata-file $M \
  --o-visualization $OUT/taxa-bar-plots.qzv

echo "== 5. Phylogeny (MAFFT + FastTree, midpoint root)"
qiime phylogeny align-to-tree-mafft-fasttree --i-sequences $OUT/rep-seqs.qza --p-n-threads "$THREADS" \
  --o-alignment $OUT/aligned-rep-seqs.qza --o-masked-alignment $OUT/masked-aligned-rep-seqs.qza \
  --o-tree $OUT/unrooted-tree.qza --o-rooted-tree $OUT/rooted-tree.qza

echo "== 6. Diversity at depth $DEPTH (seed 42 so rarefaction is reproducible)"
rm -rf $OUT/core-metrics-results
qiime diversity core-metrics-phylogenetic --i-phylogeny $OUT/rooted-tree.qza --i-table $OUT/table.qza \
  --p-sampling-depth "$DEPTH" --p-random-seed 42 --m-metadata-file $M --p-n-jobs-or-threads "$THREADS" \
  --output-dir $OUT/core-metrics-results
C=$OUT/core-metrics-results
for a in faith_pd shannon observed_features; do
  qiime diversity alpha-group-significance --i-alpha-diversity $C/${a}_vector.qza --m-metadata-file $M \
    --o-visualization $C/${a}-group-significance.qzv
done
qiime diversity alpha-correlation --i-alpha-diversity $C/faith_pd_vector.qza --m-metadata-file $M \
  --o-visualization $C/faith-pd-correlation.qzv
for col in vegetation transect-name; do
  qiime diversity beta-group-significance --i-distance-matrix $C/unweighted_unifrac_distance_matrix.qza \
    --m-metadata-file $M --m-metadata-column $col --p-pairwise \
    --o-visualization $C/unweighted-unifrac-$col-significance.qzv
done
qiime diversity beta-group-significance --i-distance-matrix $C/unweighted_unifrac_distance_matrix.qza \
  --m-metadata-file $M --m-metadata-column vegetation --p-method permdisp \
  --o-visualization $C/unweighted-unifrac-vegetation-permdisp.qzv
qiime diversity adonis --i-distance-matrix $C/unweighted_unifrac_distance_matrix.qza --m-metadata-file $M \
  --p-formula "elevation+vegetation" --o-visualization $C/unweighted-unifrac-adonis.qzv

echo "== 7. Export plain tables for the exercises (exports/)"
E=$OUT/exports
qiime tools export --input-path $OUT/denoising-stats.qza --output-path $E/stats >/dev/null
qiime tools export --input-path $OUT/taxonomy.qza --output-path $E/taxonomy >/dev/null
qiime tools export --input-path $OUT/rep-seqs.qza --output-path $E/rep-seqs >/dev/null
qiime tools export --input-path $OUT/table.qza --output-path $E/table >/dev/null
biom convert -i $E/table/feature-table.biom -o $E/table/feature-table.tsv --to-tsv
qiime tools export --input-path $C/unweighted-unifrac-adonis.qzv --output-path $E/adonis >/dev/null
echo "Done. View any .qzv at https://view.qiime2.org (drag and drop) or: qiime tools view <file.qzv>"
