<div dir="rtl">

# درس: لوله و هدایت خروجی؛ وصل کردن دستورها به هم

**بخش:** `01_Linux` · **ماژول:** `04_Pipes_Redirection` · **پیش‌نیاز:** ماژول [نگاه کردن به فایل‌ها](../03_Looking_at_Files/) · **زمان:** حدود ۴۵ دقیقه · **ابزار:** `|`، `>`، `>>`، `2>`، zcat · **آخرین اجرا:** 2026-10-20

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. با **لوله** (`|`) خروجی یک دستور را به دستور بعدی بدهید.
2. با `zcat` فایل فشرده را باز کنید و به دستورهای دیگر بدهید.
3. ریدهای یک FASTQ را بشمارید و یک رید دلخواه را بیرون بکشید.
4. خروجی را در فایل بریزید (`>`)، به پایان فایل بیفزایید (`>>`)، و پیام‌های خطا را جدا نگه دارید (`2>`).

همه‌ی دستورها را در پوشه‌ی `~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data` اجرا کنید.

---

## ۱. داستان: چند رید داریم؟

در درس پیش دیدیم که FASTQها فشرده‌اند و `head` روی آن‌ها کار نمی‌کند. ولی نخستین پرسش درباره‌ی هر نمونه این است: **چند رید دارد؟** پاسخ دو گام دارد:
1. فایل را باز کن (`zcat`).
2. خط‌هایش را بشمار (`wc -l`) و بر ۴ تقسیم کن.

هر کدام از این دو گام یک دستور است. چیزی لازم داریم که **خروجی اولی را مستقیم به دومی بدهد**، بی آن‌که فایل بازشده‌ی بزرگی روی دیسک بسازیم. این همان **لوله** است.

---

## ۲. لوله (`|`)

### تشبیه
خط تولید یک کارخانه را تصور کنید: دستگاه یکم چیزی می‌سازد و روی **نوار نقاله** می‌گذارد؛ دستگاه دوم آن را برمی‌دارد و کار خودش را رویش انجام می‌دهد. لوله (`|`) همان نوار نقاله است.

<div dir="ltr">

```text
 zcat file.gz   ───│───▶   head -n 4
(همه‌ی خط‌ها را بیرون می‌ریزد)     (تنها ۴ خط اول را نگه می‌دارد و چاپ می‌کند)
```

</div>

نشانه‌ی `|` را روی صفحه‌کلید انگلیسی با `Shift` و کلید `\` (بالای Enter) می‌نویسید.

### نخستین لوله: دیدن آغاز یک فایل فشرده

<div dir="ltr">

```bash
zcat fastq/minigut_R1.fastq.gz | head -n 4
```

</div>

<div dir="ltr">

```text
@NC_006347.1_0/1
AACGTTGGCTCGTCTGACAAGCAAAGGTAAGAACAAAGGTGCCAAATATCGTAAAGAAAAACGTGACATGGCGTCCAACC…
+
BBBBBFFFFFFFFFFFFFFFFFF/FFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF…
```

</div>

#### کالبدشکافی

<div dir="ltr">

```text
zcat   fastq/minigut_R1.fastq.gz   |   head   -n 4
 ①              ②                  ③     ④      ⑤
```

</div>

| بخش | یعنی | اگر نباشد |
| :-: | :--- | :--- |
| ① | ‏`zcat`: فایل `.gz` را باز کن و محتوا را **بیرون بده** (روی دیسک چیزی نمی‌سازد) | — |
| ② | فایل فشرده | — |
| ③ | **لوله**: خروجی `zcat` را به جای چاپ، به ورودی دستور بعدی بده | ‏`zcat` **کل** فایل (۲۰۰٬۰۰۰ خط) را در ترمینال چاپ می‌کرد |
| ④ | ‏`head`: این بار **نام فایل ندارد**؛ ورودی‌اش را از لوله می‌گیرد | — |
| ⑤ | تنها ۴ خط | ۱۰ خط (۲٫۵ رید) |

**نکته‌ی مهم:** وقتی `head` چهار خط گرفت، کارش تمام است و لوله را می‌بندد. `zcat` هم با دیدن لوله‌ی بسته می‌ایستد. پس حتی روی یک فایل ۱۰ گیگابایتی، این دستور بی‌درنگ تمام می‌شود.

---

## ۳. شمردن ریدها

<div dir="ltr">

```bash
zcat fastq/minigut_R1.fastq.gz | wc -l
```

</div>

<div dir="ltr">

```text
200000
```

</div>

**این خروجی یعنی:** فایل بازشده ۲۰۰٬۰۰۰ خط دارد. هر رید ۴ خط است، پس ۲۰۰٬۰۰۰ ÷ ۴ = **۵۰٬۰۰۰ رید**. (در ماژول `awk` یاد می‌گیرید این تقسیم را هم خود ترمینال انجام دهد.)

اینجا `wc -l` هم مانند `head` نام فایل ندارد و ورودی را از لوله می‌گیرد. برای همین خروجی‌اش تنها یک عدد است، بی نام فایل.

<details>
<summary>✋ <b>امتحان کن:</b> نمونه‌ی دوم (<code>minigut_sample2_R1</code>) چند رید دارد؟</summary>

<div dir="ltr">

```bash
zcat fastq/minigut_sample2_R1.fastq.gz | wc -l
```

</div>

پاسخ: `99972` خط، یعنی ۹۹٬۹۷۲ ÷ ۴ = **۲۴٬۹۹۳ رید**.
</details>

---

## ۴. لوله‌ی چندتایی: بیرون کشیدن رید دوم

لوله‌ها را می‌شود پشت سر هم گذاشت. رید **دوم** خط‌های ۵ تا ۸ است. پس: ۸ خط اول را بگیر، و از آن‌ها ۴ خط **آخر** را:

<div dir="ltr">

```bash
zcat fastq/minigut_R1.fastq.gz | head -n 8 | tail -n 4
```

</div>

<div dir="ltr">

```text
@NC_006347.1_1/1
CGCAAAGCCAGCTTCGCGAATTGATCCGCCAGAGTTTCAATCATCCTTCCATTTATGTATGGGGGCTTCACAATGAAGTA…
+
BBBBBFFFFFFFFFFFFFFFFFFFFFFFFFFFF/FFFFFFFFFFFFFFFFFFBFFBFFFF/FFFFFFFFFFFFFFFFFF/…
```

</div>

### گام‌به‌گام

| گام | دستور | چه می‌ماند |
| :-: | :--- | :--- |
| ۱ | `zcat …` | همه‌ی ۲۰۰٬۰۰۰ خط |
| ۲ | `\| head -n 8` | خط‌های ۱ تا ۸ (رید ۱ و ۲) |
| ۳ | `\| tail -n 4` | ۴ خط آخرِ آن ۸ خط، یعنی خط‌های ۵ تا ۸ (رید ۲) |

**الگوی کلی:** برای خط‌های `a` تا `b`: `head -n b | tail -n (b-a+1)`. برای نمونه، تنها خط ۱۰۰ GFF:

<div dir="ltr">

```bash
head -n 100 ecoli_k12.gff | tail -n 1
```

</div>

### طول یک رید با `wc -c`

<div dir="ltr">

```bash
zcat fastq/minigut_R1.fastq.gz | head -n 2 | tail -n 1 | wc -c
```

</div>

<div dir="ltr">

```text
127
```

</div>

خط دوم (توالی رید یکم) **۱۲۷ بایت** است: **۱۲۶ باز + ۱ پایان‌خط**. یادتان هست؟ `wc -c` پایان‌خط را هم می‌شمارد. پس طول رید ۱۲۶ است.

<details>
<summary>✋ <b>امتحان کن:</b> لوله‌ای بنویسید که تنها <b>خط کیفیت</b> رید یکم را نشان دهد.</summary>

خط کیفیت، خط ۴ است:

<div dir="ltr">

```bash
zcat fastq/minigut_R1.fastq.gz | head -n 4 | tail -n 1
```

</div>

</details>

---

## ۵. ریختن خروجی در فایل: `>` و `>>`

لوله خروجی را به **دستور** می‌دهد؛ `>` آن را در **فایل** می‌ریزد.

### `>`: ساختن یا بازنویسی

<div dir="ltr">

```bash
head -n 20 ecoli_k12.gff > first20.gff
wc -l first20.gff
```

</div>

<div dir="ltr">

```text
20 first20.gff
```

</div>

- چیزی در ترمینال چاپ نشد؛ خروجی `head` به جای صفحه، در `first20.gff` رفت.
- اگر `first20.gff` نبود، ساخته می‌شود. ⚠️ **اگر بود، بی هیچ هشداری پاک و بازنویسی می‌شود.**

### `>>`: افزودن به پایان

<div dir="ltr">

```bash
echo "# my note" >> first20.gff
wc -l first20.gff
tail -n 1 first20.gff
```

</div>

<div dir="ltr">

```text
21 first20.gff
# my note
```

</div>

`>>` محتوای پیشین را نگه می‌دارد و خروجی تازه را **به پایان** می‌افزاید.

| نشانه | اگر فایل نیست | اگر فایل هست |
| :-: | :--- | :--- |
| `>` | می‌سازد | **پاک می‌کند** و از نو می‌نویسد |
| `>>` | می‌سازد | به **پایانش** می‌افزاید |

### لوله و `>` با هم

<div dir="ltr">

```bash
zcat fastq/minigut_R1.fastq.gz | head -n 400 > first100reads.fastq
wc -l first100reads.fastq
```

</div>

<div dir="ltr">

```text
400 first100reads.fastq
```

</div>

۴۰۰ خط = **۱۰۰ رید** نخست، در یک فایل کوچک و بازشده؛ برای آزمودن دستورها روی داده‌ی کوچک، پیش از اجرا روی کل فایل، بسیار به کار می‌آید.

---

## ۶. پیام‌های خطا: `2>`

هر دستور دو «خروجی» جداگانه دارد:

| نام | شماره | چه چیزی در آن می‌رود |
| :--- | :-: | :--- |
| ‏**stdout** (خروجی استاندارد) | ۱ | نتیجه‌ی کار |
| ‏**stderr** (خروجی خطا) | ۲ | پیام‌های خطا و هشدار |

هر دو به‌طور پیش‌فرض در ترمینال دیده می‌شوند. ولی `>` **تنها stdout** را در فایل می‌ریزد:

<div dir="ltr">

```bash
ls nofile.txt > out.txt
```

</div>

<div dir="ltr">

```text
ls: cannot access 'nofile.txt': No such file or directory
```

</div>

پیام خطا با وجود `>` در ترمینال آمد، و `out.txt` **خالی** (۰ بایت) ماند. برای ریختن خطا در فایل، `2>` را به کار ببرید:

<div dir="ltr">

```bash
ls ecoli_k12.fna nofile.txt > out.txt 2> err.txt
cat out.txt
cat err.txt
```

</div>

<div dir="ltr">

```text
ecoli_k12.fna
ls: cannot access 'nofile.txt': No such file or directory
```

</div>

#### کالبدشکافی

| بخش | یعنی |
| :--- | :--- |
| `ls ecoli_k12.fna nofile.txt` | دو فایل را فهرست کن؛ یکی هست، یکی نیست |
| `> out.txt` | نتیجه (stdout) به `out.txt` |
| `2> err.txt` | پیام‌های خطا (stderr) به `err.txt` |

**چرا مهم است؟** ابزارهای بیوانفورماتیک در بسیاری از موارد نتیجه را در stdout و **گزارش کار** (پیشرفت، هشدارها، آمار) را در stderr می‌نویسند. با `2> log.txt` گزارش را برای بعد نگه می‌دارید، بی آن‌که با نتیجه درهم شود.

---

## ۷. سه اشتباه رایج (با خروجی واقعی)

### اشتباه ۱: ورودی و خروجی یک فایل

<div dir="ltr">

```bash
head -n 5 t.gff > t.gff
wc -l t.gff
```

</div>

<div dir="ltr">

```text
0 t.gff
```

</div>

فایل **خالی** شد! `>` پیش از اجرای `head` فایل را پاک می‌کند، پس `head` چیزی برای خواندن ندارد. **هرگز در یک دستور، از یک فایل بخوانید و با `>` در همان فایل بنویسید.** نام دیگری بگذارید و سپس با `mv` جایگزین کنید.

### اشتباه ۲: نام فایل پس از `|`

<div dir="ltr">

```bash
head -n 3 ecoli_k12.gff | out.txt
```

</div>

<div dir="ltr">

```text
bash: out.txt: command not found
```

</div>

پس از `|` باید **دستور** بیاید، نه فایل. برای فایل، `>` بنویسید.

### اشتباه ۳: فراموش کردن `head` پس از `zcat`
‏`zcat file.fastq.gz` بی لوله، **کل** فایل را در ترمینال چاپ می‌کند. روی فایل واقعی میلیون‌ها خط است و دقیقه‌ها طول می‌کشد. اگر چنین شد، **`Ctrl+C`** بزنید تا بایستد.

---

## ۸. جمع‌بندی

- **`|`** خروجی یک دستور را به ورودی دستور بعدی می‌دهد. دستور پس از لوله نام فایل نمی‌خواهد.
- ‏`zcat file.gz | head` آغاز فایل فشرده؛ `zcat file.gz | wc -l` شمار خط‌ها (رید = خط ÷ ۴).
- ‏`head -n b | tail -n k` برای بیرون کشیدن یک بازه از خط‌ها.
- **`>`** خروجی را در فایل می‌ریزد (و فایل پیشین را **پاک** می‌کند)؛ **`>>`** به پایانش می‌افزاید؛ **`2>`** پیام‌های خطا را جدا می‌ریزد.

---

## کارت دستورهای این درس

| می‌خواهم… | دستور |
| :--- | :--- |
| آغاز فایل فشرده | `zcat f.gz \| head -n 4` |
| شمار خط‌های فایل فشرده | `zcat f.gz \| wc -l` |
| رید N ام از FASTQ | `zcat f.fastq.gz \| head -n 4N \| tail -n 4` |
| خط N ام هر فایل | `head -n N file \| tail -n 1` |
| ۱۰۰ رید اول در فایل تازه | `zcat f.fastq.gz \| head -n 400 > small.fastq` |
| خروجی در فایل (بازنویسی) | `command > out.txt` |
| افزودن به پایان فایل | `command >> out.txt` |
| خطاها در فایل جدا | `command > out.txt 2> err.txt` |
| ایستاندن دستوری که تمام نمی‌شود | `Ctrl+C` |

---

<details>
<summary>📘 <b>برای کنجکاوها (اختیاری):</b> ریختن هر دو خروجی در یک فایل</summary>

برای ریختن stdout و stderr با هم در یک فایل: `command > all.txt 2>&1`. بخش `2>&1` یعنی «stderr را به همان جایی بفرست که stdout می‌رود». ترتیب مهم است: نخست `> all.txt`، سپس `2>&1`. این را در ماژول اسکریپت، برای اجرای کارهای طولانی، دوباره می‌بینید.

برای این‌که خروجی هم در ترمینال دیده شود و هم در فایل برود، دستور `tee` هست: `command | tee out.txt`.
</details>

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| لوله (pipe، `\|`) | فرستادن خروجی یک دستور به ورودی دستور بعدی |
| هدایت خروجی (redirection، `>`) | ریختن خروجی در فایل به جای ترمینال |
| stdout | خروجی اصلی (نتیجه) یک دستور؛ شماره‌ی ۱ |
| stderr | خروجی پیام‌های خطا و هشدار؛ شماره‌ی ۲ |
| `zcat` | باز کردن فایل `.gz` و بیرون دادن محتوا، بی ساختن فایل روی دیسک |

---

## منابع

### درس و کتاب رایگان
- ‏Software Carpentry — *The Unix Shell*، درس «Pipes and Filters»: https://swcarpentry.github.io/shell-novice/
- ‏Shotts W. *The Linux Command Line*، فصل ۶ (Redirection): https://linuxcommand.org/tlcl.php
- ‏Buffalo V. *Bioinformatics Data Skills*. O'Reilly, 2015 (فصل ۳، Unix Data Tools): https://vincebuffalo.com/book/

### فیلم‌های آموزشی

**Coursera:**
- Johns Hopkins University — *Command Line Tools for Genomic Data Science*: https://www.coursera.org/learn/genomic-tools

**edX:**
- ‏IBM — *Linux Commands & Shell Scripting*، بخش لوله‌ها و فیلترها: https://www.edx.org/learn/linux/ibm-linux-commands-shell-scripting

**YouTube:**
- Bioinformatics Coach — *Linux Tutorial for Bioinformatics 101, Episode 1*: https://www.youtube.com/watch?v=zvXe3udfg_I

> **وارسی نشانی‌ها (2026-10-20):** درس‌ها، کتاب‌ها و edX با درخواست مستقیم وارسی شدند. Coursera (خطای 451) و YouTube (فیلترشده) از سرور دوره باز نمی‌شوند؛ نشانی Coursera با موتور جستجو در 2026-10-19 و ویدیو آخرین بار در 2026-10-13 وارسی شد. همه‌ی دستورها در 2026-10-20 اجرا شدند.

</div>
