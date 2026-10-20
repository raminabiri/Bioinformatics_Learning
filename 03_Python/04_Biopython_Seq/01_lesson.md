<div dir="rtl">

# درس: Biopython (۱)؛ توالی، ترجمه و خواندن FASTA/FASTQ

**بخش:** `03_Python` · **ماژول:** `04_Biopython_Seq` · **پیش‌نیاز:** ماژول [تابع و فایل](../03_Python_Functions_Files/) · **زمان:** حدود ۹۰ دقیقه · **ابزار:** Python 3.13، Biopython 1.88 · **آخرین اجرا:** 2026-10-20

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. با شیء **`Seq`** کار کنید: مکمل، مکمل معکوس، رونویسی و **ترجمه با کد ژنتیکی باکتری** (`table=11`).
2. فرق `translate()` ساده و `translate(cds=True)` را بدانید (کدون آغاز GTG!).
3. فایل FASTA و FASTQ را با **`SeqIO`** بخوانید (حتی فشرده‌ی `.gz`) و کیفیت Phred هر باز را بگیرید.
4. توالی‌ها را با `SeqRecord` و `SeqIO.write` در فایل بنویسید.

**پیش از آغاز:**

<div dir="ltr">

```bash
conda activate bioinfo_course
python3 -c "import Bio; print(Bio.__version__)"
cd ~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data
P=~/Bioinformatics_Learning-main/03_Python/99_scripts_data/04_Biopython_Seq/scripts
```

</div>

<div dir="ltr">

```text
1.88
```

</div>

---

## ۱. داستان: چرا یک کتابخانه؟

در ماژول‌های پیشین، خودمان جدول کد ژنتیکی، تابع مکمل معکوس و خواننده‌ی FASTA نوشتیم. این کار برای **فهمیدن** عالی بود؛ ولی در کار روزانه:
- جدول ما تنها کد ژنتیکی **استاندارد** را دارد، نه کد میتوکندری یا باکتری؛
- خواننده‌ی ما FASTQ، GenBank و ده‌ها فرمت دیگر را نمی‌فهمد؛
- و هر کد تازه، جای تازه‌ای برای خطاست.

‏**Biopython** کتابخانه‌ای است که هزاران نفر این‌ها را در آن نوشته و آزموده‌اند. **کتابخانه** (library) یعنی مجموعه‌ای از تابع‌ها و ابزارهای آماده که با `import` به کار می‌روند؛ همان کاری که با `import sys` کردیم. (Biopython در محیط `bioinfo_course` نصب شده است.)

---

## ۲. شیء `Seq`

<div dir="ltr">

```python
>>> from Bio.Seq import Seq
>>> dna = Seq("ATGGTTTACTCCTATACCGAGAAAAAACGT")
>>> dna
Seq('ATGGTTTACTCCTATACCGAGAAAAAACGT')
>>> len(dna)
30
>>> dna[0:3]
Seq('ATG')
>>> dna.count("A")
11
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `from Bio.Seq import Seq` | از بسته‌ی `Bio`، بخش `Seq`، تنها نام `Seq` را بیاور |
| `Seq("ATG…")` | یک **توالی** بساز (۳۰ باز یکم rpoB) |
| ‏`len`، برش، `count` | همه **مانند رشته** کار می‌کنند |

پس فرقش با رشته چیست؟ **متدهای زیستی**:

<div dir="ltr">

```python
>>> dna.complement()
Seq('TACCAAATGAGGATATGGCTCTTTTTTGCA')
>>> dna.reverse_complement()
Seq('ACGTTTTTTCTCGGTATAGGAGTAAACCAT')
>>> dna.transcribe()
Seq('AUGGUUUACUCCUAUACCGAGAAAAAACGU')
>>> dna.translate(table=11)
Seq('MVYSYTEKKR')
>>> str(dna)
'ATGGTTTACTCCTATACCGAGAAAAAACGT'
```

</div>

| متد | زیست‌شناسی |
| :--- | :--- |
| `.complement()` | مکمل هر باز (A↔T، G↔C)، بی وارونه کردن |
| `.reverse_complement()` | رشته‌ی **دیگر** DNA، از ۵′ به ۳′؛ همان تابعی که ماژول پیشین نوشتیم |
| `.transcribe()` | رونویسی: T → U |
| `.translate(table=11)` | ترجمه؛ `table=11` = **کد ژنتیکی باکتری‌ها، آرکی‌ها و پلاستیدها** |
| `str(dna)` | برگرداندن به رشته‌ی ساده |

‏`MVYSYTEKKR` همان ترجمه‌ای است که در ماژول ۰۲ با جدول دست‌ساز خود گرفتیم.

### کالبدشکافی `translate`

<div dir="ltr">

```text
dna.translate( table=11 , cds=True , to_stop=True )
                  ①          ②           ③
```

</div>

| بخش | یعنی | اگر نباشد |
| :-: | :--- | :--- |
| ① `table=11` | شماره‌ی کد ژنتیکی NCBI | ‏`table=1` (استاندارد) به کار می‌رود |
| ② `cds=True` | «این یک **ژن کامل** است»: آغاز و پایان را وارسی کن | هر کدون همان‌گونه که هست ترجمه می‌شود |
| ③ `to_stop=True` | در نخستین کدون پایان بایست | کدون پایان `*` نوشته می‌شود و ترجمه ادامه می‌یابد |

<div dir="ltr">

```python
>>> Seq("ATGAAATAG").translate()
Seq('MK*')
>>> Seq("ATGAAATAG").translate(to_stop=True)
Seq('MK')
```

</div>

برای ۳۰ باز rpoB، `table=1` و `table=11` یک پاسخ می‌دهند؛ پس چرا `table=11`؟ بخش بعد.

---

## ۳. کدون آغاز GTG: چرا `cds=True` مهم است

حدود ۱۰٪ ژن‌های *E. coli* با **GTG** یا **TTG** آغاز می‌شوند، نه ATG. در یاخته، ریبوزوم کدون آغاز را **همیشه** با tRNA آغازگر (fMet) می‌خواند؛ پس پروتئین با **M** آغاز می‌شود، هرچند GTG در میانه‌ی ژن V است. یک ژن کوچک ساختگی:

<div dir="ltr">

```python
>>> s = Seq("GTGAAAAAGATGCAGTAA")
>>> s.translate(table=11)
Seq('VKKMQ*')
>>> s.translate(table=11, cds=True)
Seq('MKKMQ')
```

</div>

- بی `cds=True`: آمینواسید یکم **V** (نادرست برای یک پروتئین واقعی) و `*` پایانی.
- با `cds=True`: آمینواسید یکم **M**، و `*` برداشته شد. همچنین وارسی شد که طول مضرب ۳ باشد، کدون آخر پایان باشد و **هیچ** کدون پایانی درون ژن نباشد.

و اگر کد ژنتیکی نادرست بدهید:

<div dir="ltr">

```python
>>> s.translate(table=1, cds=True)
```

</div>

<div dir="ltr">

```text
Bio.Data.CodonTable.TranslationError: First codon 'GTG' is not a start codon
```

</div>

در کد ۱ (استاندارد)، GTG کدون آغاز به شمار نمی‌آید. **برای باکتری همیشه `table=11`.** (کد ۱۱ و ۱ در معنای کدون‌ها یکسان‌اند؛ تفاوت در **کدون‌های آغاز** است.)

اگر ژن کامل نباشد (کدون پایان نداشته باشد)، `cds=True` هم خطا می‌دهد:

<div dir="ltr">

```python
>>> Seq("GTGAAAAAGATGCAG").translate(table=11, cds=True)
```

</div>

<div dir="ltr">

```text
Bio.Data.CodonTable.TranslationError: Final codon 'CAG' is not a stop codon
```

</div>

‏**`TranslationError` دوست شماست:** به جای یک پروتئین بی‌معنی، می‌گوید مختصات یا رشته‌ی ژن نادرست است.

<details>
<summary>✋ <b>امتحان کن:</b> <code>Seq("ATGAA").translate()</code> چه می‌دهد؟</summary>

<div dir="ltr">

```text
BiopythonWarning: Partial codon, len(sequence) not a multiple of three. Explicitly trim the sequence or add trailing N before translation. This may become an error in future.
Seq('M')
```

</div>

یک **هشدار** (warning، نه خطا): طول ۵ مضرب ۳ نیست؛ دو باز پایانی `AA` کدون کامل نمی‌سازند و کنار گذاشته شدند. هشدار را جدی بگیرید: در بسیاری از موارد یعنی مختصات یکی جابه‌جاست.
</details>

---

## ۴. خواندن یک FASTA: `SeqIO.read`

<div dir="ltr">

```python
>>> from Bio import SeqIO
>>> rec = SeqIO.read("ecoli_k12.fna", "fasta")
>>> rec.id
'NC_000913.3'
>>> rec.description
'NC_000913.3 Escherichia coli str. K-12 substr. MG1655, complete genome'
>>> len(rec.seq)
4641652
```

</div>

| تکه | یعنی |
| :--- | :--- |
| ‏`SeqIO.read(فایل, فرمت)` | فایلی با **دقیقاً یک** توالی را بخوان |
| `rec` | یک **`SeqRecord`**: توالی + نام + توضیح (+ کیفیت، در FASTQ) |
| `rec.id` | شناسه (واژه‌ی یکم پس از `>`) |
| `rec.description` | کل خط عنوان |
| `rec.seq` | خود توالی، یک `Seq` |

همه‌ی کار ۱۵ خطی `read_fasta` ماژول پیشین، در یک خط.

### بریدن و ترجمه‌ی rpoB و gyrA

<div dir="ltr">

```python
>>> rpoB = rec.seq[4181245 - 1:4185273]
>>> prot = rpoB.translate(table=11)
>>> len(rpoB), len(prot)
(4029, 1343)
>>> prot[:10], prot[-3:]
(Seq('MVYSYTEKKR'), Seq('DE*'))
>>> prot_cds = rpoB.translate(table=11, cds=True)
>>> len(prot_cds)
1342
>>> prot_cds[525]
'H'
```

</div>

- **۱٬۳۴۲ آمینواسید**، همان طول RpoB در UniProt (بخش ۰۰). بی `cds=True`، ۱٬۳۴۳ نویسه، با `*` پایانی.
- ‏`prot_cds[525]`: آمینواسید **۵۲۶** (شماره‌ی پایتون از ۰). **H**: همان **His526** که در سویه‌ی مقاوم داستان ما به **Y** جهش یافته (H526Y، بخش ۰۲).

برای gyrA روی رشته‌ی منفی:

<div dir="ltr">

```python
>>> gyrA = rec.seq[2336793 - 1:2339420].reverse_complement()
>>> gyrA[:30]
Seq('ATGAGCGACCTTGCGAGAGAAATTACACCG')
>>> gyrA.translate(table=11, cds=True)[:20]
Seq('MSDLAREITPVNIEEELKSS')
>>> len(gyrA.translate(table=11, cds=True))
875
```

</div>

و اگر مکمل معکوس را **فراموش** کنید:

<div dir="ltr">

```python
>>> rec.seq[2336793 - 1:2339420].translate(table=11)[:20]
Seq('LFFFWLVVNVHFRSDFIVPF')
```

</div>

هیچ خطایی نیامد، ولی پروتئین **بی‌معنی** است (با M آغاز نمی‌شود). با `cds=True` همین اشتباه بی‌درنگ `TranslationError` می‌داد. **برای ژن‌های کامل، `cds=True` را به کار ببرید.**

---

## ۵. خواندن FASTQ: `SeqIO.parse` و کیفیت

فایل FASTQ هزاران رید دارد، پس `SeqIO.read` (تنها یک توالی) به کار نمی‌آید. **`SeqIO.parse`** رکوردها را **یکی‌یکی** می‌دهد، بی بارگذاری همه در حافظه؛ مانند `for line in f`.

فایل‌های ما `.gz` اند. کتابخانه‌ی `gzip` (همراه خود پایتون) آن‌ها را باز می‌کند:

<div dir="ltr">

```python
>>> import gzip
>>> from Bio import SeqIO
>>> f = gzip.open("fastq/minigut_sample2_R1.fastq.gz", "rt")
>>> reads = SeqIO.parse(f, "fastq")
>>> r = next(reads)
>>> r.id
'CP009257.1_0_0/1'
>>> len(r.seq)
151
>>> r.seq[:40]
Seq('ACAATATAATCACCATCAACAGGTAGCGTTACTTCACCTG')
>>> q = r.letter_annotations["phred_quality"]
>>> q[:12]
[37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37]
>>> min(q), max(q)
(12, 37)
>>> round(sum(q) / len(q), 2)
36.74
>>> f.close()
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `gzip.open(path, "rt")` | فایل فشرده را باز کن؛ `"rt"` = خواندن (*read*) به صورت **متن** (*text*). مانند `zcat` |
| `SeqIO.parse(f, "fastq")` | رکوردهای FASTQ را یکی‌یکی بده |
| `next(reads)` | رکورد **بعدی** را بگیر (این‌جا نخستین) |
| `r.letter_annotations["phred_quality"]` | فهرست **کیفیت Phred** هر باز، **عدد**، نه نویسه |

‏Biopython نویسه‌های کیفیت (`F` = ۳۷ و …) را خودش به عدد Phred برگرداند؛ همان جدولی که در بخش ۰۲ دستی خواندیم.

> **دو «میانگین کیفیت»:** برای رید یکم `minigut_R1`، این روش (میانگین ساده‌ی عددهای Phred) **۳۶٫۰۶** می‌دهد، ولی `seqkit fx2tab -q` در بخش ۰۲ **۳۰٫۴۴** داد. seqkit **احتمال خطاها** را میانگین می‌گیرد و سپس به Phred برمی‌گرداند؛ چند باز بد آن را بسیار پایین می‌کشد. هیچ‌کدام «نادرست» نیست؛ باید بدانید کدام را به کار برده‌اید.

### اسکریپت: خلاصه و گزینش ریدها

‏[fastq_quality.py](../99_scripts_data/04_Biopython_Seq/scripts/fastq_quality.py) همه‌ی ریدها را می‌خواند، می‌شمارد و ریدهایی با میانگین کیفیت دست‌کم Q را در یک فایل تازه می‌نویسد:

<div dir="ltr">

```python
def mean_quality(record):
    """Arithmetic mean of the Phred scores of one read."""
    q = record.letter_annotations["phred_quality"]
    return sum(q) / len(q)

n_reads = 0
n_bases = 0
good = []
with gzip.open(in_file, "rt") as f:
    for rec in SeqIO.parse(f, "fastq"):
        n_reads = n_reads + 1
        n_bases = n_bases + len(rec.seq)
        if mean_quality(rec) >= min_mean_q:
            good.append(rec)

n_written = SeqIO.write(good, out_file, "fastq")
```

</div>

<div dir="ltr">

```bash
python3 $P/fastq_quality.py fastq/minigut_sample2_R1.fastq.gz good.fastq 30
```

</div>

<div dir="ltr">

```text
reads: 24993
bases: 3773943
mean read length: 151.0
reads with mean Q >= 30: 24820 (99.3%)
```

</div>

- **۲۴٬۹۹۳ رید** و ۱۵۱ باز: همان عددهای `seqkit stats` در بخش ۰۲.
- ‏`SeqIO.write(فهرست رکوردها, فایل, فرمت)` همه را می‌نویسد و **شمار** نوشته‌ها را برمی‌گرداند.
- ‏`good` همه‌ی ریدهای خوب را در حافظه نگه می‌دارد. برای ۲۵ هزار رید مشکلی نیست؛ برای میلیون‌ها رید (کار واقعی) ابزارهای ویژه‌ی کنترل کیفیت (مانند fastp در بخش ۰۶، متاژنومیکس) به کار می‌روند.

‏`good.fastq` یک FASTQ درست است؛ `seqkit stats` آن را می‌فهمد:

<div dir="ltr">

```text
file        format  type  num_seqs    sum_len  min_len  avg_len  max_len
good.fastq  FASTQ   DNA     24,820  3,747,820      151      151      151
```

</div>

---

## ۶. نوشتن FASTA: `SeqRecord` و `SeqIO.write`

برای نوشتن یک توالی تازه (مانند پروتئین ترجمه‌شده)، باید آن را در یک **`SeqRecord`** بپیچیم تا نام و توضیح داشته باشد. اسکریپت [extract_gene.py](../99_scripts_data/04_Biopython_Seq/scripts/extract_gene.py):

<div dir="ltr">

```python
genome = SeqIO.read(genome_file, "fasta")
dna = genome.seq[start - 1:end]           # GFF coordinates -> Python slice
if strand == "-":
    dna = dna.reverse_complement()
protein = dna.translate(table=11, cds=True)

dna_rec = SeqRecord(dna, id=name, description=f"{genome.id}:{start}-{end}({strand})")
prot_rec = SeqRecord(protein, id=name, description=f"translated with table 11, {len(protein)} aa")
SeqIO.write(dna_rec, f"{name}.fna", "fasta")
SeqIO.write(prot_rec, f"{name}.faa", "fasta")
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `from Bio.SeqRecord import SeqRecord` | (در آغاز اسکریپت) |
| `SeqRecord(seq, id=…, description=…)` | یک رکورد بساز؛ `id` و `description` خط عنوان می‌شوند |
| ‏`SeqIO.write(رکورد, فایل, "fasta")` | بنویس؛ خط‌ها را خودش در ۶۰ نویسه می‌شکند |
| `f"{name}.faa"` | نام فایل از نام ژن؛ `.faa` = FASTA آمینواسیدی، `.fna` = نوکلئوتیدی |

پنج ورودی: ژنوم، نام، آغاز، پایان، رشته (همان ستون‌های GFF):

<div dir="ltr">

```bash
python3 $P/extract_gene.py ecoli_k12.fna rpoB 4181245 4185273 +
python3 $P/extract_gene.py ecoli_k12.fna gyrA 2336793 2339420 -
head -n 3 rpoB.faa
```

</div>

<div dir="ltr">

```text
rpoB: 4029 nt, 1342 aa, starts with MVYSYTEKKR
gyrA: 2628 nt, 875 aa, starts with MSDLAREITP
>rpoB translated with table 11, 1342 aa
MVYSYTEKKRIRKDFGKRPQVLDVPYLLSIQLDSFQKFIEQDPEGQYGLEAAFRSVFPIQ
SYSGNSELQYVSYRLGEPVFDVQECQIRGVTYSAPLRVKLRLVIYEREAPEGTVKDIKEQ
```

</div>

این `rpoB.faa` را می‌توانید در BLAST یا Clustal Omega (بخش ۰۰) بگذارید.

---

## ۷. سه اشتباه رایج (با پیام واقعی)

### اشتباه ۱: رشته‌ی نادرست
‏gyrA را با `+` (به جای `-`) بخواهید:

<div dir="ltr">

```bash
python3 $P/extract_gene.py ecoli_k12.fna gyrA 2336793 2339420 +
```

</div>

<div dir="ltr">

```text
Bio.Data.CodonTable.TranslationError: First codon 'TTA' is not a start codon
```

</div>

‏`TTA` مکمل معکوس `TAA` (کدون پایان gyrA) است: بی مکمل معکوس، از **پایان** ژن آغاز کرده‌ایم.

### اشتباه ۲: `SeqIO.read` برای فایل چندتوالی‌ای

<div dir="ltr">

```python
SeqIO.read(gzip.open("fastq/minigut_sample2_R1.fastq.gz", "rt"), "fastq")
```

</div>

<div dir="ltr">

```text
ValueError: More than one record found in handle
```

</div>

‏`read` تنها برای **یک** توالی است؛ برای بیشتر، `parse`.

### اشتباه ۳: باز کردن `.gz` بی `gzip`

<div dir="ltr">

```python
next(SeqIO.parse("fastq/minigut_sample2_R1.fastq.gz", "fastq"))
```

</div>

<div dir="ltr">

```text
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte
```

</div>

پایتون بایت‌های فشرده را مانند متن خواند. `gzip.open(…, "rt")` لازم است.

---

## ۸. جمع‌بندی

- `Seq`: `.complement()`، `.reverse_complement()`، `.transcribe()`، `.translate(table=11, cds=True)`.
- **باکتری: `table=11`؛ ژن کامل: `cds=True`.** `TranslationError` یعنی مختصات یا رشته را وارسی کنید.
- ‏`SeqIO.read` برای یک توالی؛ `SeqIO.parse` برای چندین (حلقه)؛ `SeqIO.write` برای نوشتن.
- ‏FASTQ: `rec.letter_annotations["phred_quality"]`؛ فایل `.gz` با `gzip.open(…, "rt")`.
- ‏`SeqRecord(seq, id=…, description=…)` برای ساختن رکورد تازه.

---

## کارت دستورهای این درس

| می‌خواهم… | Biopython |
| :--- | :--- |
| توالی بسازم | `from Bio.Seq import Seq` / `Seq("ATG…")` |
| مکمل معکوس | `s.reverse_complement()` |
| ترجمه‌ی ژن باکتری | `s.translate(table=11, cds=True)` |
| ترجمه تا نخستین پایان | `s.translate(table=11, to_stop=True)` |
| خواندن یک توالی | `SeqIO.read("f.fna", "fasta")` |
| خواندن چند توالی | `for rec in SeqIO.parse(f, "fastq"):` |
| باز کردن `.gz` | `import gzip` / `gzip.open(p, "rt")` |
| کیفیت هر باز | `rec.letter_annotations["phred_quality"]` |
| ساختن رکورد | `SeqRecord(seq, id="x", description="…")` |
| نوشتن | `SeqIO.write(records, "out.fa", "fasta")` |

---

<details>
<summary>📘 <b>برای کنجکاوها (اختیاری):</b> جدول‌های کد ژنتیکی و تبدیل فرمت</summary>

همه‌ی جدول‌های NCBI در Biopython هستند. برای نمونه، کدون‌های آغاز کد ۱۱:

<div dir="ltr">

```python
from Bio.Data import CodonTable
print(CodonTable.unambiguous_dna_by_id[11].start_codons)
```

</div>

<div dir="ltr">

```text
['TTG', 'CTG', 'ATT', 'ATC', 'ATA', 'ATG', 'GTG']
```

</div>

و تبدیل FASTQ به FASTA در یک خط: `SeqIO.convert("good.fastq", "fastq", "good.fasta", "fasta")`.
</details>

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| کتابخانه (library) | مجموعه‌ی کدهای آماده که با `import` به کار می‌روند |
| Biopython | کتابخانه‌ی پایتون برای داده‌های زیستی |
| `Seq` | شیء توالی با متدهای زیستی |
| `SeqRecord` | توالی + شناسه + توضیح (+ کیفیت) |
| `SeqIO` | بخش خواندن و نوشتن فرمت‌ها |
| کد ژنتیکی ۱۱ | جدول NCBI برای باکتری، آرکی و پلاستید |
| `TranslationError` | خطای Biopython هنگامی که ژن «کامل» نیست |

---

## منابع

### راهنما و مقاله
- ‏Biopython Tutorial & Cookbook، فصل‌های «Sequence objects» و «Sequence Input/Output»: https://biopython.org/docs/latest/Tutorial/
- Cock PJA, et al. (2009). Biopython: freely available Python tools for computational molecular biology and bioinformatics. *Bioinformatics* 25(11):1422–1423. https://doi.org/10.1093/bioinformatics/btp163
- جدول‌های کد ژنتیکی NCBI: https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi

### فیلم‌های آموزشی

**Coursera:**
- ‏Johns Hopkins University — *Python for Genomic Data Science* (هفته‌ی ۴، Biopython): https://www.coursera.org/learn/python-genomics

**edX:**
- UC San Diego — *Introduction to Genomic Data Science*: https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science

**YouTube:**
- Lana Dominkovic — *Bioinformatics with Biopython, Full Course*: https://www.youtube.com/watch?v=ocA2IMe7dpA
- Lana Dominkovic — *From DNA to RNA to Protein using Biopython*: https://www.youtube.com/watch?v=HzRyytIasFg

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. همه‌ی کدها در 2026-10-20 با Python 3.13.15 و Biopython 1.88 اجرا شدند.

</div>
