<div dir="rtl">

# درس: Python و Biopython برای داده‌های زیستی

**بخش:** `03_Python` · **ماژول:** `02_Biopython` · **پیش‌نیاز:** بخش ۰۱ (Bash، فرمت‌ها) · **زمان:** ۳ ساعت · **ابزار:** Python 3.13، Biopython 1.88 · **آخرین تست:** 2026-10-14

---

## ۱. مسئله

‏Bash برای شمردن، فیلتر کردن و زنجیر کردن ابزارها عالی است. ولی وقتی منطق پیچیده‌تر می‌شود، Bash به حد خودش می‌رسد. مثلاً: «هر CDS را از ژنوم بیرون بکش، اگر روی رشته‌ی منفی است مکمل معکوسش را بگیر، با کد ژنتیکی باکتری ترجمه کن، GC جایگاه سوم کدون را حساب کن، و ژن‌های غیرعادی را پیدا کن.» اینجا به یک زبان برنامه‌نویسی واقعی نیاز داریم.

‏**Python** زبان اصلی بیوانفورماتیک در کنار R است. **Biopython** کتابخانه‌ی استاندارد آن برای خواندن و نوشتن فرمت‌های زیستی، کار با توالی، و دسترسی به NCBI است.

این درس فرض می‌کند با مفاهیم پایه‌ی برنامه‌نویسی (متغیر، حلقه، شرط) آشنا هستید، یا آن‌ها را از منابع انتهای درس سریع مرور می‌کنید. تمرکز روی **کار واقعی با داده** است.

<div dir="ltr">

```bash
cd 03_Python/02_Biopython
# محیط: Python 3.11+ با biopython (در سرور دوره: محیط genomepipe_tools)
python3 -c "import Bio; print(Bio.__version__)"      # 1.88
G=../../01_Linux/99_scripts_data/data   # ژنوم و GFF مرجع E. coli (ماژول 01/01)
```

</div>

## ۲. مرور سریع Python برای داده‌ی زیستی

| ساختار | مثال | کاربرد |
| :--- | :--- | :--- |
| رشته (str) | `seq = "ATGGTT"` ؛ `seq[0:3]` ← `'ATG'` | توالی؛ **اندیس‌ها از ۰ و برش‌ها نیمه‌باز** (مثل BED) |
| لیست (list) | `lengths = [1342, 875]` | مجموعه‌ای مرتب |
| دیکشنری (dict) | `genome = {"NC_000913.3": seq}` | جستجو با کلید: شناسه ← توالی |
| مجموعه (set) | `seen = {"rpoB", "gyrA"}` | عضویت سریع، حذف تکرار |
| تابع | `def gc(s): return (s.count("G")+s.count("C"))/len(s)` | منطق قابل استفاده‌ی مجدد |

**مهم‌ترین تبدیل این درس:** GFF مختصات **مبنای ۱ و دوسر بسته** دارد. Python **مبنای ۰ و نیمه‌باز** است. پس ژنی که در GFF از `start` تا `end` است، در Python می‌شود:

<div dir="ltr">

```python
seq[start - 1 : end]
```

</div>

(همان قاعده‌ی تبدیل GFF ← BED در ماژول 01/03.)

## ‏۳. Biopython: اجزای اصلی

<div dir="ltr">

```python
from Bio import SeqIO
from Bio.Seq import Seq

rec = next(SeqIO.parse(f"{G}/ecoli_k12.fna", "fasta"))    # SeqRecord
print(rec.id, len(rec.seq))
```

</div>

<div dir="ltr">

```text
NC_000913.3 4641652
```

</div>

- ‏`SeqIO.parse(file, format)` یک **iterator** از `SeqRecord`ها برمی‌گرداند و برای فایل‌های چندتوالی‌ای و بزرگ مناسب است، چون همه را هم‌زمان در حافظه نمی‌گذارد. `SeqIO.read()` فقط برای فایل **تک‌توالی** است.
- فرمت‌های پشتیبانی‌شده: `fasta`، `fastq`، `genbank`، `embl` و ده‌ها فرمت دیگر. `SeqIO.convert()` تبدیل مستقیم انجام می‌دهد.
- ‏`Seq` توالی است با متدهای زیستی:

<div dir="ltr">

```python
rpoB = rec.seq[4181245 - 1 : 4185273]        # rpoB روی رشته‌ی +
prot = rpoB.translate(table=11)              # کد ژنتیکی ۱۱ = باکتری‌ها
print(len(rpoB), prot[:10], prot[-3:], len(prot))
```

</div>

<div dir="ltr">

```text
4029 MVYSYTEKKR IE* 1343
```

</div>

۱۳۴۲ اسیدآمینه به‌علاوه‌ی `*` (کدون پایان). همان طول UniProt `P0A8V2` در بخش ۰۰.

<div dir="ltr">

```python
gyrA = rec.seq[2336793 - 1 : 2339420].reverse_complement()   # gyrA روی رشته‌ی −
print(gyrA[:3], gyrA[-3:], len(gyrA.translate(table=11)) - 1)
```

</div>

<div dir="ltr">

```text
ATG TAA 875
```

</div>

## ۴. کار عملی: جدول همه‌ی ژن‌های پروتئین‌ساز

اسکریپت [scripts/cds_table.py](../99_scripts_data/02_Biopython/scripts/cds_table.py) همه‌ی CDSها را از FASTA + GFF استخراج، ترجمه و خلاصه می‌کند. ساختارش الگوی یک **اسکریپت خط فرمان خوب** است:
- ‏`argparse` برای ورودی‌ها و `--help`
- تابع‌های کوچک (`parse_attributes`، `read_cds`، `gc`)
- بلوک `if __name__ == "__main__":` تا هم اجراشدنی باشد و هم قابل import

<div dir="ltr">

```bash
python3 scripts/cds_table.py $G/ecoli_k12.fna $G/ecoli_k12.gff -o cds_table.tsv
head -3 cds_table.tsv ; wc -l < cds_table.tsv
```

</div>

<div dir="ltr">

```text
gene	locus_tag	protein_id	start	end	strand	length_nt	length_aa	gc	gc3	ok
thrL	b0001	NP_414542.1	190	255	+	66	21	0.5152	0.6364	True
thrA	b0002	NP_414543.1	337	2799	+	2463	820	0.5307	0.5761	True
4301
```

</div>

‏**۴٬۳۰۰ CDS** (به‌علاوه‌ی سرستون)، دقیقاً برابر با تعداد پروتئین‌های `protein.faa` در بخش ۰۰. اجرا نیم ثانیه طول کشید.

نکته‌های پیاده‌سازی:
- ‏CDSهایی که در GFF چند سطر با یک `ID` دارند، مثل ژن‌هایی با جابه‌جایی چارچوب برنامه‌ریزی‌شده (programmed frameshift)، **ادغام** می‌شوند.
- ژن‌های کاذب (`pseudo=true`) کنار گذاشته می‌شوند.
- ستون `ok` بررسی می‌کند که ترجمه با کدون پایان تمام شود و **هیچ کدون پایان داخلی** نداشته باشد.

### یافته‌ی غیرمنتظره: سه ژن «خراب»

<div dir="ltr">

```bash
awk -F'\t' '$11=="False"' cds_table.tsv | cut -f1-3,8
```

</div>

<div dir="ltr">

```text
fdnG	b1474	NP_415991.1	1015
fdoG	b3894	NP_418330.1	1016
fdhF	b4079	NP_418503.1	715
```

</div>

این سه ژن **کدون پایان داخلی** دارند. باگ کد است؟ نه. هر سه **فرمات دهیدروژناز** هستند و GFF برایشان یک ویژگی خاص دارد:

<div dir="ltr">

```bash
grep -P '\tCDS\t' $G/ecoli_k12.gff | grep 'gene=fdnG;' | grep -oE 'transl_except=[^;]+'
```

</div>

<div dir="ltr">

```text
transl_except=(pos:1547986..1547988%2Caa:Sec)
```

</div>

کدون **TGA** در این موقعیت به‌جای «پایان»، **سلنوسیستئین (Sec)**، اسیدآمینه‌ی بیست‌ویکم، را کد می‌کند. این کار به یک ساختار RNA پایین‌دست (SECIS) نیاز دارد. محاسبه‌ی ما دقیقاً همین را تأیید می‌کند: کدون پایان داخلی *fdnG* در اسیدآمینه‌ی **۱۹۶** است، یعنی 1,547,401 + 195 × 3 = **1,547,986**.

**درس:** «خطای» یک بررسی خودکار گاهی **زیست‌شناسی واقعی** است. قبل از حذف داده‌ی «غیرعادی»، آنوتیشن را بخوانید.

## ۵. خلاصه‌های زیستی از جدول

<div dir="ltr">

```python
import csv, statistics as st
rows = list(csv.DictReader(open("cds_table.tsv"), delimiter="\t"))
gc = [float(r["gc"]) for r in rows]
print(len(rows), round(st.mean(gc), 4), round(st.stdev(gc), 4))
```

</div>

<div dir="ltr">

```text
4300 0.5081 0.0524
```

</div>

میانگین GC ژن‌ها (۵۰٫۸٪) تقریباً برابر GC کل ژنوم (۵۰٫۷۹٪) است.

**کدون‌های آغاز و پایان** (از توالی هر CDS):
| | تعداد |
| :--- | ---: |
| آغاز ATG / GTG / TTG | 3,876 / 338 / 80 (به‌علاوه‌ی ۴ ATT و ۲ CTG) |
| پایان TAA / TGA / TAG | 2,753 / 1,242 / 305 |

حدود ۱۰٪ ژن‌ها با GTG یا TTG شروع می‌شوند. در سلول، ریبوزوم کدون آغاز را همیشه با tRNA آغازگر (fMet) می‌خواند، پس پروتئین واقعی با **متیونین** شروع می‌شود. ولی `translate()` در Biopython این را **خودبه‌خود نمی‌داند**: هم `table=1` و هم `table=11` اولین GTG را **V** ترجمه می‌کنند. فقط با `cds=True` کدون اول (اگر در جدول، کدون آغاز مجاز باشد) به `M` تبدیل می‌شود:

<div dir="ltr">

```python
s = Seq("GTGAAAAAGATGCAG")          # ابتدای yaaX، که با GTG شروع می‌شود
s.translate(table=11)              # 'VKKMQ'
s.translate(table=11, cds=True)    # 'MKKMQ'
s.translate(table=1, cds=True)     # TranslationError: First codon 'GTG' is not a start codon
```

</div>

‏`cds=True` علاوه بر این بررسی می‌کند که طول مضرب ۳ باشد، کدون آخر پایان باشد و کدون پایان داخلی نباشد، و `*` انتهایی را حذف می‌کند. rpoB با ATG شروع می‌شود، برای همین ترجمه‌ی بخش ۳ بدون `cds=True` هم با `M` شروع شد.

### دسترسی به NCBI با Bio.Entrez

<div dir="ltr">

```python
from Bio import Entrez, SeqIO
Entrez.email = "you@university.edu"        # الزامی طبق قوانین NCBI
h = Entrez.efetch(db="protein", id="NP_418414.1", rettype="fasta", retmode="text")
rec = SeqIO.read(h, "fasta"); h.close()
print(rec.id, len(rec.seq))
```

</div>

<div dir="ltr">

```text
NP_418414.1 1342
```

</div>

‏NCBI بدون API key حداکثر **۳ درخواست در ثانیه** را می‌پذیرد. در حلقه‌ها `time.sleep()` بگذارید، یا یک API key رایگان بگیرید (`Entrez.api_key`).

## ۶. دام‌ها (Pitfalls)

| دام | چرا مشکل است | راه درست |
| :--- | :--- | :--- |
| ‏`seq[start:end]` با مختصات GFF | ‏off-by-one: باز اول از دست می‌رود | `seq[start-1:end]` |
| فراموش کردن reverse complement برای رشته‌ی − | ترجمه‌ی بی‌معنی | `if strand == "-": s = s.reverse_complement()` |
| ترجمه‌ی CDS بدون `cds=True` | ژن‌های GTG/TTG با V/L شروع می‌شوند، نه M | `translate(table=11, cds=True)` |
| ‏`table=1` برای باکتری | ‏GTG و ATT در کد ۱ کدون آغاز نیستند؛ `cds=True` خطا می‌دهد | `table=11` |
| حذف خودکار ژن‌های «خراب» | سلنوپروتئین‌ها، frameshiftهای برنامه‌ریزی‌شده | آنوتیشن را بخوانید (`transl_except`، `exception`) |
| ‏`SeqIO.read` برای فایل چندتوالی | خطا | `SeqIO.parse` |
| خواندن کل FASTQ چندگیگی در یک لیست | حافظه تمام می‌شود | iterator (`for rec in SeqIO.parse(...)`) |
| بدون `Entrez.email` و بدون مکث | ‏NCBI درخواست‌ها را مسدود می‌کند | ایمیل + حداکثر ۳ درخواست در ثانیه |

## ۷. جمع‌بندی
- ‏Biopython: `SeqIO` برای ورودی و خروجی، `Seq` برای ترجمه و مکمل معکوس، `Entrez` برای NCBI.
- قاعده‌ی مختصات GFF ← Python: `[start-1:end]`؛ رشته‌ی منفی: reverse complement؛ باکتری: `table=11`.
- اسکریپت قابل استفاده = `argparse` + تابع‌های کوچک + `if __name__ == "__main__"`.
- استثناهای زیستی (سلنوسیستئین) را از باگ تشخیص دهید. بعضی «خطا»ها زیست‌شناسی‌اند.

---

## منابع

### مقاله و مستندات
- Cock PJA, et al. (2009). Biopython: freely available Python tools for computational molecular biology and bioinformatics. *Bioinformatics* 25(11):1422–1423. https://doi.org/10.1093/bioinformatics/btp163
- Biopython Tutorial & Cookbook: https://biopython.org/docs/latest/Tutorial/
- راهنمای E-utilities در NCBI (قوانین استفاده و API key): https://www.ncbi.nlm.nih.gov/books/NBK25497/
- آموزش رسمی Python: https://docs.python.org/3/tutorial/
- Software Carpentry — *Programming with Python*: https://swcarpentry.github.io/python-novice-inflammation/

### ویدیوهای آموزشی
- Lana Dominkovic — *Bioinformatics with Biopython, Full Course*: https://www.youtube.com/watch?v=ocA2IMe7dpA
- Lana Dominkovic — *Accessing NCBI databases and tools with Biopython (Entrez)*: https://www.youtube.com/watch?v=tl4xqdfIBh0
- Lana Dominkovic — *From DNA to RNA to Protein using Biopython*: https://www.youtube.com/watch?v=HzRyytIasFg
- rebelScience — *Bioinformatics in Python: Intro*: https://www.youtube.com/watch?v=3joOQ3A3KBQ

> لینک‌ها در تاریخ 2026-10-14 بررسی شدند (`_tools/check_links.sh`).

</div>
