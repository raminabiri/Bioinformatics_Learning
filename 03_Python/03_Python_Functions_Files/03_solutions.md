<div dir="rtl">

# پاسخ تشریحی: تابع و فایل

> کدها در 2026-10-20 با Python 3.13.15، در پوشه‌ی داده‌ی بخش ۰۱ اجرا شدند.

---

## تمرین ۱: دو تابع برای DNA

<div dir="ltr">

```python
def gc_percent(seq):
    """Return the GC percentage of a DNA sequence, rounded to 2 decimals."""
    seq = seq.upper()
    gc = seq.count("G") + seq.count("C")
    return round(gc / len(seq) * 100, 2)

def reverse_complement(seq):
    comp = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}
    out = ""
    for b in reversed(seq):
        out = out + comp[b]
    return out

g = "ATGAGCGACCTTGCGAGAGAAATTACACCG"
print(gc_percent("ATGGTTTAC"))
print(gc_percent(g))
print(gc_percent("atggcc"))
rc = reverse_complement(g)
print(rc)
print(gc_percent(rc))
print(reverse_complement(rc) == g)
```

</div>

<div dir="ltr">

```text
33.33
50.0
66.67
CGGTGTAATTTCTCTCGCAAGGTCGCTCAT
50.0
True
```

</div>

1. **۳۳٫۳۳**، **۶۶٫۶۷** (حروف کوچک هم درست شمرده شدند، به لطف `.upper()`) و **۵۰٫۰**.
2. ‏`CGGTGTAATTTCTCTCGCAAGGTCGCTCAT`، با همان **۵۰٪** GC. مکمل هر G یک C است و وارونه کردن ترتیب هم شمار را عوض نمی‌کند؛ پس GC دو رشته‌ی یک DNA همیشه برابر است.
3. ‏`True`: دو بار مکمل معکوس، توالی را به حال یکم برمی‌گرداند. این یک **آزمون ساده** برای درستی تابع است.

**نکته:** چون `gc_percent` نتیجه را `return` می‌کند، توانستیم آن را درون `print` و روی خروجی تابع دیگر (`rc`) به کار ببریم.

---

## تمرین ۲: هر نوع خط GFF چند بار آمده؟

<div dir="ltr">

```python
import sys
counts = {}
with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith("#"):
            continue
        cols = line.rstrip("\n").split("\t")
        counts[cols[2]] = counts.get(cols[2], 0) + 1
for t in counts:
    print(t, counts[t])
```

</div>

<div dir="ltr">

```bash
python3 ex2.py ecoli_k12.gff
```

</div>

<div dir="ltr">

```text
region 1
gene 4506
CDS 4340
mobile_genetic_element 50
ncRNA 108
exon 216
rRNA 22
tRNA 86
pseudogene 145
sequence_feature 48
origin_of_replication 1
```

</div>

دستور بخش ۰۱ همان عددها را می‌دهد، تنها با ترتیب دیگر (مرتب از بیشتر به کمتر):

<div dir="ltr">

```text
   4506 gene
   4340 CDS
    216 exon
    145 pseudogene
    108 ncRNA
     86 tRNA
     50 mobile_genetic_element
     48 sequence_feature
     22 rRNA
      1 region
      1 origin_of_replication
```

</div>

پایتون نوع‌ها را به **ترتیب نخستین دیدار** در فایل چاپ می‌کند (دیکشنری ترتیب افزودن را نگه می‌دارد). ۴٬۳۴۰ CDS کمتر از ۴٬۵۰۶ ژن است، چون برخی ژن‌ها RNA می‌سازند (tRNA، rRNA، ncRNA)، نه پروتئین.

---

## تمرین ۳: بلندترین ژن، با نامش

<div dir="ltr">

```python
import sys

def get_attribute(attributes, key):
    for part in attributes.split(";"):
        if part.startswith(key + "="):
            return part[len(key) + 1:]
    return ""

longest_name = ""
longest_len = 0
with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith("#"):
            continue
        cols = line.rstrip("\n").split("\t")
        if cols[2] != "gene":
            continue
        length = int(cols[4]) - int(cols[3]) + 1
        if length > longest_len:
            longest_len = length
            longest_name = get_attribute(cols[8], "Name")
print(longest_name, longest_len)
```

</div>

<div dir="ltr">

```text
yeeJ 7020
```

</div>

‏**yeeJ** با **۷٬۰۲۰** باز (بنا بر ستون `product` در خط CDS آن: `inverse autotransporter adhesin`، یک پروتئین چسبندگی سطح یاخته). نام و طول باید **با هم** در یک `if` عوض شوند؛ وگرنه نام از یک ژن و طول از ژن دیگری می‌ماند.

---

## تمرین ۴: GFF به BED، با پایتون

<div dir="ltr">

```python
# to_bed.py: write the genes of a GFF file as a BED file
import sys

def get_attribute(attributes, key):
    for part in attributes.split(";"):
        if part.startswith(key + "="):
            return part[len(key) + 1:]
    return ""

gff_file = sys.argv[1]
bed_file = sys.argv[2]
n = 0
with open(gff_file) as f, open(bed_file, "w") as out:
    for line in f:
        if line.startswith("#"):
            continue
        cols = line.rstrip("\n").split("\t")
        if cols[2] != "gene":
            continue
        start = int(cols[3]) - 1          # BED is 0-based
        end = int(cols[4])
        name = get_attribute(cols[8], "Name")
        out.write(f"{cols[0]}\t{start}\t{end}\t{name}\t0\t{cols[6]}\n")
        n = n + 1
print("wrote", n, "lines to", bed_file)
```

</div>

<div dir="ltr">

```bash
python3 to_bed.py ecoli_k12.gff genes_py.bed
head -n 3 genes_py.bed
grep -P '\trpoB\t' genes_py.bed
```

</div>

<div dir="ltr">

```text
wrote 4506 lines to genes_py.bed
NC_000913.3	189	255	thrL	0	+
NC_000913.3	336	2799	thrA	0	+
NC_000913.3	2800	3733	thrB	0	+
NC_000913.3	4181244	4185273	rpoB	0	+
```

</div>

‏thrL در GFF از ۱۹۰ تا ۲۵۵ است و در BED از **۱۸۹** تا ۲۵۵؛ rpoB هم ۴٬۱۸۱٬۲۴۴. **تفاوت با `genes.bed` درس آنوتیشن:** در آن‌جا `awk` به جای نام، `.` می‌گذاشت (بیرون کشیدن نام از ستون ۹ با `awk` دشوار بود). در پایتون، با تابع `get_attribute`، نام هم آمد؛ پس می‌توانیم با `grep` دنبال `rpoB` بگردیم.

---

## تمرین ۵: بریدن ژن از ژنوم

<div dir="ltr">

```python
def read_fasta(path):
    seqs = {}
    name = None
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith(">"):
                name = line[1:].split()[0]
                seqs[name] = []
            else:
                seqs[name].append(line)
    result = {}
    for name in seqs:
        result[name] = "".join(seqs[name])
    return result

def reverse_complement(seq):
    comp = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}
    out = ""
    for b in reversed(seq):
        out = out + comp[b]
    return out

genome = read_fasta("ecoli_k12.fna")
print(list(genome.keys()))
chrom = genome["NC_000913.3"]
print(len(chrom))
rpoB = chrom[4181245 - 1:4185273]
print(len(rpoB), rpoB[:30], rpoB[-3:])
gyrA = reverse_complement(chrom[2336793 - 1:2339420])
print(len(gyrA), gyrA[:30], gyrA[-3:])
wrong = reverse_complement(chrom[2336793:2339420])
print(len(wrong), wrong[:30])
print(wrong[-3:])
```

</div>

<div dir="ltr">

```text
['NC_000913.3']
4641652
4029 ATGGTTTACTCCTATACCGAGAAAAAACGT TAA
2628 ATGAGCGACCTTGCGAGAGAAATTACACCG TAA
2627 ATGAGCGACCTTGCGAGAGAAATTACACCG
ATA
```

</div>

1. یک توالی با **۴٬۶۴۱٬۶۵۲** باز.
2. ‏rpoB: **۴٬۰۲۹** باز، با `ATG` آغاز و با کدون پایان `TAA` تمام می‌شود.
3. ‏gyrA: **۲٬۶۲۸** باز و **بله**، دقیقاً با `ATGAGCGACC…` آغاز می‌شود و با `TAA` تمام. برای ژن رشته‌ی `-`، «آغاز» ژن در **پایان** بازه‌ی GFF است؛ مکمل معکوس آن را به ترتیب ۵′ به ۳′ ژن برمی‌گرداند.
4. بی `-1`، **یک باز کم** می‌شود (۲٬۶۲۷). این‌جا آغاز درست ماند (چون آغاز gyrA در سر دیگر بازه است)، ولی **پایان** خراب شد: به جای کدون پایان `TAA`، `ATA`. همان خطای «یکی کم/زیاد» درس BED، این بار در پایتون. ژن رشته‌ی + در همین اشتباه **آغازش** را از دست می‌دهد.

---

## تمرین ۶: جستجوی یک ژن از ترمینال

<div dir="ltr">

```python
# find_gene.py: print the coordinates of one gene from a GFF file
# Usage: python3 find_gene.py ecoli_k12.gff rpoB
import sys

def get_attribute(attributes, key):
    for part in attributes.split(";"):
        if part.startswith(key + "="):
            return part[len(key) + 1:]
    return ""

gff_file = sys.argv[1]
wanted = sys.argv[2]
found = False
with open(gff_file) as f:
    for line in f:
        if line.startswith("#"):
            continue
        cols = line.rstrip("\n").split("\t")
        if cols[2] != "gene":
            continue
        if get_attribute(cols[8], "Name") == wanted:
            start = int(cols[3])
            end = int(cols[4])
            print(wanted, start, end, cols[6], end - start + 1)
            found = True
if not found:
    print(wanted, "not found")
```

</div>

<div dir="ltr">

```bash
for g in rpoB gyrA rpoC RPOB; do python3 find_gene.py ecoli_k12.gff $g; done
python3 find_gene.py ecoli_k12.gff
```

</div>

<div dir="ltr">

```text
rpoB 4181245 4185273 + 4029
gyrA 2336793 2339420 - 2628
rpoC 4185350 4189573 + 4224
RPOB not found
```

</div>

<div dir="ltr">

```text
IndexError: list index out of range
```

</div>

- سه ژن با جای درست. (یک حلقه‌ی `for` Bash، اسکریپت پایتون را چند بار اجرا کرد: دو ابزار در کنار هم.)
- ‏**`RPOB` پیدا نشد**: مقایسه‌ی رشته‌ها در پایتون به **بزرگی و کوچکی حروف** حساس است. نام ژن‌های باکتری با حرف کوچک آغاز می‌شود (`rpoB`)، نام پروتئین با حرف بزرگ (`RpoB`).
- بی نام ژن، `sys.argv[2]` نیست (آخرین خط پیام بالا). برای پیام روشن‌تر، کادر کنجکاوهای درس (`sys.exit`) را ببینید.
- ‏`found` یک **پرچم** است: متغیری `True`/`False` که پس از حلقه می‌گوید چیزی دیده شد یا نه.

</div>
