<div dir="rtl">

# درس ۱: عامل‌های بیماری‌زایی و پیدا کردنشان با AMRFinderPlus

**بخش:** `08_AMR_Virulence_Phylogeny` · **ماژول:** `02_Virulence_Factors` · **پیش‌نیاز:** ماژول [۰۱](../01_AMR_Resistance_Genes/) (AMRFinderPlus و ستون‌هایش) · **زمان:** حدود ۴۵ دقیقه · **ابزار:** AMRFinderPlus 4.2.7 (با stxtyper درونی)، پایگاه 2026-08-07.1 · **آخرین بازبینی:** 2026-10-24

> ✅ **وضعیت: اجرا شده.** همه‌ی خروجی‌ها واقعی‌اند (2026-10-24). هر اجرای `amrfinder` نزدیک به ۸۰ ثانیه و ۱۸۳ مگابایت حافظه.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. عامل‌های بیماری‌زایی را در چند گروه کارکردی بشناسید (چسبیدن، سم، آهن‌گیری، فرار از ایمنی، سامانه‌ی ترشحی).
2. پاتوتیپ‌های *E. coli* را با ژن‌های نشانگرشان پیوند دهید (STEC، EPEC، ExPEC).
3. ‏AMRFinderPlus را برای ژن‌های بیماری‌زایی به کار ببرید و بدانید چرا `--plus` لازم است.
4. خروجی stxtyper (نوع ژن شیگاتوکسین) را بخوانید.
5. فرق «بودن ژن» و «بیماری‌زا بودن سویه» را توضیح دهید.

**پیش از آغاز:** محیط و پوشه‌ی ماژول ۰۱:

<div dir="ltr">

```bash
conda activate amr
cd ~/amr
G=~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data
P=~/Bioinformatics_Learning-main/08_AMR_Virulence_Phylogeny/99_scripts_data
```

</div>

---

## ۱. داستان

در یک مهدکودک، سه کودک با اسهال خونی بستری شده‌اند و حال یکی از آن‌ها رو به نارسایی کلیه می‌رود (سندرم همولیتیک-اورمیک، HUS). آزمایشگاه از مدفوع *E. coli* جدا کرده است. ولی *E. coli* در روده‌ی هر انسانی هست. پرسش این است: **آیا این *E. coli* همان سویه‌ی معمولی روده است، یا سویه‌ای که سم شیگا (Shiga toxin) می‌سازد؟** پاسخ در چند ژن است. در همان هفته، از ادرار یک بیمار سالمند هم *E. coli* جدا شده که به سفتریاکسون مقاوم است. آیا این دو سویه شبیه هم‌اند؟

---

## ۲. مفهوم به زبان ساده

### ۲.۱ عامل بیماری‌زایی یعنی چه؟

**عامل بیماری‌زایی** (virulence factor) هر مولکولی است که به باکتری کمک می‌کند در میزبان جا بگیرد، بماند و آسیب بزند. بیشتر آن‌ها در چند گروه جا می‌گیرند:

| گروه | کار | نمونه در *E. coli* |
| :--- | :--- | :--- |
| چسبیدن (adherence) | چنگ زدن به سلول میزبان | ‏`papC` (فیمبریه‌ی P در عفونت ادراری)، `eae` (اینتیمین) |
| سم (toxin) | آسیب مستقیم به سلول | ‏`stxA2`/`stxB2` (سم شیگا)، `cnf1`، `sat` |
| آهن‌گیری (iron uptake) | ربودن آهن از میزبان | ‏`iutA` (گیرنده‌ی آئروباکتین) |
| همولیزین | شکافتن گلبول قرمز | ‏`ehxA` (انتروهمولیزین) |
| سامانه‌ی ترشحی (secretion system) | تزریق پروتئین به سلول میزبان | سامانه‌ی ترشحی نوع ۳ در جزیره‌ی LEE |

**تشبیه:** یک دزد برای ورود به خانه به نردبان (چسبیدن)، دیلم (سم) و کیسه برای بردن (آهن‌گیری) نیاز دارد. داشتن نردبان به‌تنهایی کسی را دزد نمی‌کند؛ **ترکیب** ابزارهاست که خطر را می‌سازد.

### ۲.۲ پاتوتیپ‌های *E. coli*

بیشتر *E. coli*ها همزیست بی‌آزار روده‌اند. سویه‌های بیماری‌زا را با **ترکیب** ژن‌هایشان در **پاتوتیپ**‌ها دسته‌بندی می‌کنند:

| پاتوتیپ | بیماری | ژن‌های نشانگر |
| :--- | :--- | :--- |
| ‏STEC / EHEC (مانند O157:H7) | اسهال خونی، HUS | ‏`stx1` و/یا `stx2`؛ در EHEC همراه با `eae` و در بسیاری از موارد `ehxA` |
| ‏EPEC | اسهال کودکان | ‏`eae` **بی** `stx` |
| ‏ExPEC / UPEC | عفونت ادراری، سپسیس | ترکیبی از `pap`، `sfa/foc`، `iutA`، `sat`، `cnf1`، `hlyA`، `kpsM` |

نکته‌ی ژنومی: بسیاری از این ژن‌ها روی **عنصرهای متحرک**‌اند. ‏`stx2` روی یک **پروفاژ** است، `ehxA` روی **پلاسمید** pO157، و `eae` روی **جزیره‌ی بیماری‌زایی** LEE. این پیوند را در ماژول ۰۳ دنبال می‌کنیم.

> 📺 **فیلم:** *Bacterial virulence factors: an introduction*: https://www.youtube.com/watch?v=XBTkgu8peEY · پاتوتیپ‌های روده‌ای *E. coli*: *E.coli (Part-3)*: https://www.youtube.com/watch?v=jwU872g56eY
> 📄 **مرجع:** Kaper JB, Nataro JP, Mobley HLT (2004). *Pathogenic Escherichia coli.* Nature Reviews Microbiology 2:123–140. https://doi.org/10.1038/nrmicro818

### ۲.۳ داده‌ی این درس: دو ایزوله‌ی تازه با پاسخ معلوم

مانند ماژول ۰۱، روی کروموزوم K-12 چند contig با ژن‌های معلوم می‌گذاریم:

| ایزوله | contig | ژن | نماینده‌ی |
| :--- | :--- | :--- | :--- |
| ‏`isoD` (شبیه STEC) | ‏`isoD_island` | ‏`eae` (اینتیمین نوع گاما، نوع O157) | جزیره‌ی LEE |
| | ‏`isoD_phage` | اپرون `stx2a` فاژ 933W (`stxA2` + `stxB2`) | پروفاژ |
| | ‏`isoD_pO157` | ‏`ehxA` | پلاسمید pO157 |
| ‏`isoE` (شبیه ExPEC، مقاوم) | ‏`isoE_PAI` | ‏`papC`، `sat`، `cnf1` | جزیره‌ی بیماری‌زایی |
| | ‏`isoE_pE` | ‏`iutA` و `blaCTX-M-15` | پلاسمید |

توالی اپرون stx2a از رکورد **X07865.1** در NCBI (فاژ 933W، همان فاژ سویه‌ی O157:H7 ‏EDL933) برداشته شده است و بقیه از پایگاه AMRFinderPlus. همه در `99_scripts_data/data/virulence_genes.fna`‌اند. ‏`isoC` (همان K-12) کنترل منفی است.

---

## ۳. گام ۱: ساختن دو ژنوم

<div dir="ltr">

```bash
python3 $P/02_Virulence_Factors/scripts/make_virulence_isolates.py \
    $G/ecoli_k12.fna $P/data/virulence_genes.fna $P/data/acquired_genes.fna genomes
cat genomes/ground_truth_vir.tsv
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
Done: genomes
isolate	contig	gene	function
isoD	isoD_island	eae	intimin (attaching and effacing)
isoD	isoD_phage	stxA2+stxB2	Shiga toxin 2a
isoD	isoD_pO157	ehxA	enterohemolysin
isoE	isoE_PAI	papC	P fimbriae usher
isoE	isoE_PAI	sat	secreted autotransporter toxin
isoE	isoE_PAI	cnf1	cytotoxic necrotizing factor 1
isoE	isoE_pE	iutA	aerobactin receptor
isoE	isoE_pE	blaCTX-M-15	ESBL (resistance, module 01)
```

</div>

‏`genomes` همان پوشه‌ی ماژول ۰۱ است؛ حالا پنج ژنوم (`isoA` تا `isoE`) در آن هست.

---

## ۴. گام ۲: AMRFinderPlus روی isoD

**چرا AMRFinderPlus؟** پایگاه آن افزون بر مقاومت، ژن‌های بیماری‌زایی بازبینی‌شده را هم دارد (در گروه plus). همان دستور ماژول ۰۱ را می‌زنیم:

<div dir="ltr">

```bash
amrfinder -n genomes/isoD.fna --organism Escherichia --plus \
    --name isoD --threads 2 -o isoD.amr.tsv
awk -F'\t' '$10=="VIRULENCE"' isoD.amr.tsv | cut -f3,4,7,8,11,13,14,18 | column -t -s$'\t'
```

</div>

‏`$10=="VIRULENCE"`: ستون ۱۰ (Type) را برای ژن‌های بیماری‌زایی فیلتر می‌کند.

**خروجی واقعی:**

<div dir="ltr">

```
isoD_island  2001  eae           intimin type gamma           VIRULENCE  GAMMA   EXACTX    100.00
isoD_pO157   2001  ehxA          enterohemolysin EhxA         VIRULENCE  NA      EXACTX    100.00
isoD_phage   2001  stxA2         Shiga toxin Stx2 subunit A   VIRULENCE  stxA2   EXACTX    100.00
isoD_phage   2001  stx2a_operon  stx2a operon                 STX_TYPE   STX2A   COMPLETE  100.00
isoD_phage   2972  stxB2         Shiga toxin Stx2a subunit B  VIRULENCE  stxB2a  EXACTX    100.00
```

</div>

**توضیح خروجی** (ستون‌ها: contig، آغاز، نماد، نام، Subtype، Subclass، Method، همانندی):

- هر سه ژن افزوده با `EXACTX` و همانندی ۱۰۰٪ پیدا شدند. ‏Subclass برای `eae` نوع اینتیمین را می‌گوید: **GAMMA**، همان نوعی که در O157:H7 هست.
- سطر `stx2a_operon` از **stxtyper** است، ابزاری که AMRFinderPlus برای *Escherichia* خودکار اجرا می‌کند. ‏stxtyper دو زیرواحد A و B را با هم می‌سنجد و **زیرنوع** را می‌دهد: `STX2A`. ‏Method آن `COMPLETE` است، یعنی اپرون کامل و سالم است.
- چرا زیرنوع مهم است؟ زیرنوع‌های stx2 خطر یکسانی ندارند: stx2a بیشترین پیوند را با HUS دارد. پس `STX2A` + `eae` در گزارش یک **هشدار بالینی** است.
- ‏Stop ژن `stxA2` برابر ۲۹۵۷ است (بی کدون پایان؛ با آن ۲۹۶۰) و `stxB2` از ۲۹۷۲ آغاز می‌شود (ببینید: `cut -f4,5,7 isoD.amr.tsv | grep stx`). پس میان دو ژن تنها ۱۱ باز است؛ دو زیرواحد پشت سر هم در یک اپرون‌اند، همان‌طور که در رکورد X07865 (CDSهای 239..1198 و 1210..1479) آمده است.

> 📺 **فیلم:** سخنرانی Michael Feldgarden (NCBI) درباره‌ی پایگاه AMRFinderPlus، که ژن‌های بیماری‌زایی را هم در بر دارد: https://www.youtube.com/watch?v=tXQfHjdx0F8
> 📄 **مرجع:** stxtyper (NCBI): https://github.com/ncbi/stxtyper · معنای Type و Subtype، از جمله `STX_TYPE`: https://github.com/ncbi/amr/wiki/Interpreting-results

<details>
<summary>✋ امتحان کن: اگر در یک ایزوله <code>eae</code> باشد ولی هیچ سطر stx نباشد، به کدام پاتوتیپ فکر می‌کنید؟</summary>

‏**EPEC** (اینتیمین بی سم شیگا؛ جدول ۲.۲). ولی پیش از نتیجه‌گیری، ببینید ژن stx شاید روی لبه‌ی یک contig بریده شده باشد (`PARTIAL_CONTIG_ENDX`)؛ پروفاژها پر از تکرارند و اسمبلی short-read در بسیاری از موارد همان‌جا می‌شکند. فاژ stx هم گاهی هنگام کشت از سلول بیرون می‌افتد.

</details>

---

## ۵. گام ۳: isoE و نقش `--plus`

<div dir="ltr">

```bash
amrfinder -n genomes/isoE.fna --organism Escherichia --plus \
    --name isoE --threads 2 -o isoE.amr.tsv
awk -F'\t' '$10=="VIRULENCE" || $9=="core"' isoE.amr.tsv | cut -f3,4,7,9,10,13,14 | column -t -s$'\t'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
isoE_PAI  2001   papC         plus  VIRULENCE  NA             EXACTX
isoE_PAI  6012   sat          plus  VIRULENCE  NA             EXACTX
isoE_PAI  11400  cnf1         plus  VIRULENCE  NA             EXACTX
isoE_pE   2001   iutA         plus  VIRULENCE  NA             EXACTX
isoE_pE   5697   blaCTX-M-15  core  AMR        CEPHALOSPORIN  ALLELEX
```

</div>

**توضیح خروجی:** همه‌ی ۵ ژن افزوده پیدا شدند. به ستون ۴ نگاه کنید: **همه‌ی ژن‌های بیماری‌زایی `plus`‌اند.** پس اگر `--plus` را فراموش کنید، گزارش تنها `blaCTX-M-15` را نشان می‌دهد و همه‌ی ژن‌های بیماری‌زایی **بی‌صدا** گم می‌شوند (تمرین ۱).

**هم‌گرایی (convergence):** ‏isoE هم ژن‌های ExPEC را دارد و هم یک ESBL. چنین ترکیبی، یعنی بیماری‌زایی بالا همراه با مقاومت، در کلون پرخطر *E. coli* ST131 دیده می‌شود. در *Klebsiella pneumoniae* هم نمونه‌ی مشهور آن سویه‌های **hvKp مقاوم به کارباپنم** است (درس ۲).

<details>
<summary>✋ امتحان کن: چند سطر در isoC.amr.tsv (کنترل منفی، ماژول ۰۱) Type برابر VIRULENCE دارد؟ این درباره‌ی K-12 چه می‌گوید؟</summary>

<div dir="ltr">

```bash
awk -F'\t' '$10=="VIRULENCE"' isoC.amr.tsv | wc -l
```

</div>

**صفر.** پایگاه AMRFinderPlus تنها ژن‌های بیماری‌زایی **ویژه**ی سویه‌های بیماری‌زا را دارد، نه ژن‌های عمومی‌ای مانند فلاژل که همه‌ی *E. coli*ها دارند. در درس ۲ می‌بینید VFDB برای همین K-12 بیش از ۶۰ ژن گزارش می‌کند.

</details>

---

## ۶. «بودن ژن» در برابر «بیماری‌زا بودن»

ژنوم تنها یک **توانایی** را نشان می‌دهد. چند دلیل که بودن یک ژن، بیماری را تضمین نمی‌کند:

1. **ترکیب لازم است:** ‏`papC` به‌تنهایی سویه را UPEC نمی‌کند؛ پاتوتیپ با ترکیبی از ژن‌ها تعریف می‌شود.
2. **بیان:** ژن‌های بیماری‌زایی تنظیم سختی دارند؛ ژنی که بیان نشود کاری نمی‌کند.
3. **میزبان:** یک سویه در یک بیمار با سیستم ایمنی ضعیف بیماری‌زاست و در فرد سالم نه.
4. **ژن ناقص:** مانند `tet(A)` ماژول ۰۱، یک ژن بریده شاید کار نکند.

پس در گزارش بنویسید «ژن‌های X و Y، **نشانگر** پاتوتیپ STEC، پیدا شد»، نه «این سویه بیماری‌زاست».

> 📺 **فیلم:** *Virulence Factors of Bacteria: Comprehensive Guide to Bacterial Pathogenicity*: https://www.youtube.com/watch?v=-jeC7hdp57Y
> 📄 **مرجع:** Feldgarden M, et al. (2021). *AMRFinderPlus and the Reference Gene Catalog…* Scientific Reports 11:12728. https://doi.org/10.1038/s41598-021-91456-0

---

## ۷. سه اشتباه رایج

1. **فراموش کردن `--plus`.** همه‌ی ژن‌های بیماری‌زایی AMRFinderPlus در گروه plus‌اند و بی این گزینه دیده نمی‌شوند.
2. **پاتوتیپ از یک ژن.** همیشه ترکیب را ببینید (`eae` به‌تنهایی EPEC است، با `stx` EHEC).
3. **نادیده گرفتن زیرنوع stx.** «stx مثبت» بس نیست؛ stx2a و stx2d بیشترین پیوند را با بیماری سخت دارند. سطر stxtyper را بخوانید.

---

## 📘 برای کنجکاوها

- ‏stxtyper جدا هم نصب و اجرا می‌شود (`stxtyper -n assembly.fna`) و برای زیرنوع‌های stx1 و stx2 ‏Method‌هایی مانند `COMPLETE`، `PARTIAL` و `FRAMESHIFT` دارد.
- برای سروتایپ (O و H) *E. coli*، ابزارهایی مانند ECTyper و پایگاه `ecoh` در ABRicate هست. ‏O157:H7 یک سروتایپ است؛ پاتوتیپ را ژن‌ها تعیین می‌کنند.

---

## جمع‌بندی

- عامل‌های بیماری‌زایی در گروه‌های چسبیدن، سم، آهن‌گیری، همولیزین و سامانه‌ی ترشحی‌اند؛ بسیاری روی فاژ، پلاسمید یا جزیره‌ی ژنومی.
- ‏AMRFinderPlus با `--organism Escherichia --plus` ژن‌های بیماری‌زایی ویژه و زیرنوع stx را گزارش می‌کند.
- روی دو ژنوم شبیه‌سازی‌شده، همه‌ی ۷ ژن بیماری‌زایی و یک ژن مقاومت درست پیدا شدند و stxtyper اپرون را `STX2A COMPLETE` خواند.
- بودن ژن، نشانگر است، نه اثبات بیماری‌زایی.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
amrfinder -n ASM.fna --organism Escherichia --plus --name ID -o ID.amr.tsv
awk -F'\t' '$10=="VIRULENCE"' ID.amr.tsv             # virulence lines
awk -F'\t' '$11=="STX_TYPE"' ID.amr.tsv              # stxtyper result
awk -F'\t' '$10=="VIRULENCE" || $9=="core"' ID.amr.tsv
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| عامل بیماری‌زایی (virulence factor) | مولکولی که به جا گرفتن، ماندن یا آسیب زدن باکتری در میزبان کمک می‌کند |
| پاتوتیپ (pathotype) | گروهی از سویه‌ها با یک ترکیب ژنی و یک بیماری معین |
| ‏STEC / EHEC | ‏*E. coli* سازنده‌ی سم شیگا / زیرگروه آن با `eae` که اسهال خونی و HUS می‌دهد |
| ‏EPEC | ‏*E. coli* با `eae` بی سم شیگا |
| ‏ExPEC / UPEC | ‏*E. coli* بیرون‌روده‌ای / ادراری |
| ‏HUS | سندرم همولیتیک-اورمیک؛ نارسایی کلیه پس از عفونت STEC |
| اینتیمین (intimin) | پروتئین `eae` برای چسبیدن تنگاتنگ به سلول روده |
| ‏LEE | جزیره‌ی بیماری‌زایی «locus of enterocyte effacement» |
| پروفاژ (prophage) | ژنوم فاژی که درون کروموزوم باکتری جا گرفته |
| ‏stxtyper | ابزار NCBI برای تعیین زیرنوع ژن‌های سم شیگا |
| هم‌گرایی (convergence) | بودن هم‌زمان ژن‌های بیماری‌زایی و مقاومت در یک سویه |

---

## منابع

**مستند و مقاله**
- Kaper JB, Nataro JP, Mobley HLT (2004). *Pathogenic Escherichia coli.* Nature Reviews Microbiology 2:123–140. https://doi.org/10.1038/nrmicro818
- Feldgarden M, et al. (2021). *AMRFinderPlus and the Reference Gene Catalog facilitate examination of the genomic links among antimicrobial resistance, stress response, and virulence.* Scientific Reports 11:12728. https://doi.org/10.1038/s41598-021-91456-0
- stxtyper: https://github.com/ncbi/stxtyper · AMRFinderPlus Interpreting results: https://github.com/ncbi/amr/wiki/Interpreting-results
- NCBI nuccore X07865.1 (phage 933W stx2 operon): https://www.ncbi.nlm.nih.gov/nuccore/X07865.1

**کتاب**
- Wilson BA, Winkler ME, Ho BT (2019). *Bacterial Pathogenesis: A Molecular Approach*, 4th ed. ASM Press.

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Whole genome sequencing of bacterial genomes – tools and applications* (DTU؛ شناسایی ژن‌های بیماری‌زایی و تایپینگ): https://www.coursera.org/learn/wgs-bacteria
- ‏edX: دوره‌ای ویژه‌ی ژنومیکس بیماری‌زایی در edX نیافتیم؛ نزدیک‌ترین: *Microbiology* (Southern New Hampshire University، برنامه‌ی MicroBachelors): https://www.edx.org/learn/microbiology/southern-new-hampshire-university-microbiology
- ‏YouTube: *Bacterial virulence factors: an introduction*: https://www.youtube.com/watch?v=XBTkgu8peEY
- ‏YouTube: *E.coli (Part-3)* (پاتوتیپ‌های روده‌ای): https://www.youtube.com/watch?v=jwU872g56eY
- ‏YouTube: *Virulence Factors of Bacteria: Comprehensive Guide to Bacterial Pathogenicity*: https://www.youtube.com/watch?v=-jeC7hdp57Y
- ‏YouTube: سخنرانی Michael Feldgarden (NCBI): https://www.youtube.com/watch?v=tXQfHjdx0F8

<sub>اپرون stx2a در 2026-10-24 از NCBI efetch (X07865.1، بازهای 239 تا 1479) گرفته شد. نشانی‌های فیلم از جست‌وجوی وب در 2026-10-24‌اند؛ در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
