<div dir="rtl">

# درس ۱: ارزیابی کیفیت ریدها با FastQC و MultiQC

**بخش:** `06_Metagenomics` · **ماژول:** `01_Read_QC_Trimming` · **پیش‌نیاز:** فرمت FASTQ (01/03) · **زمان:** ۱٫۵ ساعت · **ابزار:** FastQC 0.12.1، MultiQC 1.25.1 · **آخرین تست:** 2026-10-12

---

## ۱. مسئله

قبل از هر تحلیلی باید به این سؤال جواب دهید: **«آیا این داده برای سؤال من کافی و سالم است، و اگر نه، چه چیزی باید اصلاح شود؟»** کنترل کیفیت (QC) سه نوع مشکل را پیدا می‌کند:

1. **مشکلات فنی توالی‌یابی:** افت کیفیت در انتهای ریدها، بازهای N، خطاهای یک cycle خاص.
2. **مصنوعات کتابخانه:** آداپتور (وقتی قطعه کوتاه‌تر از طول خوانش است)، دایمر پرایمر، تکرارهای PCR.
3. **مشکلات نمونه:** آلودگی، ترکیب غیرمنتظره (که در GC و توالی‌های فراوان خودش را نشان می‌دهد).

**نکته‌ی مهم برای متاژنومیکس:** FastQC برای **ژنوم یک گونه** طراحی شده و معیارهای PASS/WARN/FAIL آن همین فرض را دارند. در متاژنوم، بعضی FAILها **انتظار می‌روند** و نشانه‌ی مشکل نیستند. مهارت اصلی این درس **تفکیک این دو** است.

## ۲. یادآوری کوتاه: کیفیت Phred

هر باز یک نمره‌ی کیفیت دارد: $Q = -10 \log_{10} P_{error}$

| Q | احتمال خطا | دقت |
| :-: | :-: | :-: |
| 10 | 1/10 | 90% |
| 20 | 1/100 | 99% |
| 30 | 1/1000 | 99.9% |
| 37 | ≈ 1/5000 | ≈ 99.98% |
| 40 | 1/10000 | 99.99% |

در FASTQ امروزی نمره با **Phred+33** به کاراکتر تبدیل می‌شود (`!`=Q0، `5`=Q20، `?`=Q30، `F`=Q37). دستگاه‌های جدید Illumina کیفیت را **binned** گزارش می‌کنند، یعنی فقط چند مقدار گسسته (مثلاً NovaSeq: 2، 12، 23، 37). پس نمودار کیفیت آن‌ها پله‌ای است و این طبیعی است.

## ۳. کار عملی

<div dir="ltr">

```bash
conda activate bioinfo_course
cd 06_Metagenomics
bash data/download.sh                 # یک‌بار
mkdir -p work/01_qc/fastqc_raw work/01_qc/multiqc_raw
```

</div>

### گام ۱: نگاه اولیه بدون هیچ ابزاری

<div dir="ltr">

```bash
zcat data/raw/minigut_R1.fastq.gz | head -n 4
zcat data/raw/minigut_R1.fastq.gz | awk 'END{print NR/4, "reads"}'
```

</div>

<div dir="ltr">

```text
@NC_006347.1_0/1
AACGTTGGCTCGTCTGACAAGCAAAGGTAAGAACAAAGGTGCCAAATATCGTAAAGAAAAACGTGACATGGCGTCCAACC...
+
BBBBBFFFFFFFFFFFFFFFFFF/FFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF...
50000 reads
```

</div>

همین‌جا دو چیز مشخص است. نام رید ژنوم مبدأ را می‌گوید (داده‌ی شبیه‌سازی‌شده). کیفیت هم عمدتاً `F` (Q37) است، با یک `/` (Q14) **در وسط رید**. این نکته در درس ۲ مهم می‌شود.

### گام ۲: FastQC

<div dir="ltr">

```bash
fastqc -t 4 data/raw/*_R[12].fastq.gz -o work/01_qc/fastqc_raw
```

</div>

- ‏`-t 4`: چهار فایل هم‌زمان پردازش می‌شوند. هر thread حدود 250 MB حافظه می‌گیرد.
- ‏FastQC فایل `.gz` را مستقیم می‌خواند و نیازی به باز کردن فشرده‌سازی نیست.
- خروجی برای هر فایل یک `_fastqc.html` و یک `_fastqc.zip` است. فایل zip شامل `summary.txt` و `fastqc_data.txt` است که برای خواندن ماشینی مناسب‌اند.

خلاصه‌ی وضعیت ماژول‌ها (خروجی واقعی):

<div dir="ltr">

```bash
for z in work/01_qc/fastqc_raw/*_fastqc.zip; do
  n=$(basename $z .zip); echo "$n: $(unzip -p $z $n/summary.txt | grep -v PASS | cut -f1,2 | tr '\n' ' ')"
done
```

</div>

<div dir="ltr">

```text
minigut_R1_fastqc:
minigut_R2_fastqc:
minigut_sample2_R1_fastqc: FAIL	Per sequence GC content
minigut_sample2_R2_fastqc: FAIL	Per sequence GC content
```

</div>

### گام ۳: MultiQC

<div dir="ltr">

```bash
multiqc work/01_qc/fastqc_raw -o work/01_qc/multiqc_raw
```

</div>

گزارش `work/01_qc/multiqc_raw/multiqc_report.html` را در مرورگر باز کنید. MultiQC همان نمودارهای FastQC را **برای همه‌ی نمونه‌ها روی هم** نشان می‌دهد. نمونه‌ی غیرعادی در یک نگاه پیدا می‌شود، و این وقتی ۱۰۰ نمونه دارید حیاتی است. جدول «General Statistics» را هم می‌شود به‌صورت `multiqc_data/multiqc_general_stats.txt` برای تحلیل در R یا Python برداشت.

## ۴. تفسیر ماژول‌های FastQC برای متاژنوم

| ماژول FastQC | چه چیزی را نشان می‌دهد | در متاژنوم Shotgun | داده‌ی ما |
| :--- | :--- | :--- | :--- |
| Basic Statistics | تعداد رید، طول، %GC، کدگذاری | — | ۵۰٬۰۰۰ رید، 126 bp، GC 46%، Sanger/Illumina 1.9 (=Phred+33) |
| Per base sequence quality | توزیع کیفیت در هر موقعیت | افت تدریجی در انتهای 3' طبیعی است؛ افت ناگهانی وسط رید یعنی مشکل دستگاه | ‏PASS؛ R2 نمونه‌ی ۲ از میانگین Q36.5 به Q31 در انتهای رید می‌رسد |
| Per sequence quality scores | توزیع میانگین کیفیت ریدها | دنباله‌ی کوچک ریدهای بی‌کیفیت طبیعی است | PASS |
| Per base sequence content | نسبت A/C/G/T در هر موقعیت | در کتابخانه‌های **Nextera/تگمنتاسیون** سوگیری ۱۰ تا ۱۵ باز اول طبیعی است (FAIL قابل انتظار) | ‏PASS (شبیه‌سازی) |
| **Per sequence GC content** | توزیع GC ریدها در برابر منحنی نرمال نظری | **چندقله‌ای بودن طبیعی است**، چون هر گونه GC خودش را دارد | ‏**FAIL در نمونه‌ی ۲**، و این مشکل نیست (پایین را ببینید) |
| Per base N content | درصد N در هر موقعیت | باید نزدیک صفر باشد؛ قله در یک موقعیت یعنی خطای cycle | PASS |
| Sequence length distribution | توزیع طول | داده‌ی خام طول ثابت دارد؛ بعد از trimming WARN طبیعی است | ‏PASS (خام) / WARN (بعد از trim) |
| Sequence duplication levels | سهم توالی‌های تکراری | گونه‌های **بسیار فراوان** ریدهای «تکراری» طبیعی تولید می‌کنند؛ تکرار بالا همیشه PCR duplicate نیست | PASS |
| Overrepresented sequences | توالی‌های خیلی فراوان | آداپتور، دایمر، PhiX، rRNA؛ یا یک ویروس/پلاسمید بسیار فراوان | PASS |
| Adapter content | درصد ریدهای حاوی آداپتور در هر موقعیت | اگر بالا رود، باید trim شود | ‏PASS (شبیه‌سازی) |

### چرا GC نمونه‌ی ۲ «FAIL» است و چرا این خبر خوبی است
توزیع GC ریدهای `minigut_sample2_R1` (ستون‌ها از `fastqc_data.txt`؛ هر ۵ درصد یک نقطه):

<div dir="ltr">

```text
GC%:    20   25   30   35    40     45    50   55   60   65   70   75
count:  71  197  539  1011  1324   984   354  116   77  108  109   50
```

</div>

یک قله‌ی اصلی در حدود **۴۰٪** و یک «شانه»ی دوم در حدود **۶۵ تا ۷۰٪** وجود دارد. FastQC انتظار یک توزیع نرمال تک‌قله‌ای دارد و FAIL می‌دهد. ولی ground truth این نمونه (`data/ground_truth.tsv`) دقیقاً همین را پیش‌بینی می‌کند:
- ‏*Acinetobacter baumannii* (GC = 39.0%) با ۶۴٫۶٪ ریدها، که **قله‌ی اصلی** را می‌سازد.
- ‏*Pseudomonas aeruginosa* (66.6%)، *Cereibacter sphaeroides* (69.0%)، *Deinococcus radiodurans* (67.0%) و *Cutibacterium acnes* (60.0%) با هم حدود ۷٪ ریدها را دارند و **شانه‌ی دوم** را می‌سازند.

(مقادیر GC از توالی کامل ژنوم‌ها با `seqkit fx2tab -g` محاسبه شده است.)

**قاعده‌ی عملی:** در متاژنوم، GC چندقله‌ای **اطلاعات** است، نه خطا. شکل آن «اثر انگشت» ترکیب جامعه است. چیزی که باید نگرانتان کند، قله‌ی **تیز و باریک** غیرمنتظره است، مثلاً یک آلودگی تک‌گونه یا مقدار زیاد آداپتور دایمر. یا وقتی شکل GC یک نمونه با بقیه‌ی نمونه‌های همان گروه خیلی فرق دارد (در MultiQC روی هم ببینید).

## ۵. دام‌ها (Pitfalls)

| دام | چرا مشکل است | راه درست |
| :--- | :--- | :--- |
| «همه‌ی ماژول‌ها باید PASS باشند» | معیارهای FastQC برای ژنوم تک‌گونه است | هر FAIL را با نوع کتابخانه و نمونه تفسیر کنید (جدول بالا) |
| حذف نمونه فقط به خاطر FAIL در GC یا duplication | ممکن است ترکیب واقعی جامعه یا گونه‌ی غالب را حذف کنید | با سایر نمونه‌ها و metadata مقایسه کنید |
| حذف duplicateها در متاژنوم مثل WGS | ریدهای گونه‌های فراوان را کم می‌کند و فراوانی را مخدوش می‌کند | در متاژنوم Shotgun معمولاً deduplication انجام نمی‌شود، مگر با دلیل مشخص (مثلاً کتابخانه با PCR سنگین) |
| ‏QC فقط روی R1 | ‏R2 تقریباً همیشه کیفیت پایین‌تری دارد | همیشه هر دو فایل را بررسی کنید |
| ‏QC نکردن بعد از trimming | نمی‌فهمید پیرایش درست کار کرده یا نه | ‏QC دوباره + گزارش fastp (درس ۲) |
| ‏`OutOfMemoryError` در FastQC | حافظه برای ریدهای خیلی بلند (مثلاً Nanopore) کافی نیست | ‏`--memory 1024` (MB به ازای هر فایل) یا کم کردن `-t` |

## ۶. جمع‌بندی
- ‏FastQC مشکلات فنی، کتابخانه‌ای و نمونه‌ای را نشان می‌دهد، اما معیارهایش برای یک گونه است. در متاژنوم، GC چندقله‌ای و duplication نسبتاً بالا قابل انتظارند.
- ‏MultiQC برای مقایسه‌ی نمونه‌ها و یافتن نمونه‌ی غیرعادی ضروری است.
- در داده‌ی دوره، همه‌ی ماژول‌ها PASS است، جز GC نمونه‌ی ۲. آن FAIL هم دقیقاً با ترکیب واقعی جامعه توضیح داده می‌شود.

## ۷. منابع

### مستندات و مقالات
- ‏FastQC (Babraham Bioinformatics) — صفحه‌ی اصلی و راهنمای هر ماژول: https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
- Ewels P, et al. (2016). MultiQC: summarize analysis results for multiple tools and samples in a single report. *Bioinformatics* 32(19):3047–3048. https://doi.org/10.1093/bioinformatics/btw354
- مستندات MultiQC: https://docs.seqera.io/multiqc
- Quince C, et al. (2017). Shotgun metagenomics, from sampling to analysis. *Nature Biotechnology* 35:833–844. https://doi.org/10.1038/nbt.3935
- Galaxy Training — Quality Control: https://training.galaxyproject.org/training-material/topics/sequence-analysis/tutorials/quality-control/tutorial.html

### ویدیوهای آموزشی
- ‏Babraham Bioinformatics (سازندگان FastQC) — *Using FastQC to check the quality of high throughput sequence*: https://www.youtube.com/watch?v=bz93ReOv87Y
- Galaxy Project — *GTN Training: Intro to NGS – Quality Control (Lecture)*: https://www.youtube.com/watch?v=BWonTPS4zB8
- ‏Phil Ewels (سازنده‌ی MultiQC) — *Introduction to MultiQC*: https://www.youtube.com/watch?v=BbScv9TcaMg
- Phil Ewels — *Using MultiQC Reports*: https://www.youtube.com/watch?v=qPbIlO_KWN0
- EMBL — *Metagenomics principles and workflow*: https://www.youtube.com/watch?v=RcYXTpNS_XU

> لینک‌ها در تاریخ 2026-10-12 بررسی شدند (ویدیوها با YouTube oEmbed، DOIها با Crossref، صفحات با درخواست HTTP).

</div>
