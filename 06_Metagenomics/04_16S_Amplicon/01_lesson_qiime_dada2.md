<div dir="rtl">

# درس ۱: آمپلیکون 16S با QIIME 2، از ریدها تا جدول ASV

**بخش:** `06_Metagenomics` · **ماژول:** `04_16S_Amplicon` · **پیش‌نیاز:** ماژول [کنترل کیفیت](../01_Read_QC_Trimming/) (FASTQ و کیفیت Phred) · **زمان:** حدود ۷۵ دقیقه · **ابزار:** QIIME 2 amplicon 2026.7 (q2-demux، q2-dada2)، vsearch · **خروجی‌ها از اجرای:** 2026-10-14

> ⚠️ **داده‌ی این درس تنها برای تمرین است:** زیرنمونه‌ی ۱٪ یک ران واقعی (میانه‌ی ۲۴۳ رید در هر نمونه پس از DADA2). در پژوهش واقعی ده‌ها هزار رید در هر نمونه، و **کنترل منفی و mock community در همان ران** لازم است.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. بگویید 16S چه پرسش‌هایی را بهتر و چه پرسش‌هایی را بدتر از shotgun پاسخ می‌دهد.
2. فایل‌های `.qza` و `.qzv` و «نوع معنایی» QIIME 2 را بشناسید.
3. داده‌ی چندگانه (*multiplexed*) EMP را وارد QIIME 2 کنید و نمونه‌ها را از هم جدا کنید.
4. پارامترهای DADA2 را از روی **نمودار کیفیت** و **طول آمپلیکون** برگزینید.
5. جدول افت رید DADA2 را بخوانید و علت افت را پیدا کنید.

**پیش از آغاز:** QIIME 2 **محیط conda خودش** را دارد و با محیط `metagenomics` سازگار نیست (بخش ۰۲: چرا ابزارهای ناسازگار در محیط‌های جدا). محیط **amplicon** نسخه‌ی 2026.7 را یک بار، با دستور صفحه‌ی رسمی نصب بسازید: https://library.qiime2.org/quickstart/amplicon (نام محیط: `qiime2-amplicon-2026.7`؛ چند گیگابایت). سپس:

<div dir="ltr">

```bash
conda activate qiime2-amplicon-2026.7
mkdir -p ~/amplicon && cd ~/amplicon
C=~/Bioinformatics_Learning-main/06_Metagenomics/99_scripts_data/04_16S_Amplicon
bash $C/data/download.sh                 # about 53 MB, checked with md5
M=data/sample_metadata.tsv
qiime --version | head -n 1
```

</div>

<div dir="ltr">

```text
q2cli version 2026.7.0
```

</div>

‏`download.sh` با `curl` (بخش ۰۱) سه فایل FASTQ، جدول نمونه‌ها و مرجع SILVA را در `data/` می‌گذارد و md5 آن‌ها را می‌سنجد.

---

## ۱. داستان

بیابان آتاکاما (شیلی) یکی از خشک‌ترین خاک‌های زمین است. Neilson و همکاران (۲۰۱۷) در دو مسیر به نام‌های **Baquedano** و **Yungay**، از ارتفاع ۸۹۵ تا ۴٬۶۹۷ متر، نمونه‌ی خاک گرفتند و پرسیدند: **جامعه‌ی میکروبی خاک با رطوبت، ارتفاع و پوشش گیاهی چگونه عوض می‌شود؟**

برای چنین پرسشی، با ده‌ها نمونه، توالی‌یابی آمپلیکون 16S گزینه‌ی منطقی است:

| | آمپلیکون 16S | ‏Shotgun (ماژول‌های ۰۱ تا ۰۳) |
| :--- | :--- | :--- |
| چه خوانده می‌شود | یک ناحیه‌ی ۲۵۰ تا ۴۵۰ بازی از **یک ژن** | تکه‌های تصادفی از **همه‌ی** DNA |
| هزینه‌ی هر نمونه | کم؛ صدها نمونه در یک ران MiSeq | چند برابر |
| تفکیک تاکسونومیک | بیشتر **جنس**؛ گونه به‌ندرت | گونه و گاهی سویه |
| ژن‌ها و کارکرد | ❌ تنها **پیش‌بینی** (PICRUSt2 و همانند آن) | ✅ سنجش مستقیم |
| ‏DNA میزبان | مشکل نیست (پرایمر ویژه‌ی پروکاریوت‌هاست) | مشکل بزرگ (ماژول ۰۲) |
| ویروس و یوکاریوت | ❌ | ✅ |

**قاعده:** وقتی پرسش «چه کسی، چقدر، و آیا میان گروه‌ها فرق دارد؟» است و نمونه‌ها بسیارند، 16S بس و ارزان است. وقتی پرسش «چه ژن‌هایی، کدام سویه، کدام مسیر؟» است، shotgun لازم است.

---

## ۲. مفهوم به زبان ساده

### ۲.۱ ژن 16S و ناحیه‌ی V4

ژن 16S rRNA کمابیش ۱۵۰۰ باز است: نواحی **حفاظت‌شده** که پرایمر به آن‌ها می‌چسبد، و **۹ ناحیه‌ی متغیر** (V1 تا V9) که تفاوت تاکسون‌ها در آن‌هاست.

<div dir="ltr">

```text
16S rRNA gene (~1500 bp)
|--V1--V2--V3--[ V4 ]--V5--V6--V7--V8--V9--|
              515F ->  <- 806R
              |<-- ~253 bp -->|   (primers removed)
```

</div>

پروژه‌ی Earth Microbiome (EMP) ناحیه‌ی **V4** را با پرایمرهای **515F/806R** استاندارد کرد. قطعه کمابیش **۲۵۳ باز** است، پس دو رید ۱۵۰ بازی MiSeq روی هم می‌افتند و همه‌ی قطعه را می‌پوشانند. سه پیامد:
- **هیچ ناحیه‌ای همه‌ی تاکسون‌ها را خوب جدا نمی‌کند.** V4 برخی جنس‌های نزدیک (مانند *Escherichia* و *Shigella*) را جدا نمی‌کند.
- **پرایمر سوگیری دارد.** دو پژوهش با پرایمرهای گوناگون مستقیم سنجیدنی نیستند.
- **شمار نسخه‌های 16S** در ژنوم باکتری‌ها از ۱ تا بیش از ۱۰ فرق دارد؛ «درصد رید» برابر «درصد سلول» نیست.

### ‏۲.۲ ‏ASV در برابر OTU

روش قدیمی ریدها را با مرز ۹۷٪ همانندی در **OTU** خوشه می‌کرد. **DADA2** برای هر ران یک **مدل خطا** می‌سازد و برای هر توالی یکتا می‌پرسد: «این توالی واقعی است یا نسخه‌ی خطادار یک توالی پرشمارتر؟» خروجی **ASV** است: توالی دقیق، با تفکیک یک باز.

برتری ASV: **میان پژوهش‌ها سنجیدنی است** (یک توالی = یک شناسه). QIIME 2 شناسه‌ی هر ASV را **هش MD5 توالی‌اش** می‌گذارد؛ پس یک ASV در هر پروژه‌ای همان شناسه را دارد.

### ‏۲.۳ ‏QIIME 2: فایل‌هایی که تاریخچه دارند

| چیز | چیست |
| :--- | :--- |
| ‏`.qza` (*artifact*) | داده + **نوع** + **تاریخچه‌ی کامل** (کدام دستور، کدام پارامتر، کدام نسخه، از کدام ورودی). خودش یک zip است. |
| ‏`.qzv` (*visualization*) | گزارش تعاملی؛ با کشیدن روی https://view.qiime2.org باز می‌شود. |
| نوع معنایی (*semantic type*) | برچسبی مانند `FeatureTable[Frequency]`؛ QIIME 2 نمی‌گذارد فایل نادرست را به دستوری بدهید. |
| ‏Provenance | زبانه‌ای در view.qiime2.org که کل زنجیره‌ی تحلیل یک فایل را نشان می‌دهد. |

همه‌ی دستورها یک شکل دارند: `qiime <افزونه> <کار> --i-… --p-… --m-… --o-…`:

| پیشوند | معنی | نمونه |
| :--- | :--- | :--- |
| ‏`--i-` | ورودی (*input*): یک `.qza` | `--i-seqs` |
| ‏`--p-` | پارامتر | `--p-trunc-len-f 150` |
| ‏`--m-` | جدول نمونه‌ها (*metadata*) | `--m-barcodes-file $M` |
| ‏`--o-` | خروجی (*output*) | `--o-table table.qza` |

### ۲.۴ جدول نمونه‌ها (metadata)

<div dir="ltr">

```bash
head -n 3 $M | cut -f 1-3,7,20
```

</div>

<div dir="ltr">

```text
sample-id	barcode-sequence	elevation	transect-name	vegetation
#q2:types	categorical	numeric	categorical	categorical
BAQ1370.1.2	GCCCAAGTTCAC	1370	Baquedano	no
```

</div>

سطر دوم ویژه‌ی QIIME 2 است: `#q2:types` می‌گوید هر ستون **عددی** است یا **دسته‌ای**. بی آن، شاید `elevation` دسته‌ای خوانده شود و آزمون همبستگی روی آن اجرا نشود.

---

## ۳. گام ۱: وارد کردن ریدها

پروتکل EMP سه فایل دارد: `forward` و `reverse` (دو رید هر جفت) و `barcodes` (بارکد ۱۲ بازی هر جفت، در یک رید جدا). QIIME 2 نام‌ها را **دقیقاً** `forward.fastq.gz`، `reverse.fastq.gz` و `barcodes.fastq.gz` در یک پوشه می‌خواهد:

<div dir="ltr">

```bash
mkdir -p emp
cp data/raw/forward.fastq.gz data/raw/reverse.fastq.gz data/raw/barcodes.fastq.gz emp/
qiime tools import --type EMPPairedEndSequences --input-path emp --output-path emp-paired-end-sequences.qza
```

</div>

<div dir="ltr">

```text
Imported emp as EMPPairedEndDirFmt to emp-paired-end-sequences.qza
```

</div>

| بخش | چیست |
| :--- | :--- |
| ① `qiime tools import` | فایل‌های معمولی را به `.qza` تبدیل کن |
| ② `--type EMPPairedEndSequences` | نوع معنایی: «ریدهای جفتی EMP، هنوز جدا نشده» |
| ③ `--input-path emp` | پوشه‌ی سه فایل |
| ④ `--output-path` | نام `.qza` |

این فایل‌ها **۱۳۵٬۴۸۷** جفت رید ۱۵۱ بازی دارند.

> 📺 **فیلم:** *An introduction to QIIME 2*: https://www.youtube.com/watch?v=XIyZWpfcZ6U · *Semantic types and data formats in QIIME 2*: https://www.youtube.com/watch?v=PUsvtJgpNtE
> 📄 **مرجع:** Bolyen E, et al. (2019). *QIIME 2.* Nature Biotechnology 37:852–857. https://doi.org/10.1038/s41587-019-0209-9

---

## ۴. گام ۲: جدا کردن نمونه‌ها (*demultiplex*)

همه‌ی نمونه‌ها در یک ران خوانده شده‌اند. بارکد هر رید می‌گوید از کدام نمونه است.

<div dir="ltr">

```bash
qiime demux emp-paired --i-seqs emp-paired-end-sequences.qza \
  --m-barcodes-file $M --m-barcodes-column barcode-sequence \
  --p-rev-comp-mapping-barcodes \
  --o-per-sample-sequences demux.qza --o-error-correction-details demux-details.qza
qiime demux summarize --i-data demux.qza --o-visualization demux.qzv
```

</div>

| بخش | چیست | بی آن چه می‌شود |
| :--- | :--- | :--- |
| ① `--m-barcodes-file $M` | جدول نمونه‌ها | — |
| ② `--m-barcodes-column barcode-sequence` | ستونی که بارکد هر نمونه را دارد | — |
| ③ `--p-rev-comp-mapping-barcodes` | بارکدهای جدول را **مکمل معکوس** کن | **هیچ** رید به نمونه نمی‌رسد (پایین) |
| ④ `--o-per-sample-sequences` | ریدهای هر نمونه | — |
| ⑤ `--o-error-correction-details` | برای هر رید: کدام بارکد، چند خطای تصحیح‌شده | — |

بی گزینه‌ی ③:

<div dir="ltr">

```text
No sequences were mapped to samples. Check that your barcodes are in the correct orientation
(see the rev_comp_barcodes and/or rev_comp_mapping_barcodes options).
```

</div>

وقتی **هیچ** نمونه‌ای حتی یک رید نمی‌گیرد، مشکل تصادفی نیست، **جهت** است. در این کتابخانه، رید `barcodes` بارکد را به شکل مکمل معکوس آنچه در جدول نوشته شده می‌خواند. این به آماده‌سازی کتابخانه بستگی دارد؛ از مرکز توالی‌یابی بپرسید.

بارکدهای **Golay** چنان ساخته شده‌اند که چند خطای توالی‌یابی را **درست کنند**. نتیجه (از `demux-details.qza`؛ تمرین ۱):

| | جفت رید | ٪ |
| :--- | ---: | ---: |
| کل | 135,487 | ۱۰۰ |
| به یکی از ۷۵ نمونه رسید | **46,712** | ۳۴٫۵ |
| بی نمونه، بارکد بی‌خطا ولی ناشناخته | 60,234 | ۴۴٫۵ |
| بی نمونه، بارکد پرخطا یا `N` | 28,541 | ۲۱٫۱ |

تنها یک‌سوم ریدها به نمونه‌های ما رسیدند. خراب است؟ **نه.** ۶۰٬۲۳۴ رید بارکد **کاملاً سالم** دارند که در جدول ما نیست: این ران MiSeq نمونه‌های **پژوهش‌های دیگری** را هم داشته است. درس: پیش از گفتن «کیفیت ران بد بود»، ببینید ریدهای بی‌صاحب چه بارکدی دارند.

پخش میان نمونه‌ها بسیار نابرابر است: ۴ نمونه **هیچ** رید نگرفتند و بقیه از ۱ تا ۱٬۴۴۲ رید دارند. در داده‌ی کامل هر نمونه کمابیش صد برابر این است.

<details>
<summary>✋ امتحان کن: <code>demux.qzv</code> را در view.qiime2.org باز کنید. زبانه‌ی Overview چه نشان می‌دهد؟</summary>

شمار رید هر نمونه (جدول و نمودار پراکنش)، کمترین، بیشترین و میانه. زبانه‌ی **Interactive Quality Plot** کیفیت هر جایگاه را برای نمونه‌ای از ریدها نشان می‌دهد: ورودی گام بعد.

</details>

---

## ۵. گام ۳: برگزیدن پارامترهای DADA2

### ۵.۱ از نمودار کیفیت

میانه‌ی کیفیت در چند جایگاه (زبانه‌ی Interactive Quality Plot):

| جایگاه | ۱ | ۱۱ | ۲۱ | ۴۱ | ۱۰۱ | ۱۴۱ | ۱۵۱ |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| رید forward | 33 | 33 | 37 | 39 | 38 | 37 | **25** |
| رید reverse | 32 | 33 | 32 | 37 | 31 | 30 | **27** |

دو پارامتر:
- ‏**`--p-trim-left-f/r 13`**: چند باز نخست کیفیت کمتری دارند (۳۳ در برابر ۳۷ تا ۳۹). همان مقدار آموزش رسمی QIIME 2 برای این داده.
- ‏**`--p-trunc-len-f/r 150`**: باز ۱۵۱ آخرین چرخه‌ی ران است و کیفیتش ناگهان می‌افتد (۲۵ و ۲۷).

### ۵.۲ شرط حیاتی: هم‌پوشانی

‏DADA2 پس از پاک کردن خطاها، دو رید هر جفت را **یکی** (*merge*) می‌کند. برای این کار، دو رید باید روی هم بیفتند، دست‌کم **۱۲ باز** (`--p-min-overlap`):

<div dir="ltr">

```text
forward  5' ======================================>  150
reverse                     <====================================== 150
fragment |<------------------------- 253 ------------------------->|
overlap = 150 + 150 - 253 = 47 bases   (>= 12: OK)
```

</div>

اگر طمع کنید و هر دو رید را در ۱۲۰ ببرید: 120 + 120 = 240 < 253، یعنی **هیچ** هم‌پوشانی. DADA2 پس از چند دقیقه کار:

<div dir="ltr">

```text
No features remain after denoising. Try adjusting your truncation and trim parameter settings.
```

</div>

(پیام گمراه‌کننده است: پاک کردن خطا درست انجام شد؛ **یکی کردن** شکست خورد.) ‏`trim-left` روی هم‌پوشانی اثری ندارد، چون از **آغاز** رید می‌بُرد؛ ولی طول نهایی ASV را کم می‌کند: 253 − 13 − 13 = **۲۲۷**.

<details>
<summary>✋ امتحان کن: با <code>trunc-len</code> برابر ۱۵۰ و ۱۳۰، هم‌پوشانی چند باز است؟ پذیرفتنی است؟</summary>

‏150 + 130 − 253 = **۲۷** باز؛ بیشتر از ۱۲، پس پذیرفتنی. ولی حاشیه کمتر است: قطعه‌ای ۲۵۵ بازی (برخی تاکسون‌ها درج دارند) تنها ۲۵ باز هم‌پوشانی دارد. تمرین ۲ چند ترکیب دیگر را می‌سنجد.

</details>

---

## ۶. گام ۴: DADA2

<div dir="ltr">

```bash
qiime dada2 denoise-paired --i-demultiplexed-seqs demux.qza \
  --p-trim-left-f 13 --p-trim-left-r 13 --p-trunc-len-f 150 --p-trunc-len-r 150 --p-n-threads 4 \
  --o-table table.qza --o-representative-sequences rep-seqs.qza \
  --o-denoising-stats denoising-stats.qza --o-base-transition-stats base-transition-stats.qza
```

</div>

| بخش | چیست |
| :--- | :--- |
| ① `--p-trim-left-f/r 13` | ۱۳ باز آغاز هر رید را ببُر |
| ② `--p-trunc-len-f/r 150` | هر رید را در ۱۵۰ کوتاه کن؛ ریدهای کوتاه‌تر کنار می‌روند |
| ③ `--o-table` | جدول ASV: شمار هر ASV در هر نمونه |
| ④ `--o-representative-sequences` | توالی هر ASV |
| ⑤ `--o-denoising-stats` | افت رید در هر مرحله، برای هر نمونه |
| ⑥ `--o-base-transition-stats` | مدل خطای ساخته‌شده؛ در 2026.7 **اجباری** است |

> دستورهای آموزش‌های قدیمی‌تر بی ⑥ این خطا را می‌دهند: `Missing option '--o-base-transition-stats'`. همیشه دستورها را با `--help` همان نسخه بسنجید.

روی ۸ هسته، ۳۲ ثانیه. جمع ستون‌های `denoising-stats` روی همه‌ی نمونه‌ها (تمرین ۳ روش برداشتنش را دارد):

| مرحله | رید | از ورودی |
| :--- | ---: | ---: |
| ورودی | 46,712 | ۱۰۰٪ |
| پس از پالایش (طول، خطای پیش‌بینی‌شده ≤ ۲، N) | 41,834 | ۸۹٫۶٪ |
| پاک‌شده از خطا (*denoised*) | 33,558 | ۷۱٫۸٪ |
| **یکی‌شده (*merged*)** | **16,438** | **۳۵٫۲٪** |
| بی کایمرا (*non-chimeric*) | 16,438 | ۳۵٫۲٪ |

نتیجه: **۴۱۴ ASV**؛ ۳۷۲ تا (۹۰٪) دقیقاً **۲۲۷ باز**، همان عدد پیش‌بینی‌شده.

### بزرگ‌ترین افت: یکی کردن

نیمی از ریدهای پاک‌شده یکی نشدند. ریدها هم‌پوشانی ندارند؟ همان ریدها را بی DADA2، با vsearch یکی کردیم: **۹۲٪** یکی شدند (تمرین ۲). پس مشکل از خود ریدها نیست:
1. ‏DADA2 ریدهای forward و reverse را **جدا** پاک می‌کند و سپس ASVهای دو سو را یکی می‌کند. پیش‌فرض `--p-max-merge-mismatch` **صفر** است: یک ناهمخوانی در ناحیه‌ی هم‌پوشانی، جفت را دور می‌اندازد.
2. با تنها چند صد رید در هر نمونه، مدل خطا همه‌ی خطاهای ریدهای reverse (که بدترند) را درست نمی‌کند. خطاهای مانده در هم‌پوشانی، یکی کردن را خراب می‌کنند.

با `--p-max-merge-mismatch 2` یکی‌شده‌ها به ۱۹٬۸۷۱ می‌رسند، ولی ASVها هم از ۴۱۴ به ۵۳۱ (تمرین ۳). در داده‌ی کامل با ژرفای صد برابر، این مشکل بسیار کوچک‌تر است.

**صفر کایمرا** هم از همین است: کایمرا در DADA2 یعنی ASVی که از دو ASV **پرشمارتر در همان نمونه** ساخته شده باشد. در نمونه‌های چند صد ریدی، «والد»های پرشمار کم‌اند و شناختن کایمرا کمابیش ناشدنی است. صفر این‌جا یعنی «شناخته نشد»، نه «نبود».

> 📺 **فیلم:** *GTN Tutorial: Building an amplicon sequence variant (ASV) table from 16S data using DADA2*: https://www.youtube.com/watch?v=ISocxcJZEjw
> 📄 **مرجع:** Callahan BJ, et al. (2016). *DADA2.* Nature Methods 13:581–583. https://doi.org/10.1038/nmeth.3869

---

## ۷. سه اشتباه رایج

‏**۱. ‏`trunc-len` بی حساب هم‌پوشانی.** `trunc_f + trunc_r − طول آمپلیکون` باید دست‌کم ۱۲ باشد، با کمی حاشیه برای تاکسون‌هایی که قطعه‌ی درازتری دارند. طول آمپلیکون را با یکی کردن ریدها با vsearch بسنجید (تمرین ۲).

**۲. درصد پایین demux را «کیفیت بد» خواندن.** این‌جا ۶۵٪ ریدها به نمونه‌های ما نرسیدند، ولی بیشترشان بارکد سالمِ نمونه‌های پژوهش‌های دیگر بودند. ریدهای بی‌صاحب را بشمارید.

**۳. نخواندن `denoising-stats`.** شمار نهایی ASV به‌تنهایی نمی‌گوید کجا داده از دست رفت. این‌جا افت اصلی در یکی کردن بود و علتش ژرفای کم، نه کیفیت.

---

## 📘 برای کنجکاوها

- ‏**‏`--p-pooling-method pseudo`:** ‏DADA2 دو بار اجرا می‌شود؛ ASVهایی که در دور اول در دست‌کم دو نمونه پیدا شدند، در دور دوم به همه‌ی نمونه‌ها «یادآوری» می‌شوند. در داده‌ی کم‌ژرفا تاکسون‌های کم‌شمار را نجات می‌دهد (تمرین ۳).
- **ریدهای دراز (PacBio، Nanopore):** کل ژن 16S (کمابیش ۱۵۰۰ باز) را می‌خوانند و تفکیک گونه را بسیار بهتر می‌کنند؛ DADA2 برای PacBio HiFi هم روش دارد.
- ‏**‏`qiime tools export`:** هر `.qza` را به فایل‌های معمولی (TSV، FASTA، BIOM) برمی‌گرداند تا با Bash یا پایتون خوانده شوند (تمرین‌ها).

---

## جمع‌بندی

- ‏16S: ارزان، بسیاری نمونه، تفکیک تا جنس؛ بی اندازه‌گیری مستقیم کارکرد.
- ‏QIIME 2: هر گام یک `.qza` با نوع و تاریخچه؛ دستورها با `--i-`، `--p-`، `--m-`، `--o-`.
- ‏demux: جهت بارکد (`--p-rev-comp-mapping-barcodes`) را درست بگیرید؛ ریدهای بی‌صاحب را بشمارید.
- ‏DADA2: `trim-left` از کیفیت آغاز، `trunc-len` از کیفیت پایان و **هم‌پوشانی** (۱۵۰ + ۱۵۰ − ۲۵۳ = ۴۷).
- جدول `denoising-stats`: این‌جا افت اصلی در یکی کردن بود، به‌خاطر ژرفای کم.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
qiime tools import --type EMPPairedEndSequences --input-path emp --output-path emp-paired-end-sequences.qza
qiime demux emp-paired --i-seqs emp-paired-end-sequences.qza --m-barcodes-file $M \
  --m-barcodes-column barcode-sequence --p-rev-comp-mapping-barcodes \
  --o-per-sample-sequences demux.qza --o-error-correction-details demux-details.qza
qiime demux summarize --i-data demux.qza --o-visualization demux.qzv
qiime dada2 denoise-paired --i-demultiplexed-seqs demux.qza \
  --p-trim-left-f 13 --p-trim-left-r 13 --p-trunc-len-f 150 --p-trunc-len-r 150 \
  --o-table table.qza --o-representative-sequences rep-seqs.qza \
  --o-denoising-stats denoising-stats.qza --o-base-transition-stats base-transition-stats.qza
qiime tools export --input-path denoising-stats.qza --output-path exports/stats
# view any .qzv: drag it onto https://view.qiime2.org
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| آمپلیکون | قطعه‌ی DNA که با PCR تکثیر شده |
| ناحیه‌ی متغیر (V1 تا V9) | بخش‌هایی از ژن 16S که میان تاکسون‌ها فرق دارد |
| ‏multiplex / demultiplex | چند نمونه در یک ران / جدا کردن ریدهای هر نمونه با بارکد |
| ‏ASV | توالی دقیق یک آمپلیکون، پس از پاک کردن خطا |
| ‏OTU | خوشه‌ی توالی‌ها با مرز همانندی (برای نمونه ۹۷٪) |
| کایمرا | توالی ساختگی PCR، ساخته از دو توالی واقعی |
| ‏artifact (`.qza`) | فایل داده‌ی QIIME 2، با نوع و تاریخچه |
| ‏metadata | جدول ویژگی‌های نمونه‌ها |

---

## منابع

**مستند و مقاله**
- Bolyen E, et al. (2019). *Reproducible, interactive, scalable and extensible microbiome data science using QIIME 2.* Nature Biotechnology 37:852–857. https://doi.org/10.1038/s41587-019-0209-9
- Callahan BJ, et al. (2016). *DADA2: High-resolution sample inference from Illumina amplicon data.* Nature Methods 13:581–583. https://doi.org/10.1038/nmeth.3869
- Callahan BJ, McMurdie PJ, Holmes SP (2017). *Exact sequence variants should replace operational taxonomic units in marker-gene data analysis.* ISME J 11:2639–2643. https://doi.org/10.1038/ismej.2017.119
- Neilson JW, et al. (2017). *Significant impacts of increasing aridity on the arid soil microbiome.* mSystems 2:e00195-16. https://doi.org/10.1128/mSystems.00195-16
- QIIME 2 amplicon documentation: https://amplicon-docs.qiime2.org/en/latest/ · Installation: https://library.qiime2.org/quickstart/amplicon
- Atacama soils tutorial (this dataset): https://docs.qiime2.org/2024.10/tutorials/atacama-soils/

**کتاب**
- Beiko RG, Hsiao W, Parkinson J (eds.) (2018). *Microbiome Analysis: Methods and Protocols*. Methods Mol Biol 1849. Humana Press.

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins University). دوره‌ای ویژه‌ی QIIME 2 در Coursera نیافتیم؛ نزدیک‌ترین: https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Linux* (The Linux Foundation). دوره‌ای ویژه‌ی آمپلیکون در edX نیافتیم؛ نزدیک‌ترین: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux
- YouTube: *An introduction to QIIME 2* (QIIME 2): https://www.youtube.com/watch?v=XIyZWpfcZ6U
- YouTube: *Semantic types and data formats in QIIME 2* (QIIME 2): https://www.youtube.com/watch?v=PUsvtJgpNtE
- YouTube: *GTN Tutorial: Building an amplicon sequence variant (ASV) table from 16S data using DADA2* (Galaxy Project): https://www.youtube.com/watch?v=ISocxcJZEjw

<sub>نشانی‌های YouTube و DOIها در 2026-10-15 وارسی شدند؛ نشانی‌های Coursera و edX در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
