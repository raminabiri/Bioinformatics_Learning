<div dir="rtl">

# درس: از رید به جدول شمارش؛ HISAT2، featureCounts، Salmon و kallisto

**بخش:** `13_V2_RNAseq_Transcriptomics` · **ماژول:** `02_Alignment_Quantification` · **پیش‌نیاز:** ماژول [13/01](../01_Design_QC/) (داده‌ی `~/rnaseq`)؛ SAM/BAM، CIGAR و `samtools` ([02/04](../../02_BioLinux/04_Align_Variant_Formats/))؛ GTF ([02/03](../../02_BioLinux/03_Annotation_Formats/))؛ `Rscript` ([04](../../04_R_Packages/)) · **زمان:** حدود ۹۰ دقیقه · **ابزار:** HISAT2 2.2.3، samtools 1.24، featureCounts 2.1.1 (subread)، Salmon 2.8.0، kallisto 0.52.0، R 4.5.3 با tximport 1.38.2 (محیط `rnaseq`) · **آخرین بازبینی:** 2026-10-28

> ✅ **وضعیت: اجرا شده.** همه‌ی خروجی‌ها واقعی‌اند (2026-10-28). روی مینی‌ژنوم هر گام کمتر از ۲ ثانیه و کمتر از ۲۲۰ مگابایت حافظه. ‏STAR تنها از مستندات (✍️؛ نمایه‌ی ژنوم انسان نزدیک به ۳۲ گیگابایت حافظه می‌خواهد).

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. بگویید چرا ریدهای RNA-seq به هم‌ترازکننده‌ی **آگاه از اتصال** (splice-aware) نیاز دارند.
2. با **HISAT2** ریدها را روی ژنوم هم‌تراز کنید و ریدهای **پیوندخورده** (spliced) و **چندجایی** را بشمارید.
3. با **featureCounts** جدول شمارش ژن بسازید و تنظیم **رشته‌ویژگی** را درست بزنید.
4. با **Salmon** و **kallisto** بی هم‌ترازی کامل بشمارید و با **tximport** به سطح ژن برسید.
5. هر روش را با **پاسخ معلوم** بسنجید و بدانید شمارش در سطح **رونوشت** چقدر نامطمئن است.

**پیش از آغاز:**

<div dir="ltr">

```bash
conda activate rnaseq && cd ~/rnaseq
P=~/Bioinformatics_Learning-main/13_V2_RNAseq_Transcriptomics/99_scripts_data
ls ref reads | head -12
```

</div>

---

## ۱. داستان

در 13/01 شش نمونه ساختید و می‌دانید از هر ژن دقیقاً چند تکه آمده است (`truth_counts.tsv`). اکنون باید از **ریدها** به همان جدول برسید، بی آن‌که پاسخ را ببینید. دو راه رایج هست و هر دو را می‌آزماییم:

<div dir="ltr">

```text
route 1 (alignment):      reads --HISAT2--> BAM on genome --featureCounts--> gene counts
route 2 (pseudoalignment): reads --Salmon/kallisto--> transcript counts --tximport--> gene counts
```

</div>

**پاسخ معلوم:** هر روش باید برای هر ژن و هر نمونه به عدد `truth_counts.tsv` برسد؛ برای نمونه NR3C1 در `ctrl_1`: **۳۴۸۹** تکه.

---

## ۲. مفهوم به زبان ساده

### ۲.۱ چرا هم‌ترازی RNA-seq فرق دارد؟

ریدها از **mRNA** آمده‌اند که اینترون‌هایش برداشته شده است. ولی ژنوم اینترون دارد. رید ۱۰۰ بازی که روی مرز دو اگزون نشسته، در ژنوم **دو تکه** دارد که میانشان صدها یا هزاران باز اینترون است:

<div dir="ltr">

```text
mRNA     ...exon2exon2exon2|exon3exon3exon3...
read            ==========|==========
genome   ...exon2exon2exon2|intron.....(240 bases)......intron|exon3exon3exon3...
alignment       ==========  -------------N-------------  ==========
CIGAR           44M         240N                         52M
```

</div>

هم‌ترازکننده‌ی DNA (Bowtie2، 13/05) چنین ریدی را نمی‌گذارد یا بد می‌گذارد. هم‌ترازکننده‌ی **آگاه از اتصال** (HISAT2، STAR) رید را می‌شکند و جای خالی را با `N` در CIGAR (02/04) می‌نویسد: «این‌جا باز نیست، اینترون پریده شده».

### ۲.۲ شبه‌هم‌ترازی (pseudoalignment)

برای **شمردن**، دانستن جای دقیق هر باز لازم نیست. کافی است بدانیم رید با **کدام رونوشت‌ها** جور است. ‏Salmon و kallisto ریدها را به k-merها (تکه‌های ۳۱ بازی) می‌شکنند و با نمایه‌ی k-merهای رونوشت‌ها می‌سنجند. سپس با الگوریتم **EM** (بیشینه‌سازی امید) ریدهای مشترک میان چند رونوشت را میان آن‌ها پخش می‌کنند. بسیار سریع است و BAM نمی‌سازد.

### ۲.۳ رشته‌ویژگی در شمارش

کتابخانه‌ی ما رشته‌ویژه‌ی **dUTP** است (13/01): رید ۱ از رشته‌ی **مخالف** ژن. ابزار شمارش باید این را بداند:

| ابزار | نام تنظیم | بی‌رشته | رید ۱ هم‌سو با ژن | رید ۱ ناهم‌سو (dUTP) |
| :--- | :--- | :---: | :---: | :---: |
| featureCounts | ‏`-s` | ‏`0` | ‏`1` | ‏**`2`** |
| HISAT2 | ‏`--rna-strandness` | (نگذارید) | ‏`FR` | ‏**`RF`** |
| Salmon | ‏`-l` | ‏`IU` | ‏`ISF` | ‏**`ISR`** |
| kallisto | | (پیش‌فرض) | ‏`--fr-stranded` | ‏**`--rf-stranded`** |

---

## ۳. گام ۱: نمایه و هم‌ترازی با HISAT2

**چرا؟** هم‌ترازکننده برای جست‌وجوی سریع یک **نمایه** (index) از ژنوم می‌سازد. اگر جای اتصال‌ها و اگزون‌ها را از GTF بدهیم، ریدهای روی مرزها را بهتر می‌گذارد.

<div dir="ltr">

```bash
mkdir -p idx bam
hisat2_extract_splice_sites.py ref/mini_genes.gtf > idx/ss.txt
hisat2_extract_exons.py ref/mini_genes.gtf > idx/exons.txt
wc -l idx/ss.txt idx/exons.txt
hisat2-build -p 2 --ss idx/ss.txt --exon idx/exons.txt ref/mini_genome.fa idx/mini > idx/build.log 2>&1
for s in ctrl_1 ctrl_2 ctrl_3 dex_1 dex_2 dex_3; do
  hisat2 -p 2 --rna-strandness RF -x idx/mini -1 reads/${s}_R1.fastq.gz -2 reads/${s}_R2.fastq.gz 2> bam/$s.hisat2.log \
    | samtools sort -@2 -o bam/$s.bam -
  samtools index bam/$s.bam
done
cat bam/ctrl_1.hisat2.log
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`hisat2_extract_splice_sites.py` | جای همه‌ی اینترون‌های GTF را بیرون بکش |
| ‏`--ss` و `--exon` | آن‌ها را در نمایه بگذار (هم‌ترازی اتصال‌های شناخته‌شده بهتر می‌شود) |
| ‏`-x idx/mini` | نمایه (نام پایه‌ی فایل‌های `idx/mini.*.ht2`) |
| ‏`--rna-strandness RF` | کتابخانه‌ی dUTP (جدول ۲.۳)؛ به برچسب `XS` در BAM کمک می‌کند |
| ‏`2> …hisat2.log` | گزارش هم‌ترازی (stderr) را در فایل بنویس |
| ‏`\| samtools sort -o … -` | خروجی SAM را مستقیم مرتب کن و BAM بنویس (02/04) |

**خروجی واقعی (2026-10-28):**

<div dir="ltr">

```
  911 idx/ss.txt
  233 idx/exons.txt
 1144 total
85093 reads; of these:
  85093 (100.00%) were paired; of these:
    52 (0.06%) aligned concordantly 0 times
    83086 (97.64%) aligned concordantly exactly 1 time
    1955 (2.30%) aligned concordantly >1 times
    ----
    52 pairs aligned concordantly 0 times; of these:
      27 (51.92%) aligned discordantly 1 time
    ----
    25 pairs aligned 0 times concordantly or discordantly; of these:
      50 mates make up the pairs; of these:
        17 (34.00%) aligned 0 times
        26 (52.00%) aligned exactly 1 time
        7 (14.00%) aligned >1 times
99.99% overall alignment rate
```

</div>

**توضیح خروجی:**
- ‏۹۱۱ جای اتصال و ۲۳۳ اگزون یکتا در GTF ‏۲۰ ژن. ساختن نمایه ۱٫۸ ثانیه و ۱۲۸ مگابایت؛ هر نمونه زیر یک ثانیه.
- ‏**۹۹٫۹۹٪** جفت‌ها هم‌تراز شدند. ‏**concordantly** یعنی هر دو رید با فاصله و جهت درست. ‏**۲٫۳٪ بیش از یک جا** (multi-mapped)؛ در بخش ۳.۲ می‌بینیم چرا.
- در داده‌ی واقعی انسان نرخ ۸۵ تا ۹۵٪ رایج است: اینترون‌ها، pre-mRNA، آلودگی، و ژن‌های تکراری.

### ۳.۱ ریدهای پیوندخورده

<div dir="ltr">

```bash
samtools view -c -F 0x904 bam/ctrl_1.bam
samtools view -F 0x904 bam/ctrl_1.bam | awk '$6 ~ /N/' | wc -l
samtools view -F 0x904 bam/ctrl_1.bam \
  | awk '{t[$3]++; if ($6 ~ /N/) s[$3]++} END {for (g in t) printf "%s\t%d\t%d\t%.0f%%\n", g, t[g], s[g], 100 * s[g] / t[g]}' \
  | sort -k2,2nr | head -8
```

</div>

**تکه‌به‌تکه:** ‏`-F 0x904` هم‌ترازی‌های نامشخص (0x4)، **ثانویه** (0x100) و تکمیلی (0x800) را کنار می‌گذارد تا هر رید یک بار شمرده شود. ‏`$6` ستون CIGAR است و `$3` نام contig، که این‌جا همان نام ژن است.

**خروجی واقعی:**

<div dir="ltr">

```
170169
40639
EEF1A1	102992	19921	19%
ACTB	14075	4013	29%
GAPDH	9503	5580	59%
RPLP0	7855	5142	65%
YWHAZ	7000	666	10%
NR3C1	6978	871	12%
PGK1	6958	1455	21%
TUBB	5817	768	13%
```

</div>

- از ۱۷۰٬۱۶۹ رید هم‌ترازشده، **۴۰٬۶۳۹ (۲۴٪)** روی دست‌کم یک اتصال‌اند. یک هم‌ترازکننده‌ی DNA همه‌ی این‌ها را از دست می‌داد.
- سهم ریدهای پیوندخورده به **ساختار ژن** بستگی دارد: GAPDH و RPLP0 اگزون‌های کوتاه بسیار دارند (بیش از ۶۰٪)؛ NR3C1 یک اگزون پایانی ۴ هزار بازی دارد (۱۲٪).

### ۳.۲ ریدهای چندجایی، بی ژن تکراری

مینی‌ژنوم تنها ۲۰ ژن دارد و هیچ ژن تکراری نیست. پس چرا ۲٫۳٪ جفت‌ها بیش از یک جا دارند؟

<div dir="ltr">

```bash
q=$(samtools view bam/ctrl_1.bam | awk '/NH:i:2/ && $3 == "GAPDH" {print $1; exit}')
samtools view bam/ctrl_1.bam | awk -v q=$q '$1 == q {print $1, $2, $3, $4, $6, $NF}'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
ctrl_1.15411 163 GAPDH 1515 44M240N52M1632N4M NH:i:2
ctrl_1.15411 419 GAPDH 1515 44M240N52M1632N4M NH:i:2
ctrl_1.15411 83 GAPDH 1558 1M258N34M1632N65M NH:i:2
ctrl_1.15411 339 GAPDH 1816 35M1632N65M NH:i:2
```

</div>

یک جفت رید، دو هم‌ترازی برای رید دوم (پرچم ۸۳ و ۳۳۹ = ۸۳ + ۲۵۶، «ثانویه»): یکی با تکه‌ی **یک‌بازی** `1M` پیش از یک اینترون ۲۵۸ بازی، و دیگری بی آن تکه. هر دو در **یک ژن**. ‏HISAT2 نمی‌تواند بگوید آن یک باز از اگزون پیشین است یا خطای توالی‌یابی، پس هر دو را با `NH:i:2` گزارش می‌کند. این‌ها «تکراری» واقعی نیستند؛ ولی featureCounts در پیش‌فرض ریدهای چندجایی را **نمی‌شمارد** (گام ۲).

> 📺 **فیلم:** *Setup RNA-Seq Pipeline from scratch: fastq (reads) to counts* (Bioinformagician): https://www.youtube.com/watch?v=lG11JjovJHE
> 📄 **مرجع:** Kim D, et al. (2019). *Graph-based genome alignment and genotyping with HISAT2 and HISAT-genotype.* Nat Biotechnol 37:907–915. https://doi.org/10.1038/s41587-019-0201-4 · ‏STAR (✍️، برای ژنوم کامل): Dobin A, et al. (2013). *STAR: ultrafast universal RNA-seq aligner.* Bioinformatics 29:15–21. https://doi.org/10.1093/bioinformatics/bts635

---

## ۴. گام ۲: شمارش با featureCounts؛ و دام رشته

<div dir="ltr">

```bash
mkdir -p counts
for s in 0 1 2; do
  featureCounts -T 2 -p --countReadPairs -s $s -t exon -g gene_name -a ref/mini_genes.gtf -o counts/fc_s$s.txt bam/*.bam > counts/fc_s$s.log 2>&1
  awk -F'\t' 'NR > 2 {a += $7} END {print "s='$s' assigned ctrl_1:", a}' counts/fc_s$s.txt
done
awk -F'\t' 'NR == 1 || $2 > 0' counts/fc_s2.txt.summary | cut -f1-3
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`-p --countReadPairs` | ریدها جفت‌اند؛ هر **جفت** (تکه) را یک بار بشمار |
| ‏`-s 0/1/2` | رشته‌ویژگی (جدول ۲.۳) |
| ‏`-t exon -g gene_name` | تنها اگزون‌ها را بشمار و آن‌ها را بر پایه‌ی `gene_name` به ژن گرد آور |
| ‏`-a` | فایل GTF |
| ستون ۷ خروجی | نخستین BAM (`ctrl_1`)؛ ستون‌های ۲ تا ۶ جای ژن و طول‌اند |

**خروجی واقعی (2026-10-28؛ هر اجرا ۰٫۶ ثانیه):**

<div dir="ltr">

```
s=0 assigned ctrl_1: 83135
s=1 assigned ctrl_1: 0
s=2 assigned ctrl_1: 83135
Status	bam/ctrl_1.bam	bam/ctrl_2.bam
Assigned	83135	87858
Unassigned_Unmapped	1	0
Unassigned_MultiMapping	5144	5765
```

</div>

**توضیح خروجی:**
- با **`-s 1`** (تنظیم وارونه) **صفر** جفت شمرده شد: همه‌ی ریدها «روی رشته‌ی نادرست» دیده شدند. اگر تنها نگاه کنید که برنامه بی‌خطا تمام شد، یک جدول تمام‌صفر به تحلیل می‌رود. **همیشه `.summary` را ببینید.**
- ‏`-s 0` و `-s 2` این‌جا یکسان‌اند، تنها چون در مینی‌ژنوم هیچ دو ژنی روی دو رشته هم‌پوشانی ندارند. در ژنوم کامل، `-s 0` ریدهای ژن‌های antisense را به اشتباه به ژن روبه‌رو هم می‌دهد.
- ‏`Unassigned_MultiMapping` ‏۵۱۴۴: همان هم‌ترازی‌های چندجایی بخش ۳.۲ (شمار هم‌ترازی‌ها، نه جفت‌ها).

<details>
<summary>✋ امتحان کن: اگر نمی‌دانید کتابخانه رشته‌ویژه است یا نه، چگونه می‌فهمید؟</summary>

‏featureCounts را با `-s 1` و `-s 2` روی یک نمونه بزنید و درصد `Assigned` را بسنجید: آن که بسیار بیشتر است درست است؛ اگر نزدیک به هم بودند، کتابخانه بی‌رشته است (`-s 0`). همین کار را `infer_experiment.py` ‏(RSeQC) و جدول `lib_format_counts.json` ‏Salmon (گام ۳) می‌کنند.

</details>

> 📄 **مرجع:** Liao Y, Smyth GK, Shi W (2014). *featureCounts: an efficient general purpose program for assigning sequence reads to genomic features.* Bioinformatics 30:923–930. https://doi.org/10.1093/bioinformatics/btt656

---

## ۵. گام ۳: ‏Salmon؛ و یک گزارش گمراه‌کننده

<div dir="ltr">

```bash
mkdir -p salmon
salmon index -t ref/transcripts_all.fa -i salmon/idx -k 31 > salmon/index.log 2>&1
salmon quant -i salmon/idx -l A -1 reads/ctrl_1_R1.fastq.gz -2 reads/ctrl_1_R2.fastq.gz -p 2 -o salmon_A/ctrl_1 > salmon_A.log 2>&1
grep -E '"expected_format"|"ISR"|"IU"|strand_mapping_bias' salmon_A/ctrl_1/lib_format_counts.json
grep -i warn salmon_A.log | head -1
```

</div>

**تکه‌به‌تکه:** نمایه از **رونوشت‌ها** ساخته می‌شود (۹۶۷ رونوشت ۲۰ ژن)، نه از ژنوم. ‏`-l A` یعنی «گونه‌ی کتابخانه را خودت بیاب».

**خروجی واقعی (2026-10-28؛ نمایه ۰٫۳ ثانیه):**

<div dir="ltr">

```
  "expected_format": "IU",
  "strand_mapping_bias": 0.0,
  "IU": 0,
  "ISR": 85093,
 WARN salmon_core::libtype: detected a *potential* strand bias > 1% in an unstranded protocol (strand_mapping_bias = 0.0000); see lib_format_counts.json for details
```

</div>

(سطر WARN را ما از کدهای رنگ ترمینال پاک کرده‌ایم.)

**یک ناهمخوانی واقعی:** ‏Salmon ‏۲٫۸ نتیجه گرفت کتابخانه **`IU`** (بی‌رشته) است، ولی در همان فایل **همه**‌ی ۸۵٬۰۹۳ تکه را `ISR` (رشته‌ویژه، رید ۱ وارونه) شمرد و ۰ تکه را `IU`. ما کتابخانه را `ISR` ساخته‌ایم؛ شمارش درست است و برچسب `expected_format` نادرست. هشدار هم همین را می‌گوید («سوگیری رشته در کتابخانه‌ی بی‌رشته»). **درس:** به خلاصه‌ی یک‌کلمه‌ای اعتماد نکنید؛ شمارش‌های هر سو را بخوانید و گونه‌ی کتابخانه را صریح بدهید:

<div dir="ltr">

```bash
for s in ctrl_1 ctrl_2 ctrl_3 dex_1 dex_2 dex_3; do
  salmon quant -i salmon/idx -l ISR -1 reads/${s}_R1.fastq.gz -2 reads/${s}_R2.fastq.gz -p 2 -o salmon_isr/$s > salmon_isr/$s.log 2>&1
done
grep -E '"expected_format"' salmon_isr/ctrl_1/lib_format_counts.json
head -3 salmon_isr/ctrl_1/quant.sf
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
  "expected_format": "ISR",
Name	Length	EffectiveLength	TPM	NumReads
ENST00000394464	6778	6528.000	14551.156131	3489.000
ENST00000415690	4961	4711.000	0.000000	0.000
```

</div>

- ‏`quant.sf` یک سطر برای هر **رونوشت** دارد: طول، **طول مؤثر** (طول منهای اثر اندازه‌ی تکه)، TPM و `NumReads` (شمار برآوردی).
- رونوشت canonical ‏NR3C1 ‏**۳۴۸۹** رید گرفت: درست همان پاسخ معلوم. ✅ (با `-l ISR` هنوز یک هشدار «ISR با IU مشاهده‌شده ناهمخوان است» می‌آید؛ همان اشکال برآورد بالا.)
- در Salmon ‏۲٫۸ گزینه‌ی قدیمی `--validateMappings` دیگر اثری ندارد (هشدار می‌دهد)؛ آن را ننویسید.

> 📄 **مرجع:** Patro R, et al. (2017). *Salmon provides fast and bias-aware quantification of transcript expression.* Nat Methods 14:417–419. https://doi.org/10.1038/nmeth.4197 · راهنمای گونه‌های کتابخانه: https://salmon.readthedocs.io/en/latest/library_type.html

---

## ۶. گام ۴: از رونوشت به ژن (tximport) و سنجش با پاسخ معلوم

<div dir="ltr">

```bash
Rscript $P/02_Alignment_Quantification/scripts/compare_counts.R salmon_isr counts/fc_s2.txt ref/tx2gene.tsv reads/truth_counts.tsv
```

</div>

اسکریپت با **tximport** شمار رونوشت‌ها را برای هر ژن جمع می‌زند (`tx2gene.tsv`)، جدول featureCounts را می‌خواند، هر دو را با `truth_counts.tsv` می‌سنجد و جدول ژن‌ها را برای 13/03 در `gene_counts_salmon.tsv` می‌نویسد. فایل R ساده است و در RStudio روی ویندوز هم اجرا می‌شود.

**خروجی واقعی (2026-10-28؛ ۰٫۲ ثانیه):**

<div dir="ltr">

```
reading in files with read.delim (install 'readr' package for speed up)
1 2 3 4 5 6 
summarizing abundance
summarizing counts
summarizing length
         truth salmon featureCounts
KLF15        6      6             6
ZBTB16      16     16            16
HPRT1       34     34            32
TBP         42     42            42
TSC22D3     66     66            65
PER1        68     68            67
FKBP5      148    148           146
DUSP1      245    245           243
SDHA       352    352           336
CRISPLD2   414    414           411
PPIA      1184   1184          1167
B2M       1921   1921          1884
TUBB      2909   2909          2877
PGK1      3479   3479          3457
NR3C1     3489   3489          3476
YWHAZ     3500   3500          3497
RPLP0     3928   3928          3738
GAPDH     4754   4754          4355
ACTB      7038   7038          6802
EEF1A1   51500  51500         50518
sum over all samples: truth 528703  salmon 528703  featureCounts 515962 
largest |salmon - truth|: 0 
featureCounts / truth, all samples: 0.9759 
```

</div>

**توضیح خروجی:**
- ‏**Salmon** در سطح ژن برای **هر** ژن و **هر** نمونه درست همان پاسخ معلوم را داد (بیشینه‌ی فرق ۰). ‏**featureCounts** ‏۹۷٫۶٪ را شمرد؛ کمبود بیشتر در ژن‌هایی است که ریدهای چندجایی دارند (GAPDH ‏۹۲٪، RPLP0 ‏۹۵٪).
- **چرا Salmon این‌قدر خوب است؟** بخشی از آن ساخته‌ی شبیه‌سازی است: همه‌ی ریدها از رونوشت‌های **شناخته‌شده** آمده‌اند، بی رید اینترونی، pre-mRNA یا ژن ناشناخته. در داده‌ی واقعی این‌ها هستند؛ Salmon آن‌ها را نمی‌بیند (یا به اشتباه به رونوشتی می‌دهد) و featureCounts آن‌ها را در `Unassigned_NoFeatures` می‌گذارد. در کار، دو روش در سطح ژن همبستگی بالایی دارند.

### ۶.۱ ولی در سطح رونوشت؟

همه‌ی ریدها از رونوشت **canonical** آمده‌اند. ‏Salmon چند درصد را به همان داد؟

<div dir="ltr">

```bash
python3 $P/02_Alignment_Quantification/scripts/isoform_share.py salmon_isr/ctrl_1/quant.sf ref/tx2gene.tsv ref/transcripts_canonical.fa
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
    gene  transcripts  reads  to_canonical  pct_canonical
   KLF15            8    6.0           0.0            0.0
  ZBTB16           64   16.0           0.0            0.0
   FKBP5           97  148.0          22.1           14.9
CRISPLD2           17  414.0         341.2           82.4
     B2M           26 1921.0        1850.0           96.3
   DUSP1           11  245.0         245.0          100.0
all genes: % of reads given to the canonical transcript = 99.7
```

</div>

- در کل ۹۹٫۷٪ درست؛ ولی برای **KLF15** و **ZBTB16** همه‌ی ریدها به رونوشت **دیگری** رفت، و برای FKBP5 تنها ۱۵٪ به رونوشت درست.
- چرا؟ برای ZBTB16 رونوشت `ENST00000865543` با رونوشت canonical در ۸۳۲۳ باز پایانی (از ۸۴۹۴) **یکسان** است و تنها در اگزون نخست فرق دارد (ما با Biopython سنجیدیم). ریدی که از آن بخش مشترک بیاید با هر دو جور است؛ EM با شمار کم رید (۱۶) نمی‌تواند درست پخش کند.
- **درس:** شمارش در سطح **ژن** قابل اعتماد است؛ در سطح **رونوشت** تنها وقتی رونوشت‌ها بخش‌های **ویژه**ی کافی دارند و رید بسیار است. برای بیشتر پرسش‌های «کدام ژن تغییر کرد؟»، به سطح ژن بروید (tximport).

### ‏۶.۲ ‏kallisto در یک نگاه

<div dir="ltr">

```bash
kallisto index -i kallisto/idx ref/transcripts_all.fa > kallisto/index.log 2>&1
kallisto quant -i kallisto/idx -o kallisto/ctrl_1 --rf-stranded reads/ctrl_1_R1.fastq.gz reads/ctrl_1_R2.fastq.gz > kallisto/ctrl_1.log 2>&1
grep -E "processed|pseudoaligned" kallisto/ctrl_1.log
```

</div>

<div dir="ltr">

```
[quant] processed 85,093 reads, 85,021 reads pseudoaligned
```

</div>

‏kallisto ‏۸۵٬۰۲۱ جفت از ۸۵٬۰۹۳ را جا داد (۷۲ جفت جا نیفتادند؛ علتش را نسنجیدیم)؛ پس از جمع در سطح ژن، بیشینه‌ی فرق با پاسخ معلوم ۳۶ رید بود (ما با pandas سنجیدیم). نتیجه‌اش بسیار نزدیک به Salmon است.

> 📺 **فیلم:** *Setup RNA-Seq Pipeline from scratch* (Bioinformagician؛ همان فیلم گام ۱)
> 📄 **مرجع:** Bray NL, et al. (2016). *Near-optimal probabilistic RNA-seq quantification.* Nat Biotechnol 34:525–527. https://doi.org/10.1038/nbt.3519 · Soneson C, Love MI, Robinson MD (2016). *Differential analyses for RNA-seq: transcript-level estimates improve gene-level inferences.* F1000Research 4:1521. https://doi.org/10.12688/f1000research.7563.2

---

## ۷. سه اشتباه رایج

1. **رشته‌ویژگی نادرست.** ‏`-s 1` به جای `-s 2` همه‌ی شمارش‌ها را صفر کرد؛ با کتابخانه‌ی بی‌رشته و `-s 2`، نیمی از ریدها گم می‌شوند. همیشه `.summary` featureCounts و `lib_format_counts.json` Salmon را بخوانید، نه تنها برچسب «expected_format».
2. **باور به شمار رونوشت‌ها.** ‏Salmon برای ۲۰ ژن شمار ژن را بی‌خطا داد ولی ریدهای سه ژن را به رونوشت نادرست سپرد. گزارش «ایزوفرم X بالا رفت» شاهد بیشتری می‌خواهد.
3. **آمیختن نسخه‌ی آنوتیشن.** نمایه‌ی Salmon یا GTF ‏featureCounts باید با همان نسخه‌ی ژنوم و آنوتیشنی ساخته شود که بعد به کار می‌برید (12/01: نسخه‌ی Ensembl و GENCODE). ‏GTF یک نسخه با BAM نسخه‌ی دیگر، ژن‌ها را جابه‌جا می‌شمارد.

---

## 📘 برای کنجکاوها

- ‏**STAR:** پرکاربردترین هم‌ترازکننده‌ی RNA-seq برای ژنوم کامل؛ سریع‌تر و دقیق‌تر از HISAT2 در اتصال‌های تازه، ولی نمایه‌ی انسان نزدیک به ۳۲ گیگابایت حافظه می‌خواهد. دستور پایه: `STAR --runMode genomeGenerate --genomeDir … --genomeFastaFiles … --sjdbGTFfile …` و `STAR --genomeDir … --readFilesIn R1 R2 --readFilesCommand zcat --quantMode GeneCounts` (✍️ از راهنمای STAR).
- ‏**‏Salmon با decoy:** برای داده‌ی واقعی، نمایه را با «decoy» (کل ژنوم) بسازید تا ریدهای اینترونی و بیرون از ژن به رونوشت‌ها چسبانده نشوند.
- ‏**‏nf-core/rnaseq:** خط لوله‌ی آماده‌ای که همه‌ی این گام‌ها (FastQC، STAR یا HISAT2، Salmon، featureCounts، MultiQC) را با یک دستور می‌زند (بخش ۲۰).

---

## جمع‌بندی

- ریدهای RNA-seq روی ژنوم **پیوندخورده‌اند**: HISAT2 ‏۲۴٪ آن‌ها را با `N` در CIGAR گذاشت؛ ۹۹٫۹۹٪ هم‌ترازی.
- ‏featureCounts: ‏`-p --countReadPairs -s 2` برای dUTP؛ `-s 1` نادرست همه را صفر کرد. ‏۹۷٫۶٪ تکه‌ها شمرده شدند؛ ریدهای چندجایی کنار رفتند.
- ‏Salmon و kallisto: شبه‌هم‌ترازی روی رونوشت‌ها؛ با tximport در سطح ژن Salmon درست همان پاسخ معلوم را داد. برچسب `expected_format` ‏Salmon ‏۲٫۸ نادرست بود و شمارش‌ها درست.
- سطح رونوشت نامطمئن است: ‏KLF15 و ZBTB16 همه‌ی ریدها را به رونوشت دیگر دادند.
- جدول `gene_counts_salmon.tsv` ورودی 13/03 است.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
hisat2_extract_splice_sites.py genes.gtf > ss.txt; hisat2_extract_exons.py genes.gtf > exons.txt
hisat2-build --ss ss.txt --exon exons.txt genome.fa idx/name
hisat2 -p 2 --rna-strandness RF -x idx/name -1 R1.fq.gz -2 R2.fq.gz 2> log | samtools sort -o s.bam -
samtools view -F 0x904 s.bam | awk '$6 ~ /N/' | wc -l                       # spliced reads
featureCounts -p --countReadPairs -s 2 -t exon -g gene_name -a genes.gtf -o fc.txt *.bam
salmon index -t transcripts.fa -i salmon_idx -k 31
salmon quant -i salmon_idx -l ISR -1 R1.fq.gz -2 R2.fq.gz -o out/sample     # read lib_format_counts.json
kallisto quant -i kallisto_idx -o out --rf-stranded R1.fq.gz R2.fq.gz
Rscript compare_counts.R salmon_dir fc.txt tx2gene.tsv truth.tsv           # tximport + check
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| آگاه از اتصال (splice-aware) | هم‌ترازکننده‌ای که می‌تواند رید را روی چند اگزون بشکند |
| رید پیوندخورده (spliced) | ریدی که روی مرز دو اگزون است؛ `N` در CIGAR |
| نمایه (index) | ساختار جست‌وجوی سریع از ژنوم یا رونوشت‌ها |
| ‏concordant | هر دو رید جفت با جهت و فاصله‌ی درست |
| رید چندجایی (multi-mapped) | ریدی با بیش از یک جای ممکن (`NH:i:n` با n > ۱) |
| هم‌ترازی ثانویه | جای دیگر یک رید چندجایی (پرچم 0x100) |
| شبه‌هم‌ترازی | یافتن رونوشت‌های سازگار با k-mer، بی هم‌ترازی باز به باز |
| ‏EM | الگوریتمی که ریدهای مشترک را میان رونوشت‌ها پخش می‌کند |
| طول مؤثر | طول رونوشت پس از کم کردن اثر اندازه‌ی تکه |
| ‏tximport | بسته‌ی R برای جمع شمار رونوشت‌ها در سطح ژن |
| ‏ISR / IU | کتابخانه‌ی رشته‌ویژه با رید ۱ وارونه / بی‌رشته (در Salmon) |
| ‏decoy | توالی ژنوم که به نمایه‌ی Salmon افزوده می‌شود تا ریدهای بیرون از رونوشت جذب نشوند |

---

## منابع

**مقاله و مستند**
- ‏Kim D, et al. (2019). *Graph-based genome alignment and genotyping with HISAT2 and HISAT-genotype.* Nat Biotechnol 37:907–915. https://doi.org/10.1038/s41587-019-0201-4
- ‏Dobin A, et al. (2013). *STAR: ultrafast universal RNA-seq aligner.* Bioinformatics 29:15–21. https://doi.org/10.1093/bioinformatics/bts635
- ‏Liao Y, Smyth GK, Shi W (2014). *featureCounts.* Bioinformatics 30:923–930. https://doi.org/10.1093/bioinformatics/btt656
- ‏Patro R, et al. (2017). *Salmon provides fast and bias-aware quantification of transcript expression.* Nat Methods 14:417–419. https://doi.org/10.1038/nmeth.4197
- ‏Bray NL, et al. (2016). *Near-optimal probabilistic RNA-seq quantification.* Nat Biotechnol 34:525–527. https://doi.org/10.1038/nbt.3519
- ‏Soneson C, Love MI, Robinson MD (2016). *Differential analyses for RNA-seq: transcript-level estimates improve gene-level inferences.* F1000Research 4:1521. https://doi.org/10.12688/f1000research.7563.2
- ‏Conesa A, et al. (2016). *A survey of best practices for RNA-seq data analysis.* Genome Biol 17:13. https://doi.org/10.1186/s13059-016-0881-8

**کتاب**
- ‏Korpelainen E, et al. (2014). *RNA-seq Data Analysis: A Practical Approach.* CRC Press. (فصل‌های هم‌ترازی و شمارش)
- ‏Buffalo V (2015). *Bioinformatics Data Skills*. O'Reilly. (فصل ۱۱: داده‌ی هم‌ترازی)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins): https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Genomic Data Science* (UC San Diego): https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science
- ‏YouTube: *Setup RNA-Seq Pipeline from scratch: fastq (reads) to counts* (Bioinformagician): https://www.youtube.com/watch?v=lG11JjovJHE

<sub>همه‌ی دستورها در 2026-10-28 روی سرور دوره اجرا شدند (محیط `rnaseq`). STAR تنها از راهنمای آن نوشته شد (✍️). DOIها با Crossref وارسی شدند؛ فیلم با noembed. فصل‌های کتاب Korpelainen در وارسی پایانی سنجیده شوند.</sub>

</div>
