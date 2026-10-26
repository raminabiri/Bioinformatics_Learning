<div dir="rtl">

# درس: Biopython (۲)؛ GenBank، ویژگی‌ها و Entrez

**بخش:** `03_Python` · **ماژول:** `05_Biopython_GenBank` · **پیش‌نیاز:** ماژول [Biopython (۱)](../04_Biopython_Seq/) · **زمان:** حدود ۹۰ دقیقه · **ابزار:** Python 3.13، Biopython 1.88 · **آخرین اجرا:** 2026-10-20

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. یک فایل **GenBank** را با `SeqIO` بخوانید و اطلاعات رکورد (موجود، رده‌بندی) را بگیرید.
2. روی **ویژگی‌ها** (features) بگردید: نوع، جایگاه، رشته و **qualifier**ها (gene، product، translation).
3. توالی یک ژن را با `.extract()` بیرون بکشید و ترجمه‌ی خودتان را با ترجمه‌ی NCBI بسنجید.
4. با **`Bio.Entrez`** یک رکورد را از NCBI بگیرید.
5. همه‌ی ژن‌های پروتئین‌ساز ژنوم را وارسی کنید و به یک **یافته‌ی زیستی** برسید (سلنوسیستئین).

**پیش از آغاز:**

<div dir="ltr">

```bash
conda activate bioinfo_course
cd ~/Bioinformatics_Learning-main/03_Python/99_scripts_data/05_Biopython_GenBank/data
P=../scripts
G=~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data
ls
```

</div>

<div dir="ltr">

```text
rpo_region.gb
```

</div>

---

## ۱. داستان: FASTA تنها توالی است

در درس آنوتیشن (بخش ۰۲) دیدیم که FASTA تنها **توالی** دارد و GFF تنها **جایگاه‌ها**. فایل **GenBank** هر دو را با هم دارد، به‌علاوه‌ی نام پروتئین، شناسه‌ها و حتی ترجمه‌ی آماده. خواندن آن با چشم آسان است، ولی بیرون کشیدن اطلاعات از ده‌ها ژن با چشم، نه.

‏`rpo_region.gb` یک **ناحیه‌ی ۱۵ کیلوبازی** از ژنوم *E. coli* است (۴٬۱۷۵٬۰۰۰ تا ۴٬۱۹۰٬۰۰۰): rpoB، rpoC و همسایه‌هایشان. این فایل را با اسکریپت بخش ۵ همین درس از NCBI گرفته‌ایم و در مخزن گذاشته‌ایم تا بی اینترنت هم کار کنید.

---

## ۲. خواندن رکورد GenBank

<div dir="ltr">

```python
>>> from Bio import SeqIO
>>> rec = SeqIO.read("rpo_region.gb", "genbank")
>>> rec.id
'NC_000913.3'
>>> len(rec.seq)
15001
>>> rec.annotations["organism"]
'Escherichia coli str. K-12 substr. MG1655'
>>> rec.annotations["taxonomy"]
['Bacteria', 'Pseudomonadati', 'Pseudomonadota', 'Gammaproteobacteria', 'Enterobacterales', 'Enterobacteriaceae', 'Escherichia']
>>> len(rec.features)
31
```

</div>

همان `SeqIO.read` درس پیشین؛ تنها فرمت `"genbank"` شد. ولی این `SeqRecord` دو چیز تازه دارد:

| ویژگی | چیست | در فایل GenBank |
| :--- | :--- | :--- |
| `rec.annotations` | یک **دیکشنری** از اطلاعات کل رکورد | بخش بالای فایل (`ORGANISM`، …) |
| `rec.features` | یک **فهرست** از ویژگی‌ها: ژن، CDS، tRNA، … | بخش `FEATURES` |

۳۱ ویژگی: یک `source` (کل ناحیه)، ۱۵ `gene`، ۱۱ `CDS` و ۴ `tRNA`.

---

## ۳. یک ویژگی (feature) را کالبدشکافی کنیم

در فایل GenBank، CDS ژن rpoB چنین است (کوتاه‌شده):

<div dir="ltr">

```text
     CDS             6246..10274
                     /gene="rpoB"
                     /product="RNA polymerase subunit beta"
                     /protein_id="NP_418414.1"
                     /db_xref="UniProtKB/Swiss-Prot:P0A8V2"
                     /translation="MVYSYTEKKRIRKDFGKRPQVLDVPYLLSIQLDSFQKFIEQDPEG…"
```

</div>

(جایگاه‌ها نسبت به **آغاز همین ناحیه**‌اند: ۶٬۲۴۶ = ۴٬۱۸۱٬۲۴۵ − ۴٬۱۷۵٬۰۰۰ + ۱.)

در پایتون، با حلقه پیدایش می‌کنیم:

<div dir="ltr">

```python
>>> for f in rec.features:
...     if f.type == "CDS" and f.qualifiers["gene"][0] == "rpoB":
...         rpoB = f
...
>>> rpoB.location
SimpleLocation(ExactPosition(6245), ExactPosition(10274), strand=1)
>>> rpoB.qualifiers["db_xref"]
['UniProtKB/Swiss-Prot:P0A8V2', 'ECOCYC:EG10894', 'GeneID:948488']
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `f.type` | نوع ویژگی: `"CDS"`، `"gene"`، `"tRNA"`، … |
| `and` | **هر دو** شرط باید درست باشند |
| `f.qualifiers` | دیکشنری خط‌های `/نام="مقدار"` |
| `f.qualifiers["gene"]` | یک **فهرست** است (`['rpoB']`)، چون یک qualifier می‌تواند چند بار بیاید؛ پس `[0]` |
| `f.location` | جایگاه: آغاز، پایان، رشته |

### جایگاه: Biopython هم از ۰ می‌شمارد

‏`ExactPosition(6245)` در برابر `6246` فایل: Biopython جایگاه را **مانند برش پایتون** (و BED) نگه می‌دارد: آغاز از ۰، پایان همان. `strand=1` یعنی رشته‌ی +، و `-1` یعنی رشته‌ی −. پس:

| | آغاز | پایان |
| :--- | :-: | :-: |
| فایل GenBank / GFF | ۶٬۲۴۶ | ۱۰٬۲۷۴ |
| Biopython / BED | ۶٬۲۴۵ | ۱۰٬۲۷۴ |

### ‏`.extract()`: بریدن درست، خودکار

<div dir="ltr">

```python
>>> dna = rpoB.extract(rec.seq)
>>> len(dna), dna[:12]
(4029, Seq('ATGGTTTACTCC'))
>>> p = dna.translate(table=11, cds=True)
>>> p[525]
'H'
```

</div>

‏`.extract()` همه‌ی کارهای دستی درس پیشین را خودش می‌کند: برش درست، و **مکمل معکوس اگر ژن روی رشته‌ی − باشد**، و چسباندن تکه‌ها اگر ژن چندتکه باشد. دیگر جای خطای «یکی کم/زیاد» نمی‌ماند.

### آیا ترجمه‌ی ما با NCBI یکی است؟

<div dir="ltr">

```python
>>> prot = rpoB.qualifiers["translation"][0]
>>> len(prot), prot[:10]
(1342, 'MVYSYTEKKR')
>>> str(p) == prot
True
```

</div>

‏**`True`**: ترجمه‌ی ما دقیقاً با ترجمه‌ی NCBI برابر است. (`str(p)` لازم است چون `p` یک `Seq` است و `prot` یک رشته.)

> 📺 **فیلم:** *GenBank Tutorial*: https://www.youtube.com/watch?v=JAxpmKg0KL0
> 📄 **مرجع:** Biopython Tutorial & Cookbook, فصل Sequence annotation objects: https://biopython.org/docs/latest/Tutorial/

---

## ۴. اسکریپت: فهرست ژن‌های ناحیه

‏[gb_genes.py](../99_scripts_data/05_Biopython_GenBank/scripts/gb_genes.py) همه‌ی ویژگی‌ها (جز `source` و `gene` که تکراری‌اند) را با جایگاه و محصولشان چاپ می‌کند. هسته‌ی آن:

<div dir="ltr">

```python
def first(qualifiers, key):
    """Return the first value of a qualifier, or '-' if the feature does not have it."""
    if key in qualifiers:
        return qualifiers[key][0]
    return "-"

for f in rec.features:
    if f.type == "source" or f.type == "gene":
        continue
    start = int(f.location.start) + 1          # back to 1-based, as in the GenBank file
    end = int(f.location.end)
    …
```

</div>

- ‏`or`: **یکی** از دو شرط بس است.
- ‏`key in qualifiers`: آیا این qualifier در دیکشنری هست؟ (tRNAها `translation` ندارند؛ بی این وارسی، `KeyError` می‌گرفتیم.)
- `+ 1`: برگرداندن به شماره‌گذاری فایل، تا خروجی با چشم سنجیدنی باشد.

<div dir="ltr">

```bash
python3 $P/gb_genes.py rpo_region.gb
```

</div>

<div dir="ltr">

```text
NC_000913.3 15001 bp
CDS	coaA	1	27	-	316 aa	pantothenate kinase
tRNA	thrU	389	464	+	-	tRNA-Thr
tRNA	tyrU	473	557	+	-	tRNA-Tyr
tRNA	glyT	674	748	+	-	tRNA-Gly
tRNA	thrT	755	830	+	-	tRNA-Thr
CDS	tufB	945	2129	+	394 aa	translation elongation factor Tu 2
CDS	secE	2359	2742	+	127 aa	Sec translocon subunit SecE
CDS	nusG	2744	3289	+	181 aa	transcription termination/antitermination factor NusG
CDS	rplK	3448	3876	+	142 aa	50S ribosomal subunit protein L11
CDS	rplA	3880	4584	+	234 aa	50S ribosomal subunit protein L1
CDS	rplJ	4997	5494	+	165 aa	50S ribosomal subunit protein L10
CDS	rplL	5561	5926	+	121 aa	50S ribosomal subunit protein L12
CDS	rpoB	6246	10274	+	1342 aa	RNA polymerase subunit beta
CDS	rpoC	10351	14574	+	1407 aa	RNA polymerase subunit beta'
CDS	yjaZ	14787	15001	+	179 aa	protein YjaZ
```

</div>

**نگاه زیستی:** این ناحیه یک **خوشه‌ی ژن‌های دستگاه بیان** است: tRNAها، فاکتور طویل‌سازی EF-Tu (tufB)، پروتئین‌های ریبوزوم (rpl) و دو زیرواحد بزرگ RNA پلیمراز (rpoB، rpoC)، همه روی یک رشته و پشت سر هم. tyrU همان ژن tRNA است که یکی از SNPهای سویه‌ی مقاوم (بخش ۰۲) در آن بود.

### ژن‌های نیمه در لبه‌ها

‏`coaA` تنها ۲۷ باز در این ناحیه دارد، ولی پروتئینش ۳۱۶ آمینواسید است! در فایل:

<div dir="ltr">

```text
     CDS             complement(<1..27)
```

</div>

<div dir="ltr">

```python
>>> coaA = rec.features[2]
>>> coaA.qualifiers["gene"], coaA.location
(['coaA'], SimpleLocation(BeforePosition(0), ExactPosition(27), strand=-1))
>>> len(coaA.extract(rec.seq))
27
```

</div>

نشانه‌ی `<` (در Biopython: `BeforePosition`) یعنی «ژن **پیش از** آغاز این ناحیه آغاز می‌شود». ما ناحیه را از وسط coaA بریده‌ایم؛ `translation` از رکورد کامل آمده است. `yjaZ` هم در پایان (`>15001`) همین حال را دارد. **پیش از ترجمه‌ی یک ژن، کامل بودن جایگاهش را وارسی کنید.**

---

## ۵. گرفتن رکورد از NCBI: `Bio.Entrez`

در بخش ۰۲ با `curl` و نشانی E-utilities رکورد گرفتیم. `Bio.Entrez` همان کار را از درون پایتون می‌کند. [fetch_region.py](../99_scripts_data/05_Biopython_GenBank/scripts/fetch_region.py):

<div dir="ltr">

```python
from Bio import Entrez

Entrez.email = "your.name@example.org"     # NCBI asks for a contact email: put YOUR email here

handle = Entrez.efetch(db="nuccore", id=accession, rettype="gbwithparts", retmode="text",
                       seq_start=start, seq_stop=end)
text = handle.read()
handle.close()
```

</div>

### کالبدشکافی

| تکه | یعنی |
| :--- | :--- |
| `Entrez.email` | ‏NCBI می‌خواهد بداند درخواست از کیست، تا اگر مشکلی بود با شما تماس بگیرد. **ایمیل خودتان** را بگذارید |
| `Entrez.efetch(…)` | همان `efetch.fcgi` در نشانی‌های `curl` بخش ۰۲ |
| `db="nuccore"` | پایگاه داده‌ی توالی‌های نوکلئوتیدی |
| `id=accession` | شماره‌ی دسترسی، مانند `NC_000913.3` |
| `rettype="gbwithparts"` | فرمت GenBank **با** توالی کامل |
| `seq_start`، `seq_stop` | تنها این ناحیه (شماره از ۱)، نه کل ژنوم ۴٫۶ میلیون بازی |
| `handle.read()` | پاسخ را به صورت یک رشته بخوان |

<div dir="ltr">

```bash
python3 $P/fetch_region.py NC_000913.3 4175000 4190000 rpo_region2.gb
cmp rpo_region.gb rpo_region2.gb && echo same
```

</div>

<div dir="ltr">

```text
wrote 44417 characters to rpo_region2.gb
same
```

</div>

‏(`cmp` دو فایل را بایت‌به‌بایت می‌سنجد و اگر یکی باشند، چیزی چاپ نمی‌کند؛ `&&` تنها در آن صورت `same` را چاپ می‌کند.) پس فایل مخزن همان چیزی است که امروز از NCBI می‌آید. (روزی که NCBI آنوتیشن را به‌روز کند، این دو فایل دیگر یکی نخواهند بود.)

> **قاعده‌های NCBI:** بی کلید API، **بیش از ۳ درخواست در ثانیه** نفرستید؛ در حلقه‌ها میان درخواست‌ها مکث کنید (`import time` و `time.sleep(0.4)`). برای کار بیشتر، کلید API رایگان بگیرید. هرگز کل یک پایگاه داده را با حلقه‌ی `efetch` بارگیری نکنید؛ برای آن، فایل‌های آماده‌ی FTP یا `datasets` (بخش ۰۲) هست.

> 📺 **فیلم:** *Accessing NCBI databases and tools with Biopython (Entrez)*: https://www.youtube.com/watch?v=tl4xqdfIBh0 (Lana Dominkovic)
> 📄 **مرجع:** NCBI, *Entrez Programming Utilities Help*: https://www.ncbi.nlm.nih.gov/books/NBK25497/

---

## ۶. همه‌ی ژن‌های ژنوم: یک یافته‌ی زیستی

حالا مهارت‌های این بخش را روی **کل ژنوم** به کار ببریم. [cds_check.py](../99_scripts_data/05_Biopython_GenBank/scripts/cds_check.py) هر CDS را از FASTA و GFF ژنوم (بخش ۰۱) می‌بُرد، ترجمه می‌کند و وارسی می‌کند:

<div dir="ltr">

```python
# 1. collect the CDS lines; a few genes have two CDS lines with the same ID (two pieces)
cds = {}
with open(sys.argv[2]) as f:
    for line in f:
        …
        if cols[2] != "CDS" or "pseudo=true" in cols[8]:
            continue
        cds_id = get_attribute(cols[8], "ID")
        if cds_id not in cds:
            cds[cds_id] = {"gene": get_attribute(cols[8], "gene"), "strand": cols[6], "pieces": []}
        cds[cds_id]["pieces"].append((int(cols[3]), int(cols[4])))

# 2. cut, translate and check each CDS
for cds_id in cds:
    c = cds[cds_id]
    dna = Seq("")
    for start, end in sorted(c["pieces"]):
        dna = dna + genome[start - 1:end]
    if c["strand"] == "-":
        dna = dna.reverse_complement()
    …
    protein = dna.translate(table=11)
    if "*" in protein[:-1]:                    # a stop codon inside the gene
        broken.append(c["gene"])
```

</div>

### کالبدشکافی بخش‌های تازه

| تکه | یعنی |
| :--- | :--- |
| `"pseudo=true" in cols[8]` | **ژن‌های کاذب** (pseudogene) را کنار بگذار؛ آن‌ها پروتئین درستی نمی‌سازند |
| `cds_id not in cds` | این ID هنوز در دیکشنری **نیست**؟ |
| `{"gene": …, "strand": …, "pieces": []}` | برای هر CDS یک **دیکشنری درون دیکشنری**: نام، رشته، و فهرست تکه‌ها |
| `(int(cols[3]), int(cols[4]))` | یک **تاپل** (tuple): جفت (آغاز، پایان) در پرانتز؛ مانند فهرست، ولی تغییرناپذیر |
| `for start, end in sorted(…)` | تکه‌ها را به ترتیب بگیر و هر جفت را در دو نام باز کن؛ همان `for n, l in zip(…)` ماژول ۰۲ |
| ‏`Seq("")` و `dna + …` | از توالی تهی آغاز کن و تکه‌ها را بچسبان |
| ‏`translate(table=11)` بی `cds=True` | این‌جا **عمداً** بی `cds=True`: می‌خواهیم ژن‌های «خراب» را ببینیم، نه این‌که اسکریپت با خطا بایستد |
| `"*" in protein[:-1]` | آیا کدون پایانی **پیش از** آخرین آمینواسید هست؟ |

**چرا «تکه‌ها»؟** چند ژن در GFF دو خط CDS با یک ID دارند. نمونه: `prfB` (فاکتور رهایی RF2) که ریبوزوم هنگام خواندنش **یک باز می‌لغزد** (`exception=ribosomal slippage`)؛ این خود سازوکاری برای تنظیم مقدار RF2 است.

<div dir="ltr">

```bash
python3 $P/cds_check.py $G/ecoli_k12.fna $G/ecoli_k12.gff
```

</div>

<div dir="ltr">

```text
CDS: 4300
start codons: {'ATG': 3876, 'GTG': 338, 'TTG': 80, 'ATT': 4, 'CTG': 2}
stop codons: {'TGA': 1242, 'TAA': 2753, 'TAG': 305}
CDS with an internal stop: ['fdnG', 'fdoG', 'fdhF']
```

</div>

در کمتر از نیم ثانیه:
- **۴٬۳۰۰ ژن پروتئین‌ساز** (۴٬۳۴۰ خط CDS، منهای ژن‌های کاذب و تکه‌های تکراری).
- کدون آغاز: ATG در ۹۰٪ ژن‌ها، ولی **۳۳۸ GTG** و **۸۰ TTG**: همان دلیل اهمیت `cds=True` و `table=11` (درس پیشین).
- کدون پایان: TAA پرکاربردترین.
- **سه ژن با کدون پایان درونی!** باگ؟

### یافته: سلنوسیستئین

هر سه، زیرواحدهای **فرمات دهیدروژناز** هستند. GFF چه می‌گوید؟

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

«در جایگاه ۱٬۵۴۷٬۹۸۶ تا ۱٬۵۴۷٬۹۸۸، استثنای ترجمه: آمینواسید **Sec**» (`%2C` همان ویرگول است). در این ژن‌ها کدون **TGA** به جای «پایان»، **سلنوسیستئین**، آمینواسید بیست‌ویکم را می‌سازد. یک ساختار ویژه در mRNA (SECIS) پس از TGA به ریبوزوم این را می‌گوید. Biopython (و هر جدول کد ژنتیکی) از این آگاه نیست.

**درس:** گاهی «خطای» یک وارسی خودکار، **زیست‌شناسی واقعی** است. پیش از دور ریختن داده‌ی «ناهنجار»، آنوتیشن را بخوانید.

---

## ۷. سه اشتباه رایج (با پیام واقعی)

### اشتباه ۱: فراموش کردن `[0]`

<div dir="ltr">

```python
print(rpoB.qualifiers["gene"] == "rpoB")
```

</div>

<div dir="ltr">

```text
False
```

</div>

‏`qualifiers["gene"]` فهرست `['rpoB']` است، نه رشته‌ی `'rpoB'`؛ و فهرست با رشته برابر نیست. بی هیچ خطایی، شرط هرگز درست نمی‌شود. `["gene"][0]`.

### اشتباه ۲: qualifierی که نیست

<div dir="ltr">

```python
for f in rec.features:
    if f.type == "tRNA":
        print(f.qualifiers["translation"])
```

</div>

<div dir="ltr">

```text
KeyError: 'translation'
```

</div>

‏tRNA پروتئین نمی‌سازد، پس `translation` ندارد. یا تنها CDSها را بگیرید، یا با `if "translation" in f.qualifiers:` وارسی کنید (تابع `first` در `gb_genes.py`).

### اشتباه ۳: فرمت نادرست

<div dir="ltr">

```python
SeqIO.read("rpo_region.gb", "fasta")
```

</div>

<div dir="ltr">

```text
ValueError: This FASTA file contains comments at the beginning of the file, which are not
allowed by the 'fasta' parser.
```

</div>

(تنها دو خط یکم پیام بلند.) خواننده‌ی FASTA در آغاز فایل GenBank خط `>` پیدا نکرد و خط‌های `LOCUS`، `DEFINITION`، … را «توضیح» پنداشت. پیام سپس راه‌هایی برای FASTAهای توضیح‌دار پیشنهاد می‌کند که این‌جا به کار نمی‌آیند: **مشکل، نام فرمت است.** Biopython فرمت را خودش حدس نمی‌زند؛ باید `"genbank"` بدهید.

---

## ۸. جمع‌بندی

- ‏`SeqIO.read(f, "genbank")` → `rec.annotations` (کل رکورد) و `rec.features` (فهرست ویژگی‌ها).
- هر ویژگی: `.type`، `.location` (آغاز از ۰، `strand` ۱ یا ۱−)، `.qualifiers` (دیکشنری فهرست‌ها: `["gene"][0]`).
- ‏`.extract(rec.seq)` برش، مکمل معکوس و چسباندن تکه‌ها را درست انجام می‌دهد.
- ‏`Entrez.email` + `Entrez.efetch(db=…, id=…, rettype=…)`؛ بیش از ۳ درخواست در ثانیه نه.
- سه ژن «خراب» *E. coli* سلنوپروتئین‌اند: بعضی «خطا»ها زیست‌شناسی‌اند.

---

## کارت دستورهای این درس

| می‌خواهم… | Biopython |
| :--- | :--- |
| خواندن GenBank | `rec = SeqIO.read("f.gb", "genbank")` |
| موجود / رده‌بندی | `rec.annotations["organism"]` / `["taxonomy"]` |
| گشتن روی ویژگی‌ها | `for f in rec.features:` |
| نوع / جایگاه | `f.type` / `f.location.start`، `.end`، `.strand` |
| یک qualifier | `f.qualifiers["gene"][0]` |
| آیا qualifier هست؟ | `"translation" in f.qualifiers` |
| توالی ویژگی | `f.extract(rec.seq)` |
| گرفتن از NCBI | `Entrez.email = "…"` / `Entrez.efetch(db="nuccore", id=…, rettype="gbwithparts", retmode="text")` |

---

<details>
<summary>📘 <b>برای کنجکاوها (اختیاری):</b> جستجو در NCBI با <code>Entrez.esearch</code></summary>

‏`efetch` رکوردی را می‌گیرد که شماره‌اش را می‌دانید. برای **جستجو**، `esearch` (همان `esearch.fcgi` بخش ۰۲) و `Entrez.read` برای خواندن پاسخ XML:

<div dir="ltr">

```python
from Bio import Entrez
Entrez.email = "your.name@example.org"
handle = Entrez.esearch(db="pubmed", term="rpoB AND rifampicin resistance", retmax=0)
result = Entrez.read(handle)
handle.close()
print(result["Count"])
```

</div>

شمار مقاله‌ها هر روز بیشتر می‌شود، پس عددی این‌جا ننوشته‌ایم؛ خودتان اجرا کنید.
</details>

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| ویژگی (feature) | یک بخش آنوتیت‌شده‌ی توالی: ژن، CDS، tRNA، … |
| qualifier | خط‌های `/نام="مقدار"` زیر هر ویژگی |
| `annotations` | اطلاعات کل رکورد GenBank |
| `.extract()` | بیرون کشیدن توالی یک ویژگی، با رشته و تکه‌ها |
| Entrez / E-utilities | سامانه‌ی جستجو و بارگیری NCBI |
| ژن کاذب (pseudogene) | ژنی که دیگر پروتئین کارآمد نمی‌سازد |
| تاپل (tuple) | مانند فهرست، در پرانتز، و تغییرناپذیر |
| سلنوسیستئین (Sec) | آمینواسید ۲۱ام، که کدون TGA در زمینه‌ی ویژه‌ای آن را می‌سازد |

---

## منابع

### راهنما و مقاله
- ‏Biopython Tutorial & Cookbook، فصل‌های «Sequence annotation objects» و «Accessing NCBI's Entrez databases»: https://biopython.org/docs/latest/Tutorial/
- راهنمای E-utilities در NCBI (قاعده‌ها و کلید API): https://www.ncbi.nlm.nih.gov/books/NBK25497/
- راهنمای فرمت GenBank در NCBI: https://www.ncbi.nlm.nih.gov/genbank/samplerecord/
- Böck A, et al. (1991). Selenocysteine: the 21st amino acid. *Molecular Microbiology* 5(3):515–520. https://doi.org/10.1111/j.1365-2958.1991.tb00722.x

### کتاب
- ‏Bassi S (2017). *Python for Bioinformatics*, 2nd ed. CRC Press. (بخش Biopython و دسترسی به NCBI)

### فیلم‌های آموزشی

**Coursera:**
- ‏Johns Hopkins University — *Python for Genomic Data Science* (هفته‌ی ۴، Biopython): https://www.coursera.org/learn/python-genomics

**edX:**
- UC San Diego — *Introduction to Genomic Data Science*: https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science

**YouTube:**
- Lana Dominkovic — *Accessing NCBI databases and tools with Biopython (Entrez)*: https://www.youtube.com/watch?v=tl4xqdfIBh0
- Lana Dominkovic — *Bioinformatics with Biopython, Full Course*: https://www.youtube.com/watch?v=ocA2IMe7dpA

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. همه‌ی کدها در 2026-10-20 با Python 3.13.15 و Biopython 1.88 اجرا شدند.

</div>
