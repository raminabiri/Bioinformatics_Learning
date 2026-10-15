#!/usr/bin/env bash
# Search YouTube and print only videos that are currently public (checked via oEmbed).
# Usage: bash _tools/yt_search.sh "query" [n]      → id | channel | title
q=$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$1"); n=${2:-6}
curl -s -m 30 -H 'Accept-Language: en' "https://www.youtube.com/results?search_query=$q" \
 | grep -oE '"videoId":"[A-Za-z0-9_-]{11}"' | cut -d'"' -f4 | awk '!s[$0]++' | head -n "$n" \
 | while read -r id; do
     j=$(curl -s -m 15 "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=$id&format=json")
     [ -n "$j" ] && echo "$j" | jq -r --arg id "$id" '"\($id) | \(.author_name) | \(.title)"' 2>/dev/null
   done
