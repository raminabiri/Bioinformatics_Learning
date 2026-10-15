#!/usr/bin/env bash
# Verify every external link in the course markdown (STYLE_GUIDE §5).
#   YouTube → oEmbed (public & available), doi.org → Crossref, others → HTTP 200 (3 retries).
# Usage: bash _tools/check_links.sh [path]   (default: whole course). Prints only failures.
cd "$(dirname "$0")/.." || exit 1
grep -rhoE --include='*.md' --exclude='_old*' --exclude=PROGRESS.md 'https?://[^ )>`"]+' "${1:-.}" \
 | sed 's/[.,،]$//' | grep -v '\$(' | grep -vE '<your-|github.com/(user|username|your-username)/|eutils|portal/api/filereport|rest\.uniprot|alphafold.ebi.ac.uk/api/prediction|ftp\.sra|raw\.githubusercontent|opengene\.org|releases/download|fastqc_v[0-9]|Miniconda3-latest' \
 | sort -u | while read -r u; do
   for i in 1 2 3; do
     case "$u" in
       *youtube.com/watch*) c=$(curl -s -m 30 -o /dev/null -w '%{http_code}' "https://www.youtube.com/oembed?url=$u&format=json");;
       *doi.org/*)          c=$(curl -s -m 40 -o /dev/null -w '%{http_code}' "https://api.crossref.org/works/${u#*doi.org/}");;
       *)                   c=$(curl -sL -m 40 -o /dev/null -w '%{http_code}' -A 'Mozilla/5.0' "$u"); [ "$c" = 403 ] && c=$(curl -sL -m 40 -o /dev/null -w '%{http_code}' "$u");;
     esac
     [ "$c" = 200 ] && break; sleep 3
   done
   [ "$c" = 200 ] || echo "FAIL $c $u"
 done
echo "link check finished"
