<div dir="rtl">

# پاسخ تشریحی: Biopython (۲)؛ GenBank، ویژگی‌ها و Entrez

> کدها در 2026-10-20 با Python 3.13.15 و Biopython 1.88 اجرا شدند. تمرین ۵ به اینترنت (NCBI) نیاز داشت.

---

## تمرین ۱: ویژگی‌های `rpo_region.gb` را بشمارید

<div dir="ltr">

```python
from Bio import SeqIO
rec = SeqIO.read("rpo_region.gb", "genbank")
counts = {}
for f in rec.features:
    counts[f.type] = counts.get(f.type, 0) + 1
print(counts)
total = 0
for f in rec.features:
    if f.type == "CDS":
        total = total + len(f.qualifiers["translation"][0])
print(total)
```

</div>

<div dir="ltr">

```text
{'source': 1, 'gene': 15, 'CDS': 11, 'tRNA': 4}
4608
```

</div>

1. ‏۱ `source`، ۱۵ `gene`، ۱۱ `CDS` و ۴ `tRNA` (جمع ۳۱). هر CDS و هر tRNA یک `gene` هم دارد: ۱۱ + ۴ = ۱۵.
2. **۴٬۶۰۸** آمینواسید. نزدیک به نیمی از آن (۱٬۳۴۲ + ۱٬۴۰۷) تنها از rpoB و rpoC است.

---

## تمرین ۲: rpoC و حذف یک‌بازی سویه‌ی مقاوم

<div dir="ltr">

```python
from Bio import SeqIO
from Bio.Seq import Seq
rec = SeqIO.read("rpo_region.gb", "genbank")
for f in rec.features:
    if f.type == "CDS" and f.qualifiers["gene"][0] == "rpoC":
        rpoC = f
dna = rpoC.extract(rec.seq)
p = dna.translate(table=11, cds=True)
print(len(dna), len(p), str(p) == rpoC.qualifiers["translation"][0])

i = 4189000 - 4185350
print(i, i // 3 + 1, i % 3, dna[i])
s = str(dna)
mut = Seq(s[:i] + s[i + 1:])
print(len(mut), len(mut) % 3)
print(len(mut.translate(table=11, to_stop=True)))
print(dna.translate(table=11)[1210:1225])
print(mut.translate(table=11)[1210:1225])
```

</div>

<div dir="ltr">

```text
4224 1407 True
3650 1217 2 G
4223 2
1331
SDGPEAPHDILRLRG
SDGPEAPTTFCVCVV
```

</div>

(یک `BiopythonWarning: Partial codon` هم برای ترجمه‌ی `mut` می‌آید، چون طولش مضرب ۳ نیست؛ تمرین ۳ درس پیشین.)

1. **۴٬۲۲۴** نوکلئوتید، **۱٬۴۰۷** آمینواسید، و `True`: با NCBI یکی است.
2. کدون **۱۲۱۷** (`3650 // 3 + 1`)، باز **سوم** (`3650 % 3 = 2`)، که یک **G** است.
3. ۴٬۲۲۳ باز، باقی‌مانده ۲: **چارچوب خواندن جابه‌جا شد** (frameshift). پروتئین تنها **۱٬۳۳۱** آمینواسید پیش می‌رود و به یک کدون پایان زودرس می‌رسد، به جای ۱٬۴۰۷.
4. تا `P` جایگاه ۱۲۱۷ یکی‌اند (کدون `CCG` بی G پایانی، با باز بعدی هنوز `CC?` = Pro می‌سازد)؛ از **۱۲۱۸** همه چیز عوض می‌شود: `HDILRLRG` → `TTFCVCVV`.

**نگاه زیستی:** این حذف در سویه‌ی آموزشی ما **ساختگی** است و زیرواحد β′ را کوتاه می‌کند؛ در یاخته‌ی واقعی چنین جهشی در ژنی ضروری مانند rpoC در بسیاری از موارد کشنده است. جهش‌های جبرانی **واقعی** rpoC در سویه‌های مقاوم به ریفامپیسین، جهش‌های نقطه‌ای بدمعنی‌اند.

---

## تمرین ۳: پروتئین‌های ناحیه در یک FASTA

<div dir="ltr">

```python
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
rec = SeqIO.read("rpo_region.gb", "genbank")
proteins = []
for f in rec.features:
    if f.type == "CDS":
        name = f.qualifiers["gene"][0]
        prot = Seq(f.qualifiers["translation"][0])
        proteins.append(SeqRecord(prot, id=f.qualifiers["protein_id"][0], description=name))
n = SeqIO.write(proteins, "rpo_region_proteins.faa", "fasta")
print(n)
```

</div>

<div dir="ltr">

```bash
grep '>' rpo_region_proteins.faa
```

</div>

<div dir="ltr">

```text
11
>NP_418405.1 coaA
>NP_418407.1 tufB
>NP_418408.1 secE
>NP_418409.1 nusG
>NP_418410.1 rplK
>NP_418411.1 rplA
>NP_418412.1 rplJ
>NP_418413.1 rplL
>NP_418414.1 rpoB
>NP_418415.1 rpoC
>NP_418416.1 yjaZ
```

</div>

۱۱ پروتئین. **coaA** و **yjaZ** در لبه‌های ناحیه نیمه‌اند (`<1` و `>15001`)، ولی `translation` آن‌ها **کامل** است (۳۱۶ و ۱۷۹ آمینواسید، خروجی `gb_genes.py` در درس)، چون NCBI آن را از رکورد کامل ژنوم برداشته است. پس پروتئین این FASTA درست است، ولی اگر خودتان آن‌ها را با `.extract()` ترجمه می‌کردید، نادرست می‌شد.

---

## تمرین ۴: tRNAها

<div dir="ltr">

```python
from Bio import SeqIO
rec = SeqIO.read("rpo_region.gb", "genbank")
for f in rec.features:
    if f.type == "tRNA":
        print(f.qualifiers)
        break
```

</div>

<div dir="ltr">

```text
{'gene': ['thrU'], 'locus_tag': ['b3976'], 'gene_synonym': ['ECK3967'], 'product': ['tRNA-Thr'], 'note': ['tRNA-Thr(UGU)'], 'db_xref': ['ECOCYC:EG30102', 'GeneID:948476']}
```

</div>

‏(`break` حلقه را پس از نخستین tRNA می‌ایستاند؛ تنها برای نگاه کردن.) آنتی‌کدون در `note` است: `tRNA-Thr(UGU)`. سپس:

<div dir="ltr">

```python
for f in rec.features:
    if f.type == "tRNA":
        start = int(f.location.start) + 1
        end = int(f.location.end)
        print(f.qualifiers["gene"][0], start, end, f.qualifiers["note"][0])
```

</div>

<div dir="ltr">

```text
thrU 389 464 tRNA-Thr(UGU)
tyrU 473 557 tRNA-Tyr(GUA)
glyT 674 748 tRNA-Gly(UCC)
thrT 755 830 tRNA-Thr(GGU)
```

</div>

دو tRNA برای ترئونین با آنتی‌کدون‌های **گوناگون** (UGU و GGU): هر کدام کدون‌های متفاوتی از ترئونین را می‌خوانند (ACA/ACG و ACC/ACU، با جفت‌شدن لرزان).

---

## تمرین ۵: gyrA از NCBI

<div dir="ltr">

```bash
python3 $P/fetch_region.py NC_000913.3 2336793 2339420 gyrA.gb
python3 $P/gb_genes.py gyrA.gb
```

</div>

<div dir="ltr">

```text
wrote 13172 characters to gyrA.gb
NC_000913.3 2628 bp
CDS	gyrA	1	2628	-	875 aa	DNA gyrase subunit A
```

</div>

<div dir="ltr">

```python
from Bio import SeqIO
rec = SeqIO.read("gyrA.gb", "genbank")
for f in rec.features:
    if f.type == "CDS":
        print(f.qualifiers["gene"][0], f.location)
        dna = f.extract(rec.seq)
        print(dna[:30])
        print(rec.seq[:30])
        p = dna.translate(table=11, cds=True)
        print(len(p), p[82], p[86], str(p) == f.qualifiers["translation"][0])
```

</div>

<div dir="ltr">

```text
gyrA [0:2628](-)
ATGAGCGACCTTGCGAGAGAAATTACACCG
TTATTCTTCTTCTGGCTCGTCGTCAACGTC
875 S D True
```

</div>

1. یک CDS، gyrA، ۸۷۵ آمینواسید.
2. رشته‌ی **منفی** (`(-)`). `rec.seq` همیشه رشته‌ی + ژنوم است و با `TTA` (مکمل معکوس کدون پایان `TAA`) آغاز می‌شود؛ `.extract()` خودش مکمل معکوس کرد و `ATGAGC…` داد: همان آغاز gyrA در درس‌های پیشین.
3. ‏**S** (۸۳) و **D** (۸۷)، و ترجمه با NCBI یکی است.

---

## تمرین ۶: ژن‌هایی با کدون آغاز کمیاب

بخش دوم `cds_check.py` (بخش یکم، خواندن GFF، بی‌تغییر):

<div dir="ltr">

```python
for cds_id in cds:
    c = cds[cds_id]
    dna = Seq("")
    for start, end in sorted(c["pieces"]):
        dna = dna + genome[start - 1:end]
    if c["strand"] == "-":
        dna = dna.reverse_complement()
    first = str(dna[:3])
    if first == "ATT" or first == "CTG":
        print(c["gene"], first, dna.translate(table=11, cds=True)[:5])
```

</div>

<div dir="ltr">

```bash
python3 ex6.py $G/ecoli_k12.fna $G/ecoli_k12.gff
```

</div>

<div dir="ltr">

```text
pcnB ATT MFTRV
ymcF ATT MTQHL
ynfQ ATT MTNHI
infC ATT MKGGK
hda CTG MNTPA
yfjD CTG MEHIS
```

</div>

شش ژن، و **همه‌ی پروتئین‌ها با M** آغاز می‌شوند، چون `cds=True` کدون آغاز را fMet می‌خواند. نمونه‌ی نامدار **infC** (فاکتور آغاز ترجمه‌ی IF3) است: IF3 خودش آغاز ترجمه از کدون‌های غیرمعمول را سرکوب می‌کند، پس کدون آغاز ATT ژن خودش، **خودتنظیمی** (autoregulation) می‌سازد: هرچه IF3 بیشتر، ساخت IF3 کمتر.

</div>
