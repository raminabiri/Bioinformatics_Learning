# پاسخ تشریحی: پایپلاین با Snakemake

> اجرا شده در 2026-10-13 و 2026-10-14 با Snakemake 9.25.2.

---

## تمرین ۱

```bash
snakemake -s workflow/Snakefile --cores 4 -n
```
```text
fastp                 2
fastqc_raw            4
fastqc_trimmed        4
multiqc               1
all                   1
total                12
```
1. `fastqc_raw` روی **هر فایل** اجرا می‌شود: ۲ نمونه × ۲ رید (R1، R2) = ۴. `fastp` روی **هر نمونه** (جفت R1/R2 با هم) اجرا می‌شود: ۲. تعداد jobها از wildcardهای هر rule و از `expand()` در rule ‏`multiqc` می‌آید.
2. ```bash
   snakemake -s workflow/Snakefile --cores 4
   jq '.summary.after_filtering.total_reads' results/fastp/*.json
   ```
   ```text
   99690
   49976
   ```
   دقیقاً همان اعداد `run_qc.sh` (ماژول 06/01)، چون پارامترها یکی‌اند. بازنویسی پایپلاین در ابزار دیگر **نباید** نتیجه را عوض کند. این مقایسه خودش یک آزمون است.
3. `Nothing to be done (all requested files are present and up to date).` همه‌ی خروجی‌ها از ورودی‌هایشان جدیدترند و کد و پارامترها تغییر نکرده‌اند.

---

## تمرین ۲

| تغییر | پیش‌بینی | نتیجه‌ی واقعی (`-n`) | دلیل |
| :--- | :--- | :--- | :--- |
| `touch` روی `minigut_sample2_R1` | fastqc_raw آن فایل، fastp نمونه‌ی ۲، fastqc_trimmed دو فایل نمونه‌ی ۲، multiqc، all | **۶ job**: fastp 1، fastqc_raw 1، fastqc_trimmed 2، multiqc 1، all 1 | زمان تغییر ورودی از خروجی‌ها جدیدتر شد |
| `length_required` ۵۰ ← ۶۰ | fastp هر دو نمونه و هر چه بعد از آن | fastp **۲** + fastqc_trimmed ۴ + multiqc + all، با پیام `Params have changed since last execution: ... before: 50 now: 60` | provenance: Snakemake پارامترهای اجرای قبلی را نگه داشته است |
| حذف `results/fastqc_raw/minigut_R2_fastqc.zip` | fastqc_raw همان فایل + multiqc | **`Nothing to be done`** ⚠️ | پایین را ببینید |

**سطر سوم نتیجه‌ی غیرمنتظره‌ای است.** Snakemake از **هدف** (`multiqc_report.html`) به عقب نگاه می‌کند. هدف وجود دارد و نسبت به ورودی‌های موجودش به‌روز است، پس دلیلی برای دوباره ساختن نمی‌بیند. **فایل میانی گم‌شده خودبه‌خود دوباره ساخته نمی‌شود.** برای ساختنش آن را صریحاً بخواهید:
```bash
snakemake -s workflow/Snakefile --cores 4 results/fastqc_raw/minigut_R2_fastqc.zip
```
```text
fastqc_raw        1
total             1
```
بعد از ساخته شدن، چون zip جدید از گزارش MultiQC جدیدتر است، اجرای بعدی **multiqc** را دوباره اجرا می‌کند (۲ job: multiqc و all). در عمل: اگر شک دارید خروجی‌ها با هم سازگارند، `--forcerun <rule>` یا `-F` (همه‌چیز) بزنید.

---

## تمرین ۳

```bash
snakemake -s workflow/Snakefile --cores 4 -n results/fastp/sample3.json
```
```text
MissingInputException in rule fastp in file ".../workflow/Snakefile", line 27:
Missing input files for rule fastp:
    output: results/trimmed/sample3_R1.fastq.gz, results/trimmed/sample3_R2.fastq.gz, results/fastp/sample3.json, results/fastp/sample3.html
    wildcards: sample=sample3
    affected files:
        ../../06_Metagenomics/data/raw/sample3_R1.fastq.gz
        ../../06_Metagenomics/data/raw/sample3_R2.fastq.gz
```
Snakemake نام فایل درخواستی را با الگوی `output` همه‌ی rule‌ها مقایسه کرد. با الگوی `results/fastp/{sample}.json` در rule ‏`fastp` جور شد و `sample=sample3` به دست آمد. بعد این wildcard را در `input` گذاشت و دید فایل وجود ندارد و هیچ rule‌ای هم نمی‌تواند آن را بسازد. این خطا **قبل از اجرای هر دستوری** در dry run پیدا شد. همین مزیت `-n` است: اشتباه تایپی در نام نمونه بعد از سه ساعت محاسبه پیدا نمی‌شود، بلکه در ثانیه‌ی اول.

---

## تمرین ۴ و ۵

پاسخ هر دو در [workflow/Snakefile_solution](../99_scripts_data/02_Workflows_Snakemake/workflow/Snakefile_solution) است. Snakefile درس را با `include:` وارد می‌کند، سه rule جدید (`qc_table`، `bowtie2_index`، `host_removal`) اضافه می‌کند، و یک هدف جدید با `default_target: True` تعریف می‌کند.

```bash
snakemake -s workflow/Snakefile_solution --cores 4
cat results/qc_summary.tsv
for f in results/clean/*_R1.fastq.gz; do echo "$(basename $f) $(zcat $f | awk 'END{print NR/4}')"; done
```
```text
5 of 5 steps (100%) done
sample	reads_before	reads_after	pct_kept
minigut	100000	99690	99.69
minigut_sample2	49986	49976	99.98
minigut_R1.fastq.gz 49845
minigut_sample2_R1.fastq.gz 24988
```
- فقط **۵ job** اجرا شد. مراحل QC از قبل وجود داشتند و Snakemake آن‌ها را دوباره اجرا نکرد.
- تعداد جفت‌ریدهای تمیز (۴۹٬۸۴۵ و ۲۴٬۹۸۸) **دقیقاً همان** ماژول 06/02 است.
- نکته‌های طراحی:
  - `multiext()` شش فایل ایندکس Bowtie2 را به‌عنوان خروجی اعلام می‌کند. اگر فقط یکی را اعلام کنید، Snakemake نمی‌داند ایندکس کامل است یا نه.
  - `idx=rules.bowtie2_index.output` وابستگی به ایندکس را صریح می‌کند.
  - در `qc_table` از `r"""..."""` استفاده شده تا `\t` و `$` در shell درست بمانند.

---

## تمرین ۶

1. **Bash** (یا حتی یک خط در ترمینال). کار یک‌باره و یک‌مرحله‌ای سربار مدیر جریان کار را نمی‌ارزد.
2. **Nextflow/nf-core** (مثلاً `nf-core/mag` یا `nf-core/taxprofiler`). پایپلاین استاندارد، نسخه‌دار، تست‌شده توسط جامعه و قابل ارجاع (DOI). پشتیبانی آماده از کلاستر و کانتینر دارد. داور به‌جای بررسی کد اختصاصی، نسخه‌ی پایپلاین و پارامترها را می‌بیند.
3. **Snakemake**. مراحل اختصاصی‌اند و یادگیری Snakemake برای کسی که Python می‌داند سریع است. ردیابی تغییرات، موازی‌سازی و `conda:` برای هر rule را به‌صورت رایگان می‌گیرید. ترکیب هم ممکن است: nf-core برای مراحل استاندارد و Snakemake برای تحلیل پایین‌دستی اختصاصی.
