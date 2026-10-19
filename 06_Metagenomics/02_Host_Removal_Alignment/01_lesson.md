# درس: حذف DNA میزبان و مبانی همترازی ریدها

**بخش:** `06_Metagenomics` · **ماژول:** `02_Host_Removal_Alignment` · **پیش‌نیاز:** ماژول ۰۱ · **زمان:** ۲ ساعت · **ابزار:** Bowtie2 2.5.4، samtools 1.20، wgsim 1.20 · **آخرین تست:** 2026-10-13

---

## ۱. مسئله

نمونه‌ی متاژنومی انسانی همیشه مقداری DNA انسان دارد. سهم آن به نوع نمونه بستگی دارد: در مدفوع معمولاً کم است، ولی در بزاق، خلط، بافت یا خون می‌تواند بخش بزرگی از ریدها باشد. این ریدها باید **پیش از هر تحلیل دیگری** حذف شوند، به دو دلیل:

1. **اخلاقی و حقوقی:** ریدهای انسانی اطلاعات ژنتیکی شرکت‌کننده‌اند. انتشار آن‌ها در آرشیو عمومی همراه با ریدهای میکروبی ممکن است حریم خصوصی را نقض کند و معمولاً با رضایت‌نامه‌ی مطالعه هم سازگار نیست.
2. **علمی:** ریدهای انسانی زمان محاسبه را هدر می‌دهند و ممکن است به‌اشتباه به taxonهای میکروبی نسبت داده شوند، به‌ویژه وقتی دیتابیس آلودگی انسانی دارد. درصد میزبان هم خودش یک معیار QC است: نمونه‌ای با ۹۵٪ ریدهای انسانی عمق میکروبی کافی ندارد.

روش استاندارد: ریدها را روی ژنوم میزبان **همتراز (align)** کنید و فقط جفت‌هایی را نگه دارید که **هیچ‌کدام از دو mate** روی میزبان ننشسته‌اند.

## ۲. مفاهیم کلیدی همترازی

### ۲.۱ ایندکس و FM-index
جستجوی میلیون‌ها رید کوتاه در یک ژنوم ۳ میلیارد بازی با مقایسه‌ی مستقیم ممکن نیست. Bowtie2 ژنوم مرجع را یک‌بار با **تبدیل Burrows-Wheeler (BWT)** و **FM-index** فشرده و ایندکس می‌کند. بعد هر رید را با «seed»های کوتاه در ایندکس پیدا می‌کند و دوروبر seed را با برنامه‌ریزی پویا گسترش می‌دهد.

نکته‌ی عملی: ایندکس کامل ژنوم انسان چند گیگابایت است و ساختنش چند ساعت طول می‌کشد. **ایندکس‌های از پیش ساخته‌شده** را دانلود کنید: https://benlangmead.github.io/aws-indexes/bowtie

### ۲.۲ خروجی SAM/BAM: فیلدهایی که اینجا لازم داریم
| فیلد | معنی | در حذف میزبان |
| :--- | :--- | :--- |
| `FLAG` | وضعیت رید به‌صورت بیت‌های جمع‌شده | **مهم‌ترین فیلد**: map شده یا نه، mate map شده یا نه |
| `MAPQ` | اطمینان از **یکتا بودن** محل همترازی (Phred) | برای حذف میزبان مهم **نیست**: ریدی که روی دو جای ژنوم انسان می‌نشیند هم انسانی است |
| `CIGAR` | شکل همترازی (مثلاً `126M`) | — |
| `TLEN` | طول قطعه‌ی برآوردشده | برای فهم جفت‌های «discordant» |

بیت‌های FLAG که اینجا به کار می‌آیند:
```bash
samtools flags 77    # 0x4d  PAIRED,UNMAP,MUNMAP,READ1   ← هر دو mate unmapped: نگه دار
samtools flags 141   # 0x8d  PAIRED,UNMAP,MUNMAP,READ2
samtools flags 99    # 0x63  PAIRED,PROPER_PAIR,MREVERSE,READ1   ← جفت concordant روی میزبان
samtools flags 73    # 0x49  PAIRED,MUNMAP,READ1         ← خودش map شده، mate نه
```
`-f 12` در samtools یعنی «بیت‌های 4 (UNMAP) **و** 8 (MUNMAP) هر دو روشن باشند»، یعنی هر دو mate بدون همترازی.

### ۲.۳ concordant، discordant و تک‌مِیت
Bowtie2 جفتی را **concordant** می‌داند که جهت mateها درست باشد و طول قطعه بین `-I` و `-X` (پیش‌فرض ۰ تا **۵۰۰**) باشد. گزینه‌ی رایج `--un-conc` در Bowtie2 جفت‌هایی را بیرون می‌دهد که **concordant همتراز نشده‌اند**. این شامل جفت‌هایی هم می‌شود که هر دو mate روی میزبان نشسته‌اند ولی طول قطعه‌شان بیش از ۵۰۰ است، یا فقط یک mate نشسته است. در گام ۴ این تفاوت را با عدد می‌بینیم.

## ۳. کار عملی

```bash
cd 06_Metagenomics
# پیش‌نیاز: ماژول ۰۱ اجرا شده باشد (work/01_qc/trimmed)
bash data/download.sh     # host/host_chr21_region.fa و host/human_chr1_region.fa را هم می‌گیرد
```

### گام ۱: داده‌ی ما میزبان ندارد، پس یک آزمایش کنترل‌شده می‌سازیم
ریدهای دوره از ژنوم‌های میکروبی شبیه‌سازی شده‌اند و **۰٪ ریدهای انسانی** دارند (در گام ۳ تأیید می‌شود). برای اینکه حذف میزبان را بسنجیم، به نمونه‌ی `minigut` ریدهای انسانی شبیه‌سازی‌شده با نام منشأ اضافه می‌کنیم:

| منشأ | جفت‌رید | در ایندکس میزبان هست؟ |
| :--- | ---: | :---: |
| باکتری‌ها (minigut پس از QC) | 49,845 | — |
| انسان: ناحیه‌ی 500 kb از chr21 | 5,000 | ✅ |
| انسان: ناحیه‌ی 300 kb از chr1 (GRCh38، 100.0–100.3 Mb) | 5,000 | ❌ |

```bash
bash 02_Host_Removal_Alignment/scripts/make_spiked_sample.sh
```
اسکریپت با `wgsim` ریدهای ۱۲۶ بازی با insert حدود ۳۵۰ باز و خطای ۰٫۲٪ می‌سازد. **seed ثابت (`-S 42`)** دارد، پس نتیجه برای همه یکسان است. هر رید انسانی با پیشوند `HUMAN_chr21_` یا `HUMAN_chr1_` نام‌گذاری شده تا منشأ واقعی‌اش معلوم باشد.

### گام ۲: ایندکس و همترازی
اسکریپت [scripts/run_host_removal.sh](scripts/run_host_removal.sh) این کارها را انجام می‌دهد (هسته‌ی آن):
```bash
bowtie2-build -q data/host/host_chr21_region.fa work/02_host/index/host

bowtie2 -p 4 --very-sensitive -x work/02_host/index/host \
    -1 work/01_qc/trimmed/minigut_R1.fastq.gz -2 work/01_qc/trimmed/minigut_R2.fastq.gz \
    2> minigut.bowtie2.log \
  | samtools view -b -o minigut.unsorted.bam -

# فقط جفت‌هایی که هر دو mate بدون همترازی‌اند (-f 12) و رکورد اصلی (-F 256)
samtools view -b -f 12 -F 256 minigut.unsorted.bam \
  | samtools fastq -1 clean_R1.fastq.gz -2 clean_R2.fastq.gz -0 /dev/null -s /dev/null -n -
```
- `--very-sensitive` (= `-D 20 -R 3 -N 0 -L 20 -i S,1,0.50`) seedهای کوتاه‌تر و تلاش بیشتری دارد. برای حذف میزبان می‌خواهیم **حساسیت** بالا باشد.
- Bowtie2 دو mate هر جفت را پشت سر هم می‌نویسد. به همین دلیل `samtools fastq` بدون مرتب‌سازی، جفت‌ها را درست جدا می‌کند.

### گام ۳: اجرا روی همه‌ی نمونه‌ها
```bash
bash 02_Host_Removal_Alignment/scripts/run_host_removal.sh
IN=work/02_host/spiked bash 02_Host_Removal_Alignment/scripts/run_host_removal.sh minigut_spiked
```
```text
== minigut
   0.00% overall alignment rate   clean pairs: 49845
== minigut_sample2
   0.00% overall alignment rate   clean pairs: 24988
== minigut_spiked
   8.65% overall alignment rate   clean pairs: 54570
```
نمونه‌های اصلی ۰٪ همترازی دارند. هیچ ریدی حذف نشد و این همان انتظار ماست.

### گام ۴: سنجش با حقیقت معلوم
چون منشأ هر رید را می‌دانیم، می‌شود **حساسیت** (چند درصد ریدهای انسانی حذف شد) و **ویژگی** (چند درصد ریدهای باکتریایی دست‌نخورده ماند) را دقیق حساب کرد:
```bash
zcat work/02_host/clean/minigut_spiked_R1.fastq.gz | awk 'NR%4==1' \
  | sed -E 's/^@?(HUMAN_chr[0-9]+|NC_[0-9.]+).*/\1/' | sort | uniq -c
```

| منشأ | ورودی | باقی‌مانده با `samtools -f 12` (روش ما) | باقی‌مانده با `--un-conc` |
| :--- | ---: | ---: | ---: |
| باکتری | 49,845 | **49,845 (۱۰۰٪ حفظ)** | 49,845 |
| انسان chr21 (در ایندکس) | 5,000 | **0 (۱۰۰٪ حذف)** | 2 |
| انسان chr1 (خارج از ایندکس) | 5,000 | **4,725 (فقط ۵٫۵٪ حذف)** | 4,926 (۱٫۵٪ حذف) |

سه درس از این جدول:

1. **ویژگی عالی است.** هیچ رید باکتریایی به‌اشتباه حذف نشد.
2. **`--un-conc` نشت دارد.** دو جفت chr21 که هر دو mate روی میزبان نشسته بودند (FLAG 97/145) حذف نشدند، چون طول قطعه‌شان ۵۰۷ و ۵۱۶ باز بود، بیشتر از حد پیش‌فرض `-X 500`. پس «concordant» حساب نشدند. در نمونه‌ی واقعی با میلیون‌ها رید انسانی، این نشت به هزاران رید می‌رسد. روش `-f 12` این مشکل را ندارد.
3. **مرجع ناقص یعنی حذف ناقص.** ۹۴٫۵٪ ریدهای chr1 باقی ماندند، چون این ناحیه در ایندکس نبود. ۲۷۵ جفتی که حذف شدند احتمالاً از تکرارهای پراکنده (مثل Alu و L1) بودند که در chr21 هم نسخه دارند. **در کار واقعی باید کل ژنوم انسان را ایندکس کنید**: GRCh38 (ترجیحاً با توالی‌های alt و decoy) یا T2T-CHM13 که شکاف‌های GRCh38 را پر کرده است.

اگر chr1 را هم به مرجع اضافه کنیم (تمرین ۵)، **همه‌ی** ۱۰٬۰۰۰ جفت انسانی حذف می‌شوند و باز هم همه‌ی ریدهای باکتریایی می‌مانند.

### گام ۵: MAPQ پایین و چرا اینجا مهم نیست
```bash
samtools view -F 4 work/02_host/bam/minigut_spiked.host.bam \
  | awk '$1 ~ /chr21/ {print ($5>=30?">=30":($5>=10?"10-29":($5>=2?"2-9":"0-1")))}' | sort | uniq -c
```
```text
   5924 0-1
     50 2-9
    726 10-29
   3300 >=30
```
۵۹٪ ریدهای chr21 MAPQ صفر یا یک دارند. دلیلش این است که این ناحیه‌ی 500 kb **قطعات تکراری بزرگ** دارد: ۴۴٪ از ۴۰-مرهای آن بیش از یک بار تکرار شده‌اند، مثلاً موقعیت ۰ دقیقاً در موقعیت 381,778 هم آمده است. Bowtie2 نمی‌داند رید از کدام نسخه آمده و MAPQ پایین می‌دهد. برای variant calling چنین ریدی مشکل‌ساز است، ولی **برای حذف میزبان فرقی نمی‌کند**: رید در هر دو حالت انسانی است. پس در حذف میزبان **روی MAPQ فیلتر نکنید**.

### گام ۶: خودسنجی
```bash
bash 02_Host_Removal_Alignment/scripts/check.sh
```
```text
  [OK]   minigut: R1/R2 paired (49845)
  [OK]   minigut: no bacterial pair removed (49845 of 49845 kept)
  ...
  [OK]   spiked: chr21 human pairs left = 0 (<=10)
  [OK]   spiked: all 49845 bacterial pairs kept
Result: 8 passed, 0 failed
```

## ۴. دام‌ها (Pitfalls)

| دام | چرا مشکل است | راه درست |
| :--- | :--- | :--- |
| مرجع ناقص (یک کروموزوم، یا GRCh38 بدون alt/decoy) | ریدهای انسانی نواحی غایب باقی می‌مانند (گام ۴: ۹۴٫۵٪) | کل ژنوم؛ ترجیحاً T2T-CHM13 یا GRCh38 کامل |
| استفاده از `--un-conc` | جفت‌های discordant یا تک‌mate انسانی باقی می‌مانند | `samtools view -f 12 -F 256` روی خروجی همترازی |
| فیلتر MAPQ در حذف میزبان | ریدهای انسانی چندجایی حذف نمی‌شوند | فقط به mapped/unmapped نگاه کنید |
| گزارش نکردن درصد میزبان | معیار QC مهمی از دست می‌رود | درصد میزبان هر نمونه را در جدول QC بیاورید |
| حذف میزبان بعد از طبقه‌بندی تاکسونومیک | ریدهای انسانی ممکن است به taxon میکروبی نسبت داده شوند | همیشه **قبل** از پروفایل |
| انتشار ریدهای خام بدون حذف میزبان | نقض حریم خصوصی | ریدهای پاک‌شده را در ENA/SRA ثبت کنید |

**ابزارهای آماده:** Hostile (روی ژنوم T2T-CHM13 با mask نواحی مشترک با میکروب‌ها) و KneadData (bioBakery) همین منطق را با تنظیمات بهینه بسته‌بندی کرده‌اند. دانستن منطق بالا برای ارزیابی و گزارش آن‌ها لازم است.

## ۵. جمع‌بندی
- حذف میزبان = همترازی روی ژنوم میزبان + نگه داشتن جفت‌هایی که **هر دو** mate unmapped هستند (`-f 12`).
- کیفیت حذف به **کامل بودن مرجع** وابسته است، نه به MAPQ.
- با یک آزمایش کنترل‌شده (ریدهای با منشأ معلوم) می‌شود حساسیت و ویژگی هر روش را دقیق سنجید. روی داده‌ی ما: ویژگی ۱۰۰٪ و حساسیت ۱۰۰٪ برای نواحی موجود در مرجع.

## ۶. منابع

### مقالات و مستندات
- Langmead B, Salzberg SL (2012). Fast gapped-read alignment with Bowtie 2. *Nature Methods* 9:357–359. https://doi.org/10.1038/nmeth.1923
- Danecek P, et al. (2021). Twelve years of SAMtools and BCFtools. *GigaScience* 10(2):giab008. https://doi.org/10.1093/gigascience/giab008
- Constantinides B, et al. (2023). Hostile: accurate decontamination of microbial host sequences. *Bioinformatics* 39(12):btad728. https://doi.org/10.1093/bioinformatics/btad728
- Nurk S, et al. (2022). The complete sequence of a human genome. *Science* 376:44–53. https://doi.org/10.1126/science.abj6987
- راهنمای Bowtie2: https://github.com/BenLangmead/bowtie2
- ایندکس‌های آماده‌ی Bowtie2: https://benlangmead.github.io/aws-indexes/bowtie
- `samtools flags`: https://www.htslib.org/doc/samtools-flags.html · رمزگشای تعاملی FLAG: https://broadinstitute.github.io/picard/explain-flags.html
- Hostile: https://github.com/bede/hostile · KneadData: https://huttenhower.sph.harvard.edu/kneaddata/
- wgsim: https://github.com/lh3/wgsim

### ویدیوهای آموزشی
- Ben Langmead (سازنده‌ی Bowtie) — *Burrows-Wheeler Transform*: https://www.youtube.com/watch?v=4n7NPk5lwbI
- Ben Langmead — *FM Index*: https://www.youtube.com/watch?v=kvVGj5V65io
- Bioinformagician — *SAM flags explained*: https://www.youtube.com/watch?v=qm4NGV79t4o
- EMBL — *Metagenomics principles and workflow*: https://www.youtube.com/watch?v=RcYXTpNS_XU

> لینک‌ها در تاریخ 2026-10-13 بررسی شدند (`_tools/check_links.sh`).
