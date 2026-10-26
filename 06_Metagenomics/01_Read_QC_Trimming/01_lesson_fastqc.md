<div dir="rtl">

# درس ۱: آیا ریدها سالم‌اند؟ FastQC و MultiQC

**بخش:** `06_Metagenomics` · **ماژول:** `01_Read_QC_Trimming` · **پیش‌نیاز:** بخش‌های ۰۱ تا ۰۵ (به‌ویژه [فرمت FASTQ و کیفیت Phred](../../02_BioLinux/02_Sequence_Formats/)) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** FastQC 0.12.1، MultiQC 1.25.1 · **خروجی‌ها از اجرای:** 2026-10-12

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. ‏FastQC را روی فایل‌های FASTQ اجرا کنید و بدانید چه فایل‌هایی می‌سازد.
2. خلاصه‌ی PASS / WARN / FAIL را بی باز کردن مرورگر، از خط فرمان بخوانید.
3. هر نمودار FastQC را **برای داده‌ی متاژنوم** تفسیر کنید: کدام FAIL مشکل است و کدام نه.
4. با MultiQC گزارش همه‌ی نمونه‌ها را در یک صفحه کنار هم ببینید.

**پیش از آغاز:** محیط conda این بخش را یک بار بسازید (روش ساختن محیط از فایل: بخش ۰۲، ماژول ۰۱) و یک پوشه‌ی پروژه با ریدهای بخش ۰۱ آماده کنید:

<div dir="ltr">

```bash
C=~/Bioinformatics_Learning-main
conda env create -f $C/envs/metagenomics.yml      # once
conda activate metagenomics
mkdir -p ~/meta && cd ~/meta
cp -r $C/01_Linux/99_scripts_data/data/fastq raw
ls raw
```

</div>

در `raw/` چهار فایل هست: `minigut_R1.fastq.gz`، `minigut_R2.fastq.gz`، `minigut_sample2_R1.fastq.gz` و `minigut_sample2_R2.fastq.gz`. همه‌ی درس‌های این بخش در `~/meta` کار می‌کنند و هر ماژول پوشه‌ی خودش را می‌سازد (`qc/`، `host/`، `profile/`).

<div dir="ltr">

```bash
fastqc --version
multiqc --version
```

</div>

<div dir="ltr">

```text
FastQC v0.12.1
multiqc, version 1.25.1
```

</div>

---

## ۱. داستان

مرکز توالی‌یابی چهار فایل FASTQ برایتان فرستاده است: دو نمونه‌ی مدفوع، هر کدام با R1 و R2. پیش از هر تحلیلی باید به یک پرسش پاسخ دهید:

> **آیا این داده برای پرسش من سالم و کافی است؟ اگر نه، چه چیزی باید بریده یا دور ریخته شود؟**

اگر این پرسش را نپرسید، خطای توالی‌یابی بعداً به شکل «باکتری تازه» یا «جهش تازه» در نتیجه‌ها پیدا می‌شود. این درس **ارزیابی** است (چه مشکلی هست؟). درس ۲ **درمان** است (بریدن و دور ریختن با fastp).

---

## ۲. مفهوم به زبان ساده

### ۲.۱ سه گونه مشکل

| گونه | نمونه | از کجا می‌آید |
| :--- | :--- | :--- |
| فنی (دستگاه) | افت کیفیت در انتهای ریدها، باز `N`، خرابی یک چرخه (*cycle*) | شیمی و نوری دستگاه |
| کتابخانه | آداپتور در انتهای رید، دایمر پرایمر، تکرار PCR | آماده‌سازی نمونه در آزمایشگاه |
| نمونه | آلودگی، ترکیب نامنتظره | خود نمونه‌ی زیستی |

### ۲.۲ یادآوری: کیفیت Phred

در بخش ۰۲ دیدید که خط چهارم هر رکورد FASTQ، برای هر باز یک نویسه دارد که **احتمال خطا** را می‌گوید:

| نویسه | Q | احتمال خطا |
| :---: | :---: | :---: |
| `5` | 20 | ۱ در ۱۰۰ |
| `?` | 30 | ۱ در ۱۰۰۰ |
| `F` | 37 | کمابیش ۱ در ۵۰۰۰ |
| `/` | 14 | کمابیش ۱ در ۲۵ |

### ۲.۳ نکته‌ی کلیدی این درس

‏FastQC برای **ژنوم یک گونه** ساخته شده است. مرزهای PASS / WARN / FAIL آن همین فرض را دارند. در متاژنوم، که ده‌ها گونه با هم‌اند، برخی FAILها **انتظار می‌روند** و نشانه‌ی خرابی نیستند. مهارت اصلی این درس جدا کردن این دو است.

---

## ۳. نگاه با چشم، پیش از هر ابزاری

<div dir="ltr">

```bash
zcat raw/minigut_R1.fastq.gz | head -n 4
```

</div>

<div dir="ltr">

```text
@NC_006347.1_0/1
AACGTTGGCTCGTCTGACAAGCAAAGGTAAGAACAAAGGTGCCAAATATCGTAAAGAAAAACGTGACATGGCGTCCAACC...
+
BBBBBFFFFFFFFFFFFFFFFFF/FFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF...
```

</div>

‏(خط‌ها برای پهنای صفحه کوتاه شده‌اند: `...`.)

- بیشتر بازها `F` (Q37) و چند تا `B` (Q33) هستند: کیفیت خوب.
- یک `/` (Q14) **در میانه‌ی رید** است، نه در انتها. این نکته در درس ۲ تعیین‌کننده می‌شود.
- نام رید (`NC_006347.1`) ژنوم مبدأ را می‌گوید؛ این داده شبیه‌سازی‌شده است و پاسخ درستش را داریم (بخش ۰۱).

ولی چشم برای ۵۰٬۰۰۰ رید کار نمی‌کند. FastQC همین نگاه را برای همه‌ی ریدها انجام می‌دهد و نمودار می‌کشد.

---

## ۴. گام ۱: FastQC روی یک فایل

<div dir="ltr">

```bash
mkdir -p qc/fastqc_raw
fastqc -q -o qc/fastqc_raw raw/minigut_R1.fastq.gz
ls qc/fastqc_raw
```

</div>

<div dir="ltr">

```text
minigut_R1_fastqc.html  minigut_R1_fastqc.zip
```

</div>

| بخش | چیست | بی آن چه می‌شود |
| :--- | :--- | :--- |
| ① `fastqc` | نام ابزار | — |
| ② `-q` | آرام (*quiet*): پیام‌های پیشرفت (`Approx 5% complete…`) چاپ نشوند | صفحه پر از پیام درصد پیشرفت می‌شود؛ نتیجه همان است |
| ③ `-o qc/fastqc_raw` | پوشه‌ی خروجی؛ باید **از پیش** ساخته شده باشد (`mkdir -p`) | گزارش‌ها کنار فایل ورودی، در `raw/`، نوشته می‌شوند |
| ④ `raw/minigut_R1.fastq.gz` | فایل ورودی؛ FastQC فایل `.gz` را مستقیم می‌خواند | — |

دو خروجی برای هر فایل:
- ‏**`_fastqc.html`**: گزارش با نمودارها؛ با مرورگر باز کنید (برای نمونه، در WSL با `explorer.exe qc/fastqc_raw/minigut_R1_fastqc.html`، یا با کشیدن فایل به پنجره‌ی مرورگر).
- ‏**`_fastqc.zip`**: همان گزارش به شکل **متن**؛ برای خواندن با خط فرمان. گام بعد.

### همه‌ی فایل‌ها با یک دستور

<div dir="ltr">

```bash
fastqc -q -t 4 -o qc/fastqc_raw raw/*.fastq.gz
ls qc/fastqc_raw
```

</div>

- ‏`raw/*.fastq.gz`: هر چهار فایل (wildcard پوسته، بخش ۰۱).
- ‏`-t 4`: چهار فایل **هم‌زمان** (*threads*). هر کدام کمابیش ۲۵۰ مگابایت حافظه می‌خواهد؛ روی لپ‌تاپ کم‌حافظه `-t 2` بزنید.

اکنون هشت فایل در `qc/fastqc_raw/` هست: یک `.html` و یک `.zip` برای هر FASTQ.

> 📺 **فیلم:** *Using FastQC to check the quality of high throughput sequence*: https://www.youtube.com/watch?v=bz93ReOv87Y (Babraham Bioinformatics)
> 📄 **مرجع:** FastQC: https://www.bioinformatics.babraham.ac.uk/projects/fastqc/

---

## ۵. گام ۲: خواندن خلاصه از خط فرمان

### ۵.۱ درون فایل zip چیست؟

ابزار **`unzip`** (همراه لینوکس) فایل zip را باز می‌کند. با `-l` (*list*) تنها **فهرست** درونش را نشان می‌دهد:

<div dir="ltr">

```bash
unzip -l qc/fastqc_raw/minigut_R1_fastqc.zip | head -n 12
```

</div>

<div dir="ltr">

```text
Archive:  qc/fastqc_raw/minigut_R1_fastqc.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
        0  2026-10-12 22:12   minigut_R1_fastqc/
        0  2026-10-12 22:12   minigut_R1_fastqc/Icons/
        0  2026-10-12 22:12   minigut_R1_fastqc/Images/
     1197  2026-10-12 22:12   minigut_R1_fastqc/Icons/fastqc_icon.png
     1450  2026-10-12 22:12   minigut_R1_fastqc/Icons/warning.png
     1561  2026-10-12 22:12   minigut_R1_fastqc/Icons/error.png
     1715  2026-10-12 22:12   minigut_R1_fastqc/Icons/tick.png
      489  2026-10-12 22:12   minigut_R1_fastqc/summary.txt
    68974  2026-10-12 22:12   minigut_R1_fastqc/Images/per_base_quality.svg
```

</div>

‏(تاریخ و ساعت شما دیگر خواهد بود.) دو فایل متنی مهم درون آن:
- ‏**`summary.txt`**: یک خط برای هر بخش گزارش: PASS، WARN یا FAIL.
- ‏**`fastqc_data.txt`**: عددهای پشت هر نمودار.

### ۵.۲ چاپ یک فایل از درون zip

<div dir="ltr">

```bash
unzip -p qc/fastqc_raw/minigut_sample2_R1_fastqc.zip minigut_sample2_R1_fastqc/summary.txt
```

</div>

<div dir="ltr">

```text
PASS	Basic Statistics	minigut_sample2_R1.fastq.gz
PASS	Per base sequence quality	minigut_sample2_R1.fastq.gz
PASS	Per sequence quality scores	minigut_sample2_R1.fastq.gz
PASS	Per base sequence content	minigut_sample2_R1.fastq.gz
FAIL	Per sequence GC content	minigut_sample2_R1.fastq.gz
PASS	Per base N content	minigut_sample2_R1.fastq.gz
PASS	Sequence Length Distribution	minigut_sample2_R1.fastq.gz
PASS	Sequence Duplication Levels	minigut_sample2_R1.fastq.gz
PASS	Overrepresented sequences	minigut_sample2_R1.fastq.gz
PASS	Adapter Content	minigut_sample2_R1.fastq.gz
```

</div>

| بخش | چیست |
| :--- | :--- |
| ① `unzip -p` | فایل را به **خروجی** (*pipe*) بفرست، نه روی دیسک؛ هیچ پوشه‌ای ساخته نمی‌شود |
| ② نشانی zip | فایل zip |
| ③ `minigut_sample2_R1_fastqc/summary.txt` | نشانی فایل **درون** zip، همان که `unzip -l` نشان داد |

ده بخش، نه تا PASS و یک FAIL. چون خروجی به pipe می‌رود، `grep` و `cut` بخش ۰۱ روی آن کار می‌کنند.

### ۵.۳ همه‌ی فایل‌ها: تنها آنچه PASS نیست

ساختن گام‌به‌گام: نخست برای یک فایل، با `grep -v` (خط‌هایی که الگو را **ندارند**):

<div dir="ltr">

```bash
unzip -p qc/fastqc_raw/minigut_sample2_R1_fastqc.zip minigut_sample2_R1_fastqc/summary.txt | grep -v PASS
```

</div>

<div dir="ltr">

```text
FAIL	Per sequence GC content	minigut_sample2_R1.fastq.gz
```

</div>

سپس با یک حلقه (بخش ۰۱، ماژول ۰۹) برای هر چهار فایل. مشکل: نام پوشه‌ی درون zip برای هر فایل فرق می‌کند. `basename` (همان ماژول) آن را از نام zip درمی‌آورد:

<div dir="ltr">

```bash
for z in qc/fastqc_raw/*_fastqc.zip; do
  n=$(basename $z .zip)
  echo "== $n"
  unzip -p $z $n/summary.txt | grep -v PASS
done
```

</div>

<div dir="ltr">

```text
== minigut_R1_fastqc
== minigut_R2_fastqc
== minigut_sample2_R1_fastqc
FAIL	Per sequence GC content	minigut_sample2_R1.fastq.gz
== minigut_sample2_R2_fastqc
FAIL	Per sequence GC content	minigut_sample2_R2.fastq.gz
```

</div>

| خط | کار |
| :--- | :--- |
| `for z in …zip` | ‏`z` به نوبت هر فایل zip |
| `n=$(basename $z .zip)` | ‏`qc/fastqc_raw/minigut_R1_fastqc.zip` ← `minigut_R1_fastqc` (پوشه و پسوند برداشته می‌شوند) |
| `unzip -p $z $n/summary.txt` | خلاصه‌ی همان فایل |
| `grep -v PASS` | تنها WARN و FAIL |

نمونه‌ی `minigut` همه PASS است. `minigut_sample2` تنها یک FAIL دارد، در **GC**. بخش ۷ می‌گوید چرا این خبر بدی نیست.

<details>
<summary>✋ امتحان کن: اگر <code>grep -v PASS</code> را بردارید، حلقه چند خط چاپ می‌کند؟</summary>

برای هر فایل ۱ خط `==` و ۱۰ خط خلاصه: 4 × 11 = **۴۴ خط**.

</details>

---

## ۶. گام ۳: عددهای پشت یک نمودار

بخش «Per base sequence quality» می‌گوید کیفیت در **هر جایگاه** رید چقدر است. عددهایش در `fastqc_data.txt` است. `grep -A 7` (بخش ۰۱، ماژول ۰۵) خط یافته‌شده و ۷ خط پس از آن را می‌دهد:

<div dir="ltr">

```bash
unzip -p qc/fastqc_raw/minigut_R1_fastqc.zip minigut_R1_fastqc/fastqc_data.txt \
  | grep -A 7 '>>Per base sequence quality'
```

</div>

<div dir="ltr">

```text
>>Per base sequence quality	pass
#Base	Mean	Median	Lower Quartile	Upper Quartile	10th Percentile	90th Percentile
1	32.37272	33.0	33.0	33.0	33.0	33.0
2	32.43406	33.0	33.0	33.0	33.0	33.0
3	32.4528	33.0	33.0	33.0	33.0	33.0
4	32.42046	33.0	33.0	33.0	33.0	33.0
5	32.46712	33.0	33.0	33.0	33.0	33.0
6	36.07446	37.0	37.0	37.0	33.0	37.0
```

</div>

و پایان جدول (همان بخش، سه خط آخر پیش از `>>END_MODULE`):

<div dir="ltr">

```text
124-125	33.86825	37.0	33.0	37.0	22.0	37.0
126	30.46064	33.0	27.0	37.0	14.0	37.0
>>END_MODULE
```

</div>

- ستون ۲ (`Mean`) میانگین کیفیت در آن جایگاه است: از ۳۲٫۴ در آغاز، به ۳۶ در میانه، و ۳۰٫۵ در **آخرین** باز.
- ستون «10th Percentile» در جایگاه ۱۲۶ برابر ۱۴ است: یک‌دهم ریدها در آخرین بازشان کیفیت ۱۴ یا کمتر دارند.
- ‏FastQC جایگاه‌های پایانی را گروه می‌کند (`124-125`) تا جدول کوتاه بماند.

**تفسیر:** افت کیفیت در انتهای ۳' در Illumina **طبیعی** است: پس از صدها چرخه‌ی شیمیایی، رشته‌های یک خوشه از هم‌گامی بیرون می‌روند. تا وقتی میانگین بالای ۲۸ است، FastQC آن را PASS می‌داند. افت **ناگهانی در میانه‌ی رید**، در همه‌ی ریدها، نشانه‌ی خرابی دستگاه است.

---

## ۷. گام ۴: تفسیر بخش‌های FastQC برای متاژنوم

| بخش FastQC | چه می‌سنجد | در متاژنوم | داده‌ی ما |
| :--- | :--- | :--- | :--- |
| Basic Statistics | شمار رید، طول، ‏%GC، کدگذاری | — | ‏`minigut`: ۵۰٬۰۰۰ رید، ۱۲۶ باز، GC ۴۶٪، `Sanger / Illumina 1.9` (یعنی Phred+33) |
| Per base sequence quality | کیفیت در هر جایگاه | افت آرام در انتها طبیعی است | PASS |
| Per sequence quality scores | میانگین کیفیت هر رید | دنباله‌ی کوچکی از ریدهای بد طبیعی است | PASS |
| Per base sequence content | سهم A/C/G/T در هر جایگاه | در کتابخانه‌های Nextera، ۱۰ تا ۱۵ باز نخست سوگیری دارند (FAIL منتظره) | PASS |
| **Per sequence GC content** | پراکنش GC ریدها در برابر منحنی زنگوله‌ای | **چندقله‌ای طبیعی است**: هر گونه GC خودش را دارد | ‏**FAIL در نمونه‌ی ۲** (پایین) |
| Per base N content | سهم `N` در هر جایگاه | باید نزدیک صفر باشد | PASS |
| Sequence Length Distribution | پراکنش طول | داده‌ی خام یک طول دارد؛ پس از بریدن WARN طبیعی است | PASS |
| Sequence Duplication Levels | سهم توالی‌های تکراری | گونه‌های بسیار فراوان، ریدهای «تکراری» طبیعی می‌سازند | PASS |
| Overrepresented sequences | توالی‌های بسیار فراوان | آداپتور، دایمر، PhiX؛ یا یک ویروس بسیار فراوان | PASS |
| Adapter Content | سهم ریدهای دارای آداپتور | اگر بالا رود، باید بریده شود (درس ۲) | PASS |

### چرا GC نمونه‌ی ۲ «FAIL» است، و چرا این خبر خوبی است

پراکنش GC ریدها در `fastqc_data.txt` ۱۰۱ خط دارد (GC صفر تا ۱۰۰ درصد). با awk (بخش ۰۱) تنها هر ۵ درصد را، از ۱۵ تا ۸۵، کنار هم چاپ می‌کنیم:

<div dir="ltr">

```bash
unzip -p qc/fastqc_raw/minigut_sample2_R1_fastqc.zip minigut_sample2_R1_fastqc/fastqc_data.txt \
  | grep -A 102 '>>Per sequence GC' \
  | awk 'NR > 2 && $1 % 5 == 0 && $1 >= 15 && $1 <= 85 {printf "%s:%s  ", $1, $2} END {print ""}'
```

</div>

<div dir="ltr">

```text
15:10.5  20:71.0  25:197.0  30:539.0  35:1011.5  40:1324.5  45:984.0  50:354.0  55:116.5  60:77.0  65:108.0  70:109.0  75:50.0  80:10.5  85:1.0
```

</div>

| بخش دستور | کار |
| :--- | :--- |
| `grep -A 102 '>>Per sequence GC'` | سرآیند بخش + ۱۰۲ خط پس از آن (یک خط عنوان ستون‌ها و ۱۰۱ خط داده) |
| ‏`NR > 2` | دو خط سرآیند را رد کن |
| ‏`$1 % 5 == 0` | تنها GCهایی که بر ۵ بخش‌پذیرند (`%` = باقی‌مانده) |
| `printf "%s:%s  "` | ‏«GC:شمار» در یک خط، بی رفتن به خط تازه |
| `END {print ""}` | در پایان، یک خط تازه |

دو قله پیداست:
- قله‌ی اصلی در کمابیش **۴۰٪**.
- یک «شانه»ی دوم در **۶۵ تا ۷۰٪** (شمار از ۷۷ در GC ۶۰ دوباره بالا می‌رود تا ۱۰۹).

‏FastQC یک زنگوله‌ی تک‌قله‌ای انتظار دارد، پس FAIL می‌دهد. ولی پاسخ معلوم این نمونه (`ground_truth.tsv`، بخش ۰۱) دقیقاً همین را پیش‌بینی می‌کند:
- ‏*Acinetobacter baumannii* (GC کمابیش ۳۹٪) با ۶۴٫۶٪ ریدها **قله‌ی اصلی** را می‌سازد.
- ‏*Pseudomonas aeruginosa* (۶۶٫۶٪)، *Cereibacter sphaeroides* (۶۹٪)، *Deinococcus radiodurans* (۶۷٪) و *Cutibacterium acnes* (۶۰٪) با هم کمابیش ۷٪ ریدها را دارند و **شانه‌ی دوم** را می‌سازند.

**قاعده:** در متاژنوم، GC چندقله‌ای **اطلاعات** است، نه خطا؛ شکلش «اثر انگشت» ترکیب جامعه است. چیزی که باید نگرانتان کند، قله‌ی **تیز و باریک** نامنتظره است (آلودگی تک‌گونه یا دایمر آداپتور)، یا نمونه‌ای که شکل GC آن با هم‌گروه‌هایش بسیار فرق دارد (بخش ۸).

<details>
<summary>✋ امتحان کن: نمونه‌ی <code>minigut</code> از دو ژنوم است (GC کمابیش ۴۳ و ۵۱ درصد). چرا FastQC برای آن FAIL نمی‌دهد؟</summary>

دو قله‌ی پهن با مرکزهای **نزدیک** (فاصله‌ی کمابیش ۸ واحد) روی هم می‌افتند و یک قله‌ی پهن می‌سازند، که هنوز به زنگوله نزدیک است. GC هر رید ۱۲۶ بازی خودش چند درصد نوسان دارد. در نمونه‌ی ۲ فاصله‌ی دو گروه کمابیش ۲۷ واحد است، بیشتر از پهنای هر قله. (تمرین ۲ عددهای `minigut` را می‌خواهد.)

</details>

> 📺 **فیلم:** *GTN Training: Intro to NGS, Quality Control (Lecture)*: https://www.youtube.com/watch?v=BWonTPS4zB8 (Galaxy Project)
> 📄 **مرجع:** Galaxy Training, *Quality Control*: https://training.galaxyproject.org/

---

## ۸. گام ۵: همه‌ی نمونه‌ها در یک صفحه با MultiQC

با ۴ فایل، خواندن ۴ گزارش شدنی است؛ با ۲۰۰ نمونه نه. **MultiQC** پوشه‌ها را می‌گردد، گزارش هر ابزاری را که می‌شناسد پیدا می‌کند و همه را در **یک** صفحه کنار هم می‌گذارد.

<div dir="ltr">

```bash
multiqc qc/fastqc_raw -o qc/multiqc_raw
ls qc/multiqc_raw
```

</div>

<div dir="ltr">

```text
multiqc_data  multiqc_report.html
```

</div>

| بخش | چیست |
| :--- | :--- |
| ① `multiqc` | نام ابزار |
| ② `qc/fastqc_raw` | پوشه(هایی) که باید گشته شوند؛ می‌توانید چند پوشه بدهید |
| ③ `-o qc/multiqc_raw` | پوشه‌ی خروجی؛ MultiQC خودش آن را می‌سازد |

- ‏`multiqc_report.html`: گزارش؛ در مرورگر باز کنید. هر نمودار FastQC اکنون **چهار خط** دارد، یکی برای هر فایل؛ نمونه‌ی ناجور در یک نگاه پیداست.
- ‏`multiqc_data/`: همان عددها به شکل جدول متنی.

<div dir="ltr">

```bash
cut -f 1-3,6 qc/multiqc_raw/multiqc_data/multiqc_general_stats.txt
```

</div>

<div dir="ltr">

```text
Sample	fastqc-percent_duplicates	fastqc-percent_gc	fastqc-percent_fails
minigut_R1	1.3299999999999983	46.0	0.0
minigut_R2	1.2059999999999889	46.0	0.0
minigut_sample2_R1	0.2040571359980845	40.0	10.0
minigut_sample2_R2	0.15204257192013415	40.0	10.0
```

</div>

- ‏`percent_gc`: R1 و R2 هر نمونه **یک** GC دارند، چنان‌که باید (هر دو از یک قطعه‌ی DNA آمده‌اند). اگر R1 و R2 یک نمونه GC گوناگون داشتند، شاید فایل‌ها میان نمونه‌ها جابه‌جا شده‌اند.
- ‏`percent_fails`: درصد بخش‌های FAIL، یعنی ۱ از ۱۰ = ۱۰٪ برای نمونه‌ی ۲.
- این جدول TSV است؛ با pandas (بخش ۰۳) یا R (بخش ۰۴) خوانده می‌شود.

> 📺 **فیلم:** *Introduction to MultiQC*: https://www.youtube.com/watch?v=BbScv9TcaMg (Phil Ewels)
> 📄 **مرجع:** Ewels P, et al. (2016). *MultiQC.* Bioinformatics 32:3047–3048. https://doi.org/10.1093/bioinformatics/btw354

---

## ۹. سه اشتباه رایج

**۱. «همه باید PASS باشد».** مرزهای FastQC برای یک گونه است. حذف `minigut_sample2` به‌خاطر FAIL در GC یعنی دور ریختن **متنوع‌ترین** نمونه به‌خاطر ویژگی زیستی‌اش. هر FAIL را با نوع کتابخانه و نمونه تفسیر کنید (جدول بخش ۷).

**۲. تنها R1 را دیدن.** R2 در بیشتر داده‌ها کیفیت پایین‌تری دارد (تمرین ۱ عددش را می‌خواهد). اگر تنها R1 را ببینید، مشکل R2 پنهان می‌ماند. همیشه هر دو فایل را به FastQC بدهید (`raw/*.fastq.gz`).

**۳. فراموش کردن `-o`.** بی `-o`، FastQC گزارش‌ها را **کنار ورودی** می‌نویسد: پوشه‌ی `raw/` با فایل‌های `html` و `zip` درهم می‌شود، و اگر `raw/` را برای دیگران بفرستید، گزارش‌ها هم می‌روند. داده‌ی خام را دست‌نخورده نگه دارید؛ خروجی هر گام در پوشه‌ی خودش.

---

## 📘 برای کنجکاوها

- **کیفیت پله‌ای:** دستگاه‌های تازه‌ی Illumina کیفیت را در چند دسته‌ی محدود گزارش می‌کنند (برای نمونه NovaSeq: ۲، ۱۲، ۲۳، ۳۷). نمودار کیفیت آن‌ها پله‌ای است و این طبیعی است.
- **حافظه:** برای ریدهای بسیار بلند (Nanopore) شاید `OutOfMemoryError` ببینید؛ `--memory 1024` (مگابایت برای هر فایل) را بیفزایید.
- ‏**‏Duplication در متاژنوم:** در بیشتر پروژه‌های متاژنوم Shotgun ریدهای تکراری **برداشته نمی‌شوند**؛ برداشتنشان فراوانی گونه‌های غالب را کم نشان می‌دهد.
- ‏**‏FastQC در Snakemake:** قاعده‌ای با `input: "raw/{sample}_{read}.fastq.gz"` و دو خروجی `html` و `zip` (بخش ۰۵). درس ۲ کل این ماژول را در یک Snakefile می‌گذارد.

---

## جمع‌بندی

- ‏FastQC برای هر FASTQ یک گزارش `html` (برای چشم) و یک `zip` (برای خط فرمان) می‌سازد.
- ‏`unzip -p … summary.txt | grep -v PASS` در یک حلقه، همه‌ی مشکل‌ها را در چند خط نشان می‌دهد.
- در متاژنوم، GC چندقله‌ای و duplication نسبتاً بالا منتظره‌اند؛ FAIL در GC نمونه‌ی ۲ همان ترکیب جامعه است.
- ‏MultiQC همه‌ی نمونه‌ها را کنار هم می‌گذارد؛ نمونه‌ی ناجور را در یک نگاه پیدا می‌کنید.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
fastqc -q -t 4 -o qc/fastqc_raw raw/*.fastq.gz           # reports: .html + .zip per file
unzip -l report_fastqc.zip                                # list files inside a zip
unzip -p report_fastqc.zip report_fastqc/summary.txt      # print one file from the zip
for z in qc/fastqc_raw/*_fastqc.zip; do                   # everything that is not PASS
  n=$(basename $z .zip); echo "== $n"; unzip -p $z $n/summary.txt | grep -v PASS
done
unzip -p X_fastqc.zip X_fastqc/fastqc_data.txt | grep -A 7 '>>Per base sequence quality'
multiqc qc/fastqc_raw -o qc/multiqc_raw                   # one report for all samples
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| کنترل کیفیت (QC) | ارزیابی داده پیش از تحلیل |
| ‏PASS / WARN / FAIL | داوری FastQC برای هر بخش، بر پایه‌ی مرزهای یک گونه |
| چرخه (*cycle*) | یک دور شیمیایی دستگاه که یک باز از هر رید را می‌خواند |
| آداپتور | توالی مصنوعی متصل به دو سر قطعه‌ی DNA در کتابخانه |
| ‏GC content | درصد بازهای G و C |
| ‏Duplication | توالی‌هایی که چند بار تکرار شده‌اند |
| ‏MultiQC | ابزاری که گزارش‌های چند نمونه و چند ابزار را یکی می‌کند |

---

## منابع

**مستند و مقاله**
- FastQC (Babraham Bioinformatics), project page and help for every module: https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
- Ewels P, et al. (2016). *MultiQC: summarize analysis results for multiple tools and samples in a single report.* Bioinformatics 32(19):3047–3048. https://doi.org/10.1093/bioinformatics/btw354
- MultiQC documentation: https://docs.seqera.io/multiqc
- Quince C, et al. (2017). *Shotgun metagenomics, from sampling to analysis.* Nature Biotechnology 35:833–844. https://doi.org/10.1038/nbt.3935
- Galaxy Training, *Quality Control*: https://training.galaxyproject.org/training-material/topics/sequence-analysis/tutorials/quality-control/tutorial.html

**کتاب**
- ‏Wang X (2016). *Next-Generation Sequencing Data Analysis*. CRC Press. (فصل کنترل کیفیت ریدها)
- Nagarajan M (ed.) (2018). *Metagenomics: Perspectives, Methods, and Applications*. Academic Press.

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins University); کار با FASTQ و ابزارهای خط فرمان: https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Linux* (The Linux Foundation). دوره‌ای ویژه‌ی QC ریدها در edX نیافتیم؛ نزدیک‌ترین: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux
- ‏YouTube: *Using FastQC to check the quality of high throughput sequence* (Babraham Bioinformatics، سازندگان FastQC): https://www.youtube.com/watch?v=bz93ReOv87Y
- YouTube: *GTN Training: Intro to NGS – Quality Control (Lecture)* (Galaxy Project): https://www.youtube.com/watch?v=BWonTPS4zB8
- ‏YouTube: *Introduction to MultiQC* (Phil Ewels، سازنده‌ی MultiQC): https://www.youtube.com/watch?v=BbScv9TcaMg

<sub>نشانی‌های YouTube و DOIها در 2026-10-12 وارسی شدند. وارسی دوباره‌ی همه‌ی نشانی‌ها در پایان دوره انجام می‌شود.</sub>

</div>
