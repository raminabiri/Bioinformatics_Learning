<div dir="rtl">

# درس ۲: آنوتیشن فاژ، پروفاژ و ویروس

**بخش:** `07_Bacterial_Genomics` · **ماژول:** `02_Genome_Annotation` · **پیش‌نیاز:** [درس ۱](01_lesson_prokaryote.md) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** اجراشده: awk و Pyrodigal؛ از مستندات: Pharokka 1.10، Phold، geNomad، CheckV، VADR · **آخرین بازبینی:** 2026-10-21

> ✍️ **وضعیت:** ابزارهای ویژه‌ی فاژ و ویروس **اجرا نشده‌اند**؛ دستورها، گزینه‌ها و نمونه‌خروجی‌ها از README رسمی هر ابزار است و منبعش آمده. بخش ۳ (پروفاژهای *E. coli* K-12) و بخش ۵ (Pyrodigal روی SARS-CoV-2) **اجراشده**‌اند (2026-10-15).

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. بگویید چرا ابزارهای درس ۱ برای فاژ و ویروس خوب کار نمی‌کنند.
2. پروفاژهای یک ژنوم را از GFF درآورید و نشانه‌هایشان (GC، ژن ناشناخته، ژن کاذب، tRNA مرزی) را بسنجید.
3. نقش geNomad، CheckV، Pharokka و Phold را در یک گردش کار فاژ بشناسید.
4. توضیح دهید چرا ویروس‌های یوکاریوتی آنوتیشن **بر پایه‌ی مرجع** (VADR) می‌خواهند.

**پیش از آغاز:** در `~/genomes`، با متغیرهای `G` و `S` درس ۱.

---

## ۱. داستان

فاژها پرشمارترین زیستمندان زمین‌اند، و کمابیش هر ژنوم باکتری چند **پروفاژ** (فاژی که در کروموزوم جا گرفته) دارد. بسیاری از ژن‌های بیماری‌زایی، مانند سم شیگا در *E. coli* EHEC یا سم وبا، روی پروفاژها حمل می‌شوند. ولی ابزارهای درس ۱ برای آن‌ها ساخته نشده‌اند:

| ویژگی | باکتری | فاژ | ویروس یوکاریوتی |
| :--- | :--- | :--- | :--- |
| اندازه‌ی ژنوم | ۰٫۵ تا ۱۳ مگاباز | **۳ تا ۷۰۰ کیلوباز** | ۲ کیلوباز تا ۲ مگاباز |
| ماده‌ی ژنتیکی | dsDNA | بیشتر dsDNA؛ ssDNA و RNA هم | همه گونه، و ژنوم چندتکه |
| ژن‌های «hypothetical» | ۵ تا ۲۰٪ | **۶۰ تا ۸۰٪** | گوناگون |
| یادگیری مدل ژن از خود ژنوم | ✅ | ❌ ژنوم کوچک است | ❌ |
| کد ژنتیکی | ۱۱ (یا ۴) | ۱۱؛ گاهی **کدون پایان دیگر** | کد میزبان؛ **جابه‌جایی چارچوب**، پلی‌پروتئین، پیرایش |

---

## ۲. مفهوم: فاژ معتدل و پروفاژ

- **فاژ لیتیک:** آلوده می‌کند، تکثیر می‌شود و سلول را می‌کشد.
- **فاژ معتدل:** با **اینتگراز** خودش در کروموزوم جا می‌گیرد و به شکل **پروفاژ** با باکتری تقسیم می‌شود. بیشتر در جایگاه یک **tRNA** یا tmRNA؛ توالی اتصال بخشی از tRNA را تکرار می‌کند، پس یک **تکه‌ی tRNA** در مرز دیگر پروفاژ می‌ماند (درس ۱، بخش ۴).
- **پروفاژ خفته:** با جهش و حذف دیگر نمی‌تواند بیرون بیاید؛ ژن‌هایش بیشتر کاذب‌اند.

ژن‌های فاژهای دم‌دار در **ماژول‌های کارکردی** پشت سر هم چیده شده‌اند (بسته‌بندی DNA و سر، دم، لیز، ادغام، تنظیم، …). **ژن‌های نشانگر** فاژ، مانند **زیرواحد بزرگ ترمیناز** (TerL)، **پروتئین پورتال** و **پروتئین اصلی کپسید**، کمابیش در همه‌ی فاژهای دم‌دار هستند و در ژنوم باکتری نه.

---

## ۳. گام ۱: پروفاژهای *E. coli* K-12 (اجراشده)

آنوتیشن RefSeq این ژنوم ۱۲ ناحیه را با `Note=cryptic prophage` نشان کرده است (ستون ۳ = `sequence_feature`):

<div dir="ltr">

```bash
awk -F'\t' '$3 == "sequence_feature"' $G/ecoli_k12.gff | grep 'cryptic prophage' \
  | awk -F'\t' '{match($9, /Note=[^;]+/); print $4, $5, $5 - $4 + 1, substr($9, RSTART + 5, RLENGTH - 5)}'
```

</div>

| بخش | کار |
| :--- | :--- |
| ① نخستین awk | تنها سطرهایی که ستون ۳‌شان `sequence_feature` است |
| ② `grep 'cryptic prophage'` | تنها پروفاژهای خفته |
| ③ `match($9, /Note=[^;]+/)` | در ستون ۹، تکه‌ی `Note=…` را پیدا کن؛ `RSTART` جای آغاز و `RLENGTH` طولش را نگه می‌دارد |
| ④ `substr($9, RSTART + 5, RLENGTH - 5)` | همان تکه، بی ۵ نویسه‌ی `Note=` |

| پروفاژ | آغاز | پایان | طول (باز) |
| :--- | ---: | ---: | ---: |
| CP4-6 | 262,898 | 297,205 | 34,308 |
| DLP12 | 564,755 | 586,056 | 21,302 |
| e14 | 1,196,209 | 1,211,412 | 15,204 |
| Rac | 1,411,899 | 1,434,958 | 23,060 |
| Qin | 1,632,277 | 1,652,745 | 20,469 |
| PR-G | 2,012,502 | 2,012,663 | 162 |
| CP4-44 | 2,066,020 | 2,078,748 | 12,729 |
| PR-X | 2,167,183 | 2,167,811 | 629 |
| CPS-53 | 2,466,369 | 2,476,583 | 10,215 |
| CPZ-55 | 2,558,691 | 2,565,480 | 6,790 |
| CP4-57 | 2,755,941 | 2,777,971 | 22,031 |
| PR-Y | 4,496,675 | 4,497,940 | 1,266 |

روی هم **۱۶۸٬۱۶۵ باز (۳٫۶٪ ژنوم)**. سنجش این نواحی با بقیه‌ی ژنوم (پایتون، چند ثانیه؛ تمرین ۳):

| | پروفاژها | بقیه‌ی ژنوم |
| :--- | ---: | ---: |
| GC | **۴۷٫۴٪** | ۵۰٫۸٪ (کل ژنوم) |
| ‏CDS با محصول `uncharacterized`/`hypothetical` | **۳۰ از ۲۱۵ (۱۴٫۰٪)** | ۷۷ از ۴٬۰۸۸ (۱٫۹٪) |
| ژن کاذب | **۳۴ از ۱۴۵** ژن کاذب ژنوم (۲۳٪، در ۳٫۶٪ ژنوم) | ۱۱۱ |

پروفاژها: GC کمتر (سرچشمه‌ی بیرونی)، **هفت برابر** پروتئین ناشناخته، و **شش برابر** تراکم ژن کاذب (خفته = در حال فرسایش). و دو tRNA «افزوده»ی درس ۱ **دقیقاً روی مرز پایانی CP4-6 و DLP12**‌اند؛ tmRNA (*ssrA*) کنار **آغاز CP4-57**.

**این ۱۲ ناحیه را چه کسی یافت؟** بازبینی دستی و آزمایش در طول دهه‌ها. در ژنوم تازه‌ی یک ایزوله، ابزارهایی مانند **geNomad** این کار را می‌کنند (بخش ۴). پروفاژهای فرسوده (مانند PR-G، ۱۶۲ باز) برای ابزارها کمابیش **نادیدنی**‌اند: ژن نشانگر ندارند.

> 📺 **فیلم:** *Basics of phage genome annotation & classification*: https://www.youtube.com/watch?v=wO1w1Z1Or1w (Evelien Adriaenssens)
> 📄 **مرجع:** Camargo AP, et al. (2024). *Identification of mobile genetic elements with geNomad.* Nature Biotechnology 42:1303–1312.

---

## ۴. گام ۲: ابزارهای فاژ (از مستندات)

### ‏geNomad: یافتن فاژ و پروفاژ

‏geNomad هر توالی را به **کروموزوم، پلاسمید یا ویروس** دسته‌بندی می‌کند (شبکه‌ی عصبی + ژن‌های نشانگر)، **پروویروس**ها را درون کروموزوم می‌یابد و تاکسونومی ویروسی (ICTV) می‌دهد.

<div dir="ltr">

```bash
genomad download-database .                                       # once
genomad end-to-end --cleanup --splits 8 contigs.fa genomad_out genomad_db
```

</div>

‏`--splits 8` جست‌وجو را تکه‌تکه می‌کند تا حافظه‌ی کمتری بخواهد. نمونه‌ی خروجی `*_virus_summary.tsv` (**از مستندات**: README رسمی geNomad):

<div dir="ltr">

```text
seq_name                                 length  topology  coordinates      n_genes  genetic_code  virus_score  fdr  n_hallmarks  marker_enrichment  taxonomy
NZ_CP045015.1|provirus_3855947_3906705   50759   Provirus  3855947-3906705  79       11            0.9772       NA   16           73.7974            Viruses;Duplodnaviria;Heunggongvirae;Uroviricota;Caudoviricetes;;
```

</div>

- ‏`topology`: `Provirus` (درون میزبان)، `DTR` (تکرار مستقیم دو سر؛ نشانه‌ی ژنوم کامل)، `ITR`، یا `No terminal repeats`.
- ‏`virus_score`: ۰ تا ۱؛ پیش‌فرض دست‌کم ۰٫۷.
- ‏`n_hallmarks`: شمار ژن‌های نشانگر ویروسی.

### ‏CheckV: کیفیت ژنوم ویروس

همتای CheckM2 (ماژول ۰۱) برای ویروس‌ها: DNA میزبان را از دو سر پروویروس برمی‌دارد، کامل بودن را با ژنوم‌های ویروسی کامل می‌سنجد، و پنج سطح می‌دهد: Complete، High-quality (> ۹۰٪)، Medium (۵۰ تا ۹۰٪)، Low (< ۵۰٪)، Not-determined.

<div dir="ltr">

```bash
checkv end_to_end genomad_out/contigs_summary/contigs_virus.fna checkv_out -t 16
```

</div>

### ‏Pharokka و Phold: آنوتیشن فاژ

‏**Pharokka** گردش کار استاندارد آنوتیشن فاژ است: ژن‌ها با **PHANOTATE** (ویژه‌ی فاژ) یا در حالت متاژنوم با **prodigal-gv** (که کدهای ژنتیکی دیگر فاژها را هم می‌آزماید)؛ کارکرد با MMseqs2 و HMM در برابر **PHROGs** (خانواده‌های پروتئینی فاژ)، CARD و VFDB؛ و نزدیک‌ترین فاژ شناخته‌شده در INPHARED.

<div dir="ltr">

```bash
pharokka install -o pharokka_db                                          # once
pharokka run -i phage.fasta -o pharokka_out -d pharokka_db -t 8 --dnaapler
```

</div>

‏`--dnaapler` ژنوم را چنان می‌چرخاند که از ژن **TerL** آغاز شود (قرارداد). ‏**Phold** برای ژن‌هایی که Pharokka «unknown function» گذاشته، از **همانندی ساختاری** (ساختار پیش‌بینی‌شده و Foldseek) بهره می‌برد؛ روال پیشنهادی: نخست Pharokka، سپس Phold روی GenBank آن.

> 📺 **فیلم:** *Protein Structure-Informed Bacteriophage Genome Annotation with Phold*: https://www.youtube.com/watch?v=PItR8R_pl7o (George Bouras)
> 📄 **مرجع:** Bouras G, et al. (2023). *Pharokka.* Bioinformatics 39:btac776. https://doi.org/10.1093/bioinformatics/btac776

---

## ۵. گام ۳: ویروس یوکاریوتی با ابزار ORF (اجراشده)

در ویروس‌های یوکاریوتی، سازوکارهایی هست که یک ORF ساده نمی‌بیند:

| سازوکار | نمونه |
| :--- | :--- |
| **جابه‌جایی چارچوب برنامه‌ریزی‌شده (−۱)** | ‏SARS-CoV-2: پلی‌پروتئین pp1ab از ORF1a و ORF1b |
| **پلی‌پروتئین** که پروتئاز می‌بُرد | فلاوی‌ویروس‌ها، کروناویروس‌ها (`mat_peptide` در GenBank) |
| ‏**ORF هم‌پوشان** در چارچوب دیگر | ژن‌های کوچک درون ژن‌های بزرگ |
| **پیرایش** | آدنوویروس، HIV، آنفلوآنزا |
| **ژنوم چندتکه** | آنفلوآنزا (۸ تکه) |

‏Pyrodigal در حالت meta روی ژنوم مرجع SARS-CoV-2 (`NC_045512.2`، ۲۹٫۹ کیلوباز):

<div dir="ltr">

```bash
bash $S/virus_demo.sh
```

</div>

خلاصه‌ی خروجی (پیکان‌ها توضیح ماست):

<div dir="ltr">

```text
== reference CDS: 12 (ORF1ab has 2 segments: 266-13468 and 13468-21555, "translated by -1 ribosomal frameshift")
mature peptides (nsp1-16 etc.): 27
== Pyrodigal
266 13483 + 4405 aa        <- ORF1a (pp1a): correct
13768 21555 + 2595 aa      <- "ORF1b" as a separate gene, from an internal ATG
21563 25384 + 1273 aa      <- S (spike): correct
...
reference CDS: 12   predicted CDS: 9   same stop: 9   missed: 3 (all < 100 aa)
```

</div>

- ‏ORF1a و ژن‌های ساختاری بزرگ (S، M، N) درست یافته شدند.
- **پلی‌پروتئین pp1ab (۷٬۰۹۶ اسیدآمینه)** نیست؛ به‌جایش یک ORF جدا از یک ATG درونی. ۳۰۰ نوکلئوتید میان جای لغزش (13,468) و آن ATG، یعنی کمابیش ۱۰۰ اسیدآمینه از nsp12 (RNA پلیمراز)، در هیچ پروتئینی نیست.
- سه ژن کوتاه، **E**، **ORF7b** و **ORF10**، از دست رفتند.
- ‏**۲۷ پپتید بالغ** (nsp1 تا nsp16، …) در خروجی یک ابزار ORF اصلاً نمایش‌پذیر نیستند.

راه استاندارد: **آنوتیشن بر پایه‌ی مرجع**. ابزار NCBI برای این کار **VADR** است؛ GenBank ارسال‌های SARS-CoV-2، نوروویروس، دنگی، آنفلوآنزا، mpox و RSV را با آن بررسی و آنوتیت می‌کند، و ویژگی‌های نامنتظره (کدون پایان زودرس، frameshift، حذف) را به شکل **هشدار** (*alert*) گزارش می‌کند.

<div dir="ltr">

```bash
v-annotate.pl --mkey sarscov2 --mdir /path/to/vadr-models-sarscov2 sequences.fasta vadr_out
```

</div>

---

## ۶. سه اشتباه رایج

‏**۱. ‏Prodigal حالت `single` روی یک فاژ تنها.** ژنوم برای یادگیری کوتاه است؛ PHANOTATE یا `-p meta` / prodigal-gv.

**۲. «پروفاژ ندارد» چون ابزار چیزی نیافت.** پروفاژهای فرسوده ژن نشانگر ندارند؛ دنبال اینتگراز، tRNA مرزی و GC ناجور بگردید.

**۳. ابزار ORF برای ویروس RNA یوکاریوتی.** پلی‌پروتئین، frameshift و پیرایش دیده نمی‌شوند؛ آنوتیشن بر پایه‌ی مرجع (VADR).

---

## 📘 برای کنجکاوها

- ‏**‏PHASTEST:** وب‌سرور ویژه‌ی یافتن پروفاژ در ژنوم باکتری؛ جایگزین‌های دیگر: VIBRANT، VirSorter2.
- **کد ژنتیکی دیگر:** فاژهای crAss-like کدون پایان TAG را گلوتامین می‌خوانند (کد ۱۵)؛ با کد ۱۱ پروتئین‌هایشان بریده می‌شوند.
- ‏**‏MIUViG:** استاندارد کمینه‌ی اطلاعات برای ژنوم‌های ویروسی بازسازی‌شده؛ سطح‌های کیفیت CheckV بر پایه‌ی آن است.

---

## جمع‌بندی

- فاژ: کوچک، فشرده، ماژولار، و بیشتر ژن‌ها ناشناخته؛ PHANOTATE یا prodigal-gv برای ژن، PHROGs (Pharokka) برای کارکرد، ساختار (Phold) برای ناشناخته‌ها.
- پروفاژ: geNomad برای یافتن، CheckV برای کیفیت. ۱۲ پروفاژ خفته‌ی K-12: GC کمتر، ۷ برابر پروتئین ناشناخته، ۶ برابر ژن کاذب، و tRNA ناقص در مرزها.
- ویروس یوکاریوتی: frameshift، پلی‌پروتئین، پیرایش، ژنوم چندتکه؛ آنوتیشن **بر پایه‌ی مرجع** (VADR).

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
awk -F'\t' '$3 == "sequence_feature"' genome.gff | grep 'cryptic prophage'     # annotated prophages
genomad end-to-end --cleanup --splits 8 contigs.fa genomad_out genomad_db
checkv end_to_end virus_contigs.fna checkv_out -t 16
pharokka run -i phage.fasta -o pharokka_out -d pharokka_db -t 8 --dnaapler
v-annotate.pl --mkey sarscov2 --mdir MODELS sequences.fasta vadr_out
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| پروفاژ / پروویروس | ژنوم فاژ یا ویروس که در کروموزوم میزبان جا گرفته |
| فاژ معتدل / لیتیک | فاژی که می‌تواند پروفاژ شود / فاژی که همیشه سلول را می‌کشد |
| اینتگراز | آنزیمی که فاژ را در کروموزوم جا می‌دهد |
| ژن نشانگر (*hallmark*) | ژنی که کمابیش تنها در ویروس‌ها یافت می‌شود (TerL، پورتال، کپسید) |
| پلی‌پروتئین | یک پروتئین بلند که پروتئاز آن را به چند پروتئین بالغ می‌بُرد |
| ‏PHROGs | پایگاه خانواده‌های پروتئینی فاژ |

---

## منابع

**مستند و مقاله**
- Bouras G, et al. (2023). *Pharokka: a fast scalable bacteriophage annotation tool.* Bioinformatics 39:btac776. https://doi.org/10.1093/bioinformatics/btac776
- Terzian P, et al. (2021). *PHROG: families of prokaryotic virus proteins clustered using remote homology.* NAR Genomics and Bioinformatics 3:lqab067. https://doi.org/10.1093/nargab/lqab067
- Camargo AP, et al. (2024). *Identification of mobile genetic elements with geNomad.* Nature Biotechnology 42:1303–1312. https://doi.org/10.1038/s41587-023-01953-y
- Nayfach S, et al. (2021). *CheckV assesses the quality and completeness of metagenome-assembled viral genomes.* Nature Biotechnology 39:578–585. https://doi.org/10.1038/s41587-020-00774-7
- Schäffer AA, et al. (2020). *VADR: validation and annotation of virus sequence submissions to GenBank.* BMC Bioinformatics 21:211. https://doi.org/10.1186/s12859-020-3537-3
- Pharokka: https://github.com/gbouras13/pharokka · Phold: https://github.com/gbouras13/phold · geNomad: https://github.com/apcamargo/genomad · VADR: https://github.com/ncbi/vadr

**کتاب**
- Clokie MRJ, Kropinski AM (eds.) (2009). *Bacteriophages: Methods and Protocols, Volume 2: Molecular and Applied Aspects*. Methods Mol Biol 502. Humana Press.

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins University). دوره‌ای ویژه‌ی آنوتیشن فاژ در Coursera نیافتیم؛ نزدیک‌ترین: https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Linux* (The Linux Foundation). دوره‌ای ویژه در edX نیافتیم؛ نزدیک‌ترین: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux
- YouTube: *Basics of phage genome annotation & classification* (Evelien Adriaenssens، Phage Directory): https://www.youtube.com/watch?v=wO1w1Z1Or1w
- YouTube: *Protein Structure-Informed Bacteriophage Genome Annotation with Phold* (George Bouras): https://www.youtube.com/watch?v=PItR8R_pl7o

<sub>نشانی‌های YouTube و DOIها در 2026-10-15 وارسی شدند؛ نشانی‌های Coursera و edX در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
