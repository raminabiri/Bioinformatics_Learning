<div dir="rtl">

# درس: دریافت داده با دستور، به شکلی که دوباره‌پذیر باشد

**بخش:** `02_BioLinux` · **ماژول:** `05_Data_Download` · **پیش‌نیاز:** ماژول [فرمت‌های هم‌ترازی و واریانت](../04_Align_Variant_Formats/) و [درس پایگاه‌های داده](../../00_Orientation/02_Biological_Databases/01_lesson.md) · **زمان:** حدود ۱ ساعت · **ابزار:** `curl`، `jq`، NCBI Datasets CLI 18.38 · **آخرین اجرا:** 2026-10-12

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. بگویید چرا داده را باید با دستور دریافت کرد، نه با کلیک در مرورگر.
2. یک ژنوم را با ابزار `datasets` از NCBI بگیرید.
3. نشانی و «اثر انگشت» (md5) فایل‌های خام را از ENA بپرسید و تنها بخشی از یک فایل بزرگ را بخوانید.
4. یک اسکریپت آماده را اجرا کنید که یک ژن را در هشت پایگاه داده دنبال می‌کند، و خروجی‌اش را بفهمید.

---

## ۱. چرا با دستور؟

در [درس پایگاه‌های داده](../../00_Orientation/02_Biological_Databases/01_lesson.md) همه کارها را با مرورگر کردیم. این برای **دیدن و یاد گرفتن** خوب است، ولی برای **پژوهش** دو کاستی دارد:

1. **دوباره‌پذیر نیست.** شش ماه بعد یادتان نیست روی کدام دکمه زدید و کدام نسخه را دانلود کردید.
2. **کند است.** دانلود یک ژنوم با کلیک آسان است، ولی دانلود ۲۰۰ ژنوم نه.

راه‌حل: هر داده‌ای را که در تحلیل به کار می‌برید، با **یک اسکریپت** دریافت کنید که شناسه‌ی نسخه‌دار را دارد. در این دوره هر بخش یک فایل `data/download.sh` دارد که دقیقاً همین کار را می‌کند. اسکریپت مانند **دستور پخت دقیق** درس پیش است: هر کس اجرایش کند، به همان داده می‌رسد.

**سه راه برای دریافت داده با دستور:**

| راه | یعنی چه | در این درس |
| :--- | :--- | :--- |
| ابزار رسمی خط فرمان | برنامه‌ای که خود پایگاه داده ساخته | ‏`datasets` از NCBI |
| API | نشانی وبی که به جای صفحه‌ی زیبا، داده‌ی خام (جدول یا JSON) برمی‌گرداند | ‏ENA و UniProt با `curl` |
| اسکریپت | چند دستور پشت سر هم در یک فایل | `scripts/gene_tour.sh` |

---

## ۲. آماده‌سازی

<div dir="ltr">

```bash
conda activate bioinfo_course
cd 02_BioLinux/99_scripts_data/05_Data_Download
mkdir -p work && cd work
```

</div>

- ‏`conda activate` محیطی را روشن می‌کند که ابزارهای دوره در آن نصب‌اند (ماژول [Conda و Bioconda](../01_Conda_Bioconda/)).
- همه‌ی خروجی‌ها را در پوشه‌ی `work` می‌گذاریم تا پوشه‌ی درس شلوغ نشود.

---

## ۳. گرفتن یک ژنوم با `datasets`

**چرا؟** ژنوم مرجع *E. coli* K-12 را برای سنجش سویه‌ی خودمان لازم داریم.

<div dir="ltr">

```bash
datasets download genome accession GCF_000005845.2 --include genome,protein,gff3 --filename ecoli_k12.zip
unzip -o ecoli_k12.zip
find ncbi_dataset -type f
```

</div>

**بخش‌های دستور:**
- ‏`datasets download genome accession` یعنی «ژنومی را با این شناسه دانلود کن».
- ‏`GCF_000005845.2` شناسه‌ی نسخه‌دار ژنوم است. اگر سال دیگر NCBI نسخه‌ی ۳ را منتشر کند، این دستور باز هم همان نسخه‌ی ۲ را می‌گیرد. دوباره‌پذیری یعنی همین.
- ‏`--include genome,protein,gff3` یعنی سه چیز بده: توالی ژنوم، توالی پروتئین‌ها، و فهرست ژن‌ها (فایل GFF).
- ‏`--filename` نام فایل zip خروجی است.

**خروجی (2026-10-12):**

<div dir="ltr">

```text
ncbi_dataset/data/dataset_catalog.json
ncbi_dataset/data/assembly_data_report.jsonl
ncbi_dataset/data/GCF_000005845.2/protein.faa
ncbi_dataset/data/GCF_000005845.2/genomic.gff
ncbi_dataset/data/GCF_000005845.2/GCF_000005845.2_ASM584v2_genomic.fna
```

</div>

**این خروجی یعنی:**
- ‏`..._genomic.fna`: توالی ژنوم در فرمت FASTA (پسوند `fna` یعنی FASTA نوکلئوتید).
- ‏`protein.faa`: توالی همه‌ی پروتئین‌ها در فرمت FASTA (پسوند `faa` یعنی FASTA اسیدآمینه).
- ‏`genomic.gff`: فهرست ژن‌ها و جای هر کدام روی ژنوم.
- ‏`assembly_data_report.jsonl`: گزارشی درباره‌ی خود ژنوم (طول، شمار ژن‌ها و…).

<details>
<summary>✋ <b>امتحان کن:</b> با دستوری که در بخش لینوکس (ماژول grep) یاد گرفتید، بشمارید فایل <code>protein.faa</code> چند پروتئین دارد.</summary>

هر پروتئین در FASTA یک خط عنوان دارد که با `>` شروع می‌شود. پس:

<div dir="ltr">

```bash
grep -c '>' ncbi_dataset/data/GCF_000005845.2/protein.faa
```

</div>

پاسخ (2026-10-12): **4300**.
</details>

---

## ۴. پرسیدن از API: فایل‌های خام در ENA

**چرا؟** می‌خواهیم بدانیم فایل FASTQ یک «اجرا» کجاست، چقدر بزرگ است و اثر انگشتش چیست، پیش از آنکه دانلودش کنیم.

<div dir="ltr">

```bash
curl -s "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=ERR688359&result=read_run&fields=run_accession,fastq_ftp,fastq_md5,fastq_bytes,read_count&format=tsv"
```

</div>

**بخش‌های دستور:**
- ‏`curl -s` یک نشانی وب را می‌خواند و پاسخ را در ترمینال چاپ می‌کند (`-s` یعنی بی‌سروصدا، بی‌نوار پیشرفت).
- نشانی، یک **پرسش** از ENA است. بخش‌های پس از `?` آن را می‌سازند:
  - ‏`accession=ERR688359`: درباره‌ی این اجرا
  - ‏`result=read_run`: آگاهی‌های اجرا را بده
  - ‏`fields=…`: این ستون‌ها را بده
  - ‏`format=tsv`: به شکل جدول با جداکننده‌ی Tab

**خروجی (2026-10-12):**

<div dir="ltr">

```text
run_accession	fastq_ftp	fastq_md5	fastq_bytes	read_count
ERR688359	ftp.sra.ebi.ac.uk/vol1/fastq/ERR688/ERR688359/ERR688359.fastq.gz	891ae71035f90e8fefe6699bbeb0f90a	103709762	1158189
```

</div>

**این خروجی یعنی:**
- ‏`fastq_ftp`: نشانی فایل FASTQ برای دانلود.
- ‏`fastq_bytes`: اندازه‌ی فایل، حدود ۱۰۴ مگابایت.
- ‏`read_count`: شمار ریدها، حدود ۱٫۱۶ میلیون.
- ‏`fastq_md5`: **اثر انگشت فایل**. md5 یک رشته‌ی ۳۲ نویسه‌ای است که از محتوای فایل ساخته می‌شود. اگر حتی یک حرف فایل در دانلود خراب شود، md5 کاملاً عوض می‌شود. پس پس از دانلود، md5 فایل خودتان را حساب می‌کنید (`md5sum`) و با این عدد می‌سنجید.

### خواندن تنها آغاز یک فایل بزرگ
نیازی نیست برای دیدن چند رید، کل ۱۰۴ مگابایت را دانلود کنید:

<div dir="ltr">

```bash
curl -s https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR688/ERR688359/ERR688359.fastq.gz | zcat | head -n 4000 > ERR688359_head.fastq
```

</div>

- ‏`curl` فایل را از اینترنت می‌خواند، `zcat` آن را از حالت فشرده باز می‌کند، و `head -n 4000` تنها ۴٬۰۰۰ خط اول را نگه می‌دارد.
- هر رید در FASTQ چهار خط است، پس ۴٬۰۰۰ خط یعنی **۱٬۰۰۰ رید**.
- وقتی `head` به خط ۴٬۰۰۰ می‌رسد، لوله را می‌بندد و `curl` هم دانلود را رها می‌کند. اگر پیام `gzip: stdout: Broken pipe` دیدید، نگران نباشید؛ در این حالت پیام عادی است.

---

## ۵. یک اسکریپت آماده: سفر ژن در هشت پایگاه

در [درس پایگاه‌های داده](../../00_Orientation/02_Biological_Databases/01_lesson.md) ژن rpoB را با مرورگر دنبال کردیم. اسکریپت [gene_tour.sh](../99_scripts_data/05_Data_Download/scripts/gene_tour.sh) همان کار را با دستور می‌کند:

<div dir="ltr">

```bash
bash ../scripts/gene_tour.sh          # پیش‌فرض: ژن rpoB در E. coli K-12 (taxid 511145)
```

</div>

**خروجی (2026-10-12):**

<div dir="ltr">

```text
== 1. NCBI Taxonomy
taxid=511145  name=Escherichia coli str. K-12 substr. MG1655
== 2. NCBI Genome (reference assembly)
GCF_000005845.2  Complete Genome  length=4641652  GC=51%  genes=4651
== 3. NCBI Gene
GeneID=948488  symbol=rpoB  locus_tag=b3987  RNA polymerase subunit beta
== 4. UniProtKB (reviewed / Swiss-Prot)
Entry	Length	Protein names	EC number
P0A8V2	1342	DNA-directed RNA polymerase subunit beta (RNAP subunit beta) (EC 2.7.7.6) ...	2.7.7.6
== 5. KEGG (via UniProt cross-reference)
ENTRY       b3987             CDS       T00007
ORTHOLOGY   K03043  DNA-directed RNA polymerase subunit beta [EC:2.7.7.6]
PATHWAY     eco03020  RNA polymerase
== 6. AlphaFold DB
model=AF-P0A8V2-F1  mean_pLDDT=90.06
== 7. PDB (experimental structures that contain this UniProt sequence)
entries=391  first: 10MA, 10MB, 10MC, 10MD, 10ME
== 8. PubMed (literature)
PubMed hits for "rpoB AND rifampicin resistance": 1885
```

</div>

**این خروجی را با درس پایگاه‌های داده بسنجید.** همان عددهایی است که در مرورگر دیدیم (Gene ID، طول ۱٬۳۴۲، pLDDT نزدیک ۹۰، ۳۹۱ ساختار، ۱٬۸۸۵ مقاله)، ولی این بار در چند ثانیه و با یک دستور که هر کسی می‌تواند دوباره اجرا کند.

دو نکته‌ی تازه:
- ‏**taxid** شماره‌ی هر موجود در رده‌بندی NCBI است. `511145` یعنی دقیقاً سویه‌ی *E. coli* K-12 MG1655، نه هر *E. coli*.
- ‏**KEGG** پایگاه مسیرهای متابولیسم و کار ژن‌هاست. `K03043` یک **گروه کاری** است: همه‌ی پروتئین‌های RpoB در همه‌ی باکتری‌ها در این گروه‌اند. همین شناسه در بخش ۰۶ در جدول کار ژن‌های میکروبیوم می‌آید.

**درون اسکریپت چه می‌گذرد؟** هر گام یک پرسش از API یک پایگاه است. برای نمونه گام ۴ این است:

<div dir="ltr">

```bash
curl -s "https://rest.uniprot.org/uniprotkb/search?query=gene_exact:rpoB+AND+organism_id:83333+AND+reviewed:true&fields=accession,length,protein_name,ec&format=tsv"
```

</div>

یعنی از UniProt بپرس: «مدخل‌های بازبینی‌شده‌ی (`reviewed:true`) ژن rpoB در *E. coli* K-12 (`organism_id:83333`) را با این چهار ستون بده». لازم نیست اکنون همه‌ی اسکریپت را بفهمید؛ کافی است بدانید هر گام همین الگو را دارد.

گام‌های دیگر پاسخ را به شکل **JSON** می‌گیرند: قالبی متنی که داده را به شکل `"نام": مقدار` و تودرتو نگه می‌دارد. برای برداشتن یک تکه از JSON، اسکریپت ابزار **`jq`** را به کار می‌برد؛ برای نمونه در گام ۶، `jq -r '.[0] | "model=\(.entryId)  mean_pLDDT=\(.globalMetricValue)"'` یعنی «از نخستین مدخل، شناسه‌ی مدل و میانگین pLDDT را چاپ کن». نوشتن `jq` در این دوره لازم نیست؛ تنها بدانید کارش «`grep` و `cut` برای JSON» است.

---

## ۶. سه اشتباه رایج

| اشتباه | چرا مشکل است | به جایش چه کنیم |
| :--- | :--- | :--- |
| دانلود دستی و نگه‌نداشتن نشانی و نسخه | کسی، حتی خودتان، نمی‌تواند همان داده را دوباره بگیرد | دانلود با اسکریپت و شناسه‌ی نسخه‌دار |
| نسنجیدن md5 پس از دانلود | فایل خراب‌شده بی‌صدا تحلیل را خراب می‌کند | ‏`md5sum` و سنجش با عدد ENA |
| دانلود کامل یک فایل بزرگ تنها برای دیدن چند خط | زمان و فضا هدر می‌رود | `curl … \| zcat \| head` |

---

## ۷. جمع‌بندی

- داده را با **دستور یا اسکریپت** دریافت کنید تا هر کسی بتواند همان داده را دوباره بگیرد.
- ‏`datasets` ژنوم‌ها را از NCBI با شناسه‌ی نسخه‌دار می‌گیرد.
- ‏API نشانی وبی است که داده‌ی خام برمی‌گرداند. با `curl` از ENA و UniProt پرسیدیم.
- ‏**md5** اثر انگشت فایل است و درستی دانلود را نشان می‌دهد.
- اسکریپت `gene_tour.sh` همان سفر ژن درس پایگاه‌های داده را با هشت پرسش API انجام می‌دهد.

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| API | نشانی‌ای که برنامه‌ها (نه آدم‌ها) با آن از یک پایگاه داده می‌پرسند و داده‌ی خام می‌گیرند |
| `curl` | برنامه‌ای که یک نشانی وب را از ترمینال می‌خواند |
| JSON / TSV | دو قالب متنی برای داده‌ی ساختاریافته؛ TSV یک جدول با جداکننده‌ی Tab است |
| md5 | رشته‌ی ۳۲ نویسه‌ای که از محتوای فایل ساخته می‌شود؛ برای سنجش درستی دانلود |
| taxid | شماره‌ی یک موجود در رده‌بندی NCBI |
| KEGG Orthology (KO) | گروهی از ژن‌ها در گونه‌های گوناگون که یک کار را انجام می‌دهند |

---

## منابع

### راهنمای رسمی ابزارها
- NCBI Datasets: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/
- ENA Portal API: https://www.ebi.ac.uk/ena/portal/api/
- UniProt REST API: https://www.uniprot.org/help/api
- KEGG REST API: https://www.kegg.jp/kegg/rest/keggapi.html
- O'Leary NA, et al. (2024). Exploring and retrieving sequence and metadata for species across the tree of life with NCBI Datasets. *Scientific Data*. https://doi.org/10.1038/s41597-024-03571-y

### فیلم‌های آموزشی

**Coursera:**
- ‏Johns Hopkins University — *Command Line Tools for Genomic Data Science*. کار با داده‌ی ژنومی در خط فرمان: https://www.coursera.org/learn/genomic-tools

**edX:**
- UC San Diego — *Introduction to Genomic Data Science*: https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science

**YouTube:**
- Nuala O'Leary (NCBI), Tree of Life — *Easy programmatic access to NCBI genome data with NCBI Datasets*: https://www.youtube.com/watch?v=Ru5MzGG_rcE
- EMBL-EBI — *Nucleotide sequencing data submission and retrieval at the ENA*: https://www.youtube.com/watch?v=1qvG9mtxSYo
- EMBL-EBI — *EMBL-EBI, programmatically: UniProt*: https://www.youtube.com/watch?v=r7bq_HVO98Y
- Bioinformagician — *How to download sequencing data from SRA NCBI*: https://www.youtube.com/watch?v=zE851fWCYQg

> **وارسی نشانی‌ها:** مقاله و صفحه‌های راهنما و edX در 2026-10-19 با درخواست مستقیم وارسی شدند. Coursera از سرور دوره خطای 451 (محدودیت منطقه‌ای) می‌دهد و نشانی‌اش با موتور جستجو در 2026-10-19 وارسی شد. ویدیوهای YouTube آخرین بار در 2026-10-12 با YouTube oEmbed وارسی شدند.

</div>
