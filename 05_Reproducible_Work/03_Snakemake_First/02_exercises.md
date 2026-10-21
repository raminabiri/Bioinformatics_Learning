<div dir="rtl">

# تمرین‌ها: نخستین گردش کار با Snakemake

پیش از آغاز، Snakefile کامل درس را در پوشه‌ی تمرین بگذارید:

<div dir="ltr">

```bash
conda activate workflow
cd ~/smk_practice
cp ~/Bioinformatics_Learning-main/05_Reproducible_Work/99_scripts_data/03_Snakemake_First/workflow/Snakefile .
rm -rf counts stats
```

</div>

---

## تمرین ۱: پیش‌بینی پیش از اجرا
> **راهنمایی:** درس، بخش ۵ (`snakemake -n` و جدول `Job stats`).

پیش از اجرای هر دستوری، از روی Snakefile پیش‌بینی کنید `snakemake -n` چند کار (job) از هر قاعده نشان می‌دهد. سپس `snakemake -n` بزنید و بسنجید. بعد `snakemake -c 1` اجرا کنید.

---

## تمرین ۲: قاعده‌ی تازه، شمار ریدها
> **راهنمایی:** درس، بخش‌های ۴ و ۵ و اشتباه رایج ۱ (آکولادهای awk). خروجی تازه را به قاعده‌ی `all` هم بیفزایید.

یک قاعده‌ی تازه به نام `n_reads` بنویسید که برای هر نمونه، **شمار ریدهای** فایل R1 را در `n_reads/{sample}.txt` بنویسد (awk بخش ۰۱: `NR%4==1 {n++} END {print n}`). آن را به `rule all` بیفزایید. (الف) `snakemake -n` چند کار نشان می‌دهد و چرا `count_reads` در آن نیست؟ (ب) پس از اجرا، هر نمونه چند رید دارد؟ با جدول `stats/seqkit_stats.tsv` بسنجید.

---

## تمرین ۳: تنها یک فایل
> **راهنمایی:** درس، بخش ۴ («نام فایل خواسته را به Snakemake می‌دهید»).

‏`counts/minigut_sample2.tsv` را پاک کنید. با یک دستور، **تنها** همین فایل را دوباره بسازید (نه `all`). چگونه با `-n` مطمئن می‌شوید که کار دیگری اجرا نمی‌شود؟

---

## تمرین ۴: کدام فایل به کدام وابسته است؟
> **راهنمایی:** درس، بخش ۶ (`touch` و `reason`). به `input` هر قاعده نگاه کنید: کدام قاعده R2 را می‌خواند؟

‏`touch fastq/minigut_sample2_R2.fastq.gz` بزنید. **پیش‌بینی کنید** کدام کارها دوباره اجرا می‌شوند؛ سپس با `snakemake -n` بسنجید. چرا `count_reads` اجرا نمی‌شود؟

---

## تمرین ۵: پزشک Snakefile
> **راهنمایی:** درس، بخش ۷. هر خطا را یکی‌یکی درست کنید و دوباره `snakemake -n` بزنید.

این Snakefile **سه** اشتباه دارد. بی اجرا، آن‌ها را پیدا کنید؛ سپس در یک پوشه‌ی جدا بنویسید، اجرا کنید و با پیام‌های Snakemake بسنجید.

<div dir="ltr">

```python
rule all:
    input:
        expand("lengths/{sample}.txt", sample=["minigut", "minigut_sample"])

rule mean_length:
    input:
        "fastq/{sample}_R1.fastq.gz"
    output:
    "lengths/{sample}.txt"
    shell:
        "zcat {input} | awk 'NR%4==2 {s+=length($0); n++} END {print s/n}' > {output}"
```

</div>

---

## تمرین ۶: آیا شمارش درست است؟
> **راهنمایی:** ستون‌های `counts/…tsv` را با `awk` جابه‌جا کنید تا همانند `ground_truth.tsv` شوند؛ `diff <( … ) <( … )` دو خروجی را بی فایل میانی می‌سنجد (همان `<( )` ماژول ۰۱ Git).

ثابت کنید `counts/minigut_sample2.tsv` **دقیقاً** همان شمارهای `ground_truth.tsv` (بخش ۰۱) را برای این نمونه دارد.

---

## تمرین ۷ (فکری): `-c 4`
> **راهنمایی:** کادر کنجکاوهای درس. `/usr/bin/time -f "%e s"` زمان یک دستور را به ثانیه می‌دهد.

همه‌ی خروجی‌ها را پاک کنید و یک بار با `-c 1` و یک بار با `-c 4` اجرا کنید و زمان را بسنجید. چرا روی این داده تفاوت ناچیز است؟ روی ۲۰۰ نمونه‌ی واقعی چه انتظاری دارید؟

</div>
