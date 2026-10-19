<div dir="rtl">

# پاسخ تشریحی: آماده کردن کامپیوتر

> خروجی‌ها روی کامپیوتر دوره (Ubuntu 24.04، کاربر `ubuntu`) در 2026-10-19 گرفته شده‌اند. نام کاربری، نشانی‌ها و نسخه‌ها روی کامپیوتر شما فرق دارد و این عادی است.

---

## تمرین ۱: ترمینال را باز کنید و خودتان را بشناسید

<div dir="ltr">

```bash
whoami
pwd
echo "Sara Ahmadi"
```

</div>

<div dir="ltr">

```text
ubuntu
/home/ubuntu
Sara Ahmadi
```

</div>

1. روی کامپیوتر دوره `ubuntu`. روی کامپیوتر شما همان نامی است که هنگام نصب Ubuntu یا WSL برگزیدید.
2. پوشه‌ی خانه در لینوکس همیشه `/home/<نام‌کاربری>` است. روی مک `/Users/<نام‌کاربری>` است.
3. هر نامی که بنویسید، دوباره چاپ می‌شود. نقل‌قول (`"…"`) نام را با فاصله‌اش یک تکه نگه می‌دارد.
4. در `ubuntu@mycomputer:~$`، پیش از `@` نام کاربری و پس از آن نام کامپیوتر است. `~` جای کنونی (پوشه‌ی خانه) و `$` نشانه‌ی آمادگی است.

---

## تمرین ۲: نسخه‌ها را یادداشت کنید

<div dir="ltr">

```bash
bash --version | head -n 1
curl --version | head -n 1
unzip -v | head -n 1
```

</div>

<div dir="ltr">

```text
GNU bash, version 5.2.21(1)-release (x86_64-pc-linux-gnu)
curl 8.20.0 (x86_64-conda-linux-gnu) libcurl/8.20.0 OpenSSL/3.6.4 zlib/1.3.2 zstd/1.5.7 libssh2/1.11.1 nghttp2/1.68.1 mit-krb5/1.22.2
UnZip 6.00 of 20 April 2009, by Debian. Original by Info-ZIP.
```

</div>

1. روی کامپیوتر دوره: bash **5.2.21**، curl **8.20.0**، unzip **6.00**. نسخه‌های شما ممکن است کمی فرق کند (برای نمونه curl روی کامپیوتر دوره از راه Conda نصب شده است). این برای این دوره مشکلی نیست.
2. یک یادداشت ساده کافی است، برای نمونه: «تاریخ — Ubuntu 24.04 (WSL)، bash <نسخه>، curl <نسخه>، unzip <نسخه>»، با عددهایی که روی کامپیوتر خودتان دیدید. در بخش ۰۲ همین کار را با یک اسکریپت خودکار می‌کنیم.

**اشتباه رایج:** `unzip --version` پیام راهنما یا خطا می‌دهد. هر برنامه گزینه‌ی خودش را دارد. اگر `--version` کار نکرد، `-v` یا `-V` یا `--help` را امتحان کنید.

---

## تمرین ۳: فایل‌های دوره را بگیرید

<div dir="ltr">

```bash
cd ~
curl -sSL -o course.zip https://github.com/raminabiri/Bioinformatics_Learning/archive/refs/heads/main.zip
unzip -q course.zip
ls -1 Bioinformatics_Learning-main
ls -1 Bioinformatics_Learning-main/01_Linux
```

</div>

<div dir="ltr">

```text
00_Orientation
01_Linux
02_BioLinux
03_Python
04_R_Statistics
05_Reproducible_Work
06_Metagenomics
07_Bacterial_Genomics
08_AMR_Virulence_Phylogeny
09_Structural_Bioinformatics
10_Advanced
envs
PROGRESS.md
README.md
STYLE_GUIDE.md
_templates
_tools
01_Setup_Computer
02_Bash
99_scripts_data
README.md
```

</div>

‏(`ls -1` هر نام را در یک خط جدا نشان می‌دهد.)

1. دو فایل یا پوشه در پوشه‌ی خانه پیدا می‌شود: `course.zip` و پوشه‌ی `Bioinformatics_Learning-main`.
2. **۱۱ بخش**، از `00_Orientation` تا `10_Advanced`. (`envs`، `_templates` و `_tools` بخش درسی نیستند؛ ابزارهای نویسندگان دوره‌اند.)
3. در `01_Linux` دو ماژول (`01_Setup_Computer` و `02_Bash`)، یک `README.md` و پوشه‌ی **`99_scripts_data`** هست که اسکریپت‌ها و داده‌ی این بخش را دارد.

**اشتباه رایج:** اجرای `unzip` در پوشه‌ای که پیش‌تر نسخه‌ی کهنه‌ی دوره را دارد. `unzip` می‌پرسد آیا فایل‌ها را بازنویسی کند. اگر کارهای خودتان را در آن پوشه دارید، نخست نام پوشه‌ی کهنه را عوض کنید.

---

## تمرین ۴: حروف بزرگ و کوچک

<div dir="ltr">

```text
PWD: command not found
/home/ubuntu
Pwd: command not found
```

</div>

تنها `pwd` (با حروف کوچک) کار می‌کند. لینوکس `PWD` و `Pwd` را نام‌های دیگری می‌داند که چنین دستوری ندارند. (`PWD` با حروف بزرگ در Bash نام یک **متغیر** است که نشانی کنونی را نگه می‌دارد، ولی دستور نیست؛ متغیرها را در ماژول بعد می‌بینید.)

---

## تمرین ۵: کدام راه برای شما؟

1. ‏**WSL.** یک Ubuntu کامل کنار ویندوز می‌دهد و ویندوز دست نمی‌خورد.
2. **ترمینال مک برای کارهای سبک، و `ssh` به سرور برای اسمبلی.** اسمبلی ژنوم حافظه‌ی زیاد و زمان طولانی می‌خواهد. سرور هم توانمندتر است و هم با بسته شدن لپ‌تاپ کار را قطع نمی‌کند (در ماژول بعد `nohup` و `tmux` را می‌بینید).
3. **نشانی پر از فاصله و حروف فارسی است** و بسیاری از ابزارها با آن خطا می‌دهند. افزون بر این، در WSL کار روی `/mnt/c` کندتر است. بهتر است داده‌ها را به پوشه‌ای درون لینوکس با نامی مانند `~/msc_project/data` کپی کند.

</div>
