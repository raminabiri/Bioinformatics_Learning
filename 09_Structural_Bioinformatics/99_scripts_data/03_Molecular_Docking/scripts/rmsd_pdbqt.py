import sys, math
def models(path):
    out, cur = [], []
    for l in open(path):
        if l.startswith(('ATOM','HETATM')):
            cur.append((l[12:16].strip(), l[77:79].strip(), float(l[30:38]), float(l[38:46]), float(l[46:54])))
        elif l.startswith('ENDMDL'):
            out.append(cur); cur=[]
    if cur: out.append(cur)
    return out
ref = models(sys.argv[1])[0]
for i, m in enumerate(models(sys.argv[2]), 1):
    assert [a[0] for a in m] == [a[0] for a in ref]
    pairs = [(a, b) for a, b in zip(ref, m) if a[1] not in ('H', 'HD')]
    d = sum((a[2]-b[2])**2 + (a[3]-b[3])**2 + (a[4]-b[4])**2 for a, b in pairs)
    print(i, len(pairs), round(math.sqrt(d/len(pairs)), 2))
