<div dir="rtl">

# پاسخ تشریحی: کنترل کیفیت و پیرایش ریدها

> همه‌ی دستورها در تاریخ **2026-10-12** با FastQC 0.12.1، fastp 0.23.4، MultiQC 1.25.1 و seqkit 2.13 اجرا شده‌اند. چون داده شبیه‌سازی‌شده و ثابت است، اعداد شما باید **دقیقاً** همین‌ها باشند.

---

## تمرین ۱: کارت شناسایی داده

<div dir="ltr">

```bash
seqkit stats -a -T data/raw/*.fastq.gz | cut -f1,4,7,16,18 | column -t

mkdir -p work/01_qc/fastqc_raw
fastqc -q -t 4 data/raw/*_R[12].fastq.gz -o work/01_qc/fastqc_raw
for f in work/01_qc/fastqc_raw/*_fastqc.zip; do
  n=$(basename $f .zip)
  unzip -p $f $n/fastqc_data.txt | sed -n '/>>Per base sequence quality/,/>>END/p' \
    | grep -v '^>>\|^#' | sed -n '1p;$p' | cut -f1,2 | tr '\n' ' '; echo " ← $n"
done
```

</div>

| فایل | تعداد رید | طول | %GC | Q30 | ‏Q میانگین موقعیت ۱ | ‏Q میانگین موقعیت آخر |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| minigut_R1 | 50,000 | 126 | 46.8 | 92% | 32.4 | 30.5 |
| minigut_R2 | 50,000 | 126 | 46.8 | 90% | 31.9 | 29.8 |
| minigut_sample2_R1 | 24,993 | 151 | 40.5 | 96% | 35.5 | 34.7 |
| minigut_sample2_R2 | 24,993 | 151 | 40.5 | 90% | 36.2 | **31.1** |

**تفسیر:**
- در هر دو نمونه **R2 بدتر از R1 است** (Q30 کمتر و افت بیشتر در انتها). در نمونه‌ی ۲ تفاوت به‌خوبی دیده می‌شود: R1 در انتها 34.7 است و R2 به 31.1 می‌رسد. این با Illumina سازگار است. R2 بعد از ساخت مجدد خوشه‌ها و صدها چرخه‌ی شیمیایی خوانده می‌شود. خطای phasing (ناهم‌گامی رشته‌های یک خوشه) و افت سیگنال با هر چرخه انباشته می‌شود و کیفیت در انتهای هر رید، به‌ویژه R2، کاهش می‌یابد.
- ‏%GC دو فایل R1 و R2 یک نمونه تقریباً برابر است، که باید هم باشد چون از یک قطعه آمده‌اند. **تفاوت GC بین R1 و R2 یک نمونه علامت هشدار است**، مثلاً جابه‌جا شدن فایل‌ها بین نمونه‌ها.
- اینکه کیفیت موقعیت ۱ از موقعیت‌های بعدی کمتر است (32.4 در برابر حدود 35.6 در موقعیت ۶ R1 نمونه‌ی ۱) در Illumina رایج است: چرخه‌ی اول کالیبراسیون ضعیف‌تری دارد.

---

## تمرین ۲: دو ژنوم، یک قله؟

<div dir="ltr">

```bash
for s in minigut_R1 minigut_sample2_R1; do
  echo "== $s"
  unzip -p work/01_qc/fastqc_raw/${s}_fastqc.zip ${s}_fastqc/fastqc_data.txt \
    | sed -n '/>>Per sequence GC/,/>>END/p' | awk 'NR>2 && $1%5==0 {printf "%s:%s  ", $1, $2} END{print ""}'
done
```

</div>

<div dir="ltr">

```text
== minigut_R1
0:0.0  5:0.0  10:0.0  15:2.5  20:19.5  25:131.0  30:401.0  35:812.0  40:1380.5  45:2094.0  50:2250.5  55:1804.5  60:817.5  65:198.0  70:25.0  75:5.0  80:0.5  85:0.0  ...
== minigut_sample2_R1
0:0.0  5:0.0  10:1.0  15:10.5  20:71.0  25:197.0  30:539.0  35:1011.5  40:1324.5  45:984.0  50:354.0  55:116.5  60:77.0  65:108.0  70:109.0  75:50.0  80:10.5  85:1.0  ...
```

</div>

### ۲.۱ و ۲.۲
- ‏**minigut:** یک قله‌ی پهن با بیشینه در حدود **۴۵ تا ۵۰٪** و تقریباً متقارن. دو ژنوم GC نزدیک به هم دارند (43.3 و 50.8، فاصله‌ی ۷٫۵ واحد). از طرف دیگر، **GC هر رید ۱۲۶ بازی** خودش پراکندگی زیادی دارد: انحراف معیار GC ریدهای کوتاه از یک ژنوم چند درصد است، چون GC در طول ژنوم یکنواخت نیست و نمونه‌گیری ۱۲۶ بازی هم نوسان آماری دارد. دو توزیع پهن با مرکزهای نزدیک **روی هم می‌افتند** و یک قله‌ی پهن می‌سازند که هنوز به منحنی نرمال برازش شده توسط FastQC نزدیک است. نتیجه PASS است.
- ‏**minigut_sample2:** قله‌ی اصلی در حدود **۴۰٪** (*A. baumannii*، GC 39.0%، ۶۴٫۶٪ ریدها) و یک **شانه‌ی دوم در ۶۵ تا ۷۰٪** (*P. aeruginosa* 66.6%، *C. sphaeroides* 69.0%، *D. radiodurans* 67.0%). فاصله‌ی حدود ۲۷ واحدی دو گروه بیشتر از پهنای هر توزیع است. شانه‌ی دوم از منحنی نرمال تک‌قله‌ای فاصله‌ی زیادی دارد و FastQC (وقتی بیش از ۳۰٪ ریدها از منحنی فاصله داشته باشند) FAIL می‌دهد.

**نتیجه:** PASS یا FAIL ماژول GC در متاژنوم چیزی درباره‌ی **کیفیت** داده نمی‌گوید. فقط می‌گوید ترکیب GC جامعه چقدر از «یک گونه» فاصله دارد.

### ۲.۳ جواب به استاد راهنما (نمونه)
> ‏«FAIL در ماژول GC به این دلیل است که FastQC یک توزیع تک‌قله‌ای (مثل ژنوم یک گونه) انتظار دارد، در حالی که نمونه‌ی ۲ یک جامعه‌ی ۲۱‌گونه‌ای است که چند گونه‌ی GC بالا (مثل *Pseudomonas aeruginosa* با ۶۶٪) دارد و شانه‌ی دوم توزیع را می‌سازد. همه‌ی معیارهای کیفیت واقعی (کیفیت بازها، N، آداپتور، duplication) PASS هستند و fastp ۹۹٫۹۸٪ ریدها را نگه داشت. حذف این نمونه یعنی حذف متنوع‌ترین نمونه به خاطر ویژگی زیستی‌اش، نه نقص فنی.»

---

## تمرین ۳: سه راهبرد روی نمونه‌ی ۲

<div dir="ltr">

```bash
R=data/raw; s=minigut_sample2; T=work/01_qc/compare; mkdir -p $T
fastp -i $R/${s}_R1.fastq.gz -I $R/${s}_R2.fastq.gz -o $T/s2A_R1.fq.gz -O $T/s2A_R2.fq.gz \
      -q 20 -l 36 -j $T/s2A.json -h $T/s2A.html
fastp -i $R/${s}_R1.fastq.gz -I $R/${s}_R2.fastq.gz -o $T/s2B_R1.fq.gz -O $T/s2B_R2.fq.gz \
      --detect_adapter_for_pe --cut_right --cut_mean_quality 20 -l 50 -j $T/s2B.json -h $T/s2B.html
fastp -i $R/${s}_R1.fastq.gz -I $R/${s}_R2.fastq.gz -o $T/s2C_R1.fq.gz -O $T/s2C_R2.fq.gz \
      --detect_adapter_for_pe --cut_front --cut_tail --cut_mean_quality 20 -l 50 -j $T/s2C.json -h $T/s2C.html
for x in A B C; do
  jq -r --arg x $x '[$x, .summary.after_filtering.total_reads, .summary.after_filtering.total_bases,
     .summary.after_filtering.q30_rate, .filtering_result.too_short_reads] | @tsv' $T/s2$x.json
done
```

</div>

<div dir="ltr">

```text
A	49976	7545038	0.933715	2
B	49176	7276405	0.942056	808
C	49976	7541431	0.9341	4
```

</div>

| راهبرد | ریدها | % | بازها | Q30 | کوتاه |
| :--- | ---: | ---: | ---: | :-: | ---: |
| A | 49,976 | 99.98 | 7,545,038 | 93.37% | 2 |
| B | 49,176 | 98.38 | 7,276,405 | 94.21% | 808 |
| C | 49,976 | 99.98 | 7,541,431 | 93.41% | 4 |

(ورودی: ۴۹٬۹۸۶ رید، ۷٬۵۴۷٬۸۸۶ باز، Q30 = 93.37%.)

**چرا تفاوت B و C کمتر است؟** دو دلیل، هر دو قابل‌اندازه‌گیری از تمرین ۱:
1. کیفیت این نمونه بالاتر و یکنواخت‌تر است (Q30 R1 = 96%). پنجره‌های زیر Q20 در وسط رید کمترند، پس `--cut_right` دیرتر و کمتر فعال می‌شود.
2. ریدها ۱۵۱ بازی‌اند. حتی وقتی `--cut_right` رید را از وسط می‌بُرد، احتمال اینکه طول باقی‌مانده بالای ۵۰ بماند بیشتر است. به همین دلیل فقط ۸۰۸ رید (۱٫۶٪) با `-l 50` حذف شدند، در برابر ۱۰٬۷۳۴ (۱۰٫۷٪) در `minigut`.

**درس:** اثر یک پارامتر به **پروفایل کیفیت داده** بستگی دارد. همان دستور روی دو دیتاست نتایج کاملاً متفاوت می‌دهد.

---

## تمرین ۴: حساسیت به اندازه‌ی پنجره

<div dir="ltr">

```bash
R=data/raw; s=minigut; T=work/01_qc/compare
for w in 4 10; do
  fastp -i $R/${s}_R1.fastq.gz -I $R/${s}_R2.fastq.gz -o $T/w${w}_R1.fq.gz -O $T/w${w}_R2.fq.gz \
        --detect_adapter_for_pe --cut_right --cut_window_size $w --cut_mean_quality 20 -l 50 \
        -j $T/B_w$w.json -h $T/B_w$w.html
  printf "W=%s\t" $w
  jq -r '[.summary.after_filtering.total_reads, .summary.after_filtering.total_bases,
          .summary.after_filtering.q30_rate, .filtering_result.too_short_reads] | @tsv' $T/B_w$w.json
done
```

</div>

<div dir="ltr">

```text
W=4	89176	11110072	0.944662	10734
W=10	98788	12302191	0.923087	1132
```

</div>

1. با پنجره‌ی ۱۰، **۹۸٬۷۸۸ رید (۹۸٫۸٪)** باقی ماند و فقط **۱٬۱۳۲ رید** به دلیل کوتاهی حذف شد، در برابر ۱۰٬۷۳۴ رید با پنجره‌ی ۴.
2. **حساب:** اول ببینیم در این داده چه کاراکترهای کیفیتی هست:

   <div dir="ltr">

   ```bash
   zcat data/raw/minigut_R1.fastq.gz | awk 'NR%4==0' | head -20000 | fold -w1 | sort | uniq -c
   ```

   </div>

   بیشتر بازها `F` (Q37) و `B` (Q33) هستند. ولی `<` (Q27)، `7` (Q22) و `/` (Q14) هم به‌وفور دیده می‌شوند (۹۷٬۷۸۵ `/` در ۲۰٬۰۰۰ رید اول، یعنی حدود ۳٫۹٪ بازها). `#` (Q2) نادر است.
   - **پنجره‌ی ۴**، یک `/` بین `F`ها: (14 + 3×37) / 4 = **31.25**، بالای ۲۰، پس برش نمی‌دهد.
   - **پنجره‌ی ۴**، یک خوشه‌ی کوچک `/ / 7 <`: (14 + 14 + 22 + 27) / 4 = 77 / 4 = **19.25**، زیر ۲۰. `--cut_right` از همین نقطه **کل بقیه‌ی رید** را می‌بُرد.
   - **پنجره‌ی ۱۰**، همان خوشه همراه با ۶ باز `F`: (14 + 14 + 22 + 27 + 6×37) / 10 = 299 / 10 = **29.9**، بالای ۲۰، پس برش نمی‌دهد.

   پنجره‌ی بزرگ‌تر افت‌های **موضعی** را با بازهای خوب اطرافش میانگین می‌گیرد و فقط افت‌های **پایدار** (مثل انتهای رید) را می‌بُرد. هزینه‌اش این است که ممکن است چند باز بد در مرز برش باقی بماند، که برای Q30 بعد از برش دیده می‌شود (92.3% در برابر 94.5%).

---

## تمرین ۵: جفت‌ها سالم مانده‌اند؟

<div dir="ltr">

```bash
for s in minigut minigut_sample2; do
  for r in R1 R2; do
    printf "%s %s: " $s $r; zcat work/01_qc/trimmed/${s}_${r}.fastq.gz | awk 'END{print NR/4}'
  done
done
zcat work/01_qc/trimmed/minigut_R1.fastq.gz | awk 'NR%4==1' | sed -n '1p;$p'
zcat work/01_qc/trimmed/minigut_R2.fastq.gz | awk 'NR%4==1' | sed -n '1p;$p'
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

1. در هر نمونه **R1 = R2** است (۴۹٬۸۴۵ و ۲۴٬۹۸۸).
2. نام رید n‌ام R1 و R2 باید **جز پسوند `/1` و `/2`** یکسان باشد، مثلاً `@NC_006347.1_0/1` و `@NC_006347.1_0/2`.
3. اجرای جداگانه روی R1 و R2 باعث می‌شود رید حذف‌شده از R1 در R2 بماند، و برعکس. از آن نقطه به بعد **همه‌ی جفت‌ها جابه‌جا** می‌شوند. پیامدها:
   - ‏**Bowtie2** با تعداد نابرابر خطا می‌دهد (`Error, fewer reads in file specified with -2 than in file specified with -1`). اگر تعداد اتفاقاً برابر باشد ولی ترتیب به هم خورده باشد، خطا نمی‌دهد ولی **ریدهای نامرتبط را جفت فرض می‌کند**: نرخ «concordant» به‌شدت پایین می‌آید و insert size بی‌معنی می‌شود.
   - این حالت دوم خطرناک‌تر است، چون **بدون پیام خطا** نتیجه‌ی غلط می‌دهد.

---

## تمرین ۶ (چالشی): جدول QC برای مقاله

### ۶.۱

<div dir="ltr">

```bash
{
  printf "sample\treads_before\treads_after\tpct_kept\tq30_before\tq30_after\tlow_quality\ttoo_short\ttoo_many_N\tadapter_trimmed_reads\n"
  for j in work/01_qc/fastp_reports/*.json; do
    jq -r --arg s "$(basename $j .json)" '[$s,
      .summary.before_filtering.total_reads, .summary.after_filtering.total_reads,
      ((.summary.after_filtering.total_reads / .summary.before_filtering.total_reads * 10000 | round) / 100),
      (.summary.before_filtering.q30_rate*100|round), (.summary.after_filtering.q30_rate*100|round),
      .filtering_result.low_quality_reads, .filtering_result.too_short_reads,
      .filtering_result.too_many_N_reads, .adapter_cutting.adapter_trimmed_reads] | @tsv' $j
  done
} > work/01_qc/qc_summary.tsv
column -t work/01_qc/qc_summary.tsv
```

</div>

<div dir="ltr">

```text
sample           reads_before  reads_after  pct_kept  q30_before  q30_after  low_quality  too_short  too_many_N  adapter_trimmed_reads
minigut          100000        99690        99.69     91          91         308          2          0           12
minigut_sample2  49986         49976        99.98     93          93         4            4          2           30
```

</div>

توجه: fastp «رید» را جداگانه می‌شمارد، یعنی R1 + R2. پس ۱۰۰٬۰۰۰ برابر ۵۰٬۰۰۰ جفت است. در مقاله واحد را صریح بنویسید.

### ۶.۲ نمونه‌ی Methods و Results
> **Methods.** Read quality was assessed with FastQC v0.12.1 and summarised with MultiQC v1.25.1. Adapters and low-quality bases were removed with fastp v0.23.4 in paired-end mode (`--detect_adapter_for_pe --cut_front --cut_tail --cut_mean_quality 20 --length_required 50`; other parameters at default, i.e. reads with >40% of bases below Q15 or >5 N bases were discarded). Read pairs were discarded if either mate failed filtering. Trimming parameters were chosen after comparing three strategies; a 5'→3' sliding-window trim (`--cut_right`) was rejected because it removed 10.8% of reads in sample minigut due to isolated low-quality bases within otherwise high-quality reads.
>
> **Results.** After trimming, 99.69% and 99.98% of reads were retained for minigut and minigut_sample2, respectively (49,845 and 24,988 read pairs), with Q30 rates of 91% and 93%. The bimodal GC distribution of minigut_sample2 (flagged by FastQC) reflects its community composition rather than a technical artefact.

نکته‌ها: نسخه‌ی ابزارها، پارامترهای غیرپیش‌فرض **و** معنی پیش‌فرض‌های مهم، رفتار با جفت‌ها، و **دلیل** انتخاب پارامتر. داور با این اطلاعات می‌تواند کار را ارزیابی و تکرار کند.

</div>
