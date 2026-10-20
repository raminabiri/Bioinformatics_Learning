<div dir="rtl">

# پاسخ تشریحی: نوشتن اسکریپت

> دستورها در 2026-10-20 با bash 5.2، GNU grep 3.11 و mawk 1.3.4 در پوشه‌ی `01_Linux/99_scripts_data/data` اجرا شدند.

---

## تمرین ۱: سلام با نام

<div dir="ltr">

```bash
#!/usr/bin/env bash
set -euo pipefail
echo "Hello, $1!"
```

</div>

<div dir="ltr">

```bash
bash hello_name.sh Sara
bash hello_name.sh
```

</div>

<div dir="ltr">

```text
Hello, Sara!
hello_name.sh: line 3: $1: unbound variable
```

</div>

2. بی ورودی، `$1` تعریف نشده است و **`-u`** آن را خطا می‌داند: «unbound variable». بی `set -u`، اسکریپت `Hello, !` چاپ می‌کرد. پیام `-u` درست است ولی برای کاربر چندان روشن نیست؛ برای همین در تمرین ۲ یک وارسی `if` با پیام راهنما می‌افزاییم.

---

## تمرین ۲: count_one.sh ایمن

<div dir="ltr">

```bash
#!/usr/bin/env bash
# Count reads in one FASTQ file given as the first argument
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "Usage: bash count_one_safe.sh file.fastq.gz" >&2
  exit 1
fi
f=$1
if [ ! -s "$f" ]; then
  echo "Error: file '$f' not found or empty" >&2
  exit 1
fi
n=$(zcat "$f" | wc -l)
echo "$f has $((n/4)) reads"
```

</div>

<div dir="ltr">

```bash
bash count_one_safe.sh fastq/minigut_R1.fastq.gz; echo $?
bash count_one_safe.sh;                           echo $?
bash count_one_safe.sh missing.gz;                echo $?
bash count_one_safe.sh a b;                       echo $?
```

</div>

<div dir="ltr">

```text
fastq/minigut_R1.fastq.gz has 50000 reads
0
Usage: bash count_one_safe.sh file.fastq.gz
1
Error: file 'missing.gz' not found or empty
1
Usage: bash count_one_safe.sh file.fastq.gz
1
```

</div>

- موفق: کد **۰**. هر سه اجرای نادرست: پیام روشن و کد **۱**.
- ‏`[ $# -ne 1 ]` یعنی «شمار ورودی‌ها **نابرابر** یک است» (`-ne` = *not equal*). این هم «بی ورودی» را می‌گیرد و هم «بیش از یک ورودی» را.
- سنجش با `count_one.sh` بخش ۳ درس: آن‌جا بی ورودی، پیام گیج‌کننده‌ی `gzip: .gz: …` و «۰ رید» می‌گرفتیم.

---

## تمرین ۳: اسکریپت آماده‌ی دوره

<div dir="ltr">

```bash
bash ../scripts/count_reads.sh fastq/*.fastq.gz
bash ../scripts/count_reads.sh fastq/*.fastq.gz > reads_table.tsv
bash ../scripts/count_reads.sh fastq/minigut_R1.fastq.gz fastq/x.fastq.gz > bad.tsv
cat bad.tsv
```

</div>

<div dir="ltr">

```text
sample	reads	mean_length
minigut_R1	50000	126.0
minigut_R2	50000	126.0
minigut_sample2_R1	24993	151.0
minigut_sample2_R2	24993	151.0
Error: file 'fastq/x.fastq.gz' not found or empty
sample	reads	mean_length
minigut_R1	50000	126.0
```

</div>

1. چهار ردیف؛ R1 و R2 هر نمونه برابرند (ماژول ۰۴، تمرین ۱).
2. **بله.** `printf` خط عنوان را در stdout می‌نویسد، پس در `reads_table.tsv` می‌رود.
3. پیام خطا **در ترمینال** دیده شد (چون با `>&2` به stderr رفت، و `>` تنها stdout را در فایل ریخت). در `bad.tsv` خط عنوان و ردیف `minigut_R1` هست: فایل یکم پیش از رسیدن به فایل نادرست پردازش شده بود و سپس اسکریپت ایستاد. پس **همیشه کد خروج را هم ببینید**؛ وجود فایل خروجی به این معنا نیست که همه چیز درست بوده است.

---

## تمرین ۴: پیش‌بینی کنید، سپس ایمن کنید

بی `set -euo pipefail`:

<div dir="ltr">

```text
cleanup.sh: line 3: cd: tmp_tset: No such file or directory
Cleaning in: ~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data
cleanup.sh
download.sh
ecoli_k12.fna
ecoli_k12.gff
fastq
ground_truth.tsv
host_chr21_region.fa
sample.fasta
tmp_test
```

</div>

1 و 2. خط ۲ پوشه‌ی `tmp_test` را ساخت؛ ولی خط ۳ یک **غلط تایپی** دارد (`tmp_tset`) و `cd` شکست خورد. اسکریپت **ادامه داد** و در **همان پوشه‌ی داده** ماند: خط ۴ نشانی پوشه‌ی داده را چاپ کرد و خط ۵ **فایل‌های داده** را فهرست کرد.

3. با `set -euo pipefail` (در خط دوم):

<div dir="ltr">

```text
cleanup.sh: line 4: cd: tmp_tset: No such file or directory
```

</div>

اسکریپت پس از شکست `cd` **ایستاد** (کد خروج ۱) و به خط‌های بعدی نرسید. (شماره‌ی خط ۴ شد، چون `set` یک خط افزود.) اگر خط پایانی `rm -r *` بود، بی `set -e` **همه‌ی داده‌ها** (ژنوم، FASTQها…) پاک می‌شدند. این یکی از رایج‌ترین فاجعه‌های واقعی در کار با ترمینال است.

---

## تمرین ۵ (چالشی): اسکریپت آمار FASTA

یک پاسخ ساده، تنها با ابزارهایی که در این بخش یاد گرفتید:

<div dir="ltr">

```bash
#!/usr/bin/env bash
# Simple statistics for one or more FASTA files: number of sequences, total length, GC% (N excluded)
# Usage: bash my_fasta_stats.sh file1.fa [file2.fa ...]
set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: bash my_fasta_stats.sh file1.fa [file2.fa ...]" >&2
  exit 1
fi

printf "file\tn_seqs\tlength\tGC%%\n"
for fa in "$@"; do
  if [ ! -s "$fa" ]; then
    echo "Error: file '$fa' not found or empty" >&2
    exit 1
  fi
  nseq=$(grep -c '^>' "$fa")
  len=$(grep -v '^>' "$fa" | tr -d '\n' | wc -c)
  gc=$(grep -v '^>' "$fa" | tr -cd 'GCgc' | wc -c)
  acgt=$(grep -v '^>' "$fa" | tr -cd 'ACGTacgt' | wc -c)
  echo "$fa $nseq $len $gc $acgt" | awk '{printf "%s\t%d\t%d\t%.2f\n", $1, $2, $3, $4/$5*100}'
done
```

</div>

<div dir="ltr">

```bash
bash my_fasta_stats.sh ecoli_k12.fna host_chr21_region.fa
```

</div>

<div dir="ltr">

```text
file	n_seqs	length	GC%
ecoli_k12.fna	1	4641652	50.79
host_chr21_region.fa	1	500000	40.05
```

</div>

نکته‌ها:
- ‏**GC بر پایه‌ی A، C، G، T** (بزرگ و کوچک): برای کروموزوم ۲۱ که ۲۰٪ N دارد، تقسیم بر طول کل ۳۲٪ نادرست می‌داد (ماژول ۰۸).
- در `printf`، نشانه‌ی `%` آغاز یک جای خالی است؛ برای چاپ خود `%` باید `%%` نوشت.
- هر فایل چهار بار خوانده می‌شود (چهار `grep`). برای فایل‌های بسیار بزرگ، یک برنامه‌ی `awk` که همه را در یک بار خواندن حساب کند، تندتر است. پاسخ کامل‌تر دوره، [fasta_stats.sh](../99_scripts_data/scripts/fasta_stats.sh)، همین کار را می‌کند و کوتاه‌ترین و بلندترین توالی و فایل‌های `.gz` را هم پشتیبانی می‌کند:

<div dir="ltr">

```text
ecoli_k12.fna	1	4641652	4641652	4641652	50.79
sample.fasta	1	14	14	14	NA(protein?)
host_chr21_region.fa	1	500000	500000	500000	40.05
```

</div>

(ستون‌ها: فایل، شمار توالی، طول کل، کوتاه‌ترین، بلندترین، GC%. برای فایل پروتئینی، GC معنا ندارد و `NA` چاپ می‌شود.)

</div>
