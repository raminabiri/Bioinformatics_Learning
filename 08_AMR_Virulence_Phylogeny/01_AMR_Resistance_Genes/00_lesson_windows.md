<div dir="rtl">

# درس (مسیر ویندوز): ژن‌ها و جهش‌های مقاومت، بی لینوکس

**بخش:** `08_AMR_Virulence_Phylogeny` · **ماژول:** `01_AMR_Resistance_Genes` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [آماده کردن ویندوز](../../windows/README.md) (پایتون با Biopython، BLAST+)؛ داستان و مفهوم‌ها از [درس ۱](01_lesson_amrfinder.md) · **زمان:** حدود ۷۵ دقیقه · **ابزار:** Python 3 + Biopython 1.87، BLAST+ 2.17.0 (نسخه‌ی ویندوزی)، ResFinder و CARD RGI (وب) · **آخرین بازبینی:** 2026-10-27

> ✍️ **وضعیت:** گام‌های ۱ تا ۳ (پایتون و BLAST+) روی سرور دوره **اجرا شدند** و خروجی‌شان واقعی است؛ همین کدها روی ویندوز یکسان کار می‌کنند. گام‌های ۴ و ۵ (ResFinder و CARD در مرورگر) از **مستندات** نوشته شده‌اند و تنها **پاسخ معلوم** را برای سنجیدن می‌دهند، نه خروجی واقعی. روی ویندوز آزموده نشده است.

---

## در یک نگاه

این درس همان کار [درس ۱](01_lesson_amrfinder.md) (AMRFinderPlus روی سه ژنوم با پاسخ معلوم) را **روی ویندوز** انجام می‌دهد. ‏AMRFinderPlus نسخه‌ی ویندوزی ندارد؛ به جایش:

**در پایان این درس می‌توانید:**
1. سه ژنوم شبیه‌سازی‌شده را با پایتون روی ویندوز بسازید.
2. ژن‌های **اکتسابی** را با **BLAST+** روی ویندوز بیابید و پوشش ژن را بخوانید.
3. **جهش‌های نقطه‌ای** gyrA و parC را با یک اسکریپت Biopython بسنجید.
4. همان ژنوم‌ها را به **ResFinder** و **CARD RGI** در مرورگر بدهید و نتیجه را با پاسخ معلوم بسنجید.

**پیش از خواندن:** از درس ۱، بخش‌های **۱ (داستان)** و **۲ (مفهوم به زبان ساده: سه راه مقاومت، و داده‌ی این درس)** را بخوانید. این درس آن‌ها را تکرار نمی‌کند.

**پاسخ معلوم** (درس ۱، بخش ۲.۳):

| ایزوله | آنچه به K-12 افزوده شده |
| :--- | :--- |
| ‏isoA | جهش gyrA S83L؛ ژن کامل blaCTX-M-15 روی contig «پلاسمید» `isoA_pA` |
| ‏isoB | جهش parC S80I؛ ژن کامل blaNDM-1 و **نیمه‌ی نخست** tet(A) روی `isoB_pB` |
| ‏isoC | هیچ (کنترل منفی) |

---

## ۱. گام ۰: پوشه و داده (PowerShell)

‏✍️ PowerShell را باز کنید (منوی Start ← PowerShell). فرض: دوره را از GitHub گرفته و در `$HOME\Bioinformatics_Learning-main` باز کرده‌اید ([آماده کردن ویندوز](../../windows/README.md)).

<div dir="ltr">

```powershell
mkdir $HOME\amr; cd $HOME\amr
$C = "$HOME\Bioinformatics_Learning-main"
py $C\windows\get_k12_genome.py
copy $C\08_AMR_Virulence_Phylogeny\99_scripts_data\data\acquired_genes.fna .
```

</div>

| بخش | کار |
| :--- | :--- |
| ‏`mkdir …; cd …` | پوشه‌ی کار را بساز و به آن برو |
| ‏`$C = "…"` | یک **متغیر** در PowerShell (مانند `C=…` در لینوکس، ولی با `$` در هر دو جا) |
| ‏`py …\get_k12_genome.py` | ژنوم و GFF ‏K-12 را بگیر و باز کن (همان فایل‌های بخش ۰۱؛ MD5 یکسان) |
| ‏`copy … .` | سه ژن اکتسابی را به پوشه‌ی کنونی (`.`) کپی کن |

---

## ۲. گام ۱: ساختن سه ژنوم با پایتون

همان اسکریپت پایتون درس ۱ (گام ۱) است. پایتون است، پس روی ویندوز هم کار می‌کند:

<div dir="ltr">

```powershell
py $C\08_AMR_Virulence_Phylogeny\99_scripts_data\01_AMR_Resistance_Genes\scripts\make_mock_isolates.py ecoli_k12.fna ecoli_k12.gff acquired_genes.fna genomes
dir genomes
```

</div>

**خروجی واقعی** (همان اسکریپت روی سرور دوره، 2026-10-27):

<div dir="ltr">

```
gyrA S83L: TCG -> TTG
parC S80I: AGC -> ATC
Done: genomes
```

</div>

پوشه‌ی `genomes` چهار فایل می‌گیرد: `isoA.fna`، `isoB.fna`، `isoC.fna` (هر کدام نزدیک به ۴٫۷ مگابایت) و `ground_truth_amr.tsv`. فایل آخر را در **Excel** باز کنید (Data ← From Text/CSV): همان جدول پاسخ معلوم بالا است.

---

## ۳. گام ۲: ژن‌های اکتسابی با BLAST+

**چرا؟** ‏AMRFinderPlus ژن‌های اکتسابی را با هم‌ترازی پیدا می‌کند (درس ۱، بخش ۲.۲). روی ویندوز همین را با **BLAST+** (11/07) انجام می‌دهیم: سه ژن مرجع را در هر ژنوم می‌جوییم.

<div dir="ltr">

```powershell
foreach ($i in "isoA", "isoB", "isoC") { "== $i"; blastn -query acquired_genes.fna -subject genomes\$i.fna -outfmt "6 qseqid sseqid pident length qlen qcovs sstart send evalue" -evalue 1e-20 }
```

</div>

| بخش | کار |
| :--- | :--- |
| ‏`foreach ($i in …) { … }` | حلقه در PowerShell (همان `for i in …; do …; done` لینوکس) |
| ‏`"== $i"` | یک رشته را چاپ کن (سرخط هر ایزوله) |
| ‏`-subject` | ژنوم را مستقیم بده، بی ساختن پایگاه BLAST (11/07) |
| ‏`qlen` و `qcovs` | طول ژن مرجع و **درصد آن که در ژنوم یافت شد** |
| ‏`-evalue 1e-20` | تنها برخوردهای بسیار مطمئن |

**خروجی واقعی** (BLAST+ 2.17.0 روی سرور دوره، 2026-10-27):

<div dir="ltr">

```
== isoA
blaCTX-M-15	isoA_pA	100.000	876	876	100	2001	2876	0.0
== isoB
tet(A)	isoB_pB	100.000	600	1200	50	4314	4913	0.0
blaNDM-1	isoB_pB	100.000	813	813	100	2001	2813	0.0
== isoC
```

</div>

**توضیح خروجی:**
- ‏isoA: ‏blaCTX-M-15 **کامل** (۸۷۶ از ۸۷۶ باز، پوشش ۱۰۰٪، یکسانی ۱۰۰٪) روی `isoA_pA`. ✅
- ‏isoB: ‏blaNDM-1 کامل و **tet(A) با پوشش ۵۰٪**: تنها ۶۰۰ از ۱۲۰۰ باز. ✅ همان «نیمه‌ی نخست» پاسخ معلوم. ‏AMRFinderPlus در درس ۱ همین را `PARTIALX` با ۵۰٫۳۸٪ (بر پایه‌ی اسید آمینه) گزارش کرد.
- ‏isoC: هیچ سطری. کنترل منفی درست است. ✅
- ‏`sstart` جای ژن روی contig است (آغاز ۲۰۰۱؛ اسکریپت ۲۰۰۰ باز DNA تصادفی پیش از ژن گذاشته بود).

**فرق با AMRFinderPlus:** این‌جا تنها **سه** ژنی را جستیم که از پیش داشتیم. AMRFinderPlus هزاران ژن مرجع را یک‌جا می‌جوید. برای ژنوم ناشناخته از ابزار وب گام ۴ بهره ببرید.

---

## ۴. گام ۳: جهش‌های نقطه‌ای با Biopython

**چرا؟** مقاومت به کینولون‌ها با جهش در **gyrA** (جایگاه‌های ۸۳ و ۸۷) و **parC** (۸۰ و ۸۴) است، نه با ژن تازه (درس ۱، بخش ۲.۱). BLAST این را نمی‌گوید؛ باید کدون همان جایگاه را بخوانیم و ترجمه کنیم. اسکریپت `check_qrdr.py` جای دو ژن را از GFF برمی‌دارد، توالی را از هر ژنوم می‌برد و چهار کدون را ترجمه می‌کند.

<div dir="ltr">

```powershell
py $C\08_AMR_Virulence_Phylogeny\99_scripts_data\01_AMR_Resistance_Genes\scripts\check_qrdr.py ecoli_k12.gff genomes\isoA.fna genomes\isoB.fna genomes\isoC.fna
```

</div>

**هسته‌ی اسکریپت** (Biopython، بخش 03/04):

<div dir="ltr">

```python
chrom = next(SeqIO.parse(path, "fasta")).seq        # first record = chromosome
dna = chrom[start - 1:end]                           # GFF is 1-based, Python is 0-based
if strand == "-":
    dna = dna.reverse_complement()
codon = str(dna[(pos - 1) * 3:pos * 3])
aa = str(Seq(codon).translate())
```

</div>

‏`start - 1` همان «منهای یک» 12/02 است: GFF از ۱ می‌شمارد و پایتون از ۰. کدون جایگاه `pos` (از ۱) از باز `(pos − 1) × 3` تا `pos × 3` است.

**خروجی واقعی** (روی سرور دوره، 2026-10-27؛ ۰٫۲۷ ثانیه):

<div dir="ltr">

```
genome	gene	position	codon	aa	wild_type	status
isoA	gyrA	83	TTG	L	S	MUTANT S83L
isoA	gyrA	87	GAC	D	D	wild type
isoA	parC	80	AGC	S	S	wild type
isoA	parC	84	GAA	E	E	wild type
isoB	gyrA	83	TCG	S	S	wild type
isoB	gyrA	87	GAC	D	D	wild type
isoB	parC	80	ATC	I	S	MUTANT S80I
isoB	parC	84	GAA	E	E	wild type
isoC	gyrA	83	TCG	S	S	wild type
isoC	gyrA	87	GAC	D	D	wild type
isoC	parC	80	AGC	S	S	wild type
isoC	parC	84	GAA	E	E	wild type
```

</div>

‏isoA: ‏gyrA **S83L** ‏(TCG → TTG)؛ isoB: ‏parC **S80I** ‏(AGC → ATC)؛ isoC: همه وحشی. ✅ درست همان پاسخ معلوم و همان جهش‌هایی که AMRFinderPlus در درس ۱ با `POINTX` یافت. برای دیدن جدول در Excel، خروجی را در فایل بنویسید: `… > qrdr.tsv`.

<details>
<summary>✋ امتحان کن: اگر در اسکریپت <code>chrom[start - 1:end]</code> را <code>chrom[start:end]</code> بنویسید چه می‌شود؟ و اگر <code>chrom[start - 1:end - 1]</code>؟</summary>

ما هر دو را آزمودیم (روی سرور دوره):
- ‏**`chrom[start:end]`**: خروجی **درست همانند** بالاست! چرا؟ gyrA و parC هر دو روی **رشته‌ی منفی**‌اند (ستون ۷ ‏GFF: `-`). پس سرِ `start` (عدد کوچک‌تر) همان پایان 3′ ژن، کنار کدون پایان، است. حذف یک باز از آن‌جا کدون‌های ۸۰ تا ۸۷ را جابه‌جا نمی‌کند. خطا هست، ولی **پنهان** می‌ماند.
- ‏**`chrom[start - 1:end - 1]`**: این بار سر 5′ جابه‌جا می‌شود و همه‌ی کدون‌ها یک باز می‌لغزند:

<div dir="ltr">

```
isoB	parC	80	TCG	S	S	wild type
isoC	gyrA	83	CGG	R	S	MUTANT S83R
isoC	parC	84	AAG	K	E	MUTANT E84K
```

</div>

(سه سطر از دوازده.) کنترل منفی isoC چهار «جهش» دارد که نیستند، و جهش واقعی isoB (S80I) «وحشی» خوانده می‌شود: یک **منفی کاذب**. درس: یک خطای «منهای یک» گاهی همه‌چیز را خراب می‌کند و گاهی پنهان می‌ماند. پس همیشه کنترل منفی (isoC) و یک نمونه با پاسخ معلوم (isoA و isoB) را کنار داده‌ی خودتان اجرا کنید.

</details>

> 📺 **فیلم:** راهنمای نصب BLAST+ روی ویندوز (NCBI): https://www.ncbi.nlm.nih.gov/books/NBK52637/ (متن)
> 📄 **مرجع:** Camacho C, et al. (2009). *BLAST+: architecture and applications.* BMC Bioinformatics 10:421. https://doi.org/10.1186/1471-2105-10-421 · Cock PJA, et al. (2009). *Biopython.* Bioinformatics 25:1422–1423. https://doi.org/10.1093/bioinformatics/btp163

---

## ۵. گام ۴: ‏ResFinder در مرورگر (✍️)

**چرا؟** گام‌های ۲ و ۳ تنها آنچه را می‌دانستیم جستند. ‏**ResFinder** (مرکز اپیدمیولوژی ژنومی، دانمارک) هر ژنوم را با **همه**‌ی ژن‌های اکتسابی پایگاهش و، با **PointFinder**، با جهش‌های شناخته‌شده‌ی هر گونه می‌سنجد. همان کار AMRFinderPlus، در مرورگر.

✍️ **گام‌ها (از راهنمای ResFinder):**
1. ‏https://genepi.food.dtu.dk/resfinder را باز کنید.
2. نوع ورودی را ژنوم اسمبل‌شده (contigها) بگذارید و فایل `genomes\isoA.fna` را بارگذاری کنید.
3. گزینه‌های **Acquired antimicrobial resistance genes** و **Chromosomal point mutations** را بزنید؛ گونه: **Escherichia coli**.
4. آستانه‌های یکسانی و طول را ببینید و یادداشت کنید (نمونه‌ی README رسمی: یکسانی ۸۰٪، طول ۶۰٪).
5. ‏**Submit**. چند دقیقه بعد جدول نتیجه می‌آید: نام ژن، درصد یکسانی، طول هم‌ترازی / طول ژن، جای روی contig، و **فنوتیپ پیش‌بینی‌شده** (کدام آنتی‌بیوتیک‌ها). در بخش PointFinder، جهش‌ها با نام ژن و تغییر اسید آمینه.
6. همین را برای isoB و isoC تکرار کنید.

**با پاسخ معلوم بسنجید** (این‌ها **انتظار** است، نه خروجی دیده‌شده):

| ایزوله | باید ببینید | نکته‌ی سنجیدنی |
| :--- | :--- | :--- |
| ‏isoA | ‏blaCTX-M-15 (۱۰۰٪)؛ gyrA S83L | فنوتیپ: سفالوسپورین‌ها و کینولون‌ها |
| ‏isoB | ‏blaNDM-1؛ parC S80I | ‏**tet(A)؟** پوشش ۵۰٪ است؛ اگر آستانه‌ی طول ۶۰٪ باشد، ResFinder آن را **گزارش نمی‌کند**، در حالی که AMRFinderPlus آن را `PARTIALX` گزارش کرد |
| ‏isoC | هیچ ژن اکتسابی و هیچ جهش | کنترل منفی |

‏tet(A) نمونه‌ی خوبی است که «یافت نشد» به **آستانه**‌ها بستگی دارد. آستانه‌ی طول را در گام ۴ به ۴۰٪ پایین بیاورید و دوباره بزنید: آیا tet(A) می‌آید؟

> 📺 **فیلم:** *ResFinder: Identify antimicrobial resistance gene in next-generation sequencing data* (Dr. Jyoti Bala، کوتاه): https://www.youtube.com/shorts/iUXBlrpWkcM
> 📄 **مرجع:** Bortolaia V, et al. (2020). *ResFinder 4.0 for predictions of phenotypes from genotypes.* J Antimicrob Chemother 75:3491–3500. https://doi.org/10.1093/jac/dkaa345 · راهنما: https://github.com/genomicepidemiology/resfinder

---

## ۶. گام ۵: ‏CARD RGI در مرورگر (✍️)

**چرا؟** درس ۲ (CARD و ABRicate) نشان می‌دهد ابزارها همیشه هم‌نظر نیستند. ‏**RGI** ابزار پایگاه **CARD** است و نسخه‌ی وب دارد.

✍️ **گام‌ها (از راهنمای CARD):**
1. ‏https://card.mcmaster.ca/analyze/rgi را باز کنید.
2. فایل `genomes\isoB.fna` را بارگذاری کنید (نوع داده: DNA، ژنوم یا contig).
3. سخت‌گیری را **Perfect and Strict hits only** بگذارید (پیش‌فرض)؛ گزینه‌ی Loose را تنها برای جست‌وجوی خویشاوندان دور بزنید (درس ۲).
4. ‏**Submit**. نتیجه جدولی است با هر ژن یا جهش، «Best Hit ARO» (شناسه‌ی پایگاه CARD)، درصد یکسانی و درصد طول.

**با پاسخ معلوم بسنجید (انتظار):** ‏blaNDM-1 و parC S80I برای isoB. ‏CARD ژن‌های **ذاتی** K-12 را هم گزارش می‌کند (پمپ‌های efflux مانند acrB، و ژن‌هایی که در K-12 هست)؛ این‌ها در **هر سه** ایزوله، حتی isoC، می‌آیند. پس برای «ژن اکتسابی تازه»، فهرست isoC را از isoA و isoB کم کنید. همان کار `Scope = core/plus` در درس ۱.

> 📺 **فیلم:** *Brian Alcock – The Comprehensive Antibiotic Resistance Database*: https://www.youtube.com/watch?v=XKWfUbiQW8Q
> 📄 **مرجع:** Alcock BP, et al. (2023). *CARD 2023: expanded curation, support for machine learning, and resistome prediction at the Comprehensive Antibiotic Resistance Database.* Nucleic Acids Res 51(D1):D690–D699. https://doi.org/10.1093/nar/gkac920

---

## ۷. سه اشتباه رایج (مسیر ویندوز)

1. ‏**«blastn شناخته نشد».** پس از نصب BLAST+، پنجره‌ی **تازه**ی PowerShell باز کنید؛ اگر باز هم نشد، پوشه‌ی `bin` آن باید در PATH باشد (راهنمای NCBI در گام ۳).
2. **کپی کردن دستورهای چندسطری لینوکس.** `\` پایان سطر در PowerShell کار نمی‌کند. دستورهای این درس یک‌سطری‌اند.
3. **اعتماد به «یافت نشد» در ابزار وب.** ‏tet(A) ناقص (۵۰٪) با یک آستانه می‌آید و با دیگری نه. همیشه آستانه‌ها را یادداشت کنید و نتیجه را با کنترل منفی (isoC) بسنجید.

---

## جمع‌بندی

| یافته | ‏BLAST+ و پایتون (ویندوز، اجرا شده) | ‏AMRFinderPlus (درس ۱، لینوکس) | ‏ResFinder و RGI (وب، ✍️) |
| :--- | :--- | :--- | :--- |
| ‏isoA ‏blaCTX-M-15 | ✅ ‏۱۰۰٪ | ✅ ‏ALLELEX | انتظار: ✅ |
| ‏isoA ‏gyrA S83L | ✅ ‏TCG→TTG | ✅ ‏POINTX | انتظار: ✅ |
| ‏isoB ‏blaNDM-1 | ✅ ‏۱۰۰٪ | ✅ ‏ALLELEX | انتظار: ✅ |
| ‏isoB ‏parC S80I | ✅ ‏AGC→ATC | ✅ ‏POINTX | انتظار: ✅ |
| ‏isoB ‏tet(A) نیمه | ✅ پوشش ۵۰٪ | ✅ ‏PARTIALX ‏۵۰٫۳۸٪ | بسته به آستانه‌ی طول |
| ‏isoC | هیچ | هیچ (core) | انتظار: هیچ اکتسابی |

اکنون اگر خواستید، [درس ۱](01_lesson_amrfinder.md) را بخوانید: همان نتیجه با یک دستور AMRFinderPlus، برای صدها ژنوم.

---

## منابع

- ‏Bortolaia V, et al. (2020). *ResFinder 4.0 for predictions of phenotypes from genotypes.* J Antimicrob Chemother 75:3491–3500. https://doi.org/10.1093/jac/dkaa345
- ‏Alcock BP, et al. (2023). *CARD 2023.* Nucleic Acids Res 51(D1):D690–D699. https://doi.org/10.1093/nar/gkac920
- ‏Camacho C, et al. (2009). *BLAST+: architecture and applications.* BMC Bioinformatics 10:421. https://doi.org/10.1186/1471-2105-10-421
- ‏Cock PJA, et al. (2009). *Biopython: freely available Python tools for computational molecular biology and bioinformatics.* Bioinformatics 25:1422–1423. https://doi.org/10.1093/bioinformatics/btp163
- کتاب، Coursera، edX و فیلم‌های بیشتر: بخش منابع [درس ۱](01_lesson_amrfinder.md) و [درس ۲](02_lesson_card_abricate.md).

<sub>گام‌های ۱ تا ۳ با همان کد (Python 3 و Biopython 1.87، BLAST+ 2.17.0) روی سرور لینوکسی دوره در 2026-10-27 اجرا شدند؛ روی ویندوز آزموده نشده‌اند. گام‌های ۴ و ۵ و نصب برنامه‌ها از راهنمای رسمی ResFinder، CARD، NCBI و python.org نوشته شده‌اند (✍️). نشانی‌های ResFinder، CARD و python.org در همان روز پاسخ دادند.</sub>

</div>
