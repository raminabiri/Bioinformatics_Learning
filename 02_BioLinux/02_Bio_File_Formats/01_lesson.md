# درس: فرمت‌های داده‌ی زیستی

**بخش:** `02_BioLinux` · **ماژول:** `02_Bio_File_Formats` · **پیش‌نیاز:** 01_Bash_Linux · **زمان:** ۲ ساعت · **ابزار:** samtools 1.20، bcftools 1.21، seqkit 2.13 · **آخرین تست:** 2026-10-13

---

## ۱. مسئله

هر ابزار بیوانفورماتیک فرمت مشخصی را می‌خواند و می‌نویسد. بیشتر خطاهای بی‌صدا از **سوءتفاهم درباره‌ی فرمت** می‌آیند: مختصات مبنای ۰ در برابر ۱، FASTA چندخطی، رمزگذاری کیفیت، یا نام کروموزوم ناهمخوان (بخش 00/02، تمرین GCA در برابر GCF).

این درس هفت فرمت اصلی را با **فایل‌های واقعی همین دوره** نشان می‌دهد:
```bash
cd 02_BioLinux/02_Bio_File_Formats
bash scripts/make_examples.sh      # نیاز به داده‌ی 01/01 و خروجی ماژول‌های 06/01 و 06/02
ls data/
```

| فرمت | چه چیزی | مختصات | نسخه‌ی فشرده/ایندکس | ابزار |
| :--- | :--- | :-: | :--- | :--- |
| FASTA | توالی | — | `.fai` (samtools faidx) | seqkit، samtools |
| FASTQ | ریدها + کیفیت | — | `.gz` | seqkit، fastp |
| GFF3/GTF | آنوتیشن (ژن‌ها) | **مبنای ۱، دوسر بسته** | bgzip + tabix | awk، bedtools |
| GenBank | توالی + آنوتیشن + metadata | مبنای ۱ | — | Biopython |
| BED | بازه‌های ژنومی | **مبنای ۰، نیمه‌باز** | bgzip + tabix | bedtools |
| SAM/BAM/CRAM | همترازی ریدها | **POS مبنای ۱** | BAM + `.bai` | samtools |
| VCF/BCF | واریانت‌ها | **POS مبنای ۱** | `.vcf.gz` + `.tbi` | bcftools |

## ۲. FASTA
```bash
head -n 3 data/ecoli_10kb.fa
```
```text
>NC_000913.3:1-10000
AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTC
TGATAGCAGCTTCTGAACTGGTTACCTGCCGTGAGTAAATTAAAATTTTATTGACTTAGG
```
- خط هدر با `>` شروع می‌شود. **اولین کلمه** (تا فاصله) شناسه است و بقیه‌ی خط توضیح است. بیشتر ابزارها فقط شناسه را نگه می‌دارند.
- توالی می‌تواند در یک خط یا چند خط با طول ثابت (معمولاً ۶۰ یا ۸۰) باشد. **هر کدی که FASTA می‌خواند باید چندخطی را پشتیبانی کند** (دام ATG در 01/01).
- **ایندکس `.fai`:** دسترسی تصادفی به هر ناحیه بدون خواندن کل فایل:
  ```bash
  samtools faidx ../01_Bash_Linux/data/ecoli_k12.fna NC_000913.3:4181245-4185273 | head -2
  cat ../01_Bash_Linux/data/ecoli_k12.fna.fai
  ```
  ```text
  >NC_000913.3:4181245-4185273
  ATGGTTTACTCCTATACCGAGAAAAAACGTATTCGTAAGGATTTTGGTAAACGTCCACAAGTTCTGGATGTACCTTATCT
  NC_000913.3	4641652	72	80	81
  ```
  ستون‌های `.fai`: نام، طول، محل شروع توالی در فایل (بایت)، باز در هر خط، بایت در هر خط. ناحیه‌ی بالا همان ژن rpoB است و با `ATG` شروع می‌شود.

## ۳. FASTQ
```bash
head -n 4 data/minigut_3reads.fastq
```
```text
@NC_006347.1_0/1
AACGTTGGCTCGTCTGACAAGCAAAGGTAAGAACAAAGGTGCCAAATATCGTAAAGAAAAACGTGACATGGCGTCCAACCGTATGCAGGA...
+
BBBBBFFFFFFFFFFFFFFFFFF/FFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF...
```
- هر رکورد **دقیقاً ۴ خط** است: `@`نام، توالی، `+`، کیفیت. طول خط کیفیت برابر طول توالی است.
- کیفیت: Q = کد ASCII − 33 (Phred+33). `F` = Q37، `B` = Q33، `/` = Q14. (جزئیات در 06/01، درس FastQC.)
- **چرا `grep -c '^@'` تعداد رید نیست؟** چون `@` (Q31) می‌تواند اولین کاراکتر **خط کیفیت** هم باشد. روی داده‌ی شبیه‌سازی‌شده‌ی دوره این اتفاق نمی‌افتد، ولی روی یک فایل واقعی MiSeq (آمپلیکون SARS-CoV-2 از nf-core/test-datasets، شاخه‌ی `viralrecon`) نتیجه این است:
  ```text
  ریدهای واقعی (خطوط ÷ ۴):   27,721
  grep -c '^@':              27,829   ← ۱۰۸ خط کیفیت با @ شروع شده‌اند
  ```
  همیشه تعداد خطوط ÷ ۴ یا ابزار تخصصی (`seqkit stats`).
- فایل‌های پیرد-اند: `_R1` و `_R2`، رید n‌ام یکی جفت رید n‌ام دیگری است.

## ۴. GFF3
```bash
cat data/rpoB.gff3 | cut -c1-150
```
```text
##gff-version 3
##sequence-region NC_000913.3 1 4641652
NC_000913.3	RefSeq	region	1	4641652	.	+	.	ID=NC_000913.3:1..4641652;...
NC_000913.3	RefSeq	gene	4181245	4185273	.	+	.	ID=gene-b3987;Dbxref=ECOCYC:EG10894,GeneID:948488;Name=rpoB;...
NC_000913.3	RefSeq	CDS	4181245	4185273	.	+	0	ID=cds-NP_418414.1;Parent=gene-b3987;...
```
۹ ستون با **Tab**: seqid، منبع، نوع (`gene`، `CDS` و …)، **شروع، پایان (مبنای ۱، دوسر بسته)**، امتیاز، رشته، فاز، و ویژگی‌ها به‌صورت `key=value;...`.
- رابطه‌ی سلسله‌مراتبی با `ID` و `Parent` ساخته می‌شود: CDS فرزند gene است.
- **فاز** (ستون ۸) فقط برای CDS است: چند باز از ابتدای این قطعه باید رد شود تا به اولین کدون کامل برسیم.
- **GTF** نسخه‌ی قدیمی‌تر و رایج در ترنسکریپتومیکس است: همان ۹ ستون، ولی ستون ۹ به شکل `gene_id "x"; transcript_id "y";`.

## ۵. GenBank
```bash
head -n 7 data/rpoB.gb ; grep -n -A2 '     CDS' data/rpoB.gb
```
```text
LOCUS       NC_000913               4029 bp    DNA     linear   CON 02-SEP-2026
DEFINITION  Escherichia coli str. K-12 substr. MG1655, complete genome.
ACCESSION   NC_000913 REGION: 4181245..4185273
VERSION     NC_000913.3
DBLINK      BioProject: PRJNA57779
            BioSample: SAMN02604091
KEYWORDS    RefSeq.
164:     CDS             1..4029
165:                     /gene="rpoB"
```
GenBank **توالی، آنوتیشن، ارجاع به مقالات و metadata** را در یک فایل انسان‌خوان دارد. بخش‌ها: سرآیند (LOCUS تا REFERENCE)، **FEATURES** (ژن‌ها با `/qualifier`ها، از جمله `/translation` = توالی پروتئین)، و **ORIGIN** (توالی با شماره‌گذاری). مختصات این فایل **نسبت به ناحیه‌ی دانلودشده** است (`1..4029`)، نه کل ژنوم. برای خواندن برنامه‌نویسی‌شده از Biopython استفاده کنید (بخش ۰۲). Prokka و Bakta (بخش ۰۷) GenBank هم تولید می‌کنند.

## ۶. BED، و تله‌ی مبنای ۰
```bash
cat data/rpoB.bed
```
```text
NC_000913.3	4181244	4185273	rpoB	0	+
```
همان ژن rpoB در GFF با `4181245  4185273` آمده بود و در BED با `4181244  4185273`. هر دو **یک بازه‌اند**:

| سیستم | فرمت‌ها | اولین باز ژنوم | بازه‌ی rpoB | طول |
| :--- | :--- | :-: | :-: | :-: |
| مبنای ۱، دوسر بسته `[start, end]` | GFF، SAM، VCF، GenBank، رشته‌ی ناحیه در samtools | 1 | 4181245–4185273 | end − start + 1 = 4029 |
| مبنای ۰، نیمه‌باز `[start, end)` | BED، BAM (داخلی)، Python/C | 0 | 4181244–4185273 | end − start = 4029 |

**تبدیل GFF → BED:** `start − 1` و `end` بدون تغییر. فراموش کردن این ۱ باز خطای «off-by-one» است: یک باز اضافه یا کم، کدون جابه‌جا، و SNP روی باز اشتباه.

## ۷. SAM/BAM
```bash
grep -v '^@' data/example.sam | cut -f1-9
```
```text
HUMAN_chr21_chr21part_481728_482004_...   163  chr21part  99950   1  126M  =  100101   277
HUMAN_chr21_chr21part_99769_100198_...    83   chr21part  100073  1  126M  =  99769    -430
```
۱۱ ستون اجباری: QNAME، **FLAG**، RNAME، **POS** (مبنای ۱)، **MAPQ**، **CIGAR**، RNEXT (`=` یعنی همان کروموزوم)، PNEXT، **TLEN** (طول قطعه؛ مثبت برای mate سمت چپ و منفی برای mate سمت راست)، SEQ، QUAL. بعد از این‌ها تگ‌های اختیاری می‌آیند (`AS:i:`، `XS:i:`، `NM:i:` …).
- خطوط `@` سرآیندند: `@SQ` نام و طول مرجع، و `@PG` **تاریخچه‌ی برنامه‌ها با دستور کامل**. سرآیند BAM خودش ثبت تکرارپذیری است.
- **BAM** نسخه‌ی باینری فشرده‌ی SAM است. برای دسترسی تصادفی باید **مرتب** (`samtools sort`) و **ایندکس** (`samtools index` → `.bai`) شود. **CRAM** فشرده‌تر است ولی به مرجع وابسته است.
- FLAG، MAPQ و `samtools` در 06/02 با جزئیات آمده‌اند.

## ۸. VCF
```bash
bcftools view -h data/chr21_spiked.vcf.gz | tail -1
bcftools view -H data/chr21_spiked.vcf.gz | head -2 | cut -f1-10
```
```text
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	../../06_Metagenomics/work/02_host/bam/minigut_spiked.host.bam
chr21part	118488	.	A	T	9.87615	.	DP=4;VDB=0.72;...;MQ=42	GT:PL:AD	0/1:42,0,42:2,2
chr21part	121974	.	A	C	35.2857	.	DP=4;VDB=0.965037;...;MQ=24	GT:PL:AD	1/1:62,5,0:1,3
```
این VCF واقعی است. با `bcftools mpileup | bcftools call` از BAM ماژول 06/02 ساخته شده و جهش‌هایی را پیدا کرده که `wgsim` عمداً در ریدهای انسانی شبیه‌سازی‌شده گذاشته بود.
- `##` متادیتاست (تعریف هر فیلد INFO و FORMAT). `#CHROM` سطر سرستون است. **ستون‌های ۱۰ به بعد نمونه‌ها هستند.**
- **GT:** `0/1` ناهم‌زیگوت، `1/1` هم‌زیگوت جایگزین. **AD:** تعداد رید مرجع و جایگزین. **PL:** درست‌نمایی ژنوتیپ‌ها (Phred).
- **indel‌ها در VCF با یک باز «لنگر» قبلی نوشته می‌شوند** (مثلاً `REF=AT ALT=A` برای حذف T). موقعیت indel در VCF یک باز قبل از خود تغییر است.

```bash
bcftools stats data/chr21_spiked.vcf.gz | grep -E '^SN.*(records|SNPs|indels)'
```
```text
SN	0	number of records:	98
SN	0	number of SNPs:	87
SN	0	number of indels:	11
```

**مقایسه با حقیقت:** `wgsim` ۳۸۷ جهش ساخته بود (`data/chr21_true_mutations.txt`). از ۹۸ واریانت فراخوانی‌شده، **۸۴ مورد** در موقعیت یک جهش واقعی‌اند: precision حدود ۸۶٪، ولی recall فقط **۲۲٪**. دلیل: **میانگین عمق پوشش ۲٫۶×** است (`samtools depth`) و ۲۳٪ ناحیه هیچ ریدی ندارد. فراخوانی ژنوتیپ با ۲ یا ۳ رید ممکن نیست. **درس:** VCF فقط می‌گوید چه چیزی **دیده شد**. نبودن واریانت در VCF به معنی نبودنش در نمونه نیست، مگر اینکه پوشش آن ناحیه را هم گزارش کنید (تمرین ۶).

## ۹. فشرده‌سازی و ایندکس
- `gzip` معمولی دسترسی تصادفی ندارد. **`bgzip`** (فشرده‌سازی بلوکی) سازگار با gzip است و با **`tabix`** ایندکس می‌شود. این‌طوری می‌شود ناحیه‌ای از VCF یا BED/GFF مرتب‌شده را بدون خواندن کل فایل گرفت:
  ```bash
  bcftools view -H -r chr21part:118000-122000 data/chr21_spiked.vcf.gz | cut -f1-5
  ```
- ایندکس‌ها: `.fai` (FASTA)، `.bai`/`.csi` (BAM)، `.tbi`/`.csi` (VCF، BED، GFF با bgzip). اگر فایل اصلی عوض شود، ایندکس باید دوباره ساخته شود.

## ۱۰. دام‌ها (Pitfalls)

| دام | چرا مشکل است | راه درست |
| :--- | :--- | :--- |
| مبنای ۰ در برابر ۱ | off-by-one در تبدیل GFF ↔ BED | BED = (start−1, end) |
| `grep -c '^@'` برای شمارش رید | `@` در خط کیفیت هم هست | خطوط ÷ ۴، یا `seqkit stats` |
| نام توالی ناهمخوان (`chr1` در برابر `1`، `NC_` در برابر `U00096`) | ابزارها هیچ تطابقی پیدا نمی‌کنند | FASTA، GFF، BAM و VCF از یک منبع و یک نسخه |
| ایندکس قدیمی بعد از تغییر فایل | نتیجه‌ی غلط یا خطای مبهم | بعد از هر تغییر ایندکس دوباره |
| `gzip` به‌جای `bgzip` برای VCF | tabix کار نمی‌کند | `bgzip` یا `bcftools view -Oz` |
| «واریانت در VCF نیست» = «واریانت نیست» | پوشش کم دیده نمی‌شود | پوشش و ناحیه‌های فراخوانی‌پذیر را گزارش کنید |
| هدر FASTA با فاصله و کاراکترهای خاص | بعضی ابزارها نام را می‌شکنند | شناسه‌ی کوتاه بدون فاصله (`sed`، 01/01) |

## ۱۱. جمع‌بندی
- هفت فرمت، دو سیستم مختصات: BED مبنای ۰ و نیمه‌باز است؛ GFF، SAM و VCF مبنای ۱ و دوسر بسته‌اند.
- فرمت‌های بزرگ (FASTA، BAM، VCF) با **ایندکس** دسترسی تصادفی پیدا می‌کنند.
- سرآیندها (`@PG` در BAM، `##` در VCF) سابقه‌ی تحلیل را نگه می‌دارند. آن‌ها را نگه دارید و بخوانید.

---

## منابع

### مشخصات رسمی فرمت‌ها و مقالات
- مشخصات رسمی SAM/BAM/CRAM/VCF (hts-specs): https://samtools.github.io/hts-specs/
- Cock PJA, et al. (2010). The Sanger FASTQ file format for sequences with quality scores, and the Solexa/Illumina FASTQ variants. *Nucleic Acids Res.* 38(6):1767–1771. https://doi.org/10.1093/nar/gkp1137
- Li H, et al. (2009). The Sequence Alignment/Map format and SAMtools. *Bioinformatics* 25(16):2078–2079. https://doi.org/10.1093/bioinformatics/btp352
- Danecek P, et al. (2011). The variant call format and VCFtools. *Bioinformatics* 27(15):2156–2158. https://doi.org/10.1093/bioinformatics/btr330
- Danecek P, et al. (2021). Twelve years of SAMtools and BCFtools. *GigaScience* 10(2):giab008. https://doi.org/10.1093/gigascience/giab008
- Buffalo V. *Bioinformatics Data Skills*, فصل‌های ۶ و ۱۰: https://vincebuffalo.com/book/

### ویدیوهای آموزشی
- GenoMediCon — *Essential Genomic File Formats for Beginners: FASTA, FASTQ, SAM/BAM, and VCF Explained*: https://www.youtube.com/watch?v=BaVBesblyxw
- Bioinformagician — *Understanding Bioinformatics File Formats: SAM/BAM*: https://www.youtube.com/watch?v=vh6l9aPFUgU
- Bioinformagician — *Understanding File Formats in Bioinformatics: VCF and gVCF*: https://www.youtube.com/watch?v=cBDZSGf9HRE

> لینک‌ها در تاریخ 2026-10-13 بررسی شدند (`_tools/check_links.sh`).
