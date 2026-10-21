<div dir="rtl">

# تمرین‌ها: پایه‌های Git

تمرین‌های ۲ تا ۶ در همان مخزن `~/git_practice/ecoli_project` درس انجام می‌شوند (پس از دو commit درس). `GFF` را دوباره تعریف کنید:

<div dir="ltr">

```bash
cd ~/git_practice/ecoli_project
GFF=~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data/ecoli_k12.gff
```

</div>

---

## تمرین ۱: مخزن اسکریپت‌های خودتان
> **راهنمایی:** درس، بخش‌های ۳ و ۴: `git init`، `git add`، `git commit -m`.

یک مخزن تازه به نام `~/git_practice/my_scripts` بسازید. دو اسکریپتی را که در دوره به کار بردید در آن کپی کنید: `count_reads.sh` (بخش ۰۱، `01_Linux/99_scripts_data/scripts`) و `composition.R` (بخش ۰۴، `04_R_Packages/99_scripts_data/02_Run_Rscript/scripts`). هر دو را در **یک** commit ثبت کنید. خط خلاصه‌ی commit چند فایل و چند خط تازه گزارش می‌کند؟

---

## تمرین ۲: نادیده یا نه؟
> **راهنمایی:** درس، بخش ۴، جدول `.gitignore`. پیش‌بینی کنید، سپس `git status --short` بزنید.

در `ecoli_project` این سه را بسازید و **پیش از اجرا** پیش‌بینی کنید کدام در `git status --short` دیده می‌شوند:

<div dir="ltr">

```bash
touch sample.fastq.gz notes.txt
mkdir -p results/plots && touch results/plots/a.png
git status --short
```

</div>

پس از پاسخ، `sample.fastq.gz` و `notes.txt` را پاک کنید.

---

## تمرین ۳: تنها tRNAها
> **راهنمایی:** درس، بخش ۵ (تغییر با `sed -i`، دیدن با `git diff`، ثبت با `commit -am`). شرط awk: `$9 ~ /gene_biotype=tRNA/` (بخش ۰۱، ماژول awk).

اسکریپت را طوری عوض کنید که **تنها ژن‌های tRNA** را به تفکیک رشته بشمارد:

<div dir="ltr">

```bash
sed -i 's/\$3=="gene"/$3=="gene" \&\& $9 ~ \/gene_biotype=tRNA\//' scripts/count_genes.sh
```

</div>

(الف) `git diff` چه خطی را `-` و چه خطی را `+` نشان می‌دهد؟ (ب) اسکریپت را اجرا کنید: چند tRNA روی هر رشته؟ (ج) با پیام «Count only tRNA genes» ثبت کنید و `git log --oneline` بزنید.

---

## تمرین ۴: سه نسخه، سه پاسخ
> **راهنمایی:** درس، بخش ۶، `git show` و `bash <( … )`. حلقه‌ی `for` بخش ۰۱.

با یک حلقه، **هر سه** نسخه‌ی اسکریپت (`HEAD~2`، `HEAD~1`، `HEAD`) را روی `$GFF` اجرا کنید، بی‌آنکه پوشه‌ی کاری عوض شود. خروجی هر کدام چیست؟

---

## تمرین ۵: «فایل را پاک کردم!»
> **راهنمایی:** درس، بخش ۶، `git restore`. حرف `D` در `status --short` یعنی *deleted*.

‏`rm scripts/count_genes.sh` بزنید (فایل commit‌شده است). `git status --short` چه می‌گوید؟ فایل را برگردانید و نشان دهید پوشه تمیز است.

---

## تمرین ۶: داده‌ای که ناخواسته add شد
> **راهنمایی:** درس، اشتباه رایج ۲: `git rm --cached`.

همکارتان با `git add -f data/raw/a.fastq.gz` فایل داده را به ناحیه‌ی آماده‌سازی افزوده ولی هنوز commit نکرده. (الف) `git status --short` چه نشان می‌دهد؟ (ب) چگونه آن را از Git بیرون می‌آورید، بی‌آنکه فایل از دیسک پاک شود؟ (ج) چرا مهم است این کار **پیش از** commit انجام شود؟

---

## تمرین ۷ (فکری): چه چیزی commit شود؟
> **راهنمایی:** درس، بخش ۲ (قاعده‌ی طلایی) و کادر کنجکاوها.

پوشه‌ی پروژه‌ی پایان‌نامه‌ی شما این‌ها را دارد. برای هر کدام بگویید commit شود یا در `.gitignore` برود، و چرا:
‏`download.sh`، `reads/S1_R1.fastq.gz`، `run_deseq2.R`، `results/deseq2_results.tsv`، `envs/r_packages.yml`، `ncbi_api_key.txt`، `README.md`، `kraken_db/` (۸ گیگابایت).

</div>
