<div dir="rtl">

# درس: نخستین گردش کار با Snakemake

**بخش:** `05_Reproducible_Work` · **ماژول:** `03_Snakemake_First` · **پیش‌نیاز:** ماژول [شاخه و GitHub](../02_Git_Branches_GitHub/)؛ ماژول [اسکریپت‌های R در خط لوله](../../04_R_Packages/04_R_in_Pipelines/) · **زمان:** حدود ۷۵ دقیقه · **ابزار:** Snakemake 9.25.2، seqkit 2.13.0 · **آخرین اجرا:** 2026-10-21

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. بگویید Snakemake چه چیزی بیش از یک اسکریپت Bash به شما می‌دهد.
2. یک **قاعده** (*rule*) با `input`، `output` و `shell` بنویسید.
3. با **‏wildcard** (`{sample}`) یک قاعده را برای همه‌ی نمونه‌ها به کار ببرید و با `expand` و قاعده‌ی `all` همه‌ی خروجی‌ها را بخواهید.
4. با **اجرای آزمایشی** (`-n`) پیش‌بینی کنید چه اجرا می‌شود و **چرا** (`reason`).
5. چهار خطای رایج Snakemake را بشناسید.

**پیش از آغاز:** محیط این بخش را بسازید (یک بار؛ Snakemake، seqkit و بسته‌های R بخش ۰۴):

<div dir="ltr">

```bash
cd ~/Bioinformatics_Learning-main
CONDA_CHANNEL_PRIORITY=flexible conda env create -f envs/workflow.yml
conda activate workflow
mkdir -p ~/smk_practice && cd ~/smk_practice
cp -r ~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data/fastq .
ls fastq
```

</div>

<div dir="ltr">

```text
minigut_R1.fastq.gz  minigut_R2.fastq.gz  minigut_sample2_R1.fastq.gz  minigut_sample2_R2.fastq.gz
```

</div>

‏`CONDA_CHANNEL_PRIORITY=flexible` (یک متغیر محیطی تنها برای همین یک دستور، بخش ۰۱) اولویت کانال‌ها را برای این ساخت «نرم» می‌کند. چرا؟ در 2026-10-21 با تنظیم سخت‌گیرانه‌ی دوره (`channel_priority strict`، بخش ۰۲)، conda نسخه‌ی Snakemake کانال bioconda را نپذیرفت (`excluded by strict repo priority`)؛ با `flexible` محیط حل شد.

---

## ۱. داستان: اسکریپت Bash کجا کم می‌آورد؟

در ماژول ۰۴ بخش ۰۴، `run_all.sh` چند اسکریپت را پشت سر هم اجرا کرد. خوب بود، ولی سه کمبود داشت:

1. **همه چیز را هر بار از نو** اجرا می‌کند. اگر تنها یک نمونه تازه شود، باز همه‌ی نمونه‌ها دوباره پردازش می‌شوند؛ برای ۲۰۰ نمونه یعنی ساعت‌ها هدر.
2. **ترتیب را شما** باید بدانید و بنویسید. اگر گام ۳ به خروجی گام ۱ نیاز دارد، باید یادتان باشد.
3. **یکی‌یکی** اجرا می‌کند، حتی اگر کامپیوتر ۸ هسته‌ی بیکار دارد.

‏**Snakemake** هر سه را حل می‌کند. شما تنها می‌گویید **هر فایل از کدام فایل‌ها و با چه دستوری ساخته می‌شود**؛ Snakemake خودش ترتیب را می‌یابد، تنها چیزهای کهنه یا ناموجود را می‌سازد، و کارهای مستقل را هم‌زمان اجرا می‌کند. (نام و نحوِ نوشتن از پایتون آمده است، و از ابزار کهنه‌ی `make`.)

---

## ۲. مفهوم به زبان ساده: دستور پخت وارونه

اسکریپت Bash مانند دستور پختی است که از آغاز می‌گوید: «نخست آرد را الک کن، سپس…». Snakemake **از پایان** فکر می‌کند:

<div dir="ltr">

```text
  I want:  counts/minigut.tsv
           ▲
           │  rule count_reads:  "counts/{sample}.tsv" is made from "fastq/{sample}_R1.fastq.gz"
           │
  It needs: fastq/minigut_R1.fastq.gz   ← exists → run the command
```

</div>

- هر **قاعده** (*rule*) یک «دستور پخت» است: ورودی، خروجی، دستور.
- شما **فایلی را که می‌خواهید** نام می‌برید. Snakemake قاعده‌ای را پیدا می‌کند که آن فایل را می‌سازد، ورودی‌هایش را می‌سنجد، و اگر ورودی خودش خروجی قاعده‌ی دیگری است، آن را هم پیدا می‌کند… تا به فایل‌های موجود برسد. این زنجیره را **گراف کارها** (*DAG*) می‌نامند.
- اگر خروجی **هست** و از ورودی‌هایش **تازه‌تر** است، Snakemake کاری نمی‌کند.

---

## ۳. نخستین قاعده

با `nano Snakefile` (نام فایل باید دقیقاً همین باشد) بنویسید:

<div dir="ltr">

```python
rule count_minigut:
    input:
        "fastq/minigut_R1.fastq.gz"
    output:
        "counts/minigut.tsv"
    shell:
        "zcat {input} | awk 'NR%4==1' | grep -oE '^@[A-Z]+_?[0-9]+[.][0-9]+' | cut -c2- | sort | uniq -c > {output}"
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `rule count_minigut:` | یک قاعده با یک نام (بی فاصله) |
| `input:` | فایل(هایی) که لازم است، درون `"…"` |
| `output:` | فایل(هایی) که ساخته می‌شود؛ پوشه‌ی `counts/` را Snakemake خودش می‌سازد |
| `shell:` | دستور Bash، درون `"…"` |
| `{input}`، `{output}` | ‏Snakemake به‌جایشان نام فایل‌ها را می‌گذارد |
| **فرورفتگی** (۴ فاصله) | مانند پایتون: بخش‌ها زیر `rule`، محتوا زیر هر بخش |

خود دستور همان لوله‌ی بخش ۰۱ است، گام‌به‌گام:

| گام | کار |
| :--- | :--- |
| `zcat {input}` | باز کردن FASTQ فشرده |
| `awk 'NR%4==1'` | تنها خط یکم هر رید (سرآیند، مانند `@NC_006347.1_0/1`) |
| `grep -oE '^@[A-Z]+_?[0-9]+[.][0-9]+'` | تنها بخش accession (`@NC_006347.1`)؛ `[.]` = نقطه‌ی واقعی |
| `cut -c2-` | برداشتن `@` |
| `sort \| uniq -c` | شمار رید هر accession |

ریدهای این داده **شبیه‌سازی‌شده‌اند** و نام هر رید، ژنوم سرچشمه‌اش را دارد. پس این شمارش، ترکیب **واقعی** نمونه را می‌دهد (در داده‌ی واقعی چنین برچسبی نیست و ابزارهای طبقه‌بندی بخش ۰۶ لازم‌اند).

### اجرای آزمایشی: `-n`

<div dir="ltr">

```bash
snakemake -n
```

</div>

<div dir="ltr">

```text
Building DAG of jobs...
Job stats:
job              count
-------------  -------
count_minigut        1
total                1

rule count_minigut:
    input: fastq/minigut_R1.fastq.gz
    output: counts/minigut.tsv
    jobid: 0
    reason: Missing output files: counts/minigut.tsv
    resources: tmpdir=/tmp
...
This was a dry-run (flag -n). The order of jobs does not reflect the order of execution.
```

</div>

‏(در این درس، سرآیند Snakemake که تاریخ، نسخه و نشانی‌ها را چاپ می‌کند، برای کوتاهی برداشته شده است.)

- ‏`-n` (*dry-run*): «بگو **چه** می‌کنی، ولی نکن». **همیشه پیش از اجرای واقعی.**
- ‏`Job stats`: چند کار از هر قاعده.
- ‏`reason: Missing output files`: **چرا** این کار لازم است: خروجی هنوز نیست.

### اجرای واقعی: `-c`

<div dir="ltr">

```bash
snakemake -c 1
cat counts/minigut.tsv
```

</div>

<div dir="ltr">

```text
Building DAG of jobs...
Using shell: /usr/bin/bash
Provided cores: 1 (use --cores to define parallelism)
...
localrule count_minigut:
    input: fastq/minigut_R1.fastq.gz
    output: counts/minigut.tsv
    ...
Finished jobid: 0 (Rule: count_minigut)
1 of 1 steps (100%) done
  21088 NC_000913.3
  28912 NC_006347.1
```

</div>

‏`-c 1` (*cores*): با چند هسته‌ی CPU. **بی `-c` اجرا نمی‌شود** (`-n` نیازی به آن ندارد). نتیجه همان ترکیب `ground_truth.tsv` است: E. coli ۲۱٬۰۸۸ و B. fragilis ۲۸٬۹۱۲ جفت‌رید.

### دوباره اجرا کنید

<div dir="ltr">

```bash
snakemake -c 1
```

</div>

<div dir="ltr">

```text
Building DAG of jobs...
Nothing to be done (all requested files are present and up to date).
```

</div>

خروجی هست و از ورودی تازه‌تر است، پس کاری نیست. **این قلب Snakemake است.**

---

## ۴. یک قاعده برای همه‌ی نمونه‌ها: wildcard

قاعده‌ی بالا تنها برای `minigut` است. برای ۲۰۰ نمونه، ۲۰۰ قاعده؟ نه. نام نمونه را با یک **‏wildcard** جایگزین کنید:

<div dir="ltr">

```python
rule count_reads:
    input:
        "fastq/{sample}_R1.fastq.gz",
    output:
        "counts/{sample}.tsv",
    shell:
        "zcat {input} | awk 'NR%4==1' | grep -oE '^@[A-Z]+_?[0-9]+[.][0-9]+' | cut -c2- "
        "| sort | uniq -c | sort -k1,1nr > {output}"
```

</div>

- ‏`{sample}` در `output` یعنی «هر چیزی این‌جا باشد». اگر بخواهید `counts/minigut_sample2.tsv`، Snakemake می‌فهمد `sample = minigut_sample2` و همان را در `input` می‌گذارد: `fastq/minigut_sample2_R1.fastq.gz`.
- دو رشته‌ی پشت سر هم (`"…" "…"`) یک رشته می‌شوند (همان قاعده‌ی پایتون): برای شکستن دستور بلند.
- ‏`sort -k1,1nr`: پرریدترین بالا (بخش ۰۱).
- ویرگول پس از هر فایل اختیاری است؛ وقتی چند فایل باشد لازم می‌شود، پس عادت خوبی است.

حالا **نام فایل خواسته** را به Snakemake می‌دهید:

<div dir="ltr">

```bash
snakemake -c 1 counts/minigut_sample2.tsv
head -3 counts/minigut_sample2.tsv
```

</div>

<div dir="ltr">

```text
  16154 CP009257.1
   1178 NC_002516.2
    965 NC_004461.1
```

</div>

‏Acinetobacter baumannii (`CP009257.1`) با ۱۶٬۱۵۴، همان عدد `ground_truth.tsv`.

<details>
<summary>✋ امتحان کن: اگر بخواهید <code>counts/minigut3.tsv</code>، Snakemake چه می‌کند؟</summary>

‏`sample = minigut3`، پس ورودی `fastq/minigut3_R1.fastq.gz` لازم است که وجود ندارد: خطای `MissingInputException` (اشتباه رایج ۲). Snakemake **پیش از** اجرای هر دستوری این را می‌فهمد.

</details>

---

## ۵. قاعده‌ی `all` و `expand`: «همه را بساز»

نوشتن نام همه‌ی فایل‌ها در خط فرمان هم خسته‌کننده است. رسم این است که **نخستین** قاعده‌ی فایل، `all` باشد و همه‌ی خروجی‌های پایانی را بخواهد؛ اگر نام فایلی ندهید، Snakemake قاعده‌ی **نخست** را می‌سازد.

فایل کامل (همچنین در [`99_scripts_data/03_Snakemake_First/workflow/Snakefile`](../99_scripts_data/03_Snakemake_First/workflow/Snakefile)):

<div dir="ltr">

```python
SAMPLES = ["minigut", "minigut_sample2"]                      # ①

rule all:                                                     # ②
    input:
        expand("counts/{sample}.tsv", sample=SAMPLES),        # ③
        "stats/seqkit_stats.tsv",

rule count_reads:
    input:
        "fastq/{sample}_R1.fastq.gz",
    output:
        "counts/{sample}.tsv",
    shell:
        "zcat {input} | awk 'NR%4==1' | grep -oE '^@[A-Z]+_?[0-9]+[.][0-9]+' | cut -c2- "
        "| sort | uniq -c | sort -k1,1nr > {output}"

rule seqkit_stats:                                            # ④
    input:
        expand("fastq/{sample}_{read}.fastq.gz", sample=SAMPLES, read=["R1", "R2"]),
    output:
        "stats/seqkit_stats.tsv",
    shell:
        "seqkit stats -T {input} > {output}"
```

</div>

| نشانه | چه می‌کند |
| :---: | :--- |
| ① | یک **فهرست پایتون** (بخش ۰۳) از نام نمونه‌ها |
| ② | قاعده‌ی `all`: تنها `input` دارد، بی `output` و `shell`؛ «این‌ها را می‌خواهم» |
| ③ | ‏`expand` الگو را برای هر نمونه پر می‌کند: `["counts/minigut.tsv", "counts/minigut_sample2.tsv"]` |
| ④ | یک قاعده‌ی **بی wildcard** که همه‌ی ۴ فایل را با هم می‌گیرد؛ `expand` با دو wildcard همه‌ی ترکیب‌ها را می‌سازد (۲ نمونه × ۲ رید)؛ `seqkit stats -T` = جدول Tab‌دار (بخش ۰۲) |

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

rule count_reads:
    input: fastq/minigut_sample2_R1.fastq.gz
    output: counts/minigut_sample2.tsv
    reason: Missing output files: counts/minigut_sample2.tsv
    wildcards: sample=minigut_sample2
...
rule all:
    input: counts/minigut.tsv, counts/minigut_sample2.tsv, stats/seqkit_stats.tsv
    reason: Input files updated by another job: counts/minigut_sample2.tsv, counts/minigut.tsv, stats/seqkit_stats.tsv
...
```

</div>

(اگر پوشه‌ی `counts/` را از بخش‌های پیش دارید، نخست `rm -r counts` کنید تا همین را ببینید.) چهار کار: `count_reads` دو بار (یکی برای هر نمونه، با `wildcards: sample=…`)، `seqkit_stats` یک بار، و `all`.

### اجرا، با نمایش دستورها: `-p`

<div dir="ltr">

```bash
snakemake -c 1 -p
```

</div>

<div dir="ltr">

```text
localrule count_reads:
    input: fastq/minigut_R1.fastq.gz
    output: counts/minigut.tsv
    ...
Shell command: zcat fastq/minigut_R1.fastq.gz | awk 'NR%4==1' | grep -oE '^@[A-Z]+_?[0-9]+[.][0-9]+' | cut -c2- | sort | uniq -c | sort -k1,1nr > counts/minigut.tsv
...
Shell command: seqkit stats -T fastq/minigut_R1.fastq.gz fastq/minigut_R2.fastq.gz fastq/minigut_sample2_R1.fastq.gz fastq/minigut_sample2_R2.fastq.gz > stats/seqkit_stats.tsv
...
4 of 4 steps (100%) done
```

</div>

‏`-p` (*print*) دستور Bash کامل هر کار را، **پس از** جایگزینی `{input}` و `{output}`، چاپ می‌کند. برای فهمیدن و اشکال‌یابی بسیار سودمند است.

<div dir="ltr">

```bash
cat stats/seqkit_stats.tsv
```

</div>

<div dir="ltr">

```text
file	format	type	num_seqs	sum_len	min_len	avg_len	max_len
fastq/minigut_R1.fastq.gz	FASTQ	DNA	50000	6300000	126	126.0	126
fastq/minigut_R2.fastq.gz	FASTQ	DNA	50000	6300000	126	126.0	126
fastq/minigut_sample2_R1.fastq.gz	FASTQ	DNA	24993	3773943	151	151.0	151
fastq/minigut_sample2_R2.fastq.gz	FASTQ	DNA	24993	3773943	151	151.0	151
```

</div>

<details>
<summary>✋ امتحان کن: نمونه‌ی سومی به نام <code>gut3</code> با فایل‌های <code>fastq/gut3_R1.fastq.gz</code> و <code>_R2</code> دارید. چه چیزی را در Snakefile عوض می‌کنید؟</summary>

تنها فهرست: `SAMPLES = ["minigut", "minigut_sample2", "gut3"]`. قاعده‌ها دست نمی‌خورند. `snakemake -n` نشان می‌دهد `count_reads` **تنها برای gut3** و `seqkit_stats` دوباره (ورودی‌هایش عوض شده) اجرا می‌شوند. در ماژول ۰۴ فهرست نمونه‌ها را به یک فایل تنظیم (`config.yaml`) می‌بریم.

</details>

---

## ‏۶. Snakemake چه وقت دوباره می‌سازد؟

### ورودی تازه شد

<div dir="ltr">

```bash
touch fastq/minigut_R1.fastq.gz
snakemake -n
```

</div>

<div dir="ltr">

```text
job             count
------------  -------
count_reads         1
seqkit_stats        1
all                 1
total               3

rule seqkit_stats:
    reason: Updated input files: fastq/minigut_R1.fastq.gz
rule count_reads:
    reason: Updated input files: fastq/minigut_R1.fastq.gz
rule all:
    reason: Input files updated by another job: stats/seqkit_stats.tsv, counts/minigut.tsv
```

</div>

‏`touch` (بخش ۰۱) تاریخ تغییر فایل را «اکنون» می‌کند، گویی FASTQ عوض شده. Snakemake **تنها** کارهایی را دوباره می‌سازد که به این فایل وابسته‌اند: `count_reads` برای `minigut` (نه `minigut_sample2`) و `seqkit_stats`.

### خروجی پاک شد

<div dir="ltr">

```bash
snakemake -c 1 -q            # bring everything up to date (quiet)
rm counts/minigut.tsv
snakemake -n
```

</div>

<div dir="ltr">

```text
count_reads        1
all                1
total              2
    reason: Missing output files: counts/minigut.tsv
    reason: Input files updated by another job: counts/minigut.tsv
```

</div>

تنها همان یک فایل. (`-q` = خروجی کم؛ تنها خلاصه.)

| چه شد | ‏Snakemake چه می‌کند |
| :--- | :--- |
| خروجی نیست | می‌سازد (`Missing output files`) |
| ورودی از خروجی تازه‌تر است | دوباره می‌سازد (`Updated input files`) |
| دستور `shell` در Snakefile عوض شد | دوباره می‌سازد (`Code has changed since last execution`) |
| همه چیز تازه است | `Nothing to be done` |
| می‌خواهید به‌زور دوباره بسازد | ‏`snakemake -c 1 -F` (همه)، یا `--forcerun count_reads` (یک قاعده) |

---

## ۷. چهار اشتباه رایج

**۱. آکولادهای awk.** Snakemake هر `{…}` در `shell` را **نام یک متغیر** می‌پندارد:

<div dir="ltr">

```python
    shell:
        "zcat {input} | awk 'NR%4==1 {n++} END {print n}' > {output}"
```

</div>

<div dir="ltr">

```text
RuleException in rule n_reads in file ".../Snakefile", line 1:
NameError: The name 'n++' is unknown in this context. Please make sure that you defined that variable. Also note that braces not used for variable access have to be escaped by repeating them, i.e. {{print $1}}, when formatting the following:
zcat {input} | awk 'NR%4==1 {n++} END {print n}' > {output}
```

</div>

پیام خودش راه را می‌گوید: آکولادهای awk را **دوتایی** کنید: `awk 'NR%4==1 {{n++}} END {{print n}}'`. با این اصلاح، خروجی `50000` است.

**۲. ورودی‌ای که نیست.**

<div dir="ltr">

```bash
snakemake -c 1 counts/minigut3.tsv
```

</div>

<div dir="ltr">

```text
MissingInputException in rule count_reads in file ".../Snakefile", line 17:
Missing input files for rule count_reads:
    output: counts/minigut3.tsv
    wildcards: sample=minigut3
    affected files:
        fastq/minigut3_R1.fastq.gz
```

</div>

‏`affected files` دقیقاً فایل گمشده را می‌گوید. علت: نام نمونه‌ی نادرست، یا فایل در پوشه‌ی دیگر.

**۳. دستوری که شکست می‌خورد.** یک غلط تایپی (`zcatt`):

<div dir="ltr">

```text
/usr/bin/bash: line 1: zcatt: command not found
...
Error in rule count_reads:
    ...
    shell:
        zcatt fastq/minigut_R1.fastq.gz | wc -l > counts/minigut.tsv
        (command exited with non-zero exit code)
Removing output files of failed job count_reads since they might be corrupted:
counts/minigut.tsv
...
WorkflowError:
At least one job did not complete successfully.
```

</div>

‏Snakemake خط خطای Bash را نشان می‌دهد و **خروجی ناقص را پاک می‌کند**؛ پس هرگز نیمه‌کاره با درست اشتباه گرفته نمی‌شود (چیزی که `run_all.sh` ماژول ۰۴ بخش ۰۴ تضمین نمی‌کرد). Snakemake هر `shell` را با `set -euo pipefail` اجرا می‌کند، پس شکست هر بخش لوله دیده می‌شود.

**۴. فرورفتگی نادرست.** اگر خط فایل خروجی زیر `output:` فرو نرفته باشد:

<div dir="ltr">

```python
    output:
    "counts/{sample}.tsv"
```

</div>

<div dir="ltr">

```text
MissingRuleException:
No rule to produce counts/minigut.tsv (if you use input functions make sure that they don't raise unexpected exceptions).
```

</div>

پیام گمراه‌کننده است («قاعده‌ای نیست»): `output` تهی خوانده شد. وقتی مطمئنید قاعده هست ولی Snakemake نمی‌یابدش، **فرورفتگی‌ها** را بسنجید. هر سطح دقیقاً ۴ فاصله، نه Tab.

---

## 📘 برای کنجکاوها

- **‏`\.` و هشدار پایتون:** اگر به‌جای `[.]` بنویسید `\.`، این هشدار می‌آید: `SyntaxWarning: "\." is an invalid escape sequence. … Did you mean "\\."? A raw string is also an option.` (شماره‌ی خط آن به کد درونی Snakemake اشاره دارد، نه Snakefile شما). دستور هنوز کار می‌کند، ولی در نسخه‌های آینده‌ی پایتون نه. راه: `[.]`، یا `\\.`، یا رشته‌ی خام `r"…"`.
- ‏**‏`head` در `shell`:** چون Snakemake `pipefail` را روشن می‌کند، `zcat … | head` با کد ۱۴۱ شکست می‌خورد: `head` زودتر می‌بندد و `zcat` سیگنال SIGPIPE می‌گیرد. در قاعده‌ها از `head` پس از `zcat` بپرهیزید.
- **هم‌زمانی:** با `snakemake -c 4` کارهای مستقل (این‌جا دو `count_reads` و `seqkit_stats`) هم‌زمان اجرا می‌شوند.
- ‏**‏Nextflow و nf-core:** ابزار دیگری با همین هدف؛ بسیاری از پایپ‌لاین‌های آماده‌ی بیوانفورماتیک (nf-core) با آن نوشته شده‌اند. در بخش ۱۰.

---

## جمع‌بندی

- ‏Snakefile = چند **قاعده**؛ هر قاعده: `input`، `output`، `shell`.
- ‏Snakemake از **فایل خواسته** به عقب می‌رود و تنها چیزهای ناموجود یا کهنه را می‌سازد.
- ‏`{sample}` یک قاعده را برای همه‌ی نمونه‌ها کار می‌اندازد؛ `rule all` + `expand` همه‌ی خروجی‌ها را می‌خواهد.
- همیشه نخست `snakemake -n`؛ سپس `snakemake -c 1 -p`. ستون `reason` می‌گوید چرا.
- آکولادهای awk دوتایی؛ فرورفتگی ۴ فاصله؛ پیام `affected files` فایل گمشده را می‌گوید.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
snakemake -n                         # dry run: what and why (reason)
snakemake -c 1                       # run with 1 core (all = first rule)
snakemake -c 1 -p                    # ... and print every shell command
snakemake -c 1 counts/minigut.tsv    # make one specific file
snakemake -c 1 -q                    # quiet: summary only
snakemake -c 4                       # independent jobs in parallel
snakemake -c 1 -F                    # force: rebuild everything
snakemake -c 1 --forcerun count_reads
```

</div>

<div dir="ltr">

```python
SAMPLES = ["a", "b"]
rule all:
    input: expand("counts/{sample}.tsv", sample=SAMPLES)
rule name:
    input:  "fastq/{sample}_R1.fastq.gz",
    output: "counts/{sample}.tsv",
    shell:  "zcat {input} | awk '{{print $1}}' > {output}"     # awk braces doubled
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| گردش کار (*workflow*) | زنجیره‌ی گام‌های تحلیل، از داده‌ی خام تا نتیجه |
| ‏Snakefile | فایل قاعده‌های Snakemake |
| قاعده (*rule*) | یک گام: ورودی، خروجی و دستور |
| ‏wildcard | بخش متغیر نام فایل، مانند `{sample}` |
| ‏`expand` | ساختن فهرست نام فایل‌ها از یک الگو |
| ‏DAG | گراف کارها و وابستگی‌هایشان |
| اجرای آزمایشی (*dry-run*) | نمایش کارها بی اجرا (`-n`) |
| ‏job | یک اجرای یک قاعده برای یک مقدار wildcard |

---

## منابع

**مقاله و مستند**
- Mölder F, Jablonski KP, Letcher B, et al. (2021). *Sustainable data analysis with Snakemake.* F1000Research 10:33. https://doi.org/10.12688/f1000research.29032.2
- Snakemake documentation, *Snakemake Tutorial*: https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html
- Snakemake documentation, *Rules*: https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins University). دوره‌ای ویژه‌ی Snakemake در Coursera نیافتیم؛ نزدیک‌ترین برای خط لوله در ترمینال: https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Linux* (The Linux Foundation). دوره‌ای ویژه‌ی Snakemake در edX نیافتیم؛ نزدیک‌ترین: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux
- YouTube: *An introduction to Snakemake tutorial for beginners (CC248)* (Riffomonas Project): https://www.youtube.com/watch?v=r9PWnEmz_tc
- YouTube: *Introducing Snakemake* (Edinburgh Genomics Training): https://www.youtube.com/watch?v=NNPBDOBHlxo
- YouTube: *Snakemake #1 Writing your first Snakefile* (actually scientist): https://www.youtube.com/watch?v=Gg0SsEs16Jc

<sub>نشانی‌های YouTube در 2026-10-21 با oEmbed وارسی شدند. نشانی‌های Coursera و edX پیش‌تر در دوره به کار رفته‌اند؛ وارسی مستقیم همه‌ی نشانی‌ها در پایان دوره انجام می‌شود.</sub>

</div>
