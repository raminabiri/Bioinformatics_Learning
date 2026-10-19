<div dir="rtl">

# درس: تحلیل آمپلیکون 16S rRNA با QIIME 2

**بخش:** `06_Metagenomics` · **ماژول:** `04_16S_Amplicon` · **پیش‌نیاز:** ماژول ۰۱ این بخش (FASTQ و کیفیت)، آمار پایه · **زمان:** ۳ ساعت · **ابزار:** QIIME 2 2026.7 (DADA2، q2-feature-classifier با scikit-learn 1.7.1، q2-diversity)، vsearch، MAFFT، FastTree · **آخرین تست:** 2026-10-15

> ⚠️ **داده و مرجع این درس فقط برای تمرین است.** زیرنمونه‌ی ۱٪ یک ران واقعی (میانه‌ی ۲۴۳ رید در هر نمونه بعد از DADA2) و طبقه‌بندی که فقط تا سطح **جنس** و فقط برای ناحیه‌ی V4 آموزش دیده. در پژوهش واقعی: ده‌ها هزار رید در هر نمونه، مرجع کامل (SILVA 138.2، GTDB یا Greengenes2) که با RESCRIPt برای پرایمرهای خودتان آماده شده، و **کنترل منفی و mock community در همان ران**.

---

## ۱. مسئله

بیابان آتاکاما (شیلی) یکی از خشک‌ترین خاک‌های زمین است. Neilson و همکاران (2017) در دو مسیر (transect) به نام‌های **Baquedano** و **Yungay** از ارتفاع ۸۹۵ تا ۴٬۶۹۷ متر نمونه‌ی خاک گرفتند و پرسیدند: **جامعه‌ی میکروبی خاک با رطوبت، ارتفاع و پوشش گیاهی چطور عوض می‌شود؟**

برای این سؤال، توالی‌یابی آمپلیکون 16S انتخاب منطقی است:

| | آمپلیکون 16S | ‏Shotgun (ماژول ۰۶) |
| :--- | :--- | :--- |
| چه چیزی خوانده می‌شود | یک ناحیه‌ی ۲۵۰–۴۵۰ بازی از یک ژن | قطعه‌های تصادفی از همه‌ی DNA |
| هزینه در هر نمونه | کم؛ صدها نمونه در یک ران MiSeq | چندین برابر |
| تفکیک تاکسونومیک | معمولاً **جنس**؛ گونه به‌ندرت | گونه و گاهی سویه |
| عملکرد (ژن‌ها) | ❌ فقط **پیش‌بینی** (PICRUSt2 و مانند آن) | ✅ اندازه‌گیری مستقیم |
| ‏DNA میزبان | مشکل نیست (پرایمر اختصاصی باکتری و آرکیاست) | مشکل بزرگ (ماژول ۰۲) |
| سوگیری اصلی | پرایمر، تعداد نسخه‌ی ژن 16S، PCR | عمق، طول ژنوم، دیتابیس |
| ویروس و یوکاریوت | ❌ | ✅ |

**قاعده:** وقتی سؤال «چه کسی، چقدر، و آیا بین گروه‌ها فرق دارد؟» است و نمونه زیاد است، 16S کافی و ارزان است. وقتی سؤال «چه ژن‌هایی، کدام سویه، کدام مسیر متابولیک؟» است، shotgun لازم است.

## ۲. مفاهیم

### ۲.۱ ژن 16S و ناحیه‌ی V4
ژن 16S rRNA حدود ۱٬۵۰۰ باز است: نواحی **حفاظت‌شده** که پرایمر به آن‌ها می‌چسبد، و **۹ ناحیه‌ی متغیر** (V1 تا V9) که تفاوت تاکسون‌ها در آن‌هاست. پروژه‌ی Earth Microbiome (EMP) ناحیه‌ی **V4** را با پرایمرهای **515F/806R** استاندارد کرد. قطعه‌ی حاصل حدود ۲۵۳ باز (بدون پرایمر) است، پس دو رید ۱۵۰ بازی MiSeq روی هم می‌افتند و کل قطعه را می‌پوشانند.

پیامدهای انتخاب ناحیه:
- **هیچ ناحیه‌ای همه‌ی تاکسون‌ها را خوب تفکیک نمی‌کند.** V4 کوتاه و پرکاربرد است ولی بعضی جنس‌های نزدیک (مثل *Escherichia* و *Shigella*) را از هم جدا نمی‌کند.
- **پرایمر سوگیری دارد.** نسخه‌ی اصلاح‌شده‌ی پرایمرها (515F-Y، 806RB) را برای پوشش بهتر SAR11 و Thaumarchaeota ساختند. نتایج دو مطالعه با پرایمر متفاوت مستقیماً قابل مقایسه نیستند.
- **تعداد نسخه‌ی ژن 16S** در ژنوم باکتری‌ها از ۱ تا بیش از ۱۰ فرق می‌کند. پس «درصد ریدها» برابر «درصد سلول‌ها» نیست.

### ‏۲.۲ ASV در برابر OTU
روش قدیمی ریدها را با آستانه‌ی ۹۷٪ شباهت در **OTU** خوشه‌بندی می‌کرد. **DADA2** یک **مدل خطای** مخصوص همان ران می‌سازد و برای هر توالی منحصربه‌فرد می‌پرسد: «آیا این توالی واقعی است یا نسخه‌ی خطادار یک توالی پرتعدادتر؟» خروجی **ASV** (Amplicon Sequence Variant) است، یعنی توالی دقیق با تفکیک یک باز.

مزیت ASV: **قابل مقایسه بین مطالعه‌ها** است (یک توالی، یک شناسه)، در حالی که OTU به داده‌ی همان مطالعه وابسته است. QIIME 2 شناسه‌ی هر ASV را **هش MD5 توالی‌اش** می‌گذارد. پس یک ASV در هر پروژه‌ای همان شناسه را دارد.

### ‏۲.۳ QIIME 2: artifact، نوع معنایی، provenance
- ‏**`.qza`** (artifact): داده + نوع + **تاریخچه‌ی کامل** (کدام دستور، کدام پارامتر، کدام نسخه، از کدام ورودی). خودش یک فایل zip است.
- ‏**`.qzv`** (visualization): گزارش تعاملی. با `qiime tools view` یا با کشیدن روی https://view.qiime2.org باز می‌شود.
- **نوع معنایی (semantic type)**، مثل `FeatureTable[Frequency]` یا `SampleData[PairedEndSequencesWithQuality]`، جلوی اشتباه‌هایی مثل دادن جدول خام به جای جدول rarefy‌شده را می‌گیرد.
- ‏**Provenance:** هر `.qza` را که در view.qiime2.org باز کنید، زبانه‌ی Provenance کل زنجیره‌ی تحلیل را نشان می‌دهد. این تکرارپذیری **داخلی** است و جایگزین ثبت دستورها در اسکریپت نیست.

### ۲.۴ داده‌ی ترکیبی (compositional)
جدول ASV **تعداد مطلق** باکتری‌ها نیست. عمق توالی‌یابی هر نمونه تصادفی است و فقط **نسبت‌ها** معنی دارند. دو پیامد مهم:
- بین نمونه‌ها با عمق متفاوت نمی‌توان تعداد خام را مقایسه کرد. یا باید **rarefy** کرد (زیرنمونه‌گیری تا عمق یکسان)، یا از روش‌های مبتنی بر لگاریتم نسبت (CLR) استفاده کرد.
- افزایش یک تاکسون، **ظاهراً** بقیه را کم می‌کند، حتی اگر در واقع تغییری نکرده باشند.

## ۳. داده

| | |
| :--- | :--- |
| منبع | آموزش رسمی QIIME 2 «Atacama soil microbiome»، زیرنمونه‌ی **۱٪** |
| پروتکل | ‏EMP paired-end: سه فایل `forward`، `reverse`، `barcodes` (بارکدهای Golay ۱۲ بازی در یک رید جدا) |
| توالی‌یابی | ‏Illumina MiSeq، 2×151، ناحیه‌ی V4 (515F/806R) |
| نمونه‌ها | ۷۵ نمونه در فایل metadata؛ ستون‌های مهم: `transect-name`، `elevation`، `vegetation`، `ph`، رطوبت و دما |
| مرجع طبقه‌بندی | ‏SILVA 138 (۹۹٪) بریده‌شده به ناحیه‌ی 515F/806R: **۳۱۳٬۷۳۴** توالی |

<div dir="ltr">

```bash
cd 06_Metagenomics
bash 04_16S_Amplicon/data/download.sh       # ~53 MB, md5-checked
export PATH=/data/MicrobiomePipeline/qiime2_env/bin:$PATH   # QIIME 2 on the course server
export UNIFRAC_USE_GPU=N                    # see section 4.6
qiime --version | head -1                   # q2cli version 2026.7.0
mkdir -p work/04_16s && cd work/04_16s
M=../../04_16S_Amplicon/data/sample_metadata.tsv
```

</div>

فایل metadata یک سطر دوم خاص دارد: `#q2:types categorical numeric …`. این سطر به QIIME 2 می‌گوید هر ستون عددی است یا دسته‌ای. اگر نباشد، `elevation` ممکن است دسته‌ای خوانده شود و آزمون همبستگی روی آن اجرا نشود.

## ۴. کار عملی گام‌به‌گام

### ۴.۱ Import

<div dir="ltr">

```bash
mkdir -p emp
for f in forward reverse barcodes; do ln -sf "$(realpath ../../04_16S_Amplicon/data/raw/$f.fastq.gz)" emp/; done
qiime tools import --type EMPPairedEndSequences --input-path emp --output-path emp-paired-end-sequences.qza
```

</div>

<div dir="ltr">

```text
Imported emp as EMPPairedEndDirFmt to emp-paired-end-sequences.qza
```

</div>

‏QIIME 2 نام فایل‌ها را **دقیقاً** `forward.fastq.gz`، `reverse.fastq.gz` و `barcodes.fastq.gz` انتظار دارد. این فایل‌ها **۱۳۵٬۴۸۷** جفت رید ۱۵۱ بازی دارند.

### ‏۴.۲ Demultiplex: جدا کردن نمونه‌ها

<div dir="ltr">

```bash
qiime demux emp-paired --i-seqs emp-paired-end-sequences.qza \
  --m-barcodes-file $M --m-barcodes-column barcode-sequence \
  --p-rev-comp-mapping-barcodes \
  --o-per-sample-sequences demux.qza --o-error-correction-details demux-details.qza
qiime demux summarize --i-data demux.qza --o-visualization demux.qzv
```

</div>

- ‏`--p-rev-comp-mapping-barcodes`: در این پروتکل، بارکدی که در metadata نوشته شده **مکمل معکوس** بارکدی است که در رید `barcodes` خوانده می‌شود. بدون این گزینه تقریباً هیچ ریدی به نمونه‌ای نمی‌رسد. این بستگی به آماده‌سازی کتابخانه دارد؛ از مرکز توالی‌یابی بپرسید.
- بارکدهای **Golay** طوری طراحی شده‌اند که خطای توالی‌یابی را **تصحیح** کنند. `demux-details.qza` برای هر رید نشان می‌دهد چند خطا تصحیح شد.

نتیجه:
| | جفت رید | درصد |
| :--- | ---: | ---: |
| کل | 135,487 | ۱۰۰ |
| به یکی از ۷۵ نمونه رسید | **46,712** | ۳۴٫۵ |
| بدون نمونه (بارکد بی‌خطا ولی ناشناخته) | 60,234 | ۴۴٫۵ |
| بدون نمونه (بارکد با خطا یا N) | 28,541 | ۲۱٫۱ |

فقط یک‌سوم ریدها به نمونه‌های ما رسید. آیا demultiplex خراب است؟ نه. **۶۰٬۲۳۴ رید بارکد کاملاً سالم دارند** که در metadata ما نیست. این ران MiSeq نمونه‌های **مطالعه‌های دیگری** را هم داشته است. درس: قبل از نتیجه‌گیری «کیفیت ران بد بود»، ببینید ریدهای بی‌صاحب چه بارکدی دارند (تمرین ۱).

توزیع بین نمونه‌ها بسیار نامتوازن است: ۴ نمونه **هیچ** ریدی نگرفتند و بقیه از ۱ تا ۱٬۴۴۲ رید دارند. در داده‌ی کامل، هر نمونه حدود صد برابر این رید دارد.

### ۴.۳ نگاه به کیفیت و انتخاب پارامترهای DADA2
‏`demux.qzv` را باز کنید و زبانه‌ی **Interactive Quality Plot** را ببینید. میانه‌ی کیفیت در چند موقعیت:

| موقعیت | ۱ | ۱۱ | ۲۱ | ۴۱ | ۱۰۱ | ۱۴۱ | ۱۵۱ |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| رید forward | 33 | 33 | 37 | 39 | 38 | 37 | **25** |
| رید reverse | 32 | 33 | 32 | 37 | 31 | 30 | **27** |

تصمیم‌ها:
- ‏**`--p-trim-left-f/r 13`**: چند باز اول کیفیت کمتری دارند (میانه‌ی ۳۳ در برابر ۳۷ تا ۳۹). این همان مقداری است که آموزش رسمی QIIME 2 برای این داده استفاده می‌کند.
- ‏**`--p-trunc-len-f/r 150`**: باز ۱۵۱ آخرین چرخه‌ی ران است و کیفیتش به‌شدت افت می‌کند (میانه‌ی ۲۵).

**شرط حیاتی: همپوشانی.** طول قطعه‌ی V4 حدود ۲۵۳ باز است (با ادغام ریدها توسط vsearch اندازه‌گیری شد، تمرین ۲). پس:

<div dir="ltr">

```text
overlap = trunc_len_f + trunc_len_r - amplicon_length = 150 + 150 - 253 = 47 bases
```

</div>

‏DADA2 حداقل **۱۲ باز** همپوشانی می‌خواهد (`--p-min-overlap`). اگر طمع کنید و هر دو رید را از ۱۲۰ کوتاه کنید (۱۲۰ + ۱۲۰ = ۲۴۰ < ۲۵۳)، هیچ جفتی ادغام نمی‌شود:

<div dir="ltr">

```text
No features remain after denoising. Try adjusting your truncation and trim parameter settings.
```

</div>

‏`trim-left` روی همپوشانی اثری ندارد، چون از ابتدای رید (دور از ناحیه‌ی همپوشانی) می‌بُرد. ولی طول نهایی ASV را کم می‌کند: ۲۵۳ − ۱۳ − ۱۳ = **۲۲۷**.

### ۴.۴ DADA2

<div dir="ltr">

```bash
qiime dada2 denoise-paired --i-demultiplexed-seqs demux.qza \
  --p-trim-left-f 13 --p-trim-left-r 13 --p-trunc-len-f 150 --p-trunc-len-r 150 --p-n-threads 4 \
  --o-table table.qza --o-representative-sequences rep-seqs.qza \
  --o-denoising-stats denoising-stats.qza --o-base-transition-stats base-transition-stats.qza
```

</div>

> در QIIME 2 2026.7 خروجی `--o-base-transition-stats` **اجباری** است (نرخ تبدیل بازها در هر کیفیت، یعنی همان مدل خطا). دستورهای آموزش‌های قدیمی‌تر بدون آن خطای `Missing option '--o-base-transition-stats'` می‌دهند.

اجرا روی ۸ هسته ۳۲ ثانیه طول کشید. جمع ستون‌های `denoising-stats` روی همه‌ی نمونه‌ها:

| مرحله | رید | از ورودی |
| :--- | ---: | ---: |
| ورودی | 46,712 | ۱۰۰٪ |
| بعد از فیلتر (طول، `maxEE = 2`، N) | 41,834 | ۸۹٫۶٪ |
| denoised | 33,558 | ۷۱٫۸٪ |
| **merged** | **16,438** | **۳۵٫۲٪** |
| non-chimeric | 16,438 | ۳۵٫۲٪ |

نتیجه: **۴۱۴ ASV**، که ۳۷۲ تا (۹۰٪) دقیقاً **۲۲۷ باز** هستند (همان عددی که پیش‌بینی کردیم).

**بزرگ‌ترین افت در ادغام است: نیمی از ریدهای denoise‌شده ادغام نشدند.** آیا ریدها همپوشانی ندارند؟ همان ریدها را بدون DADA2 با vsearch ادغام کردیم: **۹۲٪** ادغام شدند. پس مشکل در خود ریدها نیست. دلیل این است که:
1. ‏DADA2 ریدهای forward و reverse را **جداگانه** denoise می‌کند و بعد ASVهای دو طرف را ادغام می‌کند. پیش‌فرض `--p-max-merge-mismatch` برابر **۰** است: یک اختلاف در ناحیه‌ی همپوشانی کافی است تا جفت دور ریخته شود.
2. با فقط چند صد رید در هر نمونه، مدل خطا نمی‌تواند همه‌ی خطاهای ریدهای reverse را (که کیفیت پایین‌تری دارند) تصحیح کند. خطاهای باقی‌مانده در همپوشانی، ادغام را خراب می‌کنند.

شاهد: با `--p-max-merge-mismatch 2` ادغام به ۱۹٬۸۷۱ و با pseudo-pooling هم به ۲۳٬۲۷۶ می‌رسد، ولی تعداد ASV هم از ۴۱۴ به ۵۳۱ و ۷۳۹ بالا می‌رود (تمرین ۳). در داده‌ی کامل با عمق صد برابر، این مشکل خیلی کوچک‌تر است.

**صفر chimera** هم به همین دلیل است: chimera در DADA2 یعنی ASVی که از دو ASV **پرتعدادتر** در **همان نمونه** ساخته شده باشد. در نمونه‌های چندصد ریدی، والدهای پرتعداد کمی وجود دارد و تشخیص chimera عملاً ممکن نیست. صفر chimera این‌جا یعنی «تشخیص داده نشد»، نه «وجود نداشت».

### ۴.۵ طبقه‌بندی تاکسونومیک

#### الف) طبقه‌بند باید با نسخه‌ی scikit-learn شما بخواند
طبقه‌بند Naive Bayes در QIIME 2 یک شیء **pickle‌شده‌ی scikit-learn** است. طبقه‌بندهای SILVA و Greengenes2 موجود روی سرور با scikit-learn 1.4.2 ساخته شده‌اند و QIIME 2 2026.7 با 1.7.1 کار می‌کند:

<div dir="ltr">

```text
Plugin error from feature-classifier:
  The scikit-learn version (1.4.2) used to generate this artifact does not match the current version
  of scikit-learn installed (1.7.1). Please retrain your classifier for your current deployment to
  prevent data-corruption errors.
```

</div>

این یک **ویژگی ایمنی** است، نه باگ: pickle بین نسخه‌ها ممکن است بی‌صدا نتیجه‌ی غلط بدهد. دو راه دارید: طبقه‌بند آماده‌ی هم‌نسخه را از صفحه‌ی Data Resources همان نسخه‌ی QIIME 2 بگیرید، یا خودتان آموزش دهید.

#### ب) آموزش طبقه‌بند خودمان

<div dir="ltr">

```bash
bash 04_16S_Amplicon/scripts/train_classifier.sh      # once; from 06_Metagenomics/
```

</div>

مرجع، SILVA 138 بریده‌شده به ناحیه‌ی 515F/806R است. چرا **بریده‌شده**؟ چون طبقه‌بندی که روی همان ناحیه‌ی ریدهای شما آموزش ببیند، دقیق‌تر است (Bokulich et al. 2018).

ما فقط تا سطح **جنس** آموزش دادیم:

| سطح برچسب | تعداد کلاس | حافظه | زمان |
| :--- | ---: | ---: | ---: |
| گونه | 67,689 | بیش از ۱۲ گیگابایت (متوقف شد) | — |
| **جنس** | **8,415** | ۵٫۵ گیگابایت | ۸ دقیقه |

حافظه‌ی Naive Bayes تقریباً با «تعداد کلاس × تعداد ویژگی (۸٬۱۹۲ k-mer هش‌شده)» بالا می‌رود. حذف سطح گونه منطقی است، چون یک قطعه‌ی ۲۵۰ بازی V4 به‌ندرت گونه را با اطمینان تشخیص می‌دهد. نام‌های گونه در SILVA هم اغلب `uncultured_bacterium` هستند.

#### ج) طبقه‌بندی

<div dir="ltr">

```bash
qiime feature-classifier classify-sklearn --i-classifier ../../04_16S_Amplicon/data/db/silva-138-99-515-806-genus-nb.qza \
  --i-reads rep-seqs.qza --p-n-jobs 1 --o-classification taxonomy.qza
qiime taxa barplot --i-table table.qza --i-taxonomy taxonomy.qza --m-metadata-file $M --o-visualization taxa-bar-plots.qzv
```

</div>

خروجی برای هر ASV یک رشته‌ی تاکسونومیک و یک **Confidence** دارد. طبقه‌بند به عمیق‌ترین سطحی می‌رود که اطمینانش از آستانه‌ی **۰٫۷** (پیش‌فرض `--p-confidence`) بالاتر باشد:

| عمیق‌ترین سطح | تعداد ASV |
| :--- | ---: |
| جنس | **368** (۸۹٪) |
| خانواده | 32 |
| راسته / رده / شاخه | 5 / 5 / 1 |
| فقط «Bacteria» | 3 |

شاخه‌های غالب (تعداد ASV): **Actinobacteriota ۱۷۰**، Proteobacteria ۶۵، Chloroflexi ۳۹، Acidobacteriota ۲۸، Gemmatimonadota ۲۵. غلبه‌ی اکتینوباکتری‌ها با خاک‌های خشک و پرتابش سازگار است. **۱۳ ASV آرکی** هم هست (عمدتاً Nitrososphaeraceae، اکسیدکننده‌های آمونیاک)، چون 515F/806R آرکی‌ها را هم تکثیر می‌کند.

فراوان‌ترین «جنس»ها (درصد از کل ریدها):

| برچسب | ٪ | نکته |
| :--- | ---: | :--- |
| `g__wb1-P19` | 16.9 | نام موقت SILVA (Nitrosococcaceae)، بدون نماینده‌ی کشت‌شده |
| `g__uncultured` | 15.6 | **جنس نیست**: برچسب جای‌خالی در ۲۰ دودمان (lineage) مختلف |
| `g__67-14` | 8.5 | نام موقت، هم‌نام خانواده‌اش |
| `g__Rubrobacter` | 5.9 | جنس واقعی؛ مقاوم به خشکی و پرتو |
| `g__Crossiella` | 4.3 | اکتینوباکتری |

**دام مهم:** همین جدول بالا مثال این دام است. ما ریدها را فقط با **نام جنس** جمع زدیم، و `g__uncultured` از ۲۰ دودمان مختلف (مثلاً Pirellulaceae، Gemmataceae و یک خانواده‌ی بی‌نام در Burkholderiales) در **یک ردیف** جمع شد: یک «جنس» ساختگی ۱۵٫۶ درصدی. `qiime taxa collapse --p-level 6` این اشتباه را نمی‌کند، چون شناسه‌ی هر سطر را کل دودمان می‌گذارد (۲۰ سطر جدا). ولی وقتی جدول را در pandas یا R با ستون «genus» گروه‌بندی می‌کنید، باید خودتان حواستان باشد. همیشه برچسب را با سطح بالاتر همراه کنید.

#### د) مقایسه با روش دوم: vsearch

<div dir="ltr">

```bash
qiime feature-classifier classify-consensus-vsearch --i-query rep-seqs.qza \
  --i-reference-reads ../../04_16S_Amplicon/data/db/silva-138-99-seqs-515-806.qza \
  --i-reference-taxonomy ../../04_16S_Amplicon/data/db/silva-138-99-tax-515-806.qza \
  --p-threads 4 --o-classification taxonomy-vsearch.qza --o-search-results vsearch-hits.qza
```

</div>

این روش نیاز به آموزش ندارد (۱۳ ثانیه اجرا شد). برای هر ASV نزدیک‌ترین توالی‌های مرجع را پیدا می‌کند و تاکسونومی **اجماع** آن‌ها را برمی‌گرداند. توافق دو روش:
- **شاخه:** ۴۱۰ از ۴۱۴ ASV یکسان (۹۹٪)
- **جنس:** از ۳۴۰ ASV که هر دو روش تا جنس رفتند، **۳۱۶** یکسان (۹۳٪)

پس در سطح بالا هر دو روش یک داستان می‌گویند. در سطح جنس حدود ۷٪ اختلاف دارند. این برای گزارش «جنس X در گروه A بیشتر بود» مهم است.

### ۴.۶ درخت فیلوژنی و تنوع

<div dir="ltr">

```bash
qiime phylogeny align-to-tree-mafft-fasttree --i-sequences rep-seqs.qza --p-n-threads 4 \
  --o-alignment aligned-rep-seqs.qza --o-masked-alignment masked-aligned-rep-seqs.qza \
  --o-tree unrooted-tree.qza --o-rooted-tree rooted-tree.qza
```

</div>

درخت برای معیارهای **فیلوژنتیک** (Faith PD، UniFrac) لازم است. این درخت از ۲۲۷ باز ساخته شده و برای **فاصله‌ی تقریبی** کافی است، ولی برای ادعای فیلوژنتیک (روابط تکاملی) نه.

**انتخاب عمق rarefaction** مهم‌ترین تصمیم این بخش است. تعداد رید هر نمونه بعد از DADA2:

<div dir="ltr">

```text
0 (15 samples), 1, 1, 1, 26, 47, 51, 90, 124, 126, 140, 159, … , 583, 584, 586
```

</div>

| عمق | نمونه‌های باقی‌مانده (از ۷۱) |
| ---: | ---: |
| 100 | 49 |
| **150** | **46** |
| 200 | 39 |
| 300 | 28 |

عمق بالاتر یعنی تنوع دقیق‌تر در هر نمونه ولی نمونه‌ی کمتر. عمق **۱۵۰** را انتخاب کردیم. نمونه‌های زیر ۱۵۰ رید کنار می‌روند.

<div dir="ltr">

```bash
export UNIFRAC_USE_GPU=N
qiime diversity core-metrics-phylogenetic --i-phylogeny rooted-tree.qza --i-table table.qza \
  --p-sampling-depth 150 --p-random-seed 42 --m-metadata-file $M --output-dir core-metrics-results
```

</div>

- ‏**`UNIFRAC_USE_GPU=N`**: برنامه‌ی `ssu` (UniFrac) در این نصب برای GPU کامپایل شده و روی سروری بدون GPU مناسب با این پیام متوقف می‌شود: `Accelerator Fatal Error: This file was compiled: -acc=gpu …`. این متغیر آن را به CPU برمی‌گرداند.
- ‏**`--p-random-seed 42`**: rarefy تصادفی است. بدون seed، هر اجرا اعداد کمی متفاوت می‌دهد و نتیجه‌ی شما با گزارش قبلی‌تان نمی‌خواند.

خروجی: چهار معیار آلفا (`observed_features`، `shannon`، `faith_pd`، `evenness`)، چهار ماتریس فاصله‌ی بتا (Jaccard، Bray-Curtis، UniFrac وزن‌دار و بی‌وزن)، و PCoA و نمودار Emperor برای هر کدام.

| معیار بتا | چه چیزی را می‌سنجد |
| :--- | :--- |
| Jaccard | حضور یا غیاب، بدون درخت |
| Bray-Curtis | فراوانی، بدون درخت |
| ‏UniFrac بی‌وزن | حضور یا غیاب + فاصله‌ی فیلوژنتیک؛ حساس به تاکسون‌های **کم‌یاب** |
| ‏UniFrac وزن‌دار | فراوانی + فاصله‌ی فیلوژنتیک؛ تحت تأثیر تاکسون‌های **غالب** |

### ۴.۷ آزمون‌های آماری

**تنوع آلفا** (Kruskal-Wallis، ۴۶ نمونه):

<div dir="ltr">

```bash
qiime diversity alpha-group-significance --i-alpha-diversity core-metrics-results/faith_pd_vector.qza \
  --m-metadata-file $M --o-visualization core-metrics-results/faith_pd-group-significance.qzv
qiime diversity alpha-correlation --i-alpha-diversity core-metrics-results/faith_pd_vector.qza \
  --m-metadata-file $M --o-visualization core-metrics-results/faith-pd-correlation.qzv
```

</div>

| معیار | ‏vegetation (۱۵ بدون / ۳۱ با گیاه) | transect (۲۰ / ۲۶) |
| :--- | :--- | :--- |
| Faith PD | H = 5.01، **p = 0.025** | H = 0.20، p = 0.66 |
| Shannon | H = 4.40، **p = 0.036** | H = 1.08، p = 0.30 |
| Observed features | H = 2.29، p = 0.13 | H = 0.01، p = 0.93 |

همبستگی Spearman، Faith PD با **ارتفاع**: ρ = 0.388، **p = 0.0077**. با **pH**: ρ = −0.099، p = 0.51.

**تنوع بتا** (PERMANOVA، ۹۹۹ جایگشت):

<div dir="ltr">

```bash
qiime diversity beta-group-significance --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
  --m-metadata-file $M --m-metadata-column vegetation --p-pairwise \
  --o-visualization core-metrics-results/unweighted-unifrac-vegetation-significance.qzv
```

</div>

| فاصله | vegetation | transect |
| :--- | :--- | :--- |
| ‏UniFrac بی‌وزن | pseudo-F = 3.77، **p = 0.001** | pseudo-F = 1.57، p = 0.058 |
| Bray-Curtis | pseudo-F = 2.36، **p = 0.001** | pseudo-F = 1.76، **p = 0.001** |

‏p-value در PERMANOVA از جایگشت تصادفی می‌آید و QIIME 2 برای آن seed ندارد. پس در اجرای شما ممکن است کمی فرق کند (مثلاً 0.058 در برابر 0.062). با ۹۹۹ جایگشت، کوچک‌ترین p ممکن **0.001** است، پس «p = 0.001» یعنی «p ≤ 0.001».

**آیا تفاوت در «مرکز» گروه‌هاست یا در «پراکندگی»؟** PERMANOVA به تفاوت پراکندگی (dispersion) هم حساس است. اگر یک گروه فقط **پراکنده‌تر** باشد، PERMANOVA هم ممکن است معنی‌دار شود (Anderson 2001). آزمون PERMDISP این را جدا می‌کند:

<div dir="ltr">

```bash
qiime diversity beta-group-significance ... --m-metadata-column vegetation --p-method permdisp ...
```

</div>

<div dir="ltr">

```text
PERMDISP  F = 0.042  p = 0.842
```

</div>

پراکندگی دو گروه فرقی ندارد. پس معنی‌داری PERMANOVA واقعاً تفاوت **ترکیب** را نشان می‌دهد.

### ۴.۸ مخدوش‌شدگی (Confounding): مهم‌ترین نکته‌ی این درس
تا این‌جا نتیجه‌ی وسوسه‌انگیز این است: «پوشش گیاهی ترکیب و تنوع میکروبی خاک را تغییر می‌دهد.» حالا به metadata نگاه کنید:

<div dir="ltr">

```bash
awk -F'\t' 'NR>2{print $3, $20}' $M | sort -n | uniq -c
```

</div>

| vegetation | بازه‌ی ارتفاع سایت‌ها (متر) |
| :--- | :--- |
| `no` | ۸۹۵ تا ۳٬۱۸۴ |
| `yes` | ۲٬۶۸۷ تا ۴٬۶۹۷ |

دو گروه فقط در بازه‌ی باریک ۲٬۶۸۷ تا ۳٬۱۸۴ متر با هم همپوشانی دارند.

**همه‌ی سایت‌های گیاه‌دار در ارتفاع ≥ ۲٬۶۸۷ متر هستند.** ارتفاع با رطوبت و دما هم همراه است. پس «اثر گیاه» و «اثر ارتفاع» از هم جدا نیستند. مدل چندمتغیره:

<div dir="ltr">

```bash
qiime diversity adonis --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
  --m-metadata-file $M --p-formula "elevation+vegetation" --o-visualization core-metrics-results/unweighted-unifrac-adonis.qzv
```

</div>

<div dir="ltr">

```text
            Df  SumOfSqs     R2      F  Pr(>F)
elevation    1    0.776  0.070  3.354   0.001
vegetation   1    0.335  0.030  1.446   0.092
Residual    43    9.952  0.900
```

</div>

وقتی ارتفاع اول وارد مدل شود، **پوشش گیاهی دیگر معنی‌دار نیست** (p = 0.092). `adonis` در QIIME 2 جمع مربعات **ترتیبی** (sequential، type I) حساب می‌کند. یعنی `vegetation` فقط با تغییراتی سنجیده می‌شود که ارتفاع توضیح نداده است.

حالا ترتیب را برعکس کنید (`--p-formula "vegetation+elevation"`):

<div dir="ltr">

```text
            Df  SumOfSqs     R2      F  Pr(>F)
vegetation   1    0.873  0.079  3.773   0.001
elevation    1    0.238  0.021  1.027   0.385
```

</div>

این بار **ارتفاع** بعد از پوشش گیاهی معنی‌دار نیست. هر متغیری که اول وارد شود، سهم **مشترک** دو متغیر را برمی‌دارد. سهم اختصاصی هیچ‌کدام به‌تنهایی معنی‌دار نیست. پس با این داده **نمی‌توان گفت** اثر از ارتفاع است یا از گیاه. فقط می‌توان گفت ترکیب میکروبی با «ارتفاع/پوشش گیاهی» همراه است.

نکته‌ی دیگر: **R² = 0.07**. ارتفاع فقط ۷٪ تغییرات UniFrac را توضیح می‌دهد و ۹۰٪ «باقیمانده» است. «معنی‌دار» با «مهم» یکی نیست.

**درس:** در مطالعه‌ی مشاهده‌ای (نه آزمایشی)، متغیرها با هم همبسته‌اند. قبل از نسبت دادن اثر به یک متغیر، جدول متقاطع متغیرها را ببینید و مدل چندمتغیره بسازید. این مخدوش‌شدگی را فقط **طراحی نمونه‌برداری** حل می‌کند: سایت‌های گیاه‌دار و بی‌گیاه در **همان** ارتفاع.

### ۴.۹ کل ماژول در یک اسکریپت

<div dir="ltr">

```bash
cd 06_Metagenomics
bash 04_16S_Amplicon/scripts/run_16s.sh       # 2 min 48 s
bash 04_16S_Amplicon/scripts/check.sh         # Result: 14 passed, 0 failed
```

</div>

> در QIIME 2 2026.7، `feature-table summarize` هم عوض شده: به جای `--m-sample-metadata-file` و `--o-visualization`، حالا `--m-metadata-file` و سه خروجی `--o-feature-frequencies`، `--o-sample-frequencies` و `--o-summary` دارد. همیشه دستورها را با `--help` همان نسخه چک کنید، نه با آموزش‌های قدیمی وب.

## ۵. دام‌ها (Pitfalls)

| دام | چرا مشکل است | راه درست |
| :--- | :--- | :--- |
| ‏`trunc-len` بدون حساب همپوشانی | ادغام صفر یا خیلی کم | ‏`f + r − طول آمپلیکون ≥ ۱۲ + حاشیه‌ی اطمینان` |
| تفسیر نرخ پایین demux به‌عنوان کیفیت بد | ریدهای مطالعه‌های دیگر هم در ران‌اند | بارکدهای بی‌صاحب را بشمارید |
| طبقه‌بند با نسخه‌ی دیگر scikit-learn | خطا (یا در نسخه‌های قدیمی، نتیجه‌ی غلط بی‌صدا) | طبقه‌بند هم‌نسخه یا آموزش مجدد |
| طبقه‌بند full-length برای ریدهای V4 | دقت کمتر | مرجع بریده‌شده با همان پرایمرها |
| گروه‌بندی با نام جنس به‌تنهایی | ‏`g__uncultured` از ۲۰ دودمان یک «جنس» ساختگی می‌سازد | با کل دودمان گروه‌بندی کنید (`taxa collapse`) |
| گزارش گونه از V4 | ‏V4 معمولاً گونه را تفکیک نمی‌کند | تا جنس گزارش کنید، یا full-length (PacBio/Nanopore) |
| ‏rarefy بدون seed | نتایج غیرقابل تکرار | `--p-random-seed` |
| عمق rarefaction بدون گزارش نمونه‌های حذف‌شده | سوگیری پنهان | عمق و تعداد نمونه‌های حذف‌شده را بنویسید |
| ‏PERMANOVA بدون PERMDISP | ممکن است فقط پراکندگی متفاوت باشد | هر دو را گزارش کنید |
| یک متغیر در مطالعه‌ی مشاهده‌ای | مخدوش‌شدگی (vegetation و elevation) | جدول متقاطع + `adonis` با چند متغیر و هر دو ترتیب |
| نبود کنترل منفی | آلودگی کیت (kitome) در نمونه‌های کم‌زیست‌توده (مثل خاک بیابان) غالب می‌شود | کنترل منفی استخراج و PCR + `decontam` |
| «صفر chimera» = پاک | با عمق کم، chimera تشخیص داده نمی‌شود | عمق کافی؛ گزارش محدودیت |
| پیش‌بینی عملکرد (PICRUSt2) به‌عنوان اندازه‌گیری | استنباط از ژنوم‌های مرجع است | «پیش‌بینی‌شده» بنویسید؛ برای ادعای عملکرد، shotgun |

## ۶. جمع‌بندی
- مسیر QIIME 2: **import → demux → DADA2 → طبقه‌بندی → درخت → تنوع → آزمون**. هر مرحله یک `.qza` با تاریخچه‌ی کامل.
- پارامترهای DADA2 از **نمودار کیفیت** و **طول آمپلیکون** می‌آیند: `trunc_f + trunc_r − ۲۵۳ ≥ ۱۲`.
- جدول `denoising-stats` را همیشه بخوانید: این‌جا افت اصلی در **ادغام** بود و دلیلش عمق کم بود، نه کیفیت.
- طبقه‌بند باید با **همان نسخه‌ی scikit-learn** و **همان ناحیه‌ی پرایمر** ساخته شده باشد. V4 را تا **جنس** گزارش کنید.
- ‏rarefy با seed، PERMANOVA همراه PERMDISP، و در داده‌ی مشاهده‌ای **مدل چندمتغیره** با هر دو ترتیب. این‌جا اثر پوشش گیاهی و ارتفاع **از هم جداشدنی نیستند**.

---

## منابع

### مقاله‌ها
- Bolyen E, et al. (2019). Reproducible, interactive, scalable and extensible microbiome data science using QIIME 2. *Nature Biotechnology* 37:852–857. https://doi.org/10.1038/s41587-019-0209-9
- Callahan BJ, et al. (2016). DADA2: High-resolution sample inference from Illumina amplicon data. *Nature Methods* 13:581–583. https://doi.org/10.1038/nmeth.3869
- Callahan BJ, McMurdie PJ, Holmes SP (2017). Exact sequence variants should replace operational taxonomic units in marker-gene data analysis. *ISME J* 11:2639–2643. https://doi.org/10.1038/ismej.2017.119
- Bokulich NA, et al. (2018). Optimizing taxonomic classification of marker-gene amplicon sequences with QIIME 2's q2-feature-classifier plugin. *Microbiome* 6:90. https://doi.org/10.1186/s40168-018-0470-z
- Quast C, et al. (2013). The SILVA ribosomal RNA gene database project. *Nucleic Acids Res* 41:D590–D596. https://doi.org/10.1093/nar/gks1219
- Robeson MS, et al. (2021). RESCRIPt: Reproducible sequence taxonomy reference database management. *PLoS Comput Biol* 17:e1009581. https://doi.org/10.1371/journal.pcbi.1009581
- Neilson JW, et al. (2017). Significant impacts of increasing aridity on the arid soil microbiome. *mSystems* 2:e00195-16. https://doi.org/10.1128/mSystems.00195-16
- Lozupone C, Knight R (2005). UniFrac: a new phylogenetic method for comparing microbial communities. *Appl Environ Microbiol* 71:8228–8235. https://doi.org/10.1128/AEM.71.12.8228-8235.2005
- Anderson MJ (2001). A new method for non-parametric multivariate analysis of variance. *Austral Ecology* 26:32–46. https://doi.org/10.1111/j.1442-9993.2001.01070.pp.x
- McMurdie PJ, Holmes S (2014). Waste not, want not: why rarefying microbiome data is inadmissible. *PLoS Comput Biol* 10:e1003531. https://doi.org/10.1371/journal.pcbi.1003531
- Gloor GB, et al. (2017). Microbiome datasets are compositional: and this is not optional. *Front Microbiol* 8:2224. https://doi.org/10.3389/fmicb.2017.02224
- Davis NM, et al. (2018). Simple statistical identification and removal of contaminant sequences in marker-gene and metagenomics data (decontam). *Microbiome* 6:226. https://doi.org/10.1186/s40168-018-0605-2

### مستندات
- مستندات آمپلیکون QIIME 2: https://amplicon-docs.qiime2.org/en/latest/
- آموزش رسمی Atacama soils (همین داده): https://docs.qiime2.org/2024.10/tutorials/atacama-soils/
- راهنمای نصب: https://library.qiime2.org/quickstart/amplicon
- انجمن پرسش و پاسخ QIIME 2: https://forum.qiime2.org

### ویدیوهای آموزشی
- QIIME 2 — *An introduction to QIIME 2*: https://www.youtube.com/watch?v=XIyZWpfcZ6U
- QIIME 2 — *Semantic types and data formats in QIIME 2*: https://www.youtube.com/watch?v=PUsvtJgpNtE
- Institute for Systems Biology — *Analyzing amplicon sequencing data with Qiime 2, Part 1*: https://www.youtube.com/watch?v=ZFiZTZXhdJ4
- Galaxy Project — *GTN Tutorial: Building an amplicon sequence variant (ASV) table from 16S data using DADA2*: https://www.youtube.com/watch?v=ISocxcJZEjw
- Brown University — *Microbiome/Metagenome Analysis Workshop: DADA2*: https://www.youtube.com/watch?v=wV5_z7rR6yw

> لینک‌ها در تاریخ 2026-10-15 بررسی شدند (`_tools/check_links.sh`).

</div>
