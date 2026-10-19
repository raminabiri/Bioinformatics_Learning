<div dir="rtl">

# پاسخ تشریحی: خط فرمان لینوکس (Bash)

> همه‌ی دستورها در 2026-10-19 (bash 5، GNU coreutils و awk) اجرا شده‌اند. نشانی‌ها نسبت به پوشه‌ی `01_Linux/99_scripts_data/02_Bash/data` است و `R=fastq`.

---

## تمرین ۱: پوشه‌ی یک پروژه بسازید

<div dir="ltr">

```bash
mkdir -p ecoli_project/data ecoli_project/results ecoli_project/scripts
cp ecoli_k12.gff ecoli_project/data/annotation.gff
ls -lh ecoli_project/data/annotation.gff
realpath ecoli_k12.gff
```

</div>

- `mkdir -p` هر سه پوشه (و پوشه‌ی پدرشان `ecoli_project`) را با هم می‌سازد. راه کوتاه‌تر: `mkdir -p ecoli_project/{data,results,scripts}`؛ Bash خودش `{…}` را به سه نام باز می‌کند.
- `ls -lh` اندازه را **2.3M** نشان می‌دهد.
- `realpath` نشانی مطلق را چاپ می‌کند؛ روی سرور دوره: `/data/bioinformatics_learning/01_Linux/99_scripts_data/02_Bash/data/ecoli_k12.gff`. روی کامپیوتر شما آغاز نشانی فرق دارد.

**اشتباه رایج:** `mkdir ecoli_project/data` بی `-p`، وقتی `ecoli_project` هنوز نیست، خطا می‌دهد: `No such file or directory`.

---

## تمرین ۲: به ژنوم نگاه کنید

<div dir="ltr">

```bash
head -n 1 ecoli_k12.fna
wc -l ecoli_k12.fna
grep -c '^>' ecoli_k12.fna
```

</div>

<div dir="ltr">

```text
>NC_000913.3 Escherichia coli str. K-12 substr. MG1655, complete genome
58022 ecoli_k12.fna
1
```

</div>

1. موجود: *Escherichia coli* سویه‌ی K-12، زیرسویه‌ی MG1655؛ ژنوم کامل.
2. **۵۸٬۰۲۲ خط.**
3. **یک توالی** (یک کروموزوم).
4. یک خط عنوان است، پس ۵۸٬۰۲۱ خط توالی: ۵۸٬۰۲۱ × ۸۰ = **۴٬۶۴۱٬۶۸۰**. طول درست ۴٬۶۴۱٬۶۵۲ است؛ تفاوت ۲۸ باز است، چون خط آخر کوتاه‌تر از ۸۰ است (۵۲ حرف دارد). تخمین بسیار نزدیک است.

---

## تمرین ۳: نمونه‌ی دوم را بشناسید

<div dir="ltr">

```bash
zcat $R/minigut_sample2_R1.fastq.gz | head -n 1
zcat $R/minigut_sample2_R1.fastq.gz | wc -l
```

</div>

<div dir="ltr">

```text
@CP009257.1_0_0/1
99972
```

</div>

1. `@CP009257.1_0_0/1`
2. **۹۹٬۹۷۲ خط**، یعنی ۹۹٬۹۷۲ ÷ ۴ = **۲۴٬۹۹۳ رید**.
3. در `minigut_R1` نام با `NC_006347.1` آغاز می‌شد و این‌جا با `CP009257.1`. این‌ها **شناسه‌ی ژنوم**اند (همان شناسه‌هایی که در بخش ۰۰ خواندیم). این داده شبیه‌سازی‌شده است و برنامه‌ی شبیه‌سازی، ژنوم سرچشمه‌ی هر رید را در نامش نوشته است. پس از روی نام ریدها می‌شود فهمید هر نمونه از چه موجوداتی ساخته شده (تمرین ۸). در داده‌ی واقعی این آگاهی را نداریم و باید آن را با ابزارهای بخش ۰۶ پیدا کنیم.

---

## تمرین ۴: الگوی طلایی، اول با چشم

<div dir="ltr">

```bash
grep -v '^#' ecoli_k12.gff | head -n 20 > small20.gff
cut -f3 small20.gff
cut -f3 small20.gff | sort | uniq -c
```

</div>

<div dir="ltr">

```text
      9 CDS
     10 gene
      1 region
```

</div>

1 و 2. **۱ region، ۱۰ gene، ۹ CDS.** با چشم: یک region و پس از آن gene و CDS یکی در میان، و خط بیستم یک gene است که CDS‌اش در خط بیست‌ویکم مانده است.

3. بی `sort`، خروجی **۲۰ ردیف** است و همه شمار ۱ دارند:

<div dir="ltr">

```text
      1 region
      1 gene
      1 CDS
      1 gene
      1 CDS
      …
```

</div>

چون `uniq -c` تنها خط‌های همانندِ **پشت سر هم** را یکی می‌کند، و این‌جا هیچ دو خط همانندی پشت سر هم نیستند (gene و CDS یکی در میان‌اند).

---

## تمرین ۵: چند ژن RNA؟

<div dir="ltr">

```bash
grep -c 'gene_biotype=tRNA' ecoli_k12.gff
awk -F'\t' '$3=="gene" && $9 ~ /gene_biotype=rRNA/' ecoli_k12.gff | wc -l
```

</div>

<div dir="ltr">

```text
86
22
```

</div>

1. **۸۶ ژن tRNA.**
2. **۲۲ ژن rRNA.**
3. **۷ اپرون**: ۷ × ۳ = ۲۱، به‌اضافه‌ی یک ژن 5S اضافه = ۲۲.

**چرا `grep -c` برای tRNA درست کار کرد؟** چون `gene_biotype=` تنها در خط‌های `gene` می‌آید. اگر واژه‌ی جستجو در خط‌های دیگر (مانند CDS) هم بود، شمار نادرست می‌شد. روش `awk` با دو شرط ایمن‌تر است.

---

## تمرین ۶: ژن gyrA کجاست؟

<div dir="ltr">

```bash
awk -F'\t' '$3=="gene" && $9 ~ /Name=gyrA;/ {print $4, $5, $7, $5-$4+1}' ecoli_k12.gff
```

</div>

<div dir="ltr">

```text
2336793 2339420 - 2628
```

</div>

1. آغاز **۲٬۳۳۶٬۷۹۳**، پایان **۲٬۳۳۹٬۴۲۰**، رشته‌ی **منفی**، طول **۲٬۶۲۸** نوکلئوتید (۸۷۵ اسیدآمینه + یک کدون پایان).
2. با NCBI Gene دقیقاً یکی است. همان آگاهی را یک بار با مرورگر و یک بار با یک خط دستور گرفتیم.

**نکته:** برای ژن روی رشته‌ی منفی، **آغاز زیستی** (کدون ATG) جای بزرگ‌تر، یعنی ۲٬۳۳۹٬۴۲۰، است. GFF همیشه عدد کوچک‌تر را در ستون ۴ می‌نویسد و جهت را در ستون ۷.

**اشتباه رایج:** نوشتن `/Name=gyrA/` بی `;`. در این ژنوم پاسخ یکی است، ولی در ژنوم‌های دیگر ممکن است ژنی مانند `gyrAB` هم پیدا شود.

---

## تمرین ۷: ژن‌های رشته‌ی منفی در یک مگاباز نخست

<div dir="ltr">

```bash
awk -F'\t' '$3=="gene" && $7=="-" && $4<=1000000' ecoli_k12.gff | wc -l
```

</div>

<div dir="ltr">

```text
437
```

</div>

1. **۴۳۷ ژن.**
2. برای «کاملاً درون»، **پایان** هم باید درون بازه باشد: `$5<=1000000`. تفاوت تنها در ژنی است که از مرز یک مگاباز می‌گذرد. در گزارش همیشه بنویسید تعریفتان چه بوده است.

---

## تمرین ۸: ریدها از کدام ژنوم‌ها آمده‌اند؟

<div dir="ltr">

```bash
zcat $R/minigut_sample2_R1.fastq.gz | awk 'NR%4==1' \
  | grep -oE '^@[A-Z]+_?[0-9]+\.[0-9]+' | sort | uniq -c | sort -rn | head -3
grep -E 'CP009257.1|NC_002516.2|NC_004461.1' ground_truth.tsv
```

</div>

<div dir="ltr">

```text
  16154 @CP009257.1
   1178 @NC_002516.2
    965 @NC_004461.1
minigut_sample2	16154	CP009257.1	Acinetobacter baumannii strain AB030
minigut_sample2	1178	NC_002516.2	Pseudomonas aeruginosa PAO1
minigut_sample2	965	NC_004461.1	Staphylococcus epidermidis ATCC 12228
```

</div>

1. *Acinetobacter baumannii* با **۱۶٬۱۵۴** رید، *Pseudomonas aeruginosa* با **۱٬۱۷۸**، و *Staphylococcus epidermidis* با **۹۶۵**.
2. شمارهای ما دقیقاً با جدول «پاسخ درست» شبیه‌سازی یکی است.

**الگو را بخوانیم:** `^@` آغاز خط نام؛ `[A-Z]+` یک یا چند حرف بزرگ (`CP` یا `NC`)؛ `_?` یک `_` که شاید باشد شاید نه؛ `[0-9]+\.[0-9]+` عدد، نقطه، عدد (نسخه). `\.` یعنی خود نقطه، چون `.` تنها «هر نویسه» است.

**اشتباه رایج:** `grep` روی کل FASTQ، نه تنها خط‌های نام. در خط کیفیت هم ممکن است نویسه‌ی `@` باشد و شمارش را خراب کند.

---

## تمرین ۹: جدول خلاصه‌ی نمونه‌ها با حلقه

<div dir="ltr">

```bash
for f in $R/*_R1.fastq.gz; do
  s=$(basename "$f" _R1.fastq.gz)
  zcat "$f" | awk -v s="$s" 'NR%4==2 {n++; L+=length($0); g+=gsub(/[GC]/,"")}
                             END{printf "%s\t%d\t%.1f\t%.2f\n", s, n, L/n, g/L*100}'
done > samples_summary.tsv
cat samples_summary.tsv
```

</div>

<div dir="ltr">

```text
minigut	50000	126.0	46.79
minigut_sample2	24993	151.0	40.51
```

</div>

1. `minigut`: ۵۰٬۰۰۰ رید، طول ۱۲۶، GC **۴۶٫۸٪**. `minigut_sample2`: ۲۴٬۹۹۳ رید، طول ۱۵۱، GC **۴۰٫۵٪**.
2. ریدهای `minigut_sample2` بلندترند و GC آن کمتر است. GC کمتر با ترکیب این نمونه جور است: بیشتر ریدهایش از *Acinetobacter baumannii* است (تمرین ۸) که GC پایینی دارد. این را در ماژول کنترل کیفیت بخش ۰۶ دقیق‌تر می‌بینیم.

**بهتر:** یک ردیف سرستون هم بیفزایید: `printf "sample\treads\tmean_len\tGC\n" > samples_summary.tsv` پیش از حلقه، و `>>` به جای `>` پس از `done`.

---

## تمرین ۱۰: اسکریپت را به کار ببرید و بیازمایید

<div dir="ltr">

```bash
bash ../scripts/count_reads.sh $R/*.fastq.gz
bash ../scripts/count_reads.sh;                 echo $?
bash ../scripts/count_reads.sh nofile.fastq.gz; echo $?
```

</div>

<div dir="ltr">

```text
sample	reads	mean_length
minigut_R1	50000	126.0
minigut_R2	50000	126.0
minigut_sample2_R1	24993	151.0
minigut_sample2_R2	24993	151.0
Usage: bash count_reads.sh file1.fastq.gz [file2 ...]
1
sample	reads	mean_length
Error: file 'nofile.fastq.gz' not found or empty
1
```

</div>

1. **بله، یکسان‌اند.** در توالی‌یابی دوخوانه (paired-end)، هر قطعه‌ی DNA از دو سر خوانده می‌شود: R1 از یک سر و R2 از سر دیگر. پس هر رید R1 یک جفت در R2 دارد و شمارشان باید برابر باشد. اگر برابر نبود، یکی از فایل‌ها ناقص است (دانلود نیمه‌کاره یا فایل خراب).
2. پیام راهنما (`Usage: …`) و کد خروج **۱**.
3. پیام `Error: file 'nofile.fastq.gz' not found or empty` و کد خروج **۱**.

کد خروج غیر صفر برای این است که اگر اسکریپت در یک زنجیره‌ی بزرگ‌تر (درس [گردش کار](../../05_Reproducible_Work/02_Workflows_Snakemake/)) اجرا شود، زنجیره بفهمد کاری شکست خورده و ادامه ندهد.

---

## تمرین ۱۱ (چالشی): اسکریپت آمار FASTA

یک پاسخ کامل: [scripts/fasta_stats.sh](../99_scripts_data/02_Bash/scripts/fasta_stats.sh)

<div dir="ltr">

```bash
bash ../scripts/fasta_stats.sh ecoli_k12.fna
bash ../scripts/fasta_stats.sh sample.fasta
bash ../scripts/fasta_stats.sh host_chr21_region.fa
```

</div>

<div dir="ltr">

```text
file	n_seqs	total_len	min_len	max_len	GC%
ecoli_k12.fna	1	4641652	4641652	4641652	50.79
file	n_seqs	total_len	min_len	max_len	GC%
sample.fasta	1	14	14	14	NA(protein?)
file	n_seqs	total_len	min_len	max_len	GC%
host_chr21_region.fa	1	500000	500000	500000	40.05
```

</div>

نکته‌های طراحی:
- **طول هر توالی:** طول توالی پیشین وقتی ثبت می‌شود که به عنوان بعدی برسیم. طول **آخرین** توالی باید در `END` ثبت شود. فراموش کردن این، رایج‌ترین اشکال است.
- **N در GC:** ناحیه‌ی کروموزوم ۲۱ انسان نزدیک به ۲۰٪ N دارد. اگر GC را بر کل طول تقسیم کنید ۳۲٪ می‌گیرید؛ تقسیم بر A+C+G+T عدد درست، یعنی **۴۰٫۰۵٪**، را می‌دهد.
- **تشخیص پروتئین:** اگر کمتر از ۹۰٪ نویسه‌ها A، C، G، T یا N باشند، فایل به احتمال زیاد پروتئینی است. این یک قاعده‌ی سرانگشتی است، نه تعریف دقیق.

</div>
