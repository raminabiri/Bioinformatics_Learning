<div dir="rtl">

# درس ۱: آنوتیشن ژنوم باکتری؛ کجا چه ژنی است؟

**بخش:** `07_Bacterial_Genomics` · **ماژول:** `02_Genome_Annotation` · **پیش‌نیاز:** ماژول [اسمبلی](../01_Assembly_Quality/)؛ [فرمت GFF](../../02_BioLinux/03_Annotation_Formats/)؛ [Biopython و GenBank](../../03_Python/05_Biopython_GenBank/) · **زمان:** حدود ۷۵ دقیقه · **ابزار:** اجراشده: Pyrodigal 3.7.1، barrnap، ARAGORN 1.2.41، tRNAscan-SE 2.0.13؛ از مستندات: Bakta 1.12.1 (پایگاه v6.0)، Prokka 1.15.6 · **آخرین بازبینی:** 2026-10-21

> ✍️ **وضعیت:** بخش‌های سبک (پیش‌بینی ژن، rRNA، tRNA و سنجش با RefSeq) روی ژنوم *E. coli* K-12 **اجرا شده‌اند** (۱۴ ثانیه، 2026-10-15) و خروجی‌شان واقعی است. Bakta و Prokka (چند دقیقه برای هر ژنوم، و پایگاه ۴ تا ۸۴ گیگابایتی برای Bakta) **اجرا نشده‌اند**؛ دستورها و توضیح خروجی‌ها از مستندات رسمی است.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. آنوتیشن **ساختاری** (کجا؟) و **کارکردی** (چه می‌کند؟) را از هم جدا کنید.
2. ژن‌ها را با Pyrodigal پیش‌بینی کنید و ستون‌های GFF آن را بخوانید.
3. پیش‌بینی را با آنوتیشن مرجع بسنجید و خطاهای رایج را بشناسید: کدون آغاز، پروتئین‌های کوچک، سلنوسیستئین، جابه‌جایی چارچوب، ژن کاذب.
4. ‏rRNA و tRNA را پیدا کنید و یک «tRNA اضافه» را تفسیر کنید.
5. ‏Bakta یا Prokka را با گزینه‌های درست اجرا کنید و نسخه‌ی پایگاه را گزارش کنید.

**پیش از آغاز:** ابزارهای سبک این ماژول در محیط [`envs/bacterial_genomics.yml`](../../envs/bacterial_genomics.yml) هستند (یک بار: `conda env create -f …`):

<div dir="ltr">

```bash
conda activate bacterial_genomics
cd ~/genomes
G=~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data
S=~/Bioinformatics_Learning-main/07_Bacterial_Genomics/99_scripts_data/02_Genome_Annotation/scripts
```

</div>

---

## ۱. داستان

خروجی ماژول ۰۱ یک فایل `contigs.fa` است: کمابیش ۵ میلیون حرف A، C، G و T. برای اینکه بفهمیم ژن مقاومت کجاست، کدام مسیر متابولیکی کامل است، یا دو ایزوله در چه ژن‌هایی فرق دارند، باید بدانیم **کجای این توالی چه چیزی است**. این کار **آنوتیشن** است و دو لایه دارد:

| لایه | پرسش | ابزار نمونه |
| :--- | :--- | :--- |
| **ساختاری** | ژن‌ها، RNAها و عناصر **کجا**یند؟ (مختصات، رشته، چارچوب) | Pyrodigal، barrnap، tRNAscan-SE |
| **کارکردی** | هر ژن **چه می‌کند**؟ (نام، محصول، EC، GO) | جست‌وجو در پایگاه با DIAMOND یا HMMER؛ Bakta و Prokka هر دو لایه را با هم دارند |

آنوتیشن **پیش‌بینی** است، نه اندازه‌گیری؛ خطاهایش در هر تحلیل بعدی (پن‌ژنوم، مقاومت، ارسال به NCBI) تکثیر می‌شوند. این درس نشان می‌دهد کجا رخ می‌دهند.

---

## ۲. مفهوم: پیدا کردن ژن در باکتری

در باکتری و آرکی **اینترون کمابیش نیست**، کمابیش ۸۸٪ ژنوم کدکننده است، و هر ژن یک **ORF** پیوسته است، از کدون آغاز تا کدون پایان. پس پرسش اصلی: «از همه‌ی ORFهای شدنی، کدام‌ها ژن واقعی‌اند و از کدام کدون آغاز می‌شوند؟»

‏**Prodigal** ابزار استاندارد است؛ **Pyrodigal** بازنویسی آن با همان الگوریتم (و همانی که Bakta به کار می‌برد):
1. **یادگیری از همان ژنوم** (حالت `single`): الگوی GC در سه جایگاه کدون، کدون‌های آغاز رایج، و **موتیف اتصال ریبوزوم** (RBS، Shine–Dalgarno، مانند `AGGAGG`). برای همین کمابیش ۲۰ کیلوباز یا بیشتر توالی می‌خواهد.
2. **امتیاز** به هر ORF و برگزیدن مجموعه‌ای کم‌هم‌پوشان.
3. **برگزیدن کدون آغاز** بر پایه‌ی RBS و گونه‌ی کدون (ATG، GTG، TTG).

حالت **`meta`** (`-p meta`): برای توالی کوتاه (کمتر از کمابیش ۲۰ کیلوباز)، فاژ، پلاسمید تنها یا متاژنوم؛ از مدل‌های از پیش آموخته به کار می‌برد. **جدول ژنتیکی** پیش‌فرض ۱۱ است؛ برای *Mycoplasma* جدول **۴** (TGA = تریپتوفان).

---

## ۳. گام ۱: Pyrodigal روی *E. coli* K-12 (اجراشده)

<div dir="ltr">

```bash
bash $S/light_annotation.sh
```

</div>

اسکریپت چهار ابزار را پشت سر هم اجرا می‌کند و خروجی‌ها را در `annotation/` می‌نویسد. گام نخستش:

<div dir="ltr">

```bash
pyrodigal -i $G/ecoli_k12.fna -g 11 -f gff -o annotation/pyrodigal.gff -a annotation/pyrodigal.faa
```

</div>

| بخش | چیست |
| :--- | :--- |
| ① `-i` | ژنوم (FASTA) |
| ② `-g 11` | جدول ژنتیکی باکتری‌ها |
| ③ `-f gff -o` | خروجی GFF |
| ④ `-a` | توالی پروتئین هر ژن (FASTA) |

<div dir="ltr">

```text
== 1. Pyrodigal (single mode, translation table 11)
predicted CDS: 4319
```

</div>

۱٫۴ ثانیه. ستون ۹ یک سطر GFF:

<div dir="ltr">

```text
ID=NC_000913.3_2;partial=00;start_type=ATG;rbs_motif=GGAG/GAGG;rbs_spacer=5-10bp;gc_cont=0.531;conf=99.99;score=336.87;...
```

</div>

- ‏`partial=00`: هر دو سر کامل‌اند؛ `10` یعنی ژن از لبه‌ی چپ توالی بیرون زده. **نخستین ژن پیش‌بینی‌شده** همین `partial=10` را دارد: ژنومی که **دایره‌ای** است، در FASTA خطی نوشته شده و ژنی که از مبدأ مختصات می‌گذرد، دو تکه دیده می‌شود (تمرین ۱).
- ‏`rbs_motif`: موتیف Shine–Dalgarno یافته‌شده؛ `conf`: اطمینان (۰ تا ۱۰۰).

### سنجش با آنوتیشن مرجع RefSeq

دو CDS را «یک ژن» می‌گیریم اگر **رشته و کدون پایان** یکسان داشته باشند (ابزارها در پایان کمابیش همیشه همخوان‌اند؛ ناهمخوانی در **آغاز** است):

<div dir="ltr">

```text
reference CDS: 4300 with 4290 distinct stops  (+ 18 pseudogene CDS)   predicted CDS: 4319
same stop:                 4119  (96.0% of reference)
  ... and same start:      3889  (94.4% of matched)
  ... different start:     230
      predicted longer: 89   shorter: 141
reference only (missed):   171
predicted only:            200  (of which on a reference pseudogene: 11)
missed genes by length:    {'<100 aa': 157, '>=100 aa': 14}
shortest missed: baxL (8 aa), yhgP (9 aa), evgL (9 aa), ykfO (10 aa), ybgV (10 aa)
longest missed:  yoeF (118 aa), yfdG (120 aa), mbiA (161 aa), yzcX (161 aa), dnaX (430 aa)
largest start disagreements: stfR (1365 nt), fdnG (636 nt), fdoG (636 nt), insK (486 nt), fdhF (468 nt)
```

</div>

1. **۹۶٪ ژن‌های مرجع** با همان کدون پایان پیدا شدند: پیش‌بینی برای باکتری خوب کار می‌کند.
2. **کدون آغاز** در ۵٫۶٪ ژن‌های همخوان فرق دارد (۲۳۰ ژن). آغاز نادرست یعنی **انتهای N نادرست**: پپتید سیگنال گم یا افزوده می‌شود.
3. **۱۷۱ ژن از دست رفت**؛ ۱۵۷ تا (۹۲٪) **کوتاه‌تر از ۱۰۰ اسیدآمینه**‌اند، کوتاه‌ترینشان ۸ تا ۱۰ (مانند *baxL*). این پروتئین‌های کوچک (sORF) را بیشتر با پروتئومیکس کشف کرده‌اند؛ هیچ ابزار پیش‌بینی آن‌ها را با اطمینان نمی‌یابد.
4. ‏***dnaX* (۴۳۰ اسیدآمینه)** از دست رفت، چون زیرواحد γ آن با **لغزش ریبوزوم** (جابه‌جایی چارچوب −۱) ساخته می‌شود؛ در GFF مرجع دو تکه دارد با `exception=ribosomal slippage`.
5. **سه سلنوپروتئین** (*fdnG*، *fdoG*، *fdhF*): Pyrodigal کدون **TGA سلنوسیستئین** را پایان خوانده و ژن را **پس از** آن آغاز کرده است (`transl_except` در GFF مرجع؛ بخش ۰۳، ماژول ۰۵).
6. **۲۰۰ پیش‌بینی بی همتا در مرجع:** ۱۱ تا روی **ژن کاذب** مرجع‌اند؛ بقیه بیشتر ORFهای کوتاه کم‌اطمینان‌اند.

**درس:** حتی برای بهترین ژنوم شناخته‌شده، کمابیش ۴٪ ژن‌ها از دست می‌روند و ۵٪ کدون آغاز نادرست دارند. استثناهای زیستی جایی است که پیش‌بینی خودکار شکست می‌خورد.

---

## ۴. گام ۲: RNAها (اجراشده)

### ‏rRNA با barrnap

<div dir="ltr">

```text
== 3. rRNA with barrnap
      7 Name=16S_rRNA
      7 Name=23S_rRNA
      8 Name=5S_rRNA
```

</div>

۲۲ ژن rRNA، **دقیقاً** برابر RefSeq: هفت اپرون (ماژول ۰۱)، که *rrnD* یک 5S افزوده دارد. **هشدار:** در اسمبلی Illumina اپرون‌ها فشرده می‌شوند؛ barrnap روی `contigs.fa` بیشتر **۱ تا ۳ نسخه** می‌یابد، نه ۷.

### ‏tRNA: دو ابزار، سه عدد

<div dir="ltr">

```text
== 4. tRNA with ARAGORN and tRNAscan-SE (bacterial model)
88 genes found
tRNAscan-SE: 89 tRNAs   RefSeq: 86
```

</div>

‏Prokka، ARAGORN را به کار می‌برد و Bakta، tRNAscan-SE را. هر دو **بیشتر از RefSeq** یافتند. سه tRNA‌ی tRNAscan-SE که در RefSeq نیستند:

| جایگاه | گونه | امتیاز | در RefSeq |
| :--- | :--- | ---: | :--- |
| 297,184–297,254 | Thr (CGT) | 44.2 | مرز پایانی **پروفاژ خفته‌ی CP4-6** |
| 586,007–586,101 | Undet، `pseudo` | 31.7 | مرز پایانی **پروفاژ DLP12** |
| 2,755,859–2,755,955 | Undet | 29.6 | ژن ***ssrA*** = **tmRNA**، کنار آغاز **پروفاژ CP4-57** |

الگویی شناخته‌شده: **فاژهای معتدل بیشتر درون یا کنار ژن‌های tRNA وارد کروموزوم می‌شوند**؛ توالی اتصال بخشی از tRNA را تکرار می‌کند و یک **تکه‌ی tRNA** در مرز پروفاژ می‌ماند. امتیاز پایین (۳۰ تا ۴۴، در برابر کمابیش ۸۰ برای tRNAهای واقعی) با «tRNA ناقص» سازگار است. درس ۲ دوباره به آن برمی‌گردد.

<details>
<summary>✋ امتحان کن: چرا «۸۹ tRNA» از tRNAscan-SE را بی‌درنگ «سه tRNA تازه» نخوانیم؟</summary>

چون جایگاه و امتیاز می‌گویند این سه، tRNAهای کامل و کارا نیستند: دو تکه‌ی tRNA در مرز پروفاژها و یک tmRNA. پیش از هر ادعایی، جایگاه (در کنار چه چیزی؟) و امتیاز را ببینید.

</details>

---

## ۵. گام ۳: آنوتیشن کامل با Bakta یا Prokka (از مستندات)

### ۵.۱ سلسله‌مراتب شواهد

هر ابزار آنوتیشن کارکردی همین منطق را دارد، از درست‌ترین به کلی‌ترین: **یکسانی کامل** با پروتئینی شناخته‌شده ← **همسانی بالا** با خانواده‌ای بازبینی‌شده ← **همسانی متوسط** با خوشه‌ای بزرگ‌تر ← **دامنه‌ی حفاظت‌شده** (Pfam) ← **هیچ**: «hypothetical protein».

### ‏۵.۲ Bakta

به گفته‌ی README رسمی، Bakta پس از پیش‌بینی با Pyrodigal، هش **MD5** هر پروتئین را با صدها میلیون پروتئین UniParc، UniRef100 و RefSeq می‌سنجد (**شناسایی بی هم‌ترازی**)؛ بقیه را با DIAMOND در برابر خوشه‌های UniRef90 و UniRef50 هم‌تراز می‌کند؛ و AMRFinderPlus (مقاومت)، VFDB (ضراوت)، پروتئین‌های کوچک، سلنوسیستئین و ژن کاذب را جدا بررسی می‌کند.

<div dir="ltr">

```bash
bakta --db /path/to/db-light --output bakta_out --prefix isolateA \
  --genus Escherichia --species coli --strain A \
  --locus-tag ECA --gram - --threads 8 shovill_out/contigs.fa
```

</div>

| بخش | چرا |
| :--- | :--- |
| ① `--db` | پایگاه. **light**: ۱٫۳ گیگابایت فشرده، ۳٫۹ باز؛ **full**: ۳۰ فشرده، ۸۴ باز. light نام‌های کلی‌تری می‌دهد |
| ② `--genus/--species/--strain` | تنها در فایل‌های خروجی نوشته می‌شوند؛ روی پیش‌بینی اثری ندارند |
| ③ `--locus-tag` | پیشوند شناسه‌ی ژن‌ها (`ECA_00001`)؛ برای ارسال به NCBI باید **ثبت‌شده** باشد |
| ④ `--gram -` | برای پیش‌بینی پپتید سیگنال (*E. coli* گرم‌منفی) |
| ⑤ `--threads 8` | هسته‌ها |

گزینه‌های دیگر: `--complete` (همه‌ی توالی‌ها replicon کامل و دایره‌ای‌اند)، `--translation-table 4`، `--compliant` (سازگار با GenBank)، `--proteins` (پروتئین‌های مورد اعتماد خودتان، با اولویت).

| خروجی | محتوا |
| :--- | :--- |
| `.gff3` | آنوتیشن + توالی (ورودی Panaroo، ماژول ۰۴) |
| `.gbff` | ‏GenBank (ورودی Snippy، ماژول ۰۵؛ و Artemis) |
| `.faa` / `.ffn` | پروتئین / نوکلئوتید هر ژن |
| `.tsv` | جدول ساده‌ی همه‌ی ویژگی‌ها |
| `.txt` | خلاصه: شمار هر گونه ویژگی |

### ‏۵.۳ Prokka

<div dir="ltr">

```bash
prokka --outdir prokka_out --prefix isolateA --kingdom Bacteria --genus Escherichia --species coli \
  --strain A --locustag ECA --gram neg --cpus 8 --compliant shovill_out/contigs.fa
```

</div>

‏`--kingdom` (Archaea، Bacteria، Mitochondria، Viruses) جدول ژنتیکی را تنظیم می‌کند؛ `--compliant` = `--addgenes --mincontiglen 200 --centre XXX`. خروجی‌ها همانند Bakta (`.gff`، `.gbk`، `.faa`، …).

| | Bakta | Prokka |
| :--- | :--- | :--- |
| پایگاه | بزرگ و به‌روز، با نسخه‌ی روشن | کوچک‌تر، درونی |
| ارجاع پایدار (`WP_`، `UniRef`) | ✅ | ❌ |
| پروتئین کوچک، ژن کاذب، سلنوسیستئین | ✅ | ❌ |
| سرعت و فضای دیسک | کندتر | سریع، بی پایگاه جدا |

برای کار تازه **Bakta**؛ و **نسخه‌ی ابزار و پایگاه** را همیشه گزارش کنید.

---

## ۶. سه اشتباه رایج

**۱. جدول ژنتیکی ۱۱ برای *Mycoplasma*.** هر ژنی با TGA درونی بریده می‌شود؛ `--translation-table 4` (Bakta) یا `--gcode 4` (Prokka).

**۲. «نبودن ژن» = «نبودن کارکرد».** پروتئین‌های کوچک و ژن‌های لبه‌ی کانتیگ از دست می‌روند (۱۵۷ ژن کوچک در *E. coli*). پیش از ادعای «ندارد»، مستقیم بجویید (برای نمونه tblastn).

**۳. آنوتیشن ایزوله‌ها با دو ابزار یا دو نسخه‌ی پایگاه.** نام‌های گوناگون در پن‌ژنوم (ماژول ۰۴) به شکل «ژن‌های گوناگون» دیده می‌شوند. یک ابزار و یک نسخه برای همه.

---

## 📘 برای کنجکاوها

- ‏**‏PGAP:** ‏NCBI ژنوم‌های RefSeq را با گردش کار خودش (PGAP) آنوتیت می‌کند؛ هنگام ارسال به GenBank هم می‌توانید آن را بخواهید.
- **لایه‌های بیشتر:** eggNOG-mapper (ارتولوگ، COG، GO، KEGG)، InterProScan (دامنه‌ها)، AMRFinderPlus و CARD (مقاومت؛ بخش ۰۸).
- **ستون ۹ GFF3 Bakta و Prokka** «percent-encoded» است (`%2C` = ویرگول)، و پس از `##FASTA` توالی هم آمده است.

---

## جمع‌بندی

- آنوتیشن = ساختاری (کجا) + کارکردی (چه)؛ پیش‌بینی است و خطا دارد.
- ‏Pyrodigal روی *E. coli*: ۹۶٪ ژن‌ها با پایان درست، ولی ۵٪ آغاز گوناگون و ۱۷۱ ژن از دست رفته (بیشتر کوچک‌تر از ۱۰۰ اسیدآمینه)؛ سلنوپروتئین‌ها و *dnaX* استثناهای زیستی‌اند.
- ‏barrnap دقیق است (۲۲ از ۲۲) ولی در اسمبلی کوتاه‌رید فشرده می‌شود؛ tRNAهای «افزوده» در مرز پروفاژها، رد پای ورود فاژند.
- ‏Bakta برای کار تازه؛ نسخه‌ی پایگاه را گزارش کنید.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
pyrodigal -i genome.fna -g 11 -f gff -o genes.gff -a proteins.faa       # [-p meta] [-c]
barrnap --kingdom bac --threads 4 genome.fna > rrna.gff
aragorn -t -gc11 -w genome.fna -o aragorn.txt
tRNAscan-SE -B --thread 4 -q -o trnascan.txt genome.fna
bakta --db DB --output out --prefix X --locus-tag X --gram - --threads 8 contigs.fa
prokka --outdir out --prefix X --kingdom Bacteria --locustag X --gram neg --cpus 8 --compliant contigs.fa
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| آنوتیشن ساختاری / کارکردی | جای ژن‌ها / کار ژن‌ها |
| ‏ORF | چارچوب خواندن باز: از کدون آغاز تا کدون پایان |
| ‏RBS (Shine–Dalgarno) | توالی اتصال ریبوزوم پیش از کدون آغاز |
| ژن کاذب (*pseudogene*) | ژنی که با جهش کارایی‌اش را از دست داده |
| سلنوسیستئین | اسیدآمینه‌ای که با کدون TGA (در بسیاری از موارد پایان) رمز می‌شود |
| ‏tmRNA | ‏RNAیی که ریبوزوم‌های گیرکرده را آزاد می‌کند (ژن *ssrA*) |
| ‏locus tag | شناسه‌ی یکتای هر ژن در یک ژنوم |

---

## منابع

**مستند و مقاله**
- Hyatt D, et al. (2010). *Prodigal: prokaryotic gene recognition and translation initiation site identification.* BMC Bioinformatics 11:119. https://doi.org/10.1186/1471-2105-11-119
- Larralde M (2022). *Pyrodigal: Python bindings and interface to Prodigal.* JOSS 7(72):4296. https://doi.org/10.21105/joss.04296
- Schwengers O, et al. (2021). *Bakta: rapid and standardized annotation of bacterial genomes via alignment-free sequence identification.* Microbial Genomics 7:000685. https://doi.org/10.1099/mgen.0.000685
- Seemann T (2014). *Prokka: rapid prokaryotic genome annotation.* Bioinformatics 30:2068–2069. https://doi.org/10.1093/bioinformatics/btu153
- Chan PP, et al. (2021). *tRNAscan-SE 2.0.* Nucleic Acids Research 49:9077–9096. https://doi.org/10.1093/nar/gkab688
- Laslett D, Canback B (2004). *ARAGORN, a program to detect tRNA genes and tmRNA genes in nucleotide sequences.* Nucleic Acids Research 32:11–16. https://doi.org/10.1093/nar/gkh152
- Bakta: https://github.com/oschwengers/bakta · Prokka: https://github.com/tseemann/prokka · barrnap: https://github.com/tseemann/barrnap

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins University). دوره‌ای ویژه‌ی آنوتیشن ژنوم باکتری در Coursera نیافتیم؛ نزدیک‌ترین: https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Linux* (The Linux Foundation). دوره‌ای ویژه در edX نیافتیم؛ نزدیک‌ترین: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux
- YouTube: *Gene Prediction Approaches and Common Methods for Bacterial Gene Prediction* (NPTEL, IIT Madras): https://www.youtube.com/watch?v=q19Ur8bi64k
- YouTube: *GTN Tutorial: Bacterial Genome Annotation* (Galaxy Project، Bakta): https://www.youtube.com/watch?v=VOwplmv0vNs
- YouTube: *GTN Training: Annotation of a Prokaryotic Genome* (Galaxy Project، Prokka): https://www.youtube.com/watch?v=B8pIQZPf21Y

<sub>نشانی‌های YouTube و DOIها در 2026-10-15 وارسی شدند؛ نشانی‌های Coursera و edX در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
