# درس: پایپلاین و مدیریت جریان کار با Snakemake

**بخش:** `05_Reproducible_Work` · **ماژول:** `02_Workflows_Snakemake` · **پیش‌نیاز:** ماژول‌های ۰۱ تا ۰۷؛ داده‌ی بخش ۰۶ · **زمان:** ۲ ساعت · **ابزار:** Snakemake 9.25.2، fastp 0.23.4، FastQC 0.12.1، MultiQC 1.25.1 · **آخرین تست:** 2026-10-13

---

## ۱. مسئله

اسکریپت `run_qc.sh` در ماژول 06/01 یک **پایپلاین خطی** است: FastQC، بعد fastp، بعد FastQC و MultiQC. برای دو نمونه خوب کار می‌کند. حالا تصور کنید:
- **۲۰۰ نمونه** دارید و fastp یکی از آن‌ها وسط کار شکست می‌خورد. باید همه را از اول اجرا کنید؟
- یک پارامتر fastp را عوض می‌کنید. کدام خروجی‌ها کهنه شده‌اند و باید دوباره ساخته شوند؟
- می‌خواهید ۱۶ نمونه را هم‌زمان روی ۱۶ هسته، یا روی کلاستر، اجرا کنید.

**مدیر جریان کار (workflow manager)** این سؤال‌ها را خودکار جواب می‌دهد. شما فقط می‌گویید **هر فایل خروجی از چه ورودی‌ای و با چه دستوری ساخته می‌شود**. ابزار ترتیب اجرا، موازی‌سازی و اینکه «چه چیزی باید دوباره ساخته شود» را خودش حساب می‌کند.

## ۲. مفاهیم

| مفهوم | معنی |
| :--- | :--- |
| **rule** | دستور ساخت یک نوع خروجی: `input`، `output`، `shell` (+ `params`، `threads`، `log`) |
| **wildcard** | جای خالی در نام فایل، مثل `{sample}`، که یک rule را برای همه‌ی نمونه‌ها قابل استفاده می‌کند |
| **هدف (target)** | فایلی که در نهایت می‌خواهید. Snakemake **از هدف به عقب** حرکت می‌کند تا بفهمد چه rule‌هایی لازم است |
| **DAG** | گراف بدون دور وابستگی‌ها بین jobها |
| **provenance** | Snakemake برای هر خروجی ثبت می‌کند با چه کد، پارامتر و ورودی‌ای ساخته شده، و اگر هر کدام عوض شود دوباره اجرا می‌کند |

| ابزار | زبان | قوت | کاربرد معمول |
| :--- | :--- | :--- | :--- |
| **Snakemake** | Python (شبیه make) | یادگیری آسان، مناسب پروژه‌های پژوهشی | پروژه‌های دانشگاهی، پایان‌نامه |
| **Nextflow** | Groovy (DSL2) | مقیاس‌پذیری، کانتینرها، جامعه‌ی **nf-core** با پایپلاین‌های آماده | پایپلاین‌های استاندارد و تولیدی (بخش ۱۰) |
| **Galaxy** | رابط وب | بدون کدنویسی | آموزش، کاربران غیربرنامه‌نویس |
| CWL / WDL | زبان توصیف استاندارد | قابل‌حمل بین پلتفرم‌ها | پلتفرم‌های ابری بزرگ |

## ۳. کار عملی: run_qc.sh به Snakefile

```bash
cd 05_Reproducible_Work/02_Workflows_Snakemake
conda activate snakemake       # یا هر محیطی که snakemake دارد
ls workflow/                   # Snakefile و config.yaml
```

### ۳.۱ پیکربندی جدا از کد
```yaml
# workflow/config.yaml
raw_dir: "../../06_Metagenomics/data/raw"
samples:
  - minigut
  - minigut_sample2
fastp:
  cut_mean_quality: 20
  length_required: 50
threads: 4
```
برای افزودن نمونه یا تغییر پارامتر، Snakefile را دست نمی‌زنید.

### ۳.۲ یک rule با wildcard
```python
rule fastp:
    input:
        r1=f"{RAW}/{{sample}}_R1.fastq.gz",
        r2=f"{RAW}/{{sample}}_R2.fastq.gz"
    output:
        r1=f"{OUT}/trimmed/{{sample}}_R1.fastq.gz",
        r2=f"{OUT}/trimmed/{{sample}}_R2.fastq.gz",
        json=f"{OUT}/fastp/{{sample}}.json",
        html=f"{OUT}/fastp/{{sample}}.html"
    params:
        q=config["fastp"]["cut_mean_quality"],
        l=config["fastp"]["length_required"]
    threads: config["threads"]
    log:
        "logs/fastp/{sample}.log"
    shell:
        "fastp -i {input.r1} -I {input.r2} -o {output.r1} -O {output.r2} "
        "--detect_adapter_for_pe --cut_front --cut_tail --cut_mean_quality {params.q} "
        "--length_required {params.l} --thread {threads} "
        "--json {output.json} --html {output.html} > {log} 2>&1"
```
- `{{sample}}` در f-string پایتون یعنی `{sample}` ادبی، که wildcard Snakemake است. `{RAW}` و `{OUT}` متغیرهای پایتون‌اند و موقع خواندن فایل جایگزین می‌شوند.
- rule اول، یعنی `all`، **هدف نهایی** را تعیین می‌کند: گزارش MultiQC. rule ‏`multiqc` با `expand()` همه‌ی ترکیب‌های `sample × read` را می‌خواهد.

کل فایل: [workflow/Snakefile](../99_scripts_data/02_Workflows_Snakemake/workflow/Snakefile).

### ۳.۳ اجرای آزمایشی (dry run)
**همیشه اول `-n`:**
```bash
snakemake -s workflow/Snakefile --cores 4 -n
```
```text
Job stats:
job               count
--------------  -------
fastp                 2
fastqc_raw            4
fastqc_trimmed        4
multiqc               1
all                   1
total                12
```
گراف rule‌ها (`snakemake --rulegraph`، که با Graphviz قابل رسم است):
```text
fastqc_raw ──────────────┐
fastp ──► fastqc_trimmed ├──► multiqc ──► all
fastp ───────────────────┘
```

### ۳.۴ اجرا
```bash
snakemake -s workflow/Snakefile --cores 4
```
```text
12 of 12 steps (100%) done
```
۲۱٫۶ ثانیه روی ۴ هسته. نتیجه دقیقاً همان `run_qc.sh` است: `jq .summary.after_filtering.total_reads results/fastp/*.json` عددهای **99690** و **49976** را می‌دهد، همان اعداد درس 06/01.

### ۳.۵ فقط آنچه لازم است دوباره اجرا می‌شود
```bash
snakemake -s workflow/Snakefile --cores 4
```
```text
Nothing to be done (all requested files are present and up to date).
```
**یک فایل ورودی تغییر کند** (اینجا با `touch` شبیه‌سازی شده):
```bash
touch ../../06_Metagenomics/data/raw/minigut_sample2_R1.fastq.gz
snakemake -s workflow/Snakefile --cores 4 -n
```
```text
fastp                 1      ← فقط نمونه‌ی ۲
fastqc_raw            1      ← فقط همان فایل
fastqc_trimmed        2
multiqc               1
all                   1
total                 6
```
**یک پارامتر تغییر کند** (`length_required: 50` ← `60` در config):
```text
Reasons:
    params have changed since last execution:
        fastp
```
```text
reason: Params have changed since last execution: ... before: 50 now: 60
```
Snakemake **یادش است** fastp با چه پارامتری اجرا شده بود. اسکریپت Bash این را نمی‌فهمد و یا همه‌چیز را دوباره اجرا می‌کنید، یا از قلم می‌افتد.

## ۴. فراتر از این درس
- **`conda:` در هر rule:** یک فایل محیط (ماژول ۰۲) برای هر rule، و اجرای `snakemake --use-conda`. هر مرحله ابزار و نسخه‌ی خودش را دارد.
- **کلاستر:** با executor plugins (مثلاً SLURM) jobها به زمان‌بند ارسال می‌شوند (بخش ۱۰).
- **Nextflow و nf-core:** برای کارهای استاندارد (مثلاً متاژنومیکس: `nf-core/mag`)، پایپلاین آماده و بازبینی‌شده بهتر از نوشتن از صفر است. داده‌ی بخش ۰۶ همان داده‌ی تست `nf-core/mag` است (بخش ۱۰).

## ۵. دام‌ها (Pitfalls)

| دام | چرا مشکل است | راه درست |
| :--- | :--- | :--- |
| اجرای بدون `-n` | ممکن است صدها job ناخواسته اجرا شود | همیشه اول dry run |
| خروجی‌ای که در `output:` ذکر نشده | Snakemake از وجودش خبر ندارد و پاکش نمی‌کند | همه‌ی خروجی‌ها را اعلام کنید |
| نوشتن چند rule در یک پوشه‌ی خروجی بدون نام یکتا | تداخل و بازنویسی | هر خروجی مسیر یکتا با wildcard |
| فرض «فایل میانی پاک‌شده خودش دوباره ساخته می‌شود» | اگر هدف نهایی به‌روز باشد، Snakemake فایل میانی گم‌شده را نمی‌سازد (تمرین ۲) | فایل را صریحاً بخواهید یا `--forcerun <rule>` |
| `shell:` بدون `log:` | خطاها گم می‌شوند | `> {log} 2>&1` |
| پارامترها در خود Snakefile | تغییر پارامتر یعنی تغییر کد | `config.yaml` |
| خروجی کهنه بعد از تغییر کد در `run:`/`script:` | بسته به تنظیمات rerun-trigger | `--rerun-triggers` را بشناسید؛ در صورت شک `--forcerun <rule>` |

## ۶. جمع‌بندی
- مدیر جریان کار با تعریف «هر خروجی از چه ورودی‌ای ساخته می‌شود» ترتیب، موازی‌سازی و اجرای مجدد را خودکار می‌کند.
- Snakemake تغییر ورودی، پارامتر و کد را ردیابی می‌کند و **فقط** jobهای لازم را دوباره اجرا می‌کند.
- پیکربندی (`config.yaml`) را از منطق (`Snakefile`) جدا کنید. همیشه اول `-n`.

---

## منابع

### مقالات و مستندات
- Mölder F, et al. (2021). Sustainable data analysis with Snakemake. *F1000Research* 10:33. https://doi.org/10.12688/f1000research.29032.2
- Di Tommaso P, et al. (2017). Nextflow enables reproducible computational workflows. *Nature Biotechnology* 35:316–319. https://doi.org/10.1038/nbt.3820
- مستندات و آموزش رسمی Snakemake: https://snakemake.readthedocs.io/
- آموزش رسمی Nextflow: https://training.nextflow.io/
- Galaxy: https://usegalaxy.org/

### ویدیوهای آموزشی
- IPAM — Johannes Köster (سازنده‌ی Snakemake), *Transparent, reproducible, and adaptable data analysis with Snakemake*: https://www.youtube.com/watch?v=1K5vOwmiXbU
- Riffomonas Project — *An introduction to Snakemake tutorial for beginners*: https://www.youtube.com/watch?v=r9PWnEmz_tc
- Edinburgh Genomics Training — *Introducing Snakemake*: https://www.youtube.com/watch?v=NNPBDOBHlxo
- Nextflow (کانال رسمی) — *Hello Nextflow 2026, Part 1: Hello World*: https://www.youtube.com/watch?v=tOukLxWCHiA

> لینک‌ها در تاریخ 2026-10-13 بررسی شدند (`_tools/check_links.sh`).
