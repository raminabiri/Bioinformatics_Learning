<div dir="rtl">

# درس ۲: آنوتیشن فاژ، پروفاژ و ویروس

**بخش:** `07_Bacterial_Genomics` · **ماژول:** `02_Genome_Annotation` · **پیش‌نیاز:** درس ۱ همین ماژول · **زمان:** ۱٫۵ ساعت · **ابزار (مستندات‌شده):** Pharokka 1.10، Phold، geNomad، CheckV، VADR، pyrodigal-gv · **آخرین بازبینی:** 2026-10-15

> ✍️ **وضعیت:** ابزارهای این درس روی سرور دوره نصب نیستند و **اجرا نشده‌اند**. دستورها، گزینه‌ها و نمونه‌خروجی‌ها از README رسمی هر ابزار است و منبعش ذکر شده. بخش ۳ (پروفاژهای *E. coli* K-12) **اجراشده** است: محاسبه‌ی سبک روی GFF و FASTA همان ژنوم.

---

## ۱. چرا جدا؟

فاژها و ویروس‌ها از نظر **کمیت** در زیست‌کره غالب‌اند. در هر ژنوم باکتری هم معمولاً چند **پروفاژ** (فاژ واردشده در کروموزوم) هست. بسیاری از ژن‌های ضراوت (مثل سم شیگا در *E. coli* EHEC، یا سم وبا) روی پروفاژها حمل می‌شوند. ولی ابزارهای درس ۱ برای آن‌ها خوب کار نمی‌کنند:

| ویژگی | باکتری | فاژ | ویروس یوکاریوتی |
| :--- | :--- | :--- | :--- |
| اندازه‌ی ژنوم | ۰٫۵ تا ۱۳ مگاباز | **۳ تا ۷۰۰ کیلوباز** (بیشتر ۲۰ تا ۲۰۰) | ۲ کیلوباز تا ۲ مگاباز (ویروس‌های غول) |
| ماده‌ی ژنتیکی | dsDNA | بیشتر dsDNA؛ ssDNA، RNA هم | همه نوع: dsDNA، ssDNA، (+)RNA، (−)RNA، ژنوم قطعه‌قطعه |
| تراکم ژن | حدود ۸۸٪ | **حدود ۹۰ تا ۹۵٪**؛ ژن‌ها گاهی همپوشان | بسیار متغیر؛ **ORF همپوشان** رایج |
| ژن‌های «hypothetical» | ۵ تا ۲۰٪ | **۶۰ تا ۸۰٪** | متغیر |
| آموزش مدل ژن روی خود ژنوم | ✅ | ❌ ژنوم کوچک است | ❌ |
| کد ژنتیکی | ۱۱ (یا ۴) | ۱۱؛ گاهی **تغییر کدون پایان** (مثلاً کد ۱۵: TAG = Gln) | کد میزبان؛ **جابه‌جایی چارچوب**، پلی‌پروتئین، پیرایش، ویرایش RNA |

## ۲. مفاهیم کلیدی

### ۲.۱ ساختار ماژولار ژنوم فاژ
ژن‌های فاژهای دم‌دار (Caudoviricetes) در **ماژول‌های عملکردی** پشت سر هم چیده شده‌اند: بسته‌بندی DNA و سر، اتصال، دم، لیز، ادغام و برش، تنظیم رونویسی، متابولیسم DNA/RNA. **PHROGs** (Terzian et al. 2021) ده‌ها هزار خانواده‌ی پروتئینی فاژ را در همین دسته‌های عملکردی (به‌علاوه‌ی «سایر» و «عملکرد نامعلوم») طبقه‌بندی کرده است. Pharokka هر ژن را به یکی از آن‌ها نسبت می‌دهد.

**ژن‌های نشانگر (hallmark)** در تشخیص فاژ مهم‌اند: **زیرواحد بزرگ ترمیناز** (TerL)، **پروتئین پورتال** و **پروتئین کپسید اصلی** (MCP) تقریباً در همه‌ی فاژهای دم‌دار هستند و در ژنوم باکتری نه. طبق قرارداد، ژنوم فاژ را طوری می‌چرخانند که از ژن **TerL** شروع شود (Pharokka با `--dnaapler` این کار را می‌کند).

### ۲.۲ معتدل در برابر لیتیک، و پروفاژ
- **فاژ لیتیک:** آلوده می‌کند، تکثیر می‌شود و سلول را می‌کُشد.
- **فاژ معتدل (temperate):** با **اینتگراز** خودش در کروموزوم وارد می‌شود و به‌شکل **پروفاژ** با باکتری تقسیم می‌شود. اغلب در محل یک **tRNA** یا tmRNA وارد می‌شود. توالی اتصال (attB/attP) بخشی از tRNA را تکرار می‌کند، پس ژن tRNA سالم می‌ماند و یک **تکه‌ی تکراری** در مرز دیگر پروفاژ باقی می‌ماند.
- **پروفاژ خفته (cryptic):** پروفاژی که با جهش و حذف دیگر نمی‌تواند خارج و تکثیر شود. ژن‌هایش اغلب ژن کاذب‌اند، ولی بعضی هنوز برای میزبان مفیدند (مقاومت به استرس، تشکیل بیوفیلم).

## ۳. پروفاژهای *E. coli* K-12 (اجراشده)

آنوتیشن RefSeq این ژنوم ۱۲ ناحیه را با `Note=cryptic prophage` مشخص کرده است (ویژگی `sequence_feature` در GFF):

<div dir="ltr">

```bash
G=../../01_Linux/99_scripts_data/02_Bash/data
grep -P '\tsequence_feature\t' $G/ecoli_k12.gff | grep 'cryptic prophage' \
  | awk -F'\t' '{match($9,/Note=[^;]+/); print $4, $5, $5-$4+1, substr($9,RSTART+5,RLENGTH-5)}'
```

</div>

| پروفاژ | شروع | پایان | طول (باز) |
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

مجموع: **۱۶۸٬۱۶۵ باز (۳٫۶٪ ژنوم)**. سه ویژگی این نواحی را با یک محاسبه‌ی ساده (Python، چند ثانیه؛ تمرین ۴) با بقیه‌ی ژنوم مقایسه کردیم:

| | پروفاژها | بقیه‌ی ژنوم |
| :--- | ---: | ---: |
| GC | **۴۷٫۴٪** | ۵۰٫۸٪ (کل ژنوم) |
| ‏CDS با محصول `uncharacterized`/`hypothetical` | **۳۰ از ۲۱۵ (۱۴٫۰٪)** | ۷۷ از ۴٬۰۸۸ (۱٫۹٪) |
| ژن کاذب | **۳۴ از ۱۴۵** کل ژن‌های کاذب ژنوم (۲۳٪، در ۳٫۶٪ ژنوم) | ۱۱۱ |

پروفاژها: GC کمتر (منشأ بیرونی، مثل ژن‌های کم‌GC ماژول 02/01)، **هفت برابر** پروتئین ناشناخته، و **شش برابر** تراکم ژن کاذب (خفته = در حال فرسایش).

و ارتباط با درس ۱: دو tRNA «اضافه» که tRNAscan-SE پیدا کرد (امتیاز ۴۴ و ۳۲)، **دقیقاً روی مرز پایانی CP4-6 و DLP12** هستند. سومی، ژن ***ssrA*** (tmRNA)، کنار **شروع CP4-57** است. این‌ها رد پای همان مکانیسم ورود از طریق tRNA در بخش ۲.۲‌اند.

**این ۱۲ ناحیه را چه کسی پیدا کرد؟** بازبینی دستی و آزمایش در طول دهه‌ها. در ژنوم تازه‌ی یک ایزوله، این کار را ابزارهایی مثل **geNomad** انجام می‌دهند (بخش ۴.۱). پروفاژهای خفته و فرسوده (مثل PR-G، ۱۶۲ باز) برای ابزارهای خودکار تقریباً **نامرئی‌اند**: ژن نشانگر کافی ندارند.

## ۴. ابزارها

### ۴.۱ پیدا کردن فاژ و پروفاژ: geNomad
‏geNomad (Camargo et al. 2024) هر توالی را به **کروموزوم، پلاسمید یا ویروس** طبقه‌بندی می‌کند، با ترکیب یک شبکه‌ی عصبی (بدون نیاز به همترازی) و **ژن‌های نشانگر**. **پروویروس**ها را هم درون کروموزوم پیدا می‌کند و تاکسونومی ویروسی (ICTV) می‌دهد.

<div dir="ltr">

```bash
genomad download-database .                                       # once
genomad end-to-end --cleanup --splits 8 contigs.fa genomad_out genomad_db
```

</div>

‏`--splits 8` جستجو را تکه‌تکه می‌کند تا حافظه کمتری مصرف شود. نمونه‌ی خروجی `*_virus_summary.tsv` (**از مستندات**: README رسمی geNomad، روی یک ژنوم باکتری نمونه):

<div dir="ltr">

```text
seq_name                                 length  topology  coordinates      n_genes  genetic_code  virus_score  fdr  n_hallmarks  marker_enrichment  taxonomy
NZ_CP045015.1|provirus_3855947_3906705   50759   Provirus  3855947-3906705  79       11            0.9772       NA   16           73.7974            Viruses;Duplodnaviria;Heunggongvirae;Uroviricota;Caudoviricetes;;
```

</div>

- ‏`topology`: `Provirus` (درون میزبان)، `DTR` (تکرار مستقیم انتهایی، نشانه‌ی ژنوم کامل یا دایره‌ای)، `ITR` (تکرار معکوس) یا `No terminal repeats`.
- ‏`virus_score`: ۰ تا ۱. پیش‌فرض: حداقل ۰٫۷، و توالی‌های کوتاه‌تر از ۲٬۵۰۰ باز باید **حداقل یک ژن نشانگر** داشته باشند.
- ‏`n_hallmarks`: تعداد ژن‌های نشانگر ویروسی.

جایگزین‌ها و مکمل‌ها: **PHASTEST** (وب‌سرور، مخصوص پروفاژ در ژنوم باکتری)، VIBRANT، VirSorter2.

### ۴.۲ کیفیت ژنوم ویروس: CheckV
معادل CheckM2 (ماژول ۰۱) برای ویروس‌ها (Nayfach et al. 2021):
1. **حذف آلودگی میزبان** از پروویروس‌ها: ژن‌ها با HMMهای ویروسی و میکروبی برچسب می‌خورند و مرز پروویروس دقیق‌تر می‌شود.
2. **کامل بودن**: مقایسه‌ی پروتئین‌ها (AAI) با دیتابیس ژنوم‌های ویروسی کامل و **نسبت طول**. اگر مرجع نزدیکی نباشد، بازه‌ای بر اساس HMMها.
3. **ژنوم بسته**: DTR، ITR یا پروویروس کامل.

<div dir="ltr">

```bash
checkv end_to_end genomad_out/contigs_summary/contigs_virus.fna checkv_out -t 16
```

</div>

پنج سطح کیفیت در `quality_summary.tsv` (منطبق با استاندارد **MIUViG**): **Complete**، **High-quality** (کامل بودن > ۹۰٪)، **Medium-quality** (۵۰ تا ۹۰٪)، **Low-quality** (< ۵۰٪) و Not-determined.

### ۴.۳ آنوتیشن فاژ: Pharokka و Phold
‏**Pharokka** (Bouras et al. 2023) خط لوله‌ی استاندارد آنوتیشن فاژ است:
- **پیش‌بینی ژن:** پیش‌فرض **PHANOTATE**، تنها ابزار پیش‌بینی ژن مخصوص فاژ (ژن‌های فشرده و همپوشان را بهتر پیدا می‌کند). در حالت متاژنوم (`-m`) پیش‌فرض **prodigal-gv** است، که **کدهای ژنتیکی جایگزین** فاژها (مثلاً ۱۵ و ۴) را هم امتحان می‌کند. برای فاژهای RNA: `pyrodigal-rv`.
- **آنوتیشن عملکردی:** MMseqs2 در برابر **PHROGs**، **CARD** (مقاومت) و **VFDB** (ضراوت)، و از نسخه‌ی 1.4 جستجوی حساس‌تر HMM روی PHROGs با PyHMMER.
- **بقیه:** tRNA (tRNAscan-SE)، tmRNA (ARAGORN)، CRISPR (MinCED)، و نزدیک‌ترین فاژ شناخته‌شده در دیتابیس **INPHARED** (با Mash).

<div dir="ltr">

```bash
pharokka install -o pharokka_db                                       # once (v1.10+; older: install_databases.py)
pharokka run -i phage.fasta -o pharokka_out -d pharokka_db -t 8 --dnaapler
pharokka run -i metavirome_contigs.fasta -o pharokka_meta -d pharokka_db -t 8 -m    # many contigs
```

</div>

از نسخه‌ی 1.10، دستور اصلی `pharokka run` است (`pharokka.py` قدیمی منسوخ شده). خروجی‌ها: `pharokka.gff`، `pharokka.gbk`، و `pharokka_cds_functions.tsv` (تعداد CDS، tRNA، tmRNA، CRISPR و تعداد ژن در هر دسته‌ی PHROG).

‏**Phold** (همان نویسندگان) برای ژن‌هایی که Pharokka «unknown function» گذاشته، از **شباهت ساختاری** استفاده می‌کند: ساختار سه‌بعدی پروتئین را پیش‌بینی و با Foldseek در دیتابیس ساختارها جستجو می‌کند. طبق README، Phold آنوتیشن را «به‌شدت» بهتر می‌کند، به‌خصوص برای فاژهای متاژنومی. ولی tRNA، tmRNA، CRISPR و جستجوی INPHARED را ندارد. پس روال توصیه‌شده: **اول Pharokka، بعد Phold روی خروجی GenBank آن**.

### ۴.۴ ویروس‌های یوکاریوتی: آنوتیشن بر اساس مرجع
برای ویروس‌های یوکاریوتی، پیش‌بینی ab initio اغلب کار نمی‌کند. دلیلش مکانیسم‌هایی است که یک ORF ساده نمی‌بیند:

| مکانیسم | مثال |
| :--- | :--- |
| **جابه‌جایی چارچوب برنامه‌ریزی‌شده (−۱)** | ‏SARS-CoV-2: پلی‌پروتئین pp1ab از ORF1a و ORF1b با یک لغزش ریبوزومی؛ HIV-1: gag-pol |
| **پلی‌پروتئین** که با پروتئاز بریده می‌شود | فلاوی‌ویروس‌ها (دنگی، زیکا)، پیکورناویروس‌ها، کروناویروس‌ها (ویژگی `mat_peptide` در GenBank) |
| ‏**ORF همپوشان** در قاب دیگر | ژن‌های کوچک درون ژن‌های بزرگ در ویروس‌های کوچک |
| **پیرایش (splicing)** | آدنوویروس، هرپس‌ویروس، HIV؛ M2 و NS2 در آنفلوآنزا |
| **ویرایش RNA** | پروتئین‌های P/V/W در پارامیکسوویروس‌ها |
| **ژنوم قطعه‌قطعه** | آنفلوآنزا (۸ قطعه)، روتاویروس |

**نمایش (اجراشده):** Pyrodigal در حالت meta روی ژنوم مرجع SARS-CoV-2 (`NC_045512.2`، ۲۹٫۹ کیلوباز). دستور: `bash scripts/virus_demo.sh`، با دانلود ۴۵ کیلوبایت و ۲ ثانیه اجرا. خلاصه‌ی خروجی (فلش‌ها توضیح ماست):

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

- ‏ORF1a و همه‌ی ژن‌های ساختاری بزرگ (S، M، N و غیره) درست پیدا شدند.
- **پلی‌پروتئین pp1ab (۷٬۰۹۶ اسیدآمینه)** وجود ندارد. به‌جایش یک ORF جدا از یک ATG داخلی در 13,768 آمده است. ۳۰۰ نوکلئوتید بین محل لغزش (13,468) و آن ATG، یعنی حدود ۱۰۰ اسیدآمینه از nsp12 (RNA پلیمراز)، در هیچ پروتئینی نیست.
- سه ژن کوتاه، **E**، **ORF7b** و **ORF10**، از دست رفتند.
- **۲۷ پپتید بالغ** (nsp1 تا nsp16 و غیره) که پروتئاز ویروسی از پلی‌پروتئین‌ها می‌بُرد، در خروجی یک ابزار ORF اصلاً قابل نمایش نیستند.

راه استاندارد: **انتقال آنوتیشن از یک ژنوم مرجع نزدیک**. ابزار NCBI برای این کار **VADR** (Viral Annotation DefineR) است. طبق README، مدل‌های آماده برای نوروویروس، دنگی، SARS-CoV-2 و دیگر فلاوی‌ویروس‌ها، کالیسی‌ویروس‌ها و کروناویروس‌ها، آنفلوآنزا، mpox و RSV دارد. GenBank ارسال‌های این ویروس‌ها را با همین ابزار **بررسی و آنوتیت** می‌کند. `v-annotate.pl` ویژگی‌های غیرمنتظره (مثلاً کدون پایان زودرس، frameshift، یا حذف) را به‌شکل **هشدار (alert)** گزارش می‌کند. توالی با هشدار جدی **رد** می‌شود.

<div dir="ltr">

```bash
v-annotate.pl --mkey sarscov2 --mdir /path/to/vadr-models-sarscov2 sequences.fasta vadr_out
```

</div>

مدل و پارامترهای دقیق برای هر ویروس در مستندات VADR آمده است (مثلاً برای SARS-CoV-2 گزینه‌های اضافی برای توالی‌های پر از N).

برای ویروس‌های **بدون مدل VADR**: آنوتیشن مرجع نزدیک‌ترین ژنوم RefSeq را با همترازی منتقل کنید، یا Prokka با `--kingdom Viruses` برای پیش‌بینی ساده، یا وب‌سرویس‌هایی مثل Genome Detective و BV-BRC.

## ۵. دام‌ها (Pitfalls)

| دام | چرا مشکل است | راه درست |
| :--- | :--- | :--- |
| ‏Prodigal حالت `single` روی فاژ تنها | ژنوم برای آموزش کوتاه است | ‏PHANOTATE یا `-p meta` / prodigal-gv |
| فرض کد ۱۱ برای همه‌ی فاژها | فاژهای با تغییر کدون پایان (مثلاً crAss-like) پروتئین‌های بریده می‌گیرند | ‏prodigal-gv (چند کد را امتحان می‌کند) |
| «پروفاژ ندارد» چون ابزار چیزی پیدا نکرد | پروفاژهای فرسوده نشانگر کافی ندارند | دنبال اینتگراز، tRNA مرزی و GC غیرعادی بگردید |
| اعتماد به مرز پروویروس | مرز دقیق با ابزار خودکار ±چند کیلوباز است | ‏CheckV (حذف میزبان) + att/tRNA |
| ‏«hypothetical» = بی‌اهمیت | ۶۰ تا ۸۰٪ ژن‌های فاژ | ‏Phold (ساختار)، بافت ماژول ژنی |
| ‏ab initio برای ویروس RNA یوکاریوتی | پلی‌پروتئین، frameshift و پیرایش دیده نمی‌شوند | آنوتیشن بر اساس مرجع (VADR) |
| ژن مقاومت یا سم روی کانتیگ فاژی | ممکن است روی پروفاژ قابل انتقال باشد | گزارش «پروفاژی»؛ بخش ۰۸ |
| ژنوم فاژ از نقطه‌ی دلخواه | مقایسه‌ی بین ژنوم‌ها سخت | چرخاندن به TerL (`--dnaapler`) |

## ۶. جمع‌بندی
- فاژ: کوچک، فشرده، ماژولار، و اکثر ژن‌ها ناشناخته. PHANOTATE یا prodigal-gv برای ژن، PHROGs برای عملکرد (Pharokka) و ساختار برای ناشناخته‌ها (Phold).
- پروفاژ: geNomad یا PHASTEST برای یافتن، CheckV برای کیفیت. ۱۲ پروفاژ خفته‌ی K-12: GC کمتر، ۷ برابر پروتئین ناشناخته، ۶ برابر ژن کاذب، و tRNA ناقص در مرزها.
- ویروس یوکاریوتی: frameshift، پلی‌پروتئین، پیرایش و ژنوم قطعه‌قطعه. آنوتیشن **بر اساس مرجع** (VADR برای ویروس‌های مهم بالینی).

---

## منابع

### مقاله‌ها
- Bouras G, et al. (2023). Pharokka: a fast scalable bacteriophage annotation tool. *Bioinformatics* 39:btac776. https://doi.org/10.1093/bioinformatics/btac776
- Terzian P, et al. (2021). PHROG: families of prokaryotic virus proteins clustered using remote homology. *NAR Genomics and Bioinformatics* 3:lqab067. https://doi.org/10.1093/nargab/lqab067
- McNair K, et al. (2019). PHANOTATE: a novel approach to gene identification in phage genomes. *Bioinformatics* 35:4537–4542. https://doi.org/10.1093/bioinformatics/btz265
- Camargo AP, et al. (2024). Identification of mobile genetic elements with geNomad. *Nature Biotechnology* 42:1303–1312. https://doi.org/10.1038/s41587-023-01953-y
- Nayfach S, et al. (2021). CheckV assesses the quality and completeness of metagenome-assembled viral genomes. *Nature Biotechnology* 39:578–585. https://doi.org/10.1038/s41587-020-00774-7
- Roux S, et al. (2019). Minimum Information about an Uncultivated Virus Genome (MIUViG). *Nature Biotechnology* 37:29–37. https://doi.org/10.1038/nbt.4306
- Schäffer AA, et al. (2020). VADR: validation and annotation of virus sequence submissions to GenBank. *BMC Bioinformatics* 21:211. https://doi.org/10.1186/s12859-020-3537-3
- Wishart DS, et al. (2023). PHASTEST: faster than PHASTER, better than PHAST. *Nucleic Acids Research* 51:W443–W450. https://doi.org/10.1093/nar/gkad382

### مستندات
- Pharokka: https://github.com/gbouras13/pharokka
- Phold: https://github.com/gbouras13/phold
- geNomad: https://github.com/apcamargo/genomad
- CheckV: https://bitbucket.org/berkeleylab/checkv
- VADR: https://github.com/ncbi/vadr

### ویدیوهای آموزشی
- Evelien Adriaenssens (Quadram Institute) — *Basics of phage genome annotation & classification* (Phage Directory): https://www.youtube.com/watch?v=wO1w1Z1Or1w
- George Bouras — *Protein Structure-Informed Bacteriophage Genome Annotation with Phold* (Microbiome Virtual International Forum): https://www.youtube.com/watch?v=PItR8R_pl7o
- Center for Phage Technology, Texas A&M University — *CPT functional workflow for phage genome annotation*: https://www.youtube.com/watch?v=33Nw1egzYPg

> لینک‌ها در تاریخ 2026-10-15 بررسی شدند (`_tools/check_links.sh`).

</div>
