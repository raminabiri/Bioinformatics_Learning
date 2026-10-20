<div dir="rtl">

# پاسخ تشریحی: اسکریپت‌های R در خط لوله

خروجی‌ها از اجرای واقعی در 2026-10-20 (bash 5، R 4.6.1) گرفته شده‌اند.

---

## پاسخ ۱: سه چراغ

<div dir="ltr">

```bash
Rscript $R02/composition.R ground_truth.tsv minigut a.png > /dev/null 2>&1; echo $?
Rscript $R02/composition.R ground_truth.tsv Minigut a.png > /dev/null 2>&1; echo $?
Rscript composition.R ground_truth.tsv minigut a.png > /dev/null 2>&1; echo $?
```

</div>

<div dir="ltr">

```text
0
1
2
```

</div>

- **۰**: همه چیز درست.
- **۱**: نمونه‌ی `Minigut` (با M بزرگ) نیست؛ اسکریپت خودش با `quit(status = 1)` بیرون رفت.
- **۲**: فایل `composition.R` در پوشه‌ی کنونی نیست؛ Rscript پیش از اجرای R ایستاد.

با `/dev/null` پیام‌ها دیده نمی‌شوند ولی **کد خروج** همچنان علت را دسته‌بندی می‌کند. (تنها برای این تمرین؛ در خط لوله گزارش‌ها را نگه دارید، اشتباه رایج ۳.)

---

## پاسخ ۲: حلقه‌ی خودتان

<div dir="ltr">

```bash
mkdir -p logs
for s in $(cut -f1 ground_truth.tsv | tail -n +2 | sort -u); do
    Rscript $R02/composition.R ground_truth.tsv "$s" "$s.png" > "logs/$s.log" 2>&1
    echo "$s: exit $?"
done
ls logs
```

</div>

<div dir="ltr">

```text
minigut: exit 0
minigut_sample2: exit 0
minigut.log
minigut_sample2.log
```

</div>

**دو** فایل گزارش، یکی برای هر نمونه. **اشتباه رایج:** فراموش کردن `mkdir -p logs`؛ آن‌گاه Bash پیش از اجرای Rscript خطا می‌دهد (`bash: logs/minigut.log: No such file or directory`) و Rscript اصلاً اجرا نمی‌شود؛ کد خروج ۱ از خود Bash است (`minigut: exit 1`).

---

## پاسخ ۳: نمونه‌ی سوم

<div dir="ltr">

```bash
bash $P/04_R_in_Pipelines/scripts/run_all.sh three.tsv results3
ls results3/*.png | wc -l
ls results3/logs
cat results3/diversity_bray.tsv
```

</div>

<div dir="ltr">

```text
composition: minigut
composition: minigut_copy
composition: minigut_sample2
diversity: all samples
done; outputs in results3
4
diversity.log
minigut_composition.log
minigut_copy_composition.log
minigut_sample2_composition.log
minigut	minigut_copy	minigut_sample2
minigut	0	0	0.969
minigut_copy	0	0	0.969
minigut_sample2	0.969	0.969	0
```

</div>

- (الف) **۴** PNG: سه نمودار ترکیب (یکی برای هر نمونه) + یک منحنی نادرسازی (`diversity_rarecurve.png`).
- (ب) **هیچ.** حلقه نام نمونه‌ها را از خود جدول می‌خواند (⑥ در درس)، پس نمونه‌ی تازه خودکار اجرا شد. همین برای ۲۰۰ نمونه هم کار می‌کند.
- (ج) ماتریس ۳×۳ متقارن: `minigut` و `minigut_copy` فاصله‌ی **۰** (یکسان)؛ هر دو با `minigut_sample2` همان **۰٫۹۶۹** درس vegan؛ قطر صفر.

---

## پاسخ ۴: کارآگاه گزارش‌ها

<div dir="ltr">

```bash
sed '1s/read_pairs/reads/' ground_truth.tsv > broken.tsv
bash $P/04_R_in_Pipelines/scripts/run_all.sh broken.tsv results_broken
echo "exit=$?"
grep -l "Error" results_broken/logs/*.log
cat results_broken/logs/minigut_composition.log
```

</div>

<div dir="ltr">

```text
composition: minigut
exit=1
results_broken/logs/minigut_composition.log
Error in `$<-.data.frame`(`*tmp*`, percent, value = numeric(0)) : 
  replacement has 0 rows, data has 2
Calls: $<- -> $<-.data.frame
Execution halted
```

</div>

- (الف) **۱**.
- (ب) `minigut_composition.log`، تنها گزارشی که ساخته شد، چون خط لوله پس از نخستین گام ایستاد.
- (ج) اسکریپت ستونی به نام `read_pairs` می‌خواهد، ولی سرستون جدول `reads` است؛ پس ستون `percent` از «هیچ» (۰ مقدار) ساخته می‌شد و R آن را در ۲ سطر جای نداد. درست کردن: نام ستون را برگردانید (`sed '1s/reads/read_pairs/'`) یا جدول درست را بدهید. **درس:** پیام R درباره‌ی «0 rows» اغلب یعنی **نام ستون** با آنچه اسکریپت می‌خواهد جور نیست؛ سرآیند اسکریپت (`input: long table with columns sample, read_pairs, organism`) را با `head -1` جدولتان بسنجید.

---

## پاسخ ۵: بی `set -e`

<div dir="ltr">

```bash
bash nosete.sh broken.tsv results_nose
echo "exit=$?"
ls results_nose results_nose/logs
```

</div>

<div dir="ltr">

```text
composition: minigut
composition: minigut_sample2
diversity: all samples
done; outputs in results_nose
exit=0
results_nose:
logs
versions.txt

results_nose/logs:
diversity.log
minigut_composition.log
minigut_sample2_composition.log
```

</div>

روی صفحه همه چیز «درست» به نظر می‌رسد: هر سه گام، `done` و کد خروج **۰**. ولی پوشه‌ی نتیجه **هیچ** جدول یا نموداری ندارد و هر سه گزارش خطا دارند. خطرناک است چون اگر این اسکریپت گامی از یک کار بزرگ‌تر بود (یا شب اجرا شد)، کسی نمی‌فهمید که چیزی ساخته نشده، تا وقتی که گام بعدی با خطای گنگ‌تری بشکند.

---

## پاسخ ۶ (فکری): بی `realpath`

<div dir="ltr">

```bash
bash norealpath.sh ground_truth.tsv results_rel
echo "exit=$?"
ls results_rel/logs
cat results_rel/logs/diversity.log
```

</div>

<div dir="ltr">

```text
cut: ground_truth.tsv: No such file or directory
diversity: all samples
exit=1
diversity.log
Error in file(file, "rt") : cannot open the connection
Calls: read.delim -> read.table -> file
In addition: Warning message:
In file(file, "rt") :
  cannot open file 'ground_truth.tsv': No such file or directory
Execution halted
```

</div>

- (الف) خطای `cut`، سپس `diversity: all samples` و ایستادن با کد ۱.
- (ب) اسکریپت پیش از حلقه `cd results_rel` کرد. آن‌جا `ground_truth.tsv` نسبی وجود ندارد، پس `cut` چیزی بیرون نداد و فهرست نمونه‌ها **تهی** شد: حلقه صفر بار اجرا شد.
- (ج) `set -e` شکستِ دستوری را که **درون `$( )` در فهرست `for`** اجرا می‌شود نمی‌بیند: Bash تنها خروجی (تهی) را برمی‌دارد و حلقه را بی هیچ دوری می‌گذراند. گام `diversity` خودش یک دستور است و کد ۱ داد، پس `set -e` همان‌جا اسکریپت را ایستاند. **درس دوگانه:** (۱) پیش از `cd` نشانی‌ها را با `realpath` کامل کنید؛ (۲) `set -e` همه‌ی شکست‌ها را نمی‌گیرد. شمردن خروجی‌ها (برای نمونه «آیا شمار PNGها برابر شمار نمونه‌هاست؟») وارسی دوم خوبی است.

</div>
