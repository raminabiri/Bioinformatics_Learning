# درس: مدیریت نرم‌افزار و محیط با Conda و Bioconda

**بخش:** `01_Computing_Foundations` · **ماژول:** `02_Conda_Environments` · **پیش‌نیاز:** 01_Bash_Linux · **زمان:** ۱٫۵ ساعت · **ابزار:** conda 26.7.2 (Miniforge)، libmamba 2.5.0 · **آخرین تست:** 2026-10-13

---

## ۱. مسئله

یک پروژه‌ی بیوانفورماتیک ده‌ها ابزار دارد. هر کدام به نسخه‌ی خاصی از Python، R، کتابخانه‌های C و ابزارهای دیگر وابسته‌اند. سه مشکل پیش می‌آید:
1. **نصب:** بسیاری از ابزارها با `apt` یا `pip` به‌سختی نصب می‌شوند (کامپایل، وابستگی‌های سیستمی).
2. **تعارض:** ابزار A با Python 3.8 کار می‌کند و ابزار B با 3.12.
3. **تکرارپذیری:** شش ماه بعد، یا روی کامپیوتر داور، همان نسخه‌ها باید دوباره نصب شوند. «با FastQC تحلیل شد» کافی نیست، باید «FastQC 0.12.1» باشد.

**Conda** مدیر بسته و محیط است و هر سه را حل می‌کند. **Bioconda** کانال تخصصی آن برای ابزارهای زیستی است و بیش از ۱۰٬۰۰۰ بسته دارد.

## ۲. مفاهیم

| مفهوم | معنی |
| :--- | :--- |
| **بسته (package)** | یک ابزار یا کتابخانه‌ی کامپایل‌شده، با نسخه و build مشخص (مثلاً `seqkit-2.13.0-he881be0_0`) |
| **کانال (channel)** | مخزنی که بسته‌ها از آن دانلود می‌شوند: `conda-forge` (عمومی، جامعه‌محور)، `bioconda` (زیستی) |
| **محیط (environment)** | پوشه‌ای ایزوله با مجموعه‌ای از بسته‌ها و Python/R مخصوص خودش. هر پروژه یا گروه ابزار یک محیط |
| **حل‌کننده (solver)** | الگوریتمی که نسخه‌های سازگار همه‌ی بسته‌ها را پیدا می‌کند. از conda 23.10 پیش‌فرض **libmamba** است |

### کدام نصب‌کننده؟ Miniforge
- **Miniforge** (توزیع conda-forge) را نصب کنید: سبک است، به‌طور پیش‌فرض از کانال `conda-forge` استفاده می‌کند و `mamba` را هم دارد.
- **Anaconda/Miniconda** به‌طور پیش‌فرض از کانال `defaults` شرکت Anaconda استفاده می‌کنند. استفاده از این کانال تابع **شرایط خدمات Anaconda** است و برای برخی سازمان‌ها مجوز تجاری لازم دارد. Bioconda هم از اوت ۲۰۲۴ `defaults` را از کانال‌های توصیه‌شده‌اش حذف کرده است.

```bash
# نصب Miniforge (یک‌بار؛ حدود ۹۰ مگابایت دانلود)
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh -b -p ~/miniforge3
~/miniforge3/bin/conda init bash     # بعد ترمینال را ببندید و باز کنید
```

### تنظیم کانال‌ها (طبق مستندات فعلی Bioconda)
```bash
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
conda config --show channels channel_priority
```
```text
channel_priority: strict
channels:
  - conda-forge
  - bioconda
```
`--add` کانال را به **بالای** فهرست اضافه می‌کند. پس آخرین `--add` (conda-forge) بالاترین اولویت را می‌گیرد. `strict` یعنی اگر بسته‌ای در کانال با اولویت بالاتر هست، از کانال پایین‌تر برداشته نشود. این جلوی ترکیب ناسازگار کتابخانه‌ها را می‌گیرد.

> **فایل محیط اولویت را تعیین می‌کند.** وقتی محیط را از فایل YAML می‌سازید، ترتیب `channels:` **در خود فایل** اعمال می‌شود. فایل‌های این دوره conda-forge را بالای bioconda می‌گذارند.

## ۳. کار عملی

### گام ۱: محیط از فایل، نه با دستورهای پراکنده
روش تکرارپذیر این است که محیط را از یک **فایل YAML** بسازید که در git نگه‌داری می‌شود:
```yaml
# demo_env.yml
name: course_demo
channels:
  - conda-forge
  - bioconda
dependencies:
  - seqkit=2.13.0
  - jq
```
```bash
conda env create -f demo_env.yml
conda activate course_demo
seqkit version ; jq --version ; which seqkit
```
```text
seqkit v2.13.0
jq-1.8.2
/home/ubuntu/miniforge3/envs/course_demo/bin/seqkit
```
`which` نشان می‌دهد ابزار از **پوشه‌ی محیط** اجرا می‌شود. اگر محیط فعال نباشد، یا ابزار پیدا نمی‌شود یا نسخه‌ی دیگری اجرا می‌شود.

فایل محیط کامل دوره: [`envs/bioinfo_course.yml`](../../envs/bioinfo_course.yml).

### گام ۲: سه شکل خروجی گرفتن از محیط
```bash
conda env export -n course_demo --from-history   # فقط چیزهایی که خودتان خواستید
```
```text
name: course_demo
channels:
  - bioconda
  - conda-forge
dependencies:
  - jq
  - seqkit=2.13.0
```
```bash
conda env export -n course_demo                  # همه‌ی بسته‌ها با نسخه و build دقیق
```
```text
dependencies:
  - _openmp_mutex=4.5=20_gnu
  - jq=1.8.2=h280c20c_1
  - libgcc=16.2.0=ha9f2e26_7
  - libgomp=16.2.0=he0feb66_7
  - oniguruma=6.9.10=hebe6cf0_1
  - seqkit=2.13.0=he881be0_0
```
```bash
conda list -n course_demo --explicit > course_demo.lock.txt   # آدرس دقیق هر فایل بسته
```

| روش | قابل‌حمل بین سیستم‌عامل‌ها؟ | دقت بازتولید | کاربرد |
| :--- | :-: | :-: | :--- |
| `--from-history` | ✅ | کم (نسخه‌ی وابستگی‌ها آزاد است) | اشتراک با دیگران، بلندمدت |
| `env export` کامل | ❌ (build وابسته به پلتفرم) | بالا | بازتولید روی همان نوع سیستم |
| `list --explicit` | ❌ | **دقیق** (همان فایل‌ها) | آرشیو همراه مقاله |

**توصیه:** فایل `--from-history` با نسخه‌ی ابزارهای اصلی پین‌شده (مثل `seqkit=2.13.0`) را در git نگه دارید. هنگام انتشار مقاله، خروجی `--explicit` را هم آرشیو کنید.

### گام ۳: مدیریت روزمره
```bash
conda env list                       # همه‌ی محیط‌ها؛ * جلوی محیط فعال
conda install -n course_demo seqtk   # افزودن بسته به محیط (بهتر: افزودن به YAML و conda env update)
conda env update -f demo_env.yml --prune   # همگام‌سازی محیط با فایل (--prune: حذف بسته‌های اضافه)
conda deactivate
conda env remove -n course_demo      # حذف کامل
conda clean --all                    # پاک کردن کش بسته‌ها و آزاد کردن فضا
```
`mamba` همان دستورها را با همان گزینه‌ها دارد (`mamba env create -f ...`). از conda 23.10 که libmamba حل‌کننده‌ی پیش‌فرض conda شد، فاصله‌ی سرعت این دو کم شده است.

### گام ۴: وقتی اینترنت یا مخزن در دسترس نیست
این وضعیت در همین دوره پیش آمد: در 2026-10-12 مخزن `conda.anaconda.org` از سرور دوره در دسترس نبود و ساخت محیط با خطای `Could not resolve host` و `SSL connect error` شکست خورد. سه راه:

1. **کش محلی:** اگر بسته‌ها قبلاً دانلود شده باشند (`~/miniforge3/pkgs/`)، conda می‌تواند بدون اینترنت محیط بسازد:
   ```bash
   conda env create --offline -f demo_env.yml     # روی سرور دوره: ۳ ثانیه
   ```
2. **mirror:** بعضی دانشگاه‌ها و کشورها mirror محلی conda-forge دارند (`conda config --add channels <mirror-url>`).
3. **نصب از منبع رسمی ابزار:** باینری یا کد منبع از GitHub یا سایت سازنده. راه آخر است، چون ثبت نسخه دستی می‌شود ([envs/README.md](../../envs/README.md)).

## ۴. دام‌ها (Pitfalls)

| دام | چرا مشکل است | راه درست |
| :--- | :--- | :--- |
| نصب همه‌چیز در `base` | base خراب می‌شود و conda از کار می‌افتد | base فقط برای conda/mamba؛ هر پروژه یک محیط |
| یک محیط غول‌پیکر برای همه‌ی ابزارها | حل وابستگی ناممکن یا خیلی کند می‌شود | محیط برای هر گروه ابزار (مثلاً QIIME 2 جدا) |
| کانال `defaults` + `conda-forge` + `bioconda` با هم | ترکیب کتابخانه‌های ناسازگار؛ مسائل مجوز | فقط conda-forge و bioconda، با `strict` |
| `pip install` داخل محیط conda بدون فکر | conda از بسته‌های pip خبر ندارد و تعارض پیش می‌آید | اول conda؛ pip فقط برای بسته‌ای که در conda نیست، آن هم در بخش `pip:` فایل YAML |
| نصب تعاملی و فراموش کردن نسخه‌ها | محیط قابل بازتولید نیست | YAML در git + `export --from-history` |
| ثبت نکردن نسخه در Methods | داور نمی‌تواند تکرار کند | نسخه‌ی هر ابزار (و لینک فایل محیط) در Methods |

## ۵. جمع‌بندی
- Miniforge نصب کنید. کانال‌ها conda-forge و bioconda باشند، با `strict`.
- هر پروژه محیط خودش را دارد و آن محیط **از یک فایل YAML** ساخته می‌شود که در git است.
- برای اشتراک از `--from-history` استفاده کنید و برای آرشیو دقیق از `--explicit`.
- برای بازتولید کامل‌تر، حتی از سیستم‌عامل مستقل، کانتینرها (Docker/Apptainer) را در بخش ۰۷ می‌بینیم.

---

## منابع

### مقاله و مستندات
- Grüning B, et al. (2018). Bioconda: sustainable and comprehensive software distribution for the life sciences. *Nature Methods* 15:475–476. https://doi.org/10.1038/s41592-018-0046-7
- مستندات Bioconda (شامل تنظیم کانال‌ها): https://bioconda.github.io/
- Miniforge: https://github.com/conda-forge/miniforge · conda-forge: https://conda-forge.org/
- مستندات conda، مدیریت محیط‌ها: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
- اعلام پیش‌فرض شدن libmamba در conda 23.10: https://discuss.python.org/t/announcement-conda-23-10-0-release-libmamba-is-now-the-default-dependency-solver/38096
- Buffalo V. *Bioinformatics Data Skills*. O'Reilly, 2015: https://vincebuffalo.com/book/

### ویدیوهای آموزشی
- ISCB / BIOINFO-CORE (ISMB/ECCB 2019) — Devon Ryan, *Conda and Bioconda, the best thing since sliced bread*: https://www.youtube.com/watch?v=x4IghzGI_6Y
- Bioinformagician — *Demystifying Conda (Anaconda, Miniconda and Bioconda) and Virtual Environments*: https://www.youtube.com/watch?v=2bXGm0ZnJ38

> لینک‌ها در تاریخ 2026-10-13 بررسی شدند (`_tools/check_links.sh`).
