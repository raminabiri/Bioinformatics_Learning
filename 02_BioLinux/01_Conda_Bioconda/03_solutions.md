<div dir="rtl">

# پاسخ تشریحی: Conda و Bioconda

> اجرا شده در 2026-10-13 با conda 26.7.2 (Miniforge) روی سرور دوره.

---

## تمرین ۱

<div dir="ltr">

```bash
conda --version
conda config --show channels channel_priority solver
conda env list
```

</div>

<div dir="ltr">

```text
conda 26.7.2
channel_priority: strict
channels:
  - bioconda
  - conda-forge
solver: libmamba
```

</div>

- حل‌کننده **libmamba** است (پیش‌فرض از conda 23.10).
- ‏`conda env list` همه‌ی محیط‌ها را نشان می‌دهد و جلوی محیط فعال `*` می‌گذارد.
- **سازگاری با توصیه:** `strict` هست و `defaults` نیست، ولی **ترتیب برعکس است**: bioconda بالای conda-forge قرار گرفته. در عمل برای کتابخانه‌هایی که در هر دو کانال هستند، نسخه‌ی bioconda ترجیح داده می‌شود. اصلاح:

  <div dir="ltr">

  ```bash
  conda config --remove channels conda-forge
  conda config --add channels conda-forge      # حالا بالای فهرست است
  conda config --show channels
  ```

  </div>

  این‌ها فقط تنظیم پیش‌فرض‌اند. محیط‌هایی که از فایل YAML ساخته می‌شوند ترتیب `channels:` خود فایل را به کار می‌برند.

---

## تمرین ۲

<div dir="ltr">

```bash
conda env create -f demo_env.yml          # یا با --offline اگر مخزن در دسترس نیست
conda activate course_demo
which seqkit ; seqkit version ; jq --version
conda deactivate
which seqkit
```

</div>

<div dir="ltr">

```text
/home/ubuntu/miniforge3/envs/course_demo/bin/seqkit
seqkit v2.13.0
jq-1.8.2
```

</div>

بعد از `conda deactivate`، `which seqkit` یا **چیزی پیدا نمی‌کند**، یا **نسخه‌ی دیگری** را از جای دیگری در `PATH` نشان می‌دهد، مثلاً اگر seqkit در base یا در `~/opt/...` باشد.

‏`conda activate` فقط **پوشه‌ی `bin` محیط را به ابتدای `PATH` اضافه می‌کند**. «کدام نسخه اجرا می‌شود» همیشه به `PATH` بستگی دارد. `which` اولین ابزار برای اشکال‌یابی است.

---

## تمرین ۳

<div dir="ltr">

```bash
conda env export -n course_demo --from-history | wc -l     # 8 خط: ۲ بسته
conda env export -n course_demo | wc -l                    # 12 خط: ۶ بسته با build
conda list -n course_demo --explicit | grep -c '^https'    # 6 آدرس فایل
```

</div>

- ‏`--from-history`: فقط **۲ بسته** (`jq` و `seqkit=2.13.0`)، یعنی همان چیزهایی که خواسته شد.
- ‏`export` کامل: **۶ بسته** با build، که وابستگی‌های `libgcc`، `libgomp`، `oniguruma` و `_openmp_mutex` را هم دارد.
- ‏`--explicit`: **۶ URL** دقیق فایل بسته‌ها، برای `linux-64`.

**همراه مقاله:** `--explicit` (و/یا export کامل). این‌ها دقیق‌ترین ثبت‌اند: داور روی Linux دقیقاً همان فایل‌ها را نصب می‌کند.
**برای همکار با macOS:** `--from-history`. build‌های `linux-64` (مثل `libgcc`) روی macOS وجود ندارند و export کامل شکست می‌خورد. فایل `--from-history` به حل‌کننده اجازه می‌دهد معادل‌های macOS را پیدا کند. نسخه‌ی ابزار اصلی پین شده است، پس نتیجه‌ی علمی باید یکسان باشد.

---

## تمرین ۴

<div dir="ltr">

```bash
for e in ~/miniforge3/envs/*; do
  [ -x "$e/bin/samtools" ] && printf "%s\t%s\n" "$(basename $e)" "$(conda list -n $(basename $e) samtools | tail -1 | awk '{print $2}')"
done
```

</div>

<div dir="ltr">

```text
genomepipe_tools	0.1.19
snippy_env	1.20
```

</div>

1. روی سرور دوره دو نسخه‌ی کاملاً متفاوت وجود دارد: **samtools 0.1.19** (سال ۲۰۱۳) و **1.20**. (در `genomepipe_tools`، `samtools --version` اصلاً وجود ندارد؛ نسخه با اجرای `samtools` بدون آرگومان چاپ می‌شود.)
2. نتیجه‌ی `samtools sort` به این بستگی دارد که **کدام محیط فعال است**، یعنی چه چیزی در `PATH` جلوتر است. سینتکس `sort` بین 0.1.x و 1.x **تغییر کرده** است: در 0.1.19 پیشوند خروجی آرگومان است، در 1.x با `-o` داده می‌شود. پس یا خطا می‌گیرید، یا بدتر، فایل با نام غیرمنتظره ساخته می‌شود. و در Methods نسخه‌ی اشتباه گزارش می‌شود.
3. ‏`conda run -n snippy_env samtools ...` فرمان را **در آن محیط** اجرا می‌کند، بدون اینکه محیط shell فعلی را تغییر دهد. در اسکریپت‌های غیرتعاملی، `conda activate` به `conda init` و `source` شدن `.bashrc` وابسته است و ممکن است کار نکند. `conda run` صریح است و به وضعیت ترمینال وابسته نیست.

   <div dir="ltr">

   ```bash
   conda run -n snippy_env samtools --version | head -1     # samtools 1.20
   ```

   </div>

---

## تمرین ۵

مشکلات:
1. **کانال `defaults`**: مسائل مجوز Anaconda، و ترکیب ناسازگار با conda-forge.
2. **ترتیب کانال‌ها**: `defaults` بالاترین اولویت را دارد و conda-forge پایین‌ترین. عکس توصیه است.
3. **هیچ نسخه‌ای پین نشده**: شش ماه بعد محیط دیگری ساخته می‌شود.
4. ‏**QIIME 2 در همان محیط**: QIIME 2 توزیع و محیط اختصاصی خودش را دارد و با ابزارهای دیگر تعارض وابستگی ایجاد می‌کند.
5. ‏**biopython و pandas از pip**: هر دو در conda-forge موجودند. نصب با pip وابستگی‌ها (مثل numpy) را خارج از کنترل conda عوض می‌کند.
6. نام کلی `my_analysis`: نام باید پروژه یا هدف را بگوید.

بازنویسی:

<div dir="ltr">

```yaml
name: gut_qc_2026
channels:
  - conda-forge
  - bioconda
dependencies:
  - python=3.11
  - fastqc=0.12.1
  - samtools=1.20
  - biopython=1.84
  - pandas=2.2
# QIIME 2 → محیط جداگانه طبق دستور نصب رسمی QIIME 2
```

</div>

(نسخه‌های biopython و pandas را با نسخه‌ای که واقعاً تست کرده‌اید جایگزین کنید.)

---

## تمرین ۶ (چالشی)

پاسخ: [scripts/record_versions.sh](../99_scripts_data/01_Conda_Bioconda/scripts/record_versions.sh)

<div dir="ltr">

```bash
bash scripts/record_versions.sh snippy_env
bash scripts/record_versions.sh course_demo seqkit jq samtools
```

</div>

<div dir="ltr">

```text
tool	version	channel
fastqc	NOT_INSTALLED	-
fastp	NOT_INSTALLED	-
multiqc	NOT_INSTALLED	-
bowtie2	NOT_INSTALLED	-
samtools	1.20	bioconda
seqkit	NOT_INSTALLED	-
# environment=snippy_env  conda=26.7.2  date=2026-10-13
tool	version	channel
seqkit	2.13.0	bioconda
jq	1.8.2	conda-forge
samtools	NOT_INSTALLED	-
# environment=course_demo  conda=26.7.2  date=2026-10-13
```

</div>

نکته‌ها:
- ‏`conda list` خروجی را **یک‌بار** می‌گیرد و برای هر ابزار جستجو می‌کند. هر بار صدا زدن `conda list` چند ثانیه طول می‌کشد.
- در `conda list`، ستون کانال برای بسته‌های کانال پیش‌فرض (در Miniforge، conda-forge) **خالی** است. اسکریپت آن را `conda-forge` می‌نویسد. این فرض را در توضیح جدول ذکر کنید.
- اگر نام محیط اشتباه باشد، پیام خطا در stderr چاپ می‌شود و اسکریپت با کد ۱ خارج می‌شود.

**پاک‌سازی بعد از تمرین‌ها:** `conda env remove -n course_demo`

</div>
