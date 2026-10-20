<div dir="rtl">

# پاسخ تشریحی: نصب ابزارهای زیستی با Conda و Bioconda

> خروجی‌ها در 2026-10-20 روی سرور دوره (conda 26.7.2) گرفته شدند. نشانی‌ها (`/home/ubuntu/…`) روی کامپیوتر شما نام کاربری خودتان را دارند.

---

## تمرین ۱: نصب و تنظیم

1. ‏`conda --version` چیزی مانند `conda 26.7.2` می‌دهد؛ نسخه‌ی شما ممکن است تازه‌تر باشد و این مشکلی نیست.
2. پس از سه دستور بخش ۳، `conda config --show channels channel_priority` باید `channel_priority: strict` و فهرست کانال‌ها را با **`conda-forge` در بالا** و `bioconda` پس از آن نشان دهد. چون `--add` هر کانال را به **بالای** فهرست می‌افزاید و `conda-forge` آخر افزوده شد. Bioconda خودش این ترتیب را می‌خواهد: بسیاری از بسته‌های Bioconda به کتابخانه‌های conda-forge وابسته‌اند.

**اشتباه رایج:** جابه‌جا نوشتن دو دستور `--add`. آن‌گاه bioconda بالاتر می‌رود. اگر چنین شد، دوباره `conda config --add channels conda-forge` بزنید تا conda-forge بالا بیاید.

---

## تمرین ۲: نخستین محیط

<div dir="ltr">

```bash
conda env create -f demo_env.yml
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

3. ‏`seqkit` از پوشه‌ی `envs/course_demo/bin/` اجرا می‌شود: یعنی از **همین محیط**، نه از جای دیگری در سیستم. اگر روزی دو نسخه از یک ابزار داشتید، `which` می‌گوید کدام اجرا می‌شود.

**اشتباه رایج:** فرورفتگی نادرست در YAML (برای نمونه `- seqkit` بی فاصله در آغاز). Conda خطای خواندن فایل می‌دهد. ردیف‌های فهرست باید با دو فاصله فرورفته باشند.

---

## تمرین ۳: درون و بیرون محیط

<div dir="ltr">

```bash
conda deactivate
seqkit version
conda env list
conda activate course_demo
```

</div>

1. ‏`bash: seqkit: command not found`؛ بیرون از محیط، `seqkit` نیست.
2. `*` کنار **`base`** است، چون پس از `deactivate` به `base` برگشتید:

<div dir="ltr">

```text
base                 *   /home/ubuntu/miniforge3
course_demo              /home/ubuntu/miniforge3/envs/course_demo
```

</div>

3. اعلان از `(base)` به `(course_demo)` تغییر کرد. **همیشه پیش از اجرای ابزار، به این پرانتز نگاه کنید.**

---

## تمرین ۴: چه چیزی واقعاً نصب شد؟

<div dir="ltr">

```bash
conda list -n course_demo | grep -v '^#' | wc -l
conda env export -n course_demo --from-history > my_env.yml
cat my_env.yml
```

</div>

<div dir="ltr">

```text
6
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

1. **۶ بسته**؛ شما **۲** خواستید (`seqkit` و `jq`). چهار تای دیگر (`_openmp_mutex`، `libgcc`، `libgomp`، `oniguruma`) **وابستگی**‌اند، کتابخانه‌هایی که این دو ابزار برای کار کردن لازم دارند.
2. همان دو بسته با همان نسخه‌ی `seqkit`. دو تفاوت: (الف) خط `prefix:`، نشانی محیط روی **همین** کامپیوتر. هنگام اشتراک فایل آن را پاک کنید، چون روی کامپیوتر دیگر معنا ندارد. (ب) ترتیب کانال‌ها در خروجی ممکن است با فایل شما فرق کند؛ هنگام اشتراک، ترتیب درست (conda-forge بالا) را خودتان بنویسید.

---

## تمرین ۵: محیط دوره و جدول نسخه‌ها

<div dir="ltr">

```bash
cd ~/Bioinformatics_Learning-main
conda env create -f envs/bioinfo_course.yml
conda activate bioinfo_course
bash 02_BioLinux/99_scripts_data/01_Conda_Bioconda/scripts/record_versions.sh bioinfo_course seqkit samtools bcftools jq python biopython pandas > versions.tsv
cat versions.tsv
```

</div>

نمونه‌ی خروجی همین اسکریپت (روی محیط `course_demo` در سرور دوره):

<div dir="ltr">

```text
tool	version	channel
seqkit	2.13.0	bioconda
jq	1.8.2	conda-forge
samtools	NOT_INSTALLED	-
# environment=course_demo  conda=26.7.2  date=2026-10-20
```

</div>

1 و 2. در `bioinfo_course` همه‌ی هفت ابزار نصب‌اند. نسخه‌هایی که فایل محیط **پین** کرده (seqkit 2.13.0، samtools 1.20، bcftools 1.21، biopython 1.88، pandas 3.0.5، python 3.13) باید در جدول شما همین‌ها باشند. نسخه‌ی `jq` و شماره‌ی آخر Python (مانند `3.13.x`) ممکن است فرق کند، چون پین نشده یا تنها تا دو رقم پین شده‌اند. (محیط کامل دوره روی سرور دوره ساخته نشد، چون مخزن Conda در دسترس نبود؛ حل‌پذیری فایل با `conda create --dry-run` وارسی شد.)

3. نمونه‌ی جمله‌ی Methods:

> «ریدها با seqkit v2.13.0 خلاصه شدند و فایل‌های هم‌ترازی با samtools v1.20 و bcftools v1.21 پردازش شدند. تحلیل‌های پایتون با Python 3.13، Biopython 1.88 و pandas 3.0.5 انجام شد. همه‌ی ابزارها از کانال‌های conda-forge و bioconda نصب شدند؛ فایل محیط Conda در مخزن کد پیوست آمده است.»

**نکته:** «فایل محیط پیوست است» از هر جمله‌ای قوی‌تر است، چون هر کس می‌تواند با یک دستور همان محیط را بسازد.

</div>
