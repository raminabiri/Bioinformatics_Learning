# پاسخ تشریحی: تحلیل آمپلیکون 16S با QIIME 2

> اجرا شده در 2026-10-14 و 2026-10-15 با QIIME 2 2026.7 (scikit-learn 1.7.1) و vsearch روی سرور دوره. اعداد demux، DADA2 و طبقه‌بندی برای شما هم دقیقاً همین‌اند. اعداد تنوع با `--p-random-seed 42` همین‌اند. p-valueهای PERMANOVA و adonis از جایگشت تصادفی می‌آیند (بدون seed در QIIME 2) و ممکن است کمی فرق کنند.

```bash
cd 03_Metagenomics/work/04_16s
export PATH=/data/MicrobiomePipeline/qiime2_env/bin:$PATH UNIFRAC_USE_GPU=N
M=../../04_16S_Amplicon/data/sample_metadata.tsv
```

---

## تمرین ۱: کجا رفتند ریدها؟

### ۱.۱ بدون `--p-rev-comp-mapping-barcodes`
```bash
qiime demux emp-paired --i-seqs emp-paired-end-sequences.qza \
  --m-barcodes-file $M --m-barcodes-column barcode-sequence \
  --o-per-sample-sequences demux_norc.qza --o-error-correction-details dd_norc.qza
```
```text
No sequences were mapped to samples. Check that your barcodes are in the correct orientation
(see the rev_comp_barcodes and/or rev_comp_mapping_barcodes options).
```
**صفر رید.** وقتی هیچ نمونه‌ای حتی یک رید نمی‌گیرد، مشکل تصادفی نیست، **جهت** است. در این پروتکل، بارکد در کتابخانه طوری قرار گرفته که رید `barcodes` آن را به شکل **مکمل معکوس** آنچه در فایل metadata نوشته شده می‌خواند. دو گزینه‌ی QIIME 2 برای دو حالت ممکن‌اند:
- `--p-rev-comp-mapping-barcodes`: بارکدهای **metadata** را برعکس کن.
- `--p-rev-comp-barcodes`: بارکدهای خوانده‌شده در **رید** را برعکس کن.

از نظر ریاضی هر دو یک مقایسه را انجام می‌دهند. ولی تصحیح خطای Golay روی رید انجام می‌شود، پس باید گزینه‌ای را انتخاب کنید که با پروتکل مرکز توالی‌یابی می‌خواند. در عمل از مرکز بپرسید یا هر دو را امتحان کنید و ببینید کدام ریدها را به نمونه‌ها می‌رساند.

### ۱.۲ چهار گروه
```bash
qiime tools export --input-path demux-details.qza --output-path dd
awk -F'\t' 'NR>1{a=($2=="None")?"unassigned":"assigned"; e=($6==0)?"no_error":"error"; print a"\t"e}' dd/details.tsv | sort | uniq -c
```
| | جفت رید | ٪ |
| :--- | ---: | ---: |
| به نمونه رسید، بدون خطا | 42,332 | ۳۱٫۲ |
| به نمونه رسید، خطا تصحیح شد (۱ تا ۳ باز) | 4,380 | ۳٫۲ |
| **بدون نمونه، بارکد بی‌خطا** | **60,234** | **۴۴٫۵** |
| بدون نمونه، با خطا (تا ۴ خطا، بیشترش `NNNNNNNNNNNN`) | 28,541 | ۲۱٫۱ |
| جمع | 135,487 | ۱۰۰ |

۴٬۳۸۰ رید فقط به لطف **تصحیح خطای Golay** نجات یافتند. بارکدهای Golay ۱۲ بازی طوری طراحی شده‌اند که فاصله‌ی همینگ بین هر دو بارکد زیاد است. پس یک بارکد با چند خطا هنوز به یک بارکد معتبر نزدیک‌تر است تا به بقیه.

### ۱.۳ بارکدهای بی‌صاحب
```bash
awk -F'\t' 'NR>1 && $2=="None" && $6==0' dd/details.tsv | cut -f4 | sort | uniq -c | sort -nr | head -3
```
```text
   1907 CCGTAAGACCAG
   1762 TGGTACAGTACC
   1745 GGTTACGGTGGT
```
هر کدام نزدیک به ۲٬۰۰۰ رید دارند، یعنی **در حد یک نمونه‌ی کامل** (پرریدترین نمونه‌ی ما ۱٬۴۴۲ رید دارد). بارکد بی‌خطا و با فراوانی بالا یعنی یک نمونه‌ی واقعی، ولی نمونه‌ی **یک مطالعه‌ی دیگر** که در همان ران MiSeq بوده است. پروژه‌های EMP معمولاً چند مطالعه را در یک ران چندگانه می‌کنند. اگر ریدهای بی‌صاحب کیفیت بد داشتند، بارکدشان پراکنده و پرخطا بود، نه چند بارکد تمیز با هزاران رید.

### ۱.۴ نمونه‌های بدون رید
```bash
awk -F'\t' 'NR>2{print $1}' $M | sort > meta_ids
qiime tools export --input-path demux.qzv --output-path demux_export
awk -F'\t' 'NR>1{print $1}' demux_export/per-sample-fastq-counts.tsv | sort | comm -23 meta_ids -
```
```text
BAQ1370.1.2
YUN1005.2
YUN3008.2
YUN3184.1
```
در این زیرنمونه‌ی ۱٪، صفر رید فقط یعنی «شانس نیاورد» (این نمونه‌ها در داده‌ی کامل هم کم‌رید بوده‌اند). اگر این‌ها **کنترل منفی** بودند، صفر رید خبر خوبی بود ولی کافی نیست: کنترل منفی‌ای که در داده‌ی کامل صفر رید دارد، ممکن است فقط زیر عمق کتابخانه رفته باشد. چیزی که اهمیت دارد، **ترکیب** ریدهای کنترل منفی در مقایسه با نمونه‌هاست (تمرین ۶).

---

## تمرین ۲: همپوشانی و طول آمپلیکون

### ۲.۱ ادغام با vsearch
```bash
qiime tools export --input-path demux.qza --output-path demux_fq
cat demux_fq/*_R1_001.fastq.gz > all_R1.fq.gz ; cat demux_fq/*_R2_001.fastq.gz > all_R2.fq.gz
vsearch --fastq_mergepairs all_R1.fq.gz --reverse all_R2.fq.gz --fastqout merged.fq --threads 4
```
```text
     46712  Pairs
     42961  Merged (92.0%)
      3751  Not merged (8.0%)
    253.20  Mean fragment length
      0.56  Mean observed errors in merged region of forward sequences
      1.27  Mean observed errors in merged region of reverse sequences
```
```bash
awk 'NR%4==2{print length($0)}' merged.fq | sort -n | uniq -c | sort -nr | head -3
```
```text
  38516 253
   3091 254
    829 252
```
طول قطعه **۲۵۳ باز** است. نکته‌ی مهم دیگر: ریدهای reverse **بیش از دو برابر** forward خطا دارند (۱٫۲۷ در برابر ۰٫۵۶ خطا در ناحیه‌ی همپوشانی). این در تمرین ۳ مهم می‌شود.

### ۲.۲ پیش‌بینی همپوشانی
همپوشانی = `f + r − 253`. اگر `trunc-len` صفر باشد، رید کامل ۱۵۱ بازی می‌ماند.

| trunc (f, r) | همپوشانی | پیش‌بینی (حداقل ۱۲) | نتیجه‌ی واقعی |
| :--- | ---: | :--- | :--- |
| 150, 150 | 47 | ✅ | 16,438 رید merged |
| 150, 130 | 27 | ✅ | 19,672 |
| 130, 120 | −3 | ❌ | — |
| 120, 120 | −13 | ❌ | `No features remain after denoising` |
| 0, 0 (151, 151) | 49 | ✅ | 16,015 |

در عمل یک **حاشیه‌ی اطمینان** هم لازم است، چون طول قطعه بین تاکسون‌ها فرق می‌کند (۲.۴). قطعه‌ی ۲۵۵ بازی با `trunc` (150, 130) فقط ۲۵ باز همپوشانی دارد.

### ۲.۳ آزمون (120, 120)
```bash
qiime dada2 denoise-paired --i-demultiplexed-seqs demux.qza --p-trim-left-f 13 --p-trim-left-r 13 \
  --p-trunc-len-f 120 --p-trunc-len-r 120 --o-table t120.qza --o-representative-sequences r120.qza \
  --o-denoising-stats s120.qza --o-base-transition-stats b120.qza
```
```text
No features remain after denoising. Try adjusting your truncation and trim parameter settings.
```
پیش‌بینی درست بود. پیام خطا گمراه‌کننده است: می‌گوید «بعد از denoise»، ولی denoise درست انجام شده و **ادغام** شکست خورده است.

### ۲.۴ طول ASVها
```bash
qiime tools export --input-path rep-seqs.qza --output-path rs
awk '!/^>/{print length($0)}' rs/dna-sequences.fasta | sort -n | uniq -c | sort -nr | head -3
```
```text
    372 227
     26 228
      9 226
```
۲۵۳ − ۱۳ (`trim-left-f`) − ۱۳ (`trim-left-r`) = **۲۲۷**. هفت ASV طول غیرعادی دارند. طبقه‌بندی آن‌ها:

| طول | تعداد رید | طبقه‌بندی |
| ---: | ---: | :--- |
| 255 | 7 | Gemmatimonadaceae; *Roseisolibacter* |
| 250 | 9 | Gemmatimonadaceae; *Roseisolibacter* |
| 248 | 11 | Gemmatimonadaceae; *Roseisolibacter* |
| 247 | 3 | Gemmatimonadaceae; uncultured |
| 242 | 5 | S0134 terrestrial group |
| 230 | 6 | Longimicrobiaceae |
| 229 | 14 | Longimicrobiaceae |

**همه** از شاخه‌ی **Gemmatimonadota** هستند (S0134 و Longimicrobiaceae هم جزو همین شاخه‌اند). این نشان می‌دهد طول متفاوت یک ویژگی زیستی است: این گروه **درج (insertion)** در ناحیه‌ی V4 دارد. پس ASVهای بلند **خطای فنی نیستند** و نباید با فیلتر طول (مثلاً «فقط ۲۲۵ تا ۲۳۰») حذف شوند. چنین فیلتری یک شاخه‌ی کامل را از داده پاک می‌کرد. اگر ASV بلند به میتوکندری، کلروپلاست یا «Unassigned» طبقه‌بندی می‌شد، داستان فرق می‌کرد (آمپلیکون غیرهدف).

---

## تمرین ۳: پارامترهای DADA2

```bash
run(){ name=$1; shift
  qiime dada2 denoise-paired --i-demultiplexed-seqs demux.qza --p-trim-left-f 13 --p-trim-left-r 13 \
    --p-n-threads 4 "$@" --o-table v_$name.table.qza --o-representative-sequences v_$name.rep.qza \
    --o-denoising-stats v_$name.stats.qza --o-base-transition-stats v_$name.bts.qza; }
run base       --p-trunc-len-f 150 --p-trunc-len-r 150
run mm2        --p-trunc-len-f 150 --p-trunc-len-r 150 --p-max-merge-mismatch 2
run pseudo     --p-trunc-len-f 150 --p-trunc-len-r 150 --p-pooling-method pseudo
run pseudo_mm2 --p-trunc-len-f 150 --p-trunc-len-r 150 --p-pooling-method pseudo --p-max-merge-mismatch 2
run r130       --p-trunc-len-f 150 --p-trunc-len-r 130
run t0         --p-trunc-len-f 0   --p-trunc-len-r 0
```
(جمع ستون‌ها از `denoising-stats` export‌شده؛ ورودی همه ۴۶٬۷۱۲.)

| تنظیم | filtered | denoised | merged | non-chimeric | ASV |
| :--- | ---: | ---: | ---: | ---: | ---: |
| base | 41,834 | 33,558 | 16,438 | 16,438 | 414 |
| mm2 | 41,834 | 33,558 | 19,871 | 19,693 | 531 |
| pseudo | 41,834 | 35,494 | 18,872 | 18,808 | 466 |
| pseudo_mm2 | 41,834 | 35,494 | **23,276** | **22,716** | **739** |
| r130 | 43,432 | 34,879 | 19,672 | 19,518 | 509 |
| t0 | 41,717 | 33,249 | 16,015 | 16,015 | 386 |

### ۳.۱
بیشترین رید و بیشترین ASV هر دو مال **pseudo_mm2** است (۲۲٬۷۱۶ رید، ۷۳۹ ASV). یعنی هر تنظیمی که رید بیشتری نگه داشت، ASV بیشتری هم ساخت. این **دو طرف یک بده‌بستان** است.

### ۳.۲ چرا `max-merge-mismatch` تعداد ASV را بالا می‌برد؟
در حالت پیش‌فرض (۰)، جفتی که در ناحیه‌ی همپوشانی حتی یک اختلاف دارد دور ریخته می‌شود. این اختلاف معمولاً از **خطای تصحیح‌نشده‌ی رید reverse** است (تمرین ۲.۱: خطای reverse دو برابر است). با اجازه‌ی ۲ اختلاف، این جفت‌ها ادغام می‌شوند. ولی توالی ادغام‌شده خطا را با خود می‌آورد و یک **ASV جدید و کاذب** می‌سازد که یک یا دو باز با ASV واقعی فرق دارد. به همین دلیل همراه با mm2، تعداد chimera هم از صفر به ۱۷۸ رسید (۱۹٬۸۷۱ − ۱۹٬۶۹۳). یعنی دنباله‌های عجیب‌تری وارد داده شدند.

### ۳.۳ pseudo-pooling
در حالت `independent`، DADA2 هر نمونه را جدا denoise می‌کند. توالی‌ای که در هر نمونه فقط ۱ یا ۲ بار دیده شده، از نظر آماری از خطا قابل تشخیص نیست و دور ریخته می‌شود. در `pseudo`، DADA2 دو دور اجرا می‌شود. ASVهایی که در دور اول در **حداقل دو نمونه** پیدا شدند، در دور دوم به‌عنوان «احتمال پیشین» به همه‌ی نمونه‌ها داده می‌شوند. پس یک تاکسون نادر که در چند نمونه هست، در هر نمونه هم شناخته می‌شود. در داده‌ی کم‌عمق (چندصد رید)، تقریباً همه چیز «نادر» است، برای همین pseudo-pooling رید denoised را از ۳۳٬۵۵۸ به ۳۵٬۴۹۴ برد. هزینه‌اش زمان دو برابر است. pooling کامل (`pool=TRUE` در R) در QIIME 2 موجود نیست.

### ۳.۴ انتخاب برای مقاله
پاسخ «درست» یکتا وجود ندارد. آنچه مهم است توجیه و گزارش است:
- **محافظه‌کار:** `base` (یا `r130` که رید reverse کم‌کیفیت را زودتر می‌بُرد و هنوز ۲۷ باز همپوشانی دارد). رید کمتر، ولی ASVها مطمئن‌ترند.
- **حساس:** `pseudo` بدون mm2. pooling منطقاً درست‌تر است، ولی mm2 خطا وارد می‌کند.
- برای این داده‌ی کم‌عمق، بهترین راه **تغییر پارامتر نیست، توالی‌یابی عمیق‌تر است**.

در روش‌ها گزارش کنید: نسخه‌ی QIIME 2 و DADA2، `trim-left` و `trunc-len` و دلیلشان (نمودار کیفیت، طول آمپلیکون)، `maxEE`، روش pooling و chimera، درصد ریدهای باقی‌مانده در هر مرحله (یا جدول `denoising-stats` در پیوست)، و تعداد ASV.

---

## تمرین ۴: طبقه‌بندی

### ۴.۱ Naive Bayes
```bash
qiime tools export --input-path taxonomy.qza --output-path tx
T=tx/taxonomy.tsv
awk -F'\t' 'NR>1{print split($2,a,"; ")}' $T | sort | uniq -c        # depth reached
awk -F'\t' 'NR>1{split($2,a,"; "); print a[2]}' $T | sort | uniq -c | sort -nr | head -5
grep -c 'd__Archaea' $T
```
- **۳۶۸ از ۴۱۴ ASV** (۸۹٪) تا سطح جنس رفتند (با Confidence ≥ ۰٫۷).
- پنج شاخه‌ی پرتعداد: Actinobacteriota ۱۷۰، Proteobacteria ۶۵، Chloroflexi ۳۹، Acidobacteriota ۲۸، Gemmatimonadota ۲۵.
- **۱۳ ASV آرکی**: ۱۲ تا Nitrososphaeraceae (Thaumarchaeota یا Crenarchaeota، اکسیدکننده‌های آمونیاک خاک) و ۱ Marine Group II.

چرا آرکی؟ «16S» نام ژن است، نه «باکتری». آرکی‌ها هم 16S rRNA دارند. پرایمرهای 515F/806R در نواحی‌ای می‌چسبند که بین باکتری‌ها و آرکی‌ها حفاظت‌شده است. پس این پرایمرها **پروکاریوت‌ها** را تکثیر می‌کنند. اگر می‌خواهید فقط باکتری را گزارش کنید، باید صریحاً فیلتر کنید (`qiime taxa filter-table --p-include d__Bacteria`) و این را بنویسید.

### ۴.۲ vsearch در برابر Naive Bayes
```bash
qiime feature-classifier classify-consensus-vsearch --i-query rep-seqs.qza \
  --i-reference-reads ../../04_16S_Amplicon/data/db/silva-138-99-seqs-515-806.qza \
  --i-reference-taxonomy ../../04_16S_Amplicon/data/db/silva-138-99-tax-515-806.qza \
  --p-threads 4 --o-classification taxonomy-vsearch.qza --o-search-results vsearch-hits.qza
```
(برای مقایسه، هر دو جدول را export کنید و با Python روی `Feature ID` به هم وصل کنید.)
- **شاخه:** ۴۱۰ از ۴۱۴ یکسان (۹۹٪).
- **جنس:** ۳۴۰ ASV در هر دو روش تا جنس رفتند، ۳۱۶ یکسان (۹۳٪).

سه اختلاف پرریدتر:

| ASV | ریدها | Naive Bayes (Confidence) | vsearch (Consensus) |
| :--- | ---: | :--- | :--- |
| `28df1c17…` | 187 | f__uncultured; g__uncultured (0.81) | f__IMCC26256; g__IMCC26256 (0.7) |
| `92f28f07…` | 62 | f__uncultured; g__uncultured (0.89) | f__IMCC26256; g__IMCC26256 (0.6) |
| `29b4b858…` | 61 | Bacillaceae; *Falsibacillus* (0.95) | Bacillaceae; *Bacillus* (0.8) |

تفسیر:
- دو مورد اول عملاً «اختلاف بر سر یک نام جای‌خالی» است. هر دو روش می‌گویند «یک دودمان بی‌نام اکتینوباکتری»، فقط با برچسب متفاوت.
- *Falsibacillus* در برابر *Bacillus* یک اختلاف واقعی است. ناحیه‌ی V4 بین جنس‌های Bacillaceae تفاوت کمی دارد.
- Confidence (NB) و Consensus (vsearch) **یک مقیاس نیستند**. Confidence احتمال بوت‌استرپ است. Consensus سهم بهترین نتیجه‌های جستجو با همان برچسب است (پیش‌فرض: ۱۰ نتیجه، حداقل ۵۱٪).

### ۴.۳ `g__uncultured`
```bash
qiime taxa collapse --i-table table.qza --i-taxonomy taxonomy.qza --p-level 6 --o-collapsed-table genus.qza
qiime tools export --input-path genus.qza --output-path genus
biom convert -i genus/feature-table.biom -o genus.tsv --to-tsv
grep -c 'g__uncultured' genus.tsv ; awk -F'\t' 'NR>2' genus.tsv | wc -l
grep 'g__uncultured' genus.tsv | cut -f1 | head -3
```
```text
20
142
d__Bacteria;p__Planctomycetota;c__Planctomycetes;o__Pirellulales;f__Pirellulaceae;g__uncultured
d__Bacteria;p__Planctomycetota;c__Planctomycetes;o__Gemmatales;f__Gemmataceae;g__uncultured
d__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Burkholderiales;f__uncultured;g__uncultured
```
`g__uncultured` در **۲۰ دودمان مختلف** هست. `taxa collapse` آن‌ها را یکی **نمی‌کند**: جدول ۱۴۲ سطر دارد و شناسه‌ی هر سطر کل دودمان است. خطر وقتی است که خودتان در pandas یا R فقط با «نام جنس» گروه‌بندی کنید: این ۲۰ سطر یک «جنس» ۱۵٫۶ درصدی می‌سازند که دومین تاکسون فراوان داده به نظر می‌رسد (درس، بخش ۴.۵).

### ۴.۴ «*Rubrobacter radiotolerans* گونه‌ی غالب بود»
1. **گونه از V4 قابل ادعا نیست.** طبقه‌بند ما اصلاً سطح گونه ندارد. حتی با طبقه‌بند گونه‌ای، یک قطعه‌ی ۲۲۷ بازی معمولاً گونه‌های یک جنس را از هم جدا نمی‌کند. حداکثر می‌توان گفت «جنس *Rubrobacter*».
2. **«غالب» نیست.** *Rubrobacter* با ۵٫۹٪ ریدها پنجمین برچسب است (بعد از wb1-P19 با ۱۶٫۹٪). به‌علاوه درصد ریدها برابر درصد سلول‌ها نیست: تعداد نسخه‌ی ژن 16S و سوگیری PCR آن را تغییر می‌دهند. باید بنویسد «فراوانی **نسبی** ریدهای *Rubrobacter*…».

---

## تمرین ۵: پوشش گیاهی یا ارتفاع؟

### ۵.۱ دو ترتیب
```bash
qiime diversity adonis --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
  --m-metadata-file $M --p-formula "elevation+vegetation" --o-visualization adonis_ev.qzv
qiime diversity adonis ... --p-formula "vegetation+elevation" --o-visualization adonis_ve.qzv
```
| ترتیب | جمله‌ی اول: R²، p | جمله‌ی دوم: R²، p |
| :--- | :--- | :--- |
| `elevation+vegetation` | elevation: 0.070، **0.001** | vegetation: 0.030، 0.092 |
| `vegetation+elevation` | vegetation: 0.079، **0.001** | elevation: 0.021، 0.385 |

`adonis` در QIIME 2 جمع مربعات **ترتیبی (type I)** می‌دهد. جمله‌ی اول همه‌ی تغییراتی را که توضیح می‌دهد برمی‌دارد، **از جمله سهم مشترک** دو متغیر. جمله‌ی دوم فقط با «باقی‌مانده» سنجیده می‌شود. چون دو متغیر شدیداً همبسته‌اند، سهم مشترک بزرگ است و به هر کدام که اول بیاید می‌رسد. Residual در هر دو مدل یکسان است (R² = 0.90)، چون مدل کامل یکی است. فقط **تقسیم** آن عوض شده است.

برای آزمون **حاشیه‌ای** (type III: «سهم هر متغیر با فرض حضور بقیه») در QIIME 2 2026.7 گزینه‌ای نیست. در R: `vegan::adonis2(d ~ elevation + vegetation, data = md, by = "margin")`. در مدل دو متغیره، **جمله‌ی دوم هر ترتیب همان آزمون حاشیه‌ای آن متغیر است**. پس از جدول بالا می‌دانیم: سهم اختصاصی پوشش گیاهی p = 0.092 و سهم اختصاصی ارتفاع p = 0.385. هیچ‌کدام به‌تنهایی معنی‌دار نیست، ولی با هم (سهم مشترک) قوی‌اند.

### ۵.۲ جدول متقاطع
```bash
awk -F'\t' 'NR>2{print $20, $3}' $M | sort -k1,1 -k2n | awk '{print $1}' | uniq -c
awk -F'\t' 'NR>2{print $20, $3}' $M | sort -k1,1 -k2n | awk '{a[$1]=a[$1]" "$2} END{for(k in a) print k":"a[k]}'
```
- بدون گیاه: ۸۹۵ تا ۳٬۱۸۴ متر
- با گیاه: ۲٬۶۸۷ تا ۴٬۶۹۷ متر
- **همپوشانی فقط بین ۲٬۶۸۷ و ۳٬۱۸۴ متر** است: سایت‌های ۲٬۶۸۷ (با گیاه)، ۲٬۸۳۸ (بدون)، ۳٬۰۰۸، ۳٬۱۵۳ و ۳٬۱۸۴ (بدون). زیر ۲٬۶۸۷ متر هیچ سایت گیاه‌داری نیست و بالای ۳٬۱۸۴ متر هیچ سایت بی‌گیاهی.

### ۵.۳ چه می‌توان نوشت؟
- ✅ «ترکیب جامعه (UniFrac بی‌وزن) بین سایت‌های با و بدون پوشش گیاهی متفاوت بود (PERMANOVA، pseudo-F = 3.77، p = 0.001، n = 46). پوشش گیاهی در این طراحی با ارتفاع هم‌خطی (collinear) بود و اثر این دو از هم قابل تفکیک نبود (adonis ترتیبی، جدول S…).»
- ❌ «پوشش گیاهی ترکیب میکروبی خاک را **تغییر می‌دهد**.» (ادعای علّی در مطالعه‌ی مشاهده‌ای)
- ❌ «ارتفاع عامل اصلی است و پوشش گیاهی اثری ندارد.» (فقط از یک ترتیب adonis)

### ۵.۴ PERMDISP
```text
PERMDISP  F = 0.042  p = 0.842
```
پراکندگی دو گروه برابر است، پس معنی‌داری PERMANOVA از تفاوت **مرکز** (ترکیب) می‌آید. اگر PERMDISP معنی‌دار بود (مثلاً 0.001)، PERMANOVA معنی‌دار دیگر به‌تنهایی قابل تفسیر نبود: تفاوت می‌توانست از پراکندگی، مرکز یا هر دو باشد. آن وقت باید نمودار PCoA را ببینید و نتیجه را محتاطانه بنویسید («گروه‌ها در ترکیب و/یا پراکندگی متفاوت بودند»). PERMANOVA به عدم تعادل حجم گروه‌ها (این‌جا ۱۵ در برابر ۳۱) همراه با پراکندگی نابرابر به‌خصوص حساس است.

### ۵.۵ عمق rarefaction
```bash
for d in 100 300; do
  qiime diversity core-metrics-phylogenetic --i-phylogeny rooted-tree.qza --i-table table.qza \
    --p-sampling-depth $d --p-random-seed 42 --m-metadata-file $M --output-dir cm$d
  qiime diversity alpha-group-significance --i-alpha-diversity cm$d/faith_pd_vector.qza \
    --m-metadata-file $M --o-visualization ag$d.qzv
done
```
| عمق | نمونه (بدون / با گیاه) | Kruskal-Wallis H | p |
| ---: | :--- | ---: | ---: |
| 100 | 49 (17 / 32) | 10.60 | 0.0011 |
| 150 | 46 (15 / 31) | 5.01 | 0.025 |
| 300 | 28 (7 / 21) | 4.17 | 0.041 |

جهت اثر ثابت ماند ولی **قدرت آن ۲۰ برابر** بین عمق‌ها تغییر کرد (p از ۰٫۰۰۱ تا ۰٫۰۴). دو اثر هم‌زمان در کارند:
- **عمق بالاتر** = تخمین دقیق‌تر تنوع هر نمونه.
- **عمق بالاتر** = نمونه‌ی کمتر (در عمق ۳۰۰، گروه بی‌گیاه فقط ۷ نمونه دارد) و حذف **غیرتصادفی** نمونه‌ها. نمونه‌های کم‌رید ممکن است به‌طور سیستماتیک از سایت‌های خشک‌تر و کم‌زیست‌توده‌تر باشند.

درس: عمق rarefaction را **قبل** از دیدن نتیجه‌ی آزمون انتخاب کنید (با منحنی rarefaction، `qiime diversity alpha-rarefaction`) و در مقاله یک **تحلیل حساسیت** با چند عمق گزارش کنید. انتخاب عمقی که «p کوچک‌تری می‌دهد» همان p-hacking است.

---

## تمرین ۶: طراحی مطالعه‌ی واقعی

### ۶.۱ طرح نمونه‌برداری
از متغیرها **جدولی کامل** بسازید: در **هر** باند ارتفاعی (مثلاً هر ۵۰۰ متر)، هم نقاط زیر گیاه (ریزوسفر یا زیر تاج پوشش) و هم نقاط بی‌گیاه در فاصله‌ی چند متری، با **نمونه‌های جفت‌شده**. آن وقت مدل `distance ~ elevation_band + vegetation + elevation_band:vegetation` با جایگشت **درون‌بلوکی** (`strata` در `adonis2`) اثر گیاه را جدا از ارتفاع می‌سنجد. اگر در ارتفاع پایین واقعاً گیاهی وجود ندارد، سؤال باید محدود شود: «در محدوده‌ی ۲٬۷۰۰ تا ۳٬۲۰۰ متر…».

### ۶.۲ کنترل‌ها برای خاک کم‌زیست‌توده
- **کنترل منفی استخراج** (کیت بدون خاک) در هر دسته‌ی استخراج، و **کنترل منفی PCR** (آب). در نمونه‌های کم‌زیست‌توده، DNA آلوده‌ی کیت‌ها («kitome»، Salter et al. 2014) می‌تواند بخش بزرگی از ریدها باشد.
- **کنترل مثبت / mock community** با ترکیب معلوم (مثلاً ZymoBIOMICS) برای سنجش خطای کل مسیر.
- **ثبت غلظت DNA** هر نمونه (در metadata این داده ستون `extract-concen` همین است).
- **حذف آلودگی با `decontam`** (Davis et al. 2018):
  - روش **frequency**: ASVی که فراوانی نسبی‌اش با غلظت DNA **رابطه‌ی معکوس** دارد، آلودگی است (آلودگی مقدار ثابتی است، پس در نمونه‌ی رقیق سهم بیشتری دارد).
  - روش **prevalence**: ASVی که در کنترل‌های منفی **شایع‌تر** از نمونه‌هاست، آلودگی است.
  - در QIIME 2 افزونه‌ی `q2-quality-control` (`decontam-identify`) یا در R بسته‌ی `decontam`.
- کنترل‌ها را **تصادفی** بین پلیت‌ها و دسته‌ها پخش کنید، نه در یک گوشه.

### ۶.۳ عمق توالی‌یابی
هدف معمول برای 16S خاک: **حداقل ۱۰٬۰۰۰ تا ۳۰٬۰۰۰ رید** پس از DADA2 در هر نمونه (خاک از متنوع‌ترین محیط‌هاست). میانه‌ی ۲۴۳ رید این داده کافی نیست، چون:
- DADA2 در عمق کم، توالی‌های نادر را از خطا تشخیص نمی‌دهد و ریدهای reverse را کامل تصحیح نمی‌کند. نتیجه: **۵۱٪ افت در ادغام** (تمرین ۳)، که در عمق کافی به چند درصد می‌رسد.
- تشخیص chimera عملاً غیرممکن است (صفر chimera).
- rarefaction به ۱۵۰ رید یعنی کنار گذاشتن یک‌سوم نمونه‌ها و تخمین پرخطای تنوع.
- قبل از تعیین عمق، **منحنی rarefaction** یک ران آزمایشی را ببینید: عمقی که منحنی در آن صاف می‌شود.

### ۶.۴ مرجع طبقه‌بندی
- **SILVA 138.2** (یا آخرین نسخه) یا **GTDB** (برای نام‌گذاری مبتنی بر ژنوم) یا **Greengenes2** (اگر می‌خواهید با داده‌ی shotgun در یک درخت ادغام کنید).
- آماده‌سازی با **RESCRIPt** (Robeson et al. 2021): دانلود، حذف توالی‌های کم‌کیفیت و کوتاه، **dereplicate** با حل اختلاف تاکسونومی، استخراج ناحیه‌ی **پرایمرهای خودتان** (`feature-classifier extract-reads`)، و آموزش Naive Bayes **با همان نسخه‌ی scikit-learn** محیط تحلیل.
- نسخه‌ی مرجع، تاریخ و پارامترهای آماده‌سازی را در روش‌ها بنویسید. اگر حافظه کم است (مثل این درس)، می‌توانید مثل ما سطح گونه را حذف کنید یا با dereplicate تعداد کلاس‌ها را کم کنید.

### ۶.۵ پاسخ به داور درباره‌ی rarefy
نمونه‌ی پاسخ:

> McMurdie & Holmes (2014) نشان دادند rarefy برای **آزمون فراوانی تفاضلی** تک‌تک تاکسون‌ها، داده را دور می‌ریزد و توان آماری را کم می‌کند. ما برای این هدف از rarefy استفاده **نکردیم**. برای فراوانی تفاضلی از روش‌های مبتنی بر لگاریتم نسبت (ANCOM-BC2 / ALDEx2) روی جدول کامل استفاده کردیم. rarefy فقط برای **معیارهای تنوع آلفا و بتا** به کار رفت، که به عمق نمونه حساس‌اند. Weiss et al. (2017) نشان دادند rarefy برای این هدف، به‌ویژه با عمق کتابخانه‌ی بسیار نابرابر، رفتار خوبی دارد. عمق ۱۵۰ را از منحنی rarefaction انتخاب کردیم و نتایج را در عمق‌های ۱۰۰ و ۳۰۰ هم گزارش کردیم (جدول S…). seed تصادفی ثابت (۴۲) بود.

جایگزین‌ها: فاصله‌ی **Aitchison** (اقلیدسی روی CLR، از `DEICODE`/`gemelli` با robust Aitchison PCA در QIIME 2) برای بتا، و برای آلفا تخمین‌گرهایی مثل **breakaway** (q2-breakaway) که تعداد گونه‌های دیده‌نشده را هم تخمین می‌زنند.

---

## منابع پاسخ‌ها
- Salter SJ, et al. (2014). Reagent and laboratory contamination can critically impact sequence-based microbiome analyses. *BMC Biology* 12:87. https://doi.org/10.1186/s12915-014-0087-z
- Weiss S, et al. (2017). Normalization and microbial differential abundance strategies depend upon data characteristics. *Microbiome* 5:27. https://doi.org/10.1186/s40168-017-0237-y
- Lin H, Peddada SD (2020). Analysis of compositions of microbiomes with bias correction (ANCOM-BC). *Nature Communications* 11:3514. https://doi.org/10.1038/s41467-020-17041-7
- سایر منابع: انتهای [01_lesson.md](01_lesson.md).
