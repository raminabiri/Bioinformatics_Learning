<div dir="rtl">

# درس: بسته‌های R؛ از کجا می‌آیند، چطور نصب و وارسی می‌شوند

**بخش:** `04_R_Packages` · **ماژول:** `01_Install_Packages` · **پیش‌نیاز:** بخش‌های [لینوکس](../../01_Linux/)، [بایولینوکس](../../02_BioLinux/) (به‌ویژه ماژول Conda) و [پایتون](../../03_Python/) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** R 4.6.1، BiocManager 1.30.27 (Bioconductor 3.23) · **آخرین اجرا:** 2026-10-20

> ⚠️ **این بخش زبان R و آمار را درس نمی‌دهد.** آن‌ها موضوع یک دوره‌ی جداگانه‌اند. این‌جا تنها یاد می‌گیرید **بسته‌های آماده‌ی R را که در بیوانفورماتیک به کار می‌روند نصب و اجرا کنید**؛ همان‌گونه که `fastp` یا `samtools` را اجرا می‌کنید، بی‌آنکه زبان C بلد باشید.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. با `Rscript -e` یک دستور کوتاه R را از ترمینال اجرا کنید.
2. وارسی کنید که یک بسته‌ی R نصب است یا نه، و کدام نسخه‌اش.
3. فرق **CRAN** و **Bioconductor** را بگویید و بدانید هر بسته از کدام می‌آید.
4. بسته‌ها را از دو راه نصب کنید: با **conda** (راه پیشنهادی دوره) یا از درون R (`install.packages` و `BiocManager::install`).
5. سه خطای رایج نصب را بشناسید و درست کنید.

**پیش از آغاز:** محیط R دوره را یک بار بسازید (R خودش به‌عنوان وابستگی می‌آید؛ نصب جداگانه‌ی R یا RStudio لازم نیست):

<div dir="ltr">

```bash
cd ~/Bioinformatics_Learning-main
conda env create -f envs/r_packages.yml     # once; downloads a few hundred MB
conda activate r_packages
P=~/Bioinformatics_Learning-main/04_R_Packages/99_scripts_data
```

</div>

---

## ۱. داستان: «تحلیل بیان افتراقی با DESeq2 انجام شد»

در بخش روش‌های بسیاری از مقاله‌های میکروب‌شناسی جمله‌هایی مانند این‌ها را می‌بینید:

> «تفاوت بیان ژن‌ها با **DESeq2** سنجیده شد… تنوع آلفا و بتا با بسته‌ی **vegan** محاسبه شد… درخت با **ggtree** رسم شد.»

هر سه **بسته‌ی R**‌اند. بیشتر ابزارهای آماری بیوانفورماتیک، به‌ویژه برای RNA-seq و میکروبیوم، تنها به شکل بسته‌ی R نوشته شده‌اند. پس اگر R بلد نیستید هم باید بتوانید آن‌ها را **نصب** کنید، **اجرا** کنید و **خروجی‌شان را بخوانید**. این بخش همین را یاد می‌دهد.

---

## ۲. مفهوم به زبان ساده: گوشی و برنامه‌ها

یک تشبیه:

| در گوشی | در R |
| :--- | :--- |
| خود گوشی | ‏**R**: موتوری که دستورها را اجرا می‌کند |
| برنامه (اپ) | **بسته** (*package*): مجموعه‌ای از دستورهای آماده برای یک کار، مانند DESeq2 |
| فروشگاه همگانی برنامه‌ها | ‏**CRAN**: فروشگاه همگانی بسته‌های R (بیش از ۲۰ هزار بسته؛ vegan، ggplot2، ape) |
| فروشگاه تخصصی | ‏**Bioconductor**: فروشگاه ویژه‌ی زیست‌شناسی (DESeq2، edgeR، ggtree، phyloseq) |
| نسخه‌ی سیستم‌عامل گوشی | **نسخه‌ی R**: هر نسخه‌ی Bioconductor تنها با یک نسخه‌ی معین R جور است |

دو نکته از همین تشبیه بیرون می‌آید:
- برنامه را **یک بار نصب** می‌کنید، ولی **هر بار که می‌خواهید به کار ببرید باز می‌کنید**. در R نصب با `install.packages` (یا conda) است و باز کردن با `library(نام)`.
- برنامه‌ی فروشگاه تخصصی را از فروشگاه همگانی نمی‌توانید بگیرید: بسته‌ی Bioconductor با `install.packages` نصب **نمی‌شود** (بخش ۵).

---

## ۳. نخستین دستورهای R از ترمینال: `Rscript -e`

‏R را سه جور می‌توان اجرا کرد:

| راه | کِی |
| :--- | :--- |
| ‏`Rscript -e 'دستور'` | یک دستور کوتاه، مانند وارسی نسخه (همین درس) |
| ‏`Rscript script.R ورودی خروجی` | اجرای یک **اسکریپت آماده** (ماژول ۰۲) |
| ‏`R` (پنجره‌ی تعاملی) | کار گام‌به‌گام؛ با `q()` بیرون بیایید. در این بخش به آن نیاز نداریم |

‏`Rscript` برای R همان کاری را می‌کند که `python3` برای پایتون.

<div dir="ltr">

```bash
Rscript --version
Rscript -e '1 + 1'
Rscript -e 'R.version.string'
```

</div>

<div dir="ltr">

```text
Rscript (R) version 4.6.1 (2026-06-24)
[1] 2
[1] "R version 4.6.1 (2026-06-24)"
```

</div>

دستور دوم را تکه‌تکه ببینیم:

| تکه | یعنی | اگر نباشد |
| :--- | :--- | :--- |
| `Rscript` | برنامه‌ی اجرای R در ترمینال | — |
| `-e` | «دستور (*expression*) همین‌جاست، نه در یک فایل» | ‏Rscript دنبال فایلی به نام `1 + 1` می‌گردد |
| `'1 + 1'` | خود دستور R، درون **تک‌کوتیشن** | ‏Bash فاصله‌ها را می‌شکند و R تنها `1` را می‌گیرد |
| ‏`[1]` در خروجی | «نخستین عنصر پاسخ»؛ R همیشه این را پیش از پاسخ می‌گذارد | — |

**تنها قاعده‌ی زبان R که در این بخش لازم است:** یک دستور R بیشتر وقت‌ها به شکل `نام(ورودی)` است، همان شکلی که در پایتون دیدید: `sqrt(16)`، `packageVersion("DESeq2")`. متن (نام بسته، نام فایل) درون **دوکوتیشن** `"…"` می‌آید.

### چرا بیرون تک‌کوتیشن و درون دوکوتیشن؟

اگر بیرون هم دوکوتیشن بگذارید، Bash دوکوتیشن‌های درونی را می‌خورد:

<div dir="ltr">

```bash
Rscript -e 'cat("hi\n")'      # right
Rscript -e "cat("hi\n")"      # wrong
```

</div>

<div dir="ltr">

```text
hi
Error: object 'hin' not found
Execution halted
```

</div>

در دستور دوم، Bash کوتیشن‌ها را جفت‌جفت برداشت و به R تنها `cat(hin)` رسید (`\n` هم به `n` تبدیل شد). R دنبال چیزی به نام `hin` گشت و نیافت. **قاعده: بیرون `'…'`، درون `"…"`.**

<details>
<summary>✋ امتحان کن: <code>Rscript -e 'sqrt(81)'</code> چه چاپ می‌کند؟ و <code>Rscript -e sqrt(81)</code> بی‌کوتیشن؟</summary>

یکمی `[1] 9` (جذر ۸۱). دومی را Bash پیش از R می‌خواند و پرانتز برایش معنای ویژه دارد، پس پیش از رسیدن به R خطای Bash می‌گیرید (`syntax error near unexpected token '('`). همیشه دستور `-e` را در `'…'` بگذارید.

</details>

---

## ۴. آیا این بسته نصب است؟ کدام نسخه؟

### یک بسته

<div dir="ltr">

```bash
Rscript -e 'packageVersion("DESeq2")'
```

</div>

<div dir="ltr">

```text
[1] ‘1.52.0’
```

</div>

‏`packageVersion("نام")` نسخه‌ی نصب‌شده را می‌گوید. اگر بسته نصب نباشد:

<div dir="ltr">

```bash
Rscript -e 'packageVersion("deseq2")'
```

</div>

<div dir="ltr">

```text
Error in packageVersion("deseq2") : there is no package called ‘deseq2’
Execution halted
```

</div>

بسته نصب است! ولی نام بسته‌ها در R **به بزرگی و کوچکی حرف حساس** است: `DESeq2` درست است، `deseq2` نه. پیام `there is no package called` را بسیار خواهید دید؛ نخستین کار همیشه این است که **املای نام** را با صفحه‌ی بسته وارسی کنید.

‏`Execution halted` یعنی «اجرا به خاطر خطا متوقف شد». هر جا این را دیدید، خط بالایش (`Error …`) علت است.

### چند بسته با یک اسکریپت آماده

برای وارسی همه‌ی بسته‌های این بخش، اسکریپت `check_packages.R` آماده است:

<div dir="ltr">

```bash
Rscript $P/01_Install_Packages/scripts/check_packages.R
```

</div>

<div dir="ltr">

```text
R: R version 4.6.1 (2026-06-24) 
BiocManager  1.30.27
ggplot2      4.0.3
vegan        2.7.6
ape          5.8.1
DESeq2       1.52.0
ggtree       4.2.0
```

</div>

می‌توانید نام بسته‌ها را هم خودتان بدهید (هر چند تا که بخواهید، با فاصله):

<div dir="ltr">

```bash
Rscript $P/01_Install_Packages/scripts/check_packages.R vegan phyloseq
```

</div>

<div dir="ltr">

```text
R: R version 4.6.1 (2026-06-24) 
vegan        2.7.6
phyloseq     NOT installed
```

</div>

‏phyloseq نصب نیست؛ در بخش ۰۶ اگر لازم شد، با روش بخش ۵ نصبش می‌کنید.

### بسته‌ها کجا نصب می‌شوند؟

<div dir="ltr">

```bash
Rscript -e '.libPaths()'
```

</div>

<div dir="ltr">

```text
[1] "/home/ubuntu/R/x86_64-pc-linux-gnu-library/4.6"
[2] "/usr/local/lib/R/site-library"                 
[3] "/usr/lib/R/site-library"                       
[4] "/usr/lib/R/library"                            
```

</div>

این‌ها **کتابخانه‌ها** (*library*)‌یند: پوشه‌هایی که R به ترتیب در آن‌ها دنبال بسته می‌گردد. خروجی بالا از R نصب‌شده روی خود سیستم است. در محیط conda، مسیرها درون پوشه‌ی محیط‌اند (مانند `~/miniforge3/envs/r_packages/lib/R/library`). **همین که بدانید کدام R را اجرا می‌کنید مهم است:**

<div dir="ltr">

```bash
which Rscript
```

</div>

اگر `conda activate r_packages` کرده باشید، پاسخ مسیری درون `envs/r_packages` است؛ اگر نه، `/usr/bin/Rscript` (R سیستم) است، با بسته‌های دیگر (اشتباه ۳).

<details>
<summary>✋ امتحان کن: نسخه‌ی <code>ggplot2</code> و <code>ape</code> را با یک دستور <code>Rscript -e</code> بگیرید.</summary>

<div dir="ltr">

```bash
Rscript -e 'packageVersion("ggplot2"); packageVersion("ape")'
```

</div>

<div dir="ltr">

```text
[1] ‘4.0.3’
[1] ‘5.8.1’
```

</div>

‏`;` دو دستور R را در یک خط جدا می‌کند. راه دیگر: `Rscript $P/01_Install_Packages/scripts/check_packages.R ggplot2 ape`.

</details>

---

## ۵. نصب بسته: دو راه

### راه ۱ (پیشنهادی دوره): conda

در ماژول Conda بخش ۰۲ دیدید که conda برنامه‌ها را با همه‌ی وابستگی‌هایشان در یک **محیط** جدا نصب می‌کند. بسته‌های R هم در conda هستند، با یک قاعده‌ی نام‌گذاری:

| بسته از | نام در conda | کانال | نمونه |
| :--- | :--- | :--- | :--- |
| CRAN | ‏`r-` + نام با حروف کوچک | conda-forge | ‏vegan ← `r-vegan`، ggplot2 ← `r-ggplot2` |
| Bioconductor | ‏`bioconductor-` + نام با حروف کوچک | bioconda | ‏DESeq2 ← `bioconductor-deseq2`، ggtree ← `bioconductor-ggtree` |

نصب یک بسته در محیط فعال:

<div dir="ltr">

```bash
conda install -c conda-forge -c bioconda bioconductor-phyloseq
```

</div>

فایل `envs/r_packages.yml` همین قاعده را دنبال می‌کند:

<div dir="ltr">

```yaml
name: r_packages
channels:
  - conda-forge
  - bioconda
dependencies:
  - r-base=4.5
  - r-biocmanager
  - r-ggplot2>=4.0
  - r-vegan>=2.7
  - r-ape>=5.8
  - bioconductor-deseq2>=1.50
  - bioconductor-ggtree>=4.0
```

</div>

| خط | یعنی |
| :--- | :--- |
| `r-base=4.5` | خود R، نسخه‌ی 4.5. این تنها جایی است که «R نصب می‌شود»؛ خودکار |
| `r-biocmanager` | نصب‌کننده‌ی Bioconductor (راه ۲) |
| ‏`>=4.0` | «دست‌کم این نسخه» |

**چرا `>=`؟ یک تجربه‌ی واقعی:** همین فایل را یک بار **بدون** `>=` آزمودیم (`--dry-run` یعنی «تنها نشان بده چه نصب می‌شود، نصب نکن»):

<div dir="ltr">

```bash
conda env create --dry-run -f r_try.yml
```

</div>

<div dir="ltr">

```text
  bioconductor-deseq2 bioconda/linux-64::bioconductor-deseq2-1.50.2-r45ha27e39d_0
  bioconductor-ggtree bioconda/linux-64::bioconductor-ggtree-1.2.12-0
  r-ape               conda-forge/linux-64::r-ape-5.8_1-r45h3704496_2
  r-base              conda-forge/linux-64::r-base-4.5.3-h502d0c9_3
```

</div>

‏conda برای ggtree نسخه‌ی **1.2.12** را برگزید، نسخه‌ای از نزدیک به ده سال پیش، چون آن نسخه‌ی کهنه با بقیه بی‌دردسرتر جور می‌شد. اسکریپت ggtree ماژول ۰۳ با آن اجرا نمی‌شود. **درس: برای بسته‌های R در conda کمینه‌ی نسخه را بنویسید.**

> 📝 در تاریخ 2026-10-20 بسته‌های Bioconductor در bioconda کمی **عقب‌تر** از خود Bioconductor‌اند (DESeq2 1.50.2 در bioconda، در برابر 1.52.0 در Bioconductor 3.23). برای کار این دوره فرقی نمی‌کند؛ ولی شاید رقم‌های پایانی خروجی‌ها کمی با درس فرق کند.

### راه ۲: از درون R

اگر conda در دسترس نیست (برای نمونه روی سرور دانشگاه که R از پیش نصب است)، از خود R نصب می‌کنید.

**بسته‌ی CRAN با `install.packages`:**

<div dir="ltr">

```bash
Rscript -e 'install.packages("permute", repos = "https://cran.r-project.org")'
```

</div>

<div dir="ltr">

```text
trying URL 'https://cran.r-project.org/src/contrib/permute_0.9-10.tar.gz'
Content type 'application/x-gzip' length 120438 bytes (117 KB)
==================================================
downloaded 117 KB

* installing *source* package ‘permute’ ...
** this is package ‘permute’ version ‘0.9-10’
...
** testing if installed package can be loaded from final location
* DONE (permute)
```

</div>

- ‏`repos = "…"`: از کدام نشانی CRAN بگیرد. اگر نگذارید، R در پنجره‌ی تعاملی از شما می‌پرسد و در `Rscript` خطا می‌دهد: `trying to use CRAN without setting a mirror`.
- ‏`*source* package`: بسته از **کد منبع** ساخته شد. بسته‌های بزرگ‌تر با کد C یا Fortran چند دقیقه کامپایل می‌شوند.
- ‏`* DONE (permute)`: نصب درست انجام شد. **همیشه دنبال این خط بگردید.** اگر به جایش `ERROR: compilation failed` آمد، کادر کنجکاوها را ببینید.

**بسته‌ی Bioconductor با `BiocManager::install`:**

<div dir="ltr">

```bash
Rscript -e 'BiocManager::install("DESeq2", update = FALSE)'
```

</div>

<div dir="ltr">

```text
Bioconductor version 3.23 (BiocManager 1.30.27), R 4.6.1 (2026-06-24)
Warning message:
package(s) not installed when version(s) same as or greater than current; use
  `force = TRUE` to re-install: 'DESeq2' 
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `BiocManager::install` | تابع `install` از بسته‌ی `BiocManager`. نشانه‌ی `::` یعنی «این تابع از آن بسته»، بی‌آنکه بسته را با `library` باز کنید |
| `update = FALSE` | بسته‌های دیگرِ نصب‌شده را به‌روز نکن (وگرنه می‌پرسد و شاید ده‌ها بسته را به‌روز کند) |
| ‏خط `Bioconductor version 3.23 … R 4.6.1` | ‏BiocManager نسخه‌ی Bioconductor را **از روی نسخه‌ی R** برمی‌گزیند |
| `Warning … not installed` | ‏DESeq2 پیش‌تر نصب بود، پس کاری نکرد. این **هشدار** است، نه خطا |

جفت شدن نسخه‌ها را این‌گونه ببینید:

<div dir="ltr">

```bash
Rscript -e 'BiocManager::version()'
```

</div>

<div dir="ltr">

```text
[1] ‘3.23’
```

</div>

‏Bioconductor سالی دو بار (بهار و پاییز) نسخه‌ی تازه می‌دهد و هر نسخه تنها برای یک نسخه‌ی R است. به همین خاطر **بسته‌های Bioconductor را باید با BiocManager نصب کرد**، نه با `install.packages`:

<div dir="ltr">

```bash
Rscript -e 'install.packages("DESeq2", repos = "https://cran.r-project.org")'
```

</div>

<div dir="ltr">

```text
Warning message:
package ‘DESeq2’ is not available for this version of R

A version of this package for your version of R might be available elsewhere,
see the ideas at
https://cran.r-project.org/doc/manuals/r-patched/R-admin.html#Installing-packages 
```

</div>

پیام گمراه‌کننده است: «برای این نسخه‌ی R نیست». درستش این است: «**در CRAN** نیست؛ در Bioconductor است.»

### از کجا بفهمم بسته در CRAN است یا Bioconductor؟

نام بسته را جست‌وجو کنید:
- صفحه‌ای در `bioconductor.org/packages/…` ← Bioconductor ← `BiocManager::install` یا `bioconductor-…` در conda.
- صفحه‌ای در `cran.r-project.org/package=…` ← CRAN ← `install.packages` یا `r-…` در conda.

صفحه‌ی هر بسته‌ی Bioconductor یک بخش **Installation** دارد که دستور نصب را دقیقاً می‌نویسد، و یک **vignette** (راهنمای گام‌به‌گام) که نمونه‌ی اجرا دارد.

<details>
<summary>✋ امتحان کن: نام conda بسته‌های <code>edgeR</code> (Bioconductor) و <code>pheatmap</code> (CRAN) چیست؟</summary>

‏`bioconductor-edger` (کانال bioconda) و `r-pheatmap` (کانال conda-forge). هر دو با حروف کوچک.

</details>

### باز کردن بسته: `library`

پس از نصب، بسته را با `library(نام)` باز می‌کنید. بسته‌های بزرگ Bioconductor هنگام باز شدن پیام‌های بسیاری چاپ می‌کنند:

<div dir="ltr">

```bash
Rscript -e 'library(DESeq2)'
```

</div>

<div dir="ltr">

```text
Loading required package: S4Vectors
Loading required package: stats4
Loading required package: BiocGenerics
Loading required package: generics

Attaching package: ‘generics’

The following objects are masked from ‘package:base’:
...
```

</div>

‏(۸۴ خط پیام.) این‌ها **خطا نیستند**: می‌گویند DESeq2 چه بسته‌های دیگری را با خود باز کرد. **تنها خطی که با `Error` آغاز شود خطاست.** اسکریپت‌های آماده‌ی این بخش این پیام‌ها را با `suppressPackageStartupMessages` خاموش می‌کنند تا خروجی خوانا بماند.

> 📺 **فیلم:** *How to install bioconductor packages in R*: https://www.youtube.com/watch?v=wWib2La9oc0 · *Download Bioconductor (BiocManager installer) & Get Started*: https://www.youtube.com/watch?v=RZMFgHRhGck
> 📄 **مرجع:** Bioconductor, *Installing Bioconductor*: https://bioconductor.org/install/

---

## ۶. سه اشتباه رایج

**۱. نصب بسته‌ی Bioconductor با `install.packages`.**
پیام: `package ‘DESeq2’ is not available for this version of R`. راه درست: `BiocManager::install("DESeq2")` یا `conda install bioconductor-deseq2`.

**۲. املای نادرست نام بسته.**
پیام: `there is no package called ‘deseq2’`. نام‌ها به بزرگی و کوچکی حرف حساس‌اند: `DESeq2`، `edgeR`، `ggtree`، `phyloseq`. (در conda همه کوچک‌اند؛ در R همان املای اصلی.)

**۳. اجرای R نادرست.**
بسته را در محیط `r_packages` نصب کرده‌اید، ولی پیش از اجرا `conda activate r_packages` را فراموش کرده‌اید. پس `Rscript` به R سیستم اشاره می‌کند که آن بسته را ندارد و همان پیام `there is no package called` می‌آید. وارسی: `which Rscript`.

---

## 📘 برای کنجکاوها

- **کامپایل نشد (`ERROR: compilation failed`):** برخی بسته‌ها هنگام نصب از منبع، کتابخانه‌های سیستمی لینوکس می‌خواهند (مانند `libxml2-dev` یا `libcurl4-openssl-dev`). پیام خطا نام فایل گمشده را می‌گوید (`xml2-config: not found`). conda این مشکل را ندارد، چون بسته‌ها را **از پیش ساخته** (باینری) می‌آورد. این یکی از دلیل‌های پیشنهاد conda است.
- ‏**‏r2u / bspm:** روی برخی سرورهای Ubuntu، مدیر سیستم ابزار bspm را روشن کرده است. در این حالت `install.packages` خودش بسته را از مخزن Ubuntu (نسخه‌ی باینری `r-cran-…`) نصب می‌کند و خروجی‌اش به‌جای `* DONE` خط‌های `apt` است. نتیجه همان است.
- ‏**‏renv:** برای ثبت دقیق نسخه‌ی همه‌ی بسته‌های یک پروژه، ابزاری به نام renv هست. در این دوره فایل `envs/r_packages.yml` همین کار را می‌کند.

---

## جمع‌بندی

- بسته‌ی R = برنامه‌ای آماده درون R. از دو فروشگاه می‌آید: **CRAN** (همگانی) و **Bioconductor** (زیستی، با نسخه‌ی جفت‌شده با R).
- ‏`Rscript -e '…'` یک دستور کوتاه R را از ترمینال اجرا می‌کند: بیرون `'…'`، درون `"…"`.
- وارسی: `packageVersion("نام")` یا `check_packages.R`. نام‌ها به بزرگی و کوچکی حرف حساس‌اند.
- نصب: در conda با `r-نام` و `bioconductor-نام` (کمینه‌ی نسخه را بنویسید)؛ یا در R با `install.packages` (CRAN) و `BiocManager::install` (Bioconductor).
- پیام‌های بارگذاری و `Warning` خطا نیستند؛ تنها `Error` و `Execution halted` نشانه‌ی شکست‌اند.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
Rscript --version                                   # which R version?
which Rscript                                       # which R (conda env or system)?
Rscript -e 'packageVersion("DESeq2")'               # is it installed? which version?
Rscript check_packages.R vegan phyloseq             # several packages at once
Rscript -e '.libPaths()'                            # where packages are installed
conda install -c conda-forge -c bioconda "bioconductor-deseq2>=1.50" "r-vegan>=2.7"
Rscript -e 'install.packages("vegan", repos = "https://cran.r-project.org")'   # CRAN
Rscript -e 'BiocManager::install("DESeq2", update = FALSE)'                    # Bioconductor
Rscript -e 'BiocManager::version()'                 # Bioconductor version for this R
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| بسته (*package*) | مجموعه‌ای از دستورهای آماده‌ی R برای یک کار |
| ‏CRAN | مخزن همگانی بسته‌های R |
| ‏Bioconductor | مخزن بسته‌های R برای داده‌های زیستی؛ دو انتشار در سال |
| ‏BiocManager | بسته‌ای که بسته‌های Bioconductor را با نسخه‌ی درست نصب می‌کند |
| کتابخانه (*library*) | پوشه‌ای که بسته‌های نصب‌شده در آن‌اند؛ `.libPaths()` |
| ‏`library(نام)` | باز کردن یک بسته‌ی نصب‌شده برای به‌کارگیری |
| ‏`::` | گرفتن یک تابع از یک بسته، بی‌آنکه بسته باز شود |
| ‏vignette | راهنمای گام‌به‌گام یک بسته، با نمونه‌ی اجرا |
| ‏Rscript | برنامه‌ی اجرای R از ترمینال |

---

## منابع

**مستند رسمی**
- Bioconductor, *Installing Bioconductor*: https://bioconductor.org/install/
- BiocManager vignette: https://cran.r-project.org/web/packages/BiocManager/vignettes/BiocManager.html
- ‏Bioconda, *Using Bioconda* (نام‌گذاری `bioconductor-…`): https://bioconda.github.io/
- ‏R Core Team, *R Installation and Administration*، بخش Add-on packages: https://cran.r-project.org/doc/manuals/r-release/R-admin.html#Add_002don-packages

**کتاب**
- ‏Gentleman R (2008). *R Programming for Bioinformatics*. CRC Press. (فصل بسته‌ها و Bioconductor)
- Wickham H, Çetinkaya-Rundel M, Grolemund G (2023). *R for Data Science*, 2nd ed. O'Reilly.

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Bioconductor for Genomic Data Science* (Johns Hopkins University، هفته‌ی ۱: نصب Bioconductor): https://www.coursera.org/learn/bioconductor
- edX: *Introduction to Bioconductor* (HarvardX PH525.5x): https://www.edx.org/learn/data-science/harvard-university-introduction-to-bioconductor
- YouTube: *Download Bioconductor (BiocManager installer) & Get Started* (Saniya Khullar): https://www.youtube.com/watch?v=RZMFgHRhGck
- YouTube: *How to install bioconductor packages in R* (Hong Qin): https://www.youtube.com/watch?v=wWib2La9oc0

<sub>نشانی‌های YouTube در 2026-10-20 با oEmbed وارسی شدند (همگانی و در دسترس). نشانی‌های Coursera و edX از نمایه‌ی جست‌وجو در همان تاریخ گرفته شدند؛ وارسی مستقیم آن‌ها در پایان دوره انجام می‌شود.</sub>

</div>
