<div dir="rtl">

# پاسخ تشریحی: برداشتن DNA میزبان

خروجی‌ها از اجرای واقعی در 2026-10-13 (Bowtie2 2.5.4، samtools 1.20، wgsim با دانه‌ی ۴۲) گرفته شده‌اند. عددهای شما باید **همین‌ها** باشند.

---

## پاسخ ۱: حساسیت و ویژگی

<div dir="ltr">

```bash
zcat host/clean/minigut_spiked_R1.fastq.gz | awk 'NR%4==1' \
  | sed -E 's/^@?(HUMAN_chr[0-9]+|NC_[0-9.]+).*/\1/' | sort | uniq -c
```

</div>

<div dir="ltr">

```text
   4725 HUMAN_chr1
  21018 NC_000913.3
  28827 NC_006347.1
```

</div>

**(الف)**

| مبدأ | ورودی | مانده | رفته |
| :--- | ---: | ---: | ---: |
| باکتری (*E. coli* + *B. fragilis*) | 49,845 | 49,845 | 0 (۰٪) |
| انسان chr21 (در مرجع) | 5,000 | 0 | 5,000 (۱۰۰٪) |
| انسان chr1 (بیرون از مرجع) | 5,000 | 4,725 | 275 (۵٫۵٪) |

**(ب)**
- حساسیت برای نواحی درون مرجع: 5000 / 5000 = **۱۰۰٪**
- حساسیت برای همه‌ی ریدهای انسانی: (5000 + 275) / 10000 = **۵۲٫۸٪**
- ویژگی: 49845 / 49845 = **۱۰۰٪**

**(ج)** «حساسیت برداشتن میزبان» باید نسبت به **همه‌ی** ریدهای انسانی واقعی باشد: ۵۲٫۸٪. عدد ۱۰۰٪ تنها می‌گوید هم‌ترازی خوب کار کرد؛ گلوگاه این‌جا الگوریتم نیست، **مرجع** است. گزارش ۱۰۰٪ بی این شرط گمراه‌کننده است. با کل ژنوم انسان این دو عدد به هم نزدیک می‌شوند (تمرین ۵).

---

## پاسخ ۲: ‏`--un-conc` در برابر `-f 12`

**(ب)**

<div dir="ltr">

```bash
zcat host/unconc_R1.fastq.gz | awk 'NR%4==1' \
  | sed -E 's/^@?(HUMAN_chr[0-9]+|NC_[0-9.]+).*/\1/' | sort | uniq -c
```

</div>

<div dir="ltr">

```text
   4926 HUMAN_chr1
      2 HUMAN_chr21
  21018 NC_000913.3
  28827 NC_006347.1
```

</div>

| مبدأ | `-f 12` | `--un-conc` |
| :--- | ---: | ---: |
| ‏chr21 مانده | 0 | **2** |
| ‏chr1 مانده | 4,725 | **4,926** |
| باکتری مانده | 49,845 | 49,845 |

**(ج)**

<div dir="ltr">

```bash
zcat host/unconc_R1.fastq.gz | awk 'NR%4==1' | grep chr21
samtools view host/bam/minigut_spiked.host.bam | awk '$2 == 97 || $2 == 145' | cut -f 1-9
```

</div>

<div dir="ltr">

```text
HUMAN_chr21_chr21part_303783_304289_..._991    97   chr21part  303783  32  126M  =  304164  0
HUMAN_chr21_chr21part_303783_304289_..._991    145  chr21part  304164  42  126M  =  303783  0
HUMAN_chr21_chr21part_405423_405938_..._107d   97   chr21part  405423  1   126M  =  405813  0
HUMAN_chr21_chr21part_405423_405938_..._107d   145  chr21part  405813  1   126M  =  405423  0
```

</div>

‏(نام‌ها برای پهنای صفحه کوتاه شده‌اند.)

- ‏`97` = PAIRED + MREVERSE + READ1 و `145` = PAIRED + REVERSE + READ2: **هر دو رید نشسته‌اند** (بیت ۴ خاموش)، ولی بیت **PROPER_PAIR (2) خاموش است**.
- نام رید wgsim جایگاه قطعه‌ی واقعی را دارد: ‏303783 تا 304289 = **۵۰۷ باز**؛ 405423 تا 405938 = **۵۱۶ باز**. هر دو بیشتر از مرز پیش‌فرض `-X 500`اند، پس Bowtie2 جفت را concordant نمی‌داند و `--un-conc` آن را بیرون می‌دهد، با آنکه هر دو رید انسانی‌اند.
- تفاوت chr1 (۴۹۲۶ − ۴۷۲۵ = ۲۰۱ جفت): ‏**۱۹۶ جفت** که تنها یک ریدشان روی تکرارهای مشترک chr21 نشسته (FLAGهای 73/133، 69/137، 89/165، 101/153) و **۵ جفت** که هر دو ریدشان نشسته‌اند ولی proper نیستند (97/145، 81/161، 65/129). `-f 12` همه را برمی‌دارد: یک رید انسانی برای مشکوک کردن کل جفت بس است. (۷۴ جفت دیگر chr1 به‌شکل proper نشسته‌اند و با هر دو روش می‌روند: 74 + 196 + 5 = 275.)

**(د)** با `-X 1000`:

<div dir="ltr">

```bash
bowtie2 -p 4 --very-sensitive -X 1000 -x host/index/host \
  -1 host/spiked/minigut_spiked_R1.fastq.gz -2 host/spiked/minigut_spiked_R2.fastq.gz \
  --un-conc-gz host/unconcX_R%.fastq.gz -S /dev/null 2> host/logs/unconcX.log
zcat host/unconcX_R1.fastq.gz | awk 'NR%4==1' \
  | sed -E 's/^@?(HUMAN_chr[0-9]+|NC_[0-9.]+).*/\1/' | sort | uniq -c
```

</div>

<div dir="ltr">

```text
   4926 HUMAN_chr1
  21018 NC_000913.3
  28827 NC_006347.1
```

</div>

دو جفت chr21 رفتند، ولی این **راه‌حل همگانی نیست**:
1. پراکنش درازای قطعه در هر کتابخانه فرق دارد؛ همیشه دنباله‌ای درازتر از هر `-X` هست.
2. جفت‌های تک‌رید (۱۹۶ جفت chr1) با `-X` درست نمی‌شوند.

راه درست، **عوض کردن منطق** است: «جفتی را نگه دار که هیچ ریدش ننشسته» (`-f 12`)، نه «جفتی که concordant ننشسته».

---

## پاسخ ۳: رمزگشایی FLAG

<div dir="ltr">

```bash
for f in 77 141 99 147 97 145 73 133; do
  printf "%s\t" $f
  samtools flags $f | cut -f 3 | tr '\n' '\t'
  samtools view host/bam/minigut_spiked.host.bam | awk -v f=$f '$2 == f' | wc -l
done
```

</div>

| FLAG | معنی | شمار رکورد | در برداشتن میزبان |
| :-: | :--- | ---: | :--- |
| 77 | PAIRED, UNMAP, MUNMAP, READ1 | 54,570 | **می‌ماند** (هر دو ننشسته) |
| 141 | PAIRED, UNMAP, MUNMAP, READ2 | 54,570 | **می‌ماند** |
| 99 | PAIRED, PROPER_PAIR, MREVERSE, READ1 | 2,548 | می‌رود |
| 147 | PAIRED, PROPER_PAIR, REVERSE, READ2 | 2,548 | می‌رود |
| 97 | ‏PAIRED, MREVERSE, READ1 (نه proper) | 4 | می‌رود (همان نشت `--un-conc`) |
| 145 | PAIRED, REVERSE, READ2 | 4 | می‌رود |
| 73 | ‏PAIRED, MUNMAP, READ1 (خودش نشسته، جفتش نه) | 50 | می‌رود |
| 133 | ‏PAIRED, UNMAP, READ2 (خودش ننشسته، جفتش نشسته) | 50 | می‌رود |

‏77 و 141 دقیقاً هم‌شمارند (۵۴٬۵۷۰) چون **دو نیمه‌ی یک جفت**‌اند: هر جفت پاک یک رکورد 77 (R1) و یک رکورد 141 (R2) دارد. همین شمار جفت‌های پاک است: 49,845 + 4,725. به همین دلیل 73 و 133 هم هم‌شمارند. جفت‌های proper در جهت دیگر 83/163‌اند (۲٬۵۲۴ رکورد هر کدام).

---

## پاسخ ۴: MAPQ

**(الف)** با `-q` (کمترین MAPQ) در چهار مرز، شمار تجمعی:

<div dir="ltr">

```bash
for q in 0 2 10 30; do
  printf "MAPQ>=%s\t" $q
  samtools view -F 4 -q $q host/bam/minigut_spiked.host.bam | grep -c '^HUMAN_chr21'
done
```

</div>

<div dir="ltr">

```text
MAPQ>=0	10000
MAPQ>=2	4076
MAPQ>=10	4026
MAPQ>=30	3300
```

</div>

با تفریق: ۰–۱: **۵۹۲۴**، ۲–۹: **۵۰**، ۱۰–۲۹: **۷۲۶**، ≥۳۰: **۳۳۰۰**. ‏۵۹٪ ریدهای chr21 MAPQ صفر یا یک دارند.

**(ب)**

<div dir="ltr">

```python
# kmer_repeats.py: how many 40-mers occur more than once in a FASTA file?
seq = ""
with open("host/ref/host_chr21_region.fa") as f:
    for line in f:
        if not line.startswith(">"):
            seq += line.strip().upper()

k = 40
counts = {}
for i in range(len(seq) - k + 1):
    kmer = seq[i:i + k]
    if "N" in kmer:
        continue
    counts[kmer] = counts.get(kmer, 0) + 1

repeated = 0
for n in counts.values():
    if n > 1:
        repeated += 1
print("distinct 40-mers", len(counts), "repeated", repeated, round(repeated / len(counts) * 100, 1), "%")
```

</div>

<div dir="ltr">

```text
distinct 40-mers 276706 repeated 121329 43.8 %
```

</div>

**۴۳٫۸٪** از ۴۰-مرهای این ناحیه بیش از یک بار آمده‌اند: ناحیه یک **تکه‌ی تکراری بزرگ** دارد (برای نمونه بازهای آغاز ناحیه در جایگاه 381,778 دوباره آمده‌اند)، و دو بلوک `N` (کمابیش ۲۰٪ ناحیه). ریدی که از چنین تکه‌ای می‌آید، دو جای هم‌امتیاز دارد؛ Bowtie2 نمی‌تواند یکی را برگزیند و MAPQ صفر یا یک می‌دهد. در کل ژنوم انسان هم کمابیش نیمی از توالی تکراری است (Alu، L1، تکرارهای قطعه‌ای، سانترومرها).

- ‏`counts.get(kmer, 0) + 1`: اگر کلید نبود، از صفر آغاز کن (بخش ۰۳).
- ‏`continue`: این k-mer را رد کن و به بعدی برو.

**(ج)**

<div dir="ltr">

```bash
samtools view -F 4 -q 30 host/bam/minigut_spiked.host.bam | cut -f 1 | sort -u | grep -c chr21
```

</div>

<div dir="ltr">

```text
1650
```

</div>

‏(`cut -f 1 | sort -u` = نام‌های یکتا، یعنی **جفت‌ها**.) تنها **۱٬۶۵۰ از ۵٬۰۰۰ جفت chr21** دست‌کم یک رید با MAPQ ≥ ۳۰ دارند. با پیشنهاد همکار، **۳٬۳۵۰ جفت انسانی (۶۷٪)** در داده‌ی «پاک» می‌ماندند. پرسش برداشتن میزبان «انسانی است؟» است، نه «دقیقاً کجای ژنوم انسان؟»؛ MAPQ به پرسش دوم پاسخ می‌دهد.

---

## پاسخ ۵: مرجع کامل‌تر

**(الف)**

<div dir="ltr">

```bash
mkdir -p host/index_full
cat host/ref/host_chr21_region.fa host/ref/human_chr1_region.fa > host/index_full/host_full.fa
IN=host/spiked REF=host/index_full/host_full.fa IDX=host/index_full/host_full \
  bash $S/run_host_removal.sh minigut_spiked
```

</div>

<div dir="ltr">

```text
== building Bowtie2 index from host/index_full/host_full.fa
== minigut_spiked
   16.71% overall alignment rate   clean pairs: 49845
```

</div>

**(ب)**

<div dir="ltr">

```text
  21018 NC_000913.3
  28827 NC_006347.1
```

</div>

| مبدأ | ورودی | مانده | رفته |
| :--- | ---: | ---: | ---: |
| باکتری | 49,845 | 49,845 | ۰٪ |
| انسان chr21 | 5,000 | 0 | ۱۰۰٪ |
| انسان chr1 | 5,000 | 0 | ۱۰۰٪ |

حساسیت برای همه‌ی ریدهای انسانی از ۵۲٫۸٪ به **۱۰۰٪** رسید و ویژگی ۱۰۰٪ ماند.

**(ج)** **کل ژنوم** میزبان را به کار ببرید. T2T-CHM13 کمابیش ۲۰۰ مگاباز توالی دارد که در GRCh38 نیست (سانترومرها و تکرارها)؛ ریدهای این نواحی با GRCh38 نمی‌روند. سوی دیگر: **مرجع بزرگ‌تر، خطر رفتن ریدهای میکروبی را بالا می‌برد**؛ ژنوم انسان تکه‌هایی همانند توالی میکروبی دارد (آلودگی‌های قدیمی اسمبلی، ژن‌های بسیار حفاظت‌شده مانند rRNA). Hostile برای همین نواحی مشترک T2T-CHM13 با ژنوم‌های میکروبی را می‌پوشاند: حساسیت بالا بماند و ریدهای باکتریایی از دست نروند. روی داده‌ی کوچک ما این اثر دیده نمی‌شود، چون مرجع تنها ۸۰۰ کیلوباز است.

---

## پاسخ ۶: بند Methods

نمونه:
> *Host reads were removed by aligning quality-trimmed read pairs to the human reference genome (<T2T-CHM13v2.0 or GRCh38 with alt and decoy sequences; index source and version>) with Bowtie2 v2.5.4 (`--very-sensitive`). A read pair was retained only if neither mate aligned to the host (samtools v1.20 `view -f 12 -F 256`, followed by `samtools fastq`); no mapping-quality filter was applied. The proportion of host reads per sample is reported in Table S<n>. The procedure was verified on a spike-in control in which 10,000 simulated human read pairs (wgsim, seed 42) were added to a sample of known bacterial composition: all bacterial pairs were retained, and all human pairs from regions present in the reference were removed.*

آنچه داور می‌خواهد: مرجع و نسخه‌اش، منطق نگه داشتن جفت‌ها (دقیقاً کدام FLAG)، **نبودن** پالایش MAPQ، و درصد میزبان هر نمونه.

</div>
