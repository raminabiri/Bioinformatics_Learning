# درس ۲: پیرایش آداپتور، پیرایش کیفیت و فیلتر ریدها با fastp

**بخش:** `06_Metagenomics` · **ماژول:** `01_Read_QC_Trimming` · **پیش‌نیاز:** درس ۱ · **زمان:** ۱٫۵ ساعت · **ابزار:** fastp 0.23.4، FastQC 0.12.1، MultiQC 1.25.1 · **آخرین تست:** 2026-10-12

---

## ۱. مسئله

درس ۱ نشان داد کجا مشکل هست. حالا باید تصمیم بگیریم **چه چیزی را حذف کنیم**. هر حذفی دو طرف دارد:
- **کم حذف کردن:** آداپتور و بازهای پرخطا وارد mapping و طبقه‌بندی می‌شوند. نتیجه mapping کمتر، k-mer کاذب در Kraken2 و آلل کاذب در فراخوانی واریانت است.
- **زیاد حذف کردن:** داده از دست می‌رود، ریدها کوتاه می‌شوند (طبقه‌بندی k-mer و mapping دقیق‌تر با رید بلند بهتر است)، و چون حذف یکنواخت نیست، **فراوانی گونه‌ها هم مخدوش می‌شود**. مثلاً اگر کیفیت به GC وابسته باشد، گونه‌های GC بالا بیشتر حذف می‌شوند.

پس هدف «تمیزترین داده‌ی ممکن» نیست، بلکه **حذف آنچه واقعاً آسیب می‌زند با کمترین هزینه** است.

## ۲. سه عملیات متفاوت در fastp

بیشتر سردرگمی‌ها از اینجاست که این سه را یکی فرض می‌کنیم:

| عملیات | چه می‌کند | گزینه‌های fastp | پیش‌فرض |
| :--- | :--- | :--- | :--- |
| **پیرایش آداپتور** | توالی آداپتور را از انتهای 3' می‌بُرد | `--detect_adapter_for_pe` یا `--adapter_sequence` | برای SE فعال است. برای PE، تشخیص با هم‌پوشانی جفت‌ها فعال است و `--detect_adapter_for_pe` تشخیص توالی را هم اضافه می‌کند |
| **پیرایش کیفیت** (trimming) | **بازها** را از سر یا ته رید می‌بُرد | `--cut_front`، `--cut_tail`، `--cut_right` (+ `--cut_mean_quality`، `--cut_window_size`) | **غیرفعال** |
| **فیلتر کیفیت** (filtering) | **کل رید** (و جفتش) را دور می‌اندازد | `-q` (حد کیفیت هر باز، پیش‌فرض 15)، `-u` (حداکثر درصد باز زیر حد، پیش‌فرض 40)، `-n` (حداکثر N، پیش‌فرض 5)، `-e` (میانگین کیفیت)، `-l` (حداقل طول، پیش‌فرض 15) | فعال |

> **اشتباه رایج:** «`fastp -q 20` بازهای زیر Q20 را می‌بُرد.» **نادرست است.** `-q` فقط تعریف می‌کند چه بازی «باکیفیت» حساب شود. سپس رید فقط وقتی **کامل** حذف می‌شود که بیش از `-u` درصد بازهایش زیر این حد باشند. هیچ بازی بریده نمی‌شود. برای بریدن باید یکی از گزینه‌های `--cut_*` را فعال کنید. متن راهنمای خود fastp (`fastp --help`) را بخوانید.

### سه حالت پیرایش کیفیت
همه با یک پنجره‌ی لغزان (پیش‌فرض ۴ باز) و حد میانگین (پیش‌فرض Q20) کار می‌کنند:

```text
رید:        5' ██████████▓▓░██████████████████▓▓░░░ 3'
                         ↑ یک افت کیفیت در وسط            ↑ افت کیفیت در انتها

--cut_front : از 5' جلو می‌رود و تا جایی که پنجره بد است می‌بُرد؛ به اولین پنجره‌ی خوب که رسید، می‌ایستد.
--cut_tail  : از 3' عقب می‌آید و تا جایی که پنجره بد است می‌بُرد؛ به اولین پنجره‌ی خوب که رسید، می‌ایستد.
              → فقط انتهای بد بریده می‌شود: ██████████▓▓░██████████████████
--cut_right : از 5' جلو می‌رود و به **اولین** پنجره‌ی بد که رسید، آن پنجره و **همه‌ی بقیه‌ی رید** را می‌بُرد.
              → ██████████   (افت وسط رید باعث از دست رفتن بیش از نیمی از رید شد)
```
`--cut_right` همان منطق `SLIDINGWINDOW` در Trimmomatic است. خود fastp آن را جایگزین گزینه‌ی قدیمی `--cut_by_quality_aggressive` («تهاجمی») معرفی می‌کند.

## ۳. کار عملی: مقایسه‌ی سه راهبرد روی داده‌ی واقعی

```bash
cd 06_Metagenomics
mkdir -p work/01_qc/compare
R=data/raw; s=minigut

# A) فقط فیلتر کیفیت (مثل دستور رایج «fastp -q 20»)
fastp -i $R/${s}_R1.fastq.gz -I $R/${s}_R2.fastq.gz \
      -o work/01_qc/compare/A_R1.fq.gz -O work/01_qc/compare/A_R2.fq.gz \
      -q 20 -l 36 -j work/01_qc/compare/A.json -h work/01_qc/compare/A.html

# B) پنجره‌ی لغزان «تهاجمی» (معادل SLIDINGWINDOW:4:20 در Trimmomatic)
fastp -i $R/${s}_R1.fastq.gz -I $R/${s}_R2.fastq.gz \
      -o work/01_qc/compare/B_R1.fq.gz -O work/01_qc/compare/B_R2.fq.gz \
      --detect_adapter_for_pe --cut_right --cut_mean_quality 20 -l 50 \
      -j work/01_qc/compare/B.json -h work/01_qc/compare/B.html

# C) پیرایش دو سر (راهبرد انتخابی این دوره)
fastp -i $R/${s}_R1.fastq.gz -I $R/${s}_R2.fastq.gz \
      -o work/01_qc/compare/C_R1.fq.gz -O work/01_qc/compare/C_R2.fq.gz \
      --detect_adapter_for_pe --cut_front --cut_tail --cut_mean_quality 20 -l 50 \
      -j work/01_qc/compare/C.json -h work/01_qc/compare/C.html

# خلاصه از گزارش‌های JSON
for x in A B C; do
  jq -r --arg x $x '[$x, .summary.after_filtering.total_reads, .summary.after_filtering.total_bases,
     .summary.after_filtering.q30_rate, .filtering_result.too_short_reads, .filtering_result.low_quality_reads] | @tsv' \
     work/01_qc/compare/$x.json
done
```

نتیجه‌ی واقعی (ورودی: ۱۰۰٬۰۰۰ رید = ۵۰٬۰۰۰ جفت، ۱۲٫۶ میلیون باز، Q30 = 91.29%):

| راهبرد | ریدهای باقی‌مانده | بازهای باقی‌مانده | Q30 بعد | حذف: کوتاه | حذف: کیفیت پایین |
| :--- | ---: | ---: | :-: | ---: | ---: |
| A: `-q 20` (فقط فیلتر) | 99,594 (99.6%) | 12,548,238 | 91.40% | 0 | 406 |
| B: `--cut_right` | **89,176 (89.2%)** | **11,110,072 (88.2%)** | 94.47% | **10,734** | 90 |
| C: `--cut_front --cut_tail` | 99,690 (99.7%) | 12,545,615 | 91.47% | 2 | 308 |

برای `minigut_sample2` (ریدهای 151 bp) همین الگو با شدت کمتر تکرار می‌شود: B ۹۸٫۴٪ ریدها را نگه می‌دارد و C ۹۹٫۹۸٪.

### تفسیر
- **A** عملاً هیچ بازی را نبرید. ۴۰۶ رید حذف شدند، چون بیش از ۴۰٪ بازهایشان زیر Q20 بود. Q30 تقریباً تغییری نکرد. اگر هدف حذف انتهای بی‌کیفیت بود، **این دستور آن کار را نمی‌کند.**
- **B** بالاترین Q30 را دارد، ولی به قیمت **۱۰٫۸٪ ریدها و ۱۱٫۸٪ بازها**. علت را از گام ۱ درس ۱ می‌دانیم: در این داده بازهای کم‌کیفیت **پراکنده در وسط ریدها** هستند، مثل `/` (Q14) در موقعیت ۲۴ رید اول. شمارش ساده نشان می‌دهد:
  ```bash
  zcat data/raw/minigut_R1.fastq.gz | awk 'NR%4==0{q=substr($0,1,60); if (q ~ /[!-4]/) c++; n++} END{print c, n, c/n}'
  # 27602 50000 0.55204   ← ۵۵٪ ریدها در ۶۰ باز اول دست‌کم یک باز زیر Q20 دارند
  ```
  `--cut_right` با هر افت موضعی که میانگین یک پنجره‌ی ۴تایی را زیر ۲۰ ببرد، کل ادامه‌ی رید را می‌بُرد. بعد بسیاری از ریدها زیر ۵۰ باز می‌روند و با `-l 50` حذف می‌شوند. **افزایش Q30 مصنوعی است:** داده را «بهتر» نکرده‌ایم، بخش بزرگی از آن را دور ریخته‌ایم.
- **C** انتهاهای بد را می‌بُرد، بازهای پراکنده‌ی کم‌کیفیت وسط رید را نگه می‌دارد (mapper و طبقه‌بند با یک باز Q14 در وسط رید مشکلی ندارند) و ۹۹٫۷٪ داده را حفظ می‌کند.

**تصمیم این دوره:** راهبرد C (`--cut_front --cut_tail --cut_mean_quality 20`) با `--detect_adapter_for_pe` و `-l 50`. دلیل `-l 50`: ریدهای خیلی کوتاه در طبقه‌بندی k-mer (Kraken2 با k=35) و mapping چندجایی مشکل‌سازند.

> این نتیجه یک قانون جهانی نیست. روی داده‌ای با افت شدید کیفیت فقط در انتهای 3'، B و C نتیجه‌ی نزدیک به هم می‌دهند. **درس اصلی این است که پارامتر را با داده‌ی خودتان و با نگاه به گزارش fastp انتخاب کنید**، نه با کپی از یک مقاله.

## ۴. اجرای نهایی برای همه‌ی نمونه‌ها

اسکریپت [scripts/run_qc.sh](scripts/run_qc.sh) همین راهبرد را روی هر دو نمونه اجرا می‌کند و FastQC و MultiQC را قبل و بعد اجرا می‌کند:
```bash
bash 01_Read_QC_Trimming/scripts/run_qc.sh
bash 01_Read_QC_Trimming/scripts/check.sh
```
```text
  [OK]   minigut: R1 and R2 still paired (49845 reads each)
  [OK]   minigut: 99.69% reads kept (>=95% expected for this dataset)
  [OK]   minigut_sample2: R1 and R2 still paired (24988 reads each)
  [OK]   minigut_sample2: 99.98% reads kept (>=95% expected for this dataset)
  ...
Result: 18 passed, 0 failed
```

**جفت‌بودن ریدها:** fastp در حالت PE اگر یکی از دو رید حذف شود، **جفتش را هم حذف می‌کند**. به همین دلیل R1 و R2 همیشه تعداد مساوی دارند. ابزارهای پایین‌دستی (Bowtie2، MetaPhlAn، HUMAnN) فرض می‌کنند رید n‌ام R1 با رید n‌ام R2 جفت است. اگر R1 و R2 را جدا پیرایش کنید، این ترتیب به هم می‌ریزد. (fastp می‌تواند ریدهای بی‌جفت را با `--unpaired1/--unpaired2` جداگانه نگه دارد.)

**FastQC بعد از پیرایش:**
```text
minigut_R1_fastqc:          WARN  Sequence Length Distribution
minigut_sample2_R1_fastqc:  FAIL  Per sequence GC content   WARN  Sequence Length Distribution
```
WARN طول **انتظار می‌رود**، چون ریدها دیگر طول یکسان ندارند. FAIL مربوط به GC هم همان FAIL «خوب» درس ۱ است: ترکیب جامعه با پیرایش عوض نشده است.

## ۵. دام‌ها (Pitfalls)

| دام | چرا مشکل است | راه درست |
| :--- | :--- | :--- |
| `-q 20` به‌عنوان «trimming» | هیچ بازی بریده نمی‌شود | `--cut_tail` (و در صورت نیاز `--cut_front`) |
| کپی کردن `SLIDINGWINDOW:4:20` یا `--cut_right` از مقالات | با افت‌های موضعی کیفیت، بخش بزرگی از داده دور ریخته می‌شود | چند راهبرد را روی داده‌ی خودتان مقایسه کنید |
| `-l` خیلی کم (مثلاً پیش‌فرض 15) | ریدهای کوتاه طبقه‌بندی و map کاذب می‌گیرند | ۳۶ تا ۵۰ برای Illumina 2×150 |
| پیرایش جداگانه‌ی R1 و R2 | جفت‌ها به هم می‌ریزند | همیشه PE را با هم پردازش کنید |
| `--dedup` در متاژنوم | فراوانی گونه‌های غالب کم برآورد می‌شود | بدون دلیل مشخص استفاده نکنید |
| گزارش «X٪ ریدها حذف شد» بدون دلیل | قابل ارزیابی نیست | دلیل حذف را از `filtering_result` گزارش fastp بیاورید |
| ندیدن گزارش fastp | fastp آداپتور، اندازه‌ی insert و duplication را هم گزارش می‌کند | HTML هر نمونه یا MultiQC تجمیعی را ببینید |

## ۶. جمع‌بندی
- در fastp سه عملیات جدا داریم: پیرایش آداپتور، **پیرایش** کیفیت (`--cut_*`) و **فیلتر** کیفیت (`-q/-u/-l`). `-q` بازی را نمی‌بُرد.
- `--cut_right` (معادل SLIDINGWINDOW) با افت‌های موضعی کیفیت تهاجمی است. روی داده‌ی ما ۱۰٫۸٪ ریدها را بی‌دلیل حذف کرد.
- راهبرد این دوره `--cut_front --cut_tail --cut_mean_quality 20 -l 50 --detect_adapter_for_pe` است که ۹۹٫۷٪ داده را نگه می‌دارد و جفت‌ها را حفظ می‌کند.
- همیشه بعد از پیرایش دوباره QC کنید و تعداد و دلیل حذف را گزارش دهید.

## ۷. منابع

### مستندات و مقالات
- Chen S, et al. (2018). fastp: an ultra-fast all-in-one FASTQ preprocessor. *Bioinformatics* 34(17):i884–i890. https://doi.org/10.1093/bioinformatics/bty560
- Chen S (2023). Ultrafast one-pass FASTQ data preprocessing, quality control, and deduplication using fastp. *iMeta* 2:e107. https://doi.org/10.1002/imt2.107
- مستندات و کد fastp: https://github.com/OpenGene/fastp
- Ewels P, et al. (2016). MultiQC. *Bioinformatics* 32(19):3047–3048. https://doi.org/10.1093/bioinformatics/btw354

### ویدیوهای آموزشی
- profbiot — *How to run fastp for trimming, filtering, and reports*: https://www.youtube.com/watch?v=zgQ6b0AerKQ
- Galaxy Project — *GTN Training: Intro to NGS – Quality Control (Tutorial)*: https://www.youtube.com/watch?v=QJRlX2hWDKM
- Phil Ewels — *Using MultiQC Reports*: https://www.youtube.com/watch?v=qPbIlO_KWN0

> لینک‌ها در تاریخ 2026-10-12 بررسی شدند (ویدیوها با YouTube oEmbed، DOIها با Crossref، صفحات با درخواست HTTP).
