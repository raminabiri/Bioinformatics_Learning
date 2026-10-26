<div dir="rtl">

# درس ۲: بریدن و پالایش ریدها با fastp

**بخش:** `06_Metagenomics` · **ماژول:** `01_Read_QC_Trimming` · **پیش‌نیاز:** [درس ۱](01_lesson_fastqc.md) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** fastp 0.23.4، FastQC 0.12.1، MultiQC 1.25.1، Python 3 · **خروجی‌ها از اجرای:** 2026-10-12

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. سه کار جدای fastp را از هم بشناسید: بریدن آداپتور، **بریدن** بازهای بد (*trimming*) و **دور ریختن** ریدهای بد (*filtering*).
2. یک دستور fastp برای ریدهای جفتی بنویسید و گزارش آن را بخوانید.
3. با سنجیدن چند راهبرد روی داده‌ی خودتان، پارامتر را **با دلیل** برگزینید.
4. بسنجید که R1 و R2 پس از بریدن هنوز جفت‌اند.
5. عددهای گزارش JSON را با پایتون بیرون بکشید.

**پیش از آغاز:** در پوشه‌ی پروژه‌ی درس ۱ باشید:

<div dir="ltr">

```bash
conda activate metagenomics
cd ~/meta
fastp --version
```

</div>

<div dir="ltr">

```text
fastp 0.23.4
```

</div>

---

## ۱. داستان

درس ۱ گفت داده سالم است، ولی بازهای کم‌کیفیتی هم دارد، در انتها و گاهی در میانه‌ی ریدها. اکنون باید **تصمیم** بگیرید چه چیزی بریده شود. هر برش دو سو دارد:

- **کم بریدن:** آداپتور و بازهای پرخطا به گام‌های بعد می‌روند: همترازی کمتر، k-mer ساختگی در Kraken2 (ماژول ۰۳)، جهش ساختگی در فراخوانی واریانت (بخش ۰۷).
- **زیاد بریدن:** داده از دست می‌رود، ریدها کوتاه می‌شوند، و چون برش یکنواخت نیست، **فراوانی گونه‌ها** هم کج می‌شود (اگر کیفیت به GC وابسته باشد، گونه‌های پر-GC بیشتر بریده می‌شوند).

پس هدف «تمیزترین داده‌ی شدنی» نیست، بلکه **برداشتن آنچه واقعاً آسیب می‌زند، با کمترین هزینه**.

---

## ۲. مفهوم: سه کار جدا

بیشتر سردرگمی‌ها از یکی دانستن این سه است:

| کار | چه می‌کند | گزینه‌ی fastp | پیش‌فرض |
| :--- | :--- | :--- | :--- |
| **بریدن آداپتور** | توالی آداپتور را از انتهای ۳' برمی‌دارد | `--detect_adapter_for_pe` | برای ریدهای جفتی، یافتن آداپتور از راه **هم‌پوشانی** دو رید روشن است؛ این گزینه جست‌وجوی **توالی** آداپتور را هم می‌افزاید |
| **بریدن کیفیت** (*trimming*) | **بازهای** بد را از سر یا ته رید می‌بُرد | `--cut_front`، `--cut_tail`، `--cut_right` | **خاموش** |
| **پالایش کیفیت** (*filtering*) | **کل رید** (و جفتش) را دور می‌اندازد | ‏`-q`، `-u`، `-n`، `-l` | روشن |

### ‏۲.۱ ‏`-q` هیچ بازی نمی‌بُرد

گزینه‌های پالایش، با پیش‌فرض‌هایشان:

| گزینه | معنی | پیش‌فرض |
| :--- | :--- | :---: |
| ‏`-q` | بازی با کیفیت کمتر از این «بد» شمرده می‌شود | 15 |
| ‏`-u` | اگر بیش از این درصد بازهای رید «بد» باشند، رید دور ریخته می‌شود | 40 |
| ‏`-n` | اگر بیش از این شمار `N` داشت، دور ریخته می‌شود | 5 |
| ‏`-l` | اگر پس از برش کوتاه‌تر از این شد، دور ریخته می‌شود | 15 |

پس `fastp -q 20` تنها می‌گوید «زیر Q20 بد است»؛ رید **تنها وقتی** دور ریخته می‌شود که بیش از ۴۰٪ بازهایش بد باشند. **هیچ بازی بریده نمی‌شود.** برای بریدن، یکی از گزینه‌های `--cut_*` لازم است.

### ۲.۲ سه گونه بریدن کیفیت

هر سه با یک **پنجره‌ی لغزان** کار می‌کنند: پنجره‌ای به پهنای ۴ باز (`--cut_window_size`) روی رید جلو می‌رود؛ اگر **میانگین** کیفیت درون پنجره کمتر از ۲۰ (`--cut_mean_quality`) باشد، پنجره «بد» است.

<div dir="ltr">

```text
read:        5' ██████████▓▓░██████████████████▓▓░░░ 3'
                         ↑ a dip in the middle       ↑ low quality at the end

--cut_front : walk from 5'; cut bad windows; stop at the first good window
--cut_tail  : walk from 3'; cut bad windows; stop at the first good window
              -> only the bad end goes:   ██████████▓▓░██████████████████
--cut_right : walk from 5'; at the FIRST bad window, cut it AND EVERYTHING after it
              -> ██████████     (a dip in the middle cost more than half the read)
```

</div>

‏`--cut_right` همان منطق `SLIDINGWINDOW:4:20` در ابزار قدیمی‌تر Trimmomatic است که در بسیاری از مقاله‌ها می‌بینید.

---

## ۳. گام ۱: نخستین دستور fastp

راهبرد این دوره (چرایی‌اش در گام ۲):

<div dir="ltr">

```bash
mkdir -p qc/trimmed qc/fastp
fastp -i raw/minigut_R1.fastq.gz -I raw/minigut_R2.fastq.gz \
      -o qc/trimmed/minigut_R1.fastq.gz -O qc/trimmed/minigut_R2.fastq.gz \
      --detect_adapter_for_pe \
      --cut_front --cut_tail --cut_mean_quality 20 \
      --length_required 50 \
      -j qc/fastp/minigut.json -h qc/fastp/minigut.html
```

</div>

| بخش | چیست | بی آن چه می‌شود |
| :--- | :--- | :--- |
| ① `-i` / `-I` | ورودی R1 / R2 (`I` بزرگ = دومی) | با تنها `-i`، fastp ریدها را تکی (*single-end*) می‌پندارد |
| ② `-o` / `-O` | خروجی R1 / R2 | بی `-o`، ریدهای پالوده **نوشته نمی‌شوند**؛ تنها گزارش ساخته می‌شود |
| ③ `--detect_adapter_for_pe` | جست‌وجوی توالی آداپتور هم | تنها از راه هم‌پوشانی دو رید |
| ④ `--cut_front --cut_tail` | بریدن بازهای بد از دو سر | هیچ بازی بریده نمی‌شود |
| ⑤ `--cut_mean_quality 20` | مرز میانگین پنجره | پیش‌فرض هم ۲۰ است؛ نوشتنش دستور را خواناتر می‌کند |
| ⑥ `--length_required 50` | همان `-l`: ریدهای کوتاه‌تر از ۵۰ دور ریخته شوند | مرز ۱۵: ریدهای بسیار کوتاه که جای درستشان را پیدا نمی‌کنند |
| ⑦ `-j` / `-h` | گزارش JSON (برای ماشین) و HTML (برای چشم) | به نام `fastp.json` و `fastp.html` در پوشه‌ی کنونی نوشته می‌شوند و اجرای بعدی رویشان می‌نویسد |

‏fastp گزارش را روی صفحه (در stderr) هم چاپ می‌کند:

<div dir="ltr">

```text
Detecting adapter sequence for read1...
No adapter detected for read1

Detecting adapter sequence for read2...
No adapter detected for read2

Read1 before filtering:
total reads: 50000
total bases: 6300000
Q20 bases: 6054456(96.1025%)
Q30 bases: 5814382(92.2918%)

Read2 before filtering:
total reads: 50000
total bases: 6300000
Q20 bases: 5974343(94.8308%)
Q30 bases: 5688358(90.2914%)

Read1 after filtering:
total reads: 49845
total bases: 6274526
Q20 bases: 6034120(96.1685%)
Q30 bases: 5795987(92.3733%)

Read2 after filtering:
total reads: 49845
total bases: 6271089
Q20 bases: 5960613(95.0491%)
Q30 bases: 5679945(90.5735%)

Filtering result:
reads passed filter: 99690
reads failed due to low quality: 308
reads failed due to too many N: 0
reads failed due to too short: 2
reads with adapter trimmed: 12
bases trimmed due to adapters: 606

Duplication rate: 0.002%

Insert size peak (evaluated by paired-end reads): 143
...
```

</div>

خواندن گزارش، از بالا:
- **آداپتور:** توالی آداپتوری یافت نشد (داده شبیه‌سازی‌شده است)؛ ولی ۱۲ رید از راه هم‌پوشانی بریده شدند.
- ‏**Q30:** ‏R1 ‏۹۲٫۳٪ و R2 ‏۹۰٫۳٪؛ R2 کمی بدتر است، چنان‌که در درس ۱ دیدیم.
- **پس از پالایش:** ۴۹٬۸۴۵ رید در **هر دو** فایل: جفت‌ها با هم مانده‌اند.
- ‏**Filtering result:** شمارش ریدهای **تکی** (R1 + R2): ۹۹٬۶۹۰ ماند، ۳۰۸ به‌خاطر کیفیت و ۲ به‌خاطر کوتاهی رفتند. 308 + 2 = 310 رید = ۱۵۵ جفت؛ 50000 − 155 = 49845. ✓
- ‏**Insert size peak 143:** درازای رایج قطعه‌ی DNA؛ از روی هم‌پوشانی دو رید ۱۲۶ بازی برآورد شده است.

> 📺 **فیلم:** *How to run fastp for trimming, filtering, and reports*: https://www.youtube.com/watch?v=zgQ6b0AerKQ (profbiot)
> 📄 **مرجع:** Chen S, et al. (2018). *fastp.* Bioinformatics 34:i884–i890. https://doi.org/10.1093/bioinformatics/bty560

---

## ۴. گام ۲: چرا این راهبرد؟ سه راهبرد را بسنجید

همان ریدها، سه دستور:

<div dir="ltr">

```bash
mkdir -p qc/compare
R=raw; s=minigut; T=qc/compare

# A) filtering only (the common "fastp -q 20")
fastp -i $R/${s}_R1.fastq.gz -I $R/${s}_R2.fastq.gz -o $T/A_R1.fq.gz -O $T/A_R2.fq.gz \
      -q 20 -l 36 -j $T/A.json -h $T/A.html 2> $T/A.log

# B) sliding window from 5' (= Trimmomatic SLIDINGWINDOW:4:20)
fastp -i $R/${s}_R1.fastq.gz -I $R/${s}_R2.fastq.gz -o $T/B_R1.fq.gz -O $T/B_R2.fq.gz \
      --detect_adapter_for_pe --cut_right --cut_mean_quality 20 -l 50 \
      -j $T/B.json -h $T/B.html 2> $T/B.log

# C) trim both ends (the course choice, as in step 1)
fastp -i $R/${s}_R1.fastq.gz -I $R/${s}_R2.fastq.gz -o $T/C_R1.fq.gz -O $T/C_R2.fq.gz \
      --detect_adapter_for_pe --cut_front --cut_tail --cut_mean_quality 20 -l 50 \
      -j $T/C.json -h $T/C.html 2> $T/C.log

grep -H 'reads passed filter\|too short' $T/*.log
```

</div>

- ‏`R=raw; s=minigut; T=qc/compare`: متغیرها (بخش ۰۱، ماژول ۰۹) دستورها را کوتاه می‌کنند.
- ‏`2> $T/A.log`: گزارش صفحه‌ی fastp (که در stderr است) به فایل می‌رود.
- ‏`grep -H`: نام فایل را هم پیش از هر خط یافته‌شده چاپ کن؛ `\|` یعنی «یا».

<div dir="ltr">

```text
qc/compare/A.log:reads passed filter: 99594
qc/compare/A.log:reads failed due to too short: 0
qc/compare/B.log:reads passed filter: 89176
qc/compare/B.log:reads failed due to too short: 10734
qc/compare/C.log:reads passed filter: 99690
qc/compare/C.log:reads failed due to too short: 2
```

</div>

با عددهای دیگر گزارش JSON (گام ۴)، روی هم (ورودی: ۱۰۰٬۰۰۰ رید تکی، ۱۲٫۶ میلیون باز، Q30 ‏۹۱٫۲۹٪):

| راهبرد | ریدهای مانده | بازهای مانده | ‏Q30 پس از آن | رفته: کوتاه | رفته: کیفیت |
| :--- | ---: | ---: | :-: | ---: | ---: |
| ‏A: `-q 20` (تنها پالایش) | 99,594 (99.6%) | 12,548,238 | 91.40% | 0 | 406 |
| ‏B: `--cut_right` | **89,176 (89.2%)** | **11,110,072 (88.2%)** | 94.47% | **10,734** | 90 |
| ‏C: `--cut_front --cut_tail` | 99,690 (99.7%) | 12,545,615 | 91.47% | 2 | 308 |

### تفسیر

- ‏**A** هیچ بازی را نبرید. ۴۰۶ رید رفتند چون بیش از ۴۰٪ بازهایشان زیر Q20 بود؛ Q30 کمابیش همان ماند. اگر می‌خواستید انتهای بد بریده شود، **این دستور آن کار را نمی‌کند**.
- ‏**B** بالاترین Q30 را دارد، ولی به بهای **۱۰٫۸٪ ریدها و ۱۱٫۸٪ بازها**. چرا؟ در گام ۳ درس ۱ دیدید که بازهای کم‌کیفیت این داده **پراکنده در میانه‌ی ریدها**یند. شمارش با awk (بخش ۰۱):

  <div dir="ltr">

  ```bash
  zcat raw/minigut_R1.fastq.gz | awk 'NR%4==0 {q=substr($0,1,60); if (q ~ /[!-4]/) c++; n++} END {print c, n, c/n}'
  ```

  </div>

  <div dir="ltr">

  ```text
  27602 50000 0.55204
  ```

  </div>

  ‏`substr($0,1,60)` = شصت باز نخست خط کیفیت؛ `/[!-4]/` = هر نویسه از `!` تا `4`، یعنی Q0 تا Q19. **۵۵٪ ریدها** در ۶۰ باز نخستشان دست‌کم یک باز زیر Q20 دارند. `--cut_right` با هر افت موضعی که میانگین پنجره‌ی ۴تایی را زیر ۲۰ ببرد، **همه‌ی باقی رید** را می‌بُرد؛ بسیاری از ریدها زیر ۵۰ باز می‌روند و با `-l 50` دور ریخته می‌شوند. **بالا رفتن Q30 ساختگی است:** داده را بهتر نکردیم، بخش بزرگی از آن را دور ریختیم.
- ‏**C** دو انتهای بد را می‌بُرد، بازهای بد پراکنده‌ی میانه را نگه می‌دارد (ابزارهای همترازی و طبقه‌بندی با یک باز Q14 در میانه‌ی رید مشکلی ندارند) و ۹۹٫۷٪ داده را نگه می‌دارد.

**تصمیم این دوره:** راهبرد C، با `-l 50`. چرا ۵۰؟ ریدهای بسیار کوتاه در طبقه‌بندی k-mer (Kraken2 با k=35، ماژول ۰۳) و همترازی، جاهای نادرست بسیاری پیدا می‌کنند.

> این یک قانون همگانی نیست. روی داده‌ای که تنها انتهای ۳' بدی دارد، B و C نتیجه‌ی نزدیکی می‌دهند (تمرین ۳). **درس اصلی:** پارامتر را با داده‌ی خودتان و گزارش fastp برگزینید، نه با رونویسی از یک مقاله.

<details>
<summary>✋ امتحان کن: پنجره‌ی ۴تایی <code>F F / F</code> (۳۷، ۳۷، ۱۴، ۳۷) را <code>--cut_right</code> می‌بُرد؟ و <code>/ / 7 &lt;</code> (۱۴، ۱۴، ۲۲، ۲۷)؟</summary>

- ‏(37 + 37 + 14 + 37) / 4 = **31.25**؛ بالای ۲۰، پس نه.
- ‏(14 + 14 + 22 + 27) / 4 = **19.25**؛ زیر ۲۰، پس از همین‌جا تا پایان رید بریده می‌شود.

یک `/` تنها کاری نمی‌کند؛ یک خوشه‌ی کوچک بازهای متوسط کافی است. تمرین ۴ اثر پهن‌تر کردن پنجره را می‌سنجد.

</details>

---

## ۵. گام ۳: جفت‌ها هنوز جفت‌اند؟

ابزارهای بعدی (Bowtie2 در ماژول ۰۲) فرض می‌کنند رید شماره‌ی n در R1 با رید شماره‌ی n در R2 جفت است. در حالت جفتی، fastp اگر یکی از دو رید را دور بیندازد، **جفتش را هم** دور می‌اندازد:

<div dir="ltr">

```bash
for r in R1 R2; do
  printf "%s: " $r
  zcat qc/trimmed/minigut_${r}.fastq.gz | awk 'END {print NR/4}'
done
```

</div>

<div dir="ltr">

```text
R1: 49845
R2: 49845
```

</div>

برابرند. اگر R1 و R2 را با **دو دستور جدا** می‌بریدید، رید دورریخته‌شده‌ی R1 در R2 می‌ماند و از آن نقطه همه‌ی جفت‌ها جابه‌جا می‌شدند (اشتباه رایج ۲).

---

## ۶. گام ۴: خواندن گزارش JSON با پایتون

گزارش HTML برای چشم است؛ برای جدول یک مقاله با ۲۰۰ نمونه، عددها را از **JSON** برمی‌داریم. JSON (بخش ۰۲، ماژول ۰۵) همان **دیکشنری‌های تودرتوی** پایتون (بخش ۰۳) است، و ماژول `json` پایتون آن را مستقیم به دیکشنری تبدیل می‌کند:

<div dir="ltr">

```python
# fastp_summary.py: a few numbers from one fastp JSON report
import json

with open("qc/fastp/minigut.json") as f:
    report = json.load(f)                       # ①

print(report.keys())                            # ②
before = report["summary"]["before_filtering"]["total_reads"]   # ③
after = report["summary"]["after_filtering"]["total_reads"]
print(before, after, round(after / before * 100, 2))
print(report["filtering_result"])               # ④
```

</div>

<div dir="ltr">

```bash
python3 fastp_summary.py
```

</div>

<div dir="ltr">

```text
dict_keys(['summary', 'filtering_result', 'duplication', 'insert_size', 'adapter_cutting', 'read1_before_filtering', 'read2_before_filtering', 'read1_after_filtering', 'read2_after_filtering', 'command'])
100000 99690 99.69
{'passed_filter_reads': 99690, 'low_quality_reads': 308, 'too_many_N_reads': 0, 'too_short_reads': 2, 'too_long_reads': 0}
```

</div>

| نشانه | کار |
| :---: | :--- |
| ① | ‏`json.load(f)` همه‌ی فایل را می‌خواند و یک **دیکشنری** برمی‌گرداند. |
| ② | کلیدهای سطح بالا: نقشه‌ی گزارش. `summary` و `filtering_result` همان بخش‌های گزارش صفحه‌اند. |
| ③ | دو کلید پشت سر هم = یک سطح پایین‌تر: «در `summary`، در `before_filtering`، `total_reads`». |
| ④ | یک دیکشنری درونی، کامل؛ همان «Filtering result» صفحه. |

تمرین ۶ همین را برای همه‌ی نمونه‌ها در یک جدول TSV می‌خواهد.

---

## ۷. گام ۵: همه‌ی نمونه‌ها، و QC دوباره

### ۷.۱ یک اسکریپت

برای هر دو نمونه، همان دستور گام ۱ در یک حلقه، و سپس FastQC و MultiQC **پس از** بریدن. اسکریپت کامل: [`99_scripts_data/01_Read_QC_Trimming/scripts/run_qc.sh`](../99_scripts_data/01_Read_QC_Trimming/scripts/run_qc.sh). هسته‌ی آن:

<div dir="ltr">

```bash
for r1 in raw/*_R1.fastq.gz; do
  s=$(basename $r1 _R1.fastq.gz)
  fastp -i $r1 -I raw/${s}_R2.fastq.gz \
        -o qc/trimmed/${s}_R1.fastq.gz -O qc/trimmed/${s}_R2.fastq.gz \
        --detect_adapter_for_pe --cut_front --cut_tail --cut_mean_quality 20 \
        --length_required 50 --thread 4 \
        -j qc/fastp/${s}.json -h qc/fastp/${s}.html 2> qc/fastp/${s}.log
done
fastqc -q -t 4 -o qc/fastqc_trimmed qc/trimmed/*.fastq.gz
multiqc qc/fastqc_trimmed qc/fastp -o qc/multiqc_trimmed
```

</div>

- ‏`basename $r1 _R1.fastq.gz`: ‏`raw/minigut_R1.fastq.gz` ← `minigut` (نام نمونه).
- حلقه **روی R1** می‌چرخد و نام R2 را از نام نمونه می‌سازد، تا هر نمونه یک بار پردازش شود.
- ‏MultiQC اکنون **دو** پوشه می‌گردد: گزارش‌های FastQC و fastp در یک صفحه.

### ‏۷.۲ ‏FastQC پس از بریدن

با حلقه‌ی بخش ۵.۳ درس ۱، این بار روی `qc/fastqc_trimmed`:

<div dir="ltr">

```text
== minigut_R1_fastqc
WARN	Sequence Length Distribution	minigut_R1.fastq.gz
== minigut_R2_fastqc
WARN	Sequence Length Distribution	minigut_R2.fastq.gz
== minigut_sample2_R1_fastqc
FAIL	Per sequence GC content	minigut_sample2_R1.fastq.gz
WARN	Sequence Length Distribution	minigut_sample2_R1.fastq.gz
== minigut_sample2_R2_fastqc
FAIL	Per sequence GC content	minigut_sample2_R2.fastq.gz
WARN	Sequence Length Distribution	minigut_sample2_R2.fastq.gz
```

</div>

- ‏**‏WARN طول، منتظره است:** پس از بریدن، ریدها دیگر یک طول ندارند. FastQC این را «غیرعادی» می‌شمارد.
- ‏**‏FAIL در GC همان FAIL خوب درس ۱ است:** ترکیب جامعه با بریدن عوض نشده است.

### ۷.۳ همان کار با Snakemake

این ماژول سه گام دارد که برای هر نمونه تکرار می‌شوند: همان چیزی که Snakemake (بخش ۰۵) برایش ساخته شده است. Snakefile آماده: [`99_scripts_data/01_Read_QC_Trimming/workflow/`](../99_scripts_data/01_Read_QC_Trimming/workflow/). قاعده‌ی fastp آن:

<div dir="ltr">

```python
rule fastp:
    input:
        r1="raw/{sample}_R1.fastq.gz",
        r2="raw/{sample}_R2.fastq.gz",
    output:
        r1="qc/trimmed/{sample}_R1.fastq.gz",
        r2="qc/trimmed/{sample}_R2.fastq.gz",
        json="qc/fastp/{sample}.json",
        html="qc/fastp/{sample}.html",
    params:
        q=config["cut_mean_quality"],
        l=config["length_required"],
    threads: 4
    log:
        "logs/fastp/{sample}.log",
    shell:
        "fastp -i {input.r1} -I {input.r2} -o {output.r1} -O {output.r2} "
        "--detect_adapter_for_pe --cut_front --cut_tail --cut_mean_quality {params.q} "
        "--length_required {params.l} --thread {threads} "
        "-j {output.json} -h {output.html} > {log} 2>&1"
```

</div>

همه‌ی ابزارهای این قاعده را در بخش ۰۵ دیده‌اید: ورودی و خروجی نام‌دار، `params` از `config.yaml`، `log`. تنها تازه‌اش `threads: 4` است که `{threads}` را در دستور پر می‌کند (کادر کنجکاوهای ماژول 05/04). با دو نمونه، `snakemake -n` این کارها را نشان می‌دهد:

<div dir="ltr">

```text
Job stats:
job               count
--------------  -------
fastp                 2
fastqc_raw            4
fastqc_trimmed        4
multiqc               1
all                   1
total                12
```

</div>

‏(این جدول از اجرای 2026-10-14 همین گردش کار است.) `fastqc_raw` ۴ بار: ۲ نمونه × ۲ رید، با دو wildcard `{sample}` و `{read}`.

> 📺 **فیلم:** *Using MultiQC Reports*: https://www.youtube.com/watch?v=qPbIlO_KWN0 (Phil Ewels)
> 📄 **مرجع:** MultiQC documentation: https://docs.seqera.io/multiqc

---

## ۸. سه اشتباه رایج

‏**۱. ‏`-q 20` را «بریدن» پنداشتن.** دیدید (راهبرد A) که هیچ بازی بریده نشد و Q30 تنها ۹۱٫۲۹ ← ۹۱٫۴۰ شد. برای بریدن: `--cut_tail` (و اگر لازم بود `--cut_front`).

**۲. بریدن R1 و R2 با دو دستور جدا.** شمار ریدها نابرابر می‌شود و جفت‌ها به هم می‌ریزند. Bowtie2 (ماژول ۰۲) با شمار نابرابر می‌ایستد:

<div dir="ltr">

```text
Error, fewer reads in file specified with -2 than in file specified with -1
```

</div>

بدتر: اگر شمارها از بخت بد برابر بمانند ولی ترتیب به هم بخورد، **هیچ پیام خطایی** نمی‌آید و ریدهای بی‌ربط جفت پنداشته می‌شوند. همیشه R1 و R2 را با هم به fastp بدهید (`-i` و `-I`).

**۳. رونویسی `SLIDINGWINDOW:4:20` یا `--cut_right` از یک مقاله.** روی این داده، ۱۰٫۸٪ ریدها را بی‌دلیل دور ریخت. پیش از برگزیدن، دست‌کم دو راهبرد را روی داده‌ی خودتان بسنجید و درصد مانده را گزارش کنید.

---

## 📘 برای کنجکاوها

- ‏**‏`--dedup`:** ‏fastp می‌تواند ریدهای تکراری را بردارد؛ در متاژنوم Shotgun بی دلیل روشن این کار را نکنید (فراوانی گونه‌های غالب کم برآورد می‌شود).
- **ریدهای بی‌جفت:** ‏`--unpaired1` / `--unpaired2` ریدهایی را که جفتشان دور ریخته شده، در فایل جدا نگه می‌دارند.
- **آداپتور معلوم:** اگر توالی آداپتور کیت را می‌دانید، `--adapter_sequence` و `--adapter_sequence_r2` از حدس زدن مطمئن‌ترند.
- **پوشش در MultiQC:** گزارش MultiQC این ماژول ستون `fastp-pct_surviving` (درصد ریدهای مانده) را هم در جدول کلی دارد؛ همان عدد `99.69`.

---

## جمع‌بندی

- ‏fastp سه کار جدا دارد: بریدن آداپتور، **بریدن** کیفیت (`--cut_*`) و **پالایش** کیفیت (`-q/-u/-n/-l`). `-q` هیچ بازی نمی‌بُرد.
- ‏`--cut_right` با افت‌های موضعی کیفیت تند است؛ روی داده‌ی ما ۱۰٫۸٪ ریدها را دور ریخت.
- راهبرد این دوره: `--detect_adapter_for_pe --cut_front --cut_tail --cut_mean_quality 20 -l 50`؛ ۹۹٫۷٪ داده می‌ماند و جفت‌ها جفت می‌مانند.
- گزارش JSON = دیکشنری تودرتو؛ با `json.load` در پایتون.
- پس از بریدن دوباره QC کنید و شمار و **دلیل** حذف را گزارش دهید.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
fastp -i R1.fq.gz -I R2.fq.gz -o out_R1.fq.gz -O out_R2.fq.gz \
      --detect_adapter_for_pe --cut_front --cut_tail --cut_mean_quality 20 \
      --length_required 50 --thread 4 -j s.json -h s.html 2> s.log
grep -H 'reads passed filter\|too short' qc/compare/*.log
zcat out_R1.fq.gz | awk 'END {print NR/4}'          # read count; R1 must equal R2
multiqc qc/fastqc_trimmed qc/fastp -o qc/multiqc_trimmed
```

</div>

<div dir="ltr">

```python
import json
with open("qc/fastp/minigut.json") as f:
    report = json.load(f)
report["summary"]["after_filtering"]["total_reads"]
report["filtering_result"]["too_short_reads"]
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| بریدن (*trimming*) | برداشتن **بازهای** بد از سر یا ته رید |
| پالایش (*filtering*) | دور ریختن **کل رید** (و جفتش) |
| پنجره‌ی لغزان | چند باز پشت سر هم که میانگین کیفیتشان سنجیده می‌شود |
| ‏Q30 rate | سهم بازهایی که کیفیت ۳۰ یا بیشتر دارند |
| ‏Insert size | درازای قطعه‌ی DNA میان دو آداپتور |
| ‏JSON | قالب متنی داده‌ی تودرتو؛ در پایتون = دیکشنری |

---

## منابع

**مستند و مقاله**
- Chen S, et al. (2018). *fastp: an ultra-fast all-in-one FASTQ preprocessor.* Bioinformatics 34(17):i884–i890. https://doi.org/10.1093/bioinformatics/bty560
- Chen S (2023). *Ultrafast one-pass FASTQ data preprocessing, quality control, and deduplication using fastp.* iMeta 2:e107. https://doi.org/10.1002/imt2.107
- fastp documentation and code: https://github.com/OpenGene/fastp
- Python documentation, *json — JSON encoder and decoder*: https://docs.python.org/3/library/json.html

**کتاب**
- ‏Wang X (2016). *Next-Generation Sequencing Data Analysis*. CRC Press. (فصل پیش‌پردازش و برش ریدها)

**فیلم و دوره‌ی آموزشی**
- Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins University): https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Linux* (The Linux Foundation). دوره‌ای ویژه‌ی بریدن ریدها در edX نیافتیم؛ نزدیک‌ترین: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux
- YouTube: *How to run fastp for trimming, filtering, and reports* (profbiot): https://www.youtube.com/watch?v=zgQ6b0AerKQ
- YouTube: *GTN Training: Intro to NGS – Quality Control (Tutorial)* (Galaxy Project): https://www.youtube.com/watch?v=QJRlX2hWDKM
- YouTube: *Using MultiQC Reports* (Phil Ewels): https://www.youtube.com/watch?v=qPbIlO_KWN0

<sub>نشانی‌های YouTube و DOIها در 2026-10-12 وارسی شدند. وارسی دوباره‌ی همه‌ی نشانی‌ها در پایان دوره انجام می‌شود.</sub>

</div>
