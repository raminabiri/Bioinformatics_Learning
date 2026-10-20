<div dir="rtl">

# پاسخ تشریحی: Python و Biopython

> اجرا شده در 2026-10-14 با Python 3.13 و Biopython 1.88 روی `NC_000913.3` (ژنوم و GFF ماژول 01/01). اعداد تمرین ۱، ۲، ۳ و ۵ برای شما هم دقیقاً همین‌اند. اعداد NCBI در تمرین ۴ با زمان تغییر می‌کنند.

<div dir="ltr">

```bash
cd 03_Python/02_Biopython
G=../../01_Linux/99_scripts_data/data
```

</div>

---

## تمرین ۱: ستون `product`

### ۱.۱ سه خط تغییر

<div dir="ltr">

```diff
                             "gene": a.get("gene", ""), "locus_tag": a.get("locus_tag", ""),
-                            "protein_id": a.get("protein_id", "")}
+                            "protein_id": a.get("protein_id", ""),
+                            "product": a.get("product", "")}
 ...
-                "length_nt", "length_aa", "gc", "gc3", "ok"])
+                "length_nt", "length_aa", "gc", "gc3", "ok", "product"])
 ...
-                    len(nt), len(prot.rstrip("*")), round(gc(nt), 4), round(gc(third), 4), ok])
+                    len(nt), len(prot.rstrip("*")), round(gc(nt), 4), round(gc(third), 4), ok, c["product"]])
```

</div>

هر سه جا لازم‌اند: خواندن از GFF (دیکشنری `cds`)، سرستون، و ردیف خروجی. اشتباه رایج: فقط سرستون را اضافه کنید. آن وقت ستون‌ها یکی جابه‌جا نمی‌شوند ولی **سرستون ۱۲ ستون و داده ۱۱ ستون** دارد و pandas یا R بی‌صدا ستون آخر را `NaN` می‌خوانند.

### ۱.۲ کاراکتر `%`

<div dir="ltr">

```bash
# cds_table_product.py = copy of scripts/cds_table.py with the three changes above
python3 cds_table_product.py $G/ecoli_k12.fna $G/ecoli_k12.gff -o cds_prod.tsv
awk -F'\t' 'NR>1 && $12~/%/' cds_prod.tsv | wc -l
grep -oE '%[0-9A-F]{2}' cds_prod.tsv | sort | uniq -c
awk -F'\t' '$1=="ilvI"' cds_prod.tsv | cut -f1,12
```

</div>

<div dir="ltr">

```text
156
    169 %2C
ilvI	acetolactate synthase/acetohydroxybutanoate synthase%2C catalytic subunit
```

</div>

**۱۵۶ سطر** و همه‌ی موارد `%2C` هستند، یعنی **ویرگول**. طبق مشخصات GFF3، کاراکترهایی که در ستون ۹ معنای ساختاری دارند (`;` `=` `&` `,` و tab) باید **percent-encode** شوند. ویرگول جداکننده‌ی چند مقدار است (مثل `Dbxref=A,B`)، پس ویرگولِ داخل متن به `%2C` تبدیل شده است. این باگ فایل نیست؛ قرارداد فرمت است.

### ۱.۳ رمزگشایی

<div dir="ltr">

```python
from urllib.parse import unquote

def parse_attributes(col9):
    """'ID=x;Name=y' -> {'ID': 'x', 'Name': 'y'} (values percent-decoded, GFF3 spec)"""
    return {k: unquote(v) for k, v in (item.split("=", 1) for item in col9.strip().split(";") if "=" in item)}
```

</div>

<div dir="ltr">

```text
0                       ← سطرهای دارای % بعد از اصلاح
ilvI	acetolactate synthase/acetohydroxybutanoate synthase, catalytic subunit
```

</div>

ده ستون اول خروجی تغییری نکرد (`cmp` بدون اختلاف)، چون `gene`، `locus_tag` و `protein_id` هیچ کاراکتر رمزشده‌ای ندارند.

نکته‌ها:
- ترتیب مهم است: **اول** با `;` و `=` جدا کنید، **بعد** رمزگشایی کنید. اگر اول `unquote` کنید، یک `%3B` (`;`) واقعی داخل متن، رشته را در جای غلط می‌شکند.
- ویرگول حالا داخل ستون است. چون فایل خروجی **TSV** است مشکلی نیست، ولی اگر CSV بنویسید باید quote شود (ماژول `csv` این را خودش انجام می‌دهد؛ `print(",".join(...))` انجام نمی‌دهد).
- کتابخانه‌هایی مثل `gffutils` و `BCBio.GFF` این کار را خودشان می‌کنند. ولی تا وقتی خودتان پارسر ننوشته‌اید، نمی‌دانید چه چیزی را از شما پنهان می‌کنند.

---

## تمرین ۲: ژن‌هایی با GC غیرعادی

<div dir="ltr">

```bash
python3 scripts/gc_outliers.py cds_table.tsv --min-aa 100 --z 2 --top 10
```

</div>

<div dir="ltr">

```text
CDS >= 100 aa: 3768  mean GC = 0.5153  sd = 0.0448
low-GC outliers (z < -2.0): 170   high-GC outliers (z > 2.0): 16

10 lowest-GC genes:
gene	locus_tag	start	length_aa	gc	z
waaS	b3629	3804181	311	0.2682	-5.51
ydcD	b1457	1529922	160	0.2733	-5.40
yfdI	b2352	2469131	443	0.2755	-5.35
ybbC	b0498	527581	122	0.3062	-4.66
ykfM	b4586	238257	159	0.3063	-4.66
ymfE	b1138	1197533	234	0.3092	-4.59
waaU	b3623	3798239	357	0.3101	-4.57
ybfB	b0702	733776	108	0.3119	-4.53
yfjW	b2642	2773318	567	0.3122	-4.53
ybcV	b0558	579184	136	0.3163	-4.44

most common gene prefixes among low-GC outliers: [('waa', 8), ('yfj', 5), ('yeh', 5), ('ybc', 4), ('yqe', 4), ('wbb', 4)]
```

</div>

### ۲.۱ چرا ژن‌های کوتاه حذف شدند؟
‏GC یک **نسبت** است و واریانس نسبت با کم شدن طول زیاد می‌شود (تقریباً p(1−p)/n). یک ژن ۲۰ اسیدآمینه‌ای (۶۳ باز) فقط به‌خاطر شانس می‌تواند ۱۰ درصد از میانگین فاصله بگیرد. با آستانه‌ی ۱۰۰ اسیدآمینه، ۳٬۷۶۸ ژن از ۴٬۳۰۰ می‌مانند و انحراف معیار به **۰٫۰۴۴۸** می‌رسد (در کل ژن‌ها ۰٫۰۵۲۴، درس بخش ۵). یعنی پراکندگی کمتر شد و دورافتاده‌ها واقعی‌ترند.

### ۲.۲ و ۲.۳ اعداد
- میانگین **0.5153**، انحراف معیار **0.0448**.
- **۱۷۰ ژن کم‌GC** در برابر **۱۶ ژن پرGC**. اگر توزیع نرمال بود، هر دم حدود ۲٫۳٪ یعنی ~۸۶ ژن داشت. دم پایین **دو برابر** انتظار است و دم بالا **یک‌پنجم**. توزیع **چوله به چپ** است؛ پس یک فرایند زیستی ژن‌های کم‌GC را به ژنوم اضافه کرده است.

### ۲.۴ خانواده‌ها
- ‏`waa` (۸ ژن) و `wbb` (۴ ژن): بیوسنتز **هسته‌ی LPS و آنتی‌ژن O**. این ناحیه‌ها در *E. coli* بین سویه‌ها بسیار متغیرند و با **انتقال افقی ژن (HGT)** جابه‌جا می‌شوند. GC پایین نشانه‌ی منشأ از گونه‌ای با ژنوم AT‌دارتر است.
- بسیاری از ژن‌های `y…` (نام موقت برای ژن با عملکرد نامعلوم) روی **پروفاژها** هستند. مثلاً موقعیت‌ها را در EcoCyc ببینید: *ymfE* در پروفاژ e14، *ybcV* در DLP12، *yfjW* در CP4-57 و *yfdI* در CPS-53. *yfdI* یک گلیکوزیل‌ترانسفراز «تغییردهنده‌ی سروتایپ» است؛ فاژ با آن آنتی‌ژن O میزبان را عوض می‌کند.
- **۳ حرف اول** فقط یک تقریب است: `yfj` یعنی «ژن ناشناخته در دقیقه‌ی ~۵۷ نقشه‌ی ژنتیکی»، نه یک اپرون. در کار واقعی خوشه‌ها را با **مجاورت روی ژنوم** پیدا کنید (ژن‌های کم‌GC پشت سر هم).

### ۲.۵ پروتئین‌های ناشناخته

<div dir="ltr">

```python
f = lambda rs: sum("uncharacterized" in r["product"].lower() for r in rs)
# all >=100 aa: 55 / 3768 ;  low-GC: 18 / 170
```

</div>

| گروه | `uncharacterized` | درصد |
| :--- | ---: | ---: |
| همه‌ی CDS ≥ ۱۰۰ aa | 55 / 3,768 | ۱٫۵٪ |
| ژن‌های کم‌GC (z < −2) | 18 / 170 | **۱۰٫۶٪** |

ژن‌های ناشناخته در گروه کم‌GC **۷ برابر** غنی‌ترند. این الگوی شناخته‌شده‌ی DNA اکتسابی است: ژن‌های فاژی و جزیره‌های ژنومی کمتر مطالعه شده‌اند. از ۱۰ ژن جدول بالا، ۵ تا `uncharacterized` هستند.

**اشتباهات رایج:**
- ‏z-score را روی **همه‌ی** ژن‌ها حساب کنید و بعد فیلتر طول کنید. میانگین و sd باید روی همان مجموعه‌ای باشد که دورافتاده را در آن جستجو می‌کنید.
- ‏GC پایین را **اثبات** HGT بدانید. این فقط یک سیگنال است. ژن‌های اکتسابی قدیمی به مرور به ترکیب ژنوم میزبان نزدیک می‌شوند (ameliorate) و دیگر دیده نمی‌شوند. ابزارهای واقعی (مثلاً IslandPath-DIMOB در بخش ۰۷) GC را با سوگیری کدون و مجاورت به اینتگراز/tRNA ترکیب می‌کنند.

---

## تمرین ۳: `translate()` و `cds=True`

### ۳.۱ کدون‌های آغاز و پایان

<div dir="ltr">

```python
from collections import Counter
from codon_usage import cds_sequences      # run with PYTHONPATH=scripts
G = "../../01_Linux/99_scripts_data/data"
seqs = list(cds_sequences(f"{G}/ecoli_k12.fna", f"{G}/ecoli_k12.gff"))
print(Counter(s[:3] for _, s in seqs).most_common())
print(Counter(s[-3:] for _, s in seqs).most_common())
print([(g, s[:3]) for g, s in seqs if s[:3] not in ("ATG", "GTG", "TTG")])
```

</div>

<div dir="ltr">

```text
[('ATG', 3876), ('GTG', 338), ('TTG', 80), ('ATT', 4), ('CTG', 2)]
[('TAA', 2753), ('TGA', 1242), ('TAG', 305)]
[('pcnB', 'ATT'), ('ymcF', 'ATT'), ('ynfQ', 'ATT'), ('infC', 'ATT'), ('hda', 'CTG'), ('yfjD', 'CTG')]
```

</div>

### ۳.۲ دو جدول ژنتیکی

<div dir="ltr">

```python
from Bio.Seq import Seq
from Bio.Data import CodonTable
for t in (11, 1):
    bad = Counter()
    for g, s in seqs:
        try:
            Seq(s).translate(table=t, cds=True)
        except Exception as e:
            bad[" ".join(str(e).split()[:2])] += 1
    print(t, sum(bad.values()), bad)
print(CodonTable.unambiguous_dna_by_id[11].start_codons)
print(CodonTable.unambiguous_dna_by_id[1].start_codons)
```

</div>

<div dir="ltr">

```text
11 3 Counter({'Extra in': 3})
1 345 Counter({'First codon': 342, 'Extra in': 3})
['TTG', 'CTG', 'ATT', 'ATC', 'ATA', 'ATG', 'GTG']
['TTG', 'CTG', 'ATG']
```

</div>

- ‏**`table=11`:** فقط ۳ خطا، همه `Extra in frame stop codon`.
- ‏**`table=1`:** ۳۴۵ خطا = ۳۳۸ ژن GTG + ۴ ژن ATT (کدون آغاز مجاز در کد ۱ فقط TTG، CTG و ATG است) + همان ۳ ژن.

یعنی `cds=True` یک **آزمون کیفیت رایگان** است: هم کد ژنتیکی اشتباه را لو می‌دهد، هم مختصات غلط (frame یا رشته‌ی اشتباه تقریباً همیشه کدون پایان داخلی می‌سازد).

### ۳.۳ سه ژن مشکل‌دار
‏*fdnG*، *fdoG* و *fdhF*، همان سه سلنوپروتئین درس (بخش ۴). **نباید حذف شوند**: پروتئین‌های واقعی و کارکردی‌اند. درست این است که کدون TGA در موقعیت `transl_except` با `U` (سلنوسیستئین) جایگزین شود. مثلاً قبل از ترجمه، برای این ژن‌ها `*` داخلی را با `U` عوض کنید. NCBI در `protein.faa` همین کار را کرده است.

### ۳.۴ خطای `rstrip("*")`
- **۳۳۸ پروتئین با V شروع می‌شوند و ۸۰ تا با L**، به جای M. در سلول، کدون آغاز همیشه با fMet-tRNA خوانده می‌شود.
- سه سلنوپروتئین یک `*` **داخلی** دارند. `rstrip` فقط `*` انتهایی را برمی‌دارد.

دردسرها:
- **پروتئومیکس:** پپتید N-ترمینال در جستجوی طیف جرمی پیدا نمی‌شود.
- **مقایسه با UniProt یا محاسبه‌ی هویت:** یک اختلاف کاذب در هر پروتئین.
- **ابزارها:** بعضی ابزارها (مثلاً InterProScan) توالی دارای `*` را نمی‌پذیرند و خطا می‌دهند.

راه درست: `seq.translate(table=11, cds=True)` داخل `try/except`، و ثبت جداگانه‌ی استثناها.

### ‏۳.۵ *infC* و ATT
‏IF3 (محصول *infC*) خودش ریبوزوم را وادار می‌کند آغاز ترجمه از کدون‌های **غیرمتعارف** را رد کند. کدون ATT ژن *infC* یک **حلقه‌ی بازخورد منفی** می‌سازد: وقتی IF3 زیاد است، ترجمه‌ی mRNA خودش را سرکوب می‌کند. وقتی کم است، ATT آسان‌تر خوانده می‌شود و IF3 بیشتری ساخته می‌شود. در آزمایش‌ها، جایگزینی ATT با ATG این تنظیم را از بین می‌برد. (منبع: صفحه‌ی *infC* در EcoCyc و UniProt `P69222`.) پس کدون آغاز «غیرعادی» این‌جا هم زیست‌شناسی است، نه خطای آنوتیشن.

---

## تمرین ۴: NCBI با `Bio.Entrez`

<div dir="ltr">

```bash
python3 scripts/entrez_tour.py --email you@uni.edu
python3 scripts/entrez_tour.py --email you@uni.edu --gene gyrA --term fluoroquinolone
```

</div>

<div dir="ltr">

```text
== 1. Taxonomy
taxid=511145  name=Escherichia coli str. K-12 substr. MG1655  rank=no rank
== 2. Nucleotide (RefSeq complete genome)
records: 14  (NC_: 1)
NC_000913.3  length=4641652  Escherichia coli str. K-12 substr. MG1655, complete genome
== 3. Gene
GeneID=948488  symbol=rpoB  RNA polymerase subunit beta  NC_000913.3:4181245-4185273
== 4. PubMed
PubMed hits for "rpoB AND rifampicin resistance": 1885
...
GeneID=946614  symbol=gyrA  DNA gyrase subunit A  NC_000913.3:2339420-2336793
PubMed hits for "gyrA AND fluoroquinolone": 2900
```

</div>

(اعداد در تاریخ 2026-10-14.)

### ۴.۱ چهارده رکورد
فیلتر `refseq[filter]` همه‌ی رکوردهای RefSeq را برمی‌گرداند و دو نوع دارد:
- ‏**`NC_`**: توالی مرجع **منتخب** (curated) که NCBI نگه می‌دارد. فقط یکی: `NC_000913.3`.
- ‏**`NZ_`** (۱۳ رکورد): نسخه‌ی RefSeq از ژنوم‌هایی که آزمایشگاه‌های دیگر از همین سویه دوباره توالی‌یابی کرده‌اند (مثلاً `NZ_CP032679.1`). طول‌هایشان کمی فرق دارد (۴٬۵۲۶٬۰۷۴ تا ۴٬۶۷۵٬۱۸۸)، چون سویه‌های آزمایشگاهی جهش، حذف و جابه‌جایی IS جمع کرده‌اند.

برای انتخاب مرجع: در Python با پیشوند `NC_` فیلتر کنید (کاری که اسکریپت می‌کند)، یا با **NCBI Datasets** و گزینه‌ی `--reference` (بخش ۰۰). درس کلی: **تعداد نتایج کوئری را همیشه چاپ کنید**. کدی که فقط `IdList[0]` را برمی‌دارد، به‌خاطر ترتیب نتایج ممکن است بی‌صدا یک ژنوم غیرمرجع را بردارد. در اجرای ما `NC_000913.3` اول آمد، ولی NCBI ترتیب ثابتی تضمین نمی‌کند.

### ۴.۲ قرارداد مختصات در Entrez Gene
| ژن | GFF | ‏Entrez `ChrStart`–`ChrStop` (خام) |
| :--- | :--- | :--- |
| *rpoB* (+) | 4181245–4185273 | 4181244–4185272 |
| *gyrA* (−) | 2336793–2339420 | **2339419–2336792** |

دو تفاوت:
1. ‏Entrez مختصات **مبنای ۰** می‌دهد (به همین خاطر اسکریپت `+1` می‌کند).
2. برای ژن رشته‌ی منفی، **start > stop** است. رشته را از ترتیب این دو می‌فهمیم.

<div dir="ltr">

```python
def entrez_to_gff(chr_start, chr_stop):
    """Entrez Gene GenomicInfo (0-based; start > stop on minus strand) -> GFF (1-based, start <= end, strand)."""
    a, b = int(chr_start), int(chr_stop)
    return min(a, b) + 1, max(a, b) + 1, "-" if a > b else "+"

entrez_to_gff("2339419", "2336792")    # (2336793, 2339420, '-')  = GFF
```

</div>

اشتباه رایج: `seq[ChrStart:ChrStop]` برای gyrA یک **رشته‌ی خالی** برمی‌گرداند (چون start > stop)، بدون هیچ خطایی.

### ۴.۳ PubMed
۱٬۸۸۵ و ۲٬۹۰۰ مقاله در 2026-10-14. PubMed هر روز رشد می‌کند و الگوریتم تطبیق اصطلاحات (Automatic Term Mapping) هم گاهی عوض می‌شود. پس عدد بدون تاریخ و **کوئری دقیق** قابل تکرار نیست. در روش‌های مقاله، کوئری کامل و تاریخ جستجو را بنویسید.

### ۴.۴ اسکریپت گیر می‌کند
در تست ما هم پیش آمد: یک درخواست به `eutils.ncbi.nlm.nih.gov` بدون پاسخ ماند و اسکریپت تا ابد منتظر ماند. پیش‌فرض Python برای socket **بدون timeout** است.

<div dir="ltr">

```python
import socket
socket.setdefaulttimeout(30)     # stalled request -> error after 30 s
Entrez.max_tries = 5             # Biopython retries failed requests
```

</div>

با این دو خط، درخواستی که گیر کرده خطا می‌دهد و Biopython دوباره امتحان می‌کند. دلیل‌های دیگر: نبودن `Entrez.email`، بیش از ۳ درخواست در ثانیه (خطای HTTP 429)، یا خروجی بافرشده‌ی Python وقتی با `| tail` اجرا می‌کنید (از `python3 -u` استفاده کنید تا پیشرفت را ببینید).

---

## تمرین ۵: سوگیری کدون در ژن‌های پربیان

<div dir="ltr">

```bash
python3 scripts/codon_usage.py $G/ecoli_k12.fna $G/ecoli_k12.gff
python3 scripts/codon_usage.py $G/ecoli_k12.fna $G/ecoli_k12.gff --genes '^rp[lsm][A-Z]$'
```

</div>

<div dir="ltr">

```text
genes: 4300  codons (no start/stop): 1325736  mean gc3: 0.544
rarest: TGA 0.00, AGG 1.09, AGA 1.96, CGA 3.51, CTA 3.90
commonest: CTG 53.6, GAA 40.0, GCG 34.2, AAA 33.9, GAT 32.2
Leu CTG 49.9%  CTT 10.3%  CTC 10.5%  CTA 3.6%  TTA 12.9%  TTG 12.8%
Arg CGT 38.4%  CGC 40.2%  CGA 6.3%  CGG 9.7%  AGA 3.5%  AGG 2.0%

genes: 54  codons (no start/stop): 7074  mean gc3: 0.494
rarest: CTA 0.14, ATA 0.14, CGA 0.28, CCC 0.28, CGG 0.42
commonest: AAA 67.7, CGT 59.4, CTG 59.1, GCT 51.2, GAA 49.2
Leu CTG 83.9%  CTT 4.8%  CTC 4.0%  CTA 0.2%  TTA 3.0%  TTG 4.0%
Arg CGT 67.4%  CGC 31.1%  CGA 0.3%  CGG 0.5%  AGA 0.6%  AGG 0.0%
```

</div>

### ۵.۱ نادر و پرکاربرد
- نادرترین کدون‌های واقعی (غیر از TGA): **AGG (۱٫۰۹‰)**، **AGA (۱٫۹۶‰)** و CGA (۳٫۵۱‰). هر سه آرژینین‌اند.
- پرکاربردترین: **CTG (۵۳٫۶‰)**، GAA (۴۰٫۰‰) و GCG (۳۴٫۲‰).
- ‏CTG به‌تنهایی نیمی از لوسین‌ها (۴۹٫۹٪) را کد می‌کند، با اینکه لوسین شش کدون دارد. توزیع یکنواخت ۱۶٫۷٪ بود.

### ۵.۲ چرا TGA تقریباً صفر و نه دقیقاً صفر؟
کدون اول و آخر را کنار گذاشتیم، پس هر TGA باقی‌مانده **داخلی** است. دقیقاً ۳ تا وجود دارد: کدون‌های **سلنوسیستئین** در *fdnG*، *fdoG* و *fdhF* (۳ / ۱٬۳۲۵٬۷۳۶ × ۱۰۰۰ = ۰٫۰۰۲‰). کدون‌های TAA و TAG داخلی اصلاً وجود ندارند و در فهرست نیستند. این یک **بررسی سلامت** است: اگر کد شما ده‌ها کدون پایان داخلی شمرد، رشته یا frame را اشتباه گرفته‌اید.

### ۵.۳ ریبوزومی در برابر همه
| شاخص | همه‌ی ژن‌ها (۴٬۳۰۰) | پروتئین‌های ریبوزومی (۵۴) |
| :--- | ---: | ---: |
| سهم CTG از Leu | ۴۹٫۹٪ | **۸۳٫۹٪** |
| سهم AGG از Arg | ۲٫۰٪ | **۰٫۰٪** (هیچ AGG در ۷٬۰۷۴ کدون) |
| سهم CGT از Arg | ۳۸٫۴٪ | **۶۷٫۴٪** |
| میانگین GC3 | 0.544 | **0.494** |

### ۵.۴ تفسیر
ژن‌های ریبوزومی جزو **پربیان‌ترین** ژن‌های سلول‌اند. در این ژن‌ها، انتخاب طبیعی **سرعت و دقت ترجمه** را بهینه کرده است. پس کدون‌هایی ترجیح داده می‌شوند که tRNA مکملشان **فراوان** است (مثلاً CTG با tRNA-Leu اصلی، CGT با tRNA-Arg2) و کدون‌هایی که tRNA کمیاب دارند (AGG، AGA، CTA، CGA) تقریباً حذف شده‌اند. این همان مشاهده‌ی کلاسیک Ikemura (1981، [doi:10.1016/0022-2836(81)90363-6](https://doi.org/10.1016/0022-2836%2881%2990363-6)) و پایه‌ی شاخص **CAI** است (Sharp & Li 1987، [doi:10.1093/nar/15.3.1281](https://doi.org/10.1093/nar/15.3.1281)).

چرا GC3 **کمتر** شد؟ چون ترجیح کدون همیشه به سمت G/C نیست. در کنار CTG، کدون‌های بهینه‌ی بسیاری از اسیدهای آمینه به **A یا T** ختم می‌شوند: AAA (Lys)، CGT (Arg)، GCT (Ala)، GAA (Glu). پس GC3 پایین در این‌جا نشانه‌ی **انتخاب برای tRNA**، نه جهش‌پذیری است. درس: GC3 را بدون نگاه به کدون‌های تک‌تک تفسیر نکنید. GC3 پایین در تمرین ۲ (HGT) و GC3 پایین در ژن‌های ریبوزومی **دو دلیل کاملاً متفاوت** دارند.

محدودیت: ۵۴ ژن و ۷٬۰۷۴ کدون نمونه‌ی کوچکی است. ۰٪ AGG یعنی «کمتر از حدود ۱ در ۷۰۰۰»، نه «ممنوع».

### ۵.۵ بیان پروتئین انسانی
‏AGG و AGA در انسان کدون‌های رایج آرژینین‌اند، ولی در *E. coli* نادرترین کدون‌ها هستند (۱٫۰۹‰ و ۱٫۹۶‰). tRNAهای مکملشان (محصول ژن‌های *argU* و *argW*) کم‌اند. خوشه‌ای از AGG/AGA باعث **توقف ریبوزوم**، پروتئین ناقص، جابه‌جایی چارچوب (frameshift) و حتی **جایگزینی اشتباه اسیدآمینه** (مثلاً Lys به‌جای Arg) می‌شود.

دو راه‌حل رایج:
1. **بهینه‌سازی کدون (codon optimization):** ژن را با کدون‌های هم‌معنی پرکاربرد *E. coli* (مثل CGT/CGC) دوباره سنتز کنید.
2. **سویه‌ی میزبانی که tRNAهای نادر را اضافه بیان می‌کند:** مثل Rosetta (پلاسمید pRARE، شامل *argU* و *argW*) یا BL21-CodonPlus-RIL (*argU*، *ileY*، *leuW*).

---

## اشتباهات رایج کل ماژول
- خواندن ستون ۹ GFF بدون رمزگشایی (`%2C`) یا با رمزگشایی **قبل** از جدا کردن.
- ‏`translate()` بدون `cds=True` برای ساختن پروتئین‌های ژنوم.
- اعتماد به `IdList[0]` بدون چاپ تعداد نتایج.
- ترکیب مختصات مبنای ۰ (Entrez، BED، Python) و مبنای ۱ (GFF، VCF، SAM) بدون تبدیل صریح.

</div>
