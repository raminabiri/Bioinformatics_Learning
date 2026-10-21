<div dir="rtl">

# پاسخ تشریحی: نخستین گردش کار با Snakemake

خروجی‌ها از اجرای واقعی در 2026-10-21 (Snakemake 9.25.2، seqkit 2.13.0) گرفته شده‌اند. سرآیند Snakemake (تاریخ، نسخه، نشانی‌ها) برای کوتاهی برداشته شده است.

---

## پاسخ ۱: پیش‌بینی پیش از اجرا

پیش‌بینی: `count_reads` دو بار (یکی برای هر نمونه در `SAMPLES`)، `seqkit_stats` یک بار (بی wildcard؛ همه‌ی فایل‌ها با هم)، `all` یک بار. روی‌هم **۴**.

<div dir="ltr">

```bash
snakemake -n
```

</div>

<div dir="ltr">

```text
Job stats:
job             count
------------  -------
count_reads         2
seqkit_stats        1
all                 1
total               4
```

</div>

‏`all` هم یک کار شمرده می‌شود، هرچند دستوری ندارد.

---

## پاسخ ۲: قاعده‌ی تازه، شمار ریدها

قاعده‌ی تازه (در پایان Snakefile) و افزوده‌ی `rule all`:

<div dir="ltr">

```python
rule all:
    input:
        expand("counts/{sample}.tsv", sample=SAMPLES),
        "stats/seqkit_stats.tsv",
        expand("n_reads/{sample}.txt", sample=SAMPLES),

rule n_reads:
    input:
        "fastq/{sample}_R1.fastq.gz",
    output:
        "n_reads/{sample}.txt",
    shell:
        "zcat {input} | awk 'NR%4==1 {{n++}} END {{print n}}' > {output}"
```

</div>

<div dir="ltr">

```bash
snakemake -n
snakemake -c 1 -q
head n_reads/*.txt
```

</div>

<div dir="ltr">

```text
Job stats:
job        count
-------  -------
n_reads        2
all            1
total          3
==> n_reads/minigut_sample2.txt <==
24993

==> n_reads/minigut.txt <==
50000
```

</div>

- (الف) **۳** کار. `count_reads` و `seqkit_stats` نیستند چون خروجی‌هایشان از تمرین ۱ هست و تازه است؛ تنها خروجی‌های **تازه‌ی** `n_reads` نیستند. (`all` دوباره «اجرا» می‌شود چون ورودی تازه گرفته.)
- (ب) `minigut`: **۵۰٬۰۰۰**؛ `minigut_sample2`: **۲۴٬۹۹۳**؛ همان ستون `num_seqs` در `seqkit_stats.tsv`.

**اشتباه رایج:** آکولادهای تکی awk ← `NameError: The name 'n++' is unknown` (درس، اشتباه ۱).

---

## پاسخ ۳: تنها یک فایل

<div dir="ltr">

```bash
rm counts/minigut_sample2.tsv
snakemake -n counts/minigut_sample2.tsv
snakemake -c 1 counts/minigut_sample2.tsv
```

</div>

‏`-n` با نام فایل، جدول `Job stats` را با **تنها** `count_reads 1` و `total 1` نشان می‌دهد: چون فایلی جز `all` خواسته‌اید، `all` هم اجرا نمی‌شود. (اگر بی‌نام `snakemake -n` می‌زدید، `all` هم می‌آمد.)

---

## پاسخ ۴: کدام فایل به کدام وابسته است؟

پیش‌بینی: `count_reads` تنها **R1** را می‌خواند؛ `seqkit_stats` هر چهار فایل را. پس تنها `seqkit_stats` (و `all`).

<div dir="ltr">

```bash
touch fastq/minigut_sample2_R2.fastq.gz
snakemake -n
```

</div>

<div dir="ltr">

```text
rule seqkit_stats:
    reason: Updated input files: fastq/minigut_sample2_R2.fastq.gz
rule all:
    reason: Input files updated by another job: stats/seqkit_stats.tsv
```

</div>

‏Snakemake از روی `input` هر قاعده **دقیقاً** می‌داند چه چیزی به چه چیزی وابسته است. یک اسکریپت Bash همه را دوباره اجرا می‌کرد.

---

## پاسخ ۵: پزشک Snakefile

سه اشتباه:
1. ‏`"minigut_sample"` به‌جای `"minigut_sample2"` در `expand`.
2. ‏`"lengths/{sample}.txt"` زیر `output:` فرو نرفته (باید ۸ فاصله باشد، همانند `input`).
3. آکولادهای awk تکی‌اند.

پیام‌ها به ترتیب، هر بار پس از درست کردن اشتباه پیشین:

<div dir="ltr">

```text
### as written
MissingInputException in rule all in file "Snakefile", line 1:
Missing input files for rule all:
    affected files:
        lengths/minigut.txt
        lengths/minigut_sample.txt
```

</div>

با `output` تهی (اشتباه ۲)، هیچ قاعده‌ای `lengths/…` را نمی‌سازد، پس `all` ورودی‌هایش را «گمشده» می‌بیند. پس از درست کردن فرورفتگی:

<div dir="ltr">

```text
MissingInputException in rule mean_length in file "Snakefile", line 5:
Missing input files for rule mean_length:
    output: lengths/minigut_sample.txt
    wildcards: sample=minigut_sample
    affected files:
        fastq/minigut_sample_R1.fastq.gz
```

</div>

‏`wildcards: sample=minigut_sample` نام نادرست را آشکار می‌کند. پس از درست کردن نام، با `snakemake -c 1`:

<div dir="ltr">

```text
RuleException in rule mean_length in file "Snakefile", line 5:
NameError: The name 's+=length($0); n++' is unknown in this context. ...
```

</div>

این خطا تنها هنگام **اجرا** می‌آید، نه با `-n`. پس از دوتایی کردن آکولادها (`{{s+=length($0); n++}} END {{print s/n}}`):

<div dir="ltr">

```bash
snakemake -c 1 -q
head lengths/*
```

</div>

<div dir="ltr">

```text
==> lengths/minigut_sample2.txt <==
151

==> lengths/minigut.txt <==
126
```

</div>

میانگین طول ریدها: ۱۵۱ و ۱۲۶؛ همان `avg_len` در `seqkit_stats.tsv`.

**درس:** خطاها را **یکی‌یکی** درست کنید و پس از هر بار `snakemake -n` بزنید؛ یک خطا گاهی پیام خطای دیگری را پنهان می‌کند.

---

## پاسخ ۶: آیا شمارش درست است؟

<div dir="ltr">

```bash
GT=~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data/ground_truth.tsv
diff <(awk 'BEGIN{OFS="\t"} {print $2, $1}' counts/minigut_sample2.tsv | sort) \
     <(awk -F'\t' 'BEGIN{OFS="\t"} $1=="minigut_sample2" {print $3, $2}' $GT | sort) && echo "identical"
```

</div>

<div dir="ltr">

```text
identical
```

</div>

- ‏awk یکم: `counts` به شکل «شمار accession» است؛ جابه‌جا به «accession شمار».
- ‏awk دوم: از `ground_truth.tsv` تنها سطرهای این نمونه، ستون ۳ (accession) و ۲ (read_pairs).
- هر دو `sort` می‌شوند تا ترتیب مهم نباشد. `diff` چیزی چاپ نکرد (یکسان‌اند) و کد خروج ۰ داد، پس `&& echo` اجرا شد.

هر ۲۱ موجود با شمار یکسان. (`awk` در `counts` ستون‌ها را با فاصله جدا می‌کند و awk بی `-F` همین را می‌فهمد.)

---

## پاسخ ۷ (فکری): `-c 4`

<div dir="ltr">

```bash
rm -r counts n_reads stats
/usr/bin/time -f "%e s" snakemake -c 4 -q
rm -r counts n_reads stats
/usr/bin/time -f "%e s" snakemake -c 1 -q
```

</div>

<div dir="ltr">

```text
1.81 s
1.96 s
```

</div>

‏(زمان روی کامپیوتر شما فرق می‌کند.) تفاوت ناچیز است چون هر کار تنها کسری از ثانیه طول می‌کشد و بیشتر زمان، آماده شدن خود Snakemake است. روی ۲۰۰ نمونه‌ی واقعی که هر کدام چند دقیقه کار دارند، `-c 4` کارهای مستقل را **چهار‌تا‌چهارتا** اجرا می‌کند و زمان کل کمابیش یک‌چهارم می‌شود (اگر دیسک و حافظه کم نیاورند).

</div>
