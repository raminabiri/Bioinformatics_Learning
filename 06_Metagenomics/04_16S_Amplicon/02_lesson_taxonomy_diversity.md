<div dir="rtl">

# درس ۲: نام‌گذاری، تنوع و یک دام آماری

**بخش:** `06_Metagenomics` · **ماژول:** `04_16S_Amplicon` · **پیش‌نیاز:** [درس ۱](01_lesson_qiime_dada2.md)؛ [تنوع آلفا و Bray–Curtis در vegan](../../04_R_Packages/03_Bioc_Examples/) · **زمان:** حدود ۷۵ دقیقه · **ابزار:** QIIME 2 amplicon 2026.7 (q2-feature-classifier با scikit-learn 1.7.1، q2-phylogeny، q2-diversity)، vsearch، MAFFT، FastTree · **خروجی‌ها از اجرای:** 2026-10-15

> ⚠️ **مرجع این درس تنها برای تمرین است:** طبقه‌بندی که تنها تا سطح **جنس** و تنها برای ناحیه‌ی V4 آموزش دیده. در پژوهش واقعی، مرجع کامل (SILVA 138.2، GTDB یا Greengenes2) که با RESCRIPt برای پرایمرهای خودتان آماده شده است.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. یک طبقه‌بند Naive Bayes سازگار با نسخه‌ی scikit-learn خودتان بسازید و ASVها را نام‌گذاری کنید.
2. برچسب‌هایی مانند `g__uncultured` را درست تفسیر کنید.
3. ژرفای rarefaction را با دلیل برگزینید و تنوع آلفا و بتا را حساب کنید.
4. یک آزمون تفاوت گروه‌ها را بخوانید (p، PERMANOVA، PERMDISP).
5. **درهم‌آمیختگی** (*confounding*) دو متغیر را در داده‌ی مشاهده‌ای بشناسید.

**پیش از آغاز:** در `~/amplicon`، با محیط QIIME 2 و متغیرهای `C` و `M` درس ۱، و خروجی‌های `rep-seqs.qza` و `table.qza` آن.

---

## ۱. داستان

درس ۱ جدولی از ۴۱۴ ASV داد: توالی‌هایی بی‌نام. اکنون سه پرسش داریم: **این‌ها چه کسانی‌اند؟** (طبقه‌بندی)، **هر نمونه چقدر گوناگون است و نمونه‌ها چقدر به هم می‌مانند؟** (تنوع)، و **آیا پوشش گیاهی جامعه را عوض می‌کند؟** (آزمون). پاسخ پرسش سوم درس اصلی این ماژول است، و آن چیزی نیست که در نگاه نخست به نظر می‌رسد.

---

## ۲. گام ۱: طبقه‌بند باید با scikit-learn شما بخواند

طبقه‌بند **Naive Bayes** در QIIME 2 یک شیء ذخیره‌شده‌ی کتابخانه‌ی پایتون scikit-learn است. یک طبقه‌بند آماده‌ی SILVA که با scikit-learn 1.4.2 ساخته شده بود، در QIIME 2 2026.7 (scikit-learn 1.7.1) این را داد:

<div dir="ltr">

```text
Plugin error from feature-classifier:
  The scikit-learn version (1.4.2) used to generate this artifact does not match the current version
  of scikit-learn installed (1.7.1). Please retrain your classifier for your current deployment to
  prevent data-corruption errors.
```

</div>

این یک **ویژگی ایمنی** است: شیء ذخیره‌شده‌ی یک نسخه، در نسخه‌ای دیگر شاید **بی‌صدا** نتیجه‌ی نادرست بدهد. دو راه: طبقه‌بند هم‌نسخه را از صفحه‌ی Data Resources همان نسخه‌ی QIIME 2 بگیرید، یا خودتان آموزش دهید:

<div dir="ltr">

```bash
bash $C/scripts/train_classifier.sh          # once: about 8 minutes, 5.5 GB of memory
```

</div>

اسکریپت دو کار می‌کند:
1. از جدول تاکسونومی SILVA سطح **گونه** را برمی‌دارد (`sed`).
2. با `qiime feature-classifier fit-classifier-naive-bayes` روی **۳۱۳٬۷۳۴** توالی SILVA 138 که **تنها به ناحیه‌ی 515F/806R بریده شده‌اند**، آموزش می‌دهد.

چرا مرجع **بریده‌شده**؟ طبقه‌بندی که روی همان ناحیه‌ی ریدهای شما آموزش ببیند، درست‌تر است (Bokulich و همکاران، ۲۰۱۸). چرا تنها تا **جنس**؟

| سطح برچسب | شمار رده | حافظه | زمان |
| :--- | ---: | ---: | ---: |
| گونه | 67,689 | بیش از ۱۲ گیگابایت (ایستاد) | — |
| **جنس** | **8,415** | ۵٫۵ گیگابایت | ۸ دقیقه |

حافظه‌ی Naive Bayes کمابیش با «شمار رده × شمار ویژگی» بالا می‌رود. برداشتن سطح گونه منطقی است: یک قطعه‌ی ۲۵۰ بازی V4 به‌ندرت گونه را با اطمینان می‌شناسد.

---

## ۳. گام ۲: نام‌گذاری ASVها

<div dir="ltr">

```bash
qiime feature-classifier classify-sklearn --i-classifier data/db/silva-138-99-515-806-genus-nb.qza \
  --i-reads rep-seqs.qza --p-n-jobs 1 --o-classification taxonomy.qza
qiime taxa barplot --i-table table.qza --i-taxonomy taxonomy.qza --m-metadata-file $M \
  --o-visualization taxa-bar-plots.qzv
```

</div>

| بخش | چیست |
| :--- | :--- |
| ① `--i-classifier` | طبقه‌بند گام ۱ |
| ② `--i-reads rep-seqs.qza` | توالی ASVها (درس ۱) |
| ③ `--p-n-jobs 1` | یک فرایند؛ هر فرایند یک نسخه از طبقه‌بند را در حافظه می‌گذارد |
| ④ `taxa barplot` | نمودار ستونی تعاملی ترکیب هر نمونه |

برای هر ASV یک رشته‌ی تاکسونومی و یک **Confidence** بیرون می‌آید. طبقه‌بند تا ژرف‌ترین سطحی می‌رود که اطمینانش از **۰٫۷** (پیش‌فرض `--p-confidence`) بیشتر باشد:

| ژرف‌ترین سطح | شمار ASV |
| :--- | ---: |
| جنس | **368** (۸۹٪) |
| خانواده | 32 |
| راسته / رده / شاخه | 5 / 5 / 1 |
| تنها «Bacteria» | 3 |

شاخه‌های پرشمار (شمار ASV): **Actinobacteriota ۱۷۰**، Proteobacteria ۶۵، Chloroflexi ۳۹، Acidobacteriota ۲۸، Gemmatimonadota ۲۵. چیرگی اکتینوباکتری‌ها با خاک‌های خشک و پرتابش سازگار است. **۱۳ ASV آرکی** هم هست: «16S» نام ژن است، نه «باکتری»؛ 515F/806R آرکی‌ها را هم تکثیر می‌کند.

### دامِ `g__uncultured`

پرشمارترین برچسب‌های جنس (درصد از همه‌ی ریدها):

| برچسب | ٪ | یادداشت |
| :--- | ---: | :--- |
| `g__wb1-P19` | 16.9 | نام موقت SILVA (Nitrosococcaceae)، بی نماینده‌ی کشت‌شده |
| `g__uncultured` | 15.6 | **جنس نیست**: برچسب جای‌خالی در ۲۰ دودمان گوناگون |
| `g__67-14` | 8.5 | نام موقت |
| `g__Rubrobacter` | 5.9 | جنس واقعی؛ مقاوم به خشکی و پرتو |
| `g__Crossiella` | 4.3 | اکتینوباکتری |

این جدول **خودش نمونه‌ی دام است**: ریدها را تنها با **نام جنس** جمع زدیم، و `g__uncultured` از ۲۰ دودمان (برای نمونه Pirellulaceae، Gemmataceae و یک خانواده‌ی بی‌نام در Burkholderiales) در **یک سطر** آمد: یک «جنس» ساختگی ۱۵٫۶ درصدی. `qiime taxa collapse --p-level 6` این اشتباه را نمی‌کند، چون شناسه‌ی هر سطر کل دودمان است. ولی وقتی جدول را در pandas یا R تنها با ستون «genus» گروه می‌کنید، خودتان باید مراقب باشید (تمرین ۴).

### روش دوم: vsearch

<div dir="ltr">

```bash
qiime feature-classifier classify-consensus-vsearch --i-query rep-seqs.qza \
  --i-reference-reads data/db/silva-138-99-seqs-515-806.qza \
  --i-reference-taxonomy data/db/silva-138-99-tax-515-806.qza \
  --p-threads 4 --o-classification taxonomy-vsearch.qza --o-search-results vsearch-hits.qza
```

</div>

این روش آموزش نمی‌خواهد (۱۳ ثانیه): برای هر ASV نزدیک‌ترین توالی‌های مرجع را می‌یابد و تاکسونومی **هم‌رأی** آن‌ها را برمی‌گرداند. همخوانی دو روش: **شاخه** ۴۱۰ از ۴۱۴ (۹۹٪)؛ **جنس** ۳۱۶ از ۳۴۰ ASVی که هر دو تا جنس رفتند (۹۳٪). در سطح بالا هر دو یک داستان می‌گویند؛ در سطح جنس کمابیش ۷٪ ناهمخوانی، که برای جمله‌ای مانند «جنس X در گروه A بیشتر بود» مهم است.

---

## ۴. گام ۳: درخت و ژرفای rarefaction

### ۴.۱ درخت

<div dir="ltr">

```bash
qiime phylogeny align-to-tree-mafft-fasttree --i-sequences rep-seqs.qza --p-n-threads 4 \
  --o-alignment aligned-rep-seqs.qza --o-masked-alignment masked-aligned-rep-seqs.qza \
  --o-tree unrooted-tree.qza --o-rooted-tree rooted-tree.qza
```

</div>

‏MAFFT ASVها را هم‌تراز می‌کند و FastTree از آن درخت می‌سازد؛ ریشه در میانه‌ی درازترین شاخه گذاشته می‌شود. درخت برای سنجه‌های **تبارزایشی** (Faith PD، UniFrac) لازم است. از ۲۲۷ باز ساخته شده: برای **فاصله‌ی تقریبی** بس است، ولی نه برای ادعای روابط تکاملی.

### ۴.۲ چرا rarefaction؟

جدول ASV **شمار مطلق** باکتری‌ها نیست: ژرفای هر نمونه تصادفی است و تنها **نسبت‌ها** معنی دارند (داده‌ی *ترکیبی*). نمونه‌ای با ۵۰۰ رید، تنها به‌خاطر ژرفا ASVهای بیشتری از نمونه‌ای با ۱۰۰ رید نشان می‌دهد. **rarefaction** از هر نمونه، به‌تصادف، به یک شمار برابر رید زیرنمونه می‌گیرد.

شمار رید هر نمونه پس از DADA2 (از کم به زیاد):

<div dir="ltr">

```text
0 (15 samples), 1, 1, 1, 26, 47, 51, 90, 124, 126, 140, 159, … , 583, 584, 586
```

</div>

| ژرفا | نمونه‌های مانده (از ۷۱) |
| ---: | ---: |
| 100 | 49 |
| **150** | **46** |
| 200 | 39 |
| 300 | 28 |

ژرفای بیشتر = تنوع درست‌تر در هر نمونه، ولی نمونه‌ی کمتر. **۱۵۰** را برگزیدیم؛ نمونه‌های زیر ۱۵۰ رید کنار می‌روند. (تمرین ۵ اثر این انتخاب را می‌سنجد.)

---

## ۵. گام ۴: تنوع

<div dir="ltr">

```bash
export UNIFRAC_USE_GPU=N
qiime diversity core-metrics-phylogenetic --i-phylogeny rooted-tree.qza --i-table table.qza \
  --p-sampling-depth 150 --p-random-seed 42 --m-metadata-file $M --output-dir core-metrics-results
```

</div>

| بخش | چیست | بی آن چه می‌شود |
| :--- | :--- | :--- |
| ① `--p-sampling-depth 150` | ژرفای rarefaction | — (اجباری) |
| ② `--p-random-seed 42` | دانه‌ی ثابت برای زیرنمونه‌گیری تصادفی | هر اجرا عددهای کمی دیگر می‌دهد |
| ③ `--output-dir` | همه‌ی خروجی‌ها در یک پوشه | — |
| ④ `UNIFRAC_USE_GPU=N` | ‏UniFrac را روی CPU حساب کن | در برخی نصب‌ها، برنامه‌ی UniFrac برای GPU ساخته شده و روی کامپیوتر بی GPU با `Accelerator Fatal Error` می‌ایستد |

خروجی: چهار سنجه‌ی **آلفا** (درون هر نمونه)، چهار ماتریس فاصله‌ی **بتا** (میان نمونه‌ها)، و برای هر ماتریس یک PCoA و نمودار تعاملی Emperor.

| سنجه‌ی بتا | چه می‌سنجد |
| :--- | :--- |
| Jaccard | بود و نبود، بی درخت |
| Bray–Curtis | فراوانی، بی درخت (همان بخش ۰۴) |
| ‏UniFrac بی‌وزن | بود و نبود + فاصله‌ی تبارزایشی؛ حساس به تاکسون‌های **کمیاب** |
| ‏UniFrac وزن‌دار | فراوانی + فاصله‌ی تبارزایشی؛ زیر اثر تاکسون‌های **چیره** |

---

## ۶. گام ۵: آیا گروه‌ها فرق دارند؟

### ۶.۱ مفهوم: p و آزمون جایگشت

‏**‏p** پاسخ این پرسش است: «اگر گروه‌ها **واقعاً** فرقی نداشتند، چقدر احتمال داشت تفاوتی به این بزرگی تنها از بخت ببینیم؟» p کوچک (برای نمونه زیر ۰٫۰۵) یعنی «بخت، توضیح خوبی نیست».

**آزمون جایگشت** (*permutation*) این احتمال را با شبیه‌سازی می‌سنجد: برچسب گروه‌ها را ۹۹۹ بار **به‌تصادف جابه‌جا** می‌کند و هر بار تفاوت را دوباره حساب می‌کند. اگر تفاوت واقعی از کمابیش همه‌ی تفاوت‌های جابه‌جاشده بزرگ‌تر باشد، p کوچک است. با ۹۹۹ جایگشت، کوچک‌ترین p شدنی **0.001** است.

### ۶.۲ آلفا: آزمون Kruskal–Wallis

<div dir="ltr">

```bash
qiime diversity alpha-group-significance --i-alpha-diversity core-metrics-results/faith_pd_vector.qza \
  --m-metadata-file $M --o-visualization core-metrics-results/faith_pd-group-significance.qzv
```

</div>

‏Kruskal–Wallis گروه‌ها را با **رتبه**ی مقدارها می‌سنجد، نه خود مقدارها؛ پس به چند نمونه‌ی بسیار دور حساس نیست. نتیجه (۴۶ نمونه):

| سنجه | ‏vegetation (۱۵ بی / ۳۱ با گیاه) | transect (۲۰ / ۲۶) |
| :--- | :--- | :--- |
| Faith PD | H = 5.01، **p = 0.025** | H = 0.20، p = 0.66 |
| Shannon | H = 4.40، **p = 0.036** | H = 1.08، p = 0.30 |
| Observed features | H = 2.29، p = 0.13 | H = 0.01، p = 0.93 |

همبستگی Spearman (`qiime diversity alpha-correlation`)، Faith PD با **ارتفاع**: ρ = 0.388، **p = 0.0077**.

### ۶.۳ بتا: PERMANOVA

<div dir="ltr">

```bash
qiime diversity beta-group-significance \
  --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
  --m-metadata-file $M --m-metadata-column vegetation --p-pairwise \
  --o-visualization core-metrics-results/unweighted-unifrac-vegetation-significance.qzv
```

</div>

‏PERMANOVA می‌پرسد: «فاصله‌ی میان گروه‌ها از فاصله‌ی درون گروه‌ها بیشتر است؟» (آماره‌ی pseudo-F)، با p از جایگشت.

| فاصله | vegetation | transect |
| :--- | :--- | :--- |
| ‏UniFrac بی‌وزن | pseudo-F = 3.77، **p = 0.001** | pseudo-F = 1.57، p = 0.058 |
| Bray–Curtis | pseudo-F = 2.36، **p = 0.001** | pseudo-F = 1.76، **p = 0.001** |

‏QIIME 2 برای جایگشت PERMANOVA دانه نمی‌گیرد؛ p شما شاید کمی فرق کند (برای نمونه 0.058 در برابر 0.062).

### ‏۶.۴ PERMDISP: «مرکز» یا «پراکندگی»؟

‏PERMANOVA به تفاوت **پراکندگی** هم حساس است: اگر یک گروه تنها **پراکنده‌تر** باشد، شاید PERMANOVA هم معنی‌دار شود (Anderson، ۲۰۰۱). PERMDISP این را جدا می‌کند:

<div dir="ltr">

```bash
qiime diversity beta-group-significance \
  --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
  --m-metadata-file $M --m-metadata-column vegetation --p-method permdisp \
  --o-visualization core-metrics-results/unweighted-unifrac-vegetation-permdisp.qzv
```

</div>

<div dir="ltr">

```text
PERMDISP  F = 0.042  p = 0.842
```

</div>

پراکندگی دو گروه فرقی ندارد؛ پس PERMANOVA واقعاً تفاوت **ترکیب** را نشان می‌دهد.

---

## ۷. گام ۶: درهم‌آمیختگی، مهم‌ترین نکته‌ی این ماژول

تا این‌جا نتیجه‌ی وسوسه‌انگیز: «پوشش گیاهی ترکیب و تنوع میکروبی خاک را عوض می‌کند.» اکنون جدول نمونه‌ها را ببینید: کمترین و بیشترین ارتفاع (ستون ۳) در هر گروه پوشش گیاهی (ستون ۲۰؛ درس ۱، بخش ۲.۴). تمرین ۵ این جدول را با awk می‌سازد:

| vegetation | بازه‌ی ارتفاع سایت‌ها (متر) |
| :--- | :--- |
| `no` | ۸۹۵ تا ۳٬۱۸۴ |
| `yes` | ۲٬۶۸۷ تا ۴٬۶۹۷ |

**همه‌ی سایت‌های گیاه‌دار در ارتفاع ۲٬۶۸۷ متر یا بالاترند.** دو گروه تنها در بازه‌ی باریک ۲٬۶۸۷ تا ۳٬۱۸۴ متر با هم‌اند. ارتفاع با رطوبت و دما هم همراه است. پس «اثر گیاه» و «اثر ارتفاع» از هم جدا نیستند: این همان **درهم‌آمیختگی** است.

### مدل چندمتغیره: `adonis`

<div dir="ltr">

```bash
qiime diversity adonis --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
  --m-metadata-file $M --p-formula "elevation+vegetation" \
  --o-visualization core-metrics-results/unweighted-unifrac-adonis.qzv
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

وقتی ارتفاع **نخست** در مدل می‌آید، پوشش گیاهی **دیگر معنی‌دار نیست** (p = 0.092). `adonis` در QIIME 2 جمع مربع‌های **ترتیبی** حساب می‌کند: `vegetation` تنها با تغییراتی سنجیده می‌شود که ارتفاع توضیح نداده است.

ترتیب را وارونه کنید (`--p-formula "vegetation+elevation"`):

<div dir="ltr">

```text
            Df  SumOfSqs     R2      F  Pr(>F)
vegetation   1    0.873  0.079  3.773   0.001
elevation    1    0.238  0.021  1.027   0.385
```

</div>

این بار **ارتفاع** پس از پوشش گیاهی معنی‌دار نیست. هر متغیری که نخست بیاید، **سهم مشترک** دو متغیر را برمی‌دارد؛ سهم ویژه‌ی هیچ‌کدام به‌تنهایی معنی‌دار نیست. پس با این داده **نمی‌توان گفت** اثر از ارتفاع است یا از گیاه؛ تنها: ترکیب میکروبی با «ارتفاع/پوشش گیاهی» همراه است.

و یک نکته‌ی دیگر: **R² = 0.07**. ارتفاع تنها ۷٪ تغییرات UniFrac را توضیح می‌دهد و ۹۰٪ «باقی‌مانده» است. «معنی‌دار» با «مهم» یکی نیست.

**درس:** در پژوهش **مشاهده‌ای** (نه آزمایشی)، متغیرها با هم همبسته‌اند. پیش از نسبت دادن اثر به یک متغیر، جدول دو متغیر را ببینید و مدل چندمتغیره بسازید، با هر دو ترتیب. این درهم‌آمیختگی را تنها **طراحی نمونه‌برداری** حل می‌کند: سایت‌های با و بی گیاه در **همان** ارتفاع (تمرین ۶).

---

## ۸. سه اشتباه رایج

**۱. طبقه‌بند با نسخه‌ی دیگر scikit-learn.** خطا (یا در نسخه‌های قدیمی‌تر، نتیجه‌ی نادرست بی‌صدا). طبقه‌بند هم‌نسخه، یا آموزش دوباره (گام ۱).

**۲. گروه کردن تنها با نام جنس.** `g__uncultured` از ۲۰ دودمان یک «جنس» ۱۵٫۶ درصدی می‌سازد. با کل دودمان گروه کنید (`taxa collapse`)، یا برچسب را همراه سطح بالاتر بنویسید.

**۳. یک متغیر در داده‌ی مشاهده‌ای.** «پوشش گیاهی معنی‌دار بود» بی دیدن ارتفاع. جدول دو متغیر + `adonis` با چند متغیر و هر دو ترتیب.

---

## 📘 برای کنجکاوها

- ‏**‏rarefaction یا نه؟** McMurdie و Holmes (۲۰۱۴) نشان دادند برای آزمون فراوانی تک‌تک تاکسون‌ها، rarefaction داده را هدر می‌دهد؛ روش‌هایی مانند ANCOM-BC2 و ALDEx2 (بر پایه‌ی لگاریتم نسبت‌ها) برای آن‌اند. برای سنجه‌های آلفا و بتا، rarefaction هنوز رایج و پذیرفتنی است (Weiss و همکاران، ۲۰۱۷).
- **کنترل منفی و `decontam`:** در نمونه‌های کم‌زیست‌توده (همین خاک بیابان)، DNA آلوده‌ی کیت‌ها می‌تواند بخش بزرگی از ریدها باشد؛ کنترل منفی در همان ران و بسته‌ی `decontam` آن را پیدا می‌کند (تمرین ۶).
- ‏**‏PICRUSt2:** کارکرد را از روی 16S **پیش‌بینی** می‌کند؛ همیشه «پیش‌بینی‌شده» بنویسید.

---

## جمع‌بندی

- طبقه‌بند باید با **همان نسخه‌ی scikit-learn** و **همان ناحیه‌ی پرایمر** ساخته شده باشد. V4 را تا **جنس** گزارش کنید.
- ‏`g__uncultured` جنس نیست؛ با کل دودمان گروه کنید.
- ‏rarefaction با دانه‌ی ثابت؛ ژرفا و شمار نمونه‌های کنارگذاشته را گزارش کنید.
- ‏PERMANOVA همراه PERMDISP؛ در داده‌ی مشاهده‌ای، **مدل چندمتغیره با هر دو ترتیب**. این‌جا اثر پوشش گیاهی و ارتفاع **جداشدنی نیست**.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
qiime feature-classifier classify-sklearn --i-classifier CLASSIFIER.qza --i-reads rep-seqs.qza --o-classification taxonomy.qza
qiime taxa barplot --i-table table.qza --i-taxonomy taxonomy.qza --m-metadata-file $M --o-visualization taxa-bar-plots.qzv
qiime phylogeny align-to-tree-mafft-fasttree --i-sequences rep-seqs.qza --o-alignment a.qza \
  --o-masked-alignment ma.qza --o-tree t.qza --o-rooted-tree rooted-tree.qza
qiime diversity core-metrics-phylogenetic --i-phylogeny rooted-tree.qza --i-table table.qza \
  --p-sampling-depth 150 --p-random-seed 42 --m-metadata-file $M --output-dir core-metrics-results
qiime diversity alpha-group-significance --i-alpha-diversity …/faith_pd_vector.qza --m-metadata-file $M --o-visualization x.qzv
qiime diversity beta-group-significance --i-distance-matrix …/unweighted_unifrac_distance_matrix.qza \
  --m-metadata-file $M --m-metadata-column vegetation [--p-method permdisp] --o-visualization y.qzv
qiime diversity adonis --i-distance-matrix … --m-metadata-file $M --p-formula "elevation+vegetation" --o-visualization z.qzv
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| ‏Naive Bayes | روش آماری طبقه‌بندی بر پایه‌ی بسامد k-merها در هر تاکسون |
| تنوع آلفا / بتا | گوناگونی درون یک نمونه / فاصله‌ی میان نمونه‌ها |
| ‏UniFrac | فاصله‌ای که درخت تبارزایشی را هم به حساب می‌آورد |
| ‏rarefaction | زیرنمونه‌گیری تصادفی همه‌ی نمونه‌ها به یک ژرفای برابر |
| ‏p-value | احتمال دیدن تفاوتی به این بزرگی، اگر واقعاً تفاوتی نبود |
| آزمون جایگشت | سنجیدن p با جابه‌جا کردن تصادفی برچسب‌ها |
| ‏PERMANOVA / PERMDISP | آزمون تفاوت مرکز / پراکندگی گروه‌ها روی ماتریس فاصله |
| درهم‌آمیختگی (*confounding*) | همراه بودن دو متغیر، چنان که اثرشان جداشدنی نیست |

---

## منابع

**مستند و مقاله**
- Bokulich NA, et al. (2018). *Optimizing taxonomic classification of marker-gene amplicon sequences with QIIME 2's q2-feature-classifier plugin.* Microbiome 6:90. https://doi.org/10.1186/s40168-018-0470-z
- Quast C, et al. (2013). *The SILVA ribosomal RNA gene database project.* Nucleic Acids Res 41:D590–D596. https://doi.org/10.1093/nar/gks1219
- Robeson MS, et al. (2021). *RESCRIPt: Reproducible sequence taxonomy reference database management.* PLoS Comput Biol 17:e1009581. https://doi.org/10.1371/journal.pcbi.1009581
- Lozupone C, Knight R (2005). *UniFrac: a new phylogenetic method for comparing microbial communities.* Appl Environ Microbiol 71:8228–8235. https://doi.org/10.1128/AEM.71.12.8228-8235.2005
- Anderson MJ (2001). *A new method for non-parametric multivariate analysis of variance.* Austral Ecology 26:32–46. https://doi.org/10.1111/j.1442-9993.2001.01070.pp.x
- McMurdie PJ, Holmes S (2014). *Waste not, want not: why rarefying microbiome data is inadmissible.* PLoS Comput Biol 10:e1003531. https://doi.org/10.1371/journal.pcbi.1003531
- Gloor GB, et al. (2017). *Microbiome datasets are compositional: and this is not optional.* Front Microbiol 8:2224. https://doi.org/10.3389/fmicb.2017.02224
- QIIME 2 forum: https://forum.qiime2.org

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins University). دوره‌ای ویژه‌ی تحلیل میکروبیوم در Coursera نیافتیم؛ نزدیک‌ترین: https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Linux* (The Linux Foundation). دوره‌ای ویژه در edX نیافتیم؛ نزدیک‌ترین: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux
- YouTube: *Analyzing amplicon sequencing data with Qiime 2, Part 1* (Institute for Systems Biology): https://www.youtube.com/watch?v=ZFiZTZXhdJ4
- YouTube: *Microbiome/Metagenome Analysis Workshop: DADA2* (Brown University): https://www.youtube.com/watch?v=wV5_z7rR6yw

<sub>نشانی‌های YouTube و DOIها در 2026-10-15 وارسی شدند؛ نشانی‌های Coursera و edX در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
