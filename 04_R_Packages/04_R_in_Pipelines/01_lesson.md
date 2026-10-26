<div dir="rtl">

# درس: اسکریپت‌های R در یک خط لوله‌ی Bash

**بخش:** `04_R_Packages` · **ماژول:** `04_R_in_Pipelines` · **پیش‌نیاز:** ماژول [سه نمونه‌ی واقعی](../03_Bioc_Examples/)؛ ماژول‌های [حلقه](../../01_Linux/09_Variables_Loops/) و [اسکریپت‌نویسی](../../01_Linux/10_Scripts/) بخش ۰۱ · **زمان:** حدود ۴۵ دقیقه · **ابزار:** bash 5، R 4.6.1، ggplot2 4.0.3، vegan 2.7.6 · **آخرین اجرا:** 2026-10-20

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. با **کد خروج** `Rscript` بفهمید یک اجرا موفق بود یا نه.
2. یک اسکریپت R را در **حلقه‌ی Bash** برای چند نمونه اجرا کنید.
3. با `set -euo pipefail` کاری کنید که خط لوله با نخستین شکست **بایستد**، نه اینکه بی‌صدا ادامه دهد.
4. برای هر اجرا **فایل گزارش** (log) نگه دارید و خطا را در گزارش‌ها پیدا کنید.
5. نسخه‌ها را خودکار در کنار نتیجه‌ها ثبت کنید.

**پیش از آغاز:**

<div dir="ltr">

```bash
conda activate r_packages
mkdir -p ~/r_practice/pipeline && cd ~/r_practice/pipeline
cp ~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data/ground_truth.tsv .
P=~/Bioinformatics_Learning-main/04_R_Packages/99_scripts_data
R02=$P/02_Run_Rscript/scripts
```

</div>

---

## ۱. داستان: از دو نمونه به دویست نمونه

در ماژول ۰۲ اسکریپت `composition.R` را برای هر نمونه **با دست** اجرا کردید. برای دو نمونه خوب است؛ برای ۲۰۰ نمونه نه. و در پروژه‌ی واقعی چند اسکریپت **پشت سر هم** اجرا می‌شوند: نخست ترکیب هر نمونه، سپس تنوع همه‌ی نمونه‌ها با هم.

در بخش ۰۱ یاد گرفتید دستورها را در **حلقه** و **اسکریپت Bash** بگذارید. ‏`Rscript` یک دستور ترمینال است مانند `grep` یا `fastp`، پس همان ابزارها برایش کار می‌کنند. تنها یک چیز تازه لازم است: اینکه **بفهمید کدام اجرا شکست خورد**.

---

## ۲. مفهوم به زبان ساده: کد خروج، چراغ سبز و قرمز

هر برنامه هنگام پایان یک عدد پنهان برمی‌گرداند، **کد خروج** (`$?`، بخش ۰۱):

| کد | ‏Rscript چه وقت می‌دهد |
| :---: | :--- |
| ‏`0` | اجرا تا پایان رفت (حتی اگر `Warning` داشت) |
| ‏`1` | خطای R (`Execution halted`) یا `quit(status = 1)` در خود اسکریپت |
| ‏`2` | ‏Rscript فایل اسکریپت را نیافت (`Fatal error: cannot open file`) |

خط لوله‌ی خوب پس از هر گام به این چراغ نگاه می‌کند: سبز (۰) ← گام بعد؛ قرمز (غیر ۰) ← بایست.

---

## ۳. حلقه، و خطری که پنهان می‌ماند

نام نمونه‌ها را از خود جدول بگیرید:

<div dir="ltr">

```bash
cut -f1 ground_truth.tsv | tail -n +2 | sort -u
```

</div>

<div dir="ltr">

```text
minigut
minigut_sample2
```

</div>

‏`tail -n +2` یعنی «از سطر **۲** تا پایان»: سرستون (`sample`) کنار می‌رود. ‏`sort -u` نام‌های تکراری را یکی می‌کند (ماژول ۰۶ بخش ۰۱).

حالا حلقه، با یک نام نادرست (`minigut3`) که عمداً افزوده‌ایم:

<div dir="ltr">

```bash
for s in minigut minigut_sample2 minigut3; do
    Rscript $R02/composition.R ground_truth.tsv $s $s.png > $s.log 2>&1
    echo "$s: exit $?"
done
```

</div>

<div dir="ltr">

```text
minigut: exit 0
minigut_sample2: exit 0
minigut3: exit 1
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `$s` | نام نمونه در هر دور حلقه |
| `$s.png` | نام خروجی از نام نمونه: `minigut.png`، … |
| `> $s.log 2>&1` | هر دو جریان (stdout و stderr) در یک فایل گزارش برای هر نمونه (بخش ۰۱، ماژول لوله‌ها) |
| `echo "$s: exit $?"` | کد خروج همان `Rscript` را چاپ کن |

حلقه **تا پایان رفت**، با آنکه `minigut3` شکست خورد. اینجا خودمان کد خروج را چاپ کردیم و شکست را دیدیم؛ ولی اگر آن `echo` نبود، روی صفحه **هیچ نشانه‌ای** نمی‌دیدید (پیام خطا در `minigut3.log` پنهان است). در ۲۰۰ نمونه، سه شکست بی‌صدا یعنی سه نمونه که در جدول نهایی **نیستند** و شاید هرگز نفهمید.

<details>
<summary>✋ امتحان کن: چرا در این حلقه شکست <code>minigut3</code> را روی صفحه نمی‌بینید (بی آن <code>echo</code>)؟</summary>

چون `> $s.log 2>&1` همه‌ی پیام‌ها، از جمله `No rows for sample: minigut3`، را به فایل گزارش فرستاد. Bash هم به‌طور پیش‌فرض پس از دستور شکست‌خورده دستور بعدی را اجرا می‌کند. با `cat minigut3.log` پیام را می‌بینید.

</details>

---

## ۴. اسکریپت خط لوله: `run_all.sh`

اسکریپت آماده‌ی این ماژول، دو اسکریپت R ماژول‌های ۰۲ و ۰۳ را پشت سر هم اجرا می‌کند:

<div dir="ltr">

```bash
cat $P/04_R_in_Pipelines/scripts/run_all.sh
```

</div>

<div dir="ltr">

```bash
#!/usr/bin/env bash
# run_all.sh: run the R scripts of part 04 one after another, like a small pipeline.
# For every sample in ground_truth.tsv: composition table + bar chart (composition.R).
# Then: diversity of all samples (diversity.R). Every R run writes a log file.
# Usage: bash run_all.sh <ground_truth.tsv> <output_folder>
set -euo pipefail                                                         # ①

if [ $# -ne 2 ]; then                                                     # ②
    echo "Usage: bash run_all.sh <ground_truth.tsv> <output_folder>" >&2
    exit 1
fi
table=$(realpath "$1")                                                    # ③
out=$2

# folder of this script -> the R scripts of modules 02 and 03 sit next to it
here=$(dirname "$(realpath "$0")")                                        # ④
R02=$here/../../02_Run_Rscript/scripts
R03=$here/../../03_Bioc_Examples/scripts

mkdir -p "$out/logs"
cd "$out"

# 1. record the R and package versions used for this run
Rscript "$here/../../01_Install_Packages/scripts/check_packages.R" ggplot2 vegan > versions.txt   # ⑤

# 2. one composition chart per sample
for sample in $(cut -f1 "$table" | tail -n +2 | sort -u); do              # ⑥
    echo "composition: $sample"
    Rscript --vanilla "$R02/composition.R" "$table" "$sample" "${sample}_composition.png" \
        > "logs/${sample}_composition.log" 2>&1
done

# 3. diversity of all samples together (genus level)
echo "diversity: all samples"
Rscript --vanilla "$R03/diversity.R" "$table" diversity genus > logs/diversity.log 2>&1

echo "done; outputs in $out"
```

</div>

| نشانه | چه می‌کند | چرا |
| :---: | :--- | :--- |
| ① | ‏`set -euo pipefail` (بخش ۰۱، ماژول ۱۰) | ‏`-e`: با **نخستین** دستوری که کد خروج غیرصفر بدهد، کل اسکریپت می‌ایستد. همان چراغ قرمز بخش ۲ |
| ② | شمردن ورودی‌ها | همان الگوی خط Usage در اسکریپت‌های R |
| ③ | ‏`realpath`: نشانی **کامل** فایل (از `/` آغاز) | اسکریپت پایین‌تر با `cd` به پوشه‌ی خروجی می‌رود؛ نشانی نسبی `ground_truth.tsv` آن‌جا دیگر پیدا نمی‌شود |
| ④ | ‏`dirname`: پوشه‌ی یک نشانی (وارونه‌ی `basename`)؛ `$0` = نشانی خود اسکریپت | اسکریپت‌های R را **نسبت به جای خودش** پیدا می‌کند، از هر پوشه‌ای که اجرا شود |
| ⑤ | ثبت نسخه‌ها در `versions.txt` | هر پوشه‌ی نتیجه، نسخه‌های سازنده‌اش را کنار خود دارد (ماژول ۰۲، بخش ۵) |
| ⑥ | حلقه روی نام نمونه‌ها، از خود جدول | نمونه‌ی تازه که به جدول افزوده شود، خودکار اجرا می‌شود |

### اجرا

<div dir="ltr">

```bash
bash $P/04_R_in_Pipelines/scripts/run_all.sh ground_truth.tsv results
echo "exit=$?"
```

</div>

<div dir="ltr">

```text
composition: minigut
composition: minigut_sample2
diversity: all samples
done; outputs in results
exit=0
```

</div>

<div dir="ltr">

```bash
ls results results/logs
cat results/versions.txt
```

</div>

<div dir="ltr">

```text
results:
diversity_alpha.tsv
diversity_bray.tsv
diversity_rarecurve.png
logs
minigut_composition.png
minigut_genus_R.tsv
minigut_sample2_composition.png
minigut_sample2_genus_R.tsv
versions.txt

results/logs:
diversity.log
minigut_composition.log
minigut_sample2_composition.log
R: R version 4.6.1 (2026-06-24) 
ggplot2      4.0.3
vegan        2.7.6
```

</div>

روی صفحه تنها پیشرفت کار آمد (`composition: …`)؛ همه‌ی جزئیات در `logs/` است. نتیجه‌ها، گزارش‌ها و نسخه‌ها همه در **یک پوشه**. این پوشه را می‌توان برای استاد فرستاد و او همه چیز را می‌داند.

<details>
<summary>✋ امتحان کن: در کدام گزارش هشدار <code>rarecurve</code> را پیدا می‌کنید؟</summary>

در `results/logs/diversity.log` (همان هشدار درس vegan). برای یافتنش: `grep -l "Warning" results/logs/*.log`. چون هشدار است، کد خروج ۰ بود و خط لوله ادامه یافت.

</details>

> 📺 **فیلم:** *Tutorial: Create a command line R script with Argparse*: https://www.youtube.com/watch?v=VpXb2PuBKkU (OGGY INFORMATICS)
> 📄 **مرجع:** GNU Bash manual, *The Set Builtin*: https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html

---

## ۵. وقتی یک گام شکست می‌خورد

یک جدول خراب بسازید: نام ستون `read_pairs` را به `reads` عوض کنید (کاری که بسیار پیش می‌آید وقتی جدول از ابزار دیگری می‌آید):

<div dir="ltr">

```bash
sed '1s/read_pairs/reads/' ground_truth.tsv > broken.tsv
head -1 broken.tsv
bash $P/04_R_in_Pipelines/scripts/run_all.sh broken.tsv results_broken
echo "exit=$?"
```

</div>

<div dir="ltr">

```text
sample	reads	accession	organism
composition: minigut
exit=1
```

</div>

خط لوله پس از **نخستین** نمونه ایستاد: نه `minigut_sample2`، نه `diversity`، نه `done`. این همان `set -e` است. حالا علت را در گزارش‌ها پیدا کنید:

<div dir="ltr">

```bash
ls results_broken/logs
grep -l "Error" results_broken/logs/*.log
cat results_broken/logs/minigut_composition.log
```

</div>

<div dir="ltr">

```text
minigut_composition.log
results_broken/logs/minigut_composition.log
Error in `$<-.data.frame`(`*tmp*`, percent, value = numeric(0)) : 
  replacement has 0 rows, data has 2
Calls: $<- -> $<-.data.frame
Execution halted
```

</div>

پیام R گنگ است: «جایگزینی ۰ سطر دارد، داده ۲ سطر». ترجمه‌اش: اسکریپت خواست ستون `percent` را از ستون `read_pairs` بسازد، ولی ستونی به آن نام **نبود** (پس «۰ مقدار»). ‏`grep -l` (تنها نام فایل‌هایی که الگو را دارند) گزارش مشکل‌دار را در میان ده‌ها گزارش پیدا می‌کند. **قاعده: وقتی خط لوله ایستاد، نخست `grep -l Error logs/*.log`، سپس `cat` همان یک فایل.**

<details>
<summary>✋ امتحان کن: اگر <code>set -euo pipefail</code> نبود، چه می‌شد؟</summary>

هر دو `composition` و `diversity` اجرا می‌شدند، همه شکست می‌خوردند (همه ستون `read_pairs` را می‌خواهند)، و اسکریپت در پایان `done; outputs in results_broken` چاپ می‌کرد با کد خروج **۰**. پوشه‌ی خروجی تنها `versions.txt` و گزارش‌های خطا را داشت، ولی پیام روی صفحه می‌گفت «تمام شد». این خطرناک‌ترین حالت است.

</details>

---

## ۶. سه اشتباه رایج

**۱. حلقه بی `set -e` یا بی وارسی کد خروج.** شکست‌ها بی‌صدا می‌گذرند (بخش ۳). هر اسکریپت خط لوله با `set -euo pipefail` آغاز شود.

**۲. نشانی نسبی پس از `cd`.** اگر اسکریپت `cd results` کند، `ground_truth.tsv` نسبی دیگر پیدا نمی‌شود و `cannot open file 'ground_truth.tsv'` می‌گیرید. راه: `realpath` پیش از `cd` (بخش ۴، ③).

**۳. گزارش‌ها را دور ریختن.** با `> /dev/null 2>&1` خروجی تمیز می‌شود ولی هنگام شکست هیچ سرنخی نمی‌ماند. هر اجرای R یک فایل `.log` بگیرد.

---

## 📘 برای کنجکاوها

- ‏**‏Snakemake (بخش ۰۵):** کار `run_all.sh` را بهتر می‌کند: تنها گام‌هایی را دوباره اجرا می‌کند که ورودی‌شان عوض شده، و چند نمونه را هم‌زمان اجرا می‌کند. اسکریپت‌های R در Snakemake به همین شکل (`shell: "Rscript … {input} {output}"`) یا با دستور ویژه‌ی `script:` اجرا می‌شوند.
- **اجرای طولانی:** DESeq2 روی ده‌ها نمونه یا vegan با هزاران جایگشت شاید ساعت‌ها طول بکشد. با `nohup bash run_all.sh … &` یا درون `tmux` (بخش ۰۱، ماژول ۱۰) اجرا کنید تا بستن ترمینال کار را نکشد.
- ‏**‏`Rscript --vanilla`** در `run_all.sh` به کار رفته تا تنظیم شخصی (`~/.Rprofile`) نتیجه را عوض نکند (ماژول ۰۲).

---

## جمع‌بندی

- ‏`Rscript` کد خروج می‌دهد: ۰ = موفق (حتی با Warning)، ۱ = خطای R، ۲ = اسکریپت پیدا نشد.
- حلقه‌ی Bash بی `set -e` پس از شکست ادامه می‌دهد؛ با `set -euo pipefail` با نخستین شکست می‌ایستد.
- هر اجرا: `> logs/نام.log 2>&1`. پس از شکست: `grep -l Error logs/*.log`.
- پیش از `cd`، نشانی‌ها را با `realpath` کامل کنید؛ اسکریپت‌های کمکی را با `dirname "$(realpath "$0")"` پیدا کنید.
- نسخه‌ها را خودکار در پوشه‌ی نتیجه بنویسید.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
Rscript script.R in out > run.log 2>&1; echo "exit $?"      # 0 ok, 1 R error, 2 script not found
cut -f1 table.tsv | tail -n +2 | sort -u                      # sample names without the header
for s in $(cut -f1 table.tsv | tail -n +2 | sort -u); do
    Rscript script.R table.tsv "$s" "$s.png" > "logs/$s.log" 2>&1
done
set -euo pipefail                                             # first failure stops the script
grep -l "Error" logs/*.log                                    # which run failed?
realpath file.tsv ; dirname /a/b/c.sh                         # full path ; folder of a path
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| خط لوله (*pipeline*) | چند گام تحلیل که پشت سر هم و خودکار اجرا می‌شوند |
| کد خروج (*exit status*) | عددی که برنامه هنگام پایان برمی‌گرداند؛ ۰ = موفق |
| فایل گزارش (*log*) | فایلی که پیام‌های یک اجرا در آن ذخیره می‌شود |
| ‏`set -e` | ایستادن اسکریپت Bash با نخستین شکست |
| ‏`realpath` | نشانی کامل یک فایل |
| ‏`dirname` | پوشه‌ی یک نشانی |
| ‏`tail -n +2` | از سطر ۲ تا پایان |
| ‏`grep -l` | تنها نام فایل‌هایی که الگو را دارند |

---

## منابع

**مستند رسمی**
- GNU Bash manual, *The Set Builtin* (`-e`، `-u`، `-o pipefail`): https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html
- ‏R Core Team, *An Introduction to R*، پیوست B «Invoking R from the command line»: https://cran.r-project.org/doc/manuals/r-release/R-intro.html#Invoking-R-from-the-command-line
- ‏Snakemake documentation, *External scripts* (اجرای R در Snakemake؛ برای بخش ۰۵): https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#external-scripts

**کتاب**
- ‏Buffalo V (2015). *Bioinformatics Data Skills*. O'Reilly. (فصل ۱۲: اسکریپت‌نویسی پوسته و خط لوله)

**فیلم و دوره‌ی آموزشی**
- Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins University): https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Linux* (The Linux Foundation). دوره‌ای ویژه‌ی خط لوله‌ی R در edX نیافتیم؛ نزدیک‌ترین برای اسکریپت‌نویسی Bash: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux
- YouTube: *run r script from linux command line with arguments input and output data file names as arguments* (Yi Li): https://www.youtube.com/watch?v=mheCAcfa1tg
- YouTube: *Tutorial - Create a command line R script with Argparse* (OGGY INFORMATICS): https://www.youtube.com/watch?v=VpXb2PuBKkU

<sub>نشانی‌های YouTube در 2026-10-20 با oEmbed وارسی شدند. نشانی‌های Coursera و edX پیش‌تر در دوره به کار رفته‌اند یا از نمایه‌ی جست‌وجو در همان تاریخ گرفته شدند؛ وارسی مستقیم آن‌ها در پایان دوره انجام می‌شود.</sub>

</div>
