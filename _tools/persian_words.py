#!/usr/bin/env python3
"""Apply the safe word replacements of STYLE_GUIDE §8 and list the ones that need a human.

Only replaces outside code (fenced blocks and `inline code`).
Usage: python3 _tools/persian_words.py FILE.md [...]
"""
import re
import sys

ZW = '‌'
SAFE = [
    (r'مثلاً|مثلا', 'برای نمونه'),
    (r'معمولاً|معمولا', 'در بسیاری از موارد'),
    (r'علناً|علنا', 'آشکارا'),
    (r'(?<![\w‌])مختلف(?![\w])', 'گوناگون'),
    (r'(?<![\w‌])سؤال|(?<![\w‌])سوال', 'پرسش'),
    (r'(?<![\w‌])جواب', 'پاسخ'),
    (r'(?<![\w‌])فقط(?![\w])', 'تنها'),
    (r'(?<![\w‌])مثل(?![\w‌])', 'مانند'),
    (r'دستور[ \u200c]?العمل\u200c?ها', 'روش‌های کار'),
    (r'دستور[ \u200c]?العمل', 'روش کار'),
]
MANUAL = r'مثال|استفاده|حتماً|حتما|عملیات|عملی|عملاً|(?<![\w‌])عمل(?![\w])|تقریباً'
PROTECT = re.compile(r'(```.*?```|~~~.*?~~~|`[^`\n]*`|https?://\S+)', re.S)

for path in sys.argv[1:]:
    src = open(path, encoding='utf-8').read()
    parts = PROTECT.split(src)
    for i in range(0, len(parts), 2):  # even indexes = prose
        for pat, rep in SAFE:
            parts[i] = re.sub(pat, rep, parts[i])
    new = ''.join(parts)
    if new != src:
        open(path, 'w', encoding='utf-8').write(new)
    prose = PROTECT.sub('', new)
    for n, line in enumerate(prose.split('\n'), 1):
        for m in re.finditer(MANUAL, line):
            print(f'{path}: manual: …{line[max(0, m.start()-25):m.end()+25]}…')
