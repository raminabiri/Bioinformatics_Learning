<div dir="rtl">

# پاسخ تشریحی: هم‌ترازی و شمارش

همه‌ی خروجی‌ها واقعی‌اند (HISAT2 2.2.3، samtools 1.24، featureCounts 2.1.1، Salmon 2.8.0؛ روی سرور دوره، 2026-10-28).

---

## پاسخ ۱: گزارش هم‌ترازی همه‌ی نمونه‌ها

<div dir="ltr">

```bash
for s in ctrl_1 ctrl_2 ctrl_3 dex_1 dex_2 dex_3; do
  printf "%s\t%s\t%s\n" $s "$(grep 'overall' bam/$s.hisat2.log | cut -d' ' -f1)" "$(grep 'concordantly >1' bam/$s.hisat2.log | awk '{print $2}')"
done
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
ctrl_1	99.99%	(2.30%)
ctrl_2	100.00%	(2.41%)
ctrl_3	100.00%	(2.49%)
dex_1	99.99%	(2.30%)
dex_2	100.00%	(2.62%)
dex_3	99.99%	(2.35%)
```

</div>

‏`$( … )` خروجی یک دستور را در جای خود می‌گذارد (01/09). همه‌ی نمونه‌ها نزدیک به ۱۰۰٪ هم‌تراز و ۲٫۳ تا ۲٫۶٪ چندجایی‌اند؛ هیچ نمونه‌ای جدا نیست. ‏dex_2 کمی بیشتر چندجایی دارد: در آن سهم GAPDH و ACTB (ژن‌های پرچندجایی، درس بخش ۳.۲) از EEF1A1 بیشتر است (13/01، تمرین ۴: EEF1A1 در dex_2 ‏۴۶٫۵٪). در داده‌ی واقعی، نمونه‌ای با نرخ هم‌ترازی چند درصد پایین‌تر از بقیه را باید بررسی کرد (آلودگی، rRNA، گونه‌ی دیگر).

---

## پاسخ ۲: سهم ریدهای پیوندخورده در سه ژن

<div dir="ltr">

```bash
for g in FKBP5 DUSP1 ZBTB16; do
  samtools view -F 0x904 bam/dex_1.bam $g | awk -v g=$g '{t++; if ($6 ~ /N/) s++} END {printf "%s\t%d\t%d\t%.0f%%\n", g, t, s, 100 * s / t}'
done
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
FKBP5	2130	577	27%
DUSP1	2604	493	19%
ZBTB16	634	42	7%
```

</div>

‏`samtools view BAM NAME` تنها ریدهای همان contig را می‌دهد (BAM باید ایندکس داشته باشد). ‏`-v g=$g` متغیر پوسته را به awk می‌دهد.

سهم ریدهای پیوندخورده به این بستگی دارد که چه بخشی از mRNA نزدیک مرز اگزون‌ها است. ‏FKBP5 ‏۱۱ اگزون دارد (12/02، تمرین ۲) با اگزون‌های میانی کوتاه (۸۴ تا ۲۴۰ باز): ۲۷٪. ‏ZBTB16 رونوشت ۸۴۹۴ بازی با یک اگزون پایانی بسیار بلند دارد؛ بیشتر ریدها درون آن اگزون‌اند: ۷٪. (برای دیدن اگزون‌ها: `awk -F'\t' '$1 == "ZBTB16" && $3 == "exon" && $9 ~ /ENST00000335953/ {print $5 - $4 + 1}' ref/mini_genes.gtf`.)

---

## پاسخ ۳: فراموش کردن `-p`

<div dir="ltr">

```bash
featureCounts -T 2 -s 2 -t exon -g gene_name -a ref/mini_genes.gtf -o counts/fc_reads.txt bam/ctrl_1.bam 2>&1 | grep -iE "error|paired"
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
||              Paired-end : no                                               ||
ERROR: Paired-end reads were detected in single-end read library : bam/ctrl_1.bam
```

</div>

‏featureCounts ‏2.1 کار را **نمی‌پذیرد** و جدولی نمی‌سازد. در نسخه‌های قدیمی‌تر featureCounts هر رید را جدا می‌شمرد و شمار هر ژن نزدیک به دو برابر می‌شد. این بی‌خطا پیش می‌رفت و تنها مقیاس را عوض می‌کرد، ولی برای آزمون‌هایی چون DESeq2 که بر پایه‌ی شمار **مستقل** کار می‌کنند، دو رید یک تکه را دو مشاهده‌ی جدا می‌پنداشت و اطمینان را بیش از اندازه نشان می‌داد. خطای آشکار بهتر از نتیجه‌ی نادرست بی‌صداست.

---

## پاسخ ۴: ریدهای چندجایی را بشماریم؟

<div dir="ltr">

```bash
featureCounts -T 2 -p --countReadPairs -s 2 -M -t exon -g gene_name -a ref/mini_genes.gtf -o counts/fc_M.txt bam/ctrl_1.bam > /dev/null 2>&1
featureCounts -T 2 -p --countReadPairs -s 2 -M --fraction -t exon -g gene_name -a ref/mini_genes.gtf -o counts/fc_Mf.txt bam/ctrl_1.bam > /dev/null 2>&1
for f in fc_s2 fc_M fc_Mf; do
  awk -F'\t' -v f=$f '$1 == "GAPDH" {print f, "GAPDH", $7} NR > 2 {a += $7} END {print f, "total", a}' counts/$f.txt
done
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
fc_s2 GAPDH 4355
fc_s2 total 83135
fc_M GAPDH 5402
fc_M total 88279
fc_Mf GAPDH 4753.00
fc_Mf total 85094.2
```

</div>

| تنظیم | GAPDH | کل | پاسخ معلوم |
| :--- | :---: | :---: | :---: |
| پیش‌فرض | ۴۳۵۵ | ۸۳٬۱۳۵ | ۴۷۵۴ و ۸۵٬۰۹۳ |
| ‏`-M` | ۵۴۰۲ | ۸۸٬۲۷۹ | |
| ‏`-M --fraction` | ‏**۴۷۵۳** | ‏**۸۵٬۰۹۴** | |

‏`-M --fraction` کمابیش درست همان پاسخ معلوم را می‌دهد. ‏`-M` تنها هر هم‌ترازی را یک بار کامل می‌شمارد؛ پس جفتی با دو جای ممکن **دو بار** شمرده می‌شود (GAPDH ‏۵۴۰۲، بیش از پاسخ). با `--fraction` هر جا سهم ۱/NH می‌گیرد (۰٫۵ برای NH=2) و جمع هر جفت یک می‌شود. این‌جا همه‌ی جاهای چندگانه در **یک ژن** بودند (بخش ۳.۲)، پس سهم‌ها همه به همان ژن برمی‌گشتند. در ژنوم واقعی با ژن‌های تکراری، `--fraction` ریدها را میان ژن‌های گوناگون پخش می‌کند، و بسیاری ترجیح می‌دهند ریدهای چندجایی را نشمارند (پیش‌فرض)، یا از Salmon بهره ببرند که آن‌ها را با EM پخش می‌کند.

---

## پاسخ ۵: ‏Salmon با رشته‌ی نادرست

<div dir="ltr">

```bash
salmon quant -i salmon/idx -l ISF -1 reads/ctrl_1_R1.fastq.gz -2 reads/ctrl_1_R2.fastq.gz -p 2 -o salmon_isf/ctrl_1 > salmon_isf.log 2>&1
grep -E "percent_mapped|num_mapped\"" salmon_isf/ctrl_1/aux_info/meta_info.json
grep -E '"num_compatible_fragments"|"num_incompatible|"ISR"' salmon_isf/ctrl_1/lib_format_counts.json
awk 'NR > 1 {s += $5} END {print "NumReads total", s}' salmon_isf/ctrl_1/quant.sf
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
  "num_mapped": 0,
  "percent_mapped": 0.0,
  "num_compatible_fragments": 0,
  "num_incompatible_fragments": 85093,
  "ISR": 85093,
NumReads total 0
```

</div>

**هیچ** تکه‌ای شمرده نشد: Salmon همه‌ی ۸۵٬۰۹۳ تکه را `ISR` دید و با `ISF` خواسته‌شده **ناسازگار** شمرد. همان رفتار featureCounts با `-s 1` (درس، گام ۲). اگر کسی تنها `quant.sf` را به DESeq2 بدهد، ستونی تمام‌صفر می‌گیرد. ‏`percent_mapped` در `meta_info.json` نخستین جایی است که باید ببینید.

---

## پاسخ ۶: رید بیشتر، رونوشت درست‌تر؟

<div dir="ltr">

```bash
python3 $P/02_Alignment_Quantification/scripts/isoform_share.py salmon_isr/dex_1/quant.sf ref/tx2gene.tsv ref/transcripts_canonical.fa
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
    gene  transcripts   reads  to_canonical  pct_canonical
    PER1           30   740.0         462.6           62.5
CRISPLD2           17  2552.0        1820.3           71.3
     B2M           26  2771.0        2771.0          100.0
    ACTB           64 10746.0       10746.0          100.0
  EEF1A1           87 51900.0       51899.0          100.0
   FKBP5           97  1066.0        1066.0          100.0
all genes: % of reads given to the canonical transcript = 98.9
```

</div>

‏ZBTB16 و KLF15 در شش سطر بدترین **نیستند**. با چند خط pandas (همانند اسکریپت) برای این دو در `dex_1` دیدیم: ‏ZBTB16 ‏۳۱۷ رید و **۱۰۰٪** به رونوشت canonical؛ ‏KLF15 ‏۱۴۶ رید و **۱۰۰٪**؛ FKBP5 ‏۱۰۶۶ رید و ۱۰۰٪. در `ctrl_1` این سه ۰٪، ۰٪ و ۱۵٪ بودند (با ۱۶، ۶ و ۱۴۸ رید).

با رید بیشتر، دست‌کم چند رید از بخش **ویژه**ی رونوشت canonical (اگزون نخست جداگانه) می‌آید و EM آن‌ها را نشانه‌ی همین رونوشت می‌گیرد؛ سپس ریدهای بخش مشترک را هم به همان می‌دهد. با چند رید انگشت‌شمار، شاید هیچ‌کدام از بخش ویژه نباشد. به جایش در `dex_1` اکنون PER1 (۶۲٫۵٪) و CRISPLD2 (۷۱٫۳٪) نادرست پخش شده‌اند. درس: کیفیت برآورد رونوشت به شمار رید **و** به ساختار رونوشت‌ها بستگی دارد و میان نمونه‌ها **ناپایدار** است؛ مقایسه‌ی ایزوفرم میان دو گروه با چنین نویزی گمراه‌کننده است.

---

## پاسخ ۷ (فکری): کدام راه؟

(الف) **Salmon + tximport** (یا kallisto). برای بیان افتراقی ژن، دقت سطح ژن بالا است، و برای ۲۰۰ نمونه بسیار سریع‌تر است (چند دقیقه در برابر ساعت‌ها برای STAR) و حافظه‌ی کم می‌خواهد. با نمایه‌ی **decoy** تا ریدهای بیرون از رونوشت‌ها جذب نشوند.

(ب) **STAR** (یا HISAT2) روی ژنوم. Salmon تنها رونوشت‌های **شناخته‌شده** را می‌بیند؛ اتصال تازه نیازمند هم‌ترازی روی ژنوم است. STAR اتصال‌های تازه را در `SJ.out.tab` گزارش می‌کند.

(ج) هر دو، و با **احتیاط**. ‏Salmon برآورد رونوشت می‌دهد، ولی تمرین ۶ نشان داد این برآورد با رید کم نادرست و ناپایدار است. ابزارهای ویژه‌ی «تغییر ایزوفرم» (DEXSeq، DRIMSeq، IsoformSwitchAnalyzeR) با تکرارهای زیستی کافی لازم‌اند، و بهتر است با هم‌ترازی روی ژنوم (ریدهای پیوندخورده‌ی ویژه‌ی هر ایزوفرم)، **رید بلند** (PacBio یا Nanopore، که هر رونوشت را یکجا می‌خواند؛ دوره‌ی جداگانه‌ی NGS) یا RT-PCR تأیید شود.

</div>
