#!/usr/bin/env bash
# Reproduce the Git session of the lesson in a throw-away folder (does not touch your global git config).
# Usage: bash git_demo.sh /path/to/ecoli_k12.gff [workdir]
# Commit dates/author are fixed so the commit hashes match the lesson exactly.
set -euo pipefail
GFF=$(realpath "${1:?Usage: git_demo.sh /path/to/ecoli_k12.gff [workdir]}")
W=${2:-$(mktemp -d)}; mkdir -p "$W"; cd "$W"
export GIT_AUTHOR_DATE="2026-10-13T10:00:00+0000" GIT_COMMITTER_DATE="2026-10-13T10:00:00+0000"

git init -q -b main ecoli_project && cd ecoli_project
git config user.name "Student"; git config user.email "student@example.org"   # local to this repo only
mkdir -p data/raw results scripts
printf 'data/raw/\n*.fastq.gz\nresults/\n' > .gitignore
printf '#!/usr/bin/env bash\nset -euo pipefail\nawk -F%s %s "$1" | wc -l\n' "'\\t'" "'\$3==\"gene\"'" > scripts/count_genes.sh
echo fake > data/raw/a.fastq.gz                      # a "large data file" that must NOT be committed
echo "== status before add";  git status --short
git add .gitignore scripts/count_genes.sh
git commit -q -m "Add gene counting script and .gitignore"

sed -i 's/wc -l/cut -f7 | sort | uniq -c/' scripts/count_genes.sh
echo "== diff";  git diff
git commit -qam "Count genes per strand"

git switch -q -c add-trna
sed -i 's/\$3=="gene"/$3=="gene" \&\& $9 ~ \/gene_biotype=tRNA\//' scripts/count_genes.sh
git commit -qam "Count only tRNA genes"
git switch -q main
sed -i 's/cut -f7/cut -f1,7/' scripts/count_genes.sh
git commit -qam "Also report chromosome"

echo "== merge (expect a CONFLICT)"; git merge add-trna || true
export GIT_AUTHOR_DATE="2026-10-13T11:00:00+0000" GIT_COMMITTER_DATE="2026-10-13T11:00:00+0000"
printf '#!/usr/bin/env bash\nset -euo pipefail\nawk -F%s %s "$1" | cut -f1,7 | sort | uniq -c\n' "'\\t'" "'\$3==\"gene\" && \$9 ~ /gene_biotype=tRNA/'" > scripts/count_genes.sh
git add scripts/count_genes.sh; git commit -q -m "Merge add-trna: tRNA genes per chromosome and strand"
echo "== history"; git log --oneline --graph --all
echo "== run current version";  bash scripts/count_genes.sh "$GFF"
git tag -a v1.0-thesis-ch2 -m "Version used for thesis chapter 2"
echo "== run an OLD version without changing the working tree"
bash <(git show HEAD~2:scripts/count_genes.sh) "$GFF"
echo "Demo repository: $W/ecoli_project"
