# پاسخ تشریحی: خط فرمان لینوکس (Bash)

> اجرا شده در 2026-10-13 (bash 5، GNU coreutils/awk). مسیرها نسبت به `01_Computing_Foundations/01_Bash_Linux/data` هستند.

---

## تمرین ۱

```bash
mkdir -p ecoli_project/{data,results,scripts}
cp ecoli_k12.gff ecoli_project/data/annotation.gff
ls -lh ecoli_project/data/annotation.gff
realpath ecoli_project/data/annotation.gff
```
- `{data,results,scripts}` (brace expansion) را خود Bash قبل از اجرای `mkdir` به سه آرگومان باز می‌کند. `-p` پوشه‌ی والد را هم می‌سازد و اگر پوشه‌ها از قبل وجود داشته باشند خطا نمی‌دهد.
- `cp` با مقصدی که نام فایل دارد، کپی و تغییر نام را یک‌جا انجام می‌دهد.
- `ls -lh` حجم را حدود `2.3M` نشان می‌دهد.

**اشتباه رایج:** `mkdir ecoli_project/data` بدون `-p` وقتی `ecoli_project` هنوز وجود ندارد خطا می‌دهد.

---

## تمرین ۲

```bash
# ۱
grep -c 'gene_biotype=tRNA' ecoli_k12.gff
awk -F'\t' '$3=="gene" && $9 ~ /gene_biotype=rRNA/' ecoli_k12.gff | wc -l
# ۲
awk -F'\t' '$3=="gene" && $7=="-" && $4<=1000000' ecoli_k12.gff | wc -l
# ۳
awk -F'\t' '$3=="gene" && $9 ~ /Name=gyrA;/ {print $4, $5, $7, $5-$4+1}' ecoli_k12.gff
```
```text
86
22
437
2336793 2339420 - 2628
```
1. **۸۶ ژن tRNA** و **۲۲ ژن rRNA** (۷ اپران rRNA × ۳ ژن 16S/23S/5S، به‌علاوه‌ی یک ژن 5S اضافه).
   - چرا `grep -c` برای tRNA درست کار کرد؟ چون `gene_biotype=` فقط در سطرهای `gene` آمده است. در حالت کلی امن‌تر است مثل خط دوم با awk هم نوع feature (`$3=="gene"`) و هم ویژگی را بررسی کنید.
2. **۴۳۷ ژن.** شرط `$4<=1000000` ژن‌هایی را که در یک مگاباز اول **شروع** می‌شوند می‌شمارد. اگر منظور «کاملاً درون» بازه باشد، باید `$5<=1000000` گذاشت. در گزارش تعریفتان را دقیق بنویسید.
3. gyrA روی **رشته‌ی منفی** از ۲٬۳۳۶٬۷۹۳ تا ۲٬۳۳۹٬۴۲۰ است و **۲٬۶۲۸ باز** طول دارد: 875 × 3 + 3 (کدون پایان) = 2628. ✓
   - برای ژن روی رشته‌ی منفی، **شروع زیستی** ژن (کدون ATG) مختصات **بزرگ‌تر** (2,339,420) است. GFF همیشه شروع < پایان می‌نویسد و جهت را در ستون ۷ می‌گذارد.

---

## تمرین ۳

```bash
grep -v '^>' ecoli_k12.fna | tr -d '\n' | wc -c                       # ۱ طول
gc=$(grep -v '^>' ecoli_k12.fna | tr -d '\n' | tr -cd 'GCgc' | wc -c)  # ۲
at=$(grep -v '^>' ecoli_k12.fna | tr -d '\n' | tr -cd 'ATat' | wc -c)
awk -v g=$gc -v a=$at 'BEGIN{printf "GC = %.2f%%\n", g/(g+a)*100}'
grep -v '^>' ecoli_k12.fna | tr -cd 'Nn' | wc -c                       # ۳
```
```text
4641652
GC = 50.79%
0
```
- طول **۴٬۶۴۱٬۶۵۲ باز** است و GC **۵۰٫۷۹٪**. هر دو با `datasets` در بخش ۰۰ (`length=4641652 GC=51%`) یکسان‌اند.
- `tr -cd 'GCgc'` یعنی همه‌چیز **جز** (`-c` = complement) این حروف را حذف کن (`-d`).
- **۰ باز N:** این ژنوم مرجع کامل و بسته است.

۴. `wc -c` اشتباه است چون:
   - (الف) **خط هدر** (حدود ۷۰ کاراکتر) را هم می‌شمارد.
   - (ب) **کاراکترهای پایان خط** (`\n`، یکی برای هر خط، یعنی ۵۸٬۰۲۲) را هم می‌شمارد.

   اگر فایل در ویندوز ساخته شده باشد، `\r` هم اضافه می‌شود.

---

## تمرین ۴

```bash
R=../../../03_Metagenomics/data/raw
zcat $R/minigut_sample2_R1.fastq.gz | awk 'NR%4==1' \
  | sed -E 's/^@([A-Z]+_?[0-9]+\.[0-9]+).*/\1/' | sort | uniq -c | sort -rn | head -3

for f in $R/*_R1.fastq.gz; do
  printf "%s\t" "$(basename $f)"; zcat "$f" | awk 'NR%4==2 && /N/ {c++} END{print c+0}'
done
```
```text
  16154 CP009257.1
   1178 NC_002516.2
    965 NC_004461.1
minigut_R1.fastq.gz	0
minigut_sample2_R1.fastq.gz	15
```
1. *Acinetobacter baumannii* (`CP009257.1`) با ۱۶٬۱۵۴، *Pseudomonas aeruginosa* (`NC_002516.2`) با ۱٬۱۷۸ و *Staphylococcus epidermidis* (`NC_004461.1`) با ۹۶۵ رید. (نام گونه‌ها در `03_Metagenomics/data/ground_truth.tsv` آمده است.)
2. `minigut`: **۰**، `minigut_sample2`: **۱۵** رید.
   - نکته‌ی کلیدی: `NR%4==2` فقط **خط توالی** را بررسی می‌کند. اگر `grep -c N` روی کل FASTQ بزنید، خطوط **کیفیت** و **هدر** هم بررسی می‌شوند و عدد بی‌معنی می‌گیرید (در Phred+33، کاراکتر `N` یعنی Q45).

---

## تمرین ۵

```bash
for f in $R/*_R1.fastq.gz; do
  s=$(basename "$f" _R1.fastq.gz)
  zcat "$f" | awk -v s="$s" 'NR%4==2 {n++; L+=length($0); g+=gsub(/[GC]/,"")}
                             END{printf "%s\t%d\t%.1f\t%.2f\n", s, n, L/n, g/L*100}'
done > samples_summary.tsv
cat samples_summary.tsv
```
```text
minigut	50000	126.0	46.79
minigut_sample2	24993	151.0	40.51
```
- `gsub(/[GC]/,"")` تعداد جایگزینی‌ها را برمی‌گرداند، یعنی تعداد G و C. (این تابع خط را تغییر می‌دهد، ولی بعد از آن به خط نیازی نداریم.)
- این اعداد با `seqkit stats` و FastQC در ماژول 03/01 یکسان‌اند (GC 46.8 و 40.5).
- بهتر است یک سطر سرستون هم اضافه کنید: `printf "sample\treads\tmean_len\tGC\n"` قبل از حلقه، و خروجی کل `{ ...; }` را redirect کنید.

---

## تمرین ۶ (چالشی)

پاسخ کامل: [scripts/fasta_stats.sh](scripts/fasta_stats.sh)

```bash
bash ../scripts/fasta_stats.sh ecoli_k12.fna
bash ../scripts/fasta_stats.sh sample.fasta
bash ../scripts/fasta_stats.sh ../../../03_Metagenomics/data/host/host_chr21_region.fa
bash ../scripts/fasta_stats.sh nonexist.fa; echo "exit=$?"
```
```text
file	n_seqs	total_len	min_len	max_len	GC%
ecoli_k12.fna	1	4641652	4641652	4641652	50.79
sample.fasta	1	14	14	14	NA(protein?)
host_chr21_region.fa	1	500000	500000	500000	40.05
Error: 'nonexist.fa' not found or empty
exit=1
```

نکته‌های طراحی:
- **ذخیره‌ی طول هر توالی:** طول توالی قبلی وقتی ثبت می‌شود که به هدر بعدی برسیم. طول **آخرین** توالی هم در بلوک `END` ثبت می‌شود. فراموش کردن این دومی رایج‌ترین باگ است.
- **N در GC:** ناحیه‌ی chr21 حدود ۲۰٪ N دارد (بخش 03/02). اگر GC را بر طول کل تقسیم کنید، ۳۲٪ می‌گیرید. تقسیم بر A+C+G+T عدد درست، یعنی ۴۰٫۰۵٪، را می‌دهد.
- **تشخیص پروتئین:** اگر کمتر از ۹۰٪ کاراکترها از A، C، G، T یا N باشند، فایل احتمالاً پروتئینی است. این یک قاعده‌ی سرانگشتی است، نه تعریف دقیق. توالی پروتئینی غنی از A، C، G و T در تئوری می‌تواند آن را فریب دهد.
- **`.gz`:** با `case` بین `zcat` و `cat` انتخاب می‌شود. ورودی فشرده و ساده هر دو کار می‌کنند.
- **خطا به stderr (`>&2`) و `exit 1`:** اگر این اسکریپت در یک پایپلاین (Snakemake، ماژول ۰۵) استفاده شود، مدیر جریان کار از کد خروجی می‌فهمد مرحله شکست خورده است.
