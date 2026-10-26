<div dir="rtl">

# درس: نصب ابزارهای زیستی با Conda و Bioconda

**بخش:** `02_BioLinux` · **ماژول:** `01_Conda_Bioconda` · **پیش‌نیاز:** بخش [لینوکس](../../01_Linux/) (به‌ویژه ماژول [اسکریپت](../../01_Linux/10_Scripts/)) · **زمان:** حدود ۷۵ دقیقه · **ابزار:** conda 26.7 (Miniforge) · **آخرین اجرا:** 2026-10-20

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. بگویید چرا ابزارهای بیوانفورماتیک را با Conda نصب می‌کنیم و «محیط» چیست.
2. ‏Miniforge را نصب و کانال‌های conda-forge و bioconda را تنظیم کنید.
3. یک محیط را از یک **فایل YAML** بسازید، فعال کنید و بسنجید که ابزار از کجا اجرا می‌شود.
4. نسخه‌ی ابزارهای یک محیط را برای گزارش (Methods) ثبت کنید.
5. محیط کامل این دوره (`bioinfo_course`) را بسازید.

---

## ۱. داستان: «روی کامپیوتر من کار می‌کرد!»

در بخش لینوکس تنها ابزارهایی را به کار بردیم که در هر لینوکسی هستند (`grep`، `awk`…). از این‌جا به بعد ابزارهای **ویژه‌ی بیوانفورماتیک** لازم داریم: `seqkit` برای توالی‌ها، `samtools` برای فایل‌های هم‌ترازی، و ده‌ها ابزار دیگر. سه دردسر پیش می‌آید:

1. **نصب:** بسیاری از این ابزارها با `apt` نصب نمی‌شوند یا نسخه‌ی کهنه دارند، و ساختن‌شان از کد منبع کار متخصص است.
2. **تعارض:** ابزار A پایتون ۳٫۸ می‌خواهد و ابزار B پایتون ۳٫۱۳. نمی‌شود هر دو را در یک جا داشت.
3. **دوباره‌پذیری:** شش ماه بعد، یا روی کامپیوتر داور مقاله، باید **همان نسخه‌ها** نصب شوند. «با samtools تحلیل شد» کافی نیست؛ باید «samtools 1.20» باشد.

‏**Conda** هر سه را حل می‌کند. **Bioconda** «فروشگاه» ویژه‌ی آن برای ابزارهای زیستی است، با هزاران بسته.

---

## ۲. مفهوم‌ها با یک تشبیه

یک **آزمایشگاه** را تصور کنید با چند **میز کار** جداگانه. روی هر میز، تنها مواد و دستگاه‌های یک آزمایش است، با نسخه و غلظت معین. اگر روی یک میز ماده‌ای عوض شود، میزهای دیگر دست نمی‌خورند.

| مفهوم | در آزمایشگاه | در Conda |
| :--- | :--- | :--- |
| **بسته** (package) | یک ماده یا دستگاه، با شماره‌ی بچ | یک ابزار یا کتابخانه، با نسخه (برای نمونه `seqkit 2.13.0`) |
| **کانال** (channel) | شرکت فروشنده | مخزن بسته‌ها: `conda-forge` (عمومی) و `bioconda` (زیستی) |
| **محیط** (environment) | یک میز کار جدا | یک پوشه‌ی جدا با بسته‌های خودش؛ هر پروژه یا گروه ابزار یک محیط |
| **فعال کردن** (activate) | رفتن پشت یک میز | ‏`conda activate نام`: از این پس، ابزارهای همین محیط به کار می‌روند |
| **فایل محیط** (YAML) | فهرست مواد آزمایش | فایل متنی که می‌گوید محیط چه بسته‌هایی با چه نسخه‌ای دارد |

---

## ۳. نصب Miniforge (یک بار)

‏**Miniforge** نسخه‌ی سبک و رایگان Conda است که به‌طور پیش‌فرض از کانال `conda-forge` بسته می‌گیرد. دستورها از راهنمای رسمی Miniforge‌اند:

<div dir="ltr">

```bash
cd ~
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh -b -p ~/miniforge3
~/miniforge3/bin/conda init bash
```

</div>

### کالبدشکافی

| دستور | کار |
| :--- | :--- |
| `curl -L -O "…"` | فایل نصب را دانلود کن (`-O`: با همان نام فایل در نشانی؛ نزدیک به ۹۰ مگابایت) |
| ‏`$(uname)` و `$(uname -m)` | جایگزینی دستور (ماژول ۰۹ لینوکس): نام سیستم‌عامل (`Linux`) و نوع پردازنده (`x86_64`)، تا فایل درست دانلود شود |
| `bash Miniforge3-….sh -b -p ~/miniforge3` | نصب‌کننده را اجرا کن؛ `-b` بی پرسش، `-p` جای نصب |
| `conda init bash` | تنظیم Bash تا `conda` همیشه در دسترس باشد |

**پس از `conda init`، ترمینال را ببندید و دوباره باز کنید.** اعلان شما اکنون با `(base)` آغاز می‌شود: نام محیط فعال.

<div dir="ltr">

```bash
conda --version
```

</div>

<div dir="ltr">

```text
conda 26.7.2
```

</div>

(نسخه‌ی شما ممکن است تازه‌تر باشد.)

### تنظیم کانال‌ها

<div dir="ltr">

```bash
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `--add channels X` | کانال X را به **بالای** فهرست بیفزا. پس کانالی که **آخر** افزوده شود (conda-forge) بالاترین اولویت را دارد |
| `channel_priority strict` | اگر بسته‌ای در کانال بالاتر هست، از کانال پایین‌تر برداشته نشود؛ جلوی ترکیب کتابخانه‌های ناسازگار را می‌گیرد |

این همان تنظیمی است که راهنمای رسمی Bioconda می‌گوید.

⚠️ **اگر `conda` نمی‌تواند به مخزن وصل شود** (خطاهایی مانند `Could not resolve host: conda.anaconda.org` یا `SSL connect error`)، دسترسی شبکه به مخزن بسته است. روی سرور همین دوره در ۲۰۲۶ چنین شد. راه‌ها: آینه‌ی (mirror) محلی دانشگاه، یا اینترنت دیگری. بخش «کنجکاوها» را ببینید.

> 📺 **فیلم:** *Demystifying Conda (Anaconda, Miniconda and Bioconda) and Virtual Environments*: https://www.youtube.com/watch?v=2bXGm0ZnJ38 (Bioinformagician)
> 📄 **مرجع:** Miniforge: https://github.com/conda-forge/miniforge

---

## ۴. نخستین محیط، از یک فایل

روش دوباره‌پذیر این است که محیط را از یک **فایل YAML** بسازید. فایل `demo_env.yml` را با `nano` بنویسید:

<div dir="ltr">

```yaml
name: course_demo
channels:
  - conda-forge
  - bioconda
dependencies:
  - seqkit=2.13.0
  - jq
```

</div>

### کالبدشکافی فایل YAML

| خط | یعنی |
| :--- | :--- |
| `name: course_demo` | نام محیط |
| `channels:` | فهرست کانال‌ها، به ترتیب اولویت. هر ردیف فهرست با `- ` (خط تیره و فاصله) آغاز می‌شود |
| `dependencies:` | فهرست بسته‌ها |
| `- seqkit=2.13.0` | ‏`seqkit` **دقیقاً** با نسخه‌ی 2.13.0 (یک `=`) |
| `- jq` | ‏`jq` با هر نسخه‌ای که سازگار باشد |

**فرورفتگی (فاصله‌ی آغاز خط) در YAML معنا دارد.** ردیف‌های فهرست باید زیر عنوانشان، با فاصله‌ی یکسان بیایند. Tab را به جای فاصله به کار نبرید.

### ساختن محیط

<div dir="ltr">

```bash
conda env create -f demo_env.yml
```

</div>

پایان خروجی:

<div dir="ltr">

```text
Preparing transaction: ...working... done
Verifying transaction: ...working... done
Executing transaction: ...working... done
#
# To activate this environment, use
#
#     $ conda activate course_demo
```

</div>

‏Conda نسخه‌های سازگار همه‌ی بسته‌ها را پیدا کرد (به این کار **حل وابستگی** می‌گویند)، دانلودشان کرد و در یک پوشه‌ی جدا نصب کرد.

### پیش و پس از فعال کردن

پیش از فعال کردن محیط:

<div dir="ltr">

```bash
seqkit version
```

</div>

<div dir="ltr">

```text
bash: seqkit: command not found
```

</div>

پس از فعال کردن:

<div dir="ltr">

```bash
conda activate course_demo
seqkit version
jq --version
which seqkit
```

</div>

<div dir="ltr">

```text
seqkit v2.13.0
jq-1.8.2
/home/ubuntu/miniforge3/envs/course_demo/bin/seqkit
```

</div>

**این خروجی یعنی:**
- ‏`seqkit` تنها **درون** محیط پیدا می‌شود.
- ‏`which` (کجاست؟) نشان می‌دهد ابزار از پوشه‌ی **محیط** (`envs/course_demo/bin/`) اجرا می‌شود.
- اعلان ترمینال اکنون با `(course_demo)` آغاز می‌شود. برای بیرون آمدن: `conda deactivate`.

<details>
<summary>✋ <b>امتحان کن:</b> یک فرمان بنویسید که همه‌ی محیط‌های شما را فهرست کند. محیط فعال چگونه نشان داده می‌شود؟</summary>

<div dir="ltr">

```bash
conda env list
```

</div>

خروجی کمابیش این است (نشانی‌ها برای شما فرق دارند):

<div dir="ltr">

```text
base                 *   /home/ubuntu/miniforge3
course_demo              /home/ubuntu/miniforge3/envs/course_demo
```

</div>

`*` کنار محیط **فعال** است. هر محیط یک پوشه در `~/miniforge3/envs/` است.
</details>

> 📺 **فیلم:** *Conda and Bioconda, the best thing since sliced bread*: https://www.youtube.com/watch?v=x4IghzGI_6Y (Devon Ryan، ISMB 2019)
> 📄 **مرجع:** Grüning B, et al. (2018). *Bioconda.* Nature Methods 15:475–476. https://doi.org/10.1038/s41592-018-0046-7

---

## ۵. ثبت نسخه‌ها برای گزارش

### ‏`conda list`: همه‌ی بسته‌های محیط

<div dir="ltr">

```bash
conda list -n course_demo
```

</div>

<div dir="ltr">

```text
# packages in environment at /home/ubuntu/miniforge3/envs/course_demo:
#
# Name                     Version          Build            Channel
_openmp_mutex              4.5              20_gnu           conda-forge
jq                         1.8.2            h280c20c_1       conda-forge
libgcc                     16.2.0           ha9f2e26_7       conda-forge
libgomp                    16.2.0           he0feb66_7       conda-forge
oniguruma                  6.9.10           hebe6cf0_1       conda-forge
seqkit                     2.13.0           he881be0_0       bioconda
```

</div>

**این خروجی یعنی:** ما تنها دو بسته خواستیم، ولی شش بسته نصب شد. چهار تای دیگر **وابستگی**‌اند: کتابخانه‌هایی که `jq` و `seqkit` برای کار کردن لازم دارند. Conda آن‌ها را خودش پیدا و نصب کرد. ستون آخر می‌گوید هر بسته از کدام کانال آمده است.

### ‏`env export`: فایل محیط را از خود محیط بسازید

<div dir="ltr">

```bash
conda env export -n course_demo --from-history
```

</div>

<div dir="ltr">

```text
name: course_demo
channels:
  - bioconda
  - conda-forge
dependencies:
  - jq
  - seqkit=2.13.0
prefix: /home/ubuntu/miniforge3/envs/course_demo
```

</div>

‏`--from-history` تنها چیزهایی را می‌آورد که **خودتان خواستید**. این برای اشتراک با دیگران بهترین است: کوتاه است و روی هر سیستم‌عاملی کار می‌کند. بی `--from-history`، همه‌ی بسته‌ها با نسخه و build دقیق می‌آیند (مانند `seqkit=2.13.0=he881be0_0`)، که برای آرشیو دقیق همراه مقاله خوب است.

### اسکریپت ثبت نسخه‌ها

اسکریپت آماده‌ی این ماژول ([record_versions.sh](../99_scripts_data/01_Conda_Bioconda/scripts/record_versions.sh)) نسخه‌ی ابزارهای دلخواه را در یک جدول می‌نویسد:

<div dir="ltr">

```bash
bash ~/Bioinformatics_Learning-main/02_BioLinux/99_scripts_data/01_Conda_Bioconda/scripts/record_versions.sh course_demo seqkit jq samtools
```

</div>

<div dir="ltr">

```text
tool	version	channel
seqkit	2.13.0	bioconda
jq	1.8.2	conda-forge
samtools	NOT_INSTALLED	-
# environment=course_demo  conda=26.7.2  date=2026-10-20
```

</div>

**این خروجی یعنی:** یک جدول آماده برای پیوست مقاله یا پایان‌نامه: نسخه و کانال هر ابزار، و تاریخ. `samtools` در این محیط نصب نیست، و اسکریپت این را آشکارا می‌گوید. (درون اسکریپت همان `if`، `for` و `awk` بخش لینوکس است.)

---

## ۶. محیط کامل دوره

همه‌ی ابزارهای بخش‌های ۰۲ و ۰۳ در فایل [`envs/bioinfo_course.yml`](../../envs/bioinfo_course.yml) آمده‌اند: `seqkit`، `samtools`، `bcftools`، `jq`، `ncbi-datasets-cli` (برای دانلود از NCBI)، و Python با Biopython و pandas.

<div dir="ltr">

```bash
cd ~/Bioinformatics_Learning-main
conda env create -f envs/bioinfo_course.yml
conda activate bioinfo_course
```

</div>

ساختن این محیط چند دقیقه طول می‌کشد و نزدیک به یک گیگابایت جا می‌گیرد. **از این پس، پیش از هر درس بخش‌های ۰۲ و ۰۳، `conda activate bioinfo_course` بزنید.**

### کارهای روزمره

| می‌خواهم… | دستور |
| :--- | :--- |
| همه‌ی محیط‌ها را ببینم | `conda env list` |
| بسته‌ای بیفزایم (بهتر: به YAML بیفزایید و `update`) | ‏`conda install -n نام بسته` |
| محیط را با فایل همگام کنم | `conda env update -f file.yml --prune` |
| از محیط بیرون بیایم | `conda deactivate` |
| محیطی را پاک کنم | ‏`conda env remove -n نام` |
| فضای دیسک را آزاد کنم (کش بسته‌ها) | `conda clean --all` |

---

## ۷. سه اشتباه رایج

### اشتباه ۱: فراموش کردن `conda activate`

<div dir="ltr">

```text
bash: seqkit: command not found
```

</div>

ابزار نصب است، ولی در محیطی که فعال نیست. اعلان ترمینال را ببینید: نام محیط فعال در پرانتز آغاز آن است.

### اشتباه ۲: نام نادرست محیط

<div dir="ltr">

```bash
conda activate no_such_env
```

</div>

<div dir="ltr">

```text
EnvironmentNameNotFound: Could not find conda environment: no_such_env
You can list all discoverable environments with `conda info --envs`.
```

</div>

با `conda env list` نام درست را ببینید.

### اشتباه ۳: نصب همه چیز در `base`

محیط `base` خود Conda را نگه می‌دارد. اگر صدها بسته در آن نصب کنید، دیر یا زود تعارضی پیش می‌آید که **خود Conda** را از کار می‌اندازد. **`base` را تنها برای Conda نگه دارید؛ برای هر پروژه یا گروه ابزار، محیط جدا بسازید.**

---

## ۸. جمع‌بندی

- ‏Conda بسته‌ها را با همه‌ی وابستگی‌هایشان نصب می‌کند؛ Bioconda کانال ابزارهای زیستی است.
- **محیط** یک «میز کار» جداست؛ با `conda activate` واردش و با `conda deactivate` بیرون می‌آیید.
- محیط را **از فایل YAML** بسازید (`conda env create -f`) و فایل را نگه دارید.
- نسخه‌ها را با `conda list`، `conda env export --from-history` یا `record_versions.sh` ثبت کنید.
- محیط دوره: `conda env create -f envs/bioinfo_course.yml` و سپس `conda activate bioinfo_course`.

---

## کارت دستورهای این درس

| می‌خواهم… | دستور |
| :--- | :--- |
| نسخه‌ی conda | `conda --version` |
| محیط از فایل | `conda env create -f env.yml` |
| فعال کردن | ‏`conda activate نام` |
| بیرون آمدن | `conda deactivate` |
| ابزار از کجا اجرا می‌شود؟ | `which seqkit` |
| فهرست محیط‌ها | `conda env list` |
| بسته‌های یک محیط | ‏`conda list -n نام` |
| فایل محیط (کوتاه) | ‏`conda env export -n نام --from-history > env.yml` |
| ثبت نسخه‌ها | ‏`bash record_versions.sh نام ابزار1 ابزار2` |
| پاک کردن محیط | ‏`conda env remove -n نام` |

---

<details>
<summary>📘 <b>برای کنجکاوها (اختیاری):</b> چرا Miniforge و نه Anaconda؟ و وقتی مخزن در دسترس نیست</summary>

‏**Anaconda و Miniconda** به‌طور پیش‌فرض از کانال `defaults` شرکت Anaconda بسته می‌گیرند. به‌کارگیری این کانال تابع شرایط خدمات آن شرکت است و برای برخی سازمان‌ها مجوز تجاری می‌خواهد. Bioconda هم `defaults` را از کانال‌های پیشنهادی‌اش برداشته است. Miniforge تنها `conda-forge` را به کار می‌برد و این دردسر را ندارد.

‏**mamba** همان conda است با حل‌کننده‌ی تندتر (`mamba env create -f …`). از conda 23.10، conda هم همان حل‌کننده (libmamba) را به‌طور پیش‌فرض دارد، پس تفاوت سرعت کم شده است.

**بی اینترنت:** اگر بسته‌ها پیش‌تر دانلود شده باشند (در `~/miniforge3/pkgs/`)، `conda env create --offline -f file.yml` محیط را بی اینترنت می‌سازد. خروجی‌های همین درس روی سرور دوره به این روش گرفته شد، چون مخزن در دسترس نبود.

‏**pip در محیط Conda:** اگر بسته‌ای در conda نیست، می‌شود آن را با `pip` نصب کرد، ولی Conda از آن خبر ندارد و ممکن است تعارض پیش آید. نخست conda؛ pip تنها برای چیزی که در conda نیست، آن هم در بخش `- pip:` فایل YAML.
</details>

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| مدیر بسته (package manager) | برنامه‌ای که نرم‌افزار را با وابستگی‌هایش نصب و به‌روز می‌کند |
| بسته (package) | یک ابزار یا کتابخانه‌ی آماده‌ی نصب، با نسخه‌ی معین |
| وابستگی (dependency) | بسته‌ای که بسته‌ی دیگر برای کار کردن لازم دارد |
| کانال (channel) | مخزن بسته‌ها (conda-forge، bioconda) |
| محیط (environment) | پوشه‌ای جدا با بسته‌های خودش |
| YAML | قالب متنی ساده برای فایل‌های تنظیم؛ فرورفتگی در آن معنا دارد |
| حل وابستگی (solving) | پیدا کردن نسخه‌هایی از همه‌ی بسته‌ها که با هم سازگارند |

---

## منابع

### مقاله و راهنمای رسمی
- Grüning B, et al. (2018). Bioconda: sustainable and comprehensive software distribution for the life sciences. *Nature Methods* 15:475–476. https://doi.org/10.1038/s41592-018-0046-7
- ‏Bioconda (راهنمای رسمی، شامل تنظیم کانال‌ها): https://bioconda.github.io/
- Miniforge: https://github.com/conda-forge/miniforge
- conda — Managing environments: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

### کتاب
- ‏Buffalo V (2015). *Bioinformatics Data Skills*. O'Reilly. (فصل ۲: سامان دادن پروژه و نرم‌افزار)

### فیلم‌های آموزشی

**Coursera:**
- ‏KAUST — *Fundamental Skills in Bioinformatics*. بخش‌های نصب ابزارها و کار در Unix: https://www.coursera.org/learn/fundamental-skills-in-bioinformatics

**edX:**
- ‏The Linux Foundation — *Introduction to Linux*، بخش مدیریت بسته‌ها: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux

**YouTube:**
- ISCB / BIOINFO-CORE (ISMB/ECCB 2019) — Devon Ryan, *Conda and Bioconda, the best thing since sliced bread*: https://www.youtube.com/watch?v=x4IghzGI_6Y
- Bioinformagician — *Demystifying Conda (Anaconda, Miniconda and Bioconda) and Virtual Environments*: https://www.youtube.com/watch?v=2bXGm0ZnJ38

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. خروجی‌های این درس در 2026-10-20 با conda 26.7.2 گرفته شد. محیط‌ها با `--offline` و از کش محلی بسته‌ها ساخته شدند، چون مخزن Conda از سرور دوره در دسترس نبود. خروجی روی کامپیوتر شما همان است، جز نشانی‌ها و نسخه‌ی conda.

</div>
