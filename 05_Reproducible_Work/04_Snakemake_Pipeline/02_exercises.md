<div dir="rtl">

# تمرین‌ها: یک گردش کار کامل

همه‌ی تمرین‌ها در پوشه‌ی درس (`~/smk_pipeline`) انجام می‌شوند، پس از یک اجرای کامل (`snakemake -c 2`) و commit بخش ۸ درس. پیش از هر تمرین، `snakemake -n` باید بگوید `Nothing to be done`.

<div dir="ltr">

```bash
conda activate workflow
cd ~/smk_pipeline
snakemake -n
```

</div>

**نکته:** پیش از هر تغییر، از `Snakefile` و `config.yaml` یک کپی بگیرید (`cp Snakefile Snakefile.bak`)؛ یا چون پروژه در Git است، با `git checkout Snakefile` (ماژول ۰۱) به نسخه‌ی commit‌شده برگردید. تمرین‌ها، جز تمرین ۷، از Snakefile درس آغاز می‌شوند.

---

## تمرین ۱: `touch` یا ویرایش؟
> **راهنمایی:** درس، بخش ۶ (جدول «چه عوض شد»). ببینید `names.tsv` ورودی کدام قاعده است. در `reason` هر کار بخوانید چرا اجرا می‌شود.

(الف) پیش‌بینی کنید پس از `touch names.tsv` کدام کارها دوباره اجرا می‌شوند؛ سپس با `snakemake -n` بسنجید. شگفت‌زده شدید؟
(ب) این بار در `names.tsv` نام `Escherichia coli K-12 MG1655` را به `Escherichia coli K-12 substr. MG1655` تغییر دهید (با `nano` یا `sed`، بخش ۰۱) و دوباره `snakemake -n` بزنید. چند کار؟ چرا `count_reads` و `seqkit_stats` در فهرست نیستند؟
(ج) چرا با این تغییر، وارسی `check_truth` باز هم `identical` می‌دهد؟
در پایان `names.tsv` را برگردانید (`git checkout names.tsv`) و `snakemake -c 2` بزنید.

---

## تمرین ۲: قاعده‌ی تازه با پارامتر از `config`
> **راهنمایی:** درس، بخش ۴ (`diversity` و `params`). `head -n عدد فایل` (بخش ۰۱) چند خط نخست را می‌دهد؛ `counts/{sample}.tsv` از پیش به ترتیب نزولی است. خروجی تازه را به `rule all` بیفزایید.

یک کلید تازه، `top_n: 3`، به `config.yaml` بیفزایید و قاعده‌ای به نام `top_accessions` بنویسید که برای هر نمونه، `top_n` accession پرشمار را در `top/{sample}.tsv` بنویسد.
(الف) `snakemake -n` چند کار نشان می‌دهد؟ (ب) چرا `top/minigut.tsv` تنها **دو** خط دارد؟ (ج) `top_n` را به ۵ برسانید: کدام کارها دوباره اجرا می‌شوند و `reason` چه می‌گوید؟

---

## تمرین ۳: فایل تنظیم دوم
> **راهنمایی:** گزینه‌ی `--configfile نام_فایل` به‌جای `config.yaml` فایل دیگری را می‌خواند (درس، بخش ۳). پیش از اجرا بیندیشید: `ground_truth.tsv` پاسخ چند نمونه را دارد؟

یک کپی از `config.yaml` به نام `config_one.yaml` بسازید که **تنها** `minigut_sample2` را دارد. گردش کار را با آن اجرا کنید:

<div dir="ltr">

```bash
snakemake --configfile config_one.yaml -n
snakemake --configfile config_one.yaml -c 2
```

</div>

(الف) کدام کارها اجرا می‌شوند و چرا `count_reads` میان آن‌ها نیست؟ (ب) چه چیزی شکست می‌خورد و نشانه‌های `>` در پیام یعنی چه؟ (ج) فایل `check/ground_truth_check.txt` اکنون کجاست؟ (د) دوباره `snakemake -c 2` (با `config.yaml` خودش) بزنید: آیا همه چیز سر جایش برمی‌گردد؟

---

## تمرین ۴: مقدار نادرست، بی هیچ خطا
> **راهنمایی:** درس، اشتباه رایج ۱ («نخست `log` را بخوانید»). نخستین خط `logs/diversity.log` را با اجرای درس بسنجید. برای بخش (ب): `sys.exit("پیام")` و `not in` از بخش ۰۳.

(الف) در `config.yaml`، `diversity_level: genus` را به `species` تغییر دهید و `snakemake -c 2` بزنید. آیا خطایی می‌بینید؟ با خواندن `logs/diversity.log` بگویید اسکریپت R در کدام سطح شمرد و چرا این خطرناک است.
(ب) چند خط پایتون در بالای Snakefile (پس از `FASTQ = …`) بیفزایید که اگر `diversity_level` نه `organism` بود و نه `genus`، Snakemake **پیش از هر کاری** با یک پیام روشن بایستد. سپس `genus` را برگردانید.

---

## تمرین ۵: اسکریپت را عوض کردم؛ Snakemake نفهمید
> **راهنمایی:** درس، کادر کنجکاوها (`--forcerun`). برای راه دوم: هر فایلی که در `input` باشد زیر نظر است؛ خود اسکریپت هم یک فایل است.

در `scripts/make_table.py` واژه‌ی `"unknown"` را به `"unassigned"` تغییر دهید و `snakemake -n` بزنید.
(الف) چه می‌بینید و چرا؟ (ب) با `--forcerun`، کدام کارها دوباره اجرا می‌شوند؟ (ج) قاعده‌ی `make_table` را چنان بازنویسید که از این پس، با **هر** تغییر اسکریپت، خودش دوباره اجرا شود.

---

## تمرین ۶: پزشک Snakefile
> **راهنمایی:** درس، بخش ۴ (نام‌های `{input.counts}` و `{wildcards.sample}`) و بخش ۳ (کلیدهای `config.yaml`). Snakemake هر بار تنها **یک** خطا را می‌گوید: درست کنید و دوباره بزنید.

این Snakefile **سه** اشتباه دارد. نخست بی اجرا پیدایشان کنید؛ سپس در یک پوشه‌ی جدا (با `fastq/`، `scripts/`، `config.yaml` و `names.tsv` درس) بنویسید، با `snakemake -c 2` اجرا کنید و پیام‌ها را بخوانید.

<div dir="ltr">

```python
configfile: "config.yaml"

SAMPLES = config["samples"]

rule all:
    input:
        expand("tables/{sample}.tsv", sample=SAMPLES),

rule count_reads:
    input:
        "fastq/{sample}_R1.fastq.gz",
    output:
        "counts/{sample}.tsv",
    shell:
        "zcat {input} | awk 'NR%4==1' | grep -oE '^@[A-Z]+_?[0-9]+[.][0-9]+' | cut -c2- "
        "| sort | uniq -c | sort -k1,1nr > {output}"

rule make_table:
    input:
        counts="counts/{sample}.tsv",
        names=config["name"],
    output:
        "tables/{sample}.tsv",
    shell:
        "python3 scripts/make_table.py {input.count} {input.names} {sample} {output}"
```

</div>

---

## تمرین ۷: بهبود را در Git بگذارید
> **راهنمایی:** ماژول ۰۱ (`git status`، `git diff`، `git commit`) و بخش ۸ درس (`.gitignore`).

پس از تمرین ۵ (ج) و اجرای `snakemake -c 2`:
(الف) `git status --short` بزنید. Snakemake چند فایل خروجی را دوباره ساخت؛ چرا Git تنها **یک** فایل را تغییرکرده می‌بیند؟
(ب) با `git diff` تغییر را ببینید، آن را با پیامی روشن commit کنید و `git log --oneline` را نشان دهید.
(ج) (فکری) `ground_truth.tsv` و `names.tsv` در Git هستند ولی `fastq/` نیست. برای یک پروژه‌ی واقعی با ۲۰۰ نمونه، کدام فایل‌ها را در Git می‌گذارید و FASTQها را کجا نگه می‌دارید تا دیگران بتوانند همه چیز را دوباره بسازند؟

</div>
