# درس: خط فرمان لینوکس (Bash) برای داده‌های زیستی

**بخش:** `01_Computing_Foundations` · **ماژول:** `01_Bash_Linux` · **پیش‌نیاز:** ندارد · **زمان:** ۳ ساعت · **ابزار:** bash 5، GNU coreutils، grep، awk، sed · **آخرین تست:** 2026-10-13

---

## ۱. مسئله

تقریباً همه‌ی ابزارهای بیوانفورماتیک برنامه‌های خط فرمان لینوکس‌اند، و داده‌هایشان فایل‌های متنی بزرگ هستند (FASTA، FASTQ، GFF، VCF، جدول‌های TSV). یک فایل FASTQ چند گیگابایتی را نمی‌شود در Excel یا Notepad باز کرد. ولی با یک خط Bash می‌شود ریدهایش را شمرد، فیلترش کرد یا خلاصه‌اش را گرفت، **بدون اینکه کل فایل در حافظه بارگذاری شود**.

هدف این درس فهرست کردن دستورها نیست. هدف یادگرفتن **الگوی فکری Unix** است: ابزارهای کوچکی که هر کدام یک کار انجام می‌دهند و با **pipe** (`|`) به هم وصل می‌شوند. همه‌ی مثال‌ها روی داده‌ی واقعی دوره اجرا شده‌اند.

```bash
cd 01_Computing_Foundations/01_Bash_Linux
bash data/download.sh          # ژنوم و GFF مرجع E. coli K-12 (حدود ۳ مگابایت)
cd data
```

### لینوکس، یونیکس، Bash، به اختصار
- **Unix** سیستم‌عامل تجاری دهه‌ی ۱۹۷۰ (Bell Labs) است. **Linux** (۱۹۹۱) یک سیستم‌عامل آزاد و «شبیه یونیکس» است. macOS هم شبیه یونیکس است و بیشتر دستورهای این درس در آن هم کار می‌کنند، با تفاوت‌های جزئی در گزینه‌های `sed` و `grep`.
- **Shell** برنامه‌ای است که دستور شما را می‌گیرد و اجرا می‌کند. **Bash** (Bourne Again SHell) رایج‌ترین shell لینوکس است.
- روی ویندوز از **WSL** (Windows Subsystem for Linux) استفاده کنید.

## ۲. جابه‌جایی و مدیریت فایل

```bash
pwd                         # کجا هستم؟ (مسیر مطلق)
ls -lh                      # فهرست با حجم خوانا و مجوزها
mkdir -p project/{data,results,scripts}   # چند پوشه با یک دستور (brace expansion)
cp ecoli_k12.gff project/data/
mv project/data/ecoli_k12.gff project/data/annotation.gff
rm -r project                # حذف؛ بازگشت‌ناپذیر است، سطل زباله ندارد
du -sh .  ;  df -h .         # حجم این پوشه / فضای آزاد دیسک
```
- **مسیر مطلق** با `/` شروع می‌شود (`/data/bioinformatics_learning/...`). **مسیر نسبی** از پوشه‌ی فعلی حساب می‌شود (`../data/file.fa`).
- کلید **Tab** نام فایل را کامل می‌کند و جلوی بیشتر خطاهای `No such file or directory` را می‌گیرد.
- `ls -l` در ستون اول **مجوزها** را نشان می‌دهد (`-rw-r--r--`: خواندن/نوشتن برای مالک، فقط خواندن برای بقیه). اسکریپت باید مجوز اجرا داشته باشد (`chmod +x script.sh`) یا با `bash script.sh` اجرا شود.

## ۳. نگاه کردن به فایل‌های بزرگ بدون باز کردن کامل آن‌ها

```bash
head -n 2 ecoli_k12.fna
```
```text
>NC_000913.3 Escherichia coli str. K-12 substr. MG1655, complete genome
AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGCTTCTGAACTG
```
```bash
tail -n 3 ecoli_k12.gff     # سه خط آخر
less -S ecoli_k12.gff       # مرور تعاملی؛ -S خطوط بلند را نمی‌شکند؛ q برای خروج
wc -l ecoli_k12.fna         # تعداد خطوط
```
```text
58022 ecoli_k12.fna
```

**فایل‌های فشرده را باز نکنید.** `zcat`، `zgrep` و `zless` مستقیم روی `.gz` کار می‌کنند:
```bash
R=../../../03_Metagenomics/data/raw          # داده‌ی بخش ۰۳ (اگر دانلود کرده‌اید)
zcat $R/minigut_R1.fastq.gz | head -n 4
zcat $R/minigut_R1.fastq.gz | awk 'END{print NR/4}'    # تعداد رید = خطوط ÷ ۴
```
```text
50000
```

## ۴. Pipe: ترکیب ابزارهای کوچک

`|` خروجی یک دستور را ورودی دستور بعدی می‌کند. الگوی **`cut | sort | uniq -c | sort -rn`** شاید پرکاربردترین الگوی بیوانفورماتیک باشد: «از هر چیز چندتا داریم؟»
```bash
grep -v '^#' ecoli_k12.gff | cut -f3 | sort | uniq -c | sort -rn | head -6
```
```text
   4506 gene
   4340 CDS
    216 exon
    145 pseudogene
    108 ncRNA
     86 tRNA
```
- `grep -v '^#'` خطوط توضیحی GFF را حذف می‌کند (`-v` یعنی معکوس، و `^` یعنی ابتدای خط).
- `cut -f3` ستون سوم را جدا می‌کند. فایل‌های GFF با **Tab** جدا شده‌اند و Tab جداکننده‌ی پیش‌فرض `cut` است.
- `uniq -c` تکرارهای **پشت‌سرهم** را می‌شمارد. به همین دلیل قبلش `sort` لازم است.

### redirect: ذخیره‌ی خروجی و خطا
```bash
grep '^>' ecoli_k12.fna > headers.txt     # > فایل را می‌سازد یا بازنویسی می‌کند
echo "second line" >> headers.txt         # >> به انتهای فایل اضافه می‌کند
some_tool input.fa > out.txt 2> err.log   # 2> خطاها (stderr) را جدا ذخیره می‌کند
```

## ۵. grep: جستجو

| گزینه | کار | مثال |
| :--- | :--- | :--- |
| `-c` | شمارش خطوط منطبق | `grep -c '^>' file.fa` (تعداد توالی) |
| `-v` | خطوط **غیر**منطبق | `grep -v '^#' file.gff` |
| `-w` | فقط کلمه‌ی کامل | `grep -w 'rpoB' file.gff` |
| `-i` | بدون حساسیت به حروف بزرگ/کوچک | `grep -i 'atg'` |
| `-E` | عبارت منظم گسترده | `grep -E 'rpo[BC]'` |
| `-o` | فقط بخش منطبق | `grep -oE 'Name=rpo[A-Z]+'` |
| `-P` | عبارت منظم Perl (مثلاً `\t`) | `grep -P '\tgene\t'` |

```bash
grep -P '\tgene\t' ecoli_k12.gff | grep -oE 'Name=rpo[A-Z]+' | sort | tr '\n' ' '
```
```text
Name=rpoA Name=rpoB Name=rpoC Name=rpoD Name=rpoE Name=rpoH Name=rpoN Name=rpoS Name=rpoZ
```

### ⚠️ یک دام واقعی: شمارش الگو در FASTA
FASTA معمولاً توالی را در خطوط ۶۰ یا ۸۰ کاراکتری می‌شکند (اینجا ۸۰). `grep` **خط به خط** کار می‌کند، پس الگویی که روی مرز دو خط افتاده دیده نمی‌شود:
```bash
grep -v '^>' ecoli_k12.fna | grep -o ATG | wc -l                 # روش ساده (غلط)
grep -v '^>' ecoli_k12.fna | tr -d '\n' | grep -o ATG | wc -l    # اول خطوط را به هم بچسبان
```
```text
74355
76282
```
روش اول **۱٬۹۲۷ مورد (۲٫۵٪) را از دست داد**، بدون هیچ پیام خطایی. این همان نوع خطای بی‌صدایی است که فقط با شناخت فرمت داده پیدا می‌شود. (برای توالی‌های بزرگ‌تر ابزار تخصصی مثل `seqkit locate` بهتر است. ATG نمی‌تواند با خودش هم‌پوشانی داشته باشد، پس `grep -o` در این مورد شمارش هم‌پوشان را از دست نمی‌دهد.)

## ۶. awk: محاسبه روی ستون‌ها

`awk` هر خط را به ستون‌های `$1`، `$2` و … می‌شکند و برای هر خط یک «عمل» اجرا می‌کند. `NR` شماره‌ی خط است و `END{}` بعد از آخرین خط اجرا می‌شود.

```bash
# تعداد ژن روی هر رشته (ستون ۷ در GFF)
awk -F'\t' '$3=="gene" {print $7}' ecoli_k12.gff | sort | uniq -c
```
```text
   2216 +
   2290 -
```
```bash
# میانگین طول ژن‌ها (مختصات GFF مبنای ۱ و دوسر بسته است → طول = پایان - شروع + ۱)
awk -F'\t' '$3=="gene" {l=$5-$4+1; s+=l; n++} END{printf "n=%d mean=%.1f\n", n, s/n}' ecoli_k12.gff
```
```text
n=4506 mean=897.4
```
```bash
# پنج ژن بلندتر
awk -F'\t' '$3=="gene" {match($9,/Name=[^;]+/); print $5-$4+1 "\t" substr($9,RSTART+5,RLENGTH-5)}' ecoli_k12.gff \
  | sort -k1,1nr | head -5
```
```text
7020	yeeJ
4962	yfhM
4617	lhr
4581	ypjA
4563	yghJ
```
```bash
# میانگین طول ریدهای FASTQ (خط دوم هر رکورد ۴خطی: NR%4==2)
zcat $R/minigut_R1.fastq.gz | awk 'NR%4==2 {n++; s+=length($0)} END{print "mean length", s/n}'
```
```text
mean length 126
```

## ۷. sed: ویرایش جریانی
```bash
sed 's/^>\(NC_[0-9.]*\) .*/>\1/' ecoli_k12.fna | head -1     # کوتاه کردن هدر به شناسه
```
```text
>NC_000913.3
```
`s/الگو/جایگزین/` جایگزینی می‌کند. `\( \)` یک گروه را نگه می‌دارد و `\1` آن را برمی‌گرداند. هدرهای طولانی با فاصله در بعضی ابزارها (مثلاً ساخت ایندکس یا درخت فیلوژنی) دردسر درست می‌کنند.

## ۸. متغیر، حلقه و اسکریپت

```bash
for f in $R/*_R1.fastq.gz; do
  s=$(basename "$f" _R1.fastq.gz)              # نام نمونه بدون پسوند
  n=$(zcat "$f" | awk 'END{print NR/4}')
  printf "%s\t%s\n" "$s" "$n"
done
```
```text
minigut	50000
minigut_sample2	24993
```
- `$(...)` خروجی یک دستور را در متغیر می‌گذارد.
- متغیرها را همیشه **داخل نقل‌قول** بنویسید (`"$f"`)، تا نام فایل با فاصله اسکریپت را نشکند.

### اسکریپت امن
هر اسکریپت تحلیلی را با این خط شروع کنید:
```bash
#!/usr/bin/env bash
set -euo pipefail
```
- `-e`: با اولین خطا متوقف شو، نه اینکه بی‌صدا ادامه بدهی.
- `-u`: استفاده از متغیر تعریف‌نشده خطاست، نه رشته‌ی خالی. این جلوی فاجعه‌هایی مثل `rm -rf "$DIR/"` با `DIR` خالی را می‌گیرد.
- `-o pipefail`: اگر هر جزء pipe خطا بدهد، کل pipe خطا حساب شود.

نمونه‌ی کامل این سبک: [`03_Metagenomics/01_Read_QC_Trimming/scripts/run_qc.sh`](../../03_Metagenomics/01_Read_QC_Trimming/scripts/run_qc.sh).

> **نکته‌ی واقعی از همین دوره:** با `pipefail`، الگوی `zcat file.gz | head` می‌تواند خطای 141 (SIGPIPE) بدهد: `head` زودتر بسته می‌شود و `zcat` شکایت می‌کند. راه‌حل در اسکریپت‌های دوره این بود که فقط برای آن خط `set +o pipefail` شود.

## ۹. کارهای طولانی
```bash
nohup bash long_job.sh > job.log 2>&1 &     # در پس‌زمینه؛ با بستن ترمینال قطع نمی‌شود
jobs ; ps aux | grep long_job               # وضعیت
tmux new -s analysis                        # جلسه‌ی پایدار؛ Ctrl-b d برای جدا شدن، tmux attach برای برگشتن
```
روی سرور مشترک، کارهای سنگین را با زمان‌بند (مثل SLURM، بخش ۰۷) اجرا کنید، نه مستقیم.

## ۱۰. دام‌ها (Pitfalls)

| دام | چرا مشکل است | راه درست |
| :--- | :--- | :--- |
| شمارش الگو در FASTA چندخطی با `grep` | تطابق‌های روی مرز خط گم می‌شوند (اینجا ۲٫۵٪) | خطوط را بچسبانید یا از `seqkit` استفاده کنید |
| `uniq -c` بدون `sort` | فقط تکرارهای پشت‌سرهم شمرده می‌شوند | `sort \| uniq -c` |
| `cut -d' '` روی فایل Tab-دار | ستون‌ها اشتباه جدا می‌شوند | جداکننده‌ی پیش‌فرض `cut` Tab است |
| متغیر بدون نقل‌قول | نام‌های دارای فاصله می‌شکنند | `"$var"` |
| اسکریپت بدون `set -euo pipefail` | خطای وسط کار نادیده گرفته می‌شود و خروجی ناقص می‌ماند | همیشه در خط دوم |
| باز کردن فایل `.gz` روی دیسک | فضا و زمان هدر می‌رود | `zcat`، `zgrep` |
| `rm -rf` با مسیر متغیر | پاک شدن پوشه‌ی اشتباه | `set -u`؛ قبل از حذف `ls` کنید |

## ۱۱. جمع‌بندی
- Bash برای کار با داده‌ی زیستی یعنی **ترکیب ابزارهای کوچک با pipe**، روی فایل‌های بزرگ، بدون بارگذاری کامل.
- `grep` برای جستجو، `cut/sort/uniq` برای شمارش، `awk` برای محاسبه روی ستون‌ها، `sed` برای ویرایش، و حلقه برای تکرار روی نمونه‌ها.
- فرمت داده را بشناسید (FASTA چندخطی، FASTQ چهارخطی، GFF مبنای ۱). خطاهای بی‌صدا از همین‌جا می‌آیند.

---

## منابع

### کتاب و مستندات
- Buffalo V. *Bioinformatics Data Skills*. O'Reilly, 2015 (فصل‌های ۳ و ۷: Unix و کار با داده‌ی متنی): https://vincebuffalo.com/book/
- Shotts W. *The Linux Command Line* (نسخه‌ی رایگان آنلاین): https://linuxcommand.org/tlcl.php
- Software Carpentry — *The Unix Shell* (درس رایگان و تعاملی): https://swcarpentry.github.io/shell-novice/

### ویدیوهای آموزشی
- Software Carpentry — *The Shell, Episode 1: Introduction*: https://www.youtube.com/watch?v=U3iNcBtycaQ
- Software Carpentry — *The Shell, Episode 2: Files and Directories*: https://www.youtube.com/watch?v=qrkvcX4HmYo
- Bioinformatics Coach — *Linux Tutorial for Bioinformatics 101, Episode 1*: https://www.youtube.com/watch?v=zvXe3udfg_I

> لینک‌ها در تاریخ 2026-10-13 بررسی شدند (`_tools/check_links.sh`).
