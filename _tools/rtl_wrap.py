#!/usr/bin/env python3
"""Make course markdown render right-to-left on GitHub (STYLE_GUIDE §7).

Wraps the whole file in <div dir="rtl"> and every fenced code block in
<div dir="ltr">, keeping the fence's indentation (so code inside lists works).
Idempotent: running it twice gives the same file.
Usage: python3 _tools/rtl_wrap.py FILE.md [FILE.md ...]
"""
import re
import sys

OPEN, CLOSE = '<div dir="rtl">', '</div>'
FENCE = re.compile(r'^(\s*)(`{3,}|~{3,})')


def unwrap(lines):
    """Remove wrappers added by an earlier run."""
    out, i = [], 0
    while i < len(lines):
        s = lines[i].strip()
        if s in (OPEN, '<div dir="ltr">', '</div>'):
            i += 1
            if i < len(lines) and lines[i].strip() == '' and out and out[-1].strip() == '':
                i += 1  # drop the blank line we added after the tag
            continue
        out.append(lines[i])
        i += 1
    return out


def wrap(text):
    lines = unwrap(text.rstrip('\n').split('\n'))
    while lines and lines[0].strip() == '':
        lines.pop(0)
    out, fence = [OPEN, ''], None
    for line in lines:
        m = FENCE.match(line)
        if fence is None and m:
            ind, fence = m.group(1), m.group(2)[0] * 3
            if out[-1].strip():
                out.append('')
            out += [ind + '<div dir="ltr">', '', line]
            continue
        out.append(line)
        if fence and line.strip().startswith(fence) and line.strip().strip(fence[0]) == '' and not m_open(line, out):
            ind = re.match(r'^(\s*)', line).group(1)
            out += ['', ind + '</div>', '']
            fence = None
    while out and out[-1].strip() == '':
        out.pop()
    out += ['', CLOSE, '']
    # collapse triple blank lines
    res = re.sub(r'\n{3,}', '\n\n', '\n'.join(out))
    return res


def m_open(line, out):
    """True if this fence line is the opening fence we just appended."""
    return len(out) >= 2 and out[-2].strip() == '' and out[-3].strip() == '<div dir="ltr">' if len(out) >= 3 else False


for path in sys.argv[1:]:
    src = open(path, encoding='utf-8').read()
    new = wrap(src)
    if new != src:
        open(path, 'w', encoding='utf-8').write(new)
        print('wrapped', path)
