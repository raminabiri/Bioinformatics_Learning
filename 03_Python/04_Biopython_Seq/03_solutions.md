<div dir="rtl">

# پاسخ تشریحی: Biopython (۱)؛ توالی، ترجمه، FASTA و FASTQ

> کدها در 2026-10-20 با Python 3.13.15 و Biopython 1.88، در پوشه‌ی داده‌ی بخش ۰۱ اجرا شدند.

---

## تمرین ۱: جهش H526Y را خودتان بسازید

<div dir="ltr">

```python
from Bio import SeqIO
from Bio.Seq import Seq
rec = SeqIO.read("ecoli_k12.fna", "fasta")
rpoB = rec.seq[4181245 - 1:4185273]
i = 4182820 - 4181245
print(i, i // 3 + 1, i % 3)
codon = rpoB[525 * 3:525 * 3 + 3]
print(codon, codon.translate(table=11))
s = str(rpoB)
mut = Seq(s[:i] + "T" + s[i + 1:])
print(mut[525 * 3:525 * 3 + 3], mut.translate(table=11, cds=True)[525])
p = rpoB.translate(table=11, cds=True)
q = mut.translate(table=11, cds=True)
print(p[520:531])
print(q[520:531])
n = 0
for a, b in zip(p, q):
    if a != b:
        n = n + 1
print(n)
```

</div>

<div dir="ltr">

```text
1575 526 0
CAC H
TAC Y
LSEITHKRRIS
LSEITYKRRIS
1
```

</div>

1. ‏`i` = **۱۵۷۵** (فاصله از باز یکم rpoB، شماره از ۰). `1575 // 3 + 1` = کدون **۵۲۶**؛ `1575 % 3` = ۰، یعنی **باز یکم** کدون.
2. ‏**CAC** → **H** (هیستیدین).
3. ‏**TAC** → **Y** (تیروزین): **H526Y**، همان جهشی که در VCF بخش ۰۲ دیدیم.
4. تنها **۱** جایگاه. یک جهش نقطه‌ای بدمعنی (missense) یک آمینواسید را عوض می‌کند؛ ولی همین یک آمینواسید، در جیب اتصال ریفامپیسین، مقاومت می‌آورد.

**چرا `str()`؟** `Seq` مانند رشته **تغییرناپذیر** است؛ نمی‌شود `s[i] = "T"` نوشت. یک رشته‌ی تازه از سه تکه می‌سازیم.

---

## تمرین ۲: جایگاه‌های مقاومت به کینولون در GyrA

<div dir="ltr">

```python
from Bio import SeqIO
rec = SeqIO.read("ecoli_k12.fna", "fasta")
gyrA = rec.seq[2336793 - 1:2339420].reverse_complement()
p = gyrA.translate(table=11, cds=True)
print(p[82], p[86])
print(gyrA[82 * 3:83 * 3], gyrA[86 * 3:87 * 3])
```

</div>

<div dir="ltr">

```text
S D
TCG GAC
```

</div>

آمینواسید ۸۳ **سرین** (کدون `TCG`) و ۸۷ **آسپارتات** (`GAC`) است. جهش‌های رایج بالینی S83L (`TCG`→`TTG`) و D87N (`GAC`→`AAC`) هستند؛ هر دو تنها با یک تغییر باز. این ناحیه (آمینواسیدهای حدود ۶۷ تا ۱۰۶) **QRDR** نام دارد، همتای RRDR در rpoB.

---

## تمرین ۳: rpoA با اسکریپت

<div dir="ltr">

```bash
python3 $P/extract_gene.py ecoli_k12.fna rpoA 3440040 3441029 -
head -n 2 rpoA.faa
```

</div>

<div dir="ltr">

```text
rpoA: 990 nt, 329 aa, starts with MQGSVTEFLK
>rpoA translated with table 11, 329 aa
MQGSVTEFLKPRLVDIEQVSSTHAKVTLEPLERGFGHTLGNALRRILLSSMPGCAVTEVE
```

</div>

**۹۹۰** نوکلئوتید، **۳۲۹** آمینواسید (۹۹۰ ÷ ۳ = ۳۳۰ کدون، منهای کدون پایان)، آغاز با `MQGSVTEFLK`. با `+`، مانند اشتباه ۱ درس، `TranslationError` می‌گیرید، چون بی مکمل معکوس، توالی از پایان ژن آغاز می‌شود.

---

## تمرین ۴: هر رید از کدام باکتری است؟

<div dir="ltr">

```python
import gzip
from Bio import SeqIO
counts = {}
with gzip.open("fastq/minigut_R1.fastq.gz", "rt") as f:
    for rec in SeqIO.parse(f, "fastq"):
        source = rec.id[:11]
        counts[source] = counts.get(source, 0) + 1
print(counts)
```

</div>

<div dir="ltr">

```text
{'NC_006347.1': 28912, 'NC_000913.3': 21088}
```

</div>

<div dir="ltr">

```bash
grep -P '^minigut\t' ground_truth.tsv
```

</div>

<div dir="ltr">

```text
minigut	28912	NC_006347.1	Bacteroides fragilis YCH46
minigut	21088	NC_000913.3	Escherichia coli K-12 MG1655
```

</div>

دقیقاً برابر: ۲۸٬۹۱۲ رید از *Bacteroides fragilis* و ۲۱٬۰۸۸ از *E. coli* (همان عدد `seqkit grep`). این نمونه‌ی **شبیه‌سازی‌شده** است و نام ریدها منبعشان را می‌گوید. در داده‌ی واقعی چنین نیست و باید ریدها را با ابزارهای **طبقه‌بندی تاکسونومیک** (بخش ۰۶) و یک پایگاه داده‌ی **کامل** نسبت داد.

---

## تمرین ۵: آستانه‌ی کیفیت

<div dir="ltr">

```bash
python3 $P/fastq_quality.py fastq/minigut_R1.fastq.gz good_30.fastq 30
python3 $P/fastq_quality.py fastq/minigut_R1.fastq.gz good_35.fastq 35
```

</div>

<div dir="ltr">

```text
reads: 50000
bases: 6300000
mean read length: 126.0
reads with mean Q >= 30: 47097 (94.2%)
reads: 50000
bases: 6300000
mean read length: 126.0
reads with mean Q >= 35: 46338 (92.7%)
```

</div>

با آستانه‌ی ۳۰، **۹۴٫۲٪** و با ۳۵، **۹۲٫۷٪**. `minigut_sample2` با ۹۹٫۳٪ کیفیت بهتری دارد (همان نتیجه‌ی Q30 در `seqkit stats -a` بخش ۰۲: ۹۲٪ در برابر ۹۶٪). آستانه‌ی سخت‌تر ریدهای بیشتری را دور می‌ریزد؛ انتخاب آن یک **داوری** است، نه یک قاعده.

---

## تمرین ۶: سه رید یکم به صورت FASTA

<div dir="ltr">

```python
import gzip
from Bio import SeqIO
first = []
with gzip.open("fastq/minigut_sample2_R1.fastq.gz", "rt") as f:
    for rec in SeqIO.parse(f, "fastq"):
        if len(first) < 3:
            first.append(rec)
n = SeqIO.write(first, "first3.fasta", "fasta")
print(n)
```

</div>

<div dir="ltr">

```bash
grep '>' first3.fasta
head -n 4 first3.fasta
```

</div>

<div dir="ltr">

```text
3
>CP009257.1_0_0/1
>CP009257.1_1_0/1
>CP009257.1_2_0/1
>CP009257.1_0_0/1
ACAATATAATCACCATCAACAGGTAGCGTTACTTCACCTGAAAAACCTACAGTCGAACCC
ACGAATAATGGCTTATCTTTACCAGGCTTTTGACCTGGAGCGAAAATATTAATATAAGCT
AAATTACCATAACTATTAGACCTCTTGCGAA
```

</div>

سه رکورد نوشته شد؛ رید ۱۵۱ بازی در خط‌های ۶۰تایی شکسته شد. **کیفیت‌ها کنار گذاشته شدند**: FASTA جایی برای کیفیت ندارد. با همان رکوردها، فرمت `"fastq"` کیفیت‌ها را نگه می‌داشت.

**نکته:** این حلقه همه‌ی ۲۴٬۹۹۳ رید را می‌خواند، هرچند تنها سه تا لازم بود. برای فایل‌های بزرگ، دستور `break` (بیرون پریدن از حلقه) کار را زودتر تمام می‌کند؛ با کمی جستجو درباره‌ی آن بخوانید.

</div>
