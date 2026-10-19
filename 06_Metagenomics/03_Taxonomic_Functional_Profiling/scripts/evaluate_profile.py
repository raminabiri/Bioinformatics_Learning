"""Compare a Bracken species-level profile with the known composition (ground truth).

Usage (from 06_Metagenomics/):
  python3 03_Taxonomic_Functional_Profiling/scripts/evaluate_profile.py \
      work/03_profile/bracken/minigut_c0.bracken minigut [--min-frac 0.001]

Prints per-species truth vs estimate, then precision, recall, F1 and Bray-Curtis
dissimilarity. Abundances are re-normalised over CLASSIFIED reads, because Bracken's
fraction_total_reads ignores unclassified reads.
"""
import argparse, csv

ap = argparse.ArgumentParser()
ap.add_argument('bracken'); ap.add_argument('sample')
ap.add_argument('--truth', default='data/ground_truth_species.tsv')
ap.add_argument('--min-frac', type=float, default=0.0,
                help='ignore predicted species below this relative abundance (noise filter)')
a = ap.parse_args()

truth = {r['species_taxid']: (r['species'], float(r['fraction']))
         for r in csv.DictReader(open(a.truth), delimiter='\t') if r['sample'] == a.sample}
pred_raw = {r['taxonomy_id']: (r['name'], int(r['new_est_reads']))
            for r in csv.DictReader(open(a.bracken), delimiter='\t')}
tot = sum(n for _, n in pred_raw.values())
pred = {t: (nm, n / tot) for t, (nm, n) in pred_raw.items() if n / tot >= a.min_frac}

tp = [t for t in pred if t in truth]
fp = [t for t in pred if t not in truth]
fn = [t for t in truth if t not in pred]
prec = len(tp) / len(pred) if pred else 0
rec = len(tp) / len(truth)
f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0
bc = 0.5 * sum(abs(truth.get(t, ('', 0))[1] - pred.get(t, ('', 0))[1]) for t in set(truth) | set(pred))

print(f"{'species':38s} {'truth':>7s} {'estimate':>9s}  status")
for t in sorted(set(truth) | set(pred), key=lambda t: -max(truth.get(t, ('', 0))[1], pred.get(t, ('', 0))[1])):
    name = truth.get(t, pred.get(t))[0]
    st = 'TP' if t in tp else ('FP' if t in fp else 'FN')
    print(f"{name[:38]:38s} {truth.get(t, ('', 0))[1]*100:6.2f}% {pred.get(t, ('', 0))[1]*100:8.2f}%  {st}")
print(f"\nspecies predicted={len(pred)}  TP={len(tp)}  FP={len(fp)}  FN={len(fn)}")
print(f"precision={prec:.3f}  recall={rec:.3f}  F1={f1:.3f}  Bray-Curtis={bc:.3f}")
