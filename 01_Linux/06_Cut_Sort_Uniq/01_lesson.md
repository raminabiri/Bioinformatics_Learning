<div dir="rtl">

# درس: ستون‌ها و شمردن با cut، sort و uniq

**بخش:** `01_Linux` · **ماژول:** `06_Cut_Sort_Uniq` · **پیش‌نیاز:** ماژول [grep](../05_grep/) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** cut، sort، uniq (GNU coreutils) · **آخرین اجرا:** 2026-10-20

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. ستون‌های فایل GFF (و هر جدول Tab‌دار) را بشناسید.
2. با `cut` تنها ستون‌های دلخواه را بردارید.
3. با `sort` خط‌ها را بر پایه‌ی متن یا **عدد**، صعودی یا نزولی، و بر پایه‌ی یک ستون مرتب کنید.
4. با `uniq -c` خط‌های همانند را بشمارید.
5. با «الگوی طلایی» `cut | sort | uniq -c | sort -rn` بشمارید «از هر چیز چندتا داریم».

همه‌ی دستورها را در پوشه‌ی `~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data` اجرا کنید.

---

## ۱. داستان: از هر نوع چندتا؟

در ماژول ۰۵ با `grep -c` شمردیم چند ژن tRNA داریم. ولی اگر بخواهید **همه‌ی** نوع‌ها را با هم ببینید (چند ژن، چند CDS، چند tRNA، چند ژن کاذب…)، باید برای هر نوع یک `grep` جدا بزنید، و حتی پیش از آن باید بدانید چه نوع‌هایی هست!

راه بهتر: **ستون نوع** را جدا کن، مرتب کن، و همانندها را بشمار. سه ابزار کوچک، پشت سر هم در یک لوله.

---

## ۲. فایل GFF: یک جدول با ۹ ستون

‏GFF یک **جدول متنی** است: هر خط یک «چیز» روی ژنوم (یک ژن، یک CDS، یک tRNA…)، و ستون‌ها با **Tab** از هم جدا شده‌اند. خط‌هایی که با `#` آغاز می‌شوند توضیح‌اند.

برای این‌که با چشم دنبال کنیم، نخست یک فایل کوچک ۸ خطی می‌سازیم:

<div dir="ltr">

```bash
grep -v '^#' ecoli_k12.gff | head -n 8 > small.gff
```

</div>

‏(`grep -v '^#'` خط‌های توضیح را کنار می‌گذارد (ماژول ۰۵)، `head -n 8` تنها ۸ خط نخست را نگه می‌دارد، و `>` آن‌ها را در `small.gff` می‌ریزد (ماژول ۰۴).)

ستون‌های خط دوم `small.gff` (ژن *thrL*):

| ستون | نام | مقدار | یعنی |
| :-: | :--- | :--- | :--- |
| 1 | seqid | `NC_000913.3` | روی کدام توالی (کروموزوم) |
| 2 | source | `RefSeq` | چه کسی یا چه برنامه‌ای این را یافته |
| 3 | type | `gene` | چه نوع چیزی (gene، CDS، tRNA…) |
| 4 | start | `190` | جای آغاز |
| 5 | end | `255` | جای پایان |
| 6 | score | `.` | امتیاز (`.` یعنی ندارد) |
| 7 | strand | `+` | روی کدام رشته |
| 8 | phase | `.` | برای CDS؛ این‌جا کاربرد ندارد |
| 9 | attributes | `ID=gene-b0001;…;Name=thrL;…` | آگاهی‌های دیگر، به شکل `نام=مقدار` با `;` جدا شده |

**طول ژن:** شماره‌گذاری در GFF از ۱ است و هر دو سر جزو ژن‌اند، پس طول = پایان − آغاز + ۱. برای *thrL*: ۲۵۵ − ۱۹۰ + ۱ = **۶۶ نوکلئوتید**. (حساب کردن خودکار طول را در ماژول ۰۷ با `awk` یاد می‌گیرید.)

---

## ‏۳. `cut`: برداشتن ستون‌ها

### یک ستون

<div dir="ltr">

```bash
cut -f3 small.gff
```

</div>

<div dir="ltr">

```text
region
gene
CDS
gene
CDS
gene
CDS
gene
```

</div>

#### کالبدشکافی

<div dir="ltr">

```text
cut    -f3    small.gff
 ①      ②         ③
```

</div>

| بخش | یعنی | اگر نباشد |
| :-: | :--- | :--- |
| ① | «ببر»: تکه‌ای از هر خط را بردار | — |
| ② | ‏`-f3`: ستون (field) **سوم** | ‏`cut` خطا می‌دهد: باید بگویید کدام ستون |
| ③ | فایل؛ یا ورودی از لوله | — |

**جداکننده‌ی پیش‌فرض `cut`، Tab است**، درست همان جداکننده‌ی GFF. پس برای GFF گزینه‌ی دیگری لازم نیست.

### چند ستون، یا یک بازه

<div dir="ltr">

```bash
cut -f1,3,4,5,7 small.gff
```

</div>

<div dir="ltr">

```text
NC_000913.3	region	1	4641652	+
NC_000913.3	gene	190	255	+
NC_000913.3	CDS	190	255	+
NC_000913.3	gene	337	2799	+
NC_000913.3	CDS	337	2799	+
NC_000913.3	gene	2801	3733	+
NC_000913.3	CDS	2801	3733	+
NC_000913.3	gene	3734	5020	+
```

</div>

| نوشتن | یعنی |
| :--- | :--- |
| `-f1,3,7` | ستون‌های ۱، ۳ و ۷ (با ویرگول، بی فاصله) |
| `-f3-5` | ستون‌های ۳ **تا** ۵ |
| `-f4-` | ستون ۴ تا آخر |

**این خروجی یعنی:** خط یکم (`region`) کل کروموزوم است، از ۱ تا ۴٬۶۴۱٬۶۵۲. سپس هر ژن دو بار آمده: یک بار به‌عنوان `gene` و یک بار به‌عنوان `CDS` (بخشی که به پروتئین ترجمه می‌شود). همه روی رشته‌ی مثبت‌اند.

### بریدن نویسه‌ها: `-c`
‏`-c` به جای ستون، **نویسه**‌ها را می‌برد:

<div dir="ltr">

```bash
head -n 1 ecoli_k12.fna | cut -c1-12
```

</div>

<div dir="ltr">

```text
>NC_000913.3
```

</div>

یعنی «نویسه‌های ۱ تا ۱۲ خط عنوان»: شناسه‌ی ژنوم، بی توضیح‌های پس از آن.

### جداکننده‌ی دیگر: `-d`
اگر ستون‌ها با چیزی جز Tab جدا شده باشند (برای نمونه ویرگول در فایل CSV)، جداکننده را با `-d` بگویید: `cut -d',' -f2 file.csv`.

---

## ‏۴. `sort`: مرتب کردن

### مرتب کردن متن

<div dir="ltr">

```bash
cut -f3 small.gff | sort
```

</div>

<div dir="ltr">

```text
CDS
CDS
CDS
gene
gene
gene
gene
region
```

</div>

‏`sort` خط‌ها را **الفبایی** مرتب می‌کند، پس همانندها کنار هم می‌افتند.

### متن یا عدد؟ `-n`

ببینید با عددها چه می‌شود. آغاز (ستون ۴) ژن‌ها را مرتب می‌کنیم و ۳ تای نخست را می‌بینیم:

<div dir="ltr">

```bash
grep -P '\tgene\t' ecoli_k12.gff | cut -f4 | sort | head -n 3
grep -P '\tgene\t' ecoli_k12.gff | cut -f4 | sort -n | head -n 3
```

</div>

<div dir="ltr">

```text
1001807
1002889
1003439
190
337
2801
```

</div>

**این خروجی یعنی:** بی `-n`، `sort` عددها را **مانند واژه** می‌سنجد، حرف به حرف از چپ: `1001807` با `1` آغاز می‌شود و `190` هم با `1`، ولی حرف دوم `0` از `9` کوچک‌تر است، پس `1001807` جلوتر می‌افتد. با `-n` (*numeric*) عددها **به‌عنوان عدد** سنجیده می‌شوند و `190` (کوچک‌ترین آغاز) نخست می‌آید.

**قاعده: برای عددها همیشه `sort -n`.**

### گزینه‌های پرکاربرد

| گزینه | یعنی |
| :--- | :--- |
| `-n` | عددی |
| `-r` | وارونه (بزرگ به کوچک) |
| `-k2,2` | بر پایه‌ی ستون **۲** (k = *key*) |
| ‏`-nr` یا `-rn` | عددی و وارونه |
| `-k2,2nr` | بر پایه‌ی ستون ۲، عددی و وارونه |

### مرتب کردن بر پایه‌ی یک ستون

فایل `ground_truth.tsv` می‌گوید هر نمونه از چند جفت رید از هر ژنوم ساخته شده است. پرریدترین ژنوم‌ها کدام‌اند؟

<div dir="ltr">

```bash
sort -k2,2nr ground_truth.tsv | head -n 4
```

</div>

<div dir="ltr">

```text
minigut	28912	NC_006347.1	Bacteroides fragilis YCH46
minigut	21088	NC_000913.3	Escherichia coli K-12 MG1655
minigut_sample2	16154	CP009257.1	Acinetobacter baumannii strain AB030
minigut_sample2	1178	NC_002516.2	Pseudomonas aeruginosa PAO1
```

</div>

#### کالبدشکافی `sort -k2,2nr`

| تکه | یعنی |
| :--- | :--- |
| `-k2,2` | کلید مرتب‌سازی از ستون ۲ آغاز و **در همان ستون ۲** پایان می‌یابد (تنها ستون ۲) |
| `n` | عددی |
| `r` | بزرگ به کوچک |

‏**`head -n 4` پس از `sort`** یعنی «چهار تای بالای فهرست»: الگوی «بزرگ‌ترین‌ها» یا «top N».

---

## ‏۵. `uniq -c`: شمردن همانندها

<div dir="ltr">

```bash
cut -f3 small.gff | sort | uniq -c
```

</div>

<div dir="ltr">

```text
      3 CDS
      4 gene
      1 region
```

</div>

‏`uniq` خط‌های همانندِ **پشت سر هم** را یکی می‌کند، و با `-c` (*count*) شمارشان را پیش از هر کدام می‌نویسد. با چشم بسنجید: در ۸ خط، ۴ ژن، ۳ CDS و ۱ region بود. ✓

### چرا `sort` پیش از `uniq` لازم است؟

<div dir="ltr">

```bash
cut -f3 small.gff | uniq -c
```

</div>

<div dir="ltr">

```text
      1 region
      1 gene
      1 CDS
      1 gene
      1 CDS
      1 gene
      1 CDS
      1 gene
```

</div>

**هشت ردیف، همه با شمار ۱!** `uniq` تنها خط‌های همانندِ **کنار هم** را می‌بیند، و این‌جا هیچ دو خط همانندی کنار هم نیستند (gene و CDS یکی در میان‌اند). `sort` همانندها را کنار هم می‌گذارد. **`uniq` همیشه پس از `sort`.**

> 📺 **فیلم:** *Sorting & Filtering in Linux (sort, uniq)*: https://www.youtube.com/watch?v=p11n_ao982I
> 📄 **مرجع:** GNU Coreutils manual (`cut`، `sort`، `uniq`): https://www.gnu.org/software/coreutils/manual/coreutils.html

---

## ۶. الگوی طلایی، گام‌به‌گام روی کل فایل

<div dir="ltr">

```bash
grep -v '^#' ecoli_k12.gff | cut -f3 | sort | uniq -c | sort -rn
```

</div>

<div dir="ltr">

```text
   4506 gene
   4340 CDS
    216 exon
    145 pseudogene
    108 ncRNA
     86 tRNA
     50 mobile_genetic_element
     48 sequence_feature
     22 rRNA
      1 region
      1 origin_of_replication
```

</div>

### گام‌به‌گام

| گام | دستور | چه می‌ماند |
| :-: | :--- | :--- |
| ۱ | `grep -v '^#' ecoli_k12.gff` | ۹٬۵۲۳ خط داده (بی توضیح‌ها) |
| ۲ | `\| cut -f3` | تنها ستون نوع (۹٬۵۲۳ واژه) |
| ۳ | `\| sort` | همان واژه‌ها، الفبایی؛ همانندها کنار هم |
| ۴ | `\| uniq -c` | هر نوع یک بار، با شمارش |
| ۵ | `\| sort -rn` | پرشمارترین بالا |

**این خروجی یعنی:** ژنوم ۴٬۵۰۶ ژن، ۴٬۳۴۰ CDS، ۱۴۵ ژن کاذب، ۸۶ tRNA، ۲۲ rRNA، ۵۰ عنصر ژنتیکی متحرک، و یک «جایگاه آغاز همانندسازی» (`origin_of_replication`) دارد. یک دستور، یک نمای کلی از کل ژنوم.

‏`sort -rn` در گام ۵ عدد شمارش را (که اکنون در آغاز هر خط است) عددی و وارونه مرتب می‌کند.

### همان الگو، پرسشی دیگر: ژن‌ها روی کدام رشته‌اند؟

<div dir="ltr">

```bash
grep -P '\tgene\t' ecoli_k12.gff | cut -f7 | sort | uniq -c
```

</div>

<div dir="ltr">

```text
   2216 +
   2290 -
```

</div>

**۲٬۲۱۶ ژن روی رشته‌ی مثبت و ۲٬۲۹۰ روی رشته‌ی منفی**؛ نزدیک به نیمه‌نیمه. `grep` نخست تنها خط‌های ژن را نگه داشت؛ وگرنه رشته‌ی CDSها، tRNAها و… هم شمرده می‌شد و هر ژن دو بار (gene و CDS) حساب می‌شد.

<details>
<summary>✋ <b>امتحان کن:</b> نام نُه ژن rpo را (ماژول ۰۵، بخش ۵) به ترتیب الفبایی بنویسید.</summary>

<div dir="ltr">

```bash
grep -o -E 'Name=rpo[A-Z]+' ecoli_k12.gff | sort
```

</div>

پاسخ: `Name=rpoA`، `rpoB`، `rpoC`، `rpoD`، `rpoE`، `rpoH`، `rpoN`، `rpoS`، `rpoZ`.
</details>

> 📺 **فیلم:** *Exploratory data analysis in bash: Using cut, sort, and uniq to count things in messy files (CC023)*: https://www.youtube.com/watch?v=gPX7d3BcZpg (Riffomonas Project)
> 📄 **مرجع:** Software Carpentry, *The Unix Shell*, درس «Pipes and Filters»: https://swcarpentry.github.io/shell-novice/

---

## ۷. سه اشتباه رایج (با خروجی واقعی)

### اشتباه ۱: `uniq -c` بی `sort`
خروجی بخش ۵ را ببینید: ۸ ردیف با شمار ۱ به جای ۳ ردیف درست. پیام خطایی هم نمی‌آید.

### اشتباه ۲: `sort` بی `-n` روی عددها

<div dir="ltr">

```bash
cut -f2 ground_truth.tsv | sort | head -n 5
```

</div>

<div dir="ltr">

```text
113
1178
156
16154
174
```

</div>

`1178` پیش از `156`، و `16154` پیش از `174`! مرتب‌سازی متنی حرف به حرف از چپ می‌سنجد. با `sort -n` درست می‌شود. (خط عنوان ستون، `read_pairs`، هم در این ستون است؛ `sort -n` آن را مانند عدد صفر می‌بیند.)

### اشتباه ۳: `cut -d' '` روی فایل Tab‌دار
اگر جداکننده را فاصله بگویید (`-d' '`)، `cut` ستون‌های GFF را درست نمی‌یابد، چون ستون‌ها با Tab جدا شده‌اند و فاصله تنها درون ستون ۹ است. برای GFF، BED، VCF و `ground_truth.tsv`، **`-d` را ننویسید** (پیش‌فرض Tab است).

---

## ۸. جمع‌بندی

- ‏GFF جدولی ۹ ستونی با جداکننده‌ی Tab است: ۳ نوع، ۴ و ۵ آغاز و پایان، ۷ رشته، ۹ آگاهی‌های دیگر.
- ‏`cut -f` ستون‌ها را برمی‌دارد (`-f3`، `-f1,3`، `-f3-5`)؛ `-c` نویسه‌ها را؛ `-d` جداکننده‌ی دیگر.
- ‏`sort` الفبایی؛ `-n` عددی، `-r` وارونه، `-k2,2` بر پایه‌ی یک ستون.
- ‏`uniq -c` همانندهای کنار هم را می‌شمارد؛ پس **همیشه پس از `sort`**.
- الگوی طلایی: `cut -fN | sort | uniq -c | sort -rn`؛ و `sort … | head -n N` برای «N تای بالا».

---

## کارت دستورهای این درس

| می‌خواهم… | دستور |
| :--- | :--- |
| ستون ۳ | `cut -f3 file` |
| چند ستون | `cut -f1,4,5 file` |
| بازه‌ای از ستون‌ها | `cut -f3-5 file` |
| نویسه‌های ۱ تا ۱۲ | `cut -c1-12` |
| ستون دوم یک CSV | `cut -d',' -f2 file.csv` |
| مرتب‌سازی الفبایی | `sort` |
| مرتب‌سازی عددی، بزرگ به کوچک | `sort -rn` |
| بر پایه‌ی ستون ۲، عددی | `sort -k2,2n file` |
| از هر چیز چندتا | `cut -f3 file \| sort \| uniq -c \| sort -rn` |
| ۵ تای بالا | `… \| sort -rn \| head -n 5` |

---

<details>
<summary>📘 <b>برای کنجکاوها (اختیاری):</b> ترتیب الفبایی به زبان سیستم بستگی دارد</summary>

ترتیب «الفبایی» `sort` به **locale** (تنظیم زبان سیستم) بستگی دارد. در `en_US.UTF-8` (پیش‌فرض بیشتر Ubuntuها) بزرگی و کوچکی حروف در گام نخست نادیده گرفته می‌شود: `CDS exon gene Gene`. در locale ساده‌ی `C`، همه‌ی حروف بزرگ پیش از همه‌ی حروف کوچک می‌آیند: `CDS Gene exon gene`. اگر دو کامپیوتر ترتیب گوناگونی دادند، دلیلش همین است. برای ترتیب یکسان همه‌جا، `LC_ALL=C sort` بنویسید.

دو گزینه‌ی سودمند دیگر: `sort -u` همانندها را حذف می‌کند (مانند `sort | uniq`)، و `uniq -d` تنها خط‌هایی را نشان می‌دهد که **تکرار** شده‌اند.
</details>

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| ستون (field) | تکه‌ای از خط میان دو جداکننده؛ در GFF با Tab |
| جداکننده (delimiter) | نویسه‌ای که ستون‌ها را جدا می‌کند (Tab، ویرگول…) |
| مرتب‌سازی متنی / عددی | سنجش حرف به حرف از چپ / سنجش مقدار عددی (`-n`) |
| کلید مرتب‌سازی (`-k`) | ستونی که مرتب‌سازی بر پایه‌ی آن است |
| الگوی طلایی | ‏`cut \| sort \| uniq -c \| sort -rn` برای شمردن از هر چیز |

---

## منابع

### راهنما و درس
- ‏GNU Coreutils manual، بخش‌های `cut`، `sort` و `uniq`: https://www.gnu.org/software/coreutils/manual/coreutils.html
- ‏GFF3 specification (تعریف رسمی ستون‌ها): https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md
- ‏Software Carpentry — *The Unix Shell*، درس «Pipes and Filters»: https://swcarpentry.github.io/shell-novice/

### کتاب
- ‏Shotts W (2019). *The Linux Command Line*, 2nd ed. No Starch Press. (فصل ۲۰: پردازش متن)
- ‏Buffalo V (2015). *Bioinformatics Data Skills*. O'Reilly. (فصل ۷: ابزارهای داده در یونیکس)

### فیلم‌های آموزشی

**Coursera:**
- Johns Hopkins University — *Command Line Tools for Genomic Data Science*: https://www.coursera.org/learn/genomic-tools

**edX:**
- ‏IBM — *Linux Commands & Shell Scripting*، بخش لوله‌ها و فیلترها: https://www.edx.org/learn/linux/ibm-linux-commands-shell-scripting

**YouTube:**
- Bioinformatics Coach — *Linux Tutorial for Bioinformatics 101, Episode 1*: https://www.youtube.com/watch?v=zvXe3udfg_I

> **وارسی نشانی‌ها (2026-10-20):** راهنماها، درس‌ها و edX با درخواست مستقیم وارسی شدند. Coursera (خطای 451) و YouTube (فیلترشده) از سرور دوره باز نمی‌شوند؛ نشانی Coursera با موتور جستجو در 2026-10-19 و ویدیو آخرین بار در 2026-10-13 وارسی شد. همه‌ی دستورها در 2026-10-20 با GNU coreutils و GNU grep 3.11 و locale `en_US.UTF-8` اجرا شدند.

</div>
