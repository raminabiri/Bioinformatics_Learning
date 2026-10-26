<div dir="rtl">

# درس: نگاه کردن به فایل‌های بزرگ، بی‌آن‌که بازشان کنید

**بخش:** `01_Linux` · **ماژول:** `03_Looking_at_Files` · **پیش‌نیاز:** ماژول [پوشه‌ها و فایل‌ها](../02_Files_Folders/) · **زمان:** حدود ۴۵ دقیقه · **ابزار:** head، tail، wc، less، zless، file · **آخرین اجرا:** 2026-10-20

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. داده‌ی این بخش (ژنوم، فهرست ژن‌ها و چند FASTQ) را دانلود کنید.
2. آغاز و پایان یک فایل بزرگ را ببینید (`head`، `tail`).
3. خط‌ها، واژه‌ها و بایت‌های یک فایل را بشمارید (`wc`).
4. یک فایل بزرگ را صفحه‌به‌صفحه ورق بزنید و در آن جستجو کنید (`less`).
5. فایل فشرده (`.gz`) را بی باز کردن روی دیسک ببینید (`zless`) و بفهمید چه چیزی در آن است (`file`).

---

## ۱. داستان: ۱٬۵۵۰ صفحه، و تنها صفحه‌ی یکم را می‌خواهیم

در بخش ۰۰ دیدیم که ژنوم *E. coli* اگر چاپ شود، نزدیک به ۱٬۵۵۰ صفحه است. یک FASTQ واقعی ده‌ها برابر بزرگ‌تر است. پرسش‌های نخست درباره‌ی هر فایل تازه این‌هاست:
- آغازش چه شکلی است؟ (فرمت درست است؟)
- پایانش چه؟ (فایل کامل دانلود شده یا نیمه‌کاره مانده؟)
- چقدر بزرگ است؟ (چند خط، چند توالی، چند رید؟)

برای این پرسش‌ها لازم نیست کل فایل را باز کنید. دستورهای این درس تنها **همان تکه‌ای** را می‌خوانند که می‌خواهید.

---

## ۲. دانلود داده‌ی این بخش

<div dir="ltr">

```bash
cd ~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data
bash download.sh
```

</div>

- فایل `download.sh` چند دستور پشت سر هم دارد که داده را با `curl` از NCBI و GitHub دانلود می‌کند (روی هم نزدیک به ۱۲ مگابایت). نوشتن چنین فایلی (**اسکریپت**) را در ماژول ۱۰ یاد می‌گیرید؛ اکنون تنها اجرایش کنید.
- ‏`bash download.sh` یعنی «دستورهای این فایل را یکی‌یکی اجرا کن».

**خروجی** (پس از یکی دو دقیقه):

<div dir="ltr">

```text
92c997bcd88e983ffdb21b2712ed3736  ecoli_k12.fna
837628601d3bbf74c218716d7ea2df86  ecoli_k12.gff
10691078950a63150244e7517ded803d  fastq/minigut_R1.fastq.gz
090cf62530b6874f7fc746ed550bd6bf  fastq/minigut_R2.fastq.gz
1d088537e5180930578097a999d2ca72  fastq/minigut_sample2_R1.fastq.gz
83a9588a59325f3798fc2f8d8ef1f3ea  fastq/minigut_sample2_R2.fastq.gz
68b50cfb970f4c490bf87388b7f43b3f  host_chr21_region.fa
Done. Files are in <نشانی همین پوشه روی کامپیوتر شما>
```

</div>

**این خروجی یعنی:** هر خط یک فایل دانلودشده است. رشته‌ی ۳۲ نویسه‌ای سمت چپ **md5** آن است: یک «اثر انگشت» که از محتوای فایل ساخته می‌شود. اگر md5 فایل‌های شما **دقیقاً** همین‌ها باشد، فایل‌ها سالم و همان فایل‌های این درس‌اند. اگر حتی یکی فرق داشت، دانلود را دوباره اجرا کنید. خط آخر نشانی پوشه را روی کامپیوتر خودتان نشان می‌دهد.

| فایل | چیست |
| :--- | :--- |
| `ecoli_k12.fna` | ژنوم *E. coli* K-12 در فرمت FASTA |
| `ecoli_k12.gff` | فهرست ژن‌ها و جای هر کدام روی ژنوم (GFF) |
| `fastq/*.fastq.gz` | ریدهای دو نمونه‌ی کوچک میکروبیوم (شبیه‌سازی‌شده)، هر نمونه R1 و R2 |
| `host_chr21_region.fa` | تکه‌ای از کروموزوم ۲۱ انسان (برای ماژول‌های بعد) |

---

## ‏۳. `head`: آغاز فایل

<div dir="ltr">

```bash
head -n 2 ecoli_k12.fna
```

</div>

<div dir="ltr">

```text
>NC_000913.3 Escherichia coli str. K-12 substr. MG1655, complete genome
AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGCTTCTGAACTG
```

</div>

### کالبدشکافی

<div dir="ltr">

```text
head    -n 2    ecoli_k12.fna
 ①       ②          ③
```

</div>

| بخش | یعنی | اگر نباشد |
| :-: | :--- | :--- |
| ① | «سر» فایل را نشان بده | — |
| ② | ‏`-n 2`: تنها **۲** خط (n = *number*) | ‏`head` به‌طور پیش‌فرض **۱۰** خط نشان می‌دهد |
| ③ | کدام فایل | ‏`head` منتظر ورودی می‌ماند (با `Ctrl+C` بیرون بیایید) |

**این خروجی یعنی:** همان FASTA بخش ۰۰: خط عنوان با `>` و سپس توالی. خط توالی ۸۰ حرف دارد.

### آغاز فایل GFF

<div dir="ltr">

```bash
head -n 5 ecoli_k12.gff
```

</div>

<div dir="ltr">

```text
##gff-version 3
#!gff-spec-version 1.21
#!processor NCBI annotwriter
#!genome-build ASM584v2
#!genome-build-accession NCBI_Assembly:GCF_000005845.2
```

</div>

خط‌هایی که با `#` آغاز می‌شوند **توضیح**‌اند: نسخه‌ی فرمت، برنامه‌ای که فایل را ساخته، و شناسه‌ی ژنوم (`GCF_000005845.2`، همان شناسه‌ای که در بخش ۰۰ دیدیم). خود جدول ژن‌ها پس از این خط‌ها می‌آید.

---

## ‏۴. `tail`: پایان فایل

<div dir="ltr">

```bash
tail -n 2 ecoli_k12.fna
```

</div>

<div dir="ltr">

```text
ATAAAACTGGTCGACTGGTTACAACAACGCCTGGGGCTTTTAGAGCAACGAGACACGGCAATGTTGCACCGTTTGCTGCA
TGATATTGAAAAAAATATCACCAAATAAAAAACGCCTTAGTAAGTATTTTTC
```

</div>

‏`tail` همان `head` است، ولی از پایان. گزینه‌ی `-n` همان معنا را دارد.

**این خروجی یعنی:** خط آخر کوتاه‌تر از ۸۰ حرف است، چون توالی همان‌جا تمام می‌شود. اگر فایلی **نیمه‌کاره** دانلود شده باشد، پایانش در بسیاری از موارد وسط یک خط یا رکورد بریده شده است. پس `tail` نخستین وارسی سلامت فایل است.

<details>
<summary>✋ <b>امتحان کن:</b> آخرین خط <code>ecoli_k12.gff</code> چیست؟</summary>

<div dir="ltr">

```bash
tail -n 1 ecoli_k12.gff
```

</div>

پاسخ: `###`. در GFF این نشانه یعنی «پایان یک بخش». خط پیش از آن آخرین CDS ژنوم است.
</details>

---

## ‏۵. `wc`: شمردن

<div dir="ltr">

```bash
wc ecoli_k12.fna
```

</div>

<div dir="ltr">

```text
  58022   58030 4699745 ecoli_k12.fna
```

</div>

### کالبدشکافی خروجی

| ستون | یعنی |
| :-: | :--- |
| `58022` | شمار **خط**‌ها |
| `58030` | شمار **واژه**‌ها (تکه‌های جداشده با فاصله) |
| `4699745` | شمار **بایت**‌ها (کمابیش شمار نویسه‌ها) |
| `ecoli_k12.fna` | نام فایل |

‏`wc` کوتاه‌شده‌ی *word count* است. بیشتر وقت‌ها تنها یکی از این سه را می‌خواهیم:

| گزینه | تنها |
| :--- | :--- |
| `wc -l` | خط‌ها (l = *lines*) |
| `wc -w` | واژه‌ها |
| `wc -c` | بایت‌ها |

می‌شود چند فایل را با هم داد:

<div dir="ltr">

```bash
wc -l ecoli_k12.fna ecoli_k12.gff
```

</div>

<div dir="ltr">

```text
  58022 ecoli_k12.fna
   9531 ecoli_k12.gff
  67553 total
```

</div>

**این خروجی یعنی:** ژنوم ۵۸٬۰۲۲ خط و فهرست ژن‌ها ۹٬۵۳۱ خط دارد؛ ردیف `total` جمع آن‌هاست.

### چرا `wc -c` طول ژنوم نیست؟

طول ژنوم ۴٬۶۴۱٬۶۵۲ باز است، ولی `wc -c` عدد ۴٬۶۹۹٬۷۴۵ را داد. تفاوت ۵۸٬۰۹۳ بایت از کجاست؟
- هر خط در پایانش یک نویسه‌ی نامرئی **پایان خط** دارد: ۵۸٬۰۲۲ خط = ۵۸٬۰۲۲ بایت.
- خط عنوان (`>NC_000913.3 Escherichia coli …`) ۷۱ نویسه است.
- ۴٬۶۴۱٬۶۵۲ + ۵۸٬۰۲۲ + ۷۱ = **۴٬۶۹۹٬۷۴۵** ✓

درس: **هر عدد را با دانستن آنچه شمرده می‌شود تفسیر کنید.** طول درست ژنوم را در ماژول‌های بعد با دستورهای دقیق‌تر حساب می‌کنیم.

---

## ‏۶. `less`: ورق زدن

<div dir="ltr">

```bash
less -S ecoli_k12.gff
```

</div>

‏`less` فایل را **صفحه‌به‌صفحه** نشان می‌دهد و تنها همان صفحه را در حافظه می‌گذارد؛ پس فایل چندگیگابایتی هم بی‌درنگ باز می‌شود. هیچ خروجی‌ای در ترمینال نمی‌ماند؛ صفحه‌ی `less` جای ترمینال را می‌گیرد تا بیرون بیایید.

| کلید | کار |
| :--- | :--- |
| ‏`Space` یا `f` | یک صفحه پایین |
| `b` | یک صفحه بالا |
| `↓` `↑` | یک خط پایین یا بالا |
| `→` `←` | چپ و راست (وقتی `-S` زده‌اید) |
| `g` / `G` | آغاز / پایان فایل |
| ‏`/rpoB` سپس Enter | جستجوی `rpoB`؛ `n` رخداد بعدی |
| `q` | **بیرون آمدن** |

گزینه‌ی `-S` خط‌های بلند را **نمی‌شکند** و بیرون از صفحه نگه می‌دارد. بی آن، هر خط GFF چند خط صفحه را می‌گیرد و ستون‌ها درهم می‌شوند.

> 📺 **فیلم:** *Linux CLI Tutorial: Cat, More, Less, Head and Tail*: https://www.youtube.com/watch?v=gfuDvpi_jYY
> 📄 **مرجع:** GNU Coreutils manual (`head`، `tail`، `wc`): https://www.gnu.org/software/coreutils/manual/coreutils.html

---

## ۷. فایل‌های فشرده: `file` و `zless`

### ‏`file`: این فایل چیست؟

<div dir="ltr">

```bash
file fastq/minigut_R1.fastq.gz ecoli_k12.fna
```

</div>

<div dir="ltr">

```text
fastq/minigut_R1.fastq.gz: gzip compressed data, was "test_minigut_R1.fastq", last modified: Mon Oct 29 17:02:45 2018, from Unix, original size modulo 2^32 13805560
ecoli_k12.fna:             ASCII text
```

</div>

**این خروجی یعنی:**
- ‏`minigut_R1.fastq.gz` با **gzip فشرده** شده است. اندازه‌ی اصلی‌اش (`original size`) **۱۳٬۸۰۵٬۵۶۰ بایت** (نزدیک به ۱۳٫۸ مگابایت) است، در حالی که `ls -lh` اندازه‌ی فشرده را **3.2M** نشان می‌دهد: نزدیک به **چهار برابر کوچک‌تر**.
- ‏`ecoli_k12.fna` یک **فایل متنی ساده** (ASCII text) است.

‏FASTQها کمابیش همیشه فشرده نگه داشته می‌شوند، چون بسیار بزرگ‌اند. بیشتر ابزارهای بیوانفورماتیک فایل `.gz` را مستقیم می‌خوانند، پس **لازم نیست آن را روی دیسک باز کنید.**

### ‏`zless`: ورق زدن فایل فشرده

<div dir="ltr">

```bash
zless fastq/minigut_sample2_R1.fastq.gz
```

</div>

‏`zless` همان `less` است برای فایل فشرده: فایل را در حافظه باز می‌کند و نشان می‌دهد، بی‌آن‌که نسخه‌ی بازشده‌ای روی دیسک بسازد. کلیدها همان کلیدهای `less`‌اند. چهار خط نخستی که می‌بینید:

<div dir="ltr">

```text
@CP009257.1_0_0/1
ACAATATAATCACCATCAACAGGTAGCGTTACTTCACCTGAAAAACCTACAGTCGAACCCACGAATAATG…
+
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF8FF…
```

</div>

یک رید کامل: نام، توالی، `+`، کیفیت (بخش ۰۰).

### اگر `head` را روی فایل فشرده بزنید؟

‏`head` فایل را **همان‌گونه که روی دیسک است** نشان می‌دهد، یعنی داده‌ی فشرده: نویسه‌های بی‌معنا و نشانه‌های عجیب، و گاهی ترمینال به هم می‌ریزد (اگر شد، `reset` بزنید). برای خواندن آغاز یک فایل فشرده با `head`، نخست باید آن را با `zcat` باز کرد و خروجی را به `head` داد. این کار **لوله** (`|`) می‌خواهد که درس ماژول بعد است.

<details>
<summary>✋ <b>امتحان کن:</b> با <code>file</code> بگویید <code>sample.fasta</code> و <code>host_chr21_region.fa</code> فشرده‌اند یا نه.</summary>

<div dir="ltr">

```bash
file sample.fasta host_chr21_region.fa
```

</div>

هر دو `ASCII text` هستند، یعنی فایل متنی ساده و فشرده‌نشده. پسوند `.fa` و `.fasta` هر دو برای FASTA به کار می‌روند.
</details>

---

## ۸. سه اشتباه رایج

| اشتباه | چه می‌شود | به جایش |
| :--- | :--- | :--- |
| ‏`cat` روی فایل بزرگ | میلیون‌ها خط از ترمینال می‌گذرد و دقیقه‌ها طول می‌کشد (با `Ctrl+C` بایستانید) | `head`، `tail`، `less` |
| ‏`head` روی `.gz` | نویسه‌های بی‌معنا؛ گاهی ترمینال به هم می‌ریزد (`reset`) | ‏`zless`، یا `zcat … \| head` (ماژول بعد) |
| ‏`gunzip` کردن فایل تنها برای دیدنش | فایل چند برابر جا می‌گیرد و نسخه‌ی فشرده پاک می‌شود | `zless` |

---

## ۹. جمع‌بندی

- داده را با `bash download.sh` گرفتیم و با md5 وارسی کردیم.
- ‏`head -n N` آغاز و `tail -n N` پایان فایل را نشان می‌دهند؛ پیش‌فرض ۱۰ خط است.
- ‏`wc` خط (`-l`)، واژه (`-w`) و بایت (`-c`) را می‌شمارد؛ هر عدد را با دانستن آنچه شمرده شده تفسیر کنید.
- ‏`less -S` برای ورق زدن (`q` بیرون، `/` جستجو).
- ‏`file` می‌گوید فایل چیست؛ `zless` فایل فشرده را بی باز کردن روی دیسک نشان می‌دهد.

---

## کارت دستورهای این درس

| می‌خواهم… | دستور |
| :--- | :--- |
| ۱۰ خط اول | `head file` |
| ‏N خط اول | `head -n N file` |
| ‏N خط آخر | `tail -n N file` |
| شمار خط‌ها | `wc -l file` |
| شمار خط، واژه و بایت | `wc file` |
| ورق زدن (بی شکستن خط) | `less -S file` |
| ورق زدن فایل فشرده | `zless file.gz` |
| فایل چیست؟ فشرده است؟ | `file name` |
| فایل کوچک را کامل ببینم | `cat file` |

---

<details>
<summary>📘 <b>برای کنجکاوها (اختیاری):</b> md5 چگونه کار می‌کند؟</summary>

‏md5 یک «تابع درهم‌ساز» (hash) است: هر فایلی، با هر اندازه‌ای، به یک رشته‌ی ۳۲ نویسه‌ای تبدیل می‌شود. اگر حتی یک بیت فایل عوض شود، رشته کاملاً دیگر می‌شود. برای ساختن md5 یک فایل: `md5sum file`. پایگاه‌هایی مانند ENA برای هر فایل FASTQ md5 را هم منتشر می‌کنند تا پس از دانلود بسنجید (ماژول دریافت داده در بخش ۰۲). md5 برای وارسی خرابی در دانلود خوب است، ولی برای امنیت (جلوگیری از دست‌کاری عمدی) دیگر ایمن شمرده نمی‌شود؛ برای آن `sha256sum` به کار می‌رود.
</details>

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| پایان خط (newline) | نویسه‌ی نامرئی پایان هر خط؛ `wc -l` همین‌ها را می‌شمارد |
| بایت (byte) | یکای اندازه‌ی فایل؛ در فایل متنی انگلیسی، هر نویسه یک بایت |
| فشرده‌سازی (gzip، `.gz`) | کوچک کردن فایل بی از دست رفتن داده؛ FASTQها نزدیک به ۴ برابر کوچک می‌شوند |
| md5 | «اثر انگشت» ۳۲ نویسه‌ای یک فایل، برای وارسی درستی دانلود |
| ASCII text | فایل متنی ساده |

---

## منابع

### درس و راهنمای رایگان
- ‏Software Carpentry — *The Unix Shell*، درس «Working With Files and Directories»: https://swcarpentry.github.io/shell-novice/

### کتاب
- ‏Shotts W. *The Linux Command Line*، فصل ۳ (Exploring the System): https://linuxcommand.org/tlcl.php
- ‏Buffalo V. *Bioinformatics Data Skills*. O'Reilly, 2015 (فصل ۳، Inspecting and Manipulating Text Data): https://vincebuffalo.com/book/
- ‏Shotts W (2019). *The Linux Command Line*, 2nd ed. No Starch Press. (فصل ۳: گشتن در سامانه)

### فیلم‌های آموزشی

**Coursera:**
- Johns Hopkins University — *Command Line Tools for Genomic Data Science*: https://www.coursera.org/learn/genomic-tools

**edX:**
- ‏The Linux Foundation — *Introduction to Linux*، بخش‌های کار با فایل‌ها: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux

**YouTube:**
- Bioinformatics Coach — *Linux Tutorial for Bioinformatics 101, Episode 1*: https://www.youtube.com/watch?v=zvXe3udfg_I
- Software Carpentry — *The Shell, Episode 1: Introduction*: https://www.youtube.com/watch?v=U3iNcBtycaQ

> **وارسی نشانی‌ها (2026-10-20):** درس‌ها، کتاب‌ها و edX با درخواست مستقیم وارسی شدند. Coursera (خطای 451) و YouTube (فیلترشده) از سرور دوره باز نمی‌شوند؛ نشانی Coursera با موتور جستجو در 2026-10-19 و ویدیوها آخرین بار در 2026-10-13 وارسی شدند. همه‌ی دستورها در 2026-10-20 اجرا شدند.

</div>
