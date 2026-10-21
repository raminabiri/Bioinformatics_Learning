<div dir="rtl">

# پاسخ تشریحی: یک گردش کار کامل

خروجی‌ها از اجرای واقعی در 2026-10-21 گرفته شده‌اند (Snakemake 9.25.2، seqkit 2.13.0، R 4.6.1). سرآیند Snakemake (تاریخ، نسخه، نشانی‌ها) و بخشی از خط‌های تکراری برای کوتاهی برداشته شده‌اند (`...`).

---

## پاسخ ۱: `touch` یا ویرایش؟

**(الف)** پیش‌بینی منطقی: `names.tsv` ورودی `make_table` است، پس `make_table` و همه‌ی پایین‌دستش. ولی:

<div dir="ltr">

```bash
touch names.tsv
snakemake -n
```

</div>

<div dir="ltr">

```text
Building DAG of jobs...
Nothing to be done (all requested files are present and up to date).
```

</div>

هیچ کاری! چرا؟ Snakemake برای فایل‌های **کوچک‌تر از ۱ مگابایت** (`names.tsv` تنها ۱۰۶۲ بایت است) به تاریخ تغییر بسنده نمی‌کند: «اثر انگشت» (*checksum*) محتوا را هم می‌سنجد. `touch` تنها تاریخ را عوض کرد، نه محتوا را؛ پس چیزی برای دوباره‌سازی نیست. (این مرز با گزینه‌ی `--max-checksum-file-size` تعیین می‌شود و پیش‌فرض آن `1MB` است. فایل‌های FASTQ ما حدود ۳ مگابایت‌اند، برای همین `touch` در ماژول ۰۳ کار کرد.)

**(ب)** اکنون محتوا را عوض می‌کنیم:

<div dir="ltr">

```bash
sed -i 's/Escherichia coli K-12 MG1655/Escherichia coli K-12 substr. MG1655/' names.tsv
snakemake -n
```

</div>

<div dir="ltr">

```text
Job stats:
job             count
------------  -------
make_table          2
composition         2
merge_tables        1
check_truth         1
diversity           1
all                 1
total               8
...
rule make_table:
    input: counts/minigut.tsv, names.tsv
    output: tables/minigut.tsv
    jobid: 2
    reason: Updated input files: names.tsv
    wildcards: sample=minigut
...
rule merge_tables:
    input: tables/minigut.tsv, tables/minigut_sample2.tsv
    output: tables/all_samples.tsv
    jobid: 8
    reason: Input files updated by another job: tables/minigut.tsv, tables/minigut_sample2.tsv
```

</div>

۸ کار: `make_table` برای **هر دو** نمونه (هر دو `names.tsv` را می‌خوانند)، و همه‌ی پایین‌دست. `count_reads` و `seqkit_stats` نیستند چون **بالادست** `names.tsv` هستند: تنها FASTQ را می‌خوانند و جدول نام‌ها را لازم ندارند.

**(ج)** `check_truth` تنها ستون‌های ۱ تا ۳ (نمونه، شمار، accession) را می‌سنجد (`cut -f1-3`)، نه نام موجود را. نام عوض شد، شمارها نه. (نمودار جنس هم همان می‌ماند، چون واژه‌ی نخست هنوز `Escherichia` است.)

<div dir="ltr">

```bash
git checkout names.tsv
snakemake -c 2
```

</div>

---

## پاسخ ۲: قاعده‌ی تازه با پارامتر از `config`

یک خط در پایان `config.yaml`:

<div dir="ltr">

```yaml
top_n: 3                      # how many accessions to keep in top/
```

</div>

در Snakefile، یک خط به `rule all` و یک قاعده‌ی تازه در پایان:

<div dir="ltr">

```python
rule all:
    input:
        expand("plots/{sample}_composition.png", sample=SAMPLES),
        "diversity/diversity_alpha.tsv",
        "check/ground_truth_check.txt",
        "stats/seqkit_stats.tsv",
        expand("top/{sample}.tsv", sample=SAMPLES),

rule top_accessions:
    input:
        "counts/{sample}.tsv",
    output:
        "top/{sample}.tsv",
    params:
        n=config["top_n"],
    shell:
        "head -n {params.n} {input} > {output}"
```

</div>

**(الف)**

<div dir="ltr">

```bash
snakemake -n
```

</div>

<div dir="ltr">

```text
Job stats:
job               count
--------------  -------
top_accessions        2
all                   1
total                 3
```

</div>

تنها قاعده‌ی تازه (برای هر نمونه) و `all`. شمارش‌ها از پیش هستند.

**(ب)**

<div dir="ltr">

```bash
snakemake -c 2 -q
head top/*.tsv
```

</div>

<div dir="ltr">

```text
==> top/minigut_sample2.tsv <==
  16154 CP009257.1
   1178 NC_002516.2
    965 NC_004461.1

==> top/minigut.tsv <==
  28912 NC_006347.1
  21088 NC_000913.3
```

</div>

‏`minigut` تنها **دو** موجود دارد (غنای ۲ در درس)؛ `head -n 3` روی فایل دوخطی، دو خط می‌دهد و خطا نمی‌دهد.

**(ج)** با `top_n: 5`:

<div dir="ltr">

```text
rule top_accessions:
    reason: Params have changed since last execution: Union of exclusive params before and now across all output: before: 3 now: 5 
rule top_accessions:
    reason: Params have changed since last execution: Union of exclusive params before and now across all output: before: 3 now: 5 
rule all:
    reason: Input files updated by another job: top/minigut_sample2.tsv, top/minigut.tsv
total                 3
```

</div>

تنها `top_accessions` (دو بار) و `all`؛ همان رفتار `diversity_level` در درس. چون مقدار از راه `params` آمده، Snakemake آن را به یاد سپرده بود.

---

## پاسخ ۳: فایل تنظیم دوم

<div dir="ltr">

```bash
sed '/^  - minigut$/d' config.yaml > config_one.yaml
head -n 4 config_one.yaml
```

</div>

<div dir="ltr">

```text
# config.yaml: everything you may change, in one place (part 05, module 04)
samples:
  - minigut_sample2

```

</div>

‏(`sed '/الگو/d'` خط‌های هم‌خوان را پاک می‌کند، بخش ۰۱. `^` و `$` نمی‌گذارند خط `  - minigut_sample2` هم پاک شود. با `nano` هم می‌شد.)

**(الف)**

<div dir="ltr">

```bash
snakemake --configfile config_one.yaml -n
```

</div>

<div dir="ltr">

```text
merge_tables        1
seqkit_stats        1
check_truth         1
diversity           1
all                 1
total               5
rule seqkit_stats:
    reason: Set of input files has changed since last execution
rule merge_tables:
    reason: Set of input files has changed since last execution
rule check_truth:
    reason: Input files updated by another job: tables/all_samples.tsv
rule diversity:
    reason: Input files updated by another job: tables/all_samples.tsv
```

</div>

‏`count_reads`، `make_table` و `composition` برای `minigut_sample2` از پیش ساخته شده‌اند؛ تنها قاعده‌های «همه‌ی نمونه‌ها» دوباره اجرا می‌شوند، چون فهرست ورودی‌شان کوتاه‌تر شد.

**(ب)**

<div dir="ltr">

```bash
snakemake --configfile config_one.yaml -c 2
```

</div>

<div dir="ltr">

```text
...
0a1,2
> minigut	21088	NC_000913.3
> minigut	28912	NC_006347.1
CalledProcessError in file ".../Snakefile", line 87:
...
Error in rule check_truth:
...
Exiting because a job execution failed. Look below for error messages
```

</div>

‏`>` یعنی «تنها در فایل **دوم**» (`ground_truth.tsv`): پاسخ معلوم دو سطر برای `minigut` دارد که جدول ما دیگر ندارد. وارسی درست کار کرد: جدول با پاسخ معلوم نمی‌خواند. (در درس، با `gut3`، نشانه `<` بود: سطرهای اضافه در فایل **یکم**.)

**(ج)**

<div dir="ltr">

```bash
ls check
```

</div>

<div dir="ltr">

```text
ls: cannot access 'check': No such file or directory
```

</div>

‏Snakemake پیش از اجرای `check_truth` خروجی کهنه‌اش را پاک کرد، و چون کار شکست خورد، فایل تازه‌ای هم نساخت. این خوب است: یک `identical` کهنه نمی‌تواند شما را فریب دهد.

**(د)**

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
merge_tables        1
seqkit_stats        1
check_truth         1
diversity           1
all                 1
total               5
```

</div>

پس از `snakemake -c 2`، `cat check/ground_truth_check.txt` دوباره `identical: …` می‌دهد. **درس:** هر دو فایل تنظیم، خروجی را در **همان** پوشه‌ها می‌نویسند و یکدیگر را بازنویسی می‌کنند. برای دو گروه نمونه‌ی واقعاً جدا، دو پوشه‌ی پروژه بسازید.

---

## پاسخ ۴: مقدار نادرست، بی هیچ خطا

**(الف)** با `diversity_level: species`، `snakemake -c 2` بی هیچ خطایی تمام می‌شود (Snakemake تنها `diversity` را دوباره اجرا می‌کند: `Params have changed`). ولی گزارش:

<div dir="ltr">

```bash
cat logs/diversity.log
```

</div>

<div dir="ltr">

```text
level: species  samples: 2  taxa: 22 
          sample reads richness shannon simpson evenness
         minigut 50000        2   0.681   0.488    0.982
 minigut_sample2 24993       21   1.608   0.572    0.528

Bray-Curtis dissimilarity (0 = same, 1 = nothing shared):
                minigut
minigut_sample2   0.987
...
```

</div>

‏`taxa: 22` و غنای ۲۱: این سطح **موجود** است، نه جنس (۱۸). `diversity.R` (بخش ۰۴، خط ۱۹) تنها می‌پرسد «آیا `genus` است؟» و هر چیز دیگری را `organism` می‌شمارد. پس اشتباه تایپی شما بی‌صدا به نتیجه‌ای دیگر انجامید. **این بدترین گونه‌ی خطاست**: گردش کار «سبز» است، ولی عددها آن نیستند که خواستید.

**(ب)** در بالای Snakefile:

<div dir="ltr">

```python
import sys

configfile: "config.yaml"

SAMPLES = config["samples"]
FASTQ = config["fastq_dir"]

if config["diversity_level"] not in ["organism", "genus"]:
    sys.exit("config.yaml: diversity_level must be organism or genus, not " + config["diversity_level"])
```

</div>

<div dir="ltr">

```bash
snakemake -n
echo $?
```

</div>

<div dir="ltr">

```text
config.yaml: diversity_level must be organism or genus, not species
1
```

</div>

‏Snakefile خودش پایتون است؛ این شرط هنگام **خواندن** آن اجرا می‌شود، پیش از ساختن هر کاری. کد خروج ۱ است، پس `set -e` در یک اسکریپت Bash (بخش ۰۴، ماژول ۰۴) هم آن را می‌گیرد. پس از برگرداندن `genus`، `snakemake -n` تنها `diversity` را نشان می‌دهد (`before: 'species' now: 'genus'`).

**قاعده:** هر کلید `config` که تنها چند مقدار درست دارد، در Snakefile وارسی شود.

---

## پاسخ ۵: اسکریپت را عوض کردم؛ Snakemake نفهمید

**(الف)**

<div dir="ltr">

```bash
sed -i 's/names.get(accession, "unknown")/names.get(accession, "unassigned")/' scripts/make_table.py
snakemake -n
```

</div>

<div dir="ltr">

```text
Nothing to be done (all requested files are present and up to date).
```

</div>

‏`scripts/make_table.py` در `input` هیچ قاعده‌ای نیست. Snakemake تنها **متن دستور** `shell` را به یاد می‌سپارد، و آن متن عوض نشده است.

**(ب)**

<div dir="ltr">

```bash
snakemake -n --forcerun make_table
```

</div>

<div dir="ltr">

```text
Job stats:
job             count
------------  -------
make_table          2
composition         2
merge_tables        1
check_truth         1
diversity           1
all                 1
total               8
```

</div>

‏`make_table` با `reason: Forced execution`، و همه‌ی پایین‌دستش با `Input files updated by another job`. ولی باید **یادتان بماند** که این گزینه را بزنید.

**(ج)** اسکریپت را یک ورودی نام‌دار کنید و در دستور از همان نام بهره ببرید:

<div dir="ltr">

```python
rule make_table:
    input:
        counts="counts/{sample}.tsv",
        names=config["names"],
        script="scripts/make_table.py",
    output:
        "tables/{sample}.tsv",
    shell:
        "python3 {input.script} {input.counts} {input.names} {wildcards.sample} {output}"
```

</div>

<div dir="ltr">

```bash
snakemake -n
```

</div>

<div dir="ltr">

```text
rule make_table:
    reason: Updated input files: scripts/make_table.py
...
total               8
```

</div>

اکنون اسکریپت هم زیر نظر است. پس از اجرا، `"unassigned"` را به `"unknown"` برگردانید (`git checkout scripts/make_table.py`): Snakemake **خودش** دوباره ۸ کار را نشان می‌دهد (`reason: Updated input files: scripts/make_table.py`). همین کار را می‌توان برای `composition.R` و `diversity.R` هم کرد. `snakemake -c 2` بزنید.

---

## پاسخ ۶: پزشک Snakefile

سه اشتباه، همه در `make_table`:

| خط | اشتباه | درست |
| :--- | :--- | :--- |
| ‏`names=config["name"]` | کلید `name` در `config.yaml` نیست | `config["names"]` |
| ‏`{input.count}` | ورودی `counts` نام دارد | `{input.counts}` |
| ‏`{sample}` | در `shell` نام wildcard تنها با `wildcards.` می‌آید | `{wildcards.sample}` |

**اجرای ۱:**

<div dir="ltr">

```text
KeyError in file ".../Snakefile", line 24:
'name'
  File ".../Snakefile", line 24, in <module>
```

</div>

‏`KeyError` (بخش ۰۳، دیکشنری): کلیدی که در `config` نیست. این خطا هنگام **خواندن** Snakefile رخ می‌دهد، پیش از هر کاری.

**اجرای ۲** (پس از درست کردن `names`):

<div dir="ltr">

```text
RuleException in rule make_table in file ".../Snakefile", line 21:
NameError: The name 'sample' is unknown in this context. Did you mean 'wildcards.sample'?, when formatting the following:
python3 scripts/make_table.py {input.count} {input.names} {sample} {output}
```

</div>

‏Snakemake خودش راه درست را پیشنهاد می‌کند.

**اجرای ۳** (پس از درست کردن `{wildcards.sample}`): شگفت‌انگیزترین پیام:

<div dir="ltr">

```text
/usr/bin/bash: line 1: built-in: No such file or directory
RuleException:
CalledProcessError in file ".../Snakefile", line 28:
Command 'set -euo pipefail;  python3 scripts/make_table.py <built-in method count of InputFiles object at 0x7b440380f950> names.tsv minigut_sample2 tables/minigut_sample2.tsv' returned non-zero exit status 1.
```

</div>

چرا Snakemake نگفت «`count` نیست»؟ چون `input` یک **فهرست** پایتون است و فهرست‌ها هم، مانند رشته‌ها، از پیش روشی به نام `count` دارند (بخش ۰۳: `dna.count("A")`). پس `{input.count}` به **نوشته‌ی آن روش** (`<built-in method count …>`) تبدیل شد. Bash نشانه‌ی `<` را «ورودی از فایل» (بخش ۰۱) خواند و دنبال فایلی به نام `built-in` گشت. **درس:** وقتی در دستور چاپ‌شده چیز عجیبی مانند `<built-in …>` می‌بینید، نام ورودی یا خروجی را نادرست نوشته‌اید. (نام‌هایی مانند `count` و `index` را برای ورودی‌ها به کار نبرید.)

**اجرای ۴:**

<div dir="ltr">

```text
...
3 of 3 steps (100%) done
```

</div>

‏(۳، نه ۵: `count_reads` در اجراهای پیشین ساخته شده بود.)

---

## پاسخ ۷: بهبود را در Git بگذارید

**(الف)**

<div dir="ltr">

```bash
snakemake -c 2 -q
git status --short
```

</div>

<div dir="ltr">

```text
 M Snakefile
```

</div>

‏Snakemake ده‌ها فایل در `tables/`، `plots/`، `diversity/` و … را دوباره ساخت، ولی همه‌ی این پوشه‌ها در `.gitignore` هستند (بخش ۸ درس). `scripts/make_table.py` هم در فهرست نیست، چون به `"unknown"` برگشت و محتوایش همان نسخه‌ی commit‌شده است.

**(ب)**

<div dir="ltr">

```bash
git diff
```

</div>

<div dir="ltr">

```text
diff --git a/Snakefile b/Snakefile
index 93104c2..9473871 100644
--- a/Snakefile
+++ b/Snakefile
@@ -34,10 +34,11 @@ rule make_table:
     input:
         counts="counts/{sample}.tsv",
         names=config["names"],
+        script="scripts/make_table.py",
     output:
         "tables/{sample}.tsv",
     shell:
-        "python3 scripts/make_table.py {input.counts} {input.names} {wildcards.sample} {output}"
+        "python3 {input.script} {input.counts} {input.names} {wildcards.sample} {output}"
 
 
 rule composition:
```

</div>

<div dir="ltr">

```bash
git add Snakefile
git commit -m "Rerun make_table when its script changes"
git log --oneline
```

</div>

<div dir="ltr">

```text
[main 4eea8db] Rerun make_table when its script changes
 1 file changed, 2 insertions(+), 1 deletion(-)
4eea8db Rerun make_table when its script changes
9386c29 Add composition and diversity workflow
```

</div>

‏(شناسه‌های شما دیگر خواهند بود.) پیام commit می‌گوید **چرا**، نه تنها «Snakefile را عوض کردم».

**(ج)** در Git: `Snakefile`، `config.yaml`، `scripts/`، جدول‌های کوچک کمکی (`names.tsv`)، فایل محیط conda (`envs/workflow.yml`)، و یک `README.md` که می‌گوید داده را از کجا بگیرید و چه دستوری بزنید. **بیرون از Git:** FASTQها (گیگابایت‌ها؛ GitHub فایل‌های بزرگ‌تر از ۱۰۰ مگابایت را نمی‌پذیرد)، خروجی‌ها (دوباره‌ساختنی‌اند) و `.snakemake/`. FASTQهای خام در یک پایگاه عمومی مانند **SRA/ENA** (بخش ۰۲) گذاشته می‌شوند و در `config.yaml` یا README تنها **شناسه‌ی** آن‌ها (مانند `SRR…`) می‌آید. آن‌گاه هر کس می‌تواند: `git clone` → دانلود FASTQ با شناسه‌ها → `snakemake -c 8`.

</div>
