#!/usr/bin/env python3
"""Make course markdown render right-to-left on GitHub (STYLE_GUIDE §7).

Wraps the whole file in <div dir="rtl"> and every fenced code block in
<div dir="ltr">, keeping the fence's indentation (so code inside lists works).

GitHub also gives every paragraph, list item, heading and table cell dir="auto",
so a Persian line that starts with an English word is laid out left-to-right and
its Persian parts get scrambled. For such lines (Persian text, but the first
letter is Latin) an invisible RIGHT-TO-LEFT MARK (U+200F) is put at the start of
the text. Lines that are entirely English are left alone (they read fine LTR).
Idempotent: running it twice gives the same file.
Usage: python3 _tools/rtl_wrap.py FILE.md [FILE.md ...]
"""
import re
import sys
import unicodedata

OPEN, CLOSE = '<div dir="rtl">', '</div>'
FENCE = re.compile(r'^(\s*)(`{3,}|~{3,})')
RLM = '\u200f'
PREFIX = re.compile(r'^(\s*(?:>\s*)*(?:#{1,6}\s+|(?:[-*+]|\d+[.)])\s+)?(?:\[[ xX]\]\s+)?)')
SEP_ROW = re.compile(r'^\s*\|?[\s:|-]+\|?\s*$')


def is_persian(ch):
    o = ord(ch)
    return 0x0600 <= o <= 0x06FF or 0xFB50 <= o <= 0xFDFF or 0xFE70 <= o <= 0xFEFF


def needs_rlm(text):
    if text.lstrip().startswith(RLM):
        return False
    t = re.sub(r'\]\([^)]*\)', ']', text)          # link targets
    t = re.sub(r'<[^>]*>', ' ', t)                    # HTML tags
    t = re.sub(r'https?://\S+', ' ', t)              # bare URLs
    letters = [c for c in t if unicodedata.category(c).startswith('L')]
    if not letters or is_persian(letters[0]):
        return False
    return any(is_persian(c) for c in letters)


def split_cells(line):
    cells, cur, code = [], '', False
    i = 0
    while i < len(line):
        c = line[i]
        if c == '`':
            code = not code
        if c == '\\' and i + 1 < len(line) and line[i + 1] == '|':
            cur += c + '|'; i += 2; continue
        if c == '|' and not code:
            cells.append(cur); cur = ''
        else:
            cur += c
        i += 1
    cells.append(cur)
    return cells


def fix_line(line):
    if not line.strip():
        return line
    if line.lstrip().startswith('|'):
        if SEP_ROW.match(line):
            return line
        cells = split_cells(line)
        for k in range(1, len(cells) - 1):
            c = cells[k]
            if needs_rlm(c):
                lead = len(c) - len(c.lstrip())
                cells[k] = c[:lead] + RLM + c[lead:]
        return '|'.join(cells)
    m = PREFIX.match(line)
    pre, rest = m.group(1), line[m.end():]
    if needs_rlm(rest):
        return pre + RLM + rest
    return line


QFENCE = re.compile(r'^(\s*(?:>\s?)*)((?:[-*+]|\d+[.)])\s+)?(`{3,}|~{3,})')
QUOTE = re.compile(r'^(\s*(?:>\s?)*)')
OPEN_LTR = '<div dir="ltr">'


def bare(line):
    """Line content without blockquote markers and surrounding spaces."""
    return QUOTE.sub('', line, count=1).strip()


def qblank(q):
    """A blank line that stays inside the same blockquote."""
    return q.rstrip() if '>' in q else ''


def unwrap(lines):
    """Remove wrappers added by an earlier run (also inside quotes and list items)."""
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        b = bare(line)
        m = re.match(r'^(\s*(?:>\s?)*)((?:[-*+]|\d+[.)])\s+)' + re.escape(OPEN_LTR) + r'\s*$', line)
        if m:  # "1. <div dir=ltr>" : put the list marker back on the fence line
            q, marker = m.group(1), m.group(2)
            i += 1
            while i < len(lines) and bare(lines[i]) == '':
                i += 1
            if i < len(lines):
                out.append(q + marker + bare(lines[i]))
                i += 1
            continue
        if b in (OPEN, OPEN_LTR, CLOSE):
            i += 1
            if i < len(lines) and bare(lines[i]) == '' and out and bare(out[-1]) == '':
                i += 1  # drop the blank line we added next to the tag
            continue
        out.append(line)
        i += 1
    return out


def wrap(text):
    lines = unwrap(text.rstrip('\n').split('\n'))
    while lines and lines[0].strip() == '':
        lines.pop(0)
    out, fence, close_ind, q = [OPEN, ''], None, '', ''
    for line in lines:
        if fence is None:
            m = QFENCE.match(line)
            if m:
                q, marker, fence = m.group(1), m.group(2) or '', m.group(3)[0] * 3
                lead = re.match(r'^\s*', q).group(0)
                if marker:
                    close_ind = q + ' ' * len(marker)
                    if out[-1].strip():
                        out.append(qblank(q))
                    out += [q + marker + OPEN_LTR, qblank(q), close_ind + line[m.end(2):]]
                else:
                    close_ind = q
                    if bare(out[-1]):
                        out.append(qblank(q))
                    out += [q + OPEN_LTR, qblank(q), line]
                continue
            out.append(fix_line(line))
            continue
        out.append(line)
        if bare(line).startswith(fence) and bare(line).strip(fence[0]) == '':
            out += [qblank(q), close_ind + CLOSE, qblank(q)]
            fence = None
    while out and out[-1].strip() == '':
        out.pop()
    out += ['', CLOSE, '']
    res = re.sub(r'\n{3,}', '\n\n', '\n'.join(out))
    return re.sub(r'(?m)^([ \t]*>)[ \t]*\n(?:[ \t]*>[ \t]*\n)+', r'\1\n', res)  # one quote-blank is enough


for path in sys.argv[1:]:
    src = open(path, encoding='utf-8').read()
    new = wrap(src)
    if new != src:
        open(path, 'w', encoding='utf-8').write(new)
        print('wrapped', path)
