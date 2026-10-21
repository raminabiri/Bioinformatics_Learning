<div dir="rtl">

# پاسخ تشریحی: پایه‌های Git

خروجی‌ها از اجرای واقعی در 2026-10-21 (git 2.43) گرفته شده‌اند. **hashهای شما فرق می‌کنند** (درس، بخش ۴)؛ بقیه‌ی خروجی‌ها باید یکسان باشند.

---

## پاسخ ۱: مخزن اسکریپت‌های خودتان

<div dir="ltr">

```bash
cd ~/git_practice
git init -b main my_scripts
cd my_scripts
cp ~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/scripts/count_reads.sh .
cp ~/Bioinformatics_Learning-main/04_R_Packages/99_scripts_data/02_Run_Rscript/scripts/composition.R .
git add count_reads.sh composition.R
git commit -m "Add read counting and composition scripts"
```

</div>

<div dir="ltr">

```text
Initialized empty Git repository in /home/you/git_practice/my_scripts/.git/
[main (root-commit) 52b4382] Add read counting and composition scripts
 2 files changed, 59 insertions(+)
 create mode 100644 composition.R
 create mode 100644 count_reads.sh
```

</div>

**۲ فایل، ۵۹ خط تازه.** (اگر نام و ایمیل را پیش‌تر با `--global` تنظیم نکرده‌اید، پیام `Author identity unknown` می‌آید؛ درس، بخش ۳، گام ۲.)

---

## پاسخ ۲: نادیده یا نه؟

<div dir="ltr">

```text
?? notes.txt
```

</div>

تنها `notes.txt`:
- ‏`sample.fastq.gz` با الگوی `*.fastq.gz` نادیده گرفته شد، هر جای پروژه که باشد.
- ‏`results/plots/a.png` درون `results/` است و کل `results/` نادیده است.
- ‏`notes.txt` با هیچ الگویی جور نیست.

برای دیدن اینکه **کدام خط** `.gitignore` یک فایل را نادیده گرفته:

<div dir="ltr">

```bash
git check-ignore -v sample.fastq.gz results/plots/a.png
```

</div>

<div dir="ltr">

```text
.gitignore:2:*.fastq.gz	sample.fastq.gz
.gitignore:3:results/	results/plots/a.png
```

</div>

---

## پاسخ ۳: تنها tRNAها

<div dir="ltr">

```bash
git diff | tail -2
bash scripts/count_genes.sh $GFF
git commit -qam "Count only tRNA genes"
git log --oneline
```

</div>

<div dir="ltr">

```text
-awk -F'\t' '$3=="gene"' "$1" | cut -f7 | sort | uniq -c
+awk -F'\t' '$3=="gene" && $9 ~ /gene_biotype=tRNA/' "$1" | cut -f7 | sort | uniq -c
     49 +
     37 -
e4a7b0e Count only tRNA genes
31e9354 Count genes per strand
cc62ffa Add gene counting script and .gitignore
```

</div>

- (الف) خط کهنه‌ی `awk` با `-` و خط تازه با شرط افزوده‌ی `$9 ~ /gene_biotype=tRNA/` با `+`.
- (ب) **۴۹** tRNA روی رشته‌ی `+` و **۳۷** روی `-`؛ روی‌هم ۸۶، همان شمار tRNAهای RefSeq که در بخش ۰۱ دیدید.
- (ج) سه commit؛ تازه‌ترین بالا. (`-q` در `commit -qam` = بی‌صدا؛ خط خلاصه را چاپ نمی‌کند.)

**اشتباه رایج:** نوشتن `sed` بی `\` پیش از `$` و `&`: در جایگزین sed، `&` یعنی «همه‌ی متن یافته‌شده» و نتیجه درهم می‌شود. پس از هر `sed -i`، `git diff` بزنید؛ این بهترین وارسی است.

---

## پاسخ ۴: سه نسخه، سه پاسخ

<div dir="ltr">

```bash
for c in HEAD~2 HEAD~1 HEAD; do
    echo "== $c"
    bash <(git show $c:scripts/count_genes.sh) $GFF
done
```

</div>

<div dir="ltr">

```text
== HEAD~2
4506
== HEAD~1
   2216 +
   2290 -
== HEAD
     49 +
     37 -
```

</div>

هر نسخه پاسخ خودش را داد: همه‌ی ژن‌ها (۴٬۵۰۶)، ژن‌ها به تفکیک رشته، tRNAها به تفکیک رشته. `git status` پس از این حلقه هم تمیز است: هیچ فایلی عوض نشد.

---

## پاسخ ۵: «فایل را پاک کردم!»

<div dir="ltr">

```bash
rm scripts/count_genes.sh
git status --short
git restore scripts/count_genes.sh
ls scripts
git status
```

</div>

<div dir="ltr">

```text
 D scripts/count_genes.sh
count_genes.sh
On branch main
nothing to commit, working tree clean
```

</div>

‏`D` = پاک‌شده. چون فایل در آخرین commit بود، `git restore` آن را **همان‌گونه که در commit بود** برگرداند. ⚠️ اگر پس از آخرین commit تغییری در آن داده بودید، آن تغییر برنمی‌گردد؛ تنها نسخه‌ی ثبت‌شده. پس **زود‌به‌زود commit کنید**.

---

## پاسخ ۶: داده‌ای که ناخواسته add شد

<div dir="ltr">

```bash
git add -f data/raw/a.fastq.gz
git status --short
git rm --cached data/raw/a.fastq.gz
git status --short
ls data/raw
```

</div>

<div dir="ltr">

```text
A  data/raw/a.fastq.gz
rm 'data/raw/a.fastq.gz'
a.fastq.gz
```

</div>

- (الف) `A  data/raw/a.fastq.gz`: آماده‌ی ثبت.
- (ب) `git rm --cached`: از ناحیه‌ی آماده‌سازی بیرون آمد (`status` دیگر چیزی نشان نمی‌دهد، چون فایل باز هم نادیده گرفته می‌شود)، و `ls` نشان می‌دهد فایل روی دیسک **مانده** است.
- (ج) پس از commit، فایل در **تاریخچه** می‌ماند، حتی اگر در commit بعدی پاکش کنید: مخزن سنگین می‌شود (GitHub فایل‌های بالای ۱۰۰ مگابایت را نمی‌پذیرد) و اگر داده حساس باشد (داده‌ی بیمار)، با هر کپی مخزن پخش می‌شود. پاک کردن از تاریخچه کار دشوار و پرخطری است.

---

## پاسخ ۷ (فکری): چه چیزی commit شود؟

| فایل | تصمیم | چرا |
| :--- | :--- | :--- |
| `download.sh` | ✅ commit | با آن هر کسی داده را دوباره می‌گیرد |
| `reads/S1_R1.fastq.gz` | ❌ `.gitignore` | داده‌ی خام بزرگ؛ با `download.sh` بازسازی می‌شود |
| `run_deseq2.R` | ✅ commit | کد تحلیل؛ اصل کار |
| `results/deseq2_results.tsv` | ❌ `.gitignore` | خروجی؛ از روی کد و داده دوباره ساخته می‌شود |
| `envs/r_packages.yml` | ✅ commit | نسخه‌های ابزارها، برای بازسازی محیط |
| `ncbi_api_key.txt` | ❌ `.gitignore` | **رمز**؛ اگر در مخزن عمومی برود، هر کسی آن را به کار می‌برد |
| `README.md` | ✅ commit | راهنمای پروژه |
| `kraken_db/` | ❌ `.gitignore` | پایگاه داده‌ی بسیار بزرگ؛ تنها دستور دانلود و نسخه‌اش در README |

یک `.gitignore` برای این پروژه:

<div dir="ltr">

```text
reads/
results/
kraken_db/
*.fastq.gz
ncbi_api_key.txt
```

</div>

</div>
