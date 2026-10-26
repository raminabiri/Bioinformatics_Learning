<div dir="rtl">

# درس ۳: آنوتیشن یوکاریوت، با تمرکز بر قارچ و مخمر

**بخش:** `07_Bacterial_Genomics` · **ماژول:** `02_Genome_Annotation` · **پیش‌نیاز:** [درس‌های ۱](01_lesson_prokaryote.md) و [۲](02_lesson_phage_virus.md) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** اجراشده: Pyrodigal؛ از مستندات: RepeatModeler2/RepeatMasker، BRAKER4، Funannotate 1.9، BUSCO · **آخرین بازبینی:** 2026-10-21

> ✍️ **وضعیت:** آنوتیشن کامل یوکاریوت (پوشاندن تکرارها، هم‌ترازی RNA-seq، آموزش مدل‌ها) ساعت‌ها تا روزها طول می‌کشد و **اجرا نشده**؛ دستورها از مستندات رسمی‌اند. بخش ۳ **اجراشده** است: Pyrodigal روی کروموزوم I مخمر (چند ثانیه، 2026-10-15).

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. بگویید چرا ژن یوکاریوتی یک ORF پیوسته نیست و ابزار باکتریایی با آن چه می‌کند.
2. گام‌های آنوتیشن یوکاریوت را به ترتیب بچینید: پوشاندن تکرار، شواهد، پیش‌بینی، کیفیت، کارکرد.
3. خط خلاصه‌ی BUSCO را بخوانید و کیفیت اسمبلی را از کیفیت آنوتیشن جدا کنید.
4. استثناهای میکروب‌های یوکاریوتی (برای نمونه کد ژنتیکی *Candida*) را بشناسید.

---

## ۱. داستان

در بخش ۰۶، ریدهای *Candida albicans* در پروفایل Kraken2 گم شدند. اگر روزی ژنوم یک مخمر یا قارچ بیماری‌زا را اسمبل کنید، ابزارهای درس ۱ آن را درست آنوتیت نمی‌کنند. چرا؟

| | باکتری | قارچ رشته‌ای / مخمر | انسان |
| :--- | :--- | :--- | :--- |
| اندازه‌ی ژنوم | ۰٫۵ تا ۱۳ مگاباز | ۱۰ تا ۱۰۰ مگاباز | کمابیش ۳٬۱۰۰ مگاباز |
| سهم کدکننده | کمابیش ۸۸٪ | ۴۰ تا ۷۰٪ | ۱ تا ۲٪ |
| اینترون | کمابیش نه | ‏*S. cerevisiae*: کم (کمابیش ۵٪ ژن‌ها)؛ قارچ رشته‌ای: چند اینترون کوتاه در هر ژن | کمابیش ۸ اینترون در هر ژن |
| تکرار و ترانسپوزون | کم | گوناگون | کمابیش ۵۰٪ |

مشکل اصلی: ژن **یک ORF پیوسته نیست**. مدل باید **مرز اگزون و اینترون** (جایگاه‌های پیرایش، بیشتر GT…AG) را بیابد؛ ابزار باکتریایی این مفهوم را ندارد.

---

## ۲. مفهوم: ژن در تکه‌ها

<div dir="ltr">

```text
DNA:   5' ==[exon 1]==---intron---==[exon 2]==---intron---==[exon 3]== 3'
                         GT......AG             GT......AG
mRNA:     [exon 1][exon 2][exon 3]          -> one protein
```

</div>

ابزاری که تنها ORF می‌جوید، یا یک اگزون را می‌یابد، یا وارد اینترون می‌شود و در نخستین کدون پایان درون آن می‌ایستد. گام بعد این را روی یک کروموزوم واقعی نشان می‌دهد.

---

## ۳. گام ۱: ابزار باکتریایی روی مخمر (اجراشده)

<div dir="ltr">

```bash
bash $S/yeast_demo.sh
```

</div>

اسکریپت کروموزوم I *S. cerevisiae* S288C (`NC_001133.9`، ۲۳۰ کیلوباز) را با `curl` دانلود می‌کند، Pyrodigal را با کد ژنتیکی ۱ اجرا می‌کند و با آنوتیشن مرجع می‌سنجد: ۹۴ ژن پروتئین‌ساز، که سه تایشان اینترون دارند.

<div dir="ltr">

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

</div>

1. **مخمر نان اینترون کمی دارد**؛ برای همین ابزار باکتریایی ۸۹٪ ژن‌ها را با پایان درست یافت. این **استثناست**؛ در قارچ رشته‌ای یا گیاه این عدد فرو می‌ریزد.
2. **هر سه ژن اینترون‌دار نادرست‌اند**، هر کدام به شکلی:
   - ‏*EFB1*: تنها بخشی از اگزون دوم (۶۸ از ۲۰۶ اسیدآمینه)؛ یک ATG درونی را آغاز گرفت.
   - ‏*SNC1*: از آغاز درست، ولی **وارد اینترون شد** و در نخستین کدون پایان درون آن ایستاد (۵۰ به‌جای ۱۱۷).
   - ‏*TFC3*: اگزون نخست (کوتاه) گم شد؛ ۱۲۷ اسیدآمینه کوتاه‌تر.
3. **۷۵ ژن ساختگی** (۸۰٪ بیش از شمار واقعی): ابزار باکتریایی ژنوم را فشرده می‌پندارد و هر ORF بلند را ژن می‌شمارد؛ در یوکاریوت ORFهای بلند تصادفی در نواحی میان‌ژنی و رشته‌ی روبه‌رو بسیارند.

**درس:** برای یوکاریوت، حتی ساده‌ترینشان، ابزار ویژه‌ی یوکاریوت لازم است.

---

## ۴. گام ۲: گردش کار آنوتیشن یوکاریوت (از مستندات)

<div dir="ltr">

```text
assembly -> 1. repeat library + soft-masking (RepeatModeler2 + RepeatMasker)
         -> 2. evidence: RNA-seq (HISAT2/STAR), proteins (OrthoDB), IsoSeq
         -> 3. gene prediction trained on the evidence (BRAKER4) or Funannotate (fungi)
         -> 4. quality: BUSCO / compleasm, OMArk
         -> 5. function: eggNOG-mapper, InterProScan (fungi: antiSMASH, CAZymes)
```

</div>

### ۴.۱ پوشاندن تکرارها، نخست از همه

به گفته‌ی راهنمای BRAKER، ژنوم پیش از پیش‌بینی باید **پوشانده** شود؛ وگرنه ترانسپوزون‌ها (که خودشان ORF دارند) ژن پیش‌بینی می‌شوند. **پوشاندن نرم** (*soft-masking*: تکرارها با حروف کوچک) بهتر از سخت (تبدیل به N) است.

<div dir="ltr">

```bash
BuildDatabase -name myfungus genome.fa
RepeatModeler -database myfungus -threads 16 -LTRStruct          # de novo repeat library
RepeatMasker -lib myfungus-families.fa -xsmall -pa 16 genome.fa   # -xsmall = soft-mask
```

</div>

### ۴.۲ شواهد و پیش‌بینی: BRAKER

‏**RNA-seq** بهترین شاهد برای مرز اگزون و اینترون است (هم‌ترازی با ابزار آگاه از پیرایش، مانند HISAT2)؛ **پروتئین‌ها**ی گونه‌های نزدیک یا OrthoDB شاهد دوم. **BRAKER** دو پیش‌بینی‌گر (GeneMark و AUGUSTUS) را با این شواهد آموزش می‌دهد و TSEBRA بهترین مدل‌ها را برمی‌گزیند:

| حالت | ورودی | دقت |
| :--- | :--- | :--- |
| ES | تنها ژنوم | کمترین |
| ET | ژنوم + RNA-seq | |
| EP | ژنوم + پروتئین‌ها | |
| **ETP** | ژنوم + RNA-seq + پروتئین‌ها | **بیشترین** |

به گفته‌ی مخزن رسمی، `braker.pl` (BRAKER3) **کنار گذاشته شده** و جانشینش **BRAKER4** است: همان منطق، بازنویسی‌شده در **Snakemake** (بخش ۰۵)، با ورودی `samples.csv` و `config.ini`؛ پوشاندن تکرار و BUSCO را هم خودکار انجام می‌دهد.

### ‏۴.۳ Funannotate، ویژه‌ی قارچ

<div dir="ltr">

```bash
funannotate clean -i assembly.fa --minlen 1000 -o clean.fa
funannotate sort  -i clean.fa -b scaffold -o sorted.fa
funannotate mask  -i sorted.fa --cpus 12 -o masked.fa
funannotate train -i masked.fa -o fun --left R1.fq.gz --right R2.fq.gz \
  --stranded RF --jaccard_clip --species "Aspergillus sp." --cpus 12
funannotate predict -i masked.fa -o fun --species "Aspergillus sp." --cpus 12
funannotate update  -i fun --cpus 12
funannotate annotate -i fun --cpus 12
```

</div>

چند پیش‌بینی‌گر (AUGUSTUS، GeneMark، SNAP، GlimmerHMM) را اجرا و با EVidenceModeler ترکیب می‌کند؛ خروجی برای **ارسال به NCBI** آماده است، و `annotate` لایه‌های ویژه‌ی قارچ (CAZymes، پروتئازها، پروتئین‌های ترشحی، خوشه‌های antiSMASH) را دارد.

> 📺 **فیلم:** *Gene prediction with BRAKER3*: https://www.youtube.com/watch?v=6U_yXIgVJNg · *GTN Tutorial: Funannotate*: https://www.youtube.com/watch?v=r-wU6BhqIpk
> 📄 **مرجع:** Gabriel L, et al. (2024). *BRAKER3.* Genome Research 34:769–777. https://doi.org/10.1101/gr.278090.123

---

## ۵. گام ۳: کیفیت با BUSCO (از مستندات)

‏**BUSCO** همتای CheckM2 برای یوکاریوت‌هاست: ژن‌های **تک‌نسخه‌ای حفاظت‌شده**ی یک دودمان (از OrthoDB؛ برای نمونه `fungi`) را می‌جوید.

<div dir="ltr">

```bash
busco -i proteins.faa -m proteins -l fungi -o busco_prot -c 8      # annotation completeness
busco -i genome.fa   -m genome   -l fungi -o busco_genome -c 8     # assembly completeness
```

</div>

خروجی یک خط خلاصه است: `C:…%[S:…%,D:…%],F:…%,M:…%,n:…`

| نشانه | معنی |
| :--- | :--- |
| C (Complete) | کامل؛ S = تک‌نسخه، D = دو نسخه یا بیشتر |
| F (Fragmented) | ناقص |
| M (Missing) | پیدا نشد |
| n | شمار ژن‌های BUSCO آن دودمان |

- ‏**BUSCO روی ژنوم بالا و روی پروتئین‌ها پایین** ← اسمبلی خوب است، **آنوتیشن** ژن‌ها را از دست داده.
- ‏**D بالا** ← هاپلوتیپ‌های تکراری در اسمبلی، دوبرابرشدن واقعی ژنوم، یا آلودگی.

<details>
<summary>✋ امتحان کن: BUSCO ژنوم C:98% و BUSCO پروتئین‌ها C:84%. مشکل کجاست؟</summary>

اسمبلی کمابیش همه‌ی ژن‌ها را دارد (۹۸٪)، ولی آنوتیشن ۱۴٪ آن‌ها را درست پیش‌بینی نکرده؛ **آنوتیشن** ضعیف است، نه اسمبلی. با شواهد بیشتر (RNA-seq، حالت ETP) دوباره پیش‌بینی کنید (تمرین ۶).

</details>

> 📺 **فیلم:** *BUSCO Tutorial: How to do a basic run with BUSCO to assess completeness of genomes*: https://www.youtube.com/watch?v=KtH1f5NrTvU
> 📄 **مرجع:** Manni M, et al. (2021). *BUSCO update.* Mol Biol Evol 38:4647–4654. https://doi.org/10.1093/molbev/msab199

---

## ۶. میکروب‌های یوکاریوتی دیگر

| گروه | نکته‌ی آنوتیشن |
| :--- | :--- |
| ‏*Candida albicans* | کد ژنتیکی **۱۲**: CTG به‌جای لوسین، **سرین** ترجمه می‌شود |
| ‏*Plasmodium* | ژنوم بسیار AT‌دار (کمابیش ۸۰٪)؛ مدل ویژه لازم است |
| ‏*Trypanosoma* | ترجمه‌ی چندژنی و trans-splicing |
| میتوکندری | کدهای ژنتیکی ویژه (برای نمونه ۳ در مخمر)؛ ابزار جدا (MITOS2) |

---

## ۷. سه اشتباه رایج

‏**۱. ‏Prokka، Bakta یا Prodigal روی یوکاریوت.** اینترون‌ها نادیده؛ ژن‌های بریده و ساختگی (مخمر: ۷۵ ژن ساختگی در ۲۳۰ کیلوباز). BRAKER4 یا Funannotate.

**۲. پیش‌بینی بی پوشاندن تکرار.** ترانسپوزاز و تکرارها ژن پیش‌بینی می‌شوند؛ RepeatModeler2 + RepeatMasker (`-xsmall`).

‏**۳. ‏BUSCO تنها روی ژنوم.** آنوتیشن ناقص دیده نمی‌شود؛ BUSCO را روی **پروتئین‌ها** هم اجرا کنید.

---

## 📘 برای کنجکاوها

- **انتقال آنوتیشن:** برای سویه‌ای از گونه‌ای با آنوتیشن خوب، **Liftoff** یا **miniprot** سریع و خوب‌اند؛ ولی ژن‌های تازه‌ی سویه را نمی‌یابند.
- **یادگیری عمیق:** Helixer و Tiberius بی آموزش روی گونه، ژن پیش‌بینی می‌کنند؛ برای ژنوم‌های بی RNA-seq روزبه‌روز رایج‌ترند.
- ‏**‏OMArk:** افزون بر کامل بودن، یکپارچگی مجموعه‌ی پروتئین‌ها و آلودگی را می‌سنجد.

---

## جمع‌بندی

- یوکاریوت = اینترون + تکرار + ژن‌های کم‌تراکم؛ ابزار باکتریایی حتی روی مخمر هر سه ژن اینترون‌دار را نادرست یافت و ۷۵ ژن ساختگی ساخت.
- ترتیب: **پوشاندن تکرار ← شواهد ← BRAKER4 یا Funannotate ← BUSCO ← آنوتیشن کارکردی**.
- ‏BUSCO هم روی ژنوم و هم روی پروتئین‌ها؛ فاصله‌ی این دو کیفیت آنوتیشن را نشان می‌دهد.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
bash $S/yeast_demo.sh                                              # bacterial tool on a yeast chromosome
RepeatModeler -database DB -threads 16 -LTRStruct
RepeatMasker -lib DB-families.fa -xsmall -pa 16 genome.fa
busco -i proteins.faa -m proteins -l fungi -o busco_prot -c 8
busco -i genome.fa -m genome -l fungi -o busco_genome -c 8
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| اگزون / اینترون | بخش ماندگار / بخش بریده‌شده‌ی ژن هنگام پیرایش |
| پیرایش (*splicing*) | برداشتن اینترون‌ها از RNA پیش‌ساز |
| پوشاندن نرم (*soft-masking*) | نوشتن تکرارها با حروف کوچک |
| شاهد (*evidence*) | داده‌ی بیرونی (RNA-seq، پروتئین) برای آموزش و تأیید مدل ژن |
| ‏BUSCO | ژن‌های تک‌نسخه‌ای حفاظت‌شده برای سنجش کامل بودن |

---

## منابع

**مستند و مقاله**
- Gabriel L, et al. (2024). *BRAKER3: Fully automated genome annotation using RNA-seq and protein evidence with GeneMark-ETP, AUGUSTUS, and TSEBRA.* Genome Research 34:769–777. https://doi.org/10.1101/gr.278090.123
- Flynn JM, et al. (2020). *RepeatModeler2 for automated genomic discovery of transposable element families.* PNAS 117:9451–9457. https://doi.org/10.1073/pnas.1921046117
- Manni M, et al. (2021). *BUSCO update: novel and streamlined workflows along with broader and deeper phylogenetic coverage.* Molecular Biology and Evolution 38:4647–4654. https://doi.org/10.1093/molbev/msab199
- Shumate A, Salzberg SL (2021). *Liftoff: accurate mapping of gene annotations.* Bioinformatics 37:1639–1643. https://doi.org/10.1093/bioinformatics/btaa1016
- BRAKER4: https://github.com/Gaius-Augustus/BRAKER4 · Funannotate: https://funannotate.readthedocs.io · BUSCO: https://busco.ezlab.org

**کتاب**
- Kollmar M (ed.) (2019). *Gene Prediction: Methods and Protocols*. Methods Mol Biol 1962. Humana Press.

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins University). دوره‌ای ویژه‌ی آنوتیشن یوکاریوت در Coursera نیافتیم؛ نزدیک‌ترین: https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Linux* (The Linux Foundation). دوره‌ای ویژه در edX نیافتیم؛ نزدیک‌ترین: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux
- YouTube: *Gene prediction with BRAKER3* (Biodiversity Genomics Academy 2023): https://www.youtube.com/watch?v=6U_yXIgVJNg
- YouTube: *GTN Tutorial: Funannotate* (Galaxy Project): https://www.youtube.com/watch?v=r-wU6BhqIpk

<sub>نشانی‌های YouTube و DOIها در 2026-10-15 وارسی شدند؛ نشانی‌های Coursera و edX در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
