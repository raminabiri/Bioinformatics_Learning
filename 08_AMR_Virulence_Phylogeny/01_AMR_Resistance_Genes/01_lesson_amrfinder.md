<div dir="rtl">

# درس ۱: پیدا کردن ژن‌ها و جهش‌های مقاومت با AMRFinderPlus

**بخش:** `08_AMR_Virulence_Phylogeny` · **ماژول:** `01_AMR_Resistance_Genes` · **پیش‌نیاز:** بخش [۰۷](../../07_Bacterial_Genomics/) (اسمبلی و آنوتیشن)، و `cut`، `sort`، `uniq` و `awk` از بخش [۰۱](../../01_Linux/) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** AMRFinderPlus 4.2.7، پایگاه 2026-08-07.1 · **آخرین بازبینی:** 2026-10-24

> ✅ **وضعیت: اجرا شده.** همه‌ی خروجی‌های این درس واقعی‌اند و در 2026-10-24 روی سه ژنوم شبیه‌سازی‌شده‌ی همین درس گرفته شده‌اند. هر اجرا نزدیک به ۸۰ ثانیه طول کشید و بیشینه‌ی حافظه‌اش **۱۸۳ مگابایت** بود؛ پس روی هر لپ‌تاپی اجرا می‌شود.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. سه راه مقاومت در ژنوم را از هم جدا کنید: ژن ذاتی، ژن اکتسابی، و جهش نقطه‌ای.
2. ‏AMRFinderPlus را روی یک اسمبلی اجرا کنید و نقش `--organism` و `--plus` را بگویید.
3. ستون‌های جدول خروجی، به‌ویژه **Method**، **Scope** و **Subclass**، را بخوانید.
4. یک ژن ناقص (`PARTIALX`) را بشناسید و بگویید چرا نمی‌توان با اطمینان آن را «مقاومت» خواند.
5. نتیجه را با یک جدول پاسخ معلوم (ground truth) بسنجید.

**پیش از آغاز:** یک محیط جدا بسازید و پایگاه AMRFinderPlus را یک بار دانلود کنید (نزدیک به ۲۰۰ مگابایت):

<div dir="ltr">

```bash
conda create -n amr -c conda-forge -c bioconda ncbi-amrfinderplus
conda activate amr
amrfinder -u
mkdir -p ~/amr && cd ~/amr
G=~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data
P=~/Bioinformatics_Learning-main/08_AMR_Virulence_Phylogeny/99_scripts_data
```

</div>

‏`amrfinder -u` پایگاه را در پوشه‌ی محیط conda می‌گذارد و BLAST index آن را می‌سازد. اگر بعدها پیام `The BLAST database for AMR_DNA-Escherichia.fa was not found` دیدید، یعنی این گام کامل نشده است؛ آن را دوباره اجرا کنید (ما روی سرور خودمان به همین پیام برخوردیم).

---

## ۱. داستان

از خون یک بیمار در بخش مراقبت ویژه *E. coli* جدا شده و آزمایشگاه میکروب‌شناسی آن را به سفتریاکسون و سیپروفلوکساسین مقاوم گزارش کرده است. پزشک می‌پرسد: **«این مقاومت از کجا آمده؟ اگر از یک پلاسمید است، شاید به باکتری‌های دیگر بخش هم برسد.»** شما اسمبلی ژنوم را دارید. در این درس با یک ابزار، ژن‌ها و جهش‌های مقاومت را پیدا می‌کنید و یاد می‌گیرید هر سطر خروجی چه می‌گوید و چه نمی‌گوید.

---

## ۲. مفهوم به زبان ساده

### ۲.۱ سه راه مقاومت در ژنوم

یک باکتری به سه راه ژنتیکی می‌تواند در برابر آنتی‌بیوتیک بایستد:

| راه | یعنی چه؟ | نمونه در این درس |
| :--- | :--- | :--- |
| **ژن ذاتی** (intrinsic) | ژنی که در کروموزوم همه‌ی سویه‌های آن گونه هست | ‏`blaEC` (بتالاکتاماز کلاس C کروموزومی *E. coli*)، پمپ‌های efflux مانند `acrF` |
| **ژن اکتسابی** (acquired) | ژنی که باکتری از راه پلاسمید، ترانسپوزون و مانند این‌ها **گرفته** است | ‏`blaCTX-M-15` (مقاومت به سفالوسپورین‌های نسل سوم)، `blaNDM-1` (کارباپنماز) |
| **جهش نقطه‌ای** (point mutation) | تغییر یک اسید آمینه در ژنی که همه دارند، ولی همین تغییر هدف دارو را عوض می‌کند | ‏`gyrA_S83L`: سرین ۸۳ ژیراز به لوسین بدل شده و فلوروکینولون کمتر به آن می‌چسبد |

**تشبیه:** آنتی‌بیوتیک کلیدی است که قفل (هدف دارو) را می‌بندد. ژن اکتسابی مانند نگهبانی است که کلید را پیش از رسیدن می‌شکند (آنزیم بتالاکتاماز). جهش نقطه‌ای مانند عوض شدن یک دندانه‌ی قفل است: کلید دیگر جا نمی‌افتد. پمپ efflux هم کلید را پیش از رسیدن به قفل بیرون می‌اندازد.

نکته‌ی مهم: **پیدا کردن ژن ذاتی در خروجی خبر بدی نیست.** هر *E. coli* ژن `blaEC` را دارد ولی بیشتر سویه‌ها به آمپی‌سیلین حساس‌اند، چون این ژن در حالت عادی کم بیان می‌شود.

> 📺 **فیلم:** *Basic Mechanisms of Antibiotic Resistance and Gene Spread* (Marilyn Roberts، University of Washington): https://www.youtube.com/watch?v=U7Dshq5Npdg
> 📄 **مرجع:** Reygaert WC (2018). *An overview of the antimicrobial resistance mechanisms of bacteria.* AIMS Microbiology 4:482–501. https://doi.org/10.3934/microbiol.2018.3.482

### ‏۲.۲ ‏AMRFinderPlus چگونه جست‌وجو می‌کند؟

‏AMRFinderPlus را NCBI می‌سازد و پایگاهش را کارشناسان NCBI دستی بازبینی (curate) می‌کنند. وقتی به آن یک اسمبلی نوکلئوتیدی می‌دهید (`-n`):

<div dir="ltr">

```
contigها ──► tblastn: پروتئین‌های پایگاه را روی هر شش چارچوب خواندن contigها می‌گذارد
          ──► blastn: جهش‌های نوکلئوتیدی (برای نمونه در 16S rRNA یا پروموتر)
          ──► اگر --organism داده شود: جایگاه‌های جهشی همان گونه را یکی‌یکی می‌سنجد
          ──► گزارش: هر سطر = یک ژن یا یک جهش
```

</div>

برای هر ژن، تصمیم بر پایه‌ی **همانندی (identity)** و **پوشش (coverage)** با نزدیک‌ترین پروتئین پایگاه گرفته می‌شود. ستون **Method** همین تصمیم را نشان می‌دهد (بخش ۴).

> 📺 **فیلم:** سخنرانی Michael Feldgarden (NCBI، نویسنده‌ی نخست مقاله‌ی AMRFinderPlus) درباره‌ی ابزارهای یافتن ژن‌های مقاومت: https://www.youtube.com/watch?v=tXQfHjdx0F8
> 📄 **مرجع:** Feldgarden M, et al. (2021). *AMRFinderPlus and the Reference Gene Catalog facilitate examination of the genomic links among antimicrobial resistance, stress response, and virulence.* Scientific Reports 11:12728. https://doi.org/10.1038/s41598-021-91456-0 · راهنمای رسمی: https://github.com/ncbi/amr/wiki

### ۲.۳ داده‌ی این درس: سه ایزوله با پاسخ معلوم

برای اینکه بتوانید درستی نتیجه را بسنجید، سه ژنوم **شبیه‌سازی‌شده** می‌سازیم. پایه‌ی همه، کروموزوم *E. coli* K-12 بخش ۰۱ است:

| ایزوله | چه چیزی به K-12 افزوده شده؟ |
| :--- | :--- |
| ‏`isoA` | جهش `gyrA` S83L، و یک contig «پلاسمید» (`isoA_pA`) با ژن کامل `blaCTX-M-15` |
| ‏`isoB` | جهش `parC` S80I، و contig `isoB_pB` با ژن کامل `blaNDM-1` و **نیمه‌ی نخست** ژن `tet(A)` (۶۰۰ از ۱۲۰۰ باز) |
| ‏`isoC` | هیچ؛ همان K-12 (کنترل منفی) |

توالی سه ژن اکتسابی از پایگاه AMRFinderPlus (نسخه‌ی 2026-08-07.1) برداشته شده و در `99_scripts_data/data/acquired_genes.fna` است. «پلاسمید»ها در واقع پلاسمید نیستند: ژن، میان دو تکه DNA تصادفی (با seed ثابت ۴۲) گذاشته شده است.

---

## ۳. گام ۱: ساختن سه ژنوم

**چرا؟** تا پیش از هر تحلیلی بدانیم پاسخ درست چیست.

<div dir="ltr">

```bash
python3 $P/01_AMR_Resistance_Genes/scripts/make_mock_isolates.py \
    $G/ecoli_k12.fna $G/ecoli_k12.gff $P/data/acquired_genes.fna genomes
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
gyrA S83L: TCG -> TTG
parC S80I: AGC -> ATC
Done: genomes
```

</div>

**توضیح خروجی:** اسکریپت پیش از تغییر هر کدون بررسی می‌کند که اسید آمینه‌ی پیشین همان باشد که انتظار داریم (سرین، S). کدون ۸۳ ژن `gyrA` در K-12 برابر `TCG` (سرین) بود و به `TTG` (لوسین) بدل شد. ‏`gyrA` روی رشته‌ی منفی است، پس اسکریپت پیش از خواندن کدون، توالی را معکوس-مکمل می‌کند؛ اگر این کار را نکند، کدون اشتباهی را تغییر می‌دهد.

<div dir="ltr">

```bash
ls genomes
cat genomes/ground_truth_amr.tsv
```

</div>

<div dir="ltr">

```
ground_truth_amr.tsv  isoA.fna  isoB.fna  isoC.fna
isolate	contig	feature	kind
isoA	isoA_chromosome	gyrA_S83L	point mutation
isoA	isoA_pA	blaCTX-M-15	acquired gene (complete)
isoB	isoB_chromosome	parC_S80I	point mutation
isoB	isoB_pB	blaNDM-1	acquired gene (complete)
isoB	isoB_pB	tet(A)	acquired gene (first 600 of 1200 bp)
isoC	-	-	none (K-12 only)
```

</div>

این جدول «برگه‌ی پاسخ» ماست. پس از هر اجرا، خروجی را با آن می‌سنجیم.

---

## ۴. گام ۲: اجرای AMRFinderPlus روی isoA

**چرا؟** ببینیم ابزار هر سه راه مقاومت را پیدا می‌کند یا نه.

<div dir="ltr">

```bash
amrfinder -n genomes/isoA.fna --organism Escherichia --plus \
    --name isoA --threads 2 -o isoA.amr.tsv --mutation_all isoA.mut_all.tsv
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`-n genomes/isoA.fna` | ورودی **نوکلئوتیدی** (اسمبلی). با `-p` می‌توان پروتئین‌های آنوتیشن (`.faa` بخش ۰۷) را داد |
| ‏`--organism Escherichia` | جست‌وجوی **جهش‌های نقطه‌ای** ویژه‌ی این جنس را روشن می‌کند. فهرست نام‌ها: `amrfinder -l` |
| ‏`--plus` | ژن‌های گروه «plus» را هم گزارش می‌کند: پمپ‌ها، مقاومت به biocide، اسید و فلز، و ژن‌های بیماری‌زایی |
| ‏`--name isoA` | یک ستون نخست `Name` با این مقدار می‌افزاید؛ برای یکی کردن جدول چند ایزوله لازم است |
| ‏`--threads 2` | دو هسته |
| ‏`-o isoA.amr.tsv` | جدول اصلی |
| ‏`--mutation_all isoA.mut_all.tsv` | گزارش **همه‌ی** جایگاه‌های جهشی سنجیده‌شده، چه جهش‌یافته چه نه |

**خروجی واقعی روی صفحه** (سطر `Database directory` روی کامپیوتر شما مسیر دیگری دارد):

<div dir="ltr">

```
Software version: 4.2.7
Database version: 2026-08-07.1
AMRFinder translated nucleotide and mutation search
Running tblastn
Running blastn
Running stxtyper
Making report
amrfinder took 81 seconds to complete
```

</div>

**توضیح خروجی:** دو سطر نخست را **همیشه در گزارش خود بنویسید.** پایگاه AMRFinderPlus چند بار در سال به‌روز می‌شود و یک ژنوم با دو نسخه‌ی پایگاه می‌تواند دو نتیجه‌ی کمی متفاوت بدهد. ‏`stxtyper` ابزار جانبی برای تایپ ژن‌های شیگاتوکسین است که برای *Escherichia* خودکار اجرا می‌شود (این ژنوم stx ندارد).

> 📺 **فیلم:** *NCBI Minute: Accessing NCBI AMR Pathogen Data in the Cloud* (NCBI؛ داده‌های Pathogen Detection که با همین ابزار ساخته می‌شوند): https://www.youtube.com/watch?v=j4dzFOo2FmI
> 📄 **مرجع:** راهنمای اجرای AMRFinderPlus: https://github.com/ncbi/amr/wiki/Running-AMRFinderPlus

---

## ۵. گام ۳: خواندن جدول

جدول ۲۳ ستون دارد. سطر نخست، نام ستون‌هاست. برای دیدن ستون‌های مهم آن‌ها را با `cut` جدا می‌کنیم و با یک دستور تازه، `column`، مرتب نشان می‌دهیم:

> **دستور تازه: `column -t -s$'\t'`** ستون‌های یک فایل را زیر هم تراز می‌کند. ‏`-t` یعنی «جدول بساز» و `-s$'\t'` یعنی «جداکننده‌ی ستون‌ها tab است». ‏`$'\t'` در Bash یعنی یک نویسه‌ی tab. این دستور فایل را تغییر نمی‌دهد؛ تنها نمایش را خواناتر می‌کند.

<div dir="ltr">

```bash
cut -f3,4,7,9,11,13,14,17,18 isoA.amr.tsv | column -t -s$'\t'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
Contig id        Start    Element symbol  Scope  Subtype  Subclass       Method   % Coverage of reference  % Identity to reference
isoA_chromosome  568315   emrE            plus   BIOCIDE  EFFLUX         EXACTX   100.00                   100.00
isoA_chromosome  1216369  ariR            plus   ACID     NA             EXACTX   100.00                   100.00
isoA_chromosome  2336796  gyrA_S83L       core   POINT    QUINOLONE      POINTX   99.66                    99.09
isoA_chromosome  3415033  acrF            plus   AMR      EFFLUX         EXACTX   100.00                   100.00
isoA_chromosome  4377814  blaEC           plus   AMR      BETA-LACTAM    EXACTX   100.00                   100.00
isoA_chromosome  4567290  mdtM            plus   AMR      EFFLUX         EXACTX   100.00                   100.00
isoA_pA          2001     blaCTX-M-15     core   AMR      CEPHALOSPORIN  ALLELEX  100.00                   100.00
```

</div>

**توضیح خروجی، ستون به ستون:**

- ‏**Scope:** ‏`core` یعنی ژن‌ها و جهش‌هایی که NCBI آن‌ها را به‌طور قطعی «مقاومت» می‌داند. ‏`plus` یعنی ژن‌هایی که تنها با `--plus` دیده می‌شوند و بودنشان در بسیاری از موارد بر فنوتیپ اثری ندارد. **دو سطر core دقیقاً همان دو چیزی‌اند که ما به isoA افزودیم.** پنج سطر plus در K-12 هم هستند (گام ۵ را ببینید).
- ‏**Subtype:** ‏`AMR` ژن مقاومت است، `POINT` جهش نقطه‌ای شناخته‌شده، و `BIOCIDE` و `ACID` مقاومت به ضدعفونی‌کننده و اسید (Type این دو `STRESS` است).
- ‏**Subclass:** ریزتر از Class. برای `blaCTX-M-15`، Class برابر `BETA-LACTAM` ولی Subclass برابر `CEPHALOSPORIN` است؛ یعنی این آنزیم سفالوسپورین‌ها (از جمله سفتریاکسون) را می‌شکند. برای `blaEC` تنها `BETA-LACTAM` آمده است.
- ‏**Method:** چگونه پیدا شده (جدول زیر).
- ‏**Identity ‏99.09 برای `gyrA_S83L`:** پروتئین مرجع پایگاه (`WP_001281243.1`) با GyrA سویه‌ی K-12 در چند اسید آمینه فرق دارد. این فرق‌ها در جایگاه‌های مقاومت نیستند؛ تصمیم درباره‌ی جهش، **تنها** با سنجیدن جایگاه ۸۳ گرفته می‌شود، نه با درصد همانندی.

**معنای ستون Method** (از صفحه‌ی رسمی *Interpreting results*). پسوند `X` یعنی «از ورودی نوکلئوتیدی، پس از ترجمه»؛ `P` یعنی «از ورودی پروتئینی»؛ `N` یعنی «با blastn روی DNA».

| Method | معنا |
| :--- | :--- |
| ‏`EXACTX` / `ALLELEX` | توالی اسید آمینه **کاملاً همسان** با یک پروتئین پایگاه است. ‏`ALLELE` برای خانواده‌هایی که شماره‌گذاری آلل دارند (مانند CTX-M-**15**) |
| ‏`BLASTX` | همانندی کمتر از ۱۰۰٪ ولی پوشش بیش از ۹۰٪ |
| ‏`PARTIALX` | پوشش کمتر از ۹۰٪ و ژن **درون** contig است |
| ‏`PARTIAL_CONTIG_ENDX` | پوشش کمتر از ۹۰٪ ولی ژن به **لبه‌ی contig** رسیده؛ شاید ژن کامل است و اسمبلر آن را دو تکه کرده |
| ‏`INTERNAL_STOP` | یک کدون پایان زودرس درون ژن (تنها با `-n`) |
| ‏`HMM` | معیار BLAST پاس نشده ولی مدل HMM خانواده پاس شده؛ در بسیاری از موارد یک خویشاوند دور |
| ‏`POINTX` / `POINTN` | یک جهش شناخته‌شده پیدا شده |

<details>
<summary>✋ امتحان کن: چرا <code>blaCTX-M-15</code> روی <code>isoA_pA</code> در جایگاه 2001 آغاز می‌شود؟</summary>

اسکریپت پیش از ژن ۲۰۰۰ باز DNA تصادفی گذاشته است (`spacer(2000)` در `make_mock_isolates.py`). پس ژن از باز ۲۰۰۱ آغاز می‌شود. ستون Stop برابر 2873 است: ‏2001 + 876 − 1 − 3 = 2873، یعنی AMRFinderPlus کدون پایان (۳ باز) را جزو پروتئین نمی‌شمارد. اگر Stop را ببینید: `cut -f4,5,7 isoA.amr.tsv | grep CTX`.

</details>

> 📄 **مرجع:** صفحه‌ی رسمی معنای ستون‌ها و Methodها: https://github.com/ncbi/amr/wiki/Interpreting-results

---

## ۶. گام ۴: ژن ناقص در isoB

<div dir="ltr">

```bash
amrfinder -n genomes/isoB.fna --organism Escherichia --plus \
    --name isoB --threads 2 -o isoB.amr.tsv --mutation_all isoB.mut_all.tsv
awk -F'\t' '$9=="core"' isoB.amr.tsv | cut -f3,4,5,7,13,14,15,16,17,18 | column -t -s$'\t'
```

</div>

‏`awk -F'\t' '$9=="core"'` (بخش 01/07) تنها سطرهایی را نگه می‌دارد که ستون ۹ (Scope) آن‌ها `core` است.

**خروجی واقعی:**

<div dir="ltr">

```
isoB_chromosome  3163718  3165973  parC_S80I  QUINOLONE     POINTX    752  752  100.00  99.87
isoB_pB          2001     2810     blaNDM-1   CARBAPENEM    ALLELEX   270  270  100.00  100.00
isoB_pB          4314     4916     tet(A)     TETRACYCLINE  PARTIALX  201  399  50.38   99.50
```

</div>

**توضیح خروجی:** ستون‌ها به ترتیب: contig، آغاز، پایان، نماد، Subclass، Method، **طول هدف** (اسید آمینه در ژنوم ما)، **طول مرجع**، پوشش، همانندی.

- ‏`blaNDM-1` با Subclass `CARBAPENEM`: کارباپنماز. این خطرناک‌ترین یافته‌ی این ایزوله است.
- ‏`tet(A)` با `PARTIALX`: تنها ۲۰۱ از ۳۹۹ اسید آمینه پیدا شده است. ‏201 / 399 = 0.5038، همان ۵۰٫۳۸٪. ما ۶۰۰ باز (۲۰۰ کدون) گذاشته بودیم؛ اسید آمینه‌ی ۲۰۱ از DNA تصادفی پس از ژن آمده است، و همین یک اسید آمینه‌ی ناهمسان، همانندی را به ۹۹٫۵۰٪ رسانده است (1/201 ≈ 0.5٪).
- ‏Method برابر `PARTIALX` است، نه `PARTIAL_CONTIG_ENDX`؛ چون ژن نیمه‌کاره **میان** contig است (آغاز 4314، و contig تا ۶۹۱۳ ادامه دارد). یعنی تکه‌تکه شدن به دست اسمبلر نیست: این ژن واقعاً ناقص است.

**پرسش زیستی:** آیا isoB به تتراسایکلین مقاوم است؟ پاسخ درست: **از روی ژنوم نمی‌دانیم.** نیمه‌ی یک پمپ efflux در بسیاری از موارد کار نمی‌کند. چنین ژنی را در گزارش با برچسب «ناقص» بیاورید و پیش‌بینی فنوتیپ را به آزمون حساسیت (AST) بسپارید.

<details>
<summary>✋ امتحان کن: اگر همین ژن ناقص در لبه‌ی یک contig بود، Method چه می‌شد و تفسیرتان چه تغییری می‌کرد؟</summary>

‏`PARTIAL_CONTIG_ENDX`. در این حالت شاید ژن کامل باشد و اسمبلی short-read آن را میان دو contig شکسته باشد (ژن‌های مقاومت در بسیاری از موارد کنار عنصرهای تکراری مانند IS هستند و اسمبلر در همین جاها می‌شکند). تفسیر: «شاید کامل»؛ برای روشن شدن، ریدها را به ژن map کنید یا اسمبلی long-read بگیرید (بخش 10/02).

</details>

---

## ۷. گام ۵: کنترل منفی و نقش گزینه‌ها

**چرا کنترل منفی؟** تا بدانیم کدام سطرها مال «پس‌زمینه»‌ی K-12‌اند و کدام مال تغییرهای ما.

<div dir="ltr">

```bash
amrfinder -n genomes/isoC.fna --organism Escherichia --plus \
    --name isoC --threads 2 -o isoC.amr.tsv --mutation_all isoC.mut_all.tsv
tail -q -n +2 isoA.amr.tsv isoB.amr.tsv isoC.amr.tsv | cut -f1 | sort | uniq -c
```

</div>

‏`tail -q -n +2` سطر نخست (نام ستون‌ها) هر فایل را کنار می‌گذارد؛ ‏`-q` نام فایل‌ها را چاپ نمی‌کند.

**خروجی واقعی:**

<div dir="ltr">

```
      7 isoA
      8 isoB
      5 isoC
```

</div>

‏isoC پنج سطر دارد: همان پنج ژن plus (`emrE`، `ariR`، `acrF`، `blaEC`، `mdtM`). ‏isoA ‏۵ + ۲ و isoB ‏۵ + ۳ سطر دارند. **هر چه بیش از کنترل منفی آمده، همان است که ما افزوده بودیم؛ نه کم، نه زیاد.**

حالا ببینیم اگر گزینه‌ها را برداریم چه می‌شود (روی isoA):

| دستور | سطرهای خروجی (واقعی) |
| :--- | :--- |
| ‏`amrfinder -n genomes/isoA.fna` | تنها `blaCTX-M-15` |
| ‏`amrfinder -n genomes/isoA.fna --organism Escherichia` | ‏`gyrA_S83L` و `blaCTX-M-15` |
| ‏`amrfinder -n genomes/isoA.fna --organism Escherichia --plus` | همان ۷ سطر گام ۳ |

**بی `--organism`، جهش `gyrA_S83L` دیده نمی‌شود** و گزارش می‌گوید «مقاومت به کینولون: هیچ»؛ در حالی که آزمایشگاه این ایزوله را مقاوم به سیپروفلوکساسین گزارش کرده بود. این مهم‌ترین گزینه‌ی این ابزار است.

### گزارش همه‌ی جایگاه‌های جهشی

جدول اصلی تنها جهش‌های **یافته‌شده** را می‌آورد. ‏`--mutation_all` نشان می‌دهد کدام جایگاه‌ها **سنجیده شدند و سالم بودند**:

<div dir="ltr">

```bash
grep -E "gyrA_S83|parC_S80" isoA.mut_all.tsv | cut -f7,8,14
```

</div>

<div dir="ltr">

```
gyrA_S83L	Escherichia quinolone resistant GyrA	POINTX
parC_S80S	DNA topoisomerase IV subunit A ParC [WILDTYPE]	POINTX
```

</div>

‏`parC_S80S` با برچسب `[WILDTYPE]` یعنی «جایگاه ۸۰ ParC سنجیده شد و همان سرین است». این برای گزارش ارزشمند است: «جهش parC نیست» را با «parC بررسی نشد» یکی نگیرید. صفحه‌ی رسمی هشدار می‌دهد: تنها جهش‌های بازبینی‌شده‌ی هر گونه سنجیده می‌شوند، پس نبودن یک جهش در گزارش، نبودن هر جهش مقاومتی نیست.

برچسب سوم در این فایل `[UNKNOWN]` است. به گفته‌ی راهنمای رسمی، این‌ها جهش‌های **تازه**‌اند: تفاوتی با توالی مرجع که در فهرست جهش‌های شناخته‌شده نیست. در K-12 (isoC) ‏۳۷۸ سطر `[WILDTYPE]` و ۱۶۳ سطر `[UNKNOWN]` است و بیشتر سطرهای UNKNOWN در 16S و 23S rRNA‌اند (هفت نسخه‌ی rRNA در کروموزوم با هم کمی فرق دارند). ‏UNKNOWN یعنی «متفاوت»، **نه** «مقاوم».

> 📺 **فیلم:** *Antibiotic Resistance (Antibiotics - Lecture 9)* (جهش هدف دارو، آزمون حساسیت و MIC): https://www.youtube.com/watch?v=2NQLUbaZSgc
> 📄 **مرجع:** Hooper DC, Jacoby GA (2015). *Mechanisms of drug resistance: quinolone resistance.* Annals of the New York Academy of Sciences 1354:12–31. https://doi.org/10.1111/nyas.12830

<details>
<summary>✋ امتحان کن: در isoB.mut_all.tsv جایگاه ۸۳ GyrA چه برچسبی دارد؟</summary>

<div dir="ltr">

```bash
grep -E "gyrA_S83" isoB.mut_all.tsv | cut -f7,8
```

</div>

دو سطر `gyrA_S83S … [WILDTYPE]` (دو مدل جهش در پایگاه به این جایگاه اشاره دارند). یعنی isoB در gyrA جهش ندارد؛ مقاومت کینولونی آن (اگر باشد) از `parC_S80I` است. در بالین، یک جهش parC به‌تنهایی در بسیاری از موارد مقاومت کمی می‌دهد و ترکیب gyrA + parC مقاومت بالا.

</details>

---

## ۸. سه اشتباه رایج

1. **فراموش کردن `--organism`.** جهش‌های نقطه‌ای (کینولون، کولیستین، و مانند این‌ها) بی‌صدا گم می‌شوند. همیشه نام گونه را از فهرست `amrfinder -l` بدهید.
2. **شمردن ژن‌های plus به‌عنوان «مقاومت».** ‏`blaEC` و `acrF` در همه‌ی *E. coli*‌ها هستند. برای گزارش بالینی، سطرهای `core` را جدا کنید و plus را تنها برای پژوهش نگه دارید.
3. **«مقاوم» خواندن هر ژن ناقص.** ‏`PARTIALX` یعنی ژن بریده شده است و شاید کار نکند؛ `PARTIAL_CONTIG_ENDX` یعنی شاید کامل است. هر دو را با برچسب و جدا گزارش کنید.

---

## 📘 برای کنجکاوها

- با ورودی پروتئینی (`-p proteins.faa`) و GFF (`-g`)، AMRFinderPlus از پروتئین‌های پیش‌بینی‌شده‌ی آنوتیشن (Bakta/Prokka بخش ۰۷) کار می‌کند و سریع‌تر است. ولی `INTERNAL_STOP` و جهش‌های نوکلئوتیدی تنها با `-n` دیده می‌شوند؛ می‌توان هر سه را با هم داد.
- برای *Salmonella* و *E. coli*، NCBI همین ابزار را روی همه‌ی ژنوم‌های عمومی اجرا می‌کند و نتیجه را در **NCBI Pathogen Detection** (Isolates Browser) می‌گذارد؛ می‌توانید ایزوله‌ی خود را با هزاران ایزوله‌ی دیگر بسنجید.

---

## جمع‌بندی

- مقاومت در ژنوم سه راه دارد: ژن ذاتی، ژن اکتسابی، و جهش نقطه‌ای. تنها دو راه آخر، تفاوت ایزوله‌ها را توضیح می‌دهند.
- ‏`amrfinder -n … --organism … --plus` هر سه را گزارش می‌کند؛ بی `--organism` جهش‌ها دیده نمی‌شوند.
- ستون‌های کلیدی: Scope (core/plus)، Subclass (کدام دارو)، Method (چگونه و چقدر کامل).
- روی داده‌ی شبیه‌سازی‌شده، AMRFinderPlus دقیقاً همه‌ی ۵ تغییر را یافت و چیزی هم افزون بر کنترل منفی گزارش نکرد.
- نسخه‌ی ابزار و پایگاه را همیشه در گزارش بنویسید.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
amrfinder -u                                    # download / update the database
amrfinder -l                                    # list --organism names
amrfinder -n ASM.fna --organism Escherichia --plus --name ID --threads 2 \
    -o ID.amr.tsv --mutation_all ID.mut_all.tsv
awk -F'\t' '$9=="core"' ID.amr.tsv              # clinical (core) lines only
cut -f3,7,13,14,17,18 ID.amr.tsv | column -t -s$'\t'
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏AMR (antimicrobial resistance) | مقاومت ضدمیکروبی |
| ژن ذاتی (intrinsic) | ژن مقاومتی که در کروموزوم همه‌ی سویه‌های یک گونه هست |
| ژن اکتسابی (acquired) | ژنی که با انتقال افقی (پلاسمید، ترانسپوزون) به دست آمده |
| جهش نقطه‌ای (point mutation) | تغییر یک باز یا یک اسید آمینه |
| ‏efflux pump | پمپ بیرون‌ران؛ پروتئینی که دارو را از سلول بیرون می‌راند |
| ‏ESBL | بتالاکتاماز با طیف گسترده؛ مانند CTX-M، که سفالوسپورین‌های نسل سوم را می‌شکند |
| کارباپنماز (carbapenemase) | آنزیمی که کارباپنم‌ها را می‌شکند؛ مانند NDM، KPC، OXA-48 |
| ‏identity / coverage | درصد همسانی / درصد طول مرجع که پوشش داده شده |
| ‏core / plus | دو گروه پایگاه AMRFinderPlus: مقاومت قطعی / ژن‌های تنش، پمپ و بیماری‌زایی |
| ‏WILDTYPE | جایگاه سنجیده شد و تغییری ندارد |
| ‏ground truth | پاسخ معلومی که نتیجه با آن سنجیده می‌شود |
| ‏AST / MIC | آزمون حساسیت آنتی‌بیوتیکی / کمترین غلظت بازدارنده |

---

## منابع

**مستند و مقاله**
- Feldgarden M, et al. (2021). *AMRFinderPlus and the Reference Gene Catalog facilitate examination of the genomic links among antimicrobial resistance, stress response, and virulence.* Scientific Reports 11:12728. https://doi.org/10.1038/s41598-021-91456-0
- AMRFinderPlus wiki: https://github.com/ncbi/amr/wiki · Interpreting results: https://github.com/ncbi/amr/wiki/Interpreting-results · Running AMRFinderPlus: https://github.com/ncbi/amr/wiki/Running-AMRFinderPlus
- Reygaert WC (2018). *An overview of the antimicrobial resistance mechanisms of bacteria.* AIMS Microbiology 4:482–501. https://doi.org/10.3934/microbiol.2018.3.482
- Hooper DC, Jacoby GA (2015). *Mechanisms of drug resistance: quinolone resistance.* Ann N Y Acad Sci 1354:12–31. https://doi.org/10.1111/nyas.12830
- NCBI Pathogen Detection: https://www.ncbi.nlm.nih.gov/pathogens/

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Antimicrobial resistance – theory and methods* (Technical University of Denmark، DTU): https://www.coursera.org/learn/antimicrobial-resistance
- ‏Coursera: *Whole genome sequencing of bacterial genomes – tools and applications* (DTU؛ بخش شناسایی ژن‌های مقاومت): https://www.coursera.org/learn/wgs-bacteria
- ‏edX: دوره‌ای ویژه‌ی AMR ژنومی در edX نیافتیم؛ نزدیک‌ترین: *Antimicrobial Stewardship: Improving Clinical Outcomes by Optimization of Antibiotic Practices* (Stanford): https://www.edx.org/learn/medicine/stanford-university-antimicrobial-stewardship-improving-clinical-outcomes-by-optimization-of-antibiotic-practices
- ‏YouTube: *Basic Mechanisms of Antibiotic Resistance and Gene Spread* (Marilyn Roberts): https://www.youtube.com/watch?v=U7Dshq5Npdg
- ‏YouTube: سخنرانی Michael Feldgarden (NCBI): https://www.youtube.com/watch?v=tXQfHjdx0F8
- ‏YouTube: *NCBI Minute: Accessing NCBI AMR Pathogen Data in the Cloud*: https://www.youtube.com/watch?v=j4dzFOo2FmI
- ‏YouTube: *Antibiotic Resistance (Antibiotics - Lecture 9)*: https://www.youtube.com/watch?v=2NQLUbaZSgc

<sub>معنای Methodها و Scope در 2026-10-24 از صفحه‌ی رسمی Interpreting results خوانده شد. نشانی‌های Coursera، edX و YouTube از جست‌وجوی وب در 2026-10-24‌اند (YouTube از سرور در دسترس نبود)؛ همه‌ی نشانی‌ها در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
