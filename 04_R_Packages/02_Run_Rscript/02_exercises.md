<div dir="rtl">

# تمرین‌ها: اجرای اسکریپت آماده‌ی R

پیش از آغاز:

<div dir="ltr">

```bash
conda activate r_packages
cd ~/r_practice
P=~/Bioinformatics_Learning-main/04_R_Packages/99_scripts_data
```

</div>

---

## تمرین ۱: نمونه‌ی دیگر
> **راهنمایی:** بخش ۳ درس. تنها ورودی دوم (نام نمونه) و سوم (نام PNG) را عوض کنید.

‏`composition.R` را برای نمونه‌ی `minigut` اجرا کنید. چند درصد ریدها از Bacteroides است؟ نام جدول خروجی چیست؟

---

## تمرین ۲: خواندن یک اسکریپت ناآشنا، بی‌اجرا
> **راهنمایی:** بخش ۲ درس، چهار جای مهم. با `head -20` و `grep -n "library"` بخوانید.

اسکریپت `$P/03_Bioc_Examples/scripts/run_deseq2.R` را (که در ماژول ۰۳ اجرا می‌کنید) **اجرا نکنید**؛ تنها بخوانید و بگویید: (الف) چند ورودی می‌خواهد و هر کدام چیست؟ (ب) کدام بسته‌ها را لازم دارد؟ (ج) چه فایل‌هایی می‌سازد اگر پیشوند خروجی `test` باشد؟

---

## تمرین ۳: پزشک خطا
> **راهنمایی:** بخش ۴ درس. برای هر پیام، خط `Error`، خط `Calls:` و هشدار زیرش را جدا بخوانید.

علت هر کدام را بگویید و دستور درست را بنویسید.

**پیام الف** (پس از `Rscript $P/02_Run_Rscript/scripts/composition.R ground_truth.csv minigut x.png`):

<div dir="ltr">

```text
Error in file(file, "rt") : cannot open the connection
Calls: read.delim -> read.table -> file
In addition: Warning message:
In file(file, "rt") :
  cannot open file 'ground_truth.csv': No such file or directory
Execution halted
```

</div>

**پیام ب** (پس از `Rscript $P/02_Run_Rscript/scripts/composition.R ground_truth.tsv Minigut x.png`):

<div dir="ltr">

```text
No rows for sample: Minigut 
```

</div>

**پیام ج** (پس از `Rscript composition.R ground_truth.tsv minigut x.png`):

<div dir="ltr">

```text
Fatal error: cannot open file 'composition.R': No such file or directory
```

</div>

---

## تمرین ۴: خطا کجا می‌رود؟
> **راهنمایی:** بخش ۵ درس (`> out 2> err`)؛ اندازه‌ی فایل‌ها را با `wc -c` ببینید.

دستور پیام «الف» تمرین ۳ را با `> e.out 2> e.err` اجرا کنید. (الف) کد خروج چیست؟ (ب) کدام فایل خالی است و چرا؟ (ج) حالا پیام «ب» را هم با `> bad.out 2> bad.err` اجرا کنید: پیام `No rows for sample` در کدام فایل است؟ چه نتیجه‌ای درباره‌ی پیام‌هایی که نویسنده‌ی اسکریپت با `cat` نوشته می‌گیرید؟

---

## تمرین ۵: نمودار پهن‌تر
> **راهنمایی:** بخش ۶ درس (کپی + `sed -i`). اندازه‌ی PNG را با دستور `file` ببینید.

در یک کپی از `composition.R`، پهنای نمودار را از ۷ به ۱۰ اینچ برسانید و برای `minigut_sample2` اجرا کنید. اندازه‌ی PNG (به پیکسل) پیش و پس از تغییر چیست؟ چرا این دو عدد؟ (در خط `ggsave`، `dpi = 120` یعنی ۱۲۰ نقطه در هر اینچ.)

---

## تمرین ۶: پایتون و R، یک پاسخ؟
> **راهنمایی:** بخش ۳ درس؛ اسکریپت `composition.py` در `03_Python/99_scripts_data/06_Pandas/scripts/` و دستور `diff` (بخش ۰۱).

هر دو اسکریپت را برای `minigut_sample2` اجرا کنید و دو جدول خروجی (`minigut_sample2_genus.tsv` از پایتون و `minigut_sample2_genus_R.tsv` از R) را با `diff` بسنجید. چه تفاوتی هست؟ آیا این تفاوت در **عدد** است یا در **نوشتن** عدد؟

---

## تمرین ۷ (فکری): جمله‌ی روش‌ها
> **راهنمایی:** بخش ۵ درس، `sessionInfo()`.

با یک دستور، نسخه‌های R و ggplot2 را در فایل `versions.txt` بنویسید و از روی آن، یک جمله برای بخش روش‌های پایان‌نامه بنویسید. چرا ثبت نسخه مهم است؟ (ماژول ۰۱: نسخه‌ی DESeq2 در conda و Bioconductor فرق داشت.)

</div>
