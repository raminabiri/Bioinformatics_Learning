<div dir="rtl">

# درس ۲: پایگاه CARD، ابزار RGI و ABRicate؛ چرا ابزارها با هم فرق دارند؟

**بخش:** `08_AMR_Virulence_Phylogeny` · **ماژول:** `01_AMR_Resistance_Genes` · **پیش‌نیاز:** [درس ۱](01_lesson_amrfinder.md) · **زمان:** حدود ۴۵ دقیقه · **ابزار (از مستندات):** RGI (پایگاه CARD)، ABRicate 1.4.0 · **آخرین بازبینی:** 2026-10-24

> ✍️ **وضعیت: نوشته‌شده، اجرا نشده.** RGI و ABRicate روی سرور ما نصب نیستند و سرور به conda.anaconda.org دسترسی ندارد؛ پس دستورها از مستند رسمی آمده‌اند و منبع کنار هر کدام نوشته شده است. پیش‌فرض‌های ABRicate (`--minid 80`، `--mincov 80`) از کد منبع نسخه‌ی 1.4.0 خوانده شده‌اند. هر جا رفتار ابزار روی ژنوم‌های درس ۱ را **پیش‌بینی** کرده‌ایم، برچسب «پیش‌بینی» دارد؛ آن را خودتان با اجرا بسنجید (تمرین ۷). هر دو ابزار سبک‌اند (BLAST روی یک ژنوم باکتری).

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. ساختار CARD را بگویید: هستی‌شناسی ARO و چهار گونه مدل (homolog، variant، rRNA، overexpression).
2. ‏RGI را اجرا کنید و رده‌های Perfect، Strict و Loose را تفسیر کنید.
3. ‏ABRicate را با چند پایگاه اجرا کنید و `--summary` بسازید.
4. بگویید چرا سه ابزار روی یک ژنوم سه جدول کمی متفاوت می‌دهند.
5. یک گزارش ژنوتیپ مقاومت بنویسید که با فنوتیپ (MIC) سنجیدنی باشد.

---

## ۱. داستان

همکارتان همان ایزوله‌ی isoB را با ABRicate بررسی کرده و می‌گوید: «من `tet(A)` ندیدم. تو گفتی هست. کدام درست است؟» هر دو درست‌اید؛ تنها **آستانه‌ها** فرق دارند. این درس یاد می‌دهد اختلاف ابزارها را پیش از آنکه به گزارش بالینی برسد بفهمید.

---

## ‏۲. ‏CARD و ابزار RGI

### ۲.۱ مفهوم به زبان ساده

‏**CARD** (Comprehensive Antibiotic Resistance Database، دانشگاه McMaster کانادا) تنها فهرست توالی نیست؛ یک **هستی‌شناسی** (ontology) به نام **ARO** (Antibiotic Resistance Ontology) دارد. هر ژن یک شناسه‌ی `ARO:…` دارد و به سه چیز پیوند می‌خورد:

<div dir="ltr">

```
ARO: CTX-M-15
  ├─ AMR Gene Family     → CTX-M beta-lactamase
  ├─ Drug Class          → cephalosporin, penam, ...
  └─ Resistance Mechanism → antibiotic inactivation
```

</div>

پس از RGI نه تنها «کدام ژن» بلکه «چه سازوکاری» و «کدام رده‌ی دارو» را هم می‌گیرید.

هر ژن در CARD با یک **مدل** جست‌وجو می‌شود:

| مدل | یعنی | نمونه |
| :--- | :--- | :--- |
| ‏protein homolog | بودن ژن بس است | ‏CTX-M-15، NDM-1 |
| ‏protein variant | ژن را همه دارند؛ تنها جهش معین مقاومت می‌دهد | ‏gyrA S83L |
| ‏rRNA gene variant | جهش در rRNA | جهش 23S در مقاومت به ماکرولید |
| ‏protein overexpression | جهش در تنظیم‌گر که بیان پمپ را بالا می‌برد | جهش در `marR` |

### ۲.۲ ‏Perfect، Strict، Loose

به گفته‌ی مستند RGI، برای مدل protein homolog:

| رده | معیار |
| :--- | :--- |
| **Perfect** | ‏۱۰۰٪ همسان با پروتئین مرجع، در **تمام طول** آن |
| **Strict** | همسان نیست، ولی bit-score از **آستانه‌ی بازبینی‌شده‌ی آن مدل** بالاتر است |
| **Loose** | ‏bit-score زیر آستانه؛ خویشاوندهای دور و ژن‌های تازه |

برای مدل‌های variant و overexpression، Strict تنها وقتی گزارش می‌شود که جهش بازبینی‌شده در توالی شما باشد. فرق مهم با AMRFinderPlus: RGI به جای درصد identity/coverage ثابت، برای **هر مدل یک آستانه‌ی bit-score جدا** دارد.

**تشبیه:** AMRFinderPlus مانند یک معلم است که با یک نمره‌ی قبولی برای همه (۹۰٪ پوشش) کار می‌کند؛ CARD برای هر درس نمره‌ی قبولی خودش را دارد.

### ۲.۳ گام‌به‌گام (از مستندات)

<div dir="ltr">

```bash
conda create -n rgi -c conda-forge -c bioconda rgi
conda activate rgi
cd ~/amr
wget https://card.mcmaster.ca/latest/data
tar -xvf data ./card.json
rgi load --card_json ./card.json --local
rgi main --input_sequence genomes/isoA.fna --output_file isoA_rgi \
    --input_type contig --local --clean
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`wget …/latest/data` و `tar … ./card.json` | آخرین نسخه‌ی CARD را می‌گیرد و تنها فایل `card.json` را از بسته بیرون می‌آورد |
| ‏`rgi load --card_json … --local` | پایگاه را در پوشه‌ی **جاری** (`./localDB`) بار می‌کند، نه در پوشه‌ی نصب. ‏`--local` را در `rgi main` هم باید داد |
| ‏`--input_type contig` | ورودی اسمبلی است (پیش‌فرض). برای پروتئین: `protein` |
| ‏`--clean` | فایل‌های میانی را پاک می‌کند |

**خروجی:** یک جدول tab-دار (`isoA_rgi.txt`) و یک فایل JSON. ستون‌های جدول، به ترتیبِ مستند رسمی، از جمله: `ORF_ID`، `Contig`، `Start`، `Stop`، `Orientation`، **`Cut_Off`** (Perfect/Strict/Loose)، `Pass_bit-score`، `Best_Hit_bit-score`، **`Best_Hit_ARO`**، `Best_Identities`، `ARO`، **`Model_type`**، **`SNPs_in_Best_Hit_ARO`**، `Other_SNPs`، **`Drug Class`**، **`Resistance Mechanism`**، **`AMR Gene Family`**، … و `Percentage Length of Reference Sequence`.

**پیش‌بینی (اجرا نشده):** برای isoA انتظار داریم `CTX-M-15` با Cut_Off برابر Perfect و Model_type برابر protein homolog بیاید، و gyrA با Model_type برابر protein variant و `S83L` در ستون `SNPs_in_Best_Hit_ARO`. RGI به‌طور پیش‌فرض رده‌ی Loose را گزارش نمی‌کند (گزینه‌ی `--include_loose`). همچنین RGI مدل‌های پمپ کروموزومی بسیاری دارد، پس انتظار داریم سطرهای «ذاتی» آن از پنج سطر plus در AMRFinderPlus بیشتر باشد. شمار دقیق را خودتان در تمرین ۷ بشمارید.

> 📺 **فیلم:** *Brian Alcock – The Comprehensive Antibiotic Resistance Database – Curating the Global Resistome*: https://www.youtube.com/watch?v=XKWfUbiQW8Q
> 📄 **مرجع:** Alcock BP, et al. (2023). *CARD 2023: expanded curation, support for machine learning, and resistome prediction at the Comprehensive Antibiotic Resistance Database.* Nucleic Acids Research 51:D690–D699. https://doi.org/10.1093/nar/gkac920 · مستند RGI: https://github.com/arpcard/rgi/blob/master/docs/rgi_main.rst · CARD: https://card.mcmaster.ca

<details>
<summary>✋ امتحان کن: یک ژن با ۹۸٪ همسانی و bit-score بالاتر از آستانه، در RGI چه رده‌ای می‌گیرد و در AMRFinderPlus چه Methodی؟</summary>

‏RGI: **Strict** (همسان نیست ولی از آستانه گذشته). ‏AMRFinderPlus: **BLASTX** (کمتر از ۱۰۰٪ همسان، پوشش بیش از ۹۰٪). هر دو «پیدا شد ولی دقیقاً همان آلل شناخته‌شده نیست» را می‌گویند. چنین ژنی شاید یک آلل تازه باشد.

</details>

---

## ‏۳. ‏ABRicate: یک ابزار، چندین پایگاه

### ۳.۱ مفهوم به زبان ساده

‏ABRicate (Torsten Seemann) تنها یک کار می‌کند: **blastn** اسمبلی شما در برابر یک پایگاه DNA. چند پایگاه آماده همراهش است: `ncbi` (همان ژن‌های AMRFinderPlus)، `card`، `resfinder`، `argannot`، `megares`، `vfdb` (بیماری‌زایی، ماژول ۰۲)، `plasmidfinder` (ماژول ۰۳)، `ecoh`، `ecoli_vf`، `victors`، `bacmet2` و `upec_expec_vf`.

به گفته‌ی README خودش، ABRicate:
- **جهش نقطه‌ای پیدا نمی‌کند**؛ تنها ژن‌های اکتسابی را می‌یابد.
- با DNA کار می‌کند، نه پروتئین؛ پس ژنی با جهش‌های هم‌معنا (synonymous) بسیار، شاید از دید آن بیفتد.
- تنها contig می‌پذیرد، نه FASTQ.

پیش‌فرض‌ها (کد منبع نسخه‌ی 1.4.0): **`--minid 80`** (کمترین همانندی DNA) و **`--mincov 80`** (کمترین پوشش). پایگاه پیش‌فرض `ncbi` است.

### ۳.۲ گام‌به‌گام (از مستندات)

<div dir="ltr">

```bash
conda create -n abricate -c conda-forge -c bioconda abricate
conda activate abricate
abricate --check
abricate --list
cd ~/amr
for db in ncbi card resfinder; do
  abricate --db $db genomes/iso*.fna > abricate_$db.tsv
done
abricate --summary abricate_ncbi.tsv > abricate_ncbi_summary.tsv
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`abricate --check` | بودن ابزارهای لازم (blastn، any2fasta و …) را بررسی می‌کند |
| ‏`abricate --list` | پایگاه‌های نصب‌شده، شمار توالی و تاریخشان را نشان می‌دهد؛ **تاریخ را در گزارش بنویسید** |
| ‏`--db $db` | پایگاه را برمی‌گزیند. حلقه‌ی `for` از بخش 01/09 است |
| ‏`genomes/iso*.fna` | چند ژنوم با هم؛ ستون نخست خروجی (`#FILE`) نام فایل را دارد |
| ‏`--summary` | ماتریس حضور/نبود: هر سطر یک فایل، هر ستون یک ژن، و در خانه‌ها **درصد پوشش** (یا `.` برای نبود) |

**ستون‌های خروجی** (README رسمی): `FILE`، `SEQUENCE`، `START`، `END`، `STRAND`، `GENE`، `COVERAGE`، `COVERAGE_MAP`، `GAPS`، `%COVERAGE`، `%IDENTITY`، `DATABASE`، `ACCESSION`، `PRODUCT`، `RESISTANCE`.

**نمونه‌خروجی از README رسمی ABRicate** (ستون‌های برگزیده؛ ژنوم *S. aureus*، نه داده‌ی ما):

<div dir="ltr">

```
FILE      SEQUENCE     START   END     STRAND  GENE     %COVERAGE  %IDENTITY  DATABASE  RESISTANCE
6159.fna  NC_017338.1  39177   41186   +       mecA_15  100.00     100.000    ncbi      FUSIDIC_ACID
6159.fna  NC_017338.1  727191  728356  -       norA_1   99.91      92.367     ncbi      FOSFOMYCIN
6159.fna  NC_017339.1  10150   10995   +       blaZ_32  100.00     100.000    ncbi      BETA-LACTAM;PENICILLIN
```

</div>

‏`COVERAGE_MAP` (در این نمونه حذف شده) یک نمودار متنی کوچک است: `=` یعنی بخشی از ژن که پیدا شده و `.` بخشی که نیست. نگاه به آن سریع‌ترین راه دیدن ژن بریده است.

**پیش‌بینی برای ژنوم‌های درس ۱ (اجرا نشده):** با `--db ncbi`، انتظار داریم `blaCTX-M-15` و `blaNDM-1` با پوشش و همانندی ۱۰۰٪ بیایند؛ چون توالی آن‌ها دقیقاً از همین پایگاه NCBI برداشته شده است. ‏`tet(A)` ناقص با پوشش نزدیک به ۵۰٪ **زیر `--mincov 80` است و گزارش نمی‌شود.** هیچ‌کدام از دو جهش gyrA و parC هم گزارش نمی‌شود. ‏isoC شاید هیچ سطری نداشته باشد یا تنها چند ژن کروموزومی داشته باشد؛ این را با اجرا روشن کنید.

> 📺 **فیلم:** *Antimicrobial Resistance Genes Detection using ABRicate tutorial*: https://www.youtube.com/watch?v=cmhuWRorCTg · نسخه‌ی گرافیکی در Galaxy: https://www.youtube.com/watch?v=n3OtDyWixpw
> 📄 **مرجع:** ABRicate: https://github.com/tseemann/abricate · ResFinder: Bortolaia V, et al. (2020). *ResFinder 4.0 for predictions of phenotypes from genotypes.* Journal of Antimicrobial Chemotherapy 75:3491–3500. https://doi.org/10.1093/jac/dkaa345

<details>
<summary>✋ امتحان کن: برای اینکه ABRicate هم tet(A) ناقص را نشان دهد، چه گزینه‌ای می‌دهید؟ آیا این کار را برای گزارش بالینی پیشنهاد می‌کنید؟</summary>

‏`--mincov 40` (یا هر عدد کمتر از ۵۰). ولی برای گزارش بالینی **نه**: با آستانه‌ی پایین، تکه‌های کوچک ژن‌ها (برای نمونه بازمانده‌ی یک ترانسپوزون) هم «مقاومت» خوانده می‌شوند. بهتر است با آستانه‌ی پیش‌فرض گزارش دهید، و برای پژوهش یک اجرای جدا با آستانه‌ی پایین بگیرید و ژن‌های ناقص را با برچسب کنار بگذارید.

</details>

---

## ۴. چرا ابزارها با هم فرق دارند؟

| | AMRFinderPlus | RGI (CARD) | ABRicate |
| :--- | :--- | :--- | :--- |
| جست‌وجو | پروتئین (tblastn) + DNA | پروتئین (BLAST یا DIAMOND) | تنها DNA (blastn) |
| جهش نقطه‌ای | ✅ با `--organism` | ✅ مدل‌های variant | ❌ |
| آستانه | ‏۹۰٪ پوشش؛ identity بازبینی‌شده برای هر خانواده | ‏bit-score بازبینی‌شده برای هر مدل | ‏۸۰٪ / ۸۰٪ ثابت (قابل تغییر) |
| ژن‌های ذاتی/پمپ | تنها با `--plus` | بسیار، به‌طور پیش‌فرض | بسته به پایگاه |
| نام‌گذاری | ‏`blaCTX-M-15` | ‏`CTX-M-15` | بسته به پایگاه (`blaCTX-M-15_1` در resfinder) |

پنج سرچشمه‌ی اختلاف: **(۱) محتوای پایگاه** (یک ژن تازه شاید تنها در یکی باشد)، **(۲) آستانه‌ها**، **(۳) DNA یا پروتئین**، **(۴) نام‌گذاری** (یک ژن با سه نام)، **(۵) جهش‌ها**. پس پیش از گفتن «ابزار X اشتباه کرد»، ببینید کدام یک از این پنج است.

**قاعده‌ی کار:** برای گزارش، یک ابزار اصلی برگزینید (برای گونه‌هایی که در `amrfinder -l` هستند، AMRFinderPlus با `--organism` گزینه‌ی خوبی است، چون جهش‌ها را هم می‌سنجد) و ابزار دوم را برای وارسی به کار ببرید. نسخه‌ی ابزار **و** پایگاه را بنویسید.

> 📺 **فیلم:** *Antibiotic Resistance Mechanisms*: https://www.youtube.com/watch?v=xYhHI-ddFJI
> 📄 **مرجع:** صفحه‌ی رسمی پایگاه‌های AMRFinderPlus و منبع ژن‌ها (Reference Gene Catalog): https://www.ncbi.nlm.nih.gov/pathogens/refgene/

---

## ۵. ژنوتیپ در برابر فنوتیپ

ژنوم به ما **ژنوتیپ** می‌دهد؛ پزشک **فنوتیپ** (MIC و رده‌ی حساس/مقاوم) را لازم دارد. چند دلیل که این دو همیشه یکی نیستند:

1. **بیان ژن:** ‏`blaEC` در K-12 هست ولی K-12 به آمپی‌سیلین حساس است.
2. **ژن ناقص یا خاموش:** ‏`tet(A)` نیمه‌کاره، یا ژنی با کدون پایان زودرس (`INTERNAL_STOP`).
3. **چند جهش با هم:** یک جهش parC مقاومت کمی می‌دهد؛ gyrA + parC مقاومت بالا.
4. **سازوکار ناشناخته:** اگر پایگاه یک ژن را نداشته باشد، «پیدا نشد» به معنای «حساس» نیست.

برای سنجیدن، جدول ژنوتیپ را کنار نتیجه‌ی AST بگذارید و ناهمخوانی‌ها را یکی‌یکی توضیح دهید. این کار را در **تمرین ۶** با یک جدول فنوتیپ فرضی انجام می‌دهید.

**یک گزارش کمینه** برای هر ایزوله:

| بند | نمونه |
| :--- | :--- |
| ابزار و نسخه | ‏AMRFinderPlus 4.2.7 |
| پایگاه و نسخه | ‏2026-08-07.1 |
| گزینه‌ها | ‏`--organism Escherichia` (بی `--plus` برای گزارش بالینی) |
| ژن‌ها و جهش‌های core | ‏`blaCTX-M-15` (ALLELEX، ‏۱۰۰/۱۰۰)، `gyrA_S83L` |
| یافته‌های ناقص | جدا، با Method و درصد پوشش |
| پیش‌بینی فنوتیپ | «مقاومت به سفالوسپورین نسل سوم و کینولون، **پیش‌بینی‌شده**؛ با AST تأیید شود» |

> 📺 **فیلم:** دوره‌ی DTU در Coursera، بخش آزمون حساسیت و WGS: https://www.coursera.org/learn/antimicrobial-resistance
> 📄 **مرجع:** Bortolaia V, et al. (2020) (بالا)؛ ResFinder پیش‌بینی فنوتیپ را بر پایه‌ی پانل‌های EUCAST می‌دهد: https://genepi.food.dtu.dk/resfinder

---

## ۶. سه اشتباه رایج

1. ‏**«ABRicate جهش gyrA را نشان نداد، پس ایزوله به کینولون حساس است.»** ‏ABRicate جهش‌ها را اصلاً جست‌وجو نمی‌کند.
2. **یکی گرفتن نام‌ها.** ‏`blaCTX-M-15` (AMRFinderPlus)، `CTX-M-15` (CARD) و `blaCTX-M-15_1` (ResFinder) یک ژن‌اند. پیش از سنجیدن جدول‌ها نام‌ها را یکسان کنید.
3. **ننوشتن نسخه‌ی پایگاه.** شش ماه بعد پایگاه به‌روز شده و یک ژن تازه پیدا می‌شود؛ بی نسخه، کسی نمی‌فهمد چرا نتیجه عوض شد.

---

## 📘 برای کنجکاوها

- ‏RGI یک حالت `bwt` هم دارد که **ریدها** را مستقیم به CARD map می‌کند (برای متاژنوم، بخش ۰۶).
- ‏CARD یک بخش «Resistomes & Variants» دارد: پیش‌بینی‌های RGI روی هزاران ژنوم عمومی، که نشان می‌دهد هر ژن در کدام گونه‌ها و روی کروموزوم یا پلاسمید دیده شده است.
- برای *Klebsiella pneumoniae*، ابزار گونه‌محور **Kleborate** مقاومت، بیماری‌زایی و ST را با هم می‌دهد (ماژول ۰۲).

---

## جمع‌بندی

- ‏CARD یک هستی‌شناسی است: ژن ← خانواده، رده‌ی دارو، سازوکار. ‏RGI با رده‌های Perfect/Strict/Loose و آستانه‌ی هر مدل کار می‌کند.
- ‏ABRicate ساده و سریع است، چند پایگاه دارد، ولی جهش پیدا نمی‌کند و آستانه‌ی ثابت ۸۰/۸۰ دارد.
- اختلاف ابزارها پنج سرچشمه دارد: پایگاه، آستانه، DNA/پروتئین، نام، جهش.
- ژنوتیپ پیش‌بینی است؛ فنوتیپ را AST می‌دهد. گزارش باید نسخه‌ها، گزینه‌ها و یافته‌های ناقص را جدا بگوید.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
# RGI (CARD)
rgi load --card_json ./card.json --local
rgi main --input_sequence ASM.fna --output_file ID_rgi --input_type contig --local --clean
# ABRicate
abricate --list
abricate --db ncbi ASM1.fna ASM2.fna > abricate_ncbi.tsv
abricate --summary abricate_ncbi.tsv > summary.tsv
abricate --db ncbi --mincov 40 ASM.fna        # research only: see partial genes
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏CARD | پایگاه جامع مقاومت آنتی‌بیوتیکی (McMaster) |
| ‏ARO | هستی‌شناسی مقاومت آنتی‌بیوتیکی؛ شناسه‌ی هر ژن یا سازوکار در CARD |
| هستی‌شناسی (ontology) | واژگان ساختاریافته که مفهوم‌ها و پیوندشان را تعریف می‌کند |
| ‏protein homolog / variant model | مدلی که بودن ژن / بودن جهش معین را می‌سنجد |
| ‏Perfect / Strict / Loose | سه رده‌ی اطمینان در RGI |
| ‏bit-score | امتیاز هم‌ردیفی BLAST که به اندازه‌ی پایگاه وابسته نیست |
| ‏ResFinder | پایگاه و ابزار DTU برای ژن‌های اکتسابی، با پیش‌بینی فنوتیپ |
| ‏genotype / phenotype | آنچه در ژنوم هست / آنچه در آزمایش دیده می‌شود |
| ‏EUCAST | کمیته‌ی اروپایی آزمون حساسیت؛ مرزهای MIC را تعیین می‌کند |

---

## منابع

**مستند و مقاله**
- Alcock BP, et al. (2023). *CARD 2023: expanded curation, support for machine learning, and resistome prediction at the Comprehensive Antibiotic Resistance Database.* Nucleic Acids Research 51:D690–D699. https://doi.org/10.1093/nar/gkac920
- RGI documentation (rgi main): https://github.com/arpcard/rgi/blob/master/docs/rgi_main.rst · CARD: https://card.mcmaster.ca
- ABRicate README and source (v1.4.0): https://github.com/tseemann/abricate
- Bortolaia V, et al. (2020). *ResFinder 4.0 for predictions of phenotypes from genotypes.* J Antimicrob Chemother 75:3491–3500. https://doi.org/10.1093/jac/dkaa345
- NCBI Reference Gene Catalog: https://www.ncbi.nlm.nih.gov/pathogens/refgene/

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Antimicrobial resistance – theory and methods* (DTU): https://www.coursera.org/learn/antimicrobial-resistance
- ‏Coursera: *Whole genome sequencing of bacterial genomes – tools and applications* (DTU): https://www.coursera.org/learn/wgs-bacteria
- ‏edX: دوره‌ای ویژه در edX نیافتیم؛ نزدیک‌ترین: *Antimicrobial Stewardship* (Stanford): https://www.edx.org/learn/medicine/stanford-university-antimicrobial-stewardship-improving-clinical-outcomes-by-optimization-of-antibiotic-practices
- ‏YouTube: *Brian Alcock – The Comprehensive Antibiotic Resistance Database*: https://www.youtube.com/watch?v=XKWfUbiQW8Q
- ‏YouTube: *Antimicrobial Resistance Genes Detection using ABRicate tutorial*: https://www.youtube.com/watch?v=cmhuWRorCTg
- ‏YouTube: ABRicate در Galaxy: https://www.youtube.com/watch?v=n3OtDyWixpw
- ‏YouTube: *Antibiotic Resistance Mechanisms*: https://www.youtube.com/watch?v=xYhHI-ddFJI

<sub>رده‌های Perfect/Strict/Loose و ستون‌های RGI در 2026-10-24 از مستند rgi_main.rst خوانده شد؛ پایگاه‌ها و ستون‌های ABRicate از README، و پیش‌فرض‌های `--minid`/`--mincov` از `bin/abricate` (VERSION 1.4.0). نشانی‌های فیلم از جست‌وجوی وب در 2026-10-24‌اند؛ در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
