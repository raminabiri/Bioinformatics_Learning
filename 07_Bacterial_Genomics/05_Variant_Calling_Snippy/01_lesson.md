<div dir="rtl">

# درس: فراخوانی واریانت در باکتری با Snippy

**بخش:** `07_Bacterial_Genomics` · **ماژول:** `05_Variant_Calling_Snippy` · **پیش‌نیاز:** ماژول [MLST](../03_MLST_Molecular_Typing/)؛ [Bowtie2/samtools](../../06_Metagenomics/02_Host_Removal_Alignment/)؛ [VCF](../../02_BioLinux/04_Align_Variant_Formats/) · **زمان:** حدود ۷۵ دقیقه · **ابزار (از مستندات):** Snippy، snippy-core، snp-dists، Gubbins · **آخرین بازبینی:** 2026-10-21

> ✍️ **وضعیت: نوشته‌شده، اجرا نشده.** نمونه‌خروجی‌ها از README رسمی Snippy آمده‌اند (منبع کنار هر کدام). جدول‌های تمرینی **فرضی**‌اند و برچسب دارند.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. بگویید فراخوانی واریانت با مرجع چه فرقی با اسمبلی de novo دارد و مرجع را چگونه برگزینید.
2. ‏Snippy را برای یک ایزوله اجرا کنید و `snps.tab` را بخوانید.
3. جهش‌های شناخته‌شده‌ی مقاومت در **gyrA** (QRDR) و **rpoB** (RRDR) را پیدا و تفسیر کنید.
4. با snippy-core هم‌ترازی هسته‌ی SNP بسازید، فاصله‌ی SNP دو به دو را حساب کنید و به پرسش «آیا انتقال رخ داده؟» پاسخ محتاطانه بدهید.

---

## ۱. داستان

ماژول ۰۳ پرسید: سه ایزوله‌ی ST258 از یک بخش، **یک شیوع**‌اند؟ MLST تنها گفت «سازگار است». اکنون به کل ژنوم نگاه می‌کنیم: میان هر دو ایزوله **چند SNP** فرق است؟ و در کنارش: ایزوله‌ی مقاوم به سیپروفلوکساسین **کدام جهش** را در gyrA دارد؟ هر دو پرسش را یک کار پاسخ می‌دهد: **نشاندن ریدها روی یک ژنوم مرجع و یافتن تفاوت‌ها**.

---

## ۲. مفهوم به زبان ساده

### ۲.۱ با مرجع، نه از صفر

در اسمبلی (ماژول ۰۱) ژنوم را از صفر می‌سازیم. در **فراخوانی واریانت**، ریدها را روی یک ژنوم **مرجع** می‌نشانیم (همانند برداشتن میزبان در بخش ۰۶) و هر جایگاهی را که ریدها همه با مرجع فرق دارند، گزارش می‌کنیم.

<div dir="ltr">

```text
reference  ...ACGTTGCA[T]CGGA...
read 1        CGTTGCA[C]CGG
read 2      ...ACGTTGCA[C]C
read 3           TTGCA[C]CGGA...
                       ^ 3 of 3 reads say C: SNP T->C
```

</div>

| گونه‌ی واریانت (`TYPE` در Snippy) | نمونه |
| :--- | :--- |
| ‏`snp` | یک باز عوض شده: `A → G` |
| ‏`mnp` | چند باز پشت سر هم عوض شده: `GA → CT` |
| ‏`ins` / `del` | درج / حذف: `ATT → ATTT` |
| ‏`complex` | ترکیبی از این‌ها |

### ۲.۲ کی یک واریانت «باور» می‌شود؟

به گفته‌ی README Snippy:
- ‏**`--mincov`**: کمترین شمار ریدهای روی یک جایگاه (پیش‌فرض **۱۰**).
- ‏**`--minfrac`**: کمترین **سهم** ریدهایی که باید با مرجع فرق داشته باشند؛ README می‌گوید «مقدارهای ۱۰ و ۰٫۹ رایج‌اند».
- ‏**`--minqual`**: کمترین «کیفیت» فراخوانی در VCF (پیش‌فرض ۱۰۰).

چرا ۰٫۹؟ باکتری هاپلوئید است: در یک کشت خالص، همه‌ی ریدها در یک جایگاه **یک** باز را می‌گویند. جایگاهی با ۵۰٪ A و ۵۰٪ G یعنی **کشت مخلوط** یا ناحیه‌ی تکراری، نه یک SNP.

### ۲.۳ برگزیدن مرجع

**مرجع نزدیک‌تر = بهتر.** با مرجعی دور، بخشی از ژنوم ایزوله‌ها اصلاً روی مرجع نمی‌نشیند (ژن‌هایی که مرجع ندارد) و آن نواحی دیده نمی‌شوند؛ و ریدهای نواحی بسیار گوناگون نادرست می‌نشینند. برای پرسش شیوع، بهترین مرجع یک ژنوم **بسته** از همان ST است (یا یکی از ایزوله‌های خود شیوع، با اسمبلی خوب). برای **شماره‌گذاری استاندارد جهش‌های مقاومت** در *E. coli*، مرجع K-12 (`NC_000913.3`) رایج است.

---

## ۳. گام ۱: اجرای Snippy برای یک ایزوله (از مستندات)

مرجع را به شکل **GenBank** بدهید تا Snippy نام ژن و اثر هر واریانت را هم بنویسد. GenBank مرجع K-12 را با `curl` (بخش ۰۱) می‌گیرید:

<div dir="ltr">

```bash
curl -s -o ecoli_k12.gbk \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000913.3&rettype=gbwithparts&retmode=text"
snippy --cpus 8 --outdir iso1_snps --ref ecoli_k12.gbk --R1 iso1_R1.fastq.gz --R2 iso1_R2.fastq.gz
```

</div>

| بخش | چیست |
| :--- | :--- |
| ① `--cpus 8` | هسته‌ها |
| ② `--outdir` | پوشه‌ی خروجی (یکی برای هر ایزوله) |
| ③ `--ref` | مرجع: FASTA یا **GenBank** (برای آنوتیشن واریانت‌ها)؛ می‌تواند چند کانتیگ باشد |
| ④ `--R1` / `--R2` | ریدهای جفتی (FASTQ، فشرده هم) |

(نمونه‌ی Quick Start در README: `snippy --cpus 16 --outdir mysnps --ref Listeria.gbk --R1 FDA_R1.fastq.gz --R2 FDA_R2.fastq.gz`.)

درون Snippy همان گام‌های آشناست: نشاندن ریدها با یک ابزار هم‌ترازی (`snps.bam`؛ بخش ۰۶)، فراخوانی واریانت به VCF (بخش ۰۲)، و آنوتیشن اثر هر واریانت روی ژن‌ها (snpEff).

---

## ۴. گام ۲: خواندن `snps.tab` (از مستندات)

خروجی‌های اصلی (README): `snps.vcf`، `snps.tab`، `snps.csv`، `snps.html`، `snps.bam`، و:
- ‏`snps.aligned.fa`: مرجع، با `-` جایی که پوشش صفر است و `N` جایی که پوشش کمتر از `--mincov` است (بی واریانت).
- ‏`snps.consensus.fa`: مرجع با همه‌ی واریانت‌ها اعمال‌شده.

نمونه‌ی `snps.tab` (**از مستندات**: README Snippy؛ ستون‌ها برای پهنای صفحه فشرده شده‌اند):

<div dir="ltr">

```text
CHROM  POS     TYPE    REF   ALT    EVIDENCE        FTYPE STRAND NT_POS AA_POS LOCUS_TAG GENE PRODUCT EFFECT
chr      5958  snp     A     G      G:44 A:0        CDS   +      41/600 13/200 ECO_0001  dnaA replication protein DnaA missense_variant c.548A>C p.Lys183Thr
chr     45722  ins     ATT   ATTT   ATTT:43 ATT:1   CDS   -                    ECO_0045  gyrA DNA gyrase
chr    100541  del     CAAA  CAA    CAA:38 CAAA:1   CDS   +                    ECO_0179      hypothetical protein
plas     3221  mnp     GA    CT     CT:39 CT:0      CDS   +                    ECO_p012  rep  hypothetical protein
```

</div>

| ستون | معنی |
| :--- | :--- |
| `CHROM` / `POS` | کدام توالی مرجع (کروموزوم، پلاسمید) و کدام جایگاه |
| `TYPE` / `REF` / `ALT` | گونه‌ی واریانت، باز مرجع، باز ایزوله |
| `EVIDENCE` | شمار ریدها برای هر باز: `G:44 A:0` = ۴۴ رید G و هیچ رید A، یعنی SNP بسیار مطمئن |
| `FTYPE` / `STRAND` | گونه‌ی ویژگی (CDS، tRNA) و رشته‌ی ژن |
| `NT_POS` / `AA_POS` | جایگاه در ژن / در پروتئین، به شکل «جایگاه/طول» |
| `LOCUS_TAG` / `GENE` / `PRODUCT` | ژن آسیب‌دیده |
| `EFFECT` | اثر (snpEff): `missense_variant` (تغییر اسیدآمینه)، `synonymous_variant`، `stop_gained`، … با تغییر نوکلئوتید (`c.`) و پروتئین (`p.`) |

‏`p.Lys183Thr` یعنی «اسیدآمینه‌ی ۱۸۳، لیزین، به ترئونین تبدیل شد».

---

## ۵. گام ۳: جهش‌های مقاومت (gyrA و rpoB)

| ژن | ناحیه | آنتی‌بیوتیک | جهش‌های شناخته‌شده در *E. coli* (شماره‌گذاری *E. coli*) |
| :--- | :--- | :--- | :--- |
| ‏*gyrA* | ‏**QRDR** (ناحیه‌ی تعیین‌کننده‌ی مقاومت به کینولون، کمابیش اسیدآمینه‌ی ۶۷ تا ۱۰۶) | فلوروکینولون‌ها (سیپروفلوکساسین) | ‏**S83L**، **D87N** (یا D87Y/G) |
| ‏*parC* | ‏QRDR | فلوروکینولون‌ها | ‏S80I، E84V |
| ‏*rpoB* | ‏**RRDR** (ناحیه‌ی تعیین‌کننده‌ی مقاومت به ریفامپیسین، کمابیش ۵۰۷ تا ۵۳۳) | ریفامپیسین | ‏S531L، H526Y/D، D516V |

بیرون کشیدن این ژن‌ها از `snps.tab`:

<div dir="ltr">

```bash
grep -E 'gyrA|parC|rpoB' iso1_snps/snps.tab
```

</div>

**الگوی بالینی:** سطح بالای مقاومت به سیپروفلوکساسین بیشتر **دو** جهش در gyrA (S83L + D87N) و یک جهش در parC می‌خواهد؛ یک جهش gyrA تنها، بیشتر حساسیت را کم می‌کند. پس **شمار و ترکیب** جهش‌ها را گزارش کنید، و جهش‌های ژنی را کنار ژن‌های پلاسمیدی مقاومت (*qnr*، بخش ۰۸) بگذارید.

<details>
<summary>✋ امتحان کن: <code>AA_POS</code> برابر <code>83/875</code> و <code>EFFECT</code> شامل <code>p.Ser83Leu</code> در ژن gyrA. چه می‌گویید؟</summary>

جهش کلاسیک **S83L** در QRDR ژن gyrA: سرین ۸۳ به لوسین. شایع‌ترین جهش مقاومت به فلوروکینولون در *E. coli*. برای سطح مقاومت، دنبال D87 در gyrA و S80/E84 در parC هم بگردید.

</details>

---

## ۶. گام ۴: چند ایزوله، هسته‌ی SNP، و فاصله‌ها (از مستندات)

برای هر ایزوله یک Snippy با **همان** مرجع، سپس:

<div dir="ltr">

```bash
snippy-core --prefix core iso1_snps iso2_snps iso3_snps iso4_snps
```

</div>

خروجی‌ها (README):

| فایل | چیست |
| :--- | :--- |
| `core.aln` | هم‌ترازی **تنها جایگاه‌های SNP هسته** (پیش‌فرض FASTA) |
| `core.full.aln` | هم‌ترازی کل ژنوم، با جایگاه‌های بی‌تغییر |
| `core.tab` / `core.vcf` | جدول و VCF همه‌ی SNPهای هسته |
| `core.txt` | آمار هر ایزوله: طول، بخش هم‌ترازشده، شمار واریانت‌ها |

برای بسیاری ایزوله، `snippy-multi` از یک جدول (`ID R1 R2`) یک اسکریپت می‌سازد که همه را اجرا و در پایان `snippy-core` را هم اجرا می‌کند.

**فاصله‌ی SNP دو به دو** با ابزار `snp-dists` (از همان نویسنده):

<div dir="ltr">

```bash
snp-dists core.aln > distances.tsv
```

</div>

خروجی یک ماتریس است: شمار SNPهای میان هر دو ایزوله.

### بازترکیبی: SNPهایی که یکجا می‌آیند

یک رویداد **بازترکیبی** (یک تکه‌ی DNA از سویه‌ای دیگر) در یک گام ده‌ها SNP می‌آورد (ماژول ۰۳، تمرین ۵). برای درخت و فاصله‌های درست، این نواحی برداشته می‌شوند. گردش کار README:

<div dir="ltr">

```bash
snippy-clean_full_aln core.full.aln > clean.full.aln
run_gubbins.py -p gubbins clean.full.aln
snp-sites -c gubbins.filtered_polymorphic_sites.fasta > clean.core.aln
FastTree -gtr -nt clean.core.aln > clean.core.tree
```

</div>

‏(Gubbins نواحی بازترکیب را می‌یابد؛ `snp-sites` تنها جایگاه‌های SNP را نگه می‌دارد؛ FastTree درخت می‌سازد. درخت و تفسیرش: بخش ۰۸.)

---

## ۷. گام ۵: «آیا انتقال رخ داده؟»، پاسخ محتاطانه

| فاصله‌ی SNP (هسته، پس از برداشتن بازترکیب) | تفسیر رایج |
| :--- | :--- |
| ۰ تا چند SNP | انتقال اخیر **محتمل**، اگر اپیدمیولوژی هم سازگار باشد |
| ده‌ها SNP | بیشتر **ورود جدا** از یک دودمان مشترک |
| صدها SNP یا بیشتر | بی‌گمان ورود جدا |

مرز دقیق **به گونه و ریتم جهش آن بستگی دارد** (و به اینکه نمونه‌ها در چه بازه‌ی زمانی گرفته شده‌اند)؛ یک عدد همگانی وجود ندارد. فاصله‌ی SNP **نمی‌گوید چه کسی به چه کسی**، تنها می‌گوید کدام ایزوله‌ها نزدیک‌اند. همیشه با داده‌ی اپیدمیولوژیک (زمان، مکان، تماس) کنار هم بخوانید.

---

## ۸. سه اشتباه رایج

**۱. مرجع دور.** با یک مرجع از دودمان دیگر، بخشی از ژنوم دیده نمی‌شود و SNPهای ساختگی در نواحی گوناگون پدید می‌آید. برای شیوع، مرجعی از همان ST (بهتر بسته).

**۲. نادیده گرفتن `EVIDENCE` و جایگاه‌های ناهمگن.** جایگاهی با ریدهای نیم‌به‌نیم (برای نمونه `G:20 A:18`) SNP نیست؛ نشانه‌ی کشت مخلوط یا ناحیه‌ی تکراری است. اگر بسیار است، کیفیت کشت را بسنجید (ماژول ۰۱).

**۳. فاصله‌ی SNP بی برداشتن بازترکیب و تکرارها.** یک رویداد بازترکیبی می‌تواند دو ایزوله‌ی یک شیوع را «ده‌ها SNP دور» نشان دهد. Gubbins (یا ابزار همانند)، و پوشاندن نواحی تکراری با `--mask` (یک فایل BED).

---

## 📘 برای کنجکاوها

- ‏**‏`--mask`:** فایل BED نواحی‌ای که نباید SNP از آن‌ها گزارش شود؛ README نمونه‌ی ژن‌های تکراری *M. tuberculosis* را می‌آورد.
- ‏**‏`snps.aligned.fa` و `N`:** این‌ها برای snippy-core مهم‌اند: جایگاهی که در یک ایزوله `N` یا `-` است، در «هسته» شمرده نمی‌شود؛ هسته با افزودن هر ایزوله‌ی کم‌پوشش کوچک‌تر می‌شود.
- **پایگاه‌های مقاومت:** AMRFinderPlus و CARD/RGI جهش‌های نقطه‌ای مقاومت را هم می‌شناسند (بخش ۰۸)؛ Snippy همه‌ی تفاوت‌ها را می‌دهد و تفسیر با شماست.

---

## جمع‌بندی

- فراخوانی واریانت = نشاندن ریدها روی مرجع + یافتن جایگاه‌هایی که ریدها (≥ ۱۰، و ≥ ۹۰٪) با مرجع فرق دارند.
- ‏`snps.tab`: هر واریانت با شواهد (`EVIDENCE`)، ژن و اثر روی پروتئین.
- جهش‌های مقاومت: gyrA S83L/D87N (و parC)، rpoB در RRDR؛ شمار و ترکیب را گزارش کنید.
- ‏snippy-core → `core.aln` → snp-dists؛ بازترکیب را با Gubbins بردارید؛ فاصله‌ی SNP را با اپیدمیولوژی بخوانید.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
snippy --cpus 8 --outdir X_snps --ref ref.gbk --R1 X_R1.fq.gz --R2 X_R2.fq.gz
grep -E 'gyrA|parC|rpoB' X_snps/snps.tab
snippy-core --prefix core A_snps B_snps C_snps
snp-dists core.aln > distances.tsv
snippy-clean_full_aln core.full.aln > clean.full.aln
run_gubbins.py -p gubbins clean.full.aln
snp-sites -c gubbins.filtered_polymorphic_sites.fasta > clean.core.aln
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| واریانت | هر تفاوت ژنوم ایزوله با مرجع (SNP، درج، حذف) |
| ‏SNP | تفاوت در یک باز |
| ‏missense / synonymous | جهشی که اسیدآمینه را عوض می‌کند / نمی‌کند |
| ‏QRDR / RRDR | نواحی تعیین‌کننده‌ی مقاومت به کینولون / ریفامپیسین |
| هسته‌ی SNP | جایگاه‌هایی که در همه‌ی ایزوله‌ها پوشش کافی دارند |
| بازترکیبی | جایگزینی یک تکه‌ی DNA با تکه‌ای از سویه‌ای دیگر |

---

## منابع

**مستند و مقاله**
- Seemann T. *Snippy: rapid haploid variant calling and core genome alignment.* https://github.com/tseemann/snippy
- Croucher NJ, et al. (2015). *Rapid phylogenetic analysis of large samples of recombinant bacterial whole genome sequences using Gubbins.* Nucleic Acids Research 43:e15. https://doi.org/10.1093/nar/gku1196
- Cingolani P, et al. (2012). *A program for annotating and predicting the effects of single nucleotide polymorphisms, SnpEff.* Fly 6:80–92. https://doi.org/10.4161/fly.19695
- Hooper DC, Jacoby GA (2015). *Mechanisms of drug resistance: quinolone resistance.* Annals of the New York Academy of Sciences 1354:12–31. https://doi.org/10.1111/nyas.12830
- snp-dists: https://github.com/tseemann/snp-dists

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins University)؛ نشاندن ریدها و فراخوانی واریانت: https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Linux* (The Linux Foundation). دوره‌ای ویژه‌ی واریانت باکتریایی در edX نیافتیم؛ نزدیک‌ترین: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux
- ‏YouTube: *Variant Calling - An Overview* (با پیوند به آموزش‌های bcftools و Snippy): https://www.youtube.com/watch?v=zk821_-Ubx4
- YouTube: *Variant Annotation and effect prediction with snpeff*: https://www.youtube.com/watch?v=Fcd3e9jT-7I

<sub>دستورها و خروجی‌های Snippy در 2026-10-21 از README رسمی خوانده شدند؛ نشانی‌های YouTube از جست‌وجوی همان روزند. همه‌ی نشانی‌ها در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
