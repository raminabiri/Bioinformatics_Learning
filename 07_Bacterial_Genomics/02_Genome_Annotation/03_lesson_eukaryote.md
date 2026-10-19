# درس ۳: آنوتیشن ژنوم یوکاریوت (با تمرکز بر قارچ‌ها و مخمرها)

**بخش:** `07_Bacterial_Genomics` · **ماژول:** `02_Genome_Annotation` · **پیش‌نیاز:** درس‌های ۱ و ۲ همین ماژول · **زمان:** ۱٫۵ ساعت · **ابزار (مستندات‌شده):** RepeatModeler2/RepeatMasker، BRAKER4 (GeneMark-ETP + AUGUSTUS + TSEBRA)، Funannotate 1.9، BUSCO/compleasm، eggNOG-mapper، InterProScan · **آخرین بازبینی:** 2026-10-15

> ✍️ **وضعیت:** آنوتیشن کامل یوکاریوت (ماسک تکرارها، همترازی RNA-seq، آموزش مدل‌ها) ساعت‌ها تا روزها طول می‌کشد و در این دوره **اجرا نشده**. دستورها از مستندات رسمی است. بخش ۲ **اجراشده** است: Pyrodigal روی کروموزوم I مخمر (۲۳۰ کیلوباز، [scripts/yeast_demo.sh](scripts/yeast_demo.sh)، چند ثانیه).

---

## ۱. چرا آنوتیشن یوکاریوت سخت‌تر است؟

| | باکتری | قارچ رشته‌ای / مخمر | انسان |
| :--- | :--- | :--- | :--- |
| اندازه‌ی ژنوم | ۰٫۵ تا ۱۳ مگاباز | ۱۰ تا ۱۰۰ مگاباز (*S. cerevisiae*: ۱۲؛ *Aspergillus*: حدود ۳۰) | حدود ۳٬۱۰۰ مگاباز |
| سهم کدکننده | حدود ۸۸٪ | ۴۰ تا ۷۰٪ | حدود ۱ تا ۲٪ |
| intron | تقریباً نه | *S. cerevisiae*: کم (حدود ۵٪ ژن‌ها، معمولاً یک intron)؛ قارچ‌های رشته‌ای: چند intron کوتاه در هر ژن | حدود ۸ intron در هر ژن، اغلب بلند |
| تکرار و ترانسپوزون | کم | متغیر (چند تا ۳۰٪+) | حدود ۵۰٪ |
| پیرایش متناوب (alternative splicing) | — | کم | رایج |

مشکل اصلی: ژن یک **ORF پیوسته نیست**. مدل باید **مرز اگزون و intron** (جایگاه‌های پیرایش، معمولاً GT…AG) را پیدا کند. ابزار باکتریایی این مفهوم را ندارد.

## ۲. ابزار باکتریایی روی ژنوم مخمر (اجراشده)

```bash
cd 07_Bacterial_Genomics/02_Genome_Annotation
bash scripts/yeast_demo.sh
```
کروموزوم I *S. cerevisiae* S288C (`NC_001133.9`، ۲۳۰ کیلوباز): ۹۴ ژن پروتئین‌ساز در آنوتیشن مرجع، که سه تا intron دارند.
```text
== Pyrodigal (single mode, genetic code 1) vs reference
reference CDS: 94 with 94 distinct stops  (+ 0 pseudogene CDS)   predicted CDS: 159
same stop:                 84  (89.4% of reference)
  ... and same start:      76  (90.5% of matched)
reference only (missed):   10
predicted only:            75
== the three intron-containing genes: reference CDS segments vs Pyrodigal
EFB1  reference 142174-143160 + (206 aa)   Pyrodigal: 142954-143160 (68 aa)
SNC1  reference 87286-87752 + (117 aa)   Pyrodigal: 87286-87438 (50 aa)
TFC3  reference 147594-151166 - (1160 aa)   Pyrodigal: 147594-150695 (1033 aa)
```
تفسیر:
1. **مخمر نان intron کمی دارد**، برای همین ابزار باکتریایی ۸۹٪ ژن‌ها را با کدون پایان درست پیدا کرد. این **استثناست**. در قارچ رشته‌ای یا گیاه، این عدد فرو می‌ریزد.
2. **هر سه ژن دارای intron اشتباه‌اند**، و هر کدام به شکلی متفاوت:
   - *EFB1*: فقط بخشی از اگزون دوم پیدا شد (۶۸ از ۲۰۶ اسیدآمینه). ابزار یک ATG داخلی را آغاز گرفت.
   - *SNC1*: از آغاز درست شروع شد، **وارد intron شد** و در اولین کدون پایان داخل intron متوقف شد (۵۰ به‌جای ۱۱۷ اسیدآمینه).
   - *TFC3*: اگزون اول (کوتاه) گم شد و پروتئین ۱۲۷ اسیدآمینه کوتاه‌تر شد.
3. **۷۵ ژن ساختگی (۸۰٪ بیش از تعداد واقعی):** ابزار باکتریایی فرض می‌کند ژنوم فشرده است و هر ORF بلند احتمالاً ژن است. در یوکاریوت، ORFهای بلند تصادفی در نواحی بین‌ژنی و در **رشته‌ی مقابل** ژن‌های واقعی زیادند.

**درس:** برای یوکاریوت (حتی «ساده»‌ترین آن‌ها) ابزار مخصوص یوکاریوت لازم است.

## ۳. مسیر کار آنوتیشن یوکاریوت

```text
assembly ─► 1. repeat library + soft-masking (RepeatModeler2 + RepeatMasker)
              │
              ├─► 2. evidence:  RNA-seq (HISAT2/STAR) · proteins (OrthoDB, related species) · IsoSeq
              │
              ├─► 3. gene prediction trained on the evidence (BRAKER4: GeneMark-ETP + AUGUSTUS → TSEBRA)
              │         or Funannotate (fungi)
              │
              ├─► 4. quality: BUSCO / compleasm, OMArk
              │
              └─► 5. functional annotation: eggNOG-mapper, InterProScan, (fungi: antiSMASH, CAZymes, secretome)
```

### ۳.۱ ماسک کردن تکرارها (اول از همه)
طبق راهنمای BRAKER: «برای پیش‌بینی دقیق ژن در یک ژنوم جدید، ژنوم باید از نظر تکرار ماسک شود.» در غیر این صورت ترانسپوزون‌ها (که خودشان ORF دارند، مثل ترانسپوزاز) به‌عنوان ژن پیش‌بینی می‌شوند. **soft-masking** (تکرارها با حروف کوچک) بهتر از **hard-masking** (تبدیل به N) است: ابزار پیش‌بینی می‌داند ناحیه تکراری است ولی توالی را هنوز می‌بیند.
```bash
BuildDatabase -name myfungus genome.fa
RepeatModeler -database myfungus -threads 16 -LTRStruct          # de novo repeat library
RepeatMasker -lib myfungus-families.fa -xsmall -pa 16 genome.fa   # -xsmall = soft-mask
```
کتابخانه‌ی تکرار باید **de novo** از همان ژنوم ساخته شود. کتابخانه‌های عمومی (Dfam) برای گونه‌های غیرمدل ناقص‌اند.

### ۳.۲ شواهد (evidence)
- **RNA-seq**: بهترین شاهد برای مرز اگزون و intron. ریدها را با یک همترازگر **آگاه از پیرایش** (HISAT2، STAR) روی ژنوم نگاشت کنید.
- **پروتئین‌ها**: پروتئین‌های گونه‌های نزدیک، یا یک پایگاه بزرگ مثل **OrthoDB** (بخش مربوط به Fungi). BRAKER از آن‌ها با همترازی «پیرایش‌آگاه» استفاده می‌کند.
- **IsoSeq** (PacBio): رونوشت‌های کامل، بهترین شاهد برای ساختار کامل ژن.

### ۳.۳ پیش‌بینی ژن: BRAKER
**BRAKER** دو پیش‌بینی‌گر را با شواهد آموزش می‌دهد: **GeneMark** (ES/ET/EP/ETP) و **AUGUSTUS**. بعد **TSEBRA** بهترین رونوشت‌ها را از هر دو انتخاب می‌کند. حالت‌ها:

| حالت | ورودی | معادل قدیمی |
| :--- | :--- | :--- |
| ES | فقط ژنوم | BRAKER (فقط ab initio)، کمترین دقت |
| ET | ژنوم + RNA-seq | BRAKER1 |
| EP | ژنوم + پروتئین‌ها | BRAKER2 |
| **ETP** | ژنوم + RNA-seq + پروتئین‌ها | **BRAKER3**، بهترین دقت |

**به‌روزرسانی مهم (۲۰۲۶):** طبق مخزن رسمی، `braker.pl` (BRAKER3) **منسوخ** شده و جایگزینش **BRAKER4** است. BRAKER4 بازنویسی همان منطق در **Snakemake** است و همه‌ی ابزارها در **Singularity** اجرا می‌شوند. ورودی آن یک فایل `samples.csv` (هر سطر یک ژنوم و شواهدش) و یک `config.ini` است. ماسک کردن تکرار (RepeatModeler2 + RepeatMasker، یا Red به‌عنوان جایگزین سریع)، ncRNAها، و کنترل کیفیت (BUSCO، compleasm، OMArk) را هم خودکار انجام می‌دهد. طبق بنچمارک README، دقت آن با `braker.pl` برابر یا کمی بهتر است. برای جزئیات دستور، راهنمای مهاجرت `MIGRATING_FROM_BRAKER3.md` را در همان مخزن ببینید.

برای **قارچ‌ها**، GeneMark-ETP یک گزینه‌ی مخصوص دارد (`--fungus` در BRAKER3) که **مدل نقطه‌ی انشعاب** (branch point) intronهای قارچی را فعال می‌کند.

**مجوز:** GeneMark برای استفاده‌ی تجاری رایگان نیست (README هر دو نسخه).

### ۳.۴ Funannotate: خط لوله‌ی مخصوص قارچ
**Funannotate** «به‌طور خاص برای قارچ‌ها ساخته شده، ولی برای یوکاریوت‌های بالاتر هم کار می‌کند» (README). نسخه‌ی 1.9.0 نسخه‌ی فعلی است و **funannotate2** یک بازنویسی کامل با دستورها و دیتابیس متفاوت است. مراحل طبق آموزش رسمی:
```bash
funannotate clean -i assembly.fa --minlen 1000 -o clean.fa         # remove short/duplicated contigs (haploid fungi)
funannotate sort  -i clean.fa -b scaffold -o sorted.fa              # rename headers
funannotate mask  -i sorted.fa --cpus 12 -o masked.fa               # soft-mask repeats
funannotate train -i masked.fa -o fun --left R1.fq.gz --right R2.fq.gz \
  --stranded RF --jaccard_clip --species "Aspergillus sp." --cpus 12  # RNA-seq: Trinity + PASA
funannotate predict -i masked.fa -o fun --species "Aspergillus sp." --cpus 12
funannotate update  -i fun --cpus 12                                # UTRs, fix models with RNA-seq
funannotate annotate -i fun --cpus 12                               # function: Pfam, eggNOG, CAZy, MEROPS, BUSCO, ...
```
Funannotate چند پیش‌بینی‌گر را اجرا می‌کند (AUGUSTUS، GeneMark، SNAP، GlimmerHMM) و نتیجه‌ها را با **EVidenceModeler** وزن‌دار ترکیب می‌کند. خروجی‌اش برای **ارسال به NCBI** آماده است (فایل `.tbl` و `.sqn` با tbl2asn). در گام `predict`، مدل‌هایی را که به‌طور خودکار درست نمی‌شوند گزارش می‌کند تا دستی اصلاح شوند.

برای قارچ‌ها، `annotate` لایه‌های مخصوص هم دارد: **CAZymes** (آنزیم‌های کربوهیدرات، dbCAN)، پروتئازها (MEROPS)، پروتئین‌های ترشحی (SignalP)، و خوشه‌های ژنی متابولیت ثانویه از **antiSMASH** (مثلاً سنتز پنی‌سیلین یا آفلاتوکسین).

### ۳.۵ کیفیت: BUSCO
**BUSCO** معادل CheckM2 برای یوکاریوت‌هاست: ژن‌های **تک‌نسخه‌ای حفاظت‌شده** یک دودمان (از OrthoDB؛ مثلاً `fungi` یا `saccharomycetes`) را جستجو می‌کند. نام دقیق مجموعه‌ها با نسخه‌ی OrthoDB عوض می‌شود (`_odb10`، `_odb12`). فهرست را با `busco --list-datasets` ببینید.
```bash
busco -i proteins.faa -m proteins -l fungi -o busco_prot -c 8      # annotation completeness
busco -i genome.fa   -m genome   -l fungi -o busco_genome -c 8     # assembly completeness
```
خروجی یک خط خلاصه است، به شکل `C:…%[S:…%,D:…%],F:…%,M:…%,n:…`:
- **C (Complete)**: کامل؛ **S**: تک‌نسخه؛ **D (Duplicated)**: دو نسخه یا بیشتر
- **F (Fragmented)**: ناقص؛ **M (Missing)**: پیدا نشد؛ **n**: تعداد ژن‌های BUSCO آن دودمان

تفسیر:
- **BUSCO روی ژنوم بالا و روی پروتئین‌ها پایین** ← اسمبلی خوب است، **آنوتیشن** ژن‌ها را از دست داده است.
- **D بالا** ← هاپلوتیپ‌های تکراری در اسمبلی (یک قارچ دوهسته‌ای یا هیبرید)، یا **دوبرابرشدن واقعی ژنوم** (مثلاً *S. cerevisiae* یک دوبرابرشدن کامل ژنوم باستانی دارد)، یا آلودگی.
- **compleasm** بازنویسی سریع‌تر BUSCO است (با miniprot). **OMArk** علاوه بر کامل بودن، **ثبات** مجموعه‌ی پروتئین‌ها و آلودگی را می‌سنجد.

### ۳.۶ آنوتیشن عملکردی
همان ابزارهای درس ۱ برای پروتئین‌ها: **eggNOG-mapper** (ارتولوگ، GO، KEGG، COG)، **InterProScan** (دامنه‌ها). برای قارچ‌ها: antiSMASH، dbCAN (CAZymes)، SignalP و DeepTMHMM (ترشح و غشا).

### ۳.۷ جایگزین‌ها
- **انتقال آنوتیشن** از گونه‌ی نزدیک با آنوتیشن خوب: **Liftoff** یا **miniprot** (همترازی پروتئین‌ها روی ژنوم). سریع و خوب برای سویه‌های یک گونه. ژن‌های جدید سویه را پیدا نمی‌کند.
- پیش‌بینی با **یادگیری عمیق** بدون نیاز به آموزش روی گونه: Helixer و Tiberius. برای ژنوم‌های بدون RNA-seq روزبه‌روز رایج‌ترند.
- **NCBI Eukaryotic Genome Annotation Pipeline (EGAP)** و **Ensembl**: آنوتیشن مرجع گونه‌های مهم را این‌ها انجام می‌دهند.

## ۴. میکروب‌های یوکاریوتی دیگر
| گروه | نکته‌ی آنوتیشن |
| :--- | :--- |
| مخمرهای بیماری‌زا (*Candida albicans*) | کد ژنتیکی **۱۲**: CTG به جای لوسین، **سرین** ترجمه می‌شود (CTG clade). ابزار با کد ۱ پروتئین‌های اشتباه می‌دهد. |
| *Plasmodium* (مالاریا) | ژنوم بسیار AT‌دار (حدود ۸۰٪ AT)؛ مدل‌های مخصوص لازم است. |
| تک‌یاخته‌های دیگر (*Trypanosoma*، *Giardia*) | ویژگی‌های غیرعادی: ترجمه‌ی چندژنی (polycistronic) در تریپانوزوم‌ها، trans-splicing. |
| میتوکندری و کلروپلاست | کدهای ژنتیکی مخصوص (مثلاً ۳ برای میتوکندری مخمر، ۴ برای قارچ‌های رشته‌ای)؛ ابزار جدا (MITOS2، MFannot). |

## ۵. دام‌ها (Pitfalls)
| دام | چرا مشکل است | راه درست |
| :--- | :--- | :--- |
| Prokka/Bakta/Prodigal روی یوکاریوت | intron‌ها نادیده؛ ژن‌های بریده و ساختگی (مخمر: ۷۵ ژن ساختگی در ۲۳۰ کیلوباز) | BRAKER4، Funannotate |
| پیش‌بینی بدون ماسک تکرار | ترانسپوزاز و تکرارها به‌عنوان ژن | RepeatModeler2 + RepeatMasker (`-xsmall`) |
| hard-masking | ژن‌های همپوشان با تکرار از دست می‌روند | soft-masking |
| ab initio تنها (حالت ES) | مرزهای intron نادقیق | RNA-seq و پروتئین (ETP) |
| کد ژنتیکی ۱ برای *Candida* | Ser به‌جای Leu (CTG) | کد ۱۲ |
| BUSCO فقط روی ژنوم | آنوتیشن ناقص دیده نمی‌شود | BUSCO روی **پروتئین‌ها** هم |
| دودمان BUSCO نامناسب | کامل بودن اشتباه | نزدیک‌ترین دودمان (`--auto-lineage` یا انتخاب دستی) |
| گزارش نکردن نسخه‌ها | تکرارپذیر نیست | نسخه‌ی ابزار، دودمان BUSCO، پایگاه پروتئین |

## ۶. جمع‌بندی
- یوکاریوت = intron + تکرار + ژن‌های کم‌تراکم. ابزار باکتریایی حتی روی مخمر هر **سه** ژن دارای intron را اشتباه پیش‌بینی کرد و ۷۵ ژن ساختگی ساخت.
- ترتیب کار: **ماسک تکرار ← شواهد (RNA-seq، پروتئین) ← BRAKER4 یا Funannotate ← BUSCO ← آنوتیشن عملکردی**.
- BUSCO هم روی ژنوم و هم روی پروتئین‌ها. اختلاف این دو کیفیت آنوتیشن را نشان می‌دهد.
- میکروب‌های یوکاریوتی استثناهای خودشان را دارند (*Candida*: کد ۱۲).

---

## منابع

### مقاله‌ها
- Gabriel L, et al. (2024). BRAKER3: Fully automated genome annotation using RNA-seq and protein evidence with GeneMark-ETP, AUGUSTUS, and TSEBRA. *Genome Research* 34:769–777. https://doi.org/10.1101/gr.278090.123
- Stanke M, et al. (2006). AUGUSTUS: ab initio prediction of alternative transcripts. *Nucleic Acids Research* 34:W435–W439. https://doi.org/10.1093/nar/gkl200
- Flynn JM, et al. (2020). RepeatModeler2 for automated genomic discovery of transposable element families. *PNAS* 117:9451–9457. https://doi.org/10.1073/pnas.1921046117
- Manni M, et al. (2021). BUSCO update: novel and streamlined workflows along with broader and deeper phylogenetic coverage. *Molecular Biology and Evolution* 38:4647–4654. https://doi.org/10.1093/molbev/msab199
- Nevers Y, et al. (2025). Quality assessment of gene repertoire annotations with OMArk. *Nature Biotechnology* 43:124–133. https://doi.org/10.1038/s41587-024-02147-w
- Shumate A, Salzberg SL (2021). Liftoff: accurate mapping of gene annotations. *Bioinformatics* 37:1639–1643. https://doi.org/10.1093/bioinformatics/btaa1016
- Li H (2023). Protein-to-genome alignment with miniprot. *Bioinformatics* 39:btad014. https://doi.org/10.1093/bioinformatics/btad014
- Blin K, et al. (2023). antiSMASH 7.0. *Nucleic Acids Research* 51:W46–W50. https://doi.org/10.1093/nar/gkad344

### مستندات
- BRAKER4: https://github.com/Gaius-Augustus/BRAKER4
- BRAKER (نسخه‌ی قدیمی، `braker.pl`): https://github.com/Gaius-Augustus/BRAKER
- Funannotate: https://funannotate.readthedocs.io
- BUSCO: https://busco.ezlab.org
- RepeatMasker و RepeatModeler: https://www.repeatmasker.org

### ویدیوهای آموزشی
- Biodiversity Genomics Academy 2023 — *Gene prediction with BRAKER3*: https://www.youtube.com/watch?v=6U_yXIgVJNg
- Biodiversity Genomics Academy 2023 — *Annotating genomes the Ensembl way (Part 1)*: https://www.youtube.com/watch?v=1RJ2y1NgTM4
- Galaxy Project — *GTN Tutorial: Funannotate*: https://www.youtube.com/watch?v=r-wU6BhqIpk

> لینک‌ها در تاریخ 2026-10-15 بررسی شدند (`_tools/check_links.sh`).
