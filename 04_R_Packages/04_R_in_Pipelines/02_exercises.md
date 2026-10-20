<div dir="rtl">

# تمرین‌ها: اسکریپت‌های R در خط لوله

پیش از آغاز:

<div dir="ltr">

```bash
conda activate r_packages
cd ~/r_practice/pipeline
P=~/Bioinformatics_Learning-main/04_R_Packages/99_scripts_data
R02=$P/02_Run_Rscript/scripts
```

</div>

---

## تمرین ۱: سه چراغ
> **راهنمایی:** درس، بخش ۲ (جدول کدهای خروج). `> /dev/null 2>&1` همه‌ی پیام‌ها را دور می‌ریزد تا تنها کد خروج را ببینید.

پیش از اجرا پیش‌بینی کنید هر دستور چه کد خروجی می‌دهد؛ سپس پس از هر کدام `echo $?` بزنید و بسنجید.

<div dir="ltr">

```bash
Rscript $R02/composition.R ground_truth.tsv minigut a.png > /dev/null 2>&1
Rscript $R02/composition.R ground_truth.tsv Minigut a.png > /dev/null 2>&1
Rscript composition.R ground_truth.tsv minigut a.png > /dev/null 2>&1
```

</div>

---

## تمرین ۲: حلقه‌ی خودتان
> **راهنمایی:** درس، بخش ۳. نام نمونه‌ها را با `cut | tail -n +2 | sort -u` بگیرید و درون `$( )` به `for` بدهید (بخش ۰۱، ماژول ۰۹).

حلقه‌ای بنویسید که `composition.R` را برای **همه‌ی** نمونه‌های `ground_truth.tsv` اجرا کند، گزارش هر نمونه را در `logs/<نمونه>.log` بنویسد و کد خروج هر اجرا را چاپ کند. چند فایل گزارش ساخته شد؟

---

## تمرین ۳: نمونه‌ی سوم
> **راهنمایی:** دستور awk تمرین ۶ ماژول ۰۳ نمونه‌ی `minigut_copy` می‌سازد. درس، بخش ۴ (`run_all.sh`).

<div dir="ltr">

```bash
awk -F'\t' 'BEGIN{OFS="\t"} {print} NR>1 && $1=="minigut" {$1="minigut_copy"; print}' \
    ground_truth.tsv > three.tsv
```

</div>

‏`run_all.sh` را روی `three.tsv` با پوشه‌ی خروجی `results3` اجرا کنید. (الف) چند نمودار PNG ساخته شد و چرا این شمار؟ (ب) آیا لازم شد چیزی در `run_all.sh` عوض کنید؟ (ج) جدول `diversity_bray.tsv` را بخوانید.

---

## تمرین ۴: کارآگاه گزارش‌ها
> **راهنمایی:** درس، بخش ۵: `grep -l "Error"` و سپس `cat`.

جدول خراب `broken.tsv` (بخش ۵ درس) را دوباره بسازید و `run_all.sh` را با پوشه‌ی `results_broken` اجرا کنید. (الف) کد خروج؟ (ب) کدام گزارش خطا دارد؟ (ج) علت را به زبان ساده بنویسید و بگویید جدول را چگونه درست می‌کنید.

---

## تمرین ۵: بی `set -e`
> **راهنمایی:** درس، کادر ✋ بخش ۵. با `sed` یک کپی بی `set -e` بسازید. چون کپی در پوشه‌ی دیگری است، خط `here=` را هم باید به پوشه‌ی اصلی اسکریپت برگردانید.

<div dir="ltr">

```bash
S=$P/04_R_in_Pipelines/scripts
sed -e 's/^set -euo pipefail/# no set -e/' -e "s|^here=.*|here=$S|" $S/run_all.sh > nosete.sh
```

</div>

‏`nosete.sh` را روی `broken.tsv` با پوشه‌ی `results_nose` اجرا کنید. روی صفحه چه می‌بینید و کد خروج چیست؟ چرا این خطرناک است؟

---

## تمرین ۶ (فکری): بی `realpath`
> **راهنمایی:** درس، بخش ۴ (③) و اشتباه رایج ۲. پس از اجرا، `ls` پوشه‌ی خروجی و `cat` گزارش‌ها.

یک کپی بسازید که به‌جای `table=$(realpath "$1")` بنویسد `table=$1`:

<div dir="ltr">

```bash
sed -e 's/^table=$(realpath "$1")/table=$1/' -e "s|^here=.*|here=$S|" $S/run_all.sh > norealpath.sh
bash norealpath.sh ground_truth.tsv results_rel
echo "exit=$?"
```

</div>

(الف) روی صفحه چه آمد؟ (ب) چرا هیچ خط `composition: …` چاپ نشد؟ (ج) چرا `set -e` همان جا اسکریپت را نایستاند و تنها در گام `diversity` ایستاد؟

</div>
