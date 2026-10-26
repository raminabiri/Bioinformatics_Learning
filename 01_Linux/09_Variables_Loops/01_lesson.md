<div dir="rtl">

# درس: متغیر و حلقه؛ یک کار برای همه‌ی فایل‌ها

**بخش:** `01_Linux` · **ماژول:** `09_Variables_Loops` · **پیش‌نیاز:** ماژول [sed و tr](../08_Sed_Tr/) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** bash 5 · **آخرین اجرا:** 2026-10-20

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. یک مقدار را در **متغیر** بگذارید و به کار ببرید، و فرق نقل‌قول تکی و دوتایی را بدانید.
2. خروجی یک دستور را در متغیر بریزید (`$( … )`) و با عددها حساب کنید (`$(( … ))`).
3. با **حلقه‌ی `for`** یک کار را برای هر چیز در یک فهرست تکرار کنید.
4. با `*` فهرستی از فایل‌ها بسازید و با `basename` نام نمونه را از نام فایل بیرون بکشید.
5. با حلقه یک جدول خلاصه برای همه‌ی نمونه‌ها بسازید.

همه‌ی دستورها را در پوشه‌ی `~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data` اجرا کنید.

---

## ۱. داستان: کاری که باید ۱۰۰ بار تکرار شود

در ماژول ۰۴ شمار ریدهای هر FASTQ را **جداگانه** گرفتیم: چهار فایل، چهار دستور، و هر بار نام فایل را دستی عوض کردیم. پروژه‌ی واقعی ده‌ها یا صدها نمونه دارد. نوشتن یک دستور ۱۰۰ بار هم کند است و هم پر از خطا: یک نام اشتباه، یک نمونه‌ی فراموش‌شده.

راه‌حل دو ابزار دارد:
- **متغیر:** نامی برای یک مقدار که می‌تواند عوض شود (مانند «نام فایل کنونی»).
- **حلقه:** «این کار را برای **هر** فایل در این فهرست تکرار کن».

---

## ۲. متغیر

### ساختن و به کار بردن

<div dir="ltr">

```bash
name="minigut"
echo "sample: $name"
```

</div>

<div dir="ltr">

```text
sample: minigut
```

</div>

#### کالبدشکافی

| تکه | یعنی |
| :--- | :--- |
| `name` | **نام** متغیر (حرف انگلیسی، عدد و `_`؛ با عدد آغاز نشود) |
| `=` | «این مقدار را در این نام بگذار». **دو سویش فاصله نگذارید** |
| `"minigut"` | **مقدار** |
| `$name` | «مقدارِ `name` را این‌جا بگذار» |

**تشبیه:** متغیر مانند یک برچسب روی لوله‌ی آزمایش است. روی برچسب `name` نوشته‌اید و درون لوله `minigut` است. هر جا `$name` بنویسید، Bash محتوای لوله را جایش می‌گذارد.

### نقل‌قول تکی یا دوتایی؟

<div dir="ltr">

```bash
echo "sample: $name"
echo 'sample: $name'
```

</div>

<div dir="ltr">

```text
sample: minigut
sample: $name
```

</div>

| نقل‌قول | ‏`$name` درونش | کاربرد |
| :--- | :--- | :--- |
| دوتایی `"…"` | **جایگزین** می‌شود | متن همراه با متغیر |
| تکی `'…'` | **همان‌گونه** می‌ماند | الگوهای `grep`، برنامه‌های `awk`، `sed` (که `$` در آن‌ها معنای خودشان را دارد) |

برای همین در ماژول ۰۷ برنامه‌ی `awk` را همیشه در نقل‌قول تکی می‌نوشتیم: در `'{print $3}'` نباید Bash به `$3` دست بزند.

### خروجی یک دستور در متغیر: `$( … )`

<div dir="ltr">

```bash
n=$(zcat fastq/minigut_R1.fastq.gz | wc -l)
echo $n
```

</div>

<div dir="ltr">

```text
200000
```

</div>

`$( … )` دستور درونش را اجرا می‌کند و **خروجی‌اش را جای خودش می‌گذارد**. پس `n` اکنون عدد ۲۰۰٬۰۰۰ را دارد.

### حساب با عدد درست: `$(( … ))`

<div dir="ltr">

```bash
echo $((n/4))
echo $((10*3+1))
echo $((7/2))
```

</div>

<div dir="ltr">

```text
50000
31
3
```

</div>

| نشانه | یعنی |
| :--- | :--- |
| `$( … )` | یک بار پرانتز: **دستور** را اجرا کن |
| `$(( … ))` | دو بار پرانتز: **حساب** کن |

⚠️ `$(( ))` تنها با **عدد درست** کار می‌کند: `7/2` می‌شود **۳**، نه ۳٫۵. برای اعشار، همان `awk` ماژول ۰۷ را به کار ببرید.

> 📺 **فیلم:** *How To Write Bash Scripts In Linux, Part 3: Variables*: https://www.youtube.com/watch?v=uQE_4Q-HZZw (LearnLinuxTV)
> 📄 **مرجع:** GNU Bash Reference Manual, بخش Shell Parameters: https://www.gnu.org/software/bash/manual/bash.html

---

## ۳. حلقه‌ی `for`

### ساختار

<div dir="ltr">

```text
for  s  in  minigut minigut_sample2 ;  do  echo "sample is $s" ;  done
 ①   ②   ③              ④                  ⑤          ⑥                 ⑦
```

</div>

| بخش | یعنی |
| :-: | :--- |
| ① | ‏`for`: «برای هر…» |
| ② | **نام متغیر** حلقه (این‌جا `s`). در هر دور، یکی از چیزهای فهرست در آن می‌نشیند |
| ③ | ‏`in`: «در…» |
| ④ | **فهرست**: چیزهایی که با فاصله جدا شده‌اند |
| ⑤ | ‏`do`: «انجام بده» |
| ⑥ | **بدنه**: کاری که برای هر چیز تکرار می‌شود (با `$s`) |
| ⑦ | ‏`done`: «پایان حلقه» |

در ترمینال بیشتر آن را در چند خط می‌نویسند (Bash تا `done` را نبیند، اجرا نمی‌کند و `>` را در آغاز خط‌های میانی نشان می‌دهد):

<div dir="ltr">

```bash
for s in minigut minigut_sample2; do
  echo "sample is $s"
done
```

</div>

<div dir="ltr">

```text
sample is minigut
sample is minigut_sample2
```

</div>

### دنبال کردن دور به دور

| دور | `$s` | بدنه چاپ می‌کند |
| :-: | :--- | :--- |
| ۱ | `minigut` | `sample is minigut` |
| ۲ | `minigut_sample2` | `sample is minigut_sample2` |
| — | فهرست تمام شد | حلقه پایان می‌یابد |

فاصله‌ی آغاز خط بدنه (دو فاصله) تنها برای خوانایی است؛ Bash به آن کاری ندارد.

> 📺 **فیلم:** *How To Write Bash Scripts In Linux, Part 9: For Loops*: https://www.youtube.com/watch?v=HvzI7c3eK5k (LearnLinuxTV)
> 📄 **مرجع:** Software Carpentry, *The Unix Shell*, درس «Loops»: https://swcarpentry.github.io/shell-novice/

---

## ۴. فهرست فایل‌ها با `*`

`*` یعنی «**هر** نویسه‌ای، هر چند تا». Bash پیش از اجرای دستور، الگوی دارای `*` را با **نام فایل‌هایی که جورند** جایگزین می‌کند:

<div dir="ltr">

```bash
echo fastq/*_R1.fastq.gz
```

</div>

<div dir="ltr">

```text
fastq/minigut_R1.fastq.gz fastq/minigut_sample2_R1.fastq.gz
```

</div>

‏`fastq/*_R1.fastq.gz` یعنی «هر فایلی در `fastq` که نامش به `_R1.fastq.gz` پایان می‌یابد». دو فایل جور بودند. (`echo` در این‌جا تنها نشان می‌دهد Bash الگو را به چه چیزی باز کرده است.)

### حلقه روی فایل‌ها

<div dir="ltr">

```bash
for f in fastq/*_R1.fastq.gz; do
  echo "$f"
done
```

</div>

<div dir="ltr">

```text
fastq/minigut_R1.fastq.gz
fastq/minigut_sample2_R1.fastq.gz
```

</div>

### ‏`basename`: نام نمونه از نام فایل

‏`basename` نشانی پوشه را برمی‌دارد، و اگر پسوندی به آن بدهید، آن را هم:

<div dir="ltr">

```bash
for f in fastq/*_R1.fastq.gz; do
  basename "$f" _R1.fastq.gz
done
```

</div>

<div dir="ltr">

```text
minigut
minigut_sample2
```

</div>

| دستور | خروجی برای `fastq/minigut_R1.fastq.gz` |
| :--- | :--- |
| `basename "$f"` | ‏`minigut_R1.fastq.gz` (بی پوشه) |
| `basename "$f" _R1.fastq.gz` | ‏`minigut` (بی پوشه و بی پسوند) |

---

## ۵. کنار هم گذاشتن همه: جدول شمار ریدها

<div dir="ltr">

```bash
for f in fastq/*_R1.fastq.gz; do
  s=$(basename "$f" _R1.fastq.gz)
  n=$(zcat "$f" | wc -l)
  printf "%s\t%s\n" "$s" "$((n/4))"
done
```

</div>

<div dir="ltr">

```text
minigut	50000
minigut_sample2	24993
```

</div>

### خط‌به‌خط

| خط | کار |
| :-: | :--- |
| ۱ | برای هر فایل R1… |
| ۲ | نام نمونه را در `s` بگذار |
| ۳ | شمار خط‌های فایل بازشده را در `n` بگذار |
| ۴ | نام نمونه، یک Tab، و شمار رید (`n/4`) را چاپ کن |

#### کالبدشکافی `printf "%s\t%s\n" "$s" "$((n/4))"`
همان `printf` ماژول ۰۷ است، این بار در خود Bash: `%s` جای یک متن، `\t` یک Tab، `\n` پایان خط. مقدارها به ترتیب در جای خالی‌ها می‌نشینند. خروجی یک **جدول TSV** است که `cut`، `sort` و `awk` آن را می‌فهمند.

### ریختن خروجی کل حلقه در فایل

`>` را **پس از `done`** بگذارید تا خروجی همه‌ی دورها در یک فایل برود:

<div dir="ltr">

```bash
for f in fastq/*_R1.fastq.gz; do
  s=$(basename "$f" _R1.fastq.gz)
  zcat "$f" | awk -v s="$s" 'NR%4==2 {n++; L+=length($0)} END{printf "%s\t%d\t%.1f\n", s, n, L/n}'
done > reads_summary.tsv
cat reads_summary.tsv
```

</div>

<div dir="ltr">

```text
minigut	50000	126.0
minigut_sample2	24993	151.0
```

</div>

‏**`awk -v s="$s"`:** متغیرهای Bash درون برنامه‌ی `awk` (که در نقل‌قول تکی است) دیده نمی‌شوند. `-v s="$s"` مقدار متغیر Bash را با همان نام به `awk` می‌دهد. خروجی: نام نمونه، شمار رید و میانگین طول؛ برای هر نمونه یک ردیف.

<details>
<summary>✋ <b>امتحان کن:</b> حلقه‌ای بنویسید که برای <b>هر چهار</b> فایل FASTQ (R1 و R2) نام فایل (بی پسوند <code>.fastq.gz</code>) و شمار خط‌هایش را چاپ کند.</summary>

<div dir="ltr">

```bash
for f in fastq/*.fastq.gz; do
  printf "%s\t%s\n" "$(basename "$f" .fastq.gz)" "$(zcat "$f" | wc -l)"
done
```

</div>

<div dir="ltr">

```text
minigut_R1	200000
minigut_R2	200000
minigut_sample2_R1	99972
minigut_sample2_R2	99972
```

</div>

`$( … )` را می‌شود مستقیم درون ورودی‌های `printf` هم نوشت.
</details>

---

## ۶. سه اشتباه رایج (با خروجی واقعی)

### اشتباه ۱: فاصله دو سوی `=`

<div dir="ltr">

```bash
name = "x"
```

</div>

<div dir="ltr">

```text
bash: name: command not found
```

</div>

‏Bash `name` را **نام یک دستور** و `=` و `"x"` را ورودی‌هایش گرفت. درستش: `name="x"`.

### اشتباه ۲: متغیر بی نقل‌قول، وقتی نام فایل فاصله دارد

فرض کنید فایلی به نام `my sample.fasta` دارید:

<div dir="ltr">

```bash
f="my sample.fasta"
wc -l $f
```

</div>

<div dir="ltr">

```text
wc: my: No such file or directory
 2 sample.fasta
 2 total
```

</div>

بی نقل‌قول، Bash مقدار را در فاصله **شکست**: دو فایل `my` و `sample.fasta`. `my` نبود (خطا)، ولی **از قضا** `sample.fasta` در همین پوشه هست، و `wc` آن را شمرد! یعنی دستور بی‌صدا روی **فایل نادرستی** کار کرد. با `wc -l "$f"` درست کار می‌کند. **قاعده: متغیرها را همیشه در `"…"` بنویسید: `"$f"`.**

### اشتباه ۳: الگویی که با هیچ فایلی جور نیست

<div dir="ltr">

```bash
for f in fastq/*_R3.fastq.gz; do
  echo "$f"
  zcat "$f" | wc -l
done
```

</div>

<div dir="ltr">

```text
fastq/*_R3.fastq.gz
gzip: fastq/*_R3.fastq.gz: No such file or directory
0
```

</div>

هیچ فایل `_R3` نیست. Bash در این حالت الگو را **همان‌گونه** (با `*`) نگه می‌دارد و حلقه **یک بار** با همین متن اجرا می‌شود. پیام خطای `zcat` (که با نام `gzip` می‌آید) نشانه‌ی این است. پیش از نوشتن حلقه، با `ls fastq/*_R3.fastq.gz` ببینید الگو با چه فایل‌هایی جور است.

---

## ۷. جمع‌بندی

- متغیر: `name="x"` (بی فاصله)، به کار بردن با `$name`؛ در `"…"` جایگزین می‌شود، در `'…'` نه.
- `$( دستور )` خروجی دستور؛ `$(( حساب ))` حساب با عدد درست.
- ‏`for x in فهرست; do … "$x" …; done` یک کار را برای هر چیز تکرار می‌کند.
- `*` در نام فایل‌ها یعنی «هر چیزی»؛ `basename "$f" پسوند` نام نمونه را می‌دهد.
- ‏`> file` پس از `done` خروجی همه‌ی دورها را در یک فایل می‌ریزد؛ `awk -v s="$s"` متغیر Bash را به `awk` می‌دهد.
- متغیرها را **همیشه** در `"…"` بنویسید.

---

## کارت دستورهای این درس

| می‌خواهم… | دستور |
| :--- | :--- |
| متغیر بسازم | `name="minigut"` |
| به کار ببرم | `echo "$name"` |
| خروجی دستور در متغیر | `n=$(zcat f.gz \| wc -l)` |
| حساب | `echo $((n/4))` |
| حلقه روی یک فهرست | `for s in a b c; do echo "$s"; done` |
| حلقه روی فایل‌ها | `for f in fastq/*_R1.fastq.gz; do …; done` |
| نام بی پوشه و پسوند | `basename "$f" _R1.fastq.gz` |
| چاپ یک ردیف جدول | `printf "%s\t%s\n" "$a" "$b"` |
| خروجی حلقه در فایل | `for …; do …; done > out.tsv` |
| متغیر Bash در awk | `awk -v s="$s" '{print s, $1}'` |

---

<details>
<summary>📘 <b>برای کنجکاوها (اختیاری):</b> حلقه روی خط‌های یک فایل، و شمارنده</summary>

**شمارنده در حلقه:**

<div dir="ltr">

```bash
i=0
for f in fastq/*.fastq.gz; do
  i=$((i+1))
done
echo $i
```

</div>

خروجی `4`: شمار فایل‌های FASTQ.

**حلقه روی خط‌های یک فایل:** اگر فهرست نمونه‌ها در یک فایل (یک نام در هر خط) باشد، حلقه‌ی `while` آن را خط‌به‌خط می‌خواند:

<div dir="ltr">

```bash
while read -r s; do
  echo "sample: $s"
done < samples.txt
```

</div>

‏`< samples.txt` فایل را به ورودی حلقه می‌دهد (وارونه‌ی `>`). `for` روی واژه‌ها کار می‌کند و `while read` روی خط‌ها؛ برای فهرستی که درونش فاصله هست، `while read` امن‌تر است.
</details>

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| متغیر (variable) | نامی برای یک مقدار (`name="x"`، سپس `$name`) |
| جایگزینی دستور (command substitution) | `$( … )`: اجرای دستور و گذاشتن خروجی‌اش به جای خودش |
| حلقه (loop) | تکرار یک کار برای هر چیز در یک فهرست |
| الگوی نام فایل (glob، `*`) | «هر چیزی» در نام فایل‌ها؛ Bash آن را به فهرست نام‌ها باز می‌کند |
| `basename` | نام فایل بی نشانی پوشه (و بی پسوند) |

---

## منابع

### درس و راهنمای رایگان
- ‏Software Carpentry — *The Unix Shell*، درس «Loops»: https://swcarpentry.github.io/shell-novice/
- GNU Bash Reference Manual: https://www.gnu.org/software/bash/manual/bash.html

### کتاب
- ‏Shotts W. *The Linux Command Line*، فصل‌های ۷ (Seeing the World as the Shell Sees It) و ۳۳ (Flow Control: Looping with for): https://linuxcommand.org/tlcl.php
- ‏Buffalo V (2015). *Bioinformatics Data Skills*. O'Reilly. (فصل ۱۲: اسکریپت‌نویسی پوسته برای بیوانفورماتیک)
- ‏Haddock SHD, Dunn CW (2011). *Practical Computing for Biologists*. Sinauer. (بخش خط فرمان)

### فیلم‌های آموزشی

**Coursera:**
- Johns Hopkins University — *Command Line Tools for Genomic Data Science*: https://www.coursera.org/learn/genomic-tools

**edX:**
- ‏IBM — *Linux Commands & Shell Scripting*، بخش متغیرها و حلقه‌ها: https://www.edx.org/learn/linux/ibm-linux-commands-shell-scripting

**YouTube:**
- Software Carpentry — *The Shell, Episode 2: Files and Directories*: https://www.youtube.com/watch?v=qrkvcX4HmYo

> **وارسی نشانی‌ها (2026-10-20):** کتاب‌ها، راهنمای Bash و edX با درخواست مستقیم وارسی شدند. Coursera (خطای 451) و YouTube (فیلترشده) از سرور دوره باز نمی‌شوند؛ نشانی Coursera با موتور جستجو در 2026-10-19 و ویدیو آخرین بار در 2026-10-13 وارسی شد. همه‌ی دستورها در 2026-10-20 با bash 5.2 اجرا شدند.

</div>
