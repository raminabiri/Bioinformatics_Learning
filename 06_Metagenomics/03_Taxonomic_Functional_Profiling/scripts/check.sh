#!/usr/bin/env bash
# Self-check for module 03/03. Run from 06_Metagenomics/ after run_profile.sh (CONF=0).
set -uo pipefail
ok=0; bad=0; pass(){ echo "  [OK]   $1"; ok=$((ok+1)); }; fail(){ echo "  [FAIL] $1"; bad=$((bad+1)); }
[ -s work/03_profile/kraken2_practice_db/hash.k2d ] && pass "practice DB built" || fail "practice DB missing (build_practice_db.sh)"
for s in minigut minigut_sample2; do
  b=work/03_profile/bracken/${s}_c0.bracken
  [ -s "$b" ] || { fail "$b missing"; continue; }
  out=$(python3 03_Taxonomic_Functional_Profiling/scripts/evaluate_profile.py "$b" $s | tail -1)
  rec=$(echo "$out" | sed -E 's/.*recall=([0-9.]+).*/\1/')
  awk -v r=$rec 'BEGIN{exit !(r>=0.95)}' && pass "$s: recall $rec" || fail "$s: recall $rec (<0.95)"
done
grep -q 'Candida' data/ground_truth_species.tsv && ! grep -q 'Candida' work/03_profile/bracken/minigut_sample2_c0.bracken \
  && pass "Candida (not in DB) correctly absent from profile" || fail "unexpected Candida handling"
echo "Result: $ok passed, $bad failed"; [ $bad -eq 0 ]
