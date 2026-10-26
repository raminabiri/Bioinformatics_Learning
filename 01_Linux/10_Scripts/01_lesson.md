<div dir="rtl">

# درس: نوشتن اسکریپت؛ دستورها را یک بار بنویسید، هر بار اجرا کنید

**بخش:** `01_Linux` · **ماژول:** `10_Scripts` · **پیش‌نیاز:** ماژول [متغیر و حلقه](../09_Variables_Loops/) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** bash 5، nano · **آخرین اجرا:** 2026-10-20

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. دستورها را در یک فایل **اسکریپت** بنویسید (با `nano`) و آن را اجرا کنید.
2. به اسکریپت **ورودی** بدهید (`$1`، `"$@"`، `$#`) و ورودی‌ها را وارسی کنید (`if`).
3. با `set -euo pipefail` اسکریپت را در برابر **خطاهای بی‌صدا** ایمن کنید.
4. پیام‌های خطا را به stderr بفرستید (`>&2`) و با کد خروج درست بیرون بیایید (`exit 1`).
5. کار طولانی را طوری اجرا کنید که با بستن ترمینال قطع نشود (`nohup`، `tmux`).

همه‌ی دستورها را در پوشه‌ی `~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data` اجرا کنید.

---

## ۱. داستان: دستور پخت دقیق

در بخش ۰۰ گفتیم که تحلیل باید مانند **دستور پخت دقیق** باشد: هر کس دنبالش کند، به همان نتیجه برسد. حلقه‌ی ماژول ۰۹ چند خط بود که هر بار باید دوباره تایپ می‌شد؛ و اگر شش ماه بعد بپرسند «جدول شمار ریدها را دقیقاً چطور ساختی؟»، پاسخی نمی‌ماند.

**اسکریپت** همان دستورهاست، نوشته‌شده در یک فایل. سه سود دارد:
- **دوباره‌پذیری:** همان دستورها، هر بار، دقیقاً همان‌گونه اجرا می‌شوند.
- **یادداشت:** خود فایل می‌گوید چه کرده‌اید.
- **اشتراک:** فایل را برای استاد یا همکار می‌فرستید و او همان کار را می‌کند.

همه‌ی فایل‌های `download.sh` این دوره اسکریپت‌اند. در ماژول ۰۳ یکی را اجرا کردید؛ حالا خودتان می‌نویسید.

---

## ۲. نخستین اسکریپت

### نوشتن با `nano`

‏`nano` یک ویرایشگر ساده‌ی درون ترمینال است:

<div dir="ltr">

```bash
nano hello.sh
```

</div>

این چند خط را بنویسید:

<div dir="ltr">

```bash
#!/usr/bin/env bash
# My first script: greet and show where we are
echo "Hello from a script!"
echo "Today is: $(date +%F)"
echo "I am in: $(pwd)"
```

</div>

سپس `Ctrl+O` و Enter (ذخیره)، و `Ctrl+X` (بیرون آمدن). (VS Code و هر ویرایشگر متن ساده‌ی دیگری هم خوب است؛ تنها Word یا برنامه‌های همانند را به کار نبرید، چون نویسه‌های پنهان به متن می‌افزایند.)

### اجرا

<div dir="ltr">

```bash
bash hello.sh
```

</div>

<div dir="ltr">

```text
Hello from a script!
Today is: 2026-10-20
I am in: ~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data
```

</div>

(تاریخ و نشانی روی کامپیوتر شما فرق دارند.)

### کالبدشکافی اسکریپت

| خط | چیست | یعنی |
| :-: | :--- | :--- |
| ۱ | `#!/usr/bin/env bash` | **شِبَنگ** (shebang): «این فایل را با Bash اجرا کن». همیشه خط یکم |
| ۲ | `# My first script…` | **یادداشت**: هر خطی که با `#` آغاز شود اجرا نمی‌شود. بنویسید اسکریپت چه می‌کند |
| ۳ | `echo "…"` | یک دستور عادی |
| ۴ | `$(date +%F)` | جایگزینی دستور (ماژول ۰۹)؛ `date +%F` تاریخ را به شکل `سال-ماه-روز` می‌دهد |
| ۵ | `$(pwd)` | نشانی پوشه‌ای که اسکریپت **از آن** اجرا شده است |

**پسوند `.sh`** برای لینوکس اجباری نیست، ولی به آدم‌ها می‌گوید این فایل اسکریپت Bash است.

<details>
<summary>📘 <b>برای کنجکاوها:</b> اجرای اسکریپت بی <code>bash</code> (<code>./hello.sh</code>)</summary>

<div dir="ltr">

```bash
./hello.sh
```

</div>

<div dir="ltr">

```text
bash: ./hello.sh: Permission denied
```

</div>

برای اجرای مستقیم، فایل باید دسترسی **اجرا** (`x`) داشته باشد (ماژول ۰۲، کادر کنجکاوها):

<div dir="ltr">

```bash
chmod +x hello.sh
./hello.sh
```

</div>

پس از `chmod +x`، `ls -l hello.sh` با `-rwxrwxr-x` آغاز می‌شود و `./hello.sh` کار می‌کند. `./` یعنی «در همین پوشه». در این دوره همیشه `bash script.sh` می‌نویسیم که `x` نمی‌خواهد.
</details>

> 📺 **فیلم:** *How To Write Bash Scripts In Linux, Part 2: Hello World*: https://www.youtube.com/watch?v=boqC9QenshY (LearnLinuxTV)
> 📄 **مرجع:** Software Carpentry, *The Unix Shell*, درس «Shell Scripts»: https://swcarpentry.github.io/shell-novice/

---

## ۳. ورودی دادن به اسکریپت

اسکریپتی که همیشه روی یک فایل ثابت کار کند، کم‌کاربرد است. بهتر است نام فایل را **هنگام اجرا** بدهیم. اسکریپت `count_one.sh`:

<div dir="ltr">

```bash
#!/usr/bin/env bash
# Count reads in one FASTQ file given as the first argument
f=$1
n=$(zcat "$f" | wc -l)
echo "$f has $((n/4)) reads"
```

</div>

<div dir="ltr">

```bash
bash count_one.sh fastq/minigut_R1.fastq.gz
bash count_one.sh fastq/minigut_sample2_R1.fastq.gz
```

</div>

<div dir="ltr">

```text
fastq/minigut_R1.fastq.gz has 50000 reads
fastq/minigut_sample2_R1.fastq.gz has 24993 reads
```

</div>

### متغیرهای ویژه‌ی ورودی

| نام | یعنی | در `bash script.sh a.gz b.gz` |
| :--- | :--- | :--- |
| `$1` | ورودی **یکم** | `a.gz` |
| `$2` | ورودی دوم | `b.gz` |
| `$#` | **شمار** ورودی‌ها | `2` |
| `"$@"` | **همه‌ی** ورودی‌ها، هر کدام جدا (برای حلقه) | ‏`a.gz` و `b.gz` |

### اگر ورودی ندهید؟

<div dir="ltr">

```bash
bash count_one.sh
```

</div>

<div dir="ltr">

```text
gzip: .gz: No such file or directory
 has 0 reads
```

</div>

`$1` خالی بود، پس `f` خالی ماند. `zcat` پیام گیج‌کننده‌ای داد، و اسکریپت با خونسردی گزارش داد «۰ رید». **هیچ نشانه‌ی روشنی نیست که اشتباه از کجاست.** بخش‌های ۴ و ۵ این را درست می‌کنند.

---

## ۴. وارسی ورودی: `if`

اسکریپت آماده‌ی این ماژول، [count_reads.sh](../99_scripts_data/scripts/count_reads.sh)، ورودی‌ها را وارسی می‌کند:

<div dir="ltr">

```bash
#!/usr/bin/env bash
# Count reads and mean read length in one or more FASTQ(.gz) files.
# Usage: bash count_reads.sh file1.fastq.gz [file2.fastq.gz ...]
set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: bash count_reads.sh file1.fastq.gz [file2 ...]" >&2
  exit 1
fi

printf "sample\treads\tmean_length\n"
for f in "$@"; do
  if [ ! -s "$f" ]; then
    echo "Error: file '$f' not found or empty" >&2
    exit 1
  fi
  name=$(basename "$f" .fastq.gz)
  zcat "$f" | awk -v s="$name" 'NR%4==2 {n++; L+=length($0)} END{printf "%s\t%d\t%.1f\n", s, n, L/n}'
done
```

</div>

### کالبدشکافی بخش‌های تازه

**ساختار `if`:**

<div dir="ltr">

```text
if [ شرط ]; then
  کار اگر شرط درست است
fi
```

</div>

‏(`fi` همان `if` وارونه است: «پایان if». فاصله‌ی پس از `[` و پیش از `]` **لازم** است.)

| تکه | یعنی |
| :--- | :--- |
| `[ $# -eq 0 ]` | آیا شمار ورودی‌ها **برابر** (`-eq` = *equal*) صفر است؟ |
| `[ ! -s "$f" ]` | آیا فایل **نیست یا خالی است**؟ (`-s` = «هست و خالی نیست»؛ `!` = «نه») |
| `>&2` | این پیام را به **stderr** بفرست (ماژول ۰۴)، نه به خروجی اصلی |
| `exit 1` | اسکریپت را **اکنون** بایستان، با کد خروج ۱ («شکست») |
| `for f in "$@"` | حلقه روی **همه‌ی** ورودی‌ها |

**کد خروج:** هر دستور پس از پایان یک عدد برمی‌گرداند: **۰ یعنی موفق**، هر عدد دیگر یعنی **شکست**. بی‌درنگ پس از هر دستور، `echo $?` آن را نشان می‌دهد. این عدد برای وقتی است که اسکریپت شما درون یک زنجیره‌ی بزرگ‌تر اجرا شود (بخش ۰۵ دوره): زنجیره از کد خروج می‌فهمد گامی شکست خورده و ادامه نمی‌دهد.

**چرا `>&2`؟** اگر کسی خروجی را در فایل بریزد (`bash count_reads.sh … > table.tsv`)، پیام خطا در جدول نمی‌رود و در ترمینال دیده می‌شود.

### اجرا

<div dir="ltr">

```bash
bash ../scripts/count_reads.sh fastq/*_R1.fastq.gz
```

</div>

<div dir="ltr">

```text
sample	reads	mean_length
minigut_R1	50000	126.0
minigut_sample2_R1	24993	151.0
```

</div>

و دو اجرای نادرست:

<div dir="ltr">

```bash
bash ../scripts/count_reads.sh;                 echo "exit=$?"
bash ../scripts/count_reads.sh nofile.fastq.gz; echo "exit=$?"
```

</div>

<div dir="ltr">

```text
Usage: bash count_reads.sh file1.fastq.gz [file2 ...]
exit=1
sample	reads	mean_length
Error: file 'nofile.fastq.gz' not found or empty
exit=1
```

</div>

**این خروجی یعنی:** هر بار پیامی روشن، که **می‌گوید چه چیزی نادرست است**، و کد خروج ۱. با `count_one.sh` بخش ۳ بسنجید.

---

## ۵. سپر ایمنی: `set -euo pipefail`

خط چهارم `count_reads.sh` را در هر اسکریپت تحلیلی بنویسید. سه بخش دارد؛ هر کدام را با یک اسکریپت کوچک می‌بینیم.

### ‏`-e`: با نخستین خطا بایست

اسکریپت `no_safety.sh`:

<div dir="ltr">

```bash
#!/usr/bin/env bash
cd results_folder_that_does_not_exist
echo "Now deleting old files in: $(pwd)"
```

</div>

<div dir="ltr">

```text
no_safety.sh: line 2: cd: results_folder_that_does_not_exist: No such file or directory
Now deleting old files in: ~/…/data
```

</div>

‏`cd` شکست خورد، ولی اسکریپت **ادامه داد**، در پوشه‌ی **نادرست**! اگر خط سوم به جای `echo` یک `rm` بود، فایل‌های پوشه‌ی داده پاک می‌شدند. همان اسکریپت با `set -euo pipefail` در خط دوم (`with_safety.sh`):

<div dir="ltr">

```text
with_safety.sh: line 3: cd: results_folder_that_does_not_exist: No such file or directory
```

</div>

و اسکریپت **همان‌جا ایستاد** (کد خروج ۱). خط بعدی اجرا نشد.

### ‏`-u`: متغیر تعریف‌نشده خطاست

یک غلط تایپی (`OUTDR` به جای `OUTDIR`):

<div dir="ltr">

```bash
OUTDIR=results
echo "Will remove: $OUTDR/old"
```

</div>

بی `-u`:

<div dir="ltr">

```text
Will remove: /old
```

</div>

با `-u`:

<div dir="ltr">

```text
unset.sh: line 4: OUTDR: unbound variable
```

</div>

بی `-u`، متغیرِ نبوده **رشته‌ی خالی** شد و نشانی به `/old` (در ریشه‌ی سیستم!) تبدیل شد. اگر این یک `rm -rf "$OUTDR/old"` بود، فاجعه بود. با `-u`، اسکریپت با پیام «unbound variable» (متغیر تعریف‌نشده) می‌ایستد.

### ‏`-o pipefail`: خطای درون لوله را ببین

<div dir="ltr">

```bash
set -e
zcat missing.fastq.gz | wc -l
echo "finished OK"
```

</div>

با `set -e` تنها:

<div dir="ltr">

```text
gzip: missing.fastq.gz: No such file or directory
0
finished OK
```

</div>

با `set -eo pipefail`:

<div dir="ltr">

```text
gzip: missing.fastq.gz: No such file or directory
0
```

</div>

بی `pipefail`، کد خروج لوله همان کد **آخرین** دستور (`wc`) است که موفق بود؛ پس `-e` چیزی نمی‌بیند و اسکریپت «finished OK» می‌گوید، در حالی که فایل نبود. با `pipefail`، شکست **هر** دستور لوله دیده می‌شود.

| بخش | بی آن | با آن |
| :--- | :--- | :--- |
| `-e` | خطا نادیده گرفته می‌شود و کار ادامه می‌یابد | با نخستین خطا می‌ایستد |
| `-u` | متغیرِ نبوده خالی می‌شود | خطا: «unbound variable» |
| `-o pipefail` | تنها خطای آخرین دستور لوله دیده می‌شود | خطای هر دستور لوله دیده می‌شود |

> 📺 **فیلم:** *How To Write Bash Scripts In Linux, Part 6: Exit Codes*: https://www.youtube.com/watch?v=6N4RNPRx0xs (LearnLinuxTV)
> 📄 **مرجع:** GNU Bash Reference Manual, بخش The Set Builtin: https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html

---

## ۶. کارهای طولانی

برخی ابزارهای بیوانفورماتیک ساعت‌ها کار می‌کنند. اگر ترمینال را ببندید یا اینترنت (در `ssh`) قطع شود، کار هم قطع می‌شود.

### `nohup … &`

<div dir="ltr">

```bash
nohup bash long_job.sh > job.log 2>&1 &
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `nohup` | «با بسته شدن ترمینال، کار را نکُش» (*no hang-up*) |
| `> job.log` | خروجی به `job.log` |
| `2>&1` | پیام‌های خطا هم به همان جا (ماژول ۰۴، کادر کنجکاوها) |
| `&` | در **پس‌زمینه** اجرا کن و ترمینال را آزاد بگذار |

ترمینال یک شماره‌ی کار نشان می‌دهد و بی‌درنگ آزاد می‌شود. پیشرفت را با `tail job.log` ببینید.

### ‏`tmux`: نشست پایدار

‏`tmux` یک «نشست» می‌سازد که حتی اگر از سرور جدا شوید، زنده می‌ماند:

<div dir="ltr">

```bash
tmux new -s analysis       # نشست تازه به نام analysis
# … کار را اجرا کنید؛ سپس Ctrl+b و پس از آن d برای جدا شدن
tmux attach -t analysis    # بازگشت به نشست، حتی فردا
```

</div>

روی سرورهای مشترک دانشگاه، کارهای سنگین را با سامانه‌ی صف (مانند SLURM، بخش ۱۰) اجرا کنید، نه مستقیم.

---

## ۷. سه اشتباه رایج

| اشتباه | چه می‌شود | به جایش |
| :--- | :--- | :--- |
| اسکریپت بی `set -euo pipefail` | خطا بی‌صدا ادامه می‌یابد؛ پوشه یا متغیر نادرست (بخش ۵) | همیشه در خط دوم |
| ورودی‌ها را وارسی نکردن | پیام‌های گیج‌کننده و خروجی نادرست («۰ رید»؛ بخش ۳) | ‏`if [ $# -eq 0 ]` و `if [ ! -s "$f" ]` |
| نوشتن اسکریپت در Word | نویسه‌های پنهان؛ اسکریپت با خطاهای عجیب اجرا نمی‌شود | ‏`nano`، VS Code یا هر ویرایشگر متن ساده |

---

## ۸. جمع‌بندی

- اسکریپت = دستورها در یک فایل؛ خط یکم `#!/usr/bin/env bash`، یادداشت‌ها با `#`، اجرا با `bash script.sh`.
- ورودی‌ها: `$1`، `$2`، … ؛ `$#` شمارشان؛ `"$@"` همه‌شان.
- ‏`if [ … ]; then … fi` برای وارسی؛ پیام خطا با `>&2`؛ پایان با `exit 1`.
- ‏`set -euo pipefail`: با خطا بایست، متغیر نبوده خطاست، خطای لوله دیده شود.
- کار طولانی: `nohup bash job.sh > job.log 2>&1 &` یا `tmux`.

---

## کارت دستورهای این درس

| می‌خواهم… | دستور |
| :--- | :--- |
| اسکریپت بنویسم | ‏`nano script.sh` (ذخیره `Ctrl+O`، بیرون `Ctrl+X`) |
| اجرا کنم | ‏`bash script.sh ورودی‌ها` |
| خط یکم و دوم هر اسکریپت | ‏`#!/usr/bin/env bash` و `set -euo pipefail` |
| ورودی یکم | `$1` |
| همه‌ی ورودی‌ها در حلقه | `for f in "$@"; do …; done` |
| اگر ورودی نبود | `if [ $# -eq 0 ]; then echo "Usage: …" >&2; exit 1; fi` |
| اگر فایل نبود یا خالی بود | `if [ ! -s "$f" ]; then …; fi` |
| کد خروج دستور پیشین | `echo $?` |
| اجرای طولانی در پس‌زمینه | `nohup bash job.sh > job.log 2>&1 &` |
| نشست پایدار | `tmux new -s name` · `tmux attach -t name` |

---

<details>
<summary>📘 <b>برای کنجکاوها (اختیاری):</b> چرا <code>zcat file | head</code> با <code>pipefail</code> گاهی خطای 141 می‌دهد؟</summary>

‏`head` پس از خواندن چند خط، لوله را می‌بندد. `zcat` که هنوز می‌خواهد بنویسد، پیام «لوله بسته شد» (SIGPIPE) می‌گیرد و با کد ۱۴۱ می‌ایستد. بی `pipefail` این دیده نمی‌شود؛ ولی با `pipefail` کل لوله «شکست» حساب می‌شود و `-e` اسکریپت را می‌ایستاند، در حالی که هیچ اشتباهی رخ نداده است. در اسکریپت‌های این دوره، برای همان یک خط `set +o pipefail` (خاموش کردن pipefail) گذاشته‌ایم و پس از آن دوباره روشنش می‌کنیم. در کار روزمره در ترمینال این مشکلی نیست، چون `pipefail` روشن نیست.
</details>

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| اسکریپت (script) | فایل متنی از دستورها که با `bash file.sh` اجرا می‌شود |
| شِبَنگ (shebang) | خط یکم `#!…` که می‌گوید فایل با چه برنامه‌ای اجرا شود |
| ورودی اسکریپت (argument) | چیزهایی که پس از نام اسکریپت می‌نویسید: `$1`، `$2`… |
| کد خروج (exit code) | عددی که هر دستور در پایان برمی‌گرداند؛ ۰ = موفق |
| stderr (`>&2`) | خروجی ویژه‌ی پیام‌های خطا |
| `set -euo pipefail` | سپر ایمنی: ایستادن با خطا، متغیر تعریف‌نشده، و خطای درون لوله |
| پس‌زمینه (`&`) | اجرای دستور بی آن‌که ترمینال منتظرش بماند |

---

## منابع

### درس و راهنمای رایگان
- ‏Software Carpentry — *The Unix Shell*، درس «Shell Scripts»: https://swcarpentry.github.io/shell-novice/
- ‏GNU Bash Reference Manual، بخش The Set Builtin: https://www.gnu.org/software/bash/manual/bash.html

### کتاب
- ‏Shotts W. *The Linux Command Line*، بخش ۴ (Writing Shell Scripts): https://linuxcommand.org/tlcl.php
- ‏Buffalo V (2015). *Bioinformatics Data Skills*. O'Reilly. (فصل ۱۲: اسکریپت‌نویسی پوسته و خط لوله)

### فیلم‌های آموزشی

**Coursera:**
- Johns Hopkins University — *Command Line Tools for Genomic Data Science*: https://www.coursera.org/learn/genomic-tools

**edX:**
- ‏IBM — *Linux Commands & Shell Scripting*، بخش نوشتن اسکریپت Bash: https://www.edx.org/learn/linux/ibm-linux-commands-shell-scripting

**YouTube:**
- Bioinformatics Coach — *Linux Tutorial for Bioinformatics 101, Episode 1*: https://www.youtube.com/watch?v=zvXe3udfg_I

> **وارسی نشانی‌ها (2026-10-20):** کتاب‌ها، راهنمای Bash و edX با درخواست مستقیم وارسی شدند. Coursera (خطای 451) و YouTube (فیلترشده) از سرور دوره باز نمی‌شوند؛ نشانی Coursera با موتور جستجو در 2026-10-19 و ویدیو آخرین بار در 2026-10-13 وارسی شد. همه‌ی دستورها در 2026-10-20 با bash 5.2 اجرا شدند. پیام‌های خطای اسکریپت‌ها با نام اسکریپت آغاز می‌شوند؛ نشانی پوشه‌ها را کوتاه کرده‌ایم.

</div>
