#!/usr/bin/env python3
"""Compare predicted genes (e.g. Pyrodigal GFF) with a reference annotation (e.g. RefSeq GFF3).

Two CDS are "the same gene" when they share strand and STOP coordinate (gene callers agree on stops far
more often than on starts). Then we check whether the START also agrees.

Usage:
  python3 compare_genecalls.py reference.gff predicted.gff [--show 5]
Reference CDS marked pseudo=true are reported separately (a caller sees an ORF there, curators see a broken gene).
"""
import argparse
from collections import Counter


def read_cds(path, keep_pseudo=False):
    """{(strand, stop): [(start, length, label), ...]} for CDS lines; multi-segment CDS use outer coordinates.
    A list, because some genes share a stop (in-frame internal starts, e.g. mcrB and mcrB-S)."""
    seg = {}
    with open(path) as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) < 9 or f[2] != "CDS":
                continue
            pseudo = "pseudo=true" in f[8]
            if pseudo != keep_pseudo:
                continue
            attr = dict(x.split("=", 1) for x in f[8].split(";") if "=" in x)
            key = attr.get("ID", f"{f[3]}-{f[4]}")
            s, e = int(f[3]), int(f[4])
            if key in seg:
                seg[key][0], seg[key][1] = min(seg[key][0], s), max(seg[key][1], e)
            else:
                seg[key] = [s, e, f[6], attr.get("gene", attr.get("locus_tag", key))]
    out = {}
    for s, e, strand, label in seg.values():
        start, stop = (s, e) if strand == "+" else (e, s)
        out.setdefault((strand, stop), []).append((start, e - s + 1, label))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("reference"); ap.add_argument("predicted")
    ap.add_argument("--show", type=int, default=5, help="examples to print per category")
    args = ap.parse_args()

    ref, pseudo, pred = read_cds(args.reference), read_cds(args.reference, keep_pseudo=True), read_cds(args.predicted)
    n_ref_total = sum(len(v) for v in ref.values())
    pred = {k: v[0] for k, v in pred.items()}            # a gene caller gives one start per stop
    both = ref.keys() & pred.keys()
    same_start = [k for k in both if pred[k][0] in {r[0] for r in ref[k]}]
    diff_start = [k for k in both if k not in set(same_start)]
    near = {k: min(ref[k], key=lambda r: abs(r[0] - pred[k][0])) for k in diff_start}   # closest reference start
    ref = {k: max(v, key=lambda r: r[1]) if k not in near else near[k] for k, v in ref.items()}
    ref_only = sorted(ref.keys() - pred.keys(), key=lambda k: ref[k][1])
    pred_only = pred.keys() - ref.keys()
    pred_on_pseudo = [k for k in pred_only if k in pseudo]

    print(f"reference CDS: {n_ref_total} with {len(ref)} distinct stops  (+ {len(pseudo)} pseudogene CDS)   predicted CDS: {len(pred)}")
    print(f"same stop:                 {len(both)}  ({100 * len(both) / len(ref):.1f}% of reference)")
    print(f"  ... and same start:      {len(same_start)}  ({100 * len(same_start) / len(both):.1f}% of matched)")
    print(f"  ... different start:     {len(diff_start)}")
    longer = sum(abs(pred[k][0] - k[1]) > abs(ref[k][0] - k[1]) for k in diff_start)
    print(f"      predicted longer: {longer}   shorter: {len(diff_start) - longer}")
    print(f"reference only (missed):   {len(ref_only)}")
    print(f"predicted only:            {len(pred_only)}  (of which on a reference pseudogene: {len(pred_on_pseudo)})")

    lens = Counter("<100 aa" if ref[k][1] < 303 else ">=100 aa" for k in ref_only)
    print(f"missed genes by length:    {dict(lens)}")
    print("shortest missed:", ", ".join(f"{ref[k][2]} ({ref[k][1] // 3 - 1} aa)" for k in ref_only[:args.show]))
    print("longest missed: ", ", ".join(f"{ref[k][2]} ({ref[k][1] // 3 - 1} aa)" for k in ref_only[-args.show:]))
    shifts = sorted(diff_start, key=lambda k: -abs(ref[k][0] - pred[k][0]))[:args.show]
    print("largest start disagreements:", ", ".join(f"{ref[k][2]} ({abs(ref[k][0] - pred[k][0])} nt)" for k in shifts))


if __name__ == "__main__":
    main()
