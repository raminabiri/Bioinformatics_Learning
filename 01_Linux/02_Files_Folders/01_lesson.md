<div dir="rtl">

# درس: پوشه‌ها و فایل‌ها در ترمینال

**بخش:** `01_Linux` · **ماژول:** `02_Files_Folders` · **پیش‌نیاز:** ماژول [آماده کردن کامپیوتر](../01_Setup_Computer/) · **زمان:** حدود ۴۵ دقیقه · **ابزار:** bash و دستورهای پایه‌ی لینوکس · **آخرین اجرا:** 2026-10-20

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. ساختار یک دستور (نام، گزینه، ورودی) را بشناسید.
2. بدانید کجا هستید (`pwd`)، چه چیزی آن‌جاست (`ls`) و به جای دیگری بروید (`cd`).
3. فرق نشانی **مطلق** و **نسبی** را بدانید و `.`، `..` و `~` را به کار ببرید.
4. پوشه بسازید (`mkdir`)، فایل کپی کنید (`cp`)، جابه‌جا یا نام‌گذاری کنید (`mv`) و پاک کنید (`rm`).
5. پیام‌های خطای رایج را بخوانید و بفهمید.

---

## ۱. داستان: میز کار پژوهشی

یک پروژه‌ی بیوانفورماتیک ده‌ها فایل دارد: داده‌ی خام، خروجی ابزارها، جدول‌ها، نمودارها و اسکریپت‌ها. اگر همه در یک پوشه ریخته شوند، پس از یک ماه کسی نمی‌داند کدام فایل خام است و کدام خروجی. پس نخستین مهارت، **ساختن و جابه‌جایی میان پوشه‌ها** است، آن هم در ترمینال، چون بیشتر ابزارها تنها آن‌جا کار می‌کنند.

در این درس یک «میز کار» برای پروژه می‌سازیم:

<div dir="ltr">

```text
project/
├── data/       ← داده‌ی خام (هرگز دستی ویرایش نمی‌شود)
└── results/    ← خروجی‌ها
```

</div>

---

## ۲. ساختار یک دستور

هر دستور مانند یک جمله است: **فعل** (چه کاری)، **قید** (چگونه) و **مفعول** (روی چه چیزی):

<div dir="ltr">

```text
ls     -l     project
 ①     ②       ③
```

</div>

| بخش | نام | یعنی | نمونه |
| :-: | :--- | :--- | :--- |
| ① | **نام دستور** | چه کاری؟ | ‏`ls` = فهرست کن |
| ② | **گزینه** (option) | چگونه؟ در بسیاری از موارد با `-` آغاز می‌شود | ‏`-l` = با جزئیات |
| ③ | **ورودی** (argument) | روی چه چیزی؟ | ‏`project` = این پوشه |

- گزینه و ورودی **اختیاری**‌اند. `ls` تنها هم کار می‌کند.
- بخش‌ها با **فاصله** از هم جدا می‌شوند. پس `ls-l` (بی فاصله) یک دستور ناشناخته است.
- چند گزینه‌ی تک‌حرفی را می‌شود کنار هم نوشت: `ls -l -h` همان `ls -lh` است.
- راهنمای هر دستور: `man ls` (با `q` بیرون بیایید) یا `ls --help`.

---

## ۳. کجا هستم و این‌جا چه هست؟

ترمینال همیشه **در یک پوشه** است. به آن **پوشه‌ی کنونی** می‌گویند. سه دستور پایه:

### ‏`pwd`: کجا هستم؟

<div dir="ltr">

```bash
cd ~/Bioinformatics_Learning-main/01_Linux
pwd
```

</div>

روی کامپیوتر دوره (که دوره در `/data/bioinformatics_learning` است):

<div dir="ltr">

```text
/data/bioinformatics_learning/01_Linux
```

</div>

روی کامپیوتر شما چیزی مانند `/home/sara/Bioinformatics_Learning-main/01_Linux` می‌بینید. `pwd` کوتاه‌شده‌ی *print working directory* است.

### ‏`ls`: این‌جا چه هست؟

<div dir="ltr">

```bash
ls
```

</div>

<div dir="ltr">

```text
01_Setup_Computer
02_Files_Folders
03_Looking_at_Files
04_Pipes_Redirection
05_grep
06_Cut_Sort_Uniq
07_awk
08_Sed_Tr
09_Variables_Loops
10_Scripts
99_scripts_data
README.md
```

</div>

(ترمینال نام‌ها را در بسیاری از موارد کنار هم در چند ستون نشان می‌دهد.)

### ‏`ls` با گزینه‌ها

<div dir="ltr">

```bash
ls -l
```

</div>

<div dir="ltr">

```text
total 48
drwxrwxr-x 2 ubuntu ubuntu 4096 Oct 20 07:04 01_Setup_Computer
drwxrwxr-x 2 ubuntu ubuntu 4096 Oct 20 07:04 02_Files_Folders
…
drwxrwxr-x 2 ubuntu ubuntu 4096 Oct 20 07:04 10_Scripts
drwxrwxr-x 4 ubuntu ubuntu 4096 Oct 20 06:55 99_scripts_data
-rw-rw-r-- 1 ubuntu ubuntu 1243 Oct 20 06:55 README.md
```

</div>

(ردیف‌های میانی را با `…` کوتاه کرده‌ایم. تاریخ‌ها و نام کاربری روی کامپیوتر شما فرق دارند.)

#### کالبدشکافی یک ردیف `ls -l`

<div dir="ltr">

```text
drwxrwxr-x  2  ubuntu  ubuntu  4096  Oct 20 07:04  01_Setup_Computer
    ①       ②     ③       ④      ⑤        ⑥              ⑦
```

</div>

| بخش | یعنی |
| :-: | :--- |
| ① | **نوع و دسترسی‌ها**. حرف یکم `d` یعنی **پوشه** (directory) و `-` یعنی **فایل**. بقیه می‌گویند چه کسی می‌تواند بخواند (`r`)، بنویسد (`w`) یا اجرا کند (`x`). |
| ② | شمار پیوندها (برای این دوره مهم نیست) |
| ③ | صاحب فایل |
| ④ | گروه صاحب |
| ⑤ | **اندازه** به بایت. برای پوشه همیشه عددی مانند 4096 است و اندازه‌ی محتوا نیست. |
| ⑥ | تاریخ آخرین تغییر |
| ⑦ | **نام** |

گزینه‌های پرکاربرد دیگر:

| دستور | چه می‌کند |
| :--- | :--- |
| `ls -lh` | مانند `-l`، ولی اندازه خوانا (`2.3M` به جای `2392468`) |
| `ls -a` | فایل‌های **پنهان** را هم نشان بده (نامشان با `.` آغاز می‌شود) |
| `ls -F` | پشت نام پوشه‌ها `/` بگذار تا از فایل جدا شوند |
| `ls project` | محتوای پوشه‌ی `project` را نشان بده، بی آن‌که به آن بروی |

---

## ۴. جابه‌جایی: `cd` و نشانی‌ها

‏`cd` (*change directory*) پوشه‌ی کنونی را عوض می‌کند. پس از `cd` هیچ خروجی نمی‌بینید؛ برای وارسی، `pwd` بزنید.

### نشانی مطلق و نسبی

پوشه‌ها مانند یک **درخت**‌اند که ریشه‌اش `/` است:

<div dir="ltr">

```text
/
└── home/
    └── sara/                          ← پوشه‌ی خانه (~)
        └── Bioinformatics_Learning-main/
            └── 01_Linux/
                └── 99_scripts_data/
                    └── data/
                        └── sample.fasta
```

</div>

| گونه | از کجا شروع می‌شود | نمونه |
| :--- | :--- | :--- |
| **مطلق** | همیشه از ریشه `/` | `/home/sara/Bioinformatics_Learning-main/01_Linux` |
| **نسبی** | از پوشه‌ی کنونی | اگر در `01_Linux` باشید: `99_scripts_data/data` |

**تشبیه:** نشانی مطلق مانند نشانی کامل پستی است («تهران، خیابان…، پلاک ۵»)، که از هر جا درست است. نشانی نسبی مانند راهنمایی به رهگذر است («دو کوچه بالاتر»)، که تنها از جای کنونی درست است.

### سه نشانه‌ی ویژه

| نشانه | یعنی | نمونه |
| :-: | :--- | :--- |
| `.` | همین پوشه | ‏`ls .` همان `ls` است |
| `..` | پوشه‌ی پدر (یک پله بالاتر) | `cd ..` |
| `~` | پوشه‌ی خانه‌ی شما | `cd ~` |

### نمونه: بالا و پایین رفتن

<div dir="ltr">

```bash
cd ~/Bioinformatics_Learning-main/01_Linux
cd 99_scripts_data     # یک پله پایین (نسبی)
pwd
cd ..                  # یک پله بالا
pwd
```

</div>

<div dir="ltr">

```text
/data/bioinformatics_learning/01_Linux/99_scripts_data
/data/bioinformatics_learning/01_Linux
```

</div>

**کلید Tab:** چند حرف اول نام را بنویسید و Tab بزنید؛ ترمینال بقیه را کامل می‌کند. اگر چند گزینه باشد، دو بار Tab همه را نشان می‌دهد. Tab هم سریع‌تر است و هم جلوی غلط تایپی را می‌گیرد.

<details>
<summary>✋ <b>امتحان کن:</b> در پوشه‌ی <code>01_Linux/99_scripts_data/data</code> هستید. دستور <code>cd ../..</code> شما را کجا می‌برد؟</summary>

دو پله بالا: یکم به `99_scripts_data`، سپس به **`01_Linux`**. با `pwd` بسنجید.
</details>

> 📺 **فیلم:** *The Shell, Episode 2: Files and Directories*: https://www.youtube.com/watch?v=qrkvcX4HmYo (Software Carpentry)
> 📄 **مرجع:** Software Carpentry, *The Unix Shell*, درس «Navigating Files and Directories»: https://swcarpentry.github.io/shell-novice/

---

## ۵. ساختن، کپی، جابه‌جایی و پاک کردن

برای تمرین، در پوشه‌ی خانه یک پروژه‌ی آزمایشی می‌سازیم:

<div dir="ltr">

```bash
cd ~
```

</div>

### ‏`mkdir`: ساختن پوشه

<div dir="ltr">

```bash
mkdir project
mkdir -p project/data project/results
ls project
```

</div>

<div dir="ltr">

```text
data
results
```

</div>

#### کالبدشکافی `mkdir -p project/data project/results`

| بخش | یعنی |
| :--- | :--- |
| `mkdir` | ‏*make directory*: پوشه بساز |
| `-p` | اگر پوشه‌ی پدر نیست، آن را هم بساز؛ و اگر پوشه از پیش هست، خطا نده |
| `project/data project/results` | **دو** ورودی: دو پوشه با هم ساخته می‌شوند |

**بی `-p` چه می‌شود؟** اگر `project/data` هنوز نباشد:

<div dir="ltr">

```bash
mkdir project/data/raw
```

</div>

<div dir="ltr">

```text
mkdir: cannot create directory ‘project/data/raw’: No such file or directory
```

</div>

یعنی «نمی‌توانم `raw` را بسازم، چون پوشه‌ی پدرش نیست». با `mkdir -p project/data/raw` هر سه پله با هم ساخته می‌شوند.

### ‏`cp`: کپی

یک فایل کوچک پروتئین (`sample.fasta`) از خود دوره را در پوشه‌ی `data` پروژه کپی می‌کنیم:

<div dir="ltr">

```bash
cp Bioinformatics_Learning-main/01_Linux/99_scripts_data/data/sample.fasta project/data/
ls project/data
```

</div>

<div dir="ltr">

```text
sample.fasta
```

</div>

#### کالبدشکافی

| بخش | یعنی |
| :--- | :--- |
| `cp` | ‏*copy*: کپی کن |
| ورودی یکم | **سرچشمه**: کدام فایل |
| ورودی دوم | **مقصد**: کجا. چون به `/` پایان یافته و یک پوشه است، فایل با **همان نام** در آن کپی می‌شود |

اگر در مقصد نام فایل بنویسید (`project/data/my_protein.fasta`)، کپی با **نام تازه** ساخته می‌شود.

### ‏`mv`: جابه‌جایی یا نام‌گذاری تازه

<div dir="ltr">

```bash
mv project/data/sample.fasta project/data/protein.fasta
ls project/data
```

</div>

<div dir="ltr">

```text
protein.fasta
```

</div>

‏`mv` (*move*) فایل را جابه‌جا می‌کند. اگر مقصد در **همان پوشه** با نام دیگری باشد، در واقع **نام را عوض می‌کند**. لینوکس دستور جداگانه‌ای برای نام‌گذاری تازه ندارد.

برای دیدن محتوای یک فایل **کوچک**، `cat` را به کار ببرید:

<div dir="ltr">

```bash
cat project/data/protein.fasta
```

</div>

<div dir="ltr">

```text
>protein_sample-1
MKTAYIAKQRQISF
```

</div>

یک توالی پروتئینی ۱۴ اسیدآمینه‌ای در قالب FASTA. ⚠️ `cat` **کل** فایل را چاپ می‌کند؛ روی فایل بزرگ (ژنوم، FASTQ) آن را نزنید. راه درست را در ماژول بعد می‌بینید.

### ‏`rm`: پاک کردن

<div dir="ltr">

```bash
rm -r project
ls
```

</div>

<div dir="ltr">

```text
Bioinformatics_Learning-main
```

</div>

| دستور | پاک می‌کند |
| :--- | :--- |
| `rm file.txt` | یک فایل |
| `rm -r folder` | یک پوشه و **هر چه درونش است** (`-r` = *recursive*: پله‌به‌پله به درون) |

**بی `-r` روی پوشه:**

<div dir="ltr">

```text
rm: cannot remove 'project': Is a directory
```

</div>

‏⚠️ **`rm` سطل زباله ندارد.** چیزی که پاک شد، برنمی‌گردد. پیش از `rm -r` همیشه با `ls` ببینید دقیقاً چه چیزی درون پوشه است.

### کپی پوشه: `cp -r`
مانند `rm`، برای کپی یک **پوشه** هم `-r` لازم است:

<div dir="ltr">

```text
cp: -r not specified; omitting directory 'a'
```

</div>

این پیام یعنی «`-r` ننوشتی، پس پوشه‌ی `a` را کپی نکردم». درستش: `cp -r a backup`.

### ساختن چند پوشه با یک دستور: `{…}`

<div dir="ltr">

```bash
mkdir -p ecoli_project/{data,results,scripts}
ls ecoli_project
```

</div>

<div dir="ltr">

```text
data
results
scripts
```

</div>

‏Bash پیش از اجرای `mkdir`، نوشته‌ی `ecoli_project/{data,results,scripts}` را به **سه** نشانی باز می‌کند: `ecoli_project/data ecoli_project/results ecoli_project/scripts`. با `echo` می‌شود دید Bash چه می‌سازد:

<div dir="ltr">

```bash
echo project/{a,b}
```

</div>

<div dir="ltr">

```text
project/a project/b
```

</div>

⚠️ درون `{…}` پس از ویرگول **فاصله نگذارید**؛ `{data, results}` کار نمی‌کند.

<details>
<summary>✋ <b>امتحان کن:</b> دستوری بنویسید که پوشه‌ی <code>thesis</code> را با دو زیرپوشه‌ی <code>raw</code> و <code>clean</code> بسازد.</summary>

<div dir="ltr">

```bash
mkdir -p thesis/{raw,clean}
```

</div>

با `ls thesis` بسنجید: `clean` و `raw`.
</details>

> 📺 **فیلم:** *Linux Commands Every Beginner Needs: mkdir, touch, cp, mv & rm*: https://www.youtube.com/watch?v=Ixnwp9uF4r8
> 📄 **مرجع:** Software Carpentry, *The Unix Shell*, درس «Working With Files and Directories»: https://swcarpentry.github.io/shell-novice/

---

## ۶. سه اشتباه رایج (با خروجی واقعی)

### اشتباه ۱: نام پوشه با فاصله

<div dir="ltr">

```bash
mkdir "my data"
cd my data
```

</div>

<div dir="ltr">

```text
bash: cd: too many arguments
```

</div>

‏Bash فاصله را جداکننده‌ی ورودی‌ها می‌داند، پس `cd my data` یعنی دو ورودی: `my` و `data`. یا نام را در نقل‌قول بنویسید (`cd "my data"`)، یا بهتر از همه، **نام بی فاصله** بگذارید: `my_data`.

### اشتباه ۲: رفتن به پوشه‌ای که نیست

<div dir="ltr">

```text
bash: cd: nofolder: No such file or directory
```

</div>

یا نام را اشتباه نوشته‌اید، یا در پوشه‌ی دیگری هستید. با `pwd` ببینید کجایید و با `ls` ببینید چه پوشه‌هایی هست. برای پیشگیری، نام‌ها را با **Tab** کامل کنید.

### اشتباه ۳: `rm -r` با نشانی نادرست
‏`rm -r data` در پوشه‌ی نادرست، داده‌ی کس دیگری (یا داده‌ی خام خودتان) را برای همیشه پاک می‌کند. **پیش از هر `rm -r`، یک `pwd` و یک `ls` بزنید.**

---

## ۷. جمع‌بندی

- هر دستور = **نام** + **گزینه** (`-…`) + **ورودی**، با فاصله میانشان.
- ‏`pwd` کجا هستم، `ls` چه هست (`-l` جزئیات، `-h` اندازه‌ی خوانا، `-a` پنهان‌ها)، `cd` برو.
- نشانی **مطلق** از `/` آغاز می‌شود و نشانی **نسبی** از پوشه‌ی کنونی؛ `.` این‌جا، `..` پدر، `~` خانه.
- ‏`mkdir -p` ساختن، `cp` کپی (`-r` برای پوشه)، `mv` جابه‌جایی یا نام تازه، `rm` پاک کردن (`-r` برای پوشه؛ **بی بازگشت**).
- نام فایل و پوشه: تنها حروف انگلیسی، عدد، `_` و `-`؛ بی فاصله.

---

## کارت دستورهای این درس

| می‌خواهم… | دستور |
| :--- | :--- |
| بدانم کجا هستم | `pwd` |
| ببینم این‌جا چه هست | `ls` · `ls -lh` · `ls -a` |
| به یک پوشه بروم | `cd folder` |
| یک پله بالا بروم | `cd ..` |
| به خانه بروم | ‏`cd ~` (یا تنها `cd`) |
| پوشه بسازم (با پدرها) | `mkdir -p a/b/c` |
| چند پوشه با هم | `mkdir -p proj/{data,results}` |
| فایل کپی کنم | `cp source destination` |
| پوشه کپی کنم | `cp -r folder backup` |
| جابه‌جا یا نام‌گذاری کنم | `mv old new` |
| فایل کوچک را ببینم | `cat file` |
| فایل پاک کنم | `rm file` |
| پوشه پاک کنم | ‏`rm -r folder` (پیش از آن `ls`!) |

---

<details>
<summary>📘 <b>برای کنجکاوها (اختیاری):</b> فایل‌های پنهان و دسترسی‌ها</summary>

**فایل پنهان:** هر فایل یا پوشه‌ای که نامش با `.` آغاز شود، در `ls` معمولی دیده نمی‌شود. برنامه‌ها تنظیماتشان را در چنین فایل‌هایی نگه می‌دارند، برای نمونه `~/.bashrc` (تنظیمات Bash). `ls -a` آن‌ها را نشان می‌دهد، همراه با `.` و `..`.

**دسترسی‌ها:** در `-rw-rw-r--`، پس از حرف یکم سه گروه سه‌حرفی هست: صاحب (`rw-`)، گروه (`rw-`) و دیگران (`r--`). `r` خواندن، `w` نوشتن و `x` اجرا. برای اجرای مستقیم یک اسکریپت، `x` لازم است (`chmod +x script.sh`). در این دوره اسکریپت‌ها را با `bash script.sh` اجرا می‌کنیم که `x` نمی‌خواهد.
</details>

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| پوشه‌ی کنونی (working directory) | پوشه‌ای که ترمینال اکنون در آن است |
| نشانی مطلق / نسبی | نشانی از ریشه (`/…`) / نشانی از پوشه‌ی کنونی |
| پوشه‌ی خانه (`~`) | پوشه‌ی شخصی شما، جای پیش‌فرض ترمینال |
| گزینه (option) | بخشی از دستور که چگونگی کار را تعیین می‌کند (`-l`) |
| ورودی (argument) | چیزی که دستور روی آن کار می‌کند (نام فایل یا پوشه) |
| بازگشتی (`-r`) | کار روی پوشه و همه‌ی محتوایش |

---

## منابع

### درس و راهنمای رایگان
- ‏Software Carpentry — *The Unix Shell*، درس‌های «Navigating Files and Directories» و «Working With Files and Directories»: https://swcarpentry.github.io/shell-novice/
- Ubuntu — *The Linux command line for beginners*: https://ubuntu.com/tutorials/command-line-for-beginners

### کتاب
- ‏Shotts W. *The Linux Command Line* (نسخه‌ی رایگان آنلاین)، فصل‌های ۲ تا ۴: https://linuxcommand.org/tlcl.php
- ‏Shotts W (2019). *The Linux Command Line*, 2nd ed. No Starch Press. (فصل ۲: جابه‌جایی؛ فصل ۴: کار با فایل‌ها و پوشه‌ها)
- ‏Haddock SHD, Dunn CW (2011). *Practical Computing for Biologists*. Sinauer. (بخش خط فرمان)

### فیلم‌های آموزشی

**Coursera:**
- ‏Johns Hopkins University — *Command Line Tools for Genomic Data Science*. هفته‌ی یکم، کار با فایل‌ها و پوشه‌ها: https://www.coursera.org/learn/genomic-tools

**edX:**
- edX — *Try It: Learn Linux Command Line*: https://www.edx.org/learn/linux/edx-try-it-learn-linux-command-line
- The Linux Foundation — *Introduction to Linux*: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux

**YouTube:**
- Software Carpentry — *The Shell, Episode 2: Files and Directories*: https://www.youtube.com/watch?v=qrkvcX4HmYo

> **وارسی نشانی‌ها (2026-10-20):** درس‌ها، کتاب و edX با درخواست مستقیم وارسی شدند. Coursera (خطای 451) و YouTube (فیلترشده) از سرور دوره باز نمی‌شوند؛ نشانی Coursera با موتور جستجو در 2026-10-19 و ویدیو آخرین بار در 2026-10-13 وارسی شد. همه‌ی دستورها در 2026-10-20 اجرا شدند. پیام‌های خطا در ترمینال تعاملی با `bash:` آغاز می‌شوند.

</div>
