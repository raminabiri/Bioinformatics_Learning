<div dir="rtl">

# درس: تایپینگ مولکولی با MLST

**بخش:** `07_Bacterial_Genomics` · **ماژول:** `03_MLST_Molecular_Typing` · **پیش‌نیاز:** ماژول [اسمبلی](../01_Assembly_Quality/) · **زمان:** حدود ۶۰ دقیقه · **ابزار (از مستندات):** mlst (Torsten Seemann)، پایگاه PubMLST · **آخرین بازبینی:** 2026-10-21

> ✍️ **وضعیت: نوشته‌شده، اجرا نشده.** نمونه‌خروجی‌ها از README رسمی `mlst` آمده‌اند و منبعشان کنار هر کدام نوشته شده؛ جدول‌های تمرینی **فرضی**‌اند و برچسب دارند. اجرای `mlst` روی ژنوم K-12 را به شما می‌سپاریم (تمرین ۱)؛ چند ثانیه طول می‌کشد.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. منطق MLST را بگویید: ۷ ژن خانه‌دار، شماره‌ی آلل، و سکانس‌تایپ (ST).
2. ‏`mlst` را روی اسمبلی‌ها اجرا کنید و خروجی آن را بخوانید، از جمله آلل‌های تازه، ناقص و گمشده.
3. ‏ST و کمپلکس کلونال را تفسیر کنید و کلون‌های پرخطر را بشناسید.
4. بگویید کِی MLST بس است و کِی cgMLST یا SNP (ماژول ۰۵) لازم است.

**پیش از آغاز:** `mlst` را در یک محیط جدا از Bioconda نصب کنید (`conda create -n mlst -c conda-forge -c bioconda mlst`). پایگاه PubMLST همراه آن نصب می‌شود.

<div dir="ltr">

```bash
conda activate mlst
cd ~/genomes
G=~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data
```

</div>

---

## ۱. داستان

در یک بخش مراقبت ویژه، در دو هفته از سه بیمار *Klebsiella pneumoniae* مقاوم به کارباپنم جدا شده است. پرسش کنترل عفونت: **یک شیوع است، یا سه رویداد جدا؟** نخستین گام، پاسخی سریع و استاندارد است: آیا این سه ایزوله «از یک تیپ»‌اند؟ **MLST** همین را، با زبانی که همه‌ی آزمایشگاه‌های دنیا می‌فهمند، پاسخ می‌دهد.

---

## ۲. مفهوم به زبان ساده

### ۲.۱ هفت ژن، هفت عدد، یک ST

‏**MLST** (*multilocus sequence typing*) تکه‌ای ۴۰۰ تا ۵۰۰ بازی از **۷ ژن خانه‌دار** را می‌سنجد: ژن‌هایی که در همه‌ی سویه‌های گونه هستند و آرام تغییر می‌کنند.

<div dir="ltr">

```text
gene:     adk  fumC  gyrB  icd  mdh  purA  recA        (E. coli, Achtman scheme)
allele:    10    11     4    8    8     8     2        <- each distinct sequence = a number
profile:  10-11-4-8-8-8-2  ->  ST10                    <- each distinct profile = a sequence type
```

</div>

- هر **توالی یکتا** از یک ژن یک شماره‌ی **آلل** می‌گیرد؛ حتی یک باز فرق = آلل تازه.
- هر **ترکیب** یکتا از هفت آلل یک **سکانس‌تایپ** (ST) است.
- شماره‌ها **هیچ معنای فاصله‌ای ندارند**: آلل ۸ به ۹ نزدیک‌تر از ۱۰۰ نیست.

پروفایل بالا پروفایل واقعی **ST10** در طرح Achtman است (PubMLST)؛ ST10 کمپلکس کلونال خودش را دارد («ST10 Cplx») و سویه‌های K-12 در آن جای می‌گیرند.

‏**طرح** (*scheme*) مجموعه‌ی ژن‌ها و آلل‌های یک گونه است. بسیاری از گونه‌ها طرح خود را در **PubMLST** (یا Pasteur) دارند؛ *E. coli* دو طرح دارد (Achtman و Pasteur)، و ST10 در طرح Achtman تعریف شده است.

### ‏۲.۲ ‏ST، کمپلکس کلونال، کلون پرخطر

- **کمپلکس کلونال** (CC): STهایی که در دست‌کم ۶ از ۷ آلل یکسان‌اند و به یک ST مرکزی می‌پیوندند.
- **کلون پرخطر**: STهایی که در سراسر دنیا با مقاومت و بیماری همراه‌اند: *E. coli* **ST131** (ESBL، فلوروکینولون)، *K. pneumoniae* **ST258** (KPC)، *S. aureus* **ST8** (USA300).

### ۲.۳ تفکیک MLST: بس است یا نه؟

| روش | ژن‌ها | تفکیک | کاربرد |
| :--- | ---: | :--- | :--- |
| ‏MLST | ۷ | پایین: یک ST می‌تواند ده‌ها سال تکامل را بپوشاند | «چه تیپی؟»، سنجش با ادبیات جهانی |
| ‏cgMLST | صدها تا هزاران ژن هسته | بالا | پایش ملی، خوشه‌یابی شیوع |
| ‏SNP (ماژول ۰۵) | کل ژنوم هسته | بالاترین | «آیا انتقال رخ داده؟» |

**درس کلیدی:** ST یکسان **لازم** است تا دو ایزوله یک کلون شیوع باشند، ولی **بس نیست**. دو ایزوله‌ی ST131 از دو قاره هم ST131‌اند.

---

## ۳. گام ۱: اجرای mlst (از مستندات)

<div dir="ltr">

```bash
mlst contigs.fa
```

</div>

نمونه‌خروجی (**از مستندات**: بخش Quick Start در README رسمی `mlst`):

<div dir="ltr">

```text
contigs.fa  neisseria  11149  abcZ(672) adk(3) aroE(4) fumC(3) gdh(8) pdhC(4) pgm(6)
```

</div>

| ستون | معنی |
| :--- | :--- |
| ۱ | نام فایل |
| ۲ | طرحی که `mlst` **خودش** تشخیص داد (این‌جا *Neisseria*) |
| ۳ | ‏ST (`-` اگر ترکیب در پایگاه نیست) |
| ۴ به بعد | ژن و شماره‌ی آلل آن |

‏`mlst` هر فایل FASTA یا GenBank (حتی فشرده) را می‌پذیرد؛ نیازی به گفتن گونه نیست. برای چند ژنوم با هم:

<div dir="ltr">

```bash
mlst --nopath assemblies/*.fa > mlst.tsv
```

</div>

| گزینه | کار |
| :--- | :--- |
| `--nopath` | تنها نام فایل، بی پوشه |
| `--scheme ecoli…` | طرح را **اجبار** کن (نام دقیق را با `mlst --list` ببینید) |
| `--label X` | به‌جای نام فایل، `X` بنویس |
| `--csv` | خروجی با ویرگول |
| `--full` | ستون‌های STATUS و SCORE را هم بیفزا |

### نشانه‌های آلل

به گفته‌ی README:

| نشانه | معنی |
| :--- | :--- |
| `n` | آلل دقیق و کامل |
| `~n` | آلل **تازه** با طول کامل، همانند آلل n |
| `n?` | همخوانی **ناقص** با یک آلل شناخته‌شده |
| `-` | آلل **گمشده** |
| `n,m` | **چند** آلل برای یک ژن |

نمونه (**از مستندات**):

<div dir="ltr">

```text
Anthrax  bcereus  -  glp(24) gmk(1) ilv(~83) pta(1) pur(~71) pyc(37) tpi(41)
```

</div>

دو آلل تازه (`~83`، `~71`)، پس ترکیب شناخته‌شده نیست و ST برابر `-` است.

با `--full`، ستون STATUS می‌آید (README این‌ها را پایدار می‌داند): **PERFECT** (همخوانی دقیق با یک ST)، **NOVEL** (آلل‌ها دقیق، ولی ترکیب ST ندارد)، **MIXED** (دست‌کم یک ژن با چند آلل)، **NONE** (هیچ همخوانی).

<details>
<summary>✋ امتحان کن: خروجی <code>recA(2,15)</code> برای یک ایزوله‌ی <i>E. coli</i> چه می‌گوید؟</summary>

دو آلل گوناگون برای یک ژن خانه‌دار تک‌نسخه‌ای. شایع‌ترین دلیل: **کشت مخلوط** دو سویه (ماژول ۰۱، درس ۲). کمتر: ژن دوبرابرشده. پیش از هر تفسیری، کیفیت اسمبلی و یکنواختی کشت را بسنجید.

</details>

> 📺 **فیلم:** *WGS-based Multilocus Sequence Typing*: https://www.youtube.com/watch?v=QCZk5_W8dII (Canadian Bioinformatics Workshops)
> 📄 **مرجع:** Maiden MCJ, et al. (1998). *Multilocus sequence typing.* PNAS 95:3140–3145. https://doi.org/10.1073/pnas.95.6.3140

---

## ۴. گام ۲: تفسیر برای پرسش شیوع

سه ایزوله‌ی داستان، هر سه ST258. نتیجه؟
- ✅ **سازگار** با یک شیوع: ST258 یک کلون پرخطر شناخته‌شده‌ی KPC است.
- ❌ **ثابت نمی‌کند**: ST258 در بسیاری از بیمارستان‌ها پایدار است؛ سه بیمار می‌توانند سه ورود جدا باشند.
- گام بعد: SNPها نسبت به یک مرجع (ماژول ۰۵). اختلاف چند SNP = انتقال اخیر بسیار محتمل؛ ده‌ها تا صدها SNP = نه.

و اگر یکی **ST11** بود؟ ST11 و ST258 در یک کمپلکس کلونال‌اند ولی در **یک آلل** فرق دارند؛ کمابیش بی‌گمان **ورود جدا**ست، نه بخشی از همان زنجیره.

> 📺 **فیلم:** *13. Galaxy MLST*: https://www.youtube.com/watch?v=4H-L1DVD3z8 (Sciensano)
> 📄 **مرجع:** Jolley KA, Bray JE, Maiden MCJ (2018). *Open-access bacterial population genomics: BIGSdb software, the PubMLST.org website and their applications.* Wellcome Open Res 3:124. https://doi.org/10.12688/wellcomeopenres.14826.1

---

## ۵. سه اشتباه رایج

‏**۱. ‏ST یکسان = شیوع.** ST تفکیک پایینی دارد؛ برای ادعای انتقال، SNP یا cgMLST لازم است.

**۲. نادیده گرفتن `~`، `?` و `-`.** آلل تازه یا گمشده بیشتر از **کیفیت اسمبلی** می‌آید (ژن روی مرز کانتیگ شکسته). پیش از ثبت آلل تازه در PubMLST، پوشش و کیفیت را بسنجید.

**۳. طرح نادرست.** تشخیص خودکار برای بیشتر گونه‌ها درست است، ولی برای گونه‌های چندطرحه (مانند *E. coli*: Achtman و Pasteur) طرح را با `--scheme` روشن کنید و نامش را گزارش کنید.

---

## 📘 برای کنجکاوها

- ‏**‏cgMLST:** همان منطق، با صدها تا هزاران ژن هسته؛ ابزارهایی مانند chewBBACA و پایگاه‌هایی مانند Enterobase برای *E. coli* و *Salmonella*.
- **به‌روز کردن پایگاه:** به گفته‌ی README، PubMLST اکنون برای API حساب کاربری می‌خواهد؛ README ابزار جداگانه‌ی `mlstdb` را برای دانلود پیشنهاد می‌کند.
- ‏**‏`--novel`:** آلل‌های تازه را در یک FASTA می‌نویسد تا به PubMLST فرستاده شوند.

---

## جمع‌بندی

- ‏MLST = ۷ ژن خانه‌دار → ۷ شماره‌ی آلل → یک ST؛ زبان مشترک جهانی تایپینگ.
- ‏`mlst` طرح را خودش تشخیص می‌دهد؛ `~`، `?`، `-` و `n,m` را جدی بگیرید.
- ‏ST یکسان لازم است، نه بس؛ برای «آیا انتقال رخ داده؟» SNP (ماژول ۰۵).

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
mlst contigs.fa                                   # auto-detect scheme
mlst --nopath assemblies/*.fa > mlst.tsv          # many genomes, one table
mlst --full --nopath assemblies/*.fa              # + STATUS and SCORE
mlst --list                                       # available schemes
mlst --scheme NAME contigs.fa                     # force a scheme
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| ژن خانه‌دار | ژنی که در همه‌ی سویه‌ها هست و برای زندگی سلول لازم است |
| آلل | هر توالی یکتای یک ژن، با یک شماره |
| ‏ST (سکانس‌تایپ) | هر ترکیب یکتای آلل‌های ۷ ژن |
| طرح (*scheme*) | فهرست ژن‌ها و آلل‌های یک گونه در PubMLST |
| کمپلکس کلونال | ‏STهایی که در ۶ از ۷ آلل یکسان‌اند |
| ‏cgMLST | ‏MLST با همه‌ی ژن‌های هسته |

---

## منابع

**مستند و مقاله**
- Maiden MCJ, et al. (1998). *Multilocus sequence typing: a portable approach to the identification of clones within populations of pathogenic microorganisms.* PNAS 95:3140–3145. https://doi.org/10.1073/pnas.95.6.3140
- Jolley KA, Bray JE, Maiden MCJ (2018). *Open-access bacterial population genomics: BIGSdb software, the PubMLST.org website and their applications.* Wellcome Open Research 3:124. https://doi.org/10.12688/wellcomeopenres.14826.1
- Wirth T, et al. (2006). *Sex and virulence in Escherichia coli: an evolutionary perspective.* Molecular Microbiology 60:1136–1151. https://doi.org/10.1111/j.1365-2958.2006.05172.x
- mlst README: https://github.com/tseemann/mlst · PubMLST: https://pubmlst.org

**کتاب**
- Robinson DA, Falush D, Feil EJ (eds.) (2010). *Bacterial Population Genetics in Infectious Disease*. Wiley-Blackwell.

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins University). دوره‌ای ویژه‌ی MLST در Coursera نیافتیم؛ نزدیک‌ترین: https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Linux* (The Linux Foundation). دوره‌ای ویژه در edX نیافتیم؛ نزدیک‌ترین: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux
- YouTube: *WGS-based Multilocus Sequence Typing* (Canadian Bioinformatics Workshops، Infectious Disease Genomic Epidemiology 2017): https://www.youtube.com/watch?v=QCZk5_W8dII
- ‏YouTube: *13. Galaxy MLST* (Sciensano، آموزش Galaxy): https://www.youtube.com/watch?v=4H-L1DVD3z8

<sub>پروفایل ST10 در 2026-10-21 از PubMLST REST API (`pubmlst_escherichia_seqdef`، طرح ۱) وارسی شد. نشانی‌های YouTube از جست‌وجوی 2026-10-21‌اند؛ همه‌ی نشانی‌ها در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
