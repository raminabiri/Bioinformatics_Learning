# درس ۱: آنوتیشن ژنوم باکتری و آرکی

**بخش:** `07_Bacterial_Genomics` · **ماژول:** `02_Genome_Annotation` · **پیش‌نیاز:** ماژول ۰۱ (اسمبلی)، 02_Programming/01 (Biopython و GFF) · **زمان:** ۲ ساعت · **ابزار:** Pyrodigal 3.7.1، barrnap 1.10.5، ARAGORN 1.2.41، tRNAscan-SE 2.0.13، Bakta 1.12.1 (دیتابیس v6.0)، Prokka 1.15.6 · **آخرین بازبینی:** 2026-10-15

> ✍️ **وضعیت:** بخش‌های سبک (پیش‌بینی ژن، rRNA، tRNA و مقایسه با RefSeq) روی ژنوم *E. coli* K-12 **اجرا شده‌اند** (۱۴ ثانیه، [scripts/light_annotation.sh](scripts/light_annotation.sh)) و خروجی‌شان واقعی است. اجرای کامل Bakta و Prokka (چند دقیقه برای هر ژنوم، و دیتابیس ۴ تا ۸۴ گیگابایتی برای Bakta) در دوره **اجرا نشده**. دستورها و توضیح خروجی‌هایشان از مستندات رسمی است.

---

## ۱. مسئله

خروجی ماژول ۰۱ یک فایل `contigs.fa` است: حدود ۵ میلیون حرف A، C، G و T. برای اینکه بفهمیم ژن مقاومت کجاست، کدام مسیر متابولیک کامل است، یا دو ایزوله در چه ژن‌هایی فرق دارند، باید بدانیم **کجای این توالی چه چیزی است**. این کار **آنوتیشن** است و دو لایه دارد:

| لایه | سؤال | ابزار نمونه |
| :--- | :--- | :--- |
| **ساختاری (structural)** | ژن‌ها، RNAها و عناصر **کجا** هستند؟ (مختصات، رشته، قاب) | Pyrodigal، barrnap، tRNAscan-SE، Infernal، MinCED |
| **عملکردی (functional)** | هر ژن **چه می‌کند**؟ (نام، محصول، EC، GO، COG) | جستجو در دیتابیس با DIAMOND، BLAST، HMMER؛ Bakta و Prokka هر دو لایه را ترکیب می‌کنند |

آنوتیشن **پیش‌بینی** است، نه اندازه‌گیری. خطاهای آن در هر تحلیل بعدی (پن‌ژنوم، مقاومت، ارسال به NCBI) تکثیر می‌شوند. این درس نشان می‌دهد این خطاها کجا رخ می‌دهند.

## ۲. پیش‌بینی ژن در پروکاریوت‌ها

### ۲.۱ چرا نسبتاً آسان است؟
در باکتری و آرکی: **intron تقریباً وجود ندارد**، حدود ۸۸٪ ژنوم کدکننده است (ژن‌ها پشت سر هم)، و هر ژن یک **ORF** پیوسته است، از کدون آغاز تا کدون پایان. پس سؤال اصلی این است: «از میان همه‌ی ORFهای ممکن، کدام‌ها ژن واقعی‌اند و از کدام کدون آغاز شروع می‌شوند؟»

### ۲.۲ Prodigal و Pyrodigal
**Prodigal** (Hyatt et al. 2010) ابزار استاندارد است. **Pyrodigal** بازنویسی آن با رابط Python است (همان الگوریتم، سریع‌تر) و Bakta از آن استفاده می‌کند. مراحل:
1. **آموزش روی همان ژنوم** (حالت `single`): الگوی GC در سه جایگاه کدون، کدون‌های آغاز رایج، و **موتیف اتصال ریبوزوم** (RBS، Shine–Dalgarno، مثل `AGGAGG`) را از خود ژنوم یاد می‌گیرد. برای همین به حدود ۲۰ کیلوباز توالی یا بیشتر نیاز دارد.
2. **امتیازدهی** به هر ORF و انتخاب مجموعه‌ای بدون همپوشانی زیاد با برنامه‌ریزی پویا.
3. **انتخاب کدون آغاز** بر اساس موتیف RBS و نوع کدون (ATG، GTG، TTG).

حالت **`meta`** (`-p meta`): برای توالی کوتاه (کمتر از حدود ۲۰ کیلوباز)، فاژ، پلاسمید تنها، یا متاژنوم. به جای آموزش، از مدل‌های از پیش آموزش‌دیده استفاده می‌کند.

**جدول ژنتیکی:** پیش‌فرض ۱۱ است. استثنای مهم: *Mycoplasma* و *Spiroplasma* (جدول **۴**، که در آن TGA تریپتوفان است). اگر جدول ۱۱ را برای *Mycoplasma* بدهید، هر ژنی با TGA داخلی **قطع** می‌شود.

### ۲.۳ اجرا روی *E. coli* K-12 و مقایسه با RefSeq (اجراشده)
```bash
cd 07_Bacterial_Genomics/02_Genome_Annotation
bash scripts/light_annotation.sh
```
```text
== 1. Pyrodigal (single mode, translation table 11)
predicted CDS: 4319
```
اجرا **۱٫۴ ثانیه** طول کشید. یک خط خروجی GFF:
```text
ID=NC_000913.3_2;partial=00;start_type=ATG;rbs_motif=GGAG/GAGG;rbs_spacer=5-10bp;gc_cont=0.531;conf=99.99;score=336.87;...
```
- `partial=00`: هر دو انتها کامل‌اند. `10` یعنی ژن از لبه‌ی چپ توالی بیرون زده است. **اولین ژن پیش‌بینی‌شده** (`NC_000913.3_1`) همین `partial=10` و `start_type=Edge` را دارد: ژنومی که در واقع **دایره‌ای** است، در FASTA خطی نوشته شده و ژنی که از مبدأ مختصات رد می‌شود، دو تکه دیده می‌شود. Bakta با `--complete` و Prodigal با `-c` (closed ends) این را مدیریت می‌کنند.
- `rbs_motif`: موتیف Shine–Dalgarno‌ای که پیدا شده. `conf`: اطمینان (۰ تا ۱۰۰).

مقایسه با آنوتیشن مرجع RefSeq، که برای این ژنوم مرجع با بازبینی دستی نگهداری می‌شود. دو CDS را «یک ژن» می‌گیریم اگر **رشته و کدون پایان** یکسان داشته باشند. ابزارهای پیش‌بینی ژن در کدون پایان تقریباً همیشه توافق دارند، اختلاف در **آغاز** است.
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

تفسیر:
1. **۹۶٪ ژن‌های مرجع** با همان کدون پایان پیدا شدند. پیش‌بینی ab initio برای باکتری خوب کار می‌کند.
2. **کدون آغاز** در ۵٫۶٪ ژن‌های مطابق فرق دارد (۲۳۰ ژن). کدون آغاز اشتباه یعنی **انتهای N پروتئین اشتباه**: پپتید سیگنال گم می‌شود یا اضافه می‌شود، و طول پروتئین در مقایسه‌ها فرق می‌کند.
3. **۱۷۱ ژن از دست رفته**، که **۱۵۷ تا (۹۲٪) کوتاه‌تر از ۱۰۰ اسیدآمینه‌اند**. کوتاه‌ترین‌ها ۸ تا ۱۰ اسیدآمینه‌اند (مثل *baxL*). این پروتئین‌های کوچک (sORF) را بیشتر با پروتئومیکس و ریبوزوم‌پروفایلینگ کشف کرده‌اند. هیچ ابزار ab initio آن‌ها را با اطمینان پیدا نمی‌کند. Bakta برای همین یک مرحله‌ی جداگانه دارد: sORFهای کوتاه‌تر از ۳۰ اسیدآمینه را فقط وقتی نگه می‌دارد که با پروتئین‌های کوچک **شناخته‌شده** در دیتابیسش مطابقت داشته باشند (اول با هش دقیق) و از فیلترهای سخت‌گیرانه‌ی همپوشانی رد شوند.
4. ***dnaX* (۴۳۰ اسیدآمینه)** از دست رفته، چون زیرواحد γ آن با **لغزش ریبوزومی** (ribosomal slippage، جابه‌جایی چارچوب −۱) ساخته می‌شود. در GFF مرجع دو تکه دارد با `exception=ribosomal slippage`:
   ```text
   492092  493375  +  ... product=DNA polymerase III subunit gamma
   493375  493386  +  ... product=DNA polymerase III subunit gamma
   ```
   کدون پایان γ در قاب دیگری است، پس هیچ ORF ساده‌ای به آن نمی‌رسد.
5. **سه سلنوپروتئین** (*fdnG*، *fdoG*، *fdhF*) با ۴۶۸ تا ۶۳۶ نوکلئوتید اختلاف آغاز: Pyrodigal کدون **TGA سلنوسیستئین** را پایان خوانده و ژن را **بعد از** آن شروع کرده است. همان استثنایی که در ماژول 02/01 دیدیم (`transl_except`). Bakta یک مرحله‌ی جدا برای «استثنای ترجمه (سلنوسیستئین)» دارد.
6. **۲۰۰ پیش‌بینی بدون معادل در مرجع:** ۱۱ تا روی **ژن کاذب** مرجع‌اند (ابزار یک ORF می‌بیند، ولی بازبین می‌داند ژن خراب است). بقیه اغلب ORFهای کوتاه و کم‌اطمینان‌اند که بازبین‌ها رد کرده‌اند.

**درس:** حتی برای بهترین ژنوم شناخته‌شده، حدود ۴٪ ژن‌ها از دست می‌روند و ۵٪ کدون آغاز اشتباه دارند. استثناهای زیستی (سلنوسیستئین، جابه‌جایی چارچوب برنامه‌ریزی‌شده، ژن کاذب، پروتئین‌های بسیار کوچک) جایی است که پیش‌بینی خودکار شکست می‌خورد.

## ۳. RNAها و عناصر دیگر

### ۳.۱ rRNA با barrnap (اجراشده)
```text
== 3. rRNA with barrnap
      7 Name=16S_rRNA
      7 Name=23S_rRNA
      8 Name=5S_rRNA
```
۲۲ ژن rRNA، **دقیقاً** برابر RefSeq. هفت اپرون (درس ۰۱) که اپرون *rrnD* یک 5S اضافه دارد. barrnap با مدل‌های HMM ساخته شده و در ۴ ثانیه اجرا شد. **هشدار:** در اسمبلی Illumina، اپرون‌های rRNA فشرده می‌شوند (ماژول ۰۱، تمرین ۵). پس barrnap روی `contigs.fa` معمولاً **۱ تا ۳ نسخه** پیدا می‌کند، نه ۷. «تعداد نسخه‌ی rRNA» از اسمبلی کوتاه‌رید قابل گزارش نیست.

### ۳.۲ tRNA: دو ابزار، سه عدد (اجراشده)
```text
== 4. tRNA with ARAGORN and tRNAscan-SE (bacterial model)
88 genes found
tRNAscan-SE: 89 tRNAs   RefSeq: 86
```
Prokka از ARAGORN و Bakta از tRNAscan-SE استفاده می‌کند. هر دو **بیشتر از RefSeq** پیدا کردند. سه مورد tRNAscan-SE که در RefSeq tRNA نیستند:

| موقعیت | نوع (tRNAscan-SE) | امتیاز | در RefSeq |
| :--- | :--- | ---: | :--- |
| 297,184–297,254 | Thr (CGT) | 44.2 | مرز پایانی **پروفاژ خفته‌ی CP4-6** (262,898–297,205) |
| 586,007–586,101 | Undet، `pseudo` | 31.7 | مرز پایانی **پروفاژ DLP12** (564,755–586,056) |
| 2,755,859–2,755,955 | Undet | 29.6 | ژن ***ssrA*** = **tmRNA**، کنار شروع **پروفاژ CP4-57** (از 2,755,941) |

این یک الگوی زیستی شناخته‌شده است: **فاژهای معتدل اغلب درون یا کنار ژن‌های tRNA (و tmRNA) وارد کروموزوم می‌شوند.** توالی اتصال (att) بخشی از tRNA را تکرار می‌کند. در نتیجه یک **تکه‌ی tRNA** در مرز پروفاژ باقی می‌ماند. امتیاز پایین (۳۰ تا ۴۴، در برابر حدود ۸۰ برای tRNAهای واقعی) با «tRNA ناقص» سازگار است. این را در درس ۲ (فاژ) دوباره می‌بینیم.

چند نکته‌ی دیگر از همین خروجی:
- **یک tRNA-SeC (Sec، آنتی‌کدون TCA)**: محصول ژن *selC* که TGA را در سه سلنوپروتئین بخش ۲.۳ می‌خواند.
- **۲ tRNA از نوع `Ile2` (آنتی‌کدون CAT)**: ظاهراً tRNA متیونین است، ولی با تغییر بعد از رونویسی (lysidine) کدون **AUA** (ایزولوسین) را می‌خواند. ابزارهای ساده‌تر آن را Met می‌نامند.

### ۳.۳ بقیه‌ی عناصر
| عنصر | ابزار رایج | در Bakta | در Prokka |
| :--- | :--- | :--- | :--- |
| tmRNA | ARAGORN | ✅ | ✅ |
| ncRNA و riboswitch | Infernal + Rfam | ✅ | با `--rfam` (کند) |
| آرایه‌ی CRISPR | PILER-CR، MinCED | ✅ | ✅ (MinCED) |
| oriC و oriT | جستجو در DoriC و دیتابیس oriT | ✅ | ❌ |
| پپتید سیگنال | DeepSig | با `--gram` | با `--gram` (SignalP) |
| ژن کاذب | — | ✅ (ترجمه‌ی بلندتر و blastx) | ❌ |
| عناصر IS | ISFinder | به‌عنوان محصول CDS | به‌عنوان محصول CDS |

## ۴. آنوتیشن عملکردی

### ۴.۱ سلسله‌مراتب شواهد
هر ابزار آنوتیشن عملکردی همین منطق را دنبال می‌کند: **از دقیق‌ترین به کلی‌ترین**.
1. **یکسانی کامل** با پروتئین شناخته‌شده: بهترین شاهد.
2. **همسانی بالا** با یک خانواده‌ی بازبینی‌شده (مثلاً ≥ ۹۰٪ هویت).
3. **همسانی متوسط** با یک خوشه‌ی بزرگ‌تر (مثلاً ≥ ۵۰٪).
4. **دامنه‌ی حفاظت‌شده** (Pfam، TIGRFAM): «حاوی دامنه‌ی ABC transporter»، بدون ادعای دقیق‌تر.
5. **هیچ**: «hypothetical protein».

### ۴.۲ Bakta
طبق README رسمی، مسیر CDS در Bakta:
1. پیش‌بینی با Pyrodigal، **جدا** برای replicon‌های کامل و کانتیگ‌های ناقص.
2. حذف CDSهای جعلی با **AntiFam**.
3. تشخیص **استثنای ترجمه (سلنوسیستئین)**.
4. **شناسایی بدون همترازی (AFSI):** هش **MD5** هر پروتئین با صدها میلیون پروتئین UniParc، UniRef100 و RefSeq مقایسه می‌شود. طبق README، برای بعضی ژنوم‌ها تا ۹۹٪ CDSها همین‌جا شناسایی می‌شوند، بدون همترازی. نتیجه: ارجاع پایدار به `WP_…` (RefSeq) و `UniRef100_…`.
5. همترازی بقیه با **DIAMOND** در برابر خوشه‌های UniRef90 (پوشش ۸۰٪ و هویت ۵۰٪)، و نسبت دادن به UniRef90 (هویت > ۹۰٪) یا UniRef50 (هویت > ۵۰٪).
6. سیستم‌های خبره: **AMRFinderPlus** (ژن مقاومت)، NCBI BlastRules، **VFDB** (ضراوت).
7. پپتید سیگنال (با `--gram`)، تشخیص **ژن کاذب**، و برای پروتئین‌های hypothetical: دامنه‌ی Pfam.

```bash
bakta --db /path/to/db-light --output bakta_out --prefix isolateA \
  --genus Escherichia --species coli --strain A \
  --locus-tag ECA --gram - --threads 8 shovill_out/contigs.fa
```
| گزینه | چرا |
| :--- | :--- |
| `--db` | دیتابیس. **light**: ۱٫۳ گیگابایت فشرده و ۳٫۹ گیگابایت باز (روی سرور دوره: v6.0، تاریخ 2025-02-24). **full**: ۳۰ گیگابایت فشرده و ۸۴ گیگابایت باز. light فقط خوشه‌های UniRef50 را برای CDS دارد، پس نام‌ها کلی‌ترند. |
| `--genus/--species/--strain` | فقط در فایل‌های خروجی نوشته می‌شوند (برای GenBank). روی پیش‌بینی اثری ندارند. |
| `--locus-tag` | پیشوند شناسه‌ی ژن‌ها (`ECA_00001`، …). برای ارسال به NCBI باید **ثبت‌شده** باشد. |
| `--complete` | همه‌ی توالی‌ها replicon کامل و دایره‌ای‌اند (فقط برای اسمبلی بسته، مثلاً long-read). |
| `--gram` | برای پیش‌بینی پپتید سیگنال (`-` برای *E. coli*). |
| `--translation-table` | ۱۱ (پیش‌فرض)، ۴ (*Mycoplasma*) یا ۲۵. |
| `--compliant` | خروجی سازگار با GenBank/ENA/DDBJ. |
| `--proteins` | پروتئین‌های **مورد اعتماد** خودتان (مثلاً ژن‌های بازبینی‌شده‌ی گونه) با اولویت بالاتر. |
| `--meta` | حالت متاژنوم (فقط پیش‌بینی CDS را عوض می‌کند). |

خروجی‌ها (پیشوند `isolateA`):
| فایل | محتوا |
| :--- | :--- |
| `.gff3` | آنوتیشن + توالی (ورودی Panaroo در ماژول ۰۷) |
| `.gbff` | GenBank: آنوتیشن + توالی، برای Artemis، Snippy و ارسال |
| `.faa` / `.ffn` | توالی پروتئین / نوکلئوتید هر ژن |
| `.tsv` | جدول ساده‌ی همه‌ی ویژگی‌ها |
| `.hypotheticals.tsv` | پروتئین‌های hypothetical، با دامنه‌ی Pfam و آمار |
| `.json` | همه‌چیز، قابل خواندن با برنامه |
| `.txt` | خلاصه: تعداد هر نوع ویژگی |
| `.png` / `.svg` | نقشه‌ی دایره‌ای ژنوم |

### ۴.۳ Prokka
```bash
prokka --outdir prokka_out --prefix isolateA --kingdom Bacteria --genus Escherichia --species coli \
  --strain A --locustag ECA --gram neg --cpus 8 --compliant shovill_out/contigs.fa
```
- `--kingdom`: `Archaea`، `Bacteria`، `Mitochondria` یا `Viruses` (جدول ژنتیکی را تنظیم می‌کند).
- `--usegenus` همراه `--genus`: اول در دیتابیس اختصاصی جنس جستجو می‌کند.
- `--proteins`: پروتئین‌های مورد اعتماد با اولویت اول.
- `--rfam`: ncRNA با Infernal («کند» به نوشته‌ی خود راهنما).
- `--compliant`: معادل `--addgenes --mincontiglen 200 --centre XXX`.

خروجی‌ها شبیه Bakta‌اند (`.gff`، `.gbk`، `.faa`، `.ffn`، `.tsv`، `.txt`).

### ۴.۴ Bakta یا Prokka؟
| | Bakta | Prokka |
| :--- | :--- | :--- |
| دیتابیس | بزرگ و به‌روز (UniRef، RefSeq، AMRFinderPlus، VFDB، …) با نسخه‌ی مشخص | کوچک‌تر، داخلی (UniProt منتخب، HAMAP، …) |
| ارجاع پایدار به پروتئین (`WP_`، `UniRef`) | ✅ | ❌ |
| پروتئین‌های کوچک (sORF)، ژن کاذب، سلنوسیستئین | ✅ | ❌ |
| سرعت و فضای دیسک | کندتر، به‌خصوص با DB کامل | سریع، بدون دیتابیس جدا |
| سازگاری با ابزارهای قدیمی‌تر | اکثر ابزارها GFF3 هر دو را می‌خوانند | بسیاری از آموزش‌ها و پایپلاین‌های قدیمی بر اساس Prokka |

توصیه: برای کار جدید **Bakta**. **نسخه‌ی ابزار و نسخه‌ی دیتابیس** را همیشه گزارش کنید. دو اجرا با دیتابیس متفاوت، نام‌های متفاوت می‌دهد، و در پن‌ژنوم این تفاوت به‌شکل «ژن‌های متفاوت» ظاهر می‌شود (ماژول ۰۷).

### ۴.۵ PGAP برای ارسال به NCBI
NCBI ژنوم‌های پروکاریوتی RefSeq را با پایپلاین خودش، **PGAP** (Prokaryotic Genome Annotation Pipeline)، آنوتیت می‌کند و هنگام ارسال به GenBank هم می‌توانید آنوتیشن با PGAP را درخواست کنید. PGAP را می‌توان محلی هم اجرا کرد (با Docker و دیتابیس چندده‌گیگابایتی). اجرای محلی برای ارسال لازم نیست. Bakta و Prokka برای **تحلیل** شما هستند.

### ۴.۶ لایه‌های عملکردی بیشتر
| هدف | ابزار |
| :--- | :--- |
| ارتولوگ، COG، GO، KEGG | **eggNOG-mapper** |
| دامنه‌ها (Pfam، TIGRFAM، CDD، …) | **InterProScan** |
| مسیرهای KEGG | **KofamScan** |
| ژن‌های مقاومت | **AMRFinderPlus**، RGI/CARD (بخش ۰۸) |
| عوامل ضراوت | VFDB (بخش ۰۸) |

## ۵. خواندن خروجی: GFF3 در برابر GenBank
همان GFF3 ماژول 01/03 و 02/01. سه نکته‌ی عملی:
- ستون ۹ **percent-encoded** است (`%2C` = ویرگول؛ ماژول 02/01 تمرین ۱).
- در GFF3 خروجی Bakta و Prokka، بعد از `##FASTA` **توالی** هم آمده است. ابزارهایی که فقط ۹ ستون می‌خوانند باید آن‌جا متوقف شوند.
- GenBank (`.gbff`) را با `Bio.SeqIO.parse(..., "genbank")` بخوانید. ویژگی‌ها در `rec.features` با `qualifiers["product"]` و `qualifiers["translation"]` هستند.

## ۶. دام‌ها (Pitfalls)

| دام | چرا مشکل است | راه درست |
| :--- | :--- | :--- |
| جدول ژنتیکی ۱۱ برای *Mycoplasma* | ژن‌ها در TGA قطع می‌شوند | `--translation-table 4` / `--gcode 4` |
| حالت `single` برای کانتیگ کوتاه، فاژ یا پلاسمید تنها | داده‌ی آموزش کافی نیست | `-p meta` (Prodigal) یا `--meta` |
| انتظار کدون آغاز درست | ۵٪ اختلاف حتی در *E. coli* | انتهای N را با ارتولوگ‌ها مقایسه کنید |
| حذف «ژن‌های خراب» | سلنوپروتئین، جابه‌جایی چارچوب، ژن کاذب | `transl_except` و `exception` را بخوانید |
| نبودن ژن = نبودن عملکرد | پروتئین‌های کوچک و ژن‌های لبه‌ی کانتیگ از دست می‌روند | جستجوی مستقیم (tblastn) قبل از ادعای «ندارد» |
| شمردن rRNA در اسمبلی Illumina | نسخه‌ها فشرده می‌شوند | فقط با اسمبلی بسته (long-read) |
| tRNA اضافه = tRNA جدید | تکه‌ی tRNA در مرز پروفاژ، یا tmRNA | امتیاز و موقعیت را ببینید |
| مقایسه‌ی آنوتیشن دو ابزار یا دو نسخه‌ی DB | نام‌های متفاوت = «ژن متفاوت» در پن‌ژنوم | یک ابزار و یک نسخه برای همه‌ی ایزوله‌ها |
| «hypothetical protein» = بی‌اهمیت | در فاژ و جزیره‌های ژنومی اکثریت‌اند | دامنه، ساختار (AlphaFold/Foldseek)، بافت ژنومی |
| گزارش نکردن نسخه‌ی DB | تکرارپذیر نیست | نسخه‌ی ابزار + DB در روش‌ها |

## ۷. جمع‌بندی
- آنوتیشن = ساختاری (کجا) + عملکردی (چه). پیش‌بینی است و خطا دارد.
- Pyrodigal روی *E. coli*: **۹۶٪** ژن‌ها با کدون پایان درست، ولی **۵٪** آغاز متفاوت و **۱۷۱** ژن از دست رفته، که بیشترشان کوچک‌تر از ۱۰۰ اسیدآمینه‌اند. سلنوپروتئین‌ها و *dnaX* (لغزش ریبوزومی) استثناهای زیستی‌اند.
- rRNA با barrnap دقیق است (۲۲ از ۲۲)، ولی در اسمبلی کوتاه‌رید فشرده می‌شود. tRNAهای «اضافه» در مرز پروفاژها، رد پای ورود فاژ هستند.
- Bakta (هش MD5، UniRef، AMRFinderPlus، sORF، ژن کاذب) برای کار جدید. نسخه‌ی DB را گزارش کنید.

---

## منابع

### مقاله‌ها
- Hyatt D, et al. (2010). Prodigal: prokaryotic gene recognition and translation initiation site identification. *BMC Bioinformatics* 11:119. https://doi.org/10.1186/1471-2105-11-119
- Larralde M (2022). Pyrodigal: Python bindings and interface to Prodigal. *Journal of Open Source Software* 7(72):4296. https://doi.org/10.21105/joss.04296
- Schwengers O, et al. (2021). Bakta: rapid and standardized annotation of bacterial genomes via alignment-free sequence identification. *Microbial Genomics* 7:000685. https://doi.org/10.1099/mgen.0.000685
- Seemann T (2014). Prokka: rapid prokaryotic genome annotation. *Bioinformatics* 30:2068–2069. https://doi.org/10.1093/bioinformatics/btu153
- Chan PP, et al. (2021). tRNAscan-SE 2.0: improved detection and functional classification of transfer RNA genes. *Nucleic Acids Research* 49:9077–9096. https://doi.org/10.1093/nar/gkab688
- Laslett D, Canback B (2004). ARAGORN, a program to detect tRNA genes and tmRNA genes in nucleotide sequences. *Nucleic Acids Research* 32:11–16. https://doi.org/10.1093/nar/gkh152
- Tatusova T, et al. (2016). NCBI prokaryotic genome annotation pipeline. *Nucleic Acids Research* 44:6614–6624. https://doi.org/10.1093/nar/gkw569
- Cantalapiedra CP, et al. (2021). eggNOG-mapper v2. *Molecular Biology and Evolution* 38:5825–5829. https://doi.org/10.1093/molbev/msab293
- Jones P, et al. (2014). InterProScan 5: genome-scale protein function classification. *Bioinformatics* 30:1236–1240. https://doi.org/10.1093/bioinformatics/btu031

### مستندات
- Bakta (README، شامل دیتابیس و مراحل): https://github.com/oschwengers/bakta
- Prokka: https://github.com/tseemann/prokka
- barrnap: https://github.com/tseemann/barrnap
- NCBI PGAP: https://github.com/ncbi/pgap

### ویدیوهای آموزشی
- Tim Hubbard (Wellcome Sanger / Ensembl) — *Genome Annotation* (Serious Science): https://www.youtube.com/watch?v=_u3UMTjkqG4
- NPTEL, IIT Madras — *Gene Prediction Approaches and Common Methods for Bacterial Gene Prediction*: https://www.youtube.com/watch?v=q19Ur8bi64k
- Galaxy Project — *GTN Tutorial: Bacterial Genome Annotation* (Bakta): https://www.youtube.com/watch?v=VOwplmv0vNs
- Galaxy Project — *GTN Training: Annotation of a Prokaryotic Genome* (Prokka): https://www.youtube.com/watch?v=B8pIQZPf21Y

> لینک‌ها در تاریخ 2026-10-15 بررسی شدند (`_tools/check_links.sh`).
