<div dir="rtl">

# پاسخ تشریحی: اجرای اسکریپت آماده‌ی R

خروجی‌ها از اجرای واقعی در 2026-10-20 (R 4.6.1، ggplot2 4.0.3) گرفته شده‌اند.

---

## پاسخ ۱: نمونه‌ی دیگر

<div dir="ltr">

```bash
Rscript $P/02_Run_Rscript/scripts/composition.R ground_truth.tsv minigut minigut.png
```

</div>

<div dir="ltr">

```text
       genus percent
 Escherichia   42.18
 Bacteroides   57.82
saved minigut_genus_R.tsv and minigut.png 
```

</div>

‏Bacteroides **۵۷٫۸۲٪**. جدول خروجی **`minigut_genus_R.tsv`** است: اسکریپت نامش را از نام نمونه می‌سازد (خط پایانی خروجی همین را می‌گوید).

---

## پاسخ ۲: خواندن یک اسکریپت ناآشنا

<div dir="ltr">

```bash
head -12 $P/03_Bioc_Examples/scripts/run_deseq2.R
grep -n "library" $P/03_Bioc_Examples/scripts/run_deseq2.R
```

</div>

<div dir="ltr">

```text
# run_deseq2.R: which genes change between two groups of RNA-seq samples? (DESeq2)
# Usage: Rscript run_deseq2.R counts.tsv samples.tsv WT deseq2
#   counts.tsv  : first column gene_id, then one column of read counts per sample
#   samples.tsv : columns sample and condition; sample names = column names of counts.tsv
#   WT          : the reference (control) group; log2FoldChange = other group vs this one
#   deseq2      : prefix of the output files
# Writes: <prefix>_results.tsv, <prefix>_MA.png, <prefix>_PCA.png
...
24:  library(DESeq2)
25:  library(ggplot2)
```

</div>

- (الف) **چهار ورودی:** جدول شمارش ریدها، جدول نمونه‌ها، نام گروه مرجع (شاهد) و پیشوند نام خروجی‌ها. بررسی `length(args) != 4` در خط‌های بعدی هم همین را می‌گوید.
- (ب) **‏DESeq2** و **ggplot2**.
- (ج) `test_results.tsv`، `test_MA.png`، `test_PCA.png` (خط `# Writes:`).

نکته: این اسکریپت یک بلوک تنظیم هم دارد (`# ---- settings you may change ----`) با `padj_cutoff <- 0.05`. اگر بخواهید چیزی را عوض کنید، تنها همان‌جاست.

---

## پاسخ ۳: پزشک خطا

**الف:** هشدار زیر خطا می‌گوید `cannot open file 'ground_truth.csv': No such file or directory`. پسوند فایل `.tsv` است نه `.csv`. `Calls: read.delim -> …` هم نشان می‌دهد خطا هنگام **خواندن جدول** رخ داد.

<div dir="ltr">

```bash
Rscript $P/02_Run_Rscript/scripts/composition.R ground_truth.tsv minigut x.png
```

</div>

**ب:** این پیام را خود اسکریپت می‌دهد: نمونه‌ای به نام `Minigut` در جدول نیست. نام‌ها به بزرگی و کوچکی حرف حساس‌اند. نام‌های درست:

<div dir="ltr">

```bash
cut -f1 ground_truth.tsv | sort | uniq -c
```

</div>

<div dir="ltr">

```text
      2 minigut
     21 minigut_sample2
      1 sample
```

</div>

‏(`sample` سرستون است.) درست: `minigut`.

**ج:** پیام از خود Rscript است (`Fatal error`)، پیش از آنکه R حتی آغاز کند: فایل اسکریپت در پوشه‌ی کنونی نیست. مسیر کامل بدهید: `$P/02_Run_Rscript/scripts/composition.R`.

---

## پاسخ ۴: خطا کجا می‌رود؟

<div dir="ltr">

```bash
Rscript $P/02_Run_Rscript/scripts/composition.R ground_truth.csv minigut x.png > e.out 2> e.err
echo "exit=$?"
wc -c e.out e.err
```

</div>

<div dir="ltr">

```text
exit=1
  0 e.out
229 e.err
229 total
```

</div>

- (الف) کد خروج **۱**.
- (ب) ‏`e.out` خالی است: اسکریپت پیش از چاپ هر جدولی ایستاد. همه‌ی پیام خطا (۲۲۹ بایت، همان پیام «الف») در `e.err` است، چون R خطاها و هشدارها را به **stderr** می‌فرستد.

<div dir="ltr">

```bash
Rscript $P/02_Run_Rscript/scripts/composition.R ground_truth.tsv Minigut x.png > bad.out 2> bad.err
echo "exit=$?"
cat bad.out
cat bad.err
```

</div>

<div dir="ltr">

```text
exit=1
No rows for sample: Minigut 
```

</div>

- (ج) پیام در **`bad.out`** است و `bad.err` خالی است! نویسنده‌ی اسکریپت پیام را با `cat` نوشت و `cat` به stdout می‌نویسد. پس **تنها به فایل err بسنده نکنید**؛ کد خروج (`1`) مطمئن‌ترین نشانه‌ی شکست است. (این همان کاری است که `set -e` در Bash بر پایه‌اش کار می‌کند؛ ماژول ۰۴.)

---

## پاسخ ۵: نمودار پهن‌تر

<div dir="ltr">

```bash
file composition_R.png
cp $P/02_Run_Rscript/scripts/composition.R big.R
sed -i 's/width = 7/width = 10/' big.R
grep -n "width" big.R
Rscript big.R ground_truth.tsv minigut_sample2 big.png
file big.png
```

</div>

<div dir="ltr">

```text
composition_R.png: PNG image data, 840 x 720, 8-bit/color RGB, non-interlaced
40:ggsave(png_file, p, width = 10, height = 6, dpi = 120)
...
saved minigut_sample2_genus_R.tsv and big.png 
big.png: PNG image data, 1200 x 720, 8-bit/color RGB, non-interlaced
```

</div>

پیش: **۸۴۰ × ۷۲۰**، پس: **۱۲۰۰ × ۷۲۰**. پیکسل = اینچ × dpi: ۷ × ۱۲۰ = ۸۴۰ و ۱۰ × ۱۲۰ = ۱۲۰۰؛ بلندی ۶ × ۱۲۰ = ۷۲۰ عوض نشد. برای مجله‌ها که اغلب ۳۰۰ dpi می‌خواهند، `dpi = 120` را به `300` برسانید.

**اشتباه رایج:** `sed -i 's/7/10/'` بی‌دقت، که نخستین `7` فایل را (هر جا باشد) عوض می‌کند. الگو را تا جای ممکن دقیق بنویسید (`width = 7`) و پس از آن با `grep -n` وارسی کنید.

---

## پاسخ ۶: پایتون و R، یک پاسخ؟

<div dir="ltr">

```bash
python3 ~/Bioinformatics_Learning-main/03_Python/99_scripts_data/06_Pandas/scripts/composition.py \
    ground_truth.tsv minigut_sample2 py.png
diff minigut_sample2_genus_R.tsv minigut_sample2_genus.tsv
```

</div>

<div dir="ltr">

```text
12c12
< Escherichia	2
---
> Escherichia	2.0
```

</div>

تنها یک سطر فرق دارد: Escherichia در R `2` و در پایتون `2.0` نوشته شده است. **عدد یکی است** (۲٪)؛ تنها شکل نوشتن فرق دارد: pandas عدد اعشاری را همیشه با `.0` می‌نویسد و R صفرهای پایانی را می‌اندازد. همه‌ی سطرهای دیگر (۱۸ سطر، با سرستون) نویسه‌به‌نویسه یکسان‌اند. (`diff` جای سطر را هم می‌گوید: `12c12` = سطر ۱۲ در هر دو «عوض شده» است.)

---

## پاسخ ۷: جمله‌ی روش‌ها

<div dir="ltr">

```bash
Rscript -e 'library(ggplot2); sessionInfo()' > versions.txt
head -1 versions.txt
grep -A1 "other attached" versions.txt
```

</div>

<div dir="ltr">

```text
R version 4.6.1 (2026-06-24)
other attached packages:
[1] ggplot2_4.0.3
```

</div>

جمله: «ترکیب جنس‌ها در هر نمونه با اسکریپت `composition.R` در R نسخه‌ی 4.6.1 حساب و با ggplot2 نسخه‌ی 4.0.3 رسم شد.»

چرا مهم است: بسته‌ها با هر نسخه کمی عوض می‌شوند (پیش‌فرض‌ها، الگوریتم‌ها). در ماژول ۰۱ دیدید DESeq2 در conda (1.50.2) و در Bioconductor (1.52.0) نسخه‌ی یکسان ندارد. بی ثبت نسخه، کسی که می‌خواهد کار شما را تکرار کند (حتی خود شما شش ماه بعد) نمی‌داند چرا رقم‌ها کمی فرق دارند.

</div>
