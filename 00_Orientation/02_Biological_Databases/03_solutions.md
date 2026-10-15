# پاسخ تشریحی: دیتابیس‌های زیستی و دریافت داده

> همه‌ی دستورها در تاریخ **2026-10-12** با NCBI Datasets CLI 18.38.0 اجرا شده‌اند. اعداد وابسته به زمان مشخص شده‌اند.

---

## تمرین ۱: شناسه‌خوانی

| شناسه | نوع رکورد | منشأ | اولیه/ثانویه | رابطه |
| :--- | :--- | :--- | :--- | :--- |
| `PRJEB7774` | BioProject (مطالعه) | ENA (حرف E) | اولیه (metadata) | والدِ همه‌ی شناسه‌های ستون اول |
| `SAMEA3136648` | BioSample (یک نمونه‌ی مدفوع) | EBI | اولیه | عضو PRJEB7774 |
| `ERX633507` | Experiment (کتابخانه) | EBI | اولیه | کتابخانه‌ی Run `ERR688506` |
| `ERR688506` | Run (فایل‌های FASTQ) | EBI | اولیه | Run پیرد-اند نمونه‌ی SAMEA3136648 |
| `GCA_000005845.2` | اسمبلی ژنوم در INSDC | GenBank | اولیه | جفتِ GCF همین ژنوم |
| `GCF_000005845.2` | اسمبلی RefSeq | NCBI RefSeq | ثانویه (curated) | کپی RefSeq از GCA بالا، با آنوتیشن NCBI |
| `NC_000913.3` | مولکول ژنومی کامل (کروموزوم) | RefSeq | ثانویه | کروموزوم GCF_000005845.2؛ معادل GenBank آن `U00096.3` است |
| `NP_418414.1` | پروتئین curated | RefSeq | ثانویه | پروتئین RpoB روی NC_000913.3 |
| `P0A8V2` | مدخل پروتئین | UniProtKB/Swiss-Prot | ثانویه | همان RpoB |
| `AF-P0A8V2-F1` | مدل ساختار پیش‌بینی‌شده | AlphaFold DB | محاسباتی | مدل P0A8V2 |
| `4HHB` | ساختار تجربی | PDB | اولیه | (هموگلوبین انسانی، X-ray، رزولوشن 1.74 Å؛ نامرتبط با بقیه) |
| `K03043` | KEGG Orthology | KEGG | ثانویه | گروه ارتولوگ RpoB (در همه‌ی گونه‌ها) |

**نکته‌ی تشریحی:** دو زنجیره در این جدول هست:
- **زنجیره‌ی داده‌ی خام:** PRJ → SAM → ERX → ERR.
- **زنجیره‌ی یک ژن:** GCF → NC → NP ↔ P0A8V2 ↔ AF-… ↔ K03043.

اشتباه رایج این است که `K03043` را شناسه‌ی «پروتئین E. coli» بدانیم. KO یک **دسته‌ی عملکردی** است که RpoB همه‌ی باکتری‌ها را در بر می‌گیرد.

---

## تمرین ۲: سفر ژن gyrA

### ۲.۱ خروجی واقعی
```bash
bash ../scripts/gene_tour.sh gyrA 511145 "fluoroquinolone resistance"
```
```text
== 3. NCBI Gene
GeneID=946614  symbol=gyrA  locus_tag=b2231  DNA gyrase subunit A
== 4. UniProtKB (reviewed / Swiss-Prot)
Entry	Length	Protein names	EC number
P0AES4	875	DNA gyrase subunit A (EC 5.6.2.2)	5.6.2.2
== 5. KEGG (via UniProt cross-reference)
ENTRY       b2231             CDS       T00007
ORTHOLOGY   K02469  DNA gyrase subunit A [EC:5.6.2.2]
== 6. AlphaFold DB
model=AF-P0AES4-F1  mean_pLDDT=87.38
== 7. PDB (experimental structures that contain this UniProt sequence)
entries=19  first: 1AB4, 1X75, 1ZI0, 3NUH, 4TMA
== 8. PubMed (literature)
PubMed hits for "gyrA AND fluoroquinolone resistance": 2848
```

| مورد | rpoB | gyrA |
| :--- | :--- | :--- |
| GeneID | 948488 | 946614 |
| locus tag | b3987 | b2231 |
| UniProt | P0A8V2 | P0AES4 |
| طول (aa) | 1342 | 875 |
| EC | 2.7.7.6 | 5.6.2.2 |
| KO | K03043 | K02469 |
| میانگین pLDDT | 90.06 | 87.38 |
| ساختار PDB | 391 | 19 |

### ۲.۲ تفاوت KEGG
برای rpoB یک سطر `PATHWAY eco03020 RNA polymerase` دیده می‌شود، ولی **gyrA هیچ سطر PATHWAY ندارد**. gyrA در KEGG فقط در سلسله‌مراتب BRITE (دسته‌بندی عملکردی، مثل «DNA replication proteins») آمده و در هیچ نقشه‌ی مسیر (map) نیست.

**پیامد برای متاژنومیکس:** اگر پروفایل عملکردی را فقط در سطح «مسیر» خلاصه کنید، ژن‌هایی که در هیچ مسیری نیستند (از جمله بسیاری از اهداف آنتی‌بیوتیکی، ژن‌های مقاومت و ضراوت) **از تحلیل حذف می‌شوند**. به همین دلیل در بخش ۰۳ پروفایل عملکردی را هم در سطح ژن/KO و هم در سطح مسیر نگاه می‌کنیم، و برای ژن‌های مقاومت (بخش ۰۵) از دیتابیس اختصاصی (CARD) استفاده می‌کنیم.

### ۲.۳ چرا RpoB ساختارهای خیلی بیشتری دارد؟
فرضیه‌های قابل قبول:
- RpoB جزئی از **هولوآنزیم RNA پلیمراز** است و هر ساختار از این کمپلکس (با فاکتورهای σ، DNA، RNA، تنظیم‌کننده‌ها و مهارکننده‌ها) زنجیره‌ی RpoB را هم دارد. RNA پلیمراز یکی از پرمطالعه‌ترین ماشین‌های مولکولی در زیست‌شناسی ساختاری، به‌ویژه با **cryo-EM**، است.
- بخش بزرگی از ساختارهای gyrase با پروتئین‌های سویه‌های دیگر (مثلاً *Staphylococcus aureus* یا *Mycobacterium tuberculosis*) یا با قطعات مجزای دومین‌ها حل شده‌اند. آن‌ها به `P0AES4` (gyrA *E. coli*) نگاشت نمی‌شوند و در این شمارش نیستند.

**درس روش‌شناختی:** کوئری ما «ساختارهایی که توالی دقیقاً همین UniProt را دارند» بود. برای یک سؤال ساختاری درباره‌ی gyrase باید ارتولوگ‌ها را هم جستجو کنید.

---

## تمرین ۳: کار با ژنوم مرجع

### ۳.۱ و ۳.۲ تعداد پروتئین و پیشوندها
```bash
grep -c '>' ncbi_dataset/data/GCF_000005845.2/protein.faa
grep '>' ncbi_dataset/data/GCF_000005845.2/protein.faa | cut -c2-4 | sort | uniq -c
```
```text
4300
   3918 NP_
    382 YP_
```
**۴۳۰۰ پروتئین**، همه با پیشوند curated (`NP_` و `YP_`). در ژنوم‌های غیرمرجع پروکاریوتی معمولاً `WP_` می‌بینید. MG1655 ژنوم مرجع است و پروتئین‌های اختصاصی curated دارد.

### ۳.۳ چرا ۴۵۰۶ و نه ۴۶۵۱؟
```bash
grep -v '^#' ncbi_dataset/data/GCF_000005845.2/genomic.gff | cut -f3 | sort | uniq -c | sort -rn | head
```
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
```
در GFF، **۱۴۵ ژن کاذب (pseudogene)** نوع feature جداگانه‌ای دارند و زیر `gene` شمرده نمی‌شوند. **4506 + 145 = 4651**، دقیقاً همان عدد گزارش NCBI. گزارش اسمبلی هم همین را جداگانه نشان می‌دهد:
```bash
jq -c '.annotationInfo.stats.geneCounts // .annotation_info.stats.gene_counts' ncbi_dataset/data/assembly_data_report.jsonl
```
```text
{"total":4651,"proteinCoding":4290,"nonCoding":215,"pseudogene":145,"other":1}
```
**درس:** «تعداد ژن» به تعریف بستگی دارد. وقتی ژنوم‌ها را مقایسه می‌کنید (بخش ۰۴)، مطمئن شوید همه را با یک تعریف و یک ابزار آنوتیشن شمرده‌اید.

### ۳.۴ مختصات rpoB
```bash
awk -F'\t' '$3=="gene" && $9 ~ /Name=rpoB;/ {print $1, $4, $5, $7, $5-$4+1}' ncbi_dataset/data/GCF_000005845.2/genomic.gff
```
```text
NC_000913.3 4181245 4185273 + 4029
```
طول ژن **۴۰۲۹ نوکلئوتید** است: 1342 × 3 = 4026 نوکلئوتید برای اسیدهای آمینه + ۳ نوکلئوتید کدون پایان = 4029. ✓
(مختصات GFF مبنای ۱ و دوسر بسته‌اند؛ پس طول = پایان − شروع + ۱.)

### ۳.۵ شناسه‌ی پروتئین
```bash
awk -F'\t' '$3=="CDS" && $9 ~ /gene=rpoB;/' ncbi_dataset/data/GCF_000005845.2/genomic.gff | grep -oE 'protein_id=[^;]+' | head -1
```
```text
protein_id=NP_418414.1
```

---

## تمرین ۴: ریدهای خام از ENA

### ۴.۱
```bash
curl -s "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=ERR688359&result=read_run&fields=fastq_ftp,fastq_md5,fastq_bytes,read_count,base_count&format=tsv"
```
```text
run_accession	fastq_ftp	fastq_md5	fastq_bytes	read_count	base_count
ERR688359	ftp.sra.ebi.ac.uk/vol1/fastq/ERR688/ERR688359/ERR688359.fastq.gz	891ae71035f90e8fefe6699bbeb0f90a	103709762	1158189	102874412
```
دقت کنید `run_accession` را نخواسته بودیم ولی ENA همیشه آن را به‌عنوان ستون اول برمی‌گرداند.

### ۴.۲ stream کردن ۱۰۰۰ رید اول
```bash
curl -s https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR688/ERR688359/ERR688359.fastq.gz | zcat | head -n 4000 > ERR688359_head.fastq
```
۱۰۰۰ رید × ۴ خط = ۴۰۰۰ خط. `head` بعد از ۴۰۰۰ خط لوله را می‌بندد و `curl` متوقف می‌شود، پس کل ۱۰۰ مگابایت دانلود نمی‌شود. ممکن است پیام `gzip: stdout: Broken pipe` ببینید که در این حالت طبیعی است.

### ۴.۳ طول ریدها
```bash
awk 'NR%4==2 {print length($0)}' ERR688359_head.fastq | sort -n | uniq -c | sort -rn | head -3
awk 'NR%4==2 {print length($0)}' ERR688359_head.fastq | sort -n | sed -n '1p;$p'
```
```text
    794 96
     20 95
     12 94
30
96
```
طول ریدها بین **۳۰ و ۹۶** است و ۷۹٫۴٪ ریدها ۹۶ باز دارند. پس این ریدها **قبلاً trim شده‌اند**. داده‌ی خام HiSeq 2000 طول ثابت دارد. میانگین طول کل فایل هم این را تأیید می‌کند: 102874412 ÷ 1158189 ≈ 88.8. **پیامد:** نتیجه‌ی QC شما روی این داده، QC داده‌ی «خام» نیست. این را باید در Methods ذکر کرد.

### ۴.۴ کدگذاری کیفیت
```bash
awk 'NR%4==0' ERR688359_head.fastq | fold -w1 | sort -u | tr -d '\n'; echo
```
```text
&'()*+,-./:;<=>?@0123456789ABCDEFGHIJ
```
کمترین کاراکتر `&` (ASCII 38) و بیشترین `J` (ASCII 74) است.
- اگر Phred+33 باشد: Q = 38 − 33 = **۵** تا 74 − 33 = **۴۱**. این بازه دقیقاً بازه‌ی Illumina 1.8+ است.
- اگر Phred+64 بود، `&` به Q منفی (−۲۶) می‌رسید که ممکن نیست.

پس کدگذاری **Phred+33** و بیشترین کیفیت **Q41** است.

### ۴.۵ (اختیاری)
```bash
wget -q https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR688/ERR688359/ERR688359.fastq.gz
md5sum ERR688359.fastq.gz      # باید 891ae71035f90e8fefe6699bbeb0f90a باشد
```

---

## تمرین ۵: GCA یا GCF؟

```bash
datasets summary genome accession GCF_000005845.2 --report sequence --as-json-lines | jq -r '"\(.genbank_accession)  \(.refseq_accession)"'
```
```text
U00096.3  NC_000913.3
```
در اسمبلی GCA نام کروموزوم **`U00096.3`** است و در GCF **`NC_000913.3`**. توالی یکی است، ولی اگر ریدها را روی FASTA نسخه‌ی GCA map کنید، فایل BAM نام `U00096.3` را دارد و GFF نسخه‌ی GCF نام `NC_000913.3` را. ابزارهای شمارش (مثل featureCounts) و نمایشگرها (IGV) **هیچ تطابقی پیدا نمی‌کنند**: یا صفر رید به ژن‌ها نسبت داده می‌شود، یا خطای «sequence not found» می‌گیرید.

علاوه بر نام‌ها، **آنوتیشن** دو نسخه هم می‌تواند فرق کند: آنوتیشن ثبت‌شده توسط نویسندگان در برابر PGAP در NCBI. **راه درست:** FASTA و GFF را همیشه از **یک** اسمبلی (و یک نسخه) بردارید.

---

## تمرین ۶ (چالشی): خلاصه‌ی نمونه‌محور

اسکریپت پاسخ در [scripts/project_summary.sh](scripts/project_summary.sh) است. نکته‌ی کلیدی‌اش این است که ستون‌ها را **با نام** پیدا می‌کند، نه با شماره، چون ENA همیشه `run_accession` را اول می‌گذارد. نسخه‌ی اول همین اسکریپت که با شماره‌ی ستون نوشته شده بود دقیقاً به همین دلیل خروجی غلط می‌داد.

```bash
bash ../scripts/project_summary.sh PRJEB7774 > PRJEB7774_samples.tsv
head -3 PRJEB7774_samples.tsv
tail -n +2 PRJEB7774_samples.tsv | cut -f2 | sort | uniq -c
tail -n +2 PRJEB7774_samples.tsv | sort -t$'\t' -k4,4n | sed -n '1p;$p'
```
```text
sample	n_runs	layouts	total_reads
SAMEA3136623	2	PAIRED,SINGLE	19967424
SAMEA3136624	2	SINGLE,PAIRED	26034931
    156 2
SAMEA3136709	2	SINGLE,PAIRED	16312237
SAMEA3136692	2	SINGLE,PAIRED	40653767
```

1. **۱۵۶ نمونه** و **هر نمونه دقیقاً ۲ Run** (یکی SINGLE و یکی PAIRED). ترتیب در ستون layouts مهم نیست.
2. کمترین مجموع: `SAMEA3136709` (۱۶٫۳ میلیون)؛ بیشترین: `SAMEA3136692` (۴۰٫۷ میلیون).
3. **ایراد مفهومی:** در ENA، `read_count` برای Run دوخوانه تعداد **جفت‌ها (spots)** است، نه تعداد کل ریدها. یعنی ۳۲ میلیون در یک Run پیرد-اند برابر ۶۴ میلیون رید است. جمع آن با تعداد ریدهای single-end دو واحد متفاوت را جمع می‌کند. علاوه بر این، دو Run از **دو کتابخانه‌ی متفاوت** (ERX متفاوت) با طول و نوع خوانش متفاوت هستند و نباید کورکورانه ادغام شوند. معیار بهتر برای مقایسه‌ی عمق نمونه‌ها `base_count` است، یا تحلیل فقط با Run پیرد-اند.
