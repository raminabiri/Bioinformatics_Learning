<div dir="rtl">

# درس: طراحی آزمایش RNA-seq و کنترل کیفیت؛ پیش از آن‌که یک رید خوانده شود

**بخش:** `13_V2_RNAseq_Transcriptomics` · **ماژول:** `01_Design_QC` · **پیش‌نیاز:** FastQC ‏([06/01](../../06_Metagenomics/01_Read_QC_Trimming/))؛ GSE52778 و CPM ‏([11/04](../../11_V2_NCBI_Databases/04_GEO/))؛ ژن‌ها و رونوشت‌های Ensembl ‏([12/01](../../12_V2_Global_Databases_Browsers/01_Ensembl_BioMart/))؛ Conda ‏([02/01](../../02_BioLinux/01_Conda_Bioconda/)) · **زمان:** حدود ۸۰ دقیقه · **ابزار:** FastQC 0.13.0، MultiQC 1.35، Python 3 (محیط `rnaseq`) · **آخرین بازبینی:** 2026-10-28

> ✅ **وضعیت: اجرا شده.** همه‌ی خروجی‌ها واقعی‌اند (2026-10-28). ساختن داده ۱۱ دقیقه طول کشید (بیشترش انتظار برای سرور Ensembl)؛ FastQC روی ۱۲ فایل ۷ ثانیه و ۵۲۶ مگابایت حافظه.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. تکرار **زیستی** را از تکرار **فنی** جدا کنید و بگویید چرا «تکرار بیشتر» از «رید بیشتر» ارزشمندتر است.
2. گونه‌های کتابخانه‌ی RNA-seq (polyA، کاهش rRNA، **رشته‌ویژه**) را بشناسید.
3. اثر **دسته** (batch) و **درهم‌آمیختگی** (confounding) را پیش از آزمایش ببینید و طرح **جفتی** را بفهمید.
4. داده‌ی مشترک بخش ۱۳ را بسازید: یک «مینی‌ژنوم» با ۲۰ ژن و شش نمونه‌ی شبیه‌سازی‌شده با **پاسخ معلوم**.
5. ‏FastQC و MultiQC را روی RNA-seq بزنید و بدانید کدام «FAIL»ها در RNA-seq **عادی‌اند**.

---

## ۱. داستان

در 11/04 و 12/06 داده‌ی GSE52778 را دیدید: سلول‌های ماهیچه‌ی صاف راه هوایی از **چهار** فرد، هر کدام با **چهار** تیمار. هفت ژن با دگزامتازون بالا رفتند و NR3C1 پایین آمد. اکنون می‌خواهید **خودتان** چنین آزمایشی را طراحی و تحلیل کنید: از رید خام تا ژن‌های تغییرکرده. بخش ۱۳ همین راه را می‌رود:

<div dir="ltr">

```text
13/01 design + QC  ->  13/02 align + count  ->  13/03 DESeq2  ->  13/04 reproduce GSE52778  ->  13/05 bacteria
     FASTQ                  BAM -> counts           genes up/down       real data                     E. coli
```

</div>

**پاسخ معلوم:** برای این‌که بتوانید درستی هر گام را بسنجید، داده‌ی آموزشی را **شبیه‌سازی** می‌کنیم: ریدها از ۲۰ ژن واقعی انسان، با تغییر بیانی که **از پیش** می‌دانیم (هشت ژن دگزامتازون با همان log2FC بازتحلیل Expression Atlas در 12/06، و ۱۲ ژن خانه‌دار بی‌تغییر).

---

## ۲. مفهوم به زبان ساده

### ‏۲.۱ ‏RNA-seq چه می‌سنجد؟

‏RNA سلول‌ها را بیرون می‌کشیم، به cDNA برمی‌گردانیم، تکه‌تکه می‌کنیم و هر تکه را از دو سر می‌خوانیم (paired-end). هرچه ژنی بیشتر بیان شود، تکه‌های بیشتری از آن داریم. پس **شمار ریدهای هر ژن** نشانه‌ی بیان آن است. ولی این شمار به **عمق** نمونه (کل ریدها) و **طول** ژن هم بستگی دارد (CPM و TPM، 11/04 و 12/06).

### ۲.۲ تکرار: زیستی یا فنی؟

| | تکرار **زیستی** | تکرار **فنی** |
| :--- | :--- | :--- |
| چیست | نمونه‌ی **جدا**: موش دیگر، بیمار دیگر، کشت سلولی جدا | همان RNA، دوباره کتابخانه‌سازی یا دوباره توالی‌یابی |
| چه می‌سنجد | گوناگونی **زیستی** (آنچه می‌خواهیم دربارهٔش نتیجه بگیریم) | خطای دستگاه (در RNA-seq کوچک) |
| در RNA-seq | **لازم**؛ دست‌کم ۳، و بهتر ۶ در هر گروه | در بسیاری از موارد بی‌ارزش |

پژوهش‌ها نشان داده‌اند که پس از نزدیک به ۱۰ میلیون رید در نمونه، **افزودن تکرار زیستی** توان آماری را بسیار بیشتر از **افزودن رید** بالا می‌برد (Liu و همکاران، ۲۰۱۴). با ۳ تکرار، بسیاری از ژن‌های با تغییر کوچک دیده نمی‌شوند. Schurch و همکاران (۲۰۱۶) با ۴۸ تکرار مخمر دیدند برای یافتن بیشتر ژن‌های تغییرکرده دست‌کم ۶ تکرار و برای همه‌ی آن‌ها ۱۲ تکرار لازم است.

### ۲.۳ کتابخانه: polyA، کاهش rRNA، رشته‌ویژه

- ‏**polyA:** تنها mRNAهای دارای دم polyA گرفته می‌شوند. برای ژن‌های کدکننده‌ی یوکاریوت خوب است. **باکتری‌ها** mRNA پلی‌آدنیله ندارند (13/05).
- **کاهش rRNA** (ribo-depletion): بیش از ۸۰٪ RNA سلول rRNA است؛ آن را برمی‌داریم و بقیه را نگه می‌داریم (RNAهای ناکدکننده، و برای باکتری لازم).
- **رشته‌ویژه** (stranded؛ روش dUTP): کتابخانه به یاد دارد رید از کدام رشته‌ی DNA آمده است. در روش dUTP ‏(Illumina TruSeq Stranded) رید ۱ از رشته‌ی **مخالف** ژن است. این برای جدا کردن ژن‌هایی که روی دو رشته هم‌پوشانی دارند (antisense) لازم است و در 13/02 اگر اشتباه تنظیم شود **همه**‌ی شمارش‌ها را صفر می‌کند.

### ۲.۴ اثر دسته و درهم‌آمیختگی

اگر نمونه‌های «تیمار» را دوشنبه و نمونه‌های «شاهد» را سه‌شنبه آماده کنید، هر فرقی میان دو گروه می‌تواند از **تیمار** یا از **روز** باشد. هیچ آماری این دو را از هم جدا نمی‌کند: تیمار و دسته **درهم‌آمیخته**‌اند.

<div dir="ltr">

```text
confounded (bad)                 balanced (good)
day 1: T T T                     day 1: T C
day 2: C C C                     day 2: T C
                                 day 3: T C
```

</div>

راه: هر دسته (روز، دستگاه، فرد) **هر دو** گروه را داشته باشد. آن‌گاه دسته را در **فرمول طراحی** (13/03) می‌آوریم و اثرش را جدا می‌کنیم.

---

## ۳. گام ۱: طرح یک آزمایش واقعی (GSE52778)

**چرا؟** پیش از ساختن داده‌ی خودمان، طرح یک آزمایش منتشرشده را بخوانیم. جدول نمونه‌های GSE52778 را در 11/04 ساختید (`geo_counts.py`، بخش نخست خروجی آن). خلاصه‌اش:

<div dir="ltr">

```text
cell line   Untreated   Dexamethasone   Albuterol   Albuterol_Dexamethasone
N61311      GSM1275862  GSM1275863      GSM1275864  GSM1275865
N052611     ...         ...             ...         ...
N080611     ...         ...             ...         ...
N061011     ...         ...             ...         ...
```

</div>

- **چهار تکرار زیستی** (چهار فرد اهداکننده).
- **طرح جفتی:** هر فرد همه‌ی چهار تیمار را دارد. پس دگزامتازون را در **هر فرد** با شاهد **همان فرد** می‌سنجیم (همان «lines_up» در 11/04). تفاوت‌های ژنتیکی افراد از مقایسه بیرون می‌رود.
- **بی درهم‌آمیختگی:** هر فرد (یک «دسته») هر چهار تیمار را دارد.

ما بر روی همبستگی بیان (log2 CPM، ۱۵٬۱۹۶ ژن با CPM ≥ ۱ در دست‌کم ۴ نمونه) میان نمونه‌های بی‌تیمار و دگزامتازون این را دیدیم (روی جدول شمارش NCBI، 2026-10-28):

<div dir="ltr">

```
same donor, different treatment: n=4 mean r=0.9734
same treatment, different donor: n=12 mean r=0.9769
```

</div>

دو نمونه‌ی **یک فرد** با دو تیمار، و دو نمونه‌ی **یک تیمار** از دو فرد، کمابیش به یک اندازه همانندند. یعنی **هم فرد و هم تیمار** بیان را جابه‌جا می‌کنند. اگر فرد را در طرح نیاوریم، تفاوت افراد در «نویز» می‌ماند و توان آماری را کم می‌کند. در 13/03 همین را با PCA و فرمول `~ cell + dex` می‌بینید.

<details>
<summary>✋ امتحان کن: پژوهشگری ۳ موش شاهد را در آزمایشگاه A و ۳ موش تیمار را در آزمایشگاه B توالی‌یابی کرده است. چه می‌گویید؟</summary>

تیمار و آزمایشگاه درهم‌آمیخته‌اند: هر تفاوتی می‌تواند از آزمایشگاه (روش استخراج، دستگاه، زمان) باشد. هیچ تحلیلی این را درست نمی‌کند. باید دوباره طراحی شود: در هر آزمایشگاه هم شاهد و هم تیمار.

</details>

> 📺 **فیلم:** *The Difference Between Technical and Biological Replicates* (StatQuest): https://www.youtube.com/watch?v=Exk0OoRG0PQ · *StatQuest: RNA-seq – the problem with technical replicates*: https://www.youtube.com/watch?v=gKnfP2_Xdpo
> 📄 **مرجع:** Schurch NJ, et al. (2016). *How many biological replicates are needed in an RNA-seq experiment and which differential expression tool should you use?* RNA 22:839–851. https://doi.org/10.1261/rna.053959.115 · Liu Y, et al. (2014). *RNA-seq differential expression studies: more sequence or more replication?* Bioinformatics 30:301–304. https://doi.org/10.1093/bioinformatics/btt688

---

## ۴. گام ۲: ساختن داده‌ی مشترک بخش ۱۳

**چرا؟** داده‌ای می‌خواهیم که (۱) روی لپ‌تاپ در چند ثانیه تحلیل شود و (۲) پاسخش را بدانیم.

**طرح داده:**
- **مینی‌ژنوم:** برای هر یک از ۲۰ ژن، جایگاه ژن در GRCh38 (با ۱۰۰۰ باز در هر سو) از Ensembl 116 گرفته می‌شود و یک contig می‌سازد. آنوتیشن همه‌ی رونوشت‌ها (GTF) هم ساخته می‌شود (12/01).
- **ریدها:** شش نمونه، `ctrl_1..3` و `dex_1..3`. سطح پایه‌ی هر ژن همان **CPM نمونه‌های بی‌تیمار GSE52778** است و log2FC همان مقدار Expression Atlas (12/06). شمار تکه‌های هر ژن از توزیع **دوجمله‌ای منفی** (negative binomial) کشیده می‌شود تا تکرارها مانند داده‌ی واقعی با هم فرق کنند. کتابخانه **رشته‌ویژه** (dUTP)، ‏2×100 باز، با کیفیتی که در طول رید آرام پایین می‌آید.

<div dir="ltr">

```bash
conda activate rnaseq            # envs/rnaseq.yml
P=~/Bioinformatics_Learning-main/13_V2_RNAseq_Transcriptomics/99_scripts_data
column -t $P/shared/data/genes.tsv | head -9
bash $P/shared/data/make_data.sh ~/rnaseq
```

</div>

**خروجی واقعی (2026-10-28؛ کوتاه‌شده):**

<div dir="ltr">

```
symbol    ncbi_gene_id  ctrl_cpm  log2fc
NR3C1     2908          179.3     -1.0
FKBP5     2289          15.1      3.3
TSC22D3   1831          18.4      2.8
ZBTB16    7704          0.8       5.1
PER1      5187          7.3       3.0
DUSP1     1843          36.9      2.8
KLF15     28999         2.3       3.4
CRISPLD2  83716         39.0      2.4
NR3C1	ENSG00000113580	chr5	-	159582 bp	32 transcripts	canonical ENST00000394464
FKBP5	ENSG00000096060	chr6	-	157678 bp	97 transcripts	canonical ENST00000357266
...
SDHA	ENSG00000073578	chr5	+	40879 bp	109 transcripts	canonical ENST00000264932
ctrl_1	85093 pairs
ctrl_2	90034 pairs
ctrl_3	85545 pairs
dex_1	93333 pairs
dex_2	82453 pairs
dex_3	92245 pairs
e6f5a007947952ac6d0e48cc538c0b42  ref/transcripts_canonical.fa
26c2e18081d284895c5f7f91b5b7f4d0  reads/truth_counts.tsv
```

</div>

**توضیح خروجی:**
- ‏contig ‏NR3C1 ‏۱۵۹٬۵۸۲ باز است: ژن ۱۵۷٬۵۸۲ باز (12/01) + دو بار ۱۰۰۰. ‏۲۰ ژن روی هم ۹۶۷ رونوشت دارند.
- هر نمونه نزدیک به ۸۵ تا ۹۳ هزار جفت رید دارد (پیش‌بینی ۱۰۰ هزار). فرق اندازه‌ی کتابخانه‌ها بیشتر از EEF1A1 است که بیش از نیمی از ریدها را دارد (در `ctrl_1` ‏۵۱٬۵۰۰ از ۸۵٬۰۹۳، یعنی ۶۱٪). همین را در داده‌ی واقعی هم می‌بینید.
- دو عدد MD5 را با خروجی خود بسنجید: اگر یکسان‌اند، داده‌ی شما درست همان داده‌ی درس است (بذر تصادفی ثابت ۱۳). ما شبیه‌سازی را دو بار زدیم و محتوای فایل‌ها یکی بود.

### ۴.۱ پاسخ معلوم

<div dir="ltr">

```bash
cd ~/rnaseq
column -t reads/truth_counts.tsv | head -9
```

</div>

<div dir="ltr">

```
symbol    log2fc_true  ctrl_1  ctrl_2  ctrl_3  dex_1  dex_2  dex_3
NR3C1     -1.0         3489    2527    2458    1255   1142   1219
FKBP5     3.3          148     124     104     1066   1366   957
TSC22D3   2.8          66      46      94      588    587    513
ZBTB16    5.1          16      14      16      317    347    307
PER1      3.0          68      39      82      740    587    388
DUSP1     2.8          245     158     114     1302   507    1133
KLF15     3.4          6       10      19      146    88     162
CRISPLD2  2.4          414     195     304     2552   1351   651
```

</div>

این شمار **تکه‌هایی** است که از هر ژن ساخته شد. هر ابزار شمارش در 13/02 باید به همین برسد. گوناگونی تکرارها را ببینید: CRISPLD2 در `dex_1` ‏۲۵۵۲ و در `dex_3` ‏۶۵۱؛ ‏KLF15 در شاهدها تنها ۶ تا ۱۹ رید. با ۳ تکرار، چنین ژن‌هایی آزمون آماری سختی دارند (13/03).

### ۴.۲ یک رید

<div dir="ltr">

```bash
zcat reads/ctrl_1_R1.fastq.gz | head -4
```

</div>

<div dir="ltr">

```
@ctrl_1.1 NR3C1/1
AGCTTCTTTTCCCATTTAATGAAAAGCCTCCTATAGTTGTCGATGAGCATCAGTTGACTTATTATTGACAACGAAGTGCACATAATTTTCTTTTTCTCAT
+
FFFFFFFFFFFFFFFFFFFFFEEEEEEEEEEEEEEEDDDDDDDDDDCCCCCCCCBBBBBBBAAAAAAA@@@@@??????>>>>>=====<<<<;;;;:::
```

</div>

- نام رید **نام ژن** را دارد (`NR3C1`): تنها در داده‌ی شبیه‌سازی‌شده، برای سنجیدن. در داده‌ی واقعی این‌جا نام دستگاه و جای خوشه است (06/01).
- کیفیت از `F` ‏(Q37) در آغاز تا `:` ‏(Q25) در پایان پایین می‌آید؛ شبیه‌ساز خطاها را به همین نسبت می‌گذارد.

---

## ۵. گام ۳: ‏FastQC و MultiQC

‏FastQC را در 06/01 دیدید. در FastQC ‏0.13.0 (این محیط) گزینه‌ی کوتاه `-o` پذیرفته **نمی‌شود**؛ ‏`--outdir` در هر دو نسخه کار می‌کند.

<div dir="ltr">

```bash
mkdir -p qc
fastqc -q -t 2 --outdir qc reads/*.fastq.gz
multiqc -q -o qc qc
column -t -s $'\t' qc/multiqc_data/multiqc_general_stats.txt | cut -c1-110 | head -5
for f in qc/*_fastqc.zip; do unzip -p $f '*/summary.txt' | cut -f1,2; done | sort | uniq -c | sort -k3
```

</div>

**تکه‌به‌تکه:** ‏`unzip -p` یک فایل را از درون zip به خروجی می‌فرستد (بی باز کردن روی دیسک). ‏`summary.txt` برای هر بخش FastQC یک سطر PASS/WARN/FAIL دارد.

**خروجی واقعی (2026-10-28):**

<div dir="ltr">

```
Sample     fastqc-percent_duplicates  fastqc-percent_gc  fastqc-avg_sequence_length  fastqc-median_seq
ctrl_1_R1  76.57386624046632          44.0               100.0                       100
ctrl_1_R2  76.56799031647726          45.0               100.0                       100
ctrl_2_R1  77.8572539262945           45.0               100.0                       100
ctrl_2_R2  77.9061243530222           45.0               100.0                       100
     12 PASS	Adapter Content
     12 PASS	Basic Statistics
     12 PASS	Overrepresented sequences
     12 PASS	Per base N content
     12 PASS	Per base sequence content
     12 PASS	Per base sequence quality
      3 PASS	Per sequence GC content
      3 WARN	Per sequence GC content
      6 FAIL	Per sequence GC content
     12 PASS	Per sequence quality scores
     12 FAIL	Sequence Duplication Levels
     12 PASS	Sequence Length Distribution
```

</div>

**توضیح خروجی:**
- ‏**Sequence Duplication Levels: FAIL در هر ۱۲ فایل** (نزدیک به ۷۷٪ تکراری). برای DNA ژنومی این نشانه‌ی PCR زیاد است. ولی در RNA-seq ژن‌های پربیان (EEF1A1 با بیش از نیمی از ریدها) **ناگزیر** تکه‌های یکسان بسیار می‌سازند. این FAIL در RNA-seq **عادی** است و ریدهای تکراری را **پاک نمی‌کنیم** (پاک کردن، بیان ژن‌های پربیان را کم نشان می‌دهد). در داده‌ی ما با تنها ۲۰ ژن این عدد از داده‌ی واقعی با هزاران ژن بالاتر است.
- ‏**Per sequence GC content: FAIL یا WARN در ۹ فایل.** ‏FastQC انتظار یک منحنی زنگوله‌ای می‌دارد (ژنوم). ریدهای RNA-seq از چند ژن پربیان با GC ویژه‌ی خودشان می‌آیند و منحنی چندکوهانه می‌شود. باز هم **عادی**.
- ‏**Per base sequence quality: PASS**: کیفیت از Q37 به Q25 رسید (MultiQC: پایگاه ۱ ‏37.0، پایگاه ۱۰۰ ‏25.0)، هنوز بالای مرز ۲۰.
- ‏**Adapter content: PASS**: تکه‌ها (میانگین ۲۵۰ باز) از رید (۱۰۰) بلندترند. در داده‌ی واقعی با تکه‌های کوتاه، آداپتور می‌آید و باید با fastp (06/01) بریده شود.

**درس:** محدوده‌های پیش‌فرض FastQC برای DNA ژنومی ساخته شده‌اند. در RNA-seq چند FAIL عادی است؛ به جای PASS/FAIL، **همه‌ی نمونه‌ها را کنار هم** در MultiQC ببینید و نمونه‌ای را بیابید که با بقیه **فرق دارد**.

> 📺 **فیلم:** *RNA Seq Analysis: Quality Control* (BioCode Ltd.): https://www.youtube.com/watch?v=YM9rQFUA-GM · *Quality control* (Chipster Tutorials؛ با سنجش رشته‌ویژگی): https://www.youtube.com/watch?v=wpgRjgDMrH4
> 📄 **مرجع:** Ewels P, et al. (2016). *MultiQC.* Bioinformatics 32:3047–3048. https://doi.org/10.1093/bioinformatics/btw354 · Conesa A, et al. (2016). *A survey of best practices for RNA-seq data analysis.* Genome Biol 17:13. https://doi.org/10.1186/s13059-016-0881-8

---

## ۶. گام ۴: نشانه‌های ویژه‌ی RNA-seq (پس از هم‌ترازی)

برخی کیفیت‌ها تنها پس از هم‌ترازی (13/02) دیده می‌شوند:

| نشانه | پرسش | ابزار |
| :--- | :--- | :--- |
| **رشته‌ویژگی** | کتابخانه stranded است و کدام سو؟ | ‏Salmon (‏`lib_format_counts.json`)، RSeQC ‏`infer_experiment.py` |
| **پوشش ۵′ تا ۳′** | آیا RNA تجزیه شده است؟ (RNA شکسته بیشتر سر 3′ را می‌دهد) | ‏RSeQC ‏`geneBody_coverage.py` |
| **سهم rRNA** | کاهش rRNA خوب کار کرد؟ | شمار ریدها روی ژن‌های rRNA (13/05) |
| **سهم اینترون** | چقدر pre-mRNA آمده است؟ | ‏featureCounts (رید بی ژن) |
| **RIN** | کیفیت RNA پیش از توالی‌یابی | دستگاه Bioanalyzer (آزمایشگاه)؛ RIN ≥ ۷ خوب است |

در 13/02 رشته‌ویژگی را خودتان می‌سنجید، و می‌بینید تنظیم اشتباه آن همه‌ی شمارش‌ها را صفر می‌کند.

> 📄 **مرجع:** Levin JZ, et al. (2010). *Comprehensive comparative analysis of strand-specific RNA sequencing methods.* Nat Methods 7:709–715. https://doi.org/10.1038/nmeth.1491 · ‏RSeQC: https://rseqc.sourceforge.net/

---

## ۷. سه اشتباه رایج

1. **سه تکرار فنی به جای سه تکرار زیستی.** یک RNA سه بار توالی‌یابی‌شده تنها خطای دستگاه را می‌سنجد، نه گوناگونی زیستی را؛ نتیجه به جمعیت تعمیم نمی‌یابد.
2. **درهم‌آمیختن تیمار و دسته.** همه‌ی شاهدها یک روز و همه‌ی تیمارها روز دیگر: جبران‌ناپذیر. پیش از آزمایش جدول نمونه‌ها را با ستون‌های «روز»، «دستگاه» و «فرد» بنویسید.
3. **«درست کردن» FAILهای عادی.** پاک کردن ریدهای تکراری یا دور ریختن نمونه برای GC در RNA-seq کار نادرستی است. نمونه‌ی **متفاوت با بقیه** نگران‌کننده است، نه FAILی که همه دارند.

---

## 📘 برای کنجکاوها

- **توان آماری از پیش:** ابزارهایی چون `RNASeqPower` (R) و `PROPER` می‌گویند برای یافتن تغییر ۱٫۵ برابری با پراکندگی معین چند تکرار لازم است.
- ‏**‏UMI:** در روش‌های تک‌سلولی و برخی کتابخانه‌های کم‌ورودی، هر مولکول یک برچسب تصادفی می‌گیرد تا تکرار PCR از تکرار زیستی جدا شود؛ آن‌جا پاک کردن تکرارها درست است.
- **شبیه‌سازی:** ما شبیه‌ساز ساده‌ای نوشتیم (`simulate_reads.py`). ابزارهای کامل‌تر (polyester در R، RSEM) سوگیری‌های واقعی‌تر (GC، تکه‌شدن، اینترون) را هم می‌سازند.

---

## جمع‌بندی

- تکرار زیستی، نه فنی؛ دست‌کم ۳ و بهتر ۶. تکرار بیشتر از رید بیشتر ارزش دارد.
- کتابخانه: polyA یا کاهش rRNA؛ رشته‌ویژه (dUTP: رید ۱ از رشته‌ی مخالف).
- دسته را با تیمار درهم نیامیزید؛ طرح جفتی (GSE52778: هر فرد هر چهار تیمار) تفاوت افراد را بیرون می‌برد. در GSE52778 همانندی «یک فرد» و «یک تیمار» کمابیش یکسان بود (r ‏۰٫۹۷۳ و ۰٫۹۷۷).
- داده‌ی بخش ۱۳: مینی‌ژنوم ۲۰ ژن (Ensembl 116) و شش نمونه با پاسخ معلوم (`truth_counts.tsv`).
- ‏FastQC روی RNA-seq: FAIL تکرار و GC عادی است؛ نمونه‌های ناهمخوان را بجویید.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
conda env create -f envs/rnaseq.yml && conda activate rnaseq
bash $P/shared/data/make_data.sh ~/rnaseq                  # mini-genome + 6 simulated samples
fastqc -q -t 2 --outdir qc reads/*.fastq.gz                # FastQC 0.13: use --outdir, not -o
multiqc -q -o qc qc                                        # one report for all samples
unzip -p qc/X_fastqc.zip '*/summary.txt'                   # PASS/WARN/FAIL per module
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| تکرار زیستی / فنی | نمونه‌ی جدا / همان نمونه دوباره سنجیده |
| توان آماری | احتمال این‌که تغییر واقعی را بیابید |
| عمق (depth) | شمار ریدهای یک نمونه |
| ‏polyA / کاهش rRNA | دو راه برگزیدن RNA برای کتابخانه |
| رشته‌ویژه (stranded) | کتابخانه‌ای که رشته‌ی RNA را نگه می‌دارد |
| ‏dUTP | روش رایج رشته‌ویژه؛ رید ۱ از رشته‌ی مخالف ژن |
| اثر دسته (batch) | تفاوت فنی میان گروه‌هایی از نمونه‌ها (روز، دستگاه) |
| درهم‌آمیختگی (confounding) | وقتی دو عامل جدا نمی‌شوند |
| طرح جفتی | هر فرد در همه‌ی گروه‌ها؛ سنجش درون فرد |
| دوجمله‌ای منفی | توزیع شمارش‌ها با پراکندگی بیش از پواسون؛ پایه‌ی DESeq2 |
| ‏RIN | عدد یکپارچگی RNA (۱ تا ۱۰) |
| مینی‌ژنوم | ژنوم کوچک آموزشی از چند جایگاه ژن |

---

## منابع

**مقاله و مستند**
- ‏Conesa A, et al. (2016). *A survey of best practices for RNA-seq data analysis.* Genome Biol 17:13. https://doi.org/10.1186/s13059-016-0881-8
- ‏Schurch NJ, et al. (2016). *How many biological replicates are needed in an RNA-seq experiment and which differential expression tool should you use?* RNA 22:839–851. https://doi.org/10.1261/rna.053959.115
- ‏Liu Y, Zhou J, White KP (2014). *RNA-seq differential expression studies: more sequence or more replication?* Bioinformatics 30:301–304. https://doi.org/10.1093/bioinformatics/btt688
- ‏Levin JZ, et al. (2010). *Comprehensive comparative analysis of strand-specific RNA sequencing methods.* Nat Methods 7:709–715. https://doi.org/10.1038/nmeth.1491
- ‏Ewels P, et al. (2016). *MultiQC: summarize analysis results for multiple tools and samples in a single report.* Bioinformatics 32:3047–3048. https://doi.org/10.1093/bioinformatics/btw354
- ‏Himes BE, et al. (2014). *RNA-Seq transcriptome profiling identifies CRISPLD2 as a glucocorticoid responsive gene…* PLoS ONE 9:e99625. https://doi.org/10.1371/journal.pone.0099625
- راهنمای FastQC: https://www.bioinformatics.babraham.ac.uk/projects/fastqc/

**کتاب**
- ‏Korpelainen E, et al. (2014). *RNA-seq Data Analysis: A Practical Approach.* CRC Press. (فصل ۲: کنترل کیفیت؛ فصل ۸: طراحی و بیان افتراقی)
- ‏Buffalo V (2015). *Bioinformatics Data Skills*. O'Reilly. (فصل ۱۰: FASTQ و کیفیت)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Bioconductor for Genomic Data Science* (Johns Hopkins): https://www.coursera.org/learn/bioconductor
- ‏edX: *Introduction to Genomic Data Science* (UC San Diego): https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science
- ‏YouTube: *The Difference Between Technical and Biological Replicates* (StatQuest): https://www.youtube.com/watch?v=Exk0OoRG0PQ
- ‏YouTube: *StatQuest: RNA-seq – the problem with technical replicates*: https://www.youtube.com/watch?v=gKnfP2_Xdpo
- ‏YouTube: *RNA Seq Analysis: Quality Control* (BioCode Ltd.): https://www.youtube.com/watch?v=YM9rQFUA-GM

<sub>همه‌ی دستورها در 2026-10-28 روی سرور دوره اجرا شدند (FastQC 0.13.0، MultiQC 1.35، Python 3 در محیط `rnaseq`؛ Ensembl REST ‏release 116). همبستگی GSE52778 با جدول شمارش NCBI (11/04) حساب شد. DOIها با Crossref وارسی شدند؛ فیلم‌ها با noembed. فصل‌های کتاب Korpelainen در وارسی پایانی با فهرست کتاب سنجیده شوند.</sub>

</div>
