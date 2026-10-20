<div dir="rtl">

# پاسخ تشریحی: نصب و وارسی بسته‌های R

خروجی‌ها از اجرای واقعی در 2026-10-20 روی R 4.6.1 گرفته شده‌اند. در محیط conda شما شاید نسخه‌ها کمی فرق کند (درس، بخش ۵).

---

## پاسخ ۱: کدام نصب است؟

<div dir="ltr">

```bash
Rscript $P/01_Install_Packages/scripts/check_packages.R vegan edgeR ape phyloseq dada2
```

</div>

<div dir="ltr">

```text
R: R version 4.6.1 (2026-06-24) 
vegan        2.7.6
edgeR        4.10.5
ape          5.8.1
phyloseq     NOT installed
dada2        NOT installed
```

</div>

- نسخه‌ی vegan: **2.7.6**.
- ‏`phyloseq` و `dada2` نصب نیستند.
- ‏`edgeR`: این خروجی از R سیستمِ سرور نویسنده است که edgeR را جداگانه دارد. در محیط `r_packages` دوره، edgeR در فهرست `envs/r_packages.yml` نیست، پس آن‌جا باید `NOT installed` ببینید. این خودش درسی است: **پاسخ به این بستگی دارد که کدام R را اجرا می‌کنید** (اشتباه رایج ۳).

---

## پاسخ ۲: سه دستور خراب

**دستور یکم: کوتیشن‌ها.**

<div dir="ltr">

```text
Error: object 'vegan' not found
Execution halted
```

</div>

‏Bash دوکوتیشن‌های درونی را خورد و به R تنها `packageVersion(vegan)` رسید. R `vegan` بی‌کوتیشن را **نام یک متغیر** پنداشت و آن را نیافت. درست: بیرون تک‌کوتیشن.

<div dir="ltr">

```bash
Rscript -e 'packageVersion("vegan")'
```

</div>

<div dir="ltr">

```text
[1] ‘2.7.6’
```

</div>

**دستور دوم: املای نام.**

<div dir="ltr">

```text
Error in packageVersion("Ggplot2") : there is no package called ‘Ggplot2’
Execution halted
```

</div>

نام درست با حرف کوچک است: `ggplot2`.

<div dir="ltr">

```bash
Rscript -e 'packageVersion("ggplot2")'
```

</div>

<div dir="ltr">

```text
[1] ‘4.0.3’
```

</div>

**دستور سوم: فروشگاه نادرست.** DESeq2 در Bioconductor است، نه CRAN. پیام `package ‘DESeq2’ is not available for this version of R` را می‌دهد (درس، بخش ۵). درست:

<div dir="ltr">

```bash
Rscript -e 'BiocManager::install("DESeq2", update = FALSE)'
# or, with conda:
conda install -c conda-forge -c bioconda "bioconductor-deseq2>=1.50"
```

</div>

**اشتباه رایج:** در دستور دوم تنها `G` را کوچک کنید ولی کوتیشن‌ها را هم از دستور یکم کپی کنید؛ آن‌گاه دوباره خطای `object … not found` می‌گیرید. هر بار **نخستین** خط `Error` را بخوانید.

---

## پاسخ ۳: فروشگاه درست

| بسته | مخزن | نام در conda | کانال |
| :--- | :--- | :--- | :--- |
| ‏phyloseq | Bioconductor | `bioconductor-phyloseq` | bioconda |
| ‏pheatmap | CRAN | `r-pheatmap` | conda-forge |
| ‏dada2 | Bioconductor | `bioconductor-dada2` | bioconda |
| ‏ape | CRAN | `r-ape` | conda-forge |
| ‏edgeR | Bioconductor | `bioconductor-edger` | bioconda |
| ‏vegan | CRAN | `r-vegan` | conda-forge |

راه پیدا کردن: جست‌وجوی «phyloseq bioconductor» به صفحه‌ی `bioconductor.org/packages/phyloseq` می‌رسد؛ «pheatmap» به `cran.r-project.org/package=pheatmap`. در conda همه‌ی نام‌ها **کوچک**‌اند (`edgeR` ← `edger`).

---

## پاسخ ۴: خواندن گزارش نصب

- (الف) خط دوم: `length 120438 bytes (117 KB)`. پس **۱۱۷ کیلوبایت**.
- (ب) خط `* installing *source* package ‘permute’` و پسوند فایل (`.tar.gz` در پوشه‌ی `src/contrib`) می‌گویند **از کد منبع** ساخته شد. permute کد C ندارد، پس ساختنش چند ثانیه بیشتر نکشید.
- (ج) خط پایانی: **`* DONE (permute)`**. خط‌های `** testing if installed package can be loaded …` هم نشان می‌دهند R پس از نصب یک بار آزمود که بسته باز می‌شود.

اگر نصب شکست بخورد، به‌جای `DONE` چیزی مانند `ERROR: compilation failed for package` و در پایان `installation of package ‘…’ had non-zero exit status` می‌آید.

---

## پاسخ ۵: پیام‌ها یا خطا؟

<div dir="ltr">

```bash
Rscript -e 'library(vegan); cat("ok\n")'
echo "exit=$?"
```

</div>

<div dir="ltr">

```text
Loading required package: permute
ok
exit=0
```

</div>

- (الف) دو خط؛ واژه‌ی `Error` در آن نیست.
- (ب) vegan برای کار خود به بسته‌ی **permute** نیاز دارد (یک **وابستگی**) و آن را خودکار باز کرد. پیام آگاهی است، نه خطا.
- (ج) دو نشانه: `ok`، که **پس از** `library` آمده، چاپ شد؛ و کد خروج `0` است (کد خروج را در ماژول اسکریپت‌نویسی بخش ۰۱ دیدید). اگر `library` شکست می‌خورد، R همان‌جا با `Execution halted` می‌ایستاد، `ok` چاپ نمی‌شد و کد خروج `1` می‌بود.

---

## پاسخ ۶: «نصب کردم، ولی پیدا نمی‌شود!»

دو دستور:

<div dir="ltr">

```bash
which Rscript
Rscript -e '.libPaths()'
```

</div>

علت محتمل: محیط `r_packages` امروز **فعال نیست** (ترمینال تازه باز شده و `conda activate r_packages` زده نشده). پس `Rscript` به R دیگری اشاره می‌کند که phyloseq را ندارد.

نمونه‌ی واقعی همین وضعیت روی سرور نویسنده: R سیستم DESeq2 را دارد، ولی در یک محیط conda دیگر (به نام `deg_r`) که DESeq2 در آن نصب نشده:

<div dir="ltr">

```bash
conda activate deg_r
which Rscript
Rscript -e '.libPaths()'
Rscript -e 'library(DESeq2)'
```

</div>

<div dir="ltr">

```text
/home/ubuntu/miniforge3/envs/deg_r/bin/Rscript
[1] "/home/ubuntu/miniforge3/envs/deg_r/lib/R/library"
Error in library(DESeq2) : there is no package called ‘DESeq2’
Execution halted
```

</div>

‏`which` نشان می‌دهد R از درون محیط `deg_r` اجرا شده و `.libPaths()` نشان می‌دهد تنها کتابخانه‌ی همان محیط جست‌وجو می‌شود. راه درست: `conda activate r_packages` و دوباره اجرا.

---

## پاسخ ۷: افزودن یک بسته به فایل محیط

خط تازه، زیر بقیه‌ی بسته‌های Bioconductor:

<div dir="ltr">

```yaml
  - bioconductor-phyloseq>=1.50
```

</div>

- ‏`>=`: تا conda نسخه‌ای بسیار کهنه را برنگزیند، همان‌گونه که بی‌محدودیت برای ggtree نسخه‌ی 1.2.12 را برگزید. اسکریپت‌ها و راهنماهای امروز برای نسخه‌های تازه نوشته شده‌اند.
- پیش از ساختن: `conda env create --dry-run -f envs/r_packages.yml` (یا برای محیط موجود: `conda install --dry-run …`). در فهرستی که چاپ می‌کند، نسخه‌ی برگزیده‌ی هر بسته را ببینید.

</div>
