#!/usr/bin/env bash
# check.sh (part 06, module 03): self-check after run_profile.sh (confidence 0)
# Run inside the project folder (cd ~/meta); ground_truth_species.tsv must be there (lesson 1).
set -uo pipefail
S=$(dirname "$0")
ok=0
bad=0
pass() { echo "  [OK]   $1"; ok=$((ok + 1)); }
fail() { echo "  [FAIL] $1"; bad=$((bad + 1)); }

[ -s profile/kraken2_practice_db/hash.k2d ] && pass "practice DB built" || fail "practice DB missing (build_practice_db.sh)"
for s in minigut minigut_sample2; do
  b=profile/bracken/${s}_c0.bracken
  if [ ! -s "$b" ]; then fail "$b missing"; continue; fi
  rec=$(python3 $S/evaluate_profile.py "$b" $s | tail -n 1 | sed -E 's/.*recall=([0-9.]+).*/\1/')
  awk -v r="$rec" 'BEGIN {exit !(r >= 0.95)}' && pass "$s: recall $rec" || fail "$s: recall $rec (< 0.95)"
done
if grep -q 'Candida' ground_truth_species.tsv && ! grep -q 'Candida' profile/bracken/minigut_sample2_c0.bracken; then
  pass "Candida (not in the DB) is absent from the profile, as expected"
else
  fail "unexpected Candida handling"
fi
echo "Result: $ok passed, $bad failed"
[ $bad -eq 0 ]
