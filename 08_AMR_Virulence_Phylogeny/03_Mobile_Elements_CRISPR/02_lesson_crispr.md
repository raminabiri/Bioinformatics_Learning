<div dir="rtl">

# درس ۲: ‏CRISPR-Cas؛ دفترچه‌ی خاطرات ایمنی باکتری

**بخش:** `08_AMR_Virulence_Phylogeny` · **ماژول:** `03_Mobile_Elements_CRISPR` · **پیش‌نیاز:** [درس ۱](01_lesson_plasmids_is.md)؛ GFF و `awk` از بخش‌های ۰۱ و ۰۲ · **زمان:** حدود ۴۰ دقیقه · **ابزار:** ‏awk، Python (`find_crispr.py`)؛ CRISPRCasFinder و MinCED از مستندات · **آخرین بازبینی:** 2026-10-24

> **وضعیت:** بخش‌های ۳ و ۴ ✅ اجرا شده‌اند (اسکریپت Python نزدیک به ۲ ثانیه و ۲۲ مگابایت). بخش ۵ (CRISPRCasFinder، MinCED) ✍️ از مستندات است.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. بگویید CRISPR-Cas چگونه یک سامانه‌ی ایمنی **سازگار** (adaptive) در باکتری است.
2. ژن‌های cas را در آنوتیشن K-12 پیدا کنید و نوع سامانه را بگویید.
3. آرایه‌ی CRISPR را از روی تکرار شناخته‌شده‌اش پیدا کنید و spacerها را بشمارید.
4. بگویید spacerها چه چیزی درباره‌ی گذشته‌ی باکتری می‌گویند و چرا برای تایپ سویه‌ها به کار می‌روند.

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

در درس ۱ دیدیم پلاسمیدها و فاژها ژن‌ها را میان باکتری‌ها جابه‌جا می‌کنند. ولی باکتری بی‌دفاع نیست. در سال ۲۰۰۷ پژوهشگران یک شرکت لبنیات (برای ماست و پنیر) دیدند سویه‌های *Streptococcus thermophilus* که در برابر یک فاژ زنده مانده بودند، یک تکه‌ی کوچک از DNA همان فاژ را در یک ناحیه‌ی تکراری ژنوم خود گذاشته بودند. **باکتری فاژ را «به خاطر سپرده» بود.** این ناحیه CRISPR بود. همان سامانه‌ای که بعدها ابزار ویرایش ژن شد، در اصل ایمنی باکتری است.

---

## ۲. مفهوم به زبان ساده

‏**CRISPR** (Clustered Regularly Interspaced Short Palindromic Repeats) یک **آرایه** است: یک توالی تکراری کوتاه (**repeat**، در *E. coli* ‏۲۹ باز) که میان هر دو تکرار، یک **spacer** (نزدیک به ۳۲ باز) نشسته است. هر spacer تکه‌ای از DNA یک فاژ یا پلاسمید است که روزی به باکتری حمله کرده.

<div dir="ltr">

```
leader ─ R ─ S1 ─ R ─ S2 ─ R ─ S3 ─ … ─ R        (R = repeat, S = spacer)
          ↑ spacerهای تازه این‌جا، کنار leader، افزوده می‌شوند
```

</div>

ژن‌های **cas** کنار آرایه، سه کار را انجام می‌دهند:

| گام | چه رخ می‌دهد | پروتئین‌ها در *E. coli* (نوع I-E) |
| :--- | :--- | :--- |
| ۱. سازگاری (adaptation) | تکه‌ای از DNA مهاجم به‌عنوان spacer تازه گذاشته می‌شود | ‏Cas1، Cas2 |
| ۲. ساخت crRNA | آرایه رونویسی و به RNAهای کوچک بریده می‌شود | ‏CasE (Cas6e) |
| ۳. تداخل (interference) | ‏crRNA مجموعه‌ی Cascade را به DNA همسان می‌برد و Cas3 آن را می‌برد | ‏CasA تا CasE (Cascade)، Cas3 |

**تشبیه:** آرایه‌ی CRISPR یک **آلبوم عکس پلیس** است: از هر مجرم پیشین (فاژ) یک عکس (spacer). عکس تازه همیشه در **صفحه‌ی نخست** چسبانده می‌شود؛ پس ترتیب spacerها تاریخچه است: نزدیک به leader = تازه، دور = کهنه.

**یک پیوند با مقاومت:** باکتری‌ای که CRISPR فعال دارد، پلاسمیدها را هم می‌تواند پس بزند. در برخی گونه‌ها (برای نمونه *Enterococcus faecalis*) دیده‌اند سویه‌های بسیار مقاوم در بسیاری از موارد CRISPR-Cas کاملی ندارند.

> 📺 **فیلم:** *How CRISPR Works in Nature* (PBS NOVA؛ این فیلم در YouTube نیست): https://www.pbs.org/wgbh/nova/video/how-crispr-works · *Bacterial Adaptive Immunity with CRISPR/Cas9*: https://www.youtube.com/watch?v=MbJ7Hnc2K3Q
> 📄 **مرجع:** Barrangou R, et al. (2007). *CRISPR provides acquired resistance against viruses in prokaryotes.* Science 315:1709–1712. https://doi.org/10.1126/science.1138140

---

## ۳. گام ۱: ژن‌های cas در K-12

آنوتیشن K-12 (بخش ۰۱) را با `awk` می‌جوییم: سطرهای نوع `gene` که نامشان با `cas` آغاز می‌شود.

<div dir="ltr">

```bash
awk -F'\t' '$3=="gene" && $9 ~ /Name=cas/ {match($9, /Name=[^;]+/); print $4, $5, $7, substr($9, RSTART+5, RLENGTH-5)}' $G/ecoli_k12.gff
```

</div>

| بخش | کار |
| :--- | :--- |
| ‏`$9 ~ /Name=cas/` | ستون ۹ (ویژگی‌ها) شامل `Name=cas` باشد |
| ‏`match($9, /Name=[^;]+/)` | جای `Name=…` تا نخستین `;` را پیدا می‌کند و در `RSTART` و `RLENGTH` نگه می‌دارد |
| ‏`substr($9, RSTART+5, RLENGTH-5)` | تنها نام را (بی پنج نویسه‌ی `Name=`) برمی‌دارد |

**خروجی واقعی:**

<div dir="ltr">

```
2878569 2878853 - cas2
2878855 2879772 - cas1
2879788 2880387 - casE
2880374 2881048 - casD
2881051 2882142 - casC
2882155 2882637 - casB
2882630 2884138 - casA
2884553 2887219 - cas3
```

</div>

**توضیح خروجی:** هشت ژن cas در یک ناحیه‌ی ۹ هزار بازی، همه روی رشته‌ی منفی. ‏`casA` تا `casE` همان مجموعه‌ی **Cascade**‌اند؛ آنوتیشن آن‌ها را «type I-E CRISPR system Cascade subunit» می‌نامد. پس K-12 یک سامانه‌ی **نوع I-E** دارد. چون ژن‌ها روی رشته‌ی منفی‌اند، ترتیب خواندنشان از مختصات بزرگ به کوچک است: `cas3` ← `casA` … ← `cas1` ← `cas2`. آرایه‌ی CRISPR باید درست پس از `cas2` بیاید، یعنی در مختصات **کوچک‌تر** از ۲٬۸۷۸٬۵۶۹.

---

## ۴. گام ۲: پیدا کردن آرایه و spacerها

تکرار CRISPR در *E. coli* نوع I-E یک توالی ۲۹ بازی شناخته‌شده است: `CGGTTTATCCCCGCTGGCGCGGGGAACTC`. اسکریپت `find_crispr.py` این تکرار را روی هر دو رشته با حداکثر چند ناهمسانی می‌جوید، تکرارهای نزدیک به هم (کمتر از ۱۰۰ باز فاصله) را یک آرایه می‌شمارد، و spacerهای میان آن‌ها را در قالب FASTA می‌نویسد.

<div dir="ltr">

```bash
python3 $P/03_Mobile_Elements_CRISPR/scripts/find_crispr.py \
    genomes/isoC.fna CGGTTTATCCCCGCTGGCGCGGGGAACTC 3 > k12_spacers.fna
grep -c ">" k12_spacers.fna
head -4 k12_spacers.fna
```

</div>

| بخش | کار |
| :--- | :--- |
| ‏`genomes/isoC.fna` | همان K-12 |
| ‏`CGG…CTC` | توالی تکرار |
| ‏`3` | حداکثر ۳ ناهمسانی؛ تکرارهای یک آرایه در بسیاری از موارد دقیقاً یکسان نیستند |
| ‏`> k12_spacers.fna` | ‏spacerها به خروجی استاندارد؛ خلاصه‌ی آرایه‌ها به stderr (روی صفحه) |

**خروجی واقعی:**

<div dir="ltr">

```
isoC_chromosome	array1	2877701-2878463	strand +	repeats 13 (exact 10)	spacers 12
isoC_chromosome	array2	2904013-2904407	strand +	repeats 7 (exact 0)	spacers 6
18
>isoC_chromosome_array1_spacer1 len=32
CAGCGTCAGGCGTGAAATCTCACCGTCGTTGC
>isoC_chromosome_array1_spacer2 len=32
TCGGTTCAGGCGTTGCAAACCTGGCTACCGGG
```

</div>

**توضیح خروجی:**

- ‏**array1** (‏۲٬۸۷۷٬۷۰۱ تا ۲٬۸۷۸٬۴۶۳): ‏۱۳ تکرار و **۱۲ spacer**. این آرایه درست پیش از `cas2` (۲٬۸۷۸٬۵۶۹) است، همان‌جایی که در گام ۱ پیش‌بینی کردیم. ‏۱۰ تکرار دقیقاً همسان‌اند و ۳ تا چند ناهمسانی دارند.
- ‏**array2** (‏۲٬۹۰۴٬۰۱۳): ‏۷ تکرار و **۶ spacer**، ولی **هیچ** تکراری دقیقاً همسان نیست. این آرایه‌ی دوم، تکرار کمی متفاوتی دارد و تنها با اجازه‌ی ۳ ناهمسانی پیدا شد (تمرین ۵).
- ‏spacerها ۳۲ یا ۳۳ بازند (`grep ">" k12_spacers.fna | grep -oE "len=[0-9]+" | sort | uniq -c`: ‏۱۶ تا ۳۲ باز و ۲ تا ۳۳ باز).

‏**spacerها از کجا آمده‌اند؟** هر spacer را می‌توان در BLAST وب (ماژول 00/03) در برابر پایگاه nt جست‌وجو کرد تا دید با کدام فاژ یا پلاسمید همسان است. بسیاری از spacerهای *E. coli* هیچ همسانی در پایگاه‌ها ندارند، چون بیشتر فاژهای طبیعت هنوز توالی‌یابی نشده‌اند. ما این جست‌وجو را اجرا نکرده‌ایم و نتیجه‌ای از آن نمی‌آوریم.

<details>
<summary>✋ امتحان کن: اگر همین اسکریپت را روی isoA اجرا کنید، چند spacer می‌یابید؟ چرا؟</summary>

دقیقاً همان ۱۸ spacer: کروموزوم isoA همان K-12 است (تنها یک جهش gyrA دارد که دور از CRISPR است) و contig `isoA_pA` تکرار CRISPR ندارد. در ایزوله‌های واقعی، دو سویه‌ی خویشاوند در بسیاری از موارد بیشتر spacerهای **کهنه** را با هم دارند و در spacerهای **تازه** (نزدیک leader) فرق می‌کنند.

</details>

### ‏CRISPR برای تایپ سویه‌ها

چون آرایه‌ها با هر برخورد تازه بلندتر می‌شوند و spacerهای کهنه گاهی از دست می‌روند، **ترکیب spacerها** میان سویه‌ها فرق می‌کند. این پایه‌ی روش‌هایی مانند **spoligotyping** در *Mycobacterium tuberculosis* و تایپ CRISPR در *Salmonella* است: سویه‌هایی با spacerهای یکسان در بسیاری از موارد خویشاوند نزدیک‌اند. این یک نگاه دیگر به پرسش ماژول ۰۴ است.

> 📺 **فیلم:** *How CRISPR Works in Nature* (PBS NOVA): https://www.pbs.org/wgbh/nova/video/how-crispr-works
> 📄 **مرجع:** Couvin D, et al. (2018). *CRISPRCasFinder, an update of CRISRFinder, includes a portable version, enhanced performance and integrates search for Cas proteins.* Nucleic Acids Research 46:W246–W251. https://doi.org/10.1093/nar/gky425

---

## ۵. ابزارهای عمومی CRISPR (از مستندات)

اسکریپت ما تنها **یک تکرار شناخته‌شده** را می‌جوید. برای ژنومی که تکرارش را نمی‌دانیم، ابزارها الگوی «تکرار–فاصله–تکرار» را بی دانستن توالی پیدا می‌کنند:

- ‏**CRISPRCasFinder** (Institut Pasteur / I2BC): آرایه‌ها را با **سطح اطمینان** ۱ تا ۴ گزارش می‌کند (۴ = مطمئن‌ترین) و ژن‌های cas را هم با مدل‌های پروتئینی می‌جوید و نوع سامانه را می‌دهد. نسخه‌ی وب: https://crisprcas.i2bc.paris-saclay.fr
- ‏**MinCED**: ابزار خط فرمانی سبک (برپایه‌ی CRT) که تنها آرایه‌ها را پیدا می‌کند:

<div dir="ltr">

```bash
conda create -n minced -c conda-forge -c bioconda minced
conda activate minced
minced genomes/isoC.fna isoC.crisprs isoC.crisprs.gff
```

</div>

**پیش‌بینی (اجرا نشده):** انتظار داریم MinCED دست‌کم array1 را در همان بازه بیابد. اینکه array2 را هم با تکرارهای ناهمسانش بیابد یا نه، به آستانه‌های آن بستگی دارد؛ خودتان بسنجید.

> 📺 **فیلم:** دوره‌ی DTU در Coursera (تایپ مولکولی باکتری‌ها): https://www.coursera.org/learn/wgs-bacteria
> 📄 **مرجع:** MinCED: https://github.com/ctSkennerton/minced · Bland C, et al. (2007). *CRISPR Recognition Tool (CRT): a tool for automatic detection of clustered regularly interspaced palindromic repeats.* BMC Bioinformatics 8:209. https://doi.org/10.1186/1471-2105-8-209

---

## ۶. سه اشتباه رایج

1. **جست‌وجوی دقیق (۰ ناهمسانی).** تکرارهای یک آرایه کمی با هم فرق دارند؛ با جست‌وجوی دقیق، بخشی از آرایه و گاهی کل یک آرایه گم می‌شود (تمرین ۵).
2. **یکی گرفتن «CRISPR دارد» با «ایمن است».** ‏CRISPR در K-12 در شرایط آزمایشگاهی کم بیان می‌شود. بودن آرایه، فعال بودن سامانه را نشان نمی‌دهد.
3. **انتظار همسانی برای هر spacer.** بیشتر spacerها در پایگاه‌ها همسانی ندارند؛ «همسانی پیدا نشد» به معنای خطا نیست.

---

## جمع‌بندی

- ‏CRISPR-Cas ایمنی سازگار باکتری است: سازگاری (Cas1/Cas2)، ساخت crRNA، تداخل (Cascade + Cas3).
- ‏K-12 یک سامانه‌ی نوع I-E دارد: هشت ژن cas (۲٬۸۷۸٬۵۶۹ تا ۲٬۸۸۷٬۲۱۹) و آرایه‌ای با ۱۲ spacer درست کنار آن، و آرایه‌ی دومی با ۶ spacer.
- ترتیب spacerها تاریخچه است: نزدیک leader = تازه.
- ترکیب spacerها برای تایپ برخی گونه‌ها به کار می‌رود.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
awk -F'\t' '$3=="gene" && $9 ~ /Name=cas/ {match($9, /Name=[^;]+/); print $4, $5, $7, substr($9, RSTART+5, RLENGTH-5)}' GENOME.gff
python3 find_crispr.py GENOME.fna REPEAT 3 > spacers.fna     # array summary on screen
minced GENOME.fna out.crisprs out.gff                          # documented, not run here
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏CRISPR | آرایه‌ی تکرارهای کوتاه با spacerهای میانشان |
| ‏repeat / spacer | توالی تکراری ثابت / تکه‌ی DNA مهاجم میان دو تکرار |
| ‏leader | توالی آغاز آرایه که spacerهای تازه کنارش افزوده می‌شوند |
| ‏cas | ژن‌های همراه CRISPR |
| ‏Cascade | مجموعه‌ی پروتئینی CasA تا CasE در نوع I-E که crRNA را حمل می‌کند |
| ‏crRNA | ‏RNA کوچک ساخته‌شده از یک spacer که راهنمای برش است |
| ایمنی سازگار (adaptive immunity) | ایمنی‌ای که از برخورد پیشین «یاد می‌گیرد» |
| ‏spoligotyping | تایپ *M. tuberculosis* بر پایه‌ی بودن یا نبودن spacerهای معین |

---

## منابع

**مستند و مقاله**
- Barrangou R, et al. (2007). *CRISPR provides acquired resistance against viruses in prokaryotes.* Science 315:1709–1712. https://doi.org/10.1126/science.1138140
- Couvin D, et al. (2018). *CRISPRCasFinder…* Nucleic Acids Research 46:W246–W251. https://doi.org/10.1093/nar/gky425 · https://crisprcas.i2bc.paris-saclay.fr
- Bland C, et al. (2007). *CRISPR Recognition Tool (CRT)…* BMC Bioinformatics 8:209. https://doi.org/10.1186/1471-2105-8-209 · MinCED: https://github.com/ctSkennerton/minced

**کتاب**
- Barrangou R, van der Oost J (eds.) (2013). *CRISPR-Cas Systems: RNA-mediated Adaptive Immunity in Bacteria and Archaea*. Springer.

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Whole genome sequencing of bacterial genomes – tools and applications* (DTU): https://www.coursera.org/learn/wgs-bacteria
- ‏edX: دوره‌ای ویژه‌ی CRISPR باکتریایی در edX نیافتیم؛ نزدیک‌ترین: *Microbiology* (SNHU، MicroBachelors): https://www.edx.org/learn/microbiology/southern-new-hampshire-university-microbiology
- ویدئو: *How CRISPR Works in Nature* (PBS NOVA): https://www.pbs.org/wgbh/nova/video/how-crispr-works
- ‏YouTube: *Bacterial Adaptive Immunity with CRISPR/Cas9*: https://www.youtube.com/watch?v=MbJ7Hnc2K3Q (یافته در جست‌وجوی 2026-10-26؛ در وارسی پایان دوره سنجیده می‌شود)

<sub>تکرار ۲۹ بازی نوع I-E و مختصات ژن‌های cas از آنوتیشن RefSeq ‏K-12 (GCF_000005845.2) در 2026-10-24. نشانی‌ها در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
