"""Report broken relative links in course markdown. Usage: python3 _tools/check_internal_links.py"""
import os, re, sys
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
bad = 0
for d, _, fs in os.walk(root):
    if '.git' in d.split(os.sep) or os.sep + 'work' in d:
        continue
    for f in fs:
        if f.endswith('.md') and not f.startswith('_old'):
            p = os.path.join(d, f)
            for t in re.findall(r'\]\(([^)#\s]+)\)', open(p, encoding='utf-8').read()):
                if not t.startswith('http') and not os.path.exists(os.path.normpath(os.path.join(d, t))):
                    print('BROKEN', os.path.relpath(p, root), '->', t); bad += 1
print('broken links:', bad); sys.exit(1 if bad else 0)
