# تمرین‌ها: پایپلاین با Snakemake

> پیش‌نیاز: داده‌ی بخش ۰۳ (`bash 03_Metagenomics/data/download.sh`)، و `snakemake`، `fastp`، `fastqc` و `multiqc` در PATH.
> ```bash
> cd 01_Computing_Foundations/05_Workflows_Pipelines
> ```

---

## تمرین ۱ (اجرا و خواندن خروجی)

1. dry run بگیرید. چند job ساخته می‌شود؟ چرا `fastqc_raw` چهار بار و `fastp` دو بار؟
2. workflow را با ۴ هسته اجرا کنید. جدول نهایی `jq .summary.after_filtering.total_reads results/fastp/*.json` را با درس 03/01 مقایسه کنید.
3. دوباره اجرا کنید. چه پیامی می‌گیرید و چرا؟

---

## تمرین ۲ (پیش‌بینی): چه چیزی دوباره اجرا می‌شود؟

برای هر تغییر، **قبل از اجرای `-n`** پیش‌بینی کنید چند job و از کدام rule‌ها دوباره اجرا می‌شود. بعد با `-n` بررسی کنید:
1. `touch ../../03_Metagenomics/data/raw/minigut_sample2_R1.fastq.gz`
2. تغییر `length_required` از ۵۰ به ۶۰ در `config.yaml`
3. پاک کردن `results/fastqc_raw/minigut_R2_fastqc.zip`

(بعد از تمرین، تغییرها را برگردانید و workflow را دوباره اجرا کنید تا همه‌چیز به‌روز شود.)

---

## تمرین ۳ (خطا): ورودی‌ای که وجود ندارد

از Snakemake بخواهید خروجی fastp نمونه‌ای را بسازد که داده‌اش وجود ندارد:
```bash
snakemake -s workflow/Snakefile --cores 4 -n results/fastp/sample3.json
```
پیام خطا چیست؟ Snakemake از کجا فهمید به کدام فایل‌ها نیاز دارد؟

---

## تمرین ۴ (rule جدید): جدول QC

یک rule به نام `qc_table` بنویسید که همه‌ی `results/fastp/*.json` را بخواند و فایل `results/qc_summary.tsv` با ستون‌های `sample, reads_before, reads_after, pct_kept` بسازد. (همان محاسبه‌ی تمرین ۶ ماژول 03/01 با `jq`.) آن را به هدف نهایی اضافه کنید.

---

## تمرین ۵ (چالشی): افزودن حذف میزبان

منطق ماژول 03/02 را به workflow اضافه کنید:
- rule `bowtie2_index` روی `../../03_Metagenomics/data/host/host_chr21_region.fa`
- rule `host_removal` با ورودی `results/trimmed/{sample}_R{1,2}.fastq.gz` و خروجی `results/clean/{sample}_R{1,2}.fastq.gz`، با منطق `samtools view -f 12 -F 256`

تعداد جفت‌رید `results/clean/` را با ماژول 03/02 مقایسه کنید.
راهنمایی: می‌توانید Snakefile درس را با `include:` در یک Snakefile جدید وارد کنید.

---

## تمرین ۶ (مفهومی)

برای هر سناریو بگویید Bash، Snakemake یا Nextflow/nf-core را انتخاب می‌کنید و چرا:
1. شمارش یک‌باره‌ی ژن‌های یک فایل GFF.
2. تحلیل متاژنومی ۳۰۰ نمونه روی کلاستر دانشگاه، با پایپلاین استاندارد و قابل دفاع برای داور.
3. پایان‌نامه‌ای با ۵ مرحله‌ی تحلیل اختصاصی که ابزار آماده ندارد.
