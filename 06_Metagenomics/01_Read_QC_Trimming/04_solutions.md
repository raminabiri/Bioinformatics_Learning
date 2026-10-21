<div dir="rtl">

# پاسخ تشریحی: کنترل کیفیت و بریدن ریدها

خروجی‌ها از اجرای واقعی در 2026-10-12 (FastQC 0.12.1، fastp 0.23.4، MultiQC 1.25.1، seqkit 2.13) گرفته شده‌اند. داده شبیه‌سازی‌شده و ثابت است، پس عددهای شما باید **همین‌ها** باشند.

---

## پاسخ ۱: کارت شناسایی داده

<div dir="ltr">

```bash
seqkit stats -a -T raw/*.fastq.gz | cut -f 1,4,7,16,18
```

</div>

ستون‌های `seqkit stats -a -T`: ۱ فایل، ۴ شمار، ۷ میانگین طول، ۱۶ ‏Q30(%)، ۱۸ ‏GC(%). کیفیت جایگاه‌ها از `fastqc_data.txt`:

<div dir="ltr">

```bash
for z in qc/fastqc_raw/*_fastqc.zip; do
  n=$(basename $z .zip)
  echo "== $n"
  unzip -p $z $n/fastqc_data.txt | grep -A 2 '>>Per base sequence quality' | tail -n 1 | cut -f 1,2
  unzip -p $z $n/fastqc_data.txt | grep -B 1 -m 2 '>>END_MODULE' | tail -n 2 | head -n 1 | cut -f 1,2
done
```

</div>

‏(‏`grep -B 1` خط **پیش از** هر `>>END_MODULE`؛ `-m 2` تنها دو یافته‌ی نخست را می‌دهد، یعنی پایان بخش‌های ۱ و ۲؛ پایان بخش ۲ همان آخرین جایگاه جدول کیفیت است.)

| فایل | شمار رید | طول | ‏%GC | ‏Q30 | ‏Q جایگاه ۱ | ‏Q جایگاه آخر |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| minigut_R1 | 50,000 | 126 | 46.8 | 92% | 32.4 | 30.5 |
| minigut_R2 | 50,000 | 126 | 46.8 | 90% | 31.9 | 29.8 |
| minigut_sample2_R1 | 24,993 | 151 | 40.5 | 96% | 35.5 | 34.7 |
| minigut_sample2_R2 | 24,993 | 151 | 40.5 | 90% | 36.2 | **31.1** |

**تفسیر:**
- در هر دو نمونه **R2 بدتر است**: Q30 کمتر و افت بیشتر در انتها. در نمونه‌ی ۲ آشکار است: آخرین جایگاه R1 ‏۳۴٫۷ و R2 ‏۳۱٫۱. R2 پس از صدها چرخه‌ی شیمیایی و بازسازی خوشه‌ها خوانده می‌شود؛ ناهم‌گامی رشته‌های یک خوشه انباشته می‌شود.
- ‏GC دو فایل یک نمونه برابر است، چنان‌که باید. **تفاوت GC میان R1 و R2 یک نمونه زنگ خطر است** (شاید فایل‌ها جابه‌جا شده‌اند).
- کیفیت جایگاه ۱ از جایگاه‌های بعدی کمتر است (۳۲٫۴ در برابر ۳۶٫۱ در جایگاه ۶ در `minigut_R1`؛ درس ۱، بخش ۶): چرخه‌های نخست Illumina کالیبراسیون ضعیف‌تری دارند.

---

## پاسخ ۲: دو ژنوم، یک قله؟

<div dir="ltr">

```bash
unzip -p qc/fastqc_raw/minigut_R1_fastqc.zip minigut_R1_fastqc/fastqc_data.txt \
  | grep -A 102 '>>Per sequence GC' \
  | awk 'NR > 2 && $1 % 5 == 0 && $1 >= 15 && $1 <= 85 {printf "%s:%s  ", $1, $2} END {print ""}'
```

</div>

<div dir="ltr">

```text
15:2.5  20:19.5  25:131.0  30:401.0  35:812.0  40:1380.5  45:2094.0  50:2250.5  55:1804.5  60:817.5  65:198.0  70:25.0  75:5.0  80:0.5  85:0.0
```

</div>

**(الف)** یک قله‌ی پهن با بیشینه در **۴۵ تا ۵۰٪**، کمابیش متقارن.

**(ب)** دو ژنوم GC نزدیک به هم دارند (فاصله‌ی ۷٫۵ واحد)، و GC هر رید ۱۲۶ بازی خودش چند درصد نوسان دارد؛ پس دو قله‌ی پهن روی هم می‌افتند و یک زنگوله‌ی پهن می‌سازند. در `minigut_sample2` فاصله‌ی دو گروه (کمابیش ۴۰ و ۶۷ درصد) از پهنای هر قله بیشتر است، پس شانه‌ی دوم جدا می‌ماند.

**(ج)** نمونه‌ی پاسخ:
> ‏«FAIL در بخش GC به این دلیل است که FastQC یک پراکنش تک‌قله‌ای، همانند ژنوم یک گونه، انتظار دارد؛ نمونه‌ی ۲ جامعه‌ای ۲۱‌گونه‌ای با چند گونه‌ی پر-GC (مانند *Pseudomonas aeruginosa* با ۶۶٪) است که شانه‌ی دوم را می‌سازند. همه‌ی سنجه‌های کیفیت واقعی (کیفیت بازها، N، آداپتور، duplication) PASS هستند و fastp ‏۹۹٫۹۸٪ ریدها را نگه داشت. حذف این نمونه یعنی حذف متنوع‌ترین نمونه به‌خاطر ویژگی زیستی‌اش، نه نقص فنی.»

---

## پاسخ ۳: سه راهبرد روی نمونه‌ی ۲

<div dir="ltr">

```bash
R=raw; s=minigut_sample2; T=qc/compare
fastp -i $R/${s}_R1.fastq.gz -I $R/${s}_R2.fastq.gz -o $T/s2A_R1.fq.gz -O $T/s2A_R2.fq.gz \
      -q 20 -l 36 -j $T/s2A.json -h $T/s2A.html 2> $T/s2A.log
fastp -i $R/${s}_R1.fastq.gz -I $R/${s}_R2.fastq.gz -o $T/s2B_R1.fq.gz -O $T/s2B_R2.fq.gz \
      --detect_adapter_for_pe --cut_right --cut_mean_quality 20 -l 50 \
      -j $T/s2B.json -h $T/s2B.html 2> $T/s2B.log
fastp -i $R/${s}_R1.fastq.gz -I $R/${s}_R2.fastq.gz -o $T/s2C_R1.fq.gz -O $T/s2C_R2.fq.gz \
      --detect_adapter_for_pe --cut_front --cut_tail --cut_mean_quality 20 -l 50 \
      -j $T/s2C.json -h $T/s2C.html 2> $T/s2C.log
grep -H 'reads passed filter\|too short' $T/s2*.log
```

</div>

<div dir="ltr">

```text
qc/compare/s2A.log:reads passed filter: 49976
qc/compare/s2A.log:reads failed due to too short: 2
qc/compare/s2B.log:reads passed filter: 49176
qc/compare/s2B.log:reads failed due to too short: 808
qc/compare/s2C.log:reads passed filter: 49976
qc/compare/s2C.log:reads failed due to too short: 4
```

</div>

| راهبرد | ریدهای مانده | ‏% مانده | رفته: کوتاه |
| :--- | ---: | ---: | ---: |
| A | 49,976 | 99.98 | 2 |
| B | 49,176 | 98.38 | 808 |
| C | 49,976 | 99.98 | 4 |

**چرا تفاوت B و C کمتر است؟**
1. کیفیت این نمونه بالاتر و یکنواخت‌تر است (Q30 در R1 ‏۹۶٪، تمرین ۱): پنجره‌های زیر Q20 در میانه‌ی رید کمترند، پس `--cut_right` دیرتر و کمتر به کار می‌افتد.
2. ریدها ۱۵۱ بازی‌اند: حتی وقتی رید از میانه بریده می‌شود، شانس اینکه بالای ۵۰ باز بماند بیشتر است. تنها ۸۰۸ رید (۱٫۶٪) با `-l 50` رفتند، در برابر ۱۰٬۷۳۴ (۱۰٫۷٪) در `minigut`.

**درس:** اثر یک پارامتر به **نمایه‌ی کیفیت داده** بستگی دارد؛ یک دستور روی دو داده‌ی گوناگون نتیجه‌ی بسیار گوناگون می‌دهد.

---

## پاسخ ۴: پهنای پنجره

<div dir="ltr">

```bash
R=raw; s=minigut; T=qc/compare
fastp -i $R/${s}_R1.fastq.gz -I $R/${s}_R2.fastq.gz -o $T/w10_R1.fq.gz -O $T/w10_R2.fq.gz \
      --detect_adapter_for_pe --cut_right --cut_window_size 10 --cut_mean_quality 20 -l 50 \
      -j $T/B_w10.json -h $T/B_w10.html 2> $T/B_w10.log
grep -H 'reads passed filter\|too short' $T/B.log $T/B_w10.log
```

</div>

<div dir="ltr">

```text
qc/compare/B.log:reads passed filter: 89176
qc/compare/B.log:reads failed due to too short: 10734
qc/compare/B_w10.log:reads passed filter: 98788
qc/compare/B_w10.log:reads failed due to too short: 1132
```

</div>

**(الف)** با پنجره‌ی ۱۰، **۹۸٬۷۸۸ رید (۹۸٫۸٪)** ماند و تنها **۱٬۱۳۲** رید به‌خاطر کوتاهی رفتند، در برابر ۱۰٬۷۳۴ با پنجره‌ی ۴.

**(ب)**
- پنجره‌ی ۴: ‏(14 + 14 + 22 + 27) / 4 = **19.25** ← زیر ۲۰ ← برش از همین‌جا تا پایان رید.
- پنجره‌ی ۱۰: ‏(14 + 14 + 22 + 27 + 6×37) / 10 = 299 / 10 = **29.9** ← بالای ۲۰ ← بی برش.

پنجره‌ی پهن‌تر افت‌های **موضعی** را با بازهای خوب پیرامونشان میانگین می‌گیرد و تنها افت‌های **پایدار** (مانند انتهای رید) را می‌بُرد. بهایش: چند باز بد در مرز برش می‌مانند. Q30 پس از برش این را نشان می‌دهد: ۹۲٫۳٪ با پنجره‌ی ۱۰، در برابر ۹۴٫۵٪ با پنجره‌ی ۴ (از گزارش JSON، `q30_rate`).

---

## پاسخ ۵: جفت‌ها

<div dir="ltr">

```bash
for s in minigut minigut_sample2; do
  for r in R1 R2; do
    printf "%s %s: " $s $r
    zcat qc/trimmed/${s}_${r}.fastq.gz | awk 'END {print NR/4}'
  done
done
```

</div>

<div dir="ltr">

```text
minigut R1: 49845
minigut R2: 49845
minigut_sample2 R1: 24988
minigut_sample2 R2: 24988
```

</div>

**(الف)** در هر نمونه R1 = R2.

<div dir="ltr">

```bash
for r in R1 R2; do
  zcat qc/trimmed/minigut_${r}.fastq.gz | awk 'NR%4==1' | head -n 1
  zcat qc/trimmed/minigut_${r}.fastq.gz | awk 'NR%4==1' | tail -n 1
done
```

</div>

<div dir="ltr">

```text
@NC_006347.1_0/1
@NC_006347.1_14455/1
@NC_006347.1_0/2
@NC_006347.1_14455/2
```

</div>

**(ب)** نام رید شماره‌ی n در R1 و R2 باید **جز پسوند `/1` و `/2`** یکسان باشد: `NC_006347.1_0` و `NC_006347.1_14455` در هر دو فایل. این همان چیزی است که Bowtie2 (ماژول ۰۲) فرض می‌کند. (آخرین رید `_14455` است، با آنکه فایل ۴۹٬۸۴۵ رید دارد: شبیه‌ساز ریدهای دو ژنوم را پشت سر هم ننوشته است. شماره‌ها شناسه‌اند، نه جایگاه.)

---

## پاسخ ۶: جدول QC برای مقاله

**(الف)**

<div dir="ltr">

```python
# fastp_table.py: one TSV row per fastp JSON report
import glob
import json

columns = ["sample", "reads_before", "reads_after", "pct_kept", "q30_before", "q30_after",
           "low_quality", "too_short", "too_many_N", "adapter_trimmed"]
print("\t".join(columns))

for path in sorted(glob.glob("qc/fastp/*.json")):
    with open(path) as f:
        r = json.load(f)
    sample = path.split("/")[-1].replace(".json", "")
    before = r["summary"]["before_filtering"]
    after = r["summary"]["after_filtering"]
    filt = r["filtering_result"]
    row = [sample,
           before["total_reads"], after["total_reads"],
           round(after["total_reads"] / before["total_reads"] * 100, 2),
           round(before["q30_rate"] * 100, 1), round(after["q30_rate"] * 100, 1),
           filt["low_quality_reads"], filt["too_short_reads"], filt["too_many_N_reads"],
           r["adapter_cutting"]["adapter_trimmed_reads"]]
    print("\t".join(str(x) for x in row))
```

</div>

<div dir="ltr">

```bash
python3 fastp_table.py > qc/qc_summary.tsv
cat qc/qc_summary.tsv
```

</div>

<div dir="ltr">

```text
sample	reads_before	reads_after	pct_kept	q30_before	q30_after	low_quality	too_short	too_many_N	adapter_trimmed
minigut	100000	99690	99.69	91.3	91.5	308	2	0	12
minigut_sample2	49986	49976	99.98	93.4	93.4	4	4	2	30
```

</div>

- ‏`path.split("/")[-1]`: بخش پایانی نشانی (`minigut.json`)؛ سپس `.replace` پسوند را برمی‌دارد (بخش ۰۳).
- ‏`str(x) for x in row`: هر عدد به متن، تا `"\t".join` کار کند.
- ‏fastp ریدها را **تکی** می‌شمارد: ۱۰۰٬۰۰۰ = ۵۰٬۰۰۰ جفت. در مقاله یکا را روشن بنویسید.

**(ب)** نمونه:
> **Methods.** Read quality was assessed with FastQC v0.12.1 and summarised with MultiQC v1.25.1. Adapters and low-quality bases were removed with fastp v0.23.4 in paired-end mode (`--detect_adapter_for_pe --cut_front --cut_tail --cut_mean_quality 20 --length_required 50`; other parameters at default, i.e. reads with >40% of bases below Q15 or >5 N bases were discarded). A read pair was discarded if either mate failed filtering. A 5'→3' sliding-window trim (`--cut_right`) was rejected because it removed 10.8% of reads in sample minigut owing to isolated low-quality bases within otherwise high-quality reads.
>
> **Results.** After trimming, 99.69% and 99.98% of reads were retained for minigut and minigut_sample2 (49,845 and 24,988 read pairs). The bimodal GC distribution of minigut_sample2 flagged by FastQC reflects its community composition rather than a technical artefact.

یک داور با این‌ها کار را می‌سنجد و تکرار می‌کند: نسخه‌ی ابزارها، پارامترهای غیرپیش‌فرض **و** معنی پیش‌فرض‌های مهم، رفتار با جفت‌ها، و **دلیل** برگزیدن پارامتر.

---

## پاسخ ۷ (فکری): Snakemake

**(الف)** با ۳ نمونه:

| قاعده | شمار | چرا |
| :--- | ---: | :--- |
| `fastqc_raw` | 6 | ۳ نمونه × ۲ رید |
| `fastp` | 3 | یکی برای هر نمونه (R1 و R2 با هم) |
| `fastqc_trimmed` | 6 | ۳ × ۲ |
| `multiqc` | 1 | همه با هم |
| `all` | 1 | |
| **روی هم** | **17** | |

**(ب)** ‏`cut_mean_quality` از راه `params` به قاعده‌ی `fastp` می‌رسد، پس Snakemake تغییرش را می‌بیند (`Params have changed`):
- دوباره: `fastp` (برای هر نمونه)، و هر چه پایین‌دست آن است: `fastqc_trimmed` (ورودی‌اش ریدهای بریده‌شده است)، `multiqc`، `all`.
- نه: `fastqc_raw`. ورودی‌اش ریدهای **خام** است که عوض نشده‌اند و پارامتری از `config` ندارد.

با دو نمونه: 2 + 4 + 1 + 1 = **۸ کار**. این همان جدول «چه عوض شد / کدام کارها دوباره» در ماژول 05/04 است.

</div>
