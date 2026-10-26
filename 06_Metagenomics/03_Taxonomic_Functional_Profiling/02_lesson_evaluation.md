<div dir="rtl">

# درس ۲: پروفایل چقدر درست است؟ سنجیدن با پاسخ معلوم

**بخش:** `06_Metagenomics` · **ماژول:** `03_Taxonomic_Functional_Profiling` · **پیش‌نیاز:** [درس ۱](01_lesson_kraken.md) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** Kraken2 2.17.1، Bracken 3.0.1، Python 3 · **خروجی‌ها از اجرای:** 2026-10-13

> ⚠️ همه‌ی عددهای این درس از **پایگاه داده‌ی تمرینی** (۴۵ ژنوم) است و درباره‌ی **رفتار** ابزار است، نه درباره‌ی دقت Kraken2 با پایگاه کامل.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. یک پروفایل را با ترکیب واقعی بسنجید: درستی (*precision*)، بازیابی (*recall*) و فاصله‌ی Bray–Curtis.
2. اثر `--confidence` و آستانه‌ی فراوانی را آزمایش کنید و انتخابتان را با عدد توجیه کنید.
3. سه محدودیت بنیادی را بشناسید: گونه‌ی غایب از پایگاه، گروه‌های گونه‌ای بسیار نزدیک، و فراوانی رید در برابر سلول.
4. بدانید پروفایل **عملکردی** (HUMAnN) چه می‌دهد و MetaPhlAn چه فرقی با Kraken2 دارد.

**پیش از آغاز:** در `~/meta`، با متغیر `S` درس ۱ (`S=…/99_scripts_data/03_Taxonomic_Functional_Profiling/scripts`) و خروجی‌های `profile/` آن.

---

## ۱. داستان

درس ۱ برای نمونه‌ای دوگونه‌ای، ۹ گونه گزارش داد و فراوانی *E. coli* را ۲۷٪ گفت (درست: ۴۲٪). در یک نمونه‌ی واقعی، پاسخ درست را **نمی‌دانید**؛ پس نمی‌فهمید کدام عدد ساختگی است. تنها راه: ابزار و پارامترها را **روی داده‌ای با پاسخ معلوم** بسنجید (*mock community* یا داده‌ی شبیه‌سازی‌شده)، و سپس با همان تنظیم روی داده‌ی واقعی کار کنید. این درس همین کار را می‌کند.

---

## ۲. مفهوم: سه عدد برای سنجیدن یک پروفایل

| | در نمونه هست | در نمونه نیست |
| :--- | :---: | :---: |
| **ابزار گزارش کرد** | ‏TP (درست مثبت) | ‏FP (مثبت ساختگی) |
| **ابزار گزارش نکرد** | ‏FN (منفی ساختگی) | — |

- **درستی** = TP / (TP + FP): «از آنچه گزارش شد، چند تا واقعی بود؟»
- **بازیابی** = TP / (TP + FN): «از آنچه واقعاً بود، چند تا پیدا شد؟»
- ‏**‏Bray–Curtis** (بخش ۰۴، vegan): فاصله‌ی دو ترکیب، از ۰ (یکسان) تا ۱ (هیچ گونه‌ی مشترک). برای فراوانی‌های نسبی = نیم جمع قدرمطلق تفاوت‌ها.

نمونه با دست، برای `minigut` (درس ۱): ۹ گونه گزارش شد که ۲ تا واقعی‌اند.
- درستی = 2 / 9 = **0.222**؛ بازیابی = 2 / 2 = **1.000**.
- ‏Bray–Curtis: ‏*B. fragilis* |57.83 − 54.06| = 3.77؛ *E. coli* |42.17 − 27.25| = 14.92؛ هفت گونه‌ی ساختگی روی هم 18.69. نیم جمع: (3.77 + 14.92 + 18.69) / 2 = **18.69٪ = 0.187**.

---

## ۳. گام ۱: اسکریپت سنجش

اسکریپت آماده‌ی [`evaluate_profile.py`](../99_scripts_data/03_Taxonomic_Functional_Profiling/scripts/evaluate_profile.py) همین حساب را برای هر خروجی Bracken می‌کند:

<div dir="ltr">

```bash
python3 $S/evaluate_profile.py profile/bracken/minigut_c0.bracken minigut
```

</div>

<div dir="ltr">

```text
species                                  truth  estimate  status
Bacteroides fragilis                    57.83%    54.06%  TP
Escherichia coli                        42.17%    27.25%  TP
Shigella sonnei                          0.00%     8.10%  FP
Shigella flexneri                        0.00%     5.53%  FP
Phocaeicola dorei                        0.00%     3.21%  FP
Escherichia fergusonii                   0.00%     1.68%  FP
Klebsiella pneumoniae                    0.00%     0.08%  FP
Salmonella enterica                      0.00%     0.06%  FP
Bacteroides thetaiotaomicron             0.00%     0.03%  FP

species predicted=9  TP=2  FP=7  FN=0
precision=0.222  recall=1.000  F1=0.364  Bray-Curtis=0.187
```

</div>

- ورودی‌ها: فایل `.bracken` و نام نمونه؛ پاسخ درست از `ground_truth_species.tsv` (که در آغاز درس ۱ کپی کردید) خوانده می‌شود.
- اسکریپت گونه‌ها را با **taxid** جفت می‌کند، نه با نام، تا تفاوت نوشتار نام‌ها (بخش ۰۴) دردسر نشود.
- ‏F1 میانگین هم‌ساز درستی و بازیابی است: یک عدد برای هر دو.
- همان عددهای حساب دستی بخش ۲. ✓

خروجی را در فایل‌هایی بنویسید تا با هم بسنجید؛ `tail -n 1` تنها خط آخر را می‌دهد.

---

## ۴. گام ۲: ‏`--confidence`

‏`--confidence c` در Kraken2 می‌گوید: رید را تنها وقتی به یک تاکسون بده که دست‌کم سهم `c` از k-merهای رید آن تاکسون (یا زیرشاخه‌هایش) را پشتیبانی کنند؛ وگرنه رید را به سطح بالاتر ببر. پیش‌فرض ۰ است: کمترین سخت‌گیری.

<div dir="ltr">

```bash
CONF=0.1 bash $S/run_profile.sh
for s in minigut minigut_sample2; do
  for c in 0 0.1; do
    printf "%s c=%s  " $s $c
    python3 $S/evaluate_profile.py profile/bracken/${s}_c$c.bracken $s | tail -n 1
  done
done
```

</div>

‏`CONF=0.1 bash …`: متغیر را تنها برای همین اجرا به اسکریپت می‌دهد (ماژول ۰۲، بخش ۹). خروجی‌ها روی هم:

| نمونه | `--confidence` | گونه‌ی گزارش‌شده | TP | FP | FN | درستی | بازیابی | Bray–Curtis |
| :--- | :-: | -: | -: | -: | -: | :-: | :-: | :-: |
| minigut | 0 | 9 | 2 | 7 | 0 | 0.222 | 1.000 | 0.187 |
| minigut | 0.1 | 6 | 2 | 4 | 0 | 0.333 | 1.000 | 0.156 |
| minigut_sample2 | 0 | 28 | 20 | 8 | 1 | 0.714 | 0.952 | 0.099 |
| minigut_sample2 | 0.1 | 27 | 20 | 7 | 1 | 0.741 | 0.952 | 0.092 |

- ‏**بازیابی بالا، درستی پایین:** الگوی همیشگی Kraken2. هر چه هست را می‌یابد، و چیزهایی را هم که نیست.
- ‏**`--confidence 0.1`** هم مثبت‌های ساختگی و هم خطای فراوانی را کم کرد، بی آنکه گونه‌ی واقعی‌ای از دست برود.
- بهترین مقدار به **پایگاه و جامعه** وابسته است؛ تمرین ۳ پنج مقدار را می‌آزماید.

> 📺 **فیلم:** *GTN Tutorial: Taxonomic Profiling and Visualization of Metagenomic Data*: https://www.youtube.com/watch?v=jszMnBKm6ig (Galaxy Project)
> 📄 **مرجع:** Lu J, et al. (2022). *Metagenome analysis using the Kraken software suite.* Nature Protocols 17:2815–2839.

---

## ۵. گام ۳: تنها منفی ساختگی، و ریدهای طبقه‌بندی‌نشده

در `minigut_sample2` تنها یک FN هست: ***Candida albicans***، که عمداً در پایگاه نیست.

<div dir="ltr">

```bash
python3 $S/evaluate_profile.py profile/bracken/minigut_sample2_c0.bracken minigut_sample2 | grep FN
```

</div>

<div dir="ltr">

```text
Candida albicans                         3.50%     0.00%  FN
species predicted=28  TP=20  FP=8  FN=1
```

</div>

‏(خط دوم هم `FN` را دارد، پس `grep` آن را هم چاپ کرد.)

**ابزار نمی‌گوید چه چیزی را نمی‌شناسد.** ریدهای *Candida* بی‌صدا در «طبقه‌بندی‌نشده» (۱۴٫۵٪) رفتند؛ هیچ هشداری نیامد. «۱۴٫۵٪ طبقه‌بندی‌نشده» یک پرسش است، نه یک عدد برای نادیده گرفتن: **چه چیزی در این ریدهاست؟** (تمرین ۲: بیشترشان اصلاً از *Candida* نیستند.)

---

## ۶. گام ۴: آستانه‌ی فراوانی، شمشیر دولبه

پالایش رایج «گونه‌های زیر ۱٪ را کنار بگذار» را بیازمایید (گزینه‌ی `--min-frac` اسکریپت):

<div dir="ltr">

```bash
python3 $S/evaluate_profile.py profile/bracken/minigut_sample2_c0.bracken minigut_sample2 --min-frac 0.01 | tail -n 2
```

</div>

<div dir="ltr">

```text
species predicted=13  TP=12  FP=1  FN=9
precision=0.923  recall=0.571  F1=0.706  Bray-Curtis=0.111
```

</div>

درستی از ۰٫۷۱ به ۰٫۹۲ رسید، ولی **بازیابی از ۰٫۹۵ به ۰٫۵۷ افتاد**: ۹ گونه‌ی واقعی با فراوانی زیر ۱٪ کنار رفتند. در جامعه‌ای واقعی با دنباله‌ی بلند گونه‌های کم‌فراوان، چنین آستانه‌ای بخش بزرگی از تنوع را پاک می‌کند (و شاخص‌های تنوع بخش ۰۴ را عوض می‌کند). **آستانه را با هدف تحلیل برگزینید و گزارشش کنید.**

---

## ۷. سه محدودیت بنیادی

**۱. گروه‌های بسیار نزدیک.** *E. coli/Shigella*، *A. baumannii/pittii*، *Bacillus cereus/anthracis/thuringiensis*: ریدهای کوتاه آن‌ها را جدا نمی‌کنند. در `minigut`، ۱۵ واحد درصد *E. coli* به *Shigella* و *E. fergusonii* رفت. اگر گزارش را در سطح «گروه *Escherichia/Shigella*» بدهید، این خطا کمابیش ناپدید می‌شود (تمرین ۴). **برگزیدن سطح گزارش، یک تصمیم علمی است.**

**۲. «درصد رید» برابر «درصد سلول» نیست.** ژنوم بزرگ‌تر، رید بیشتری می‌دهد. Kraken2/Bracken سهم **رید** را برآورد می‌کنند (تمرین ۵).

**۳. پایگاه، سقف دانش ابزار است.** گونه‌ی غایب (*Candida*) دیده نمی‌شود؛ سویه‌ی دیگر (همه‌ی ۲۱ گونه‌ی این پایگاه) بخشی از ریدها را بی‌برچسب می‌گذارد یا به خویشاوند می‌دهد.

---

## ۸. پروفایل عملکردی و MetaPhlAn (معرفی؛ در این دوره اجرا نمی‌شود)

> **این بخش اجرا نشده است.** پایگاه‌های لازم ده‌ها گیگابایت‌اند. دستورها از مستندات رسمی‌اند؛ خروجی‌ای نشان داده نمی‌شود.

### ‏MetaPhlAn 4: رویکرد ژن نشانگر

| | ‏**Kraken2** (k-mer) | ‏**MetaPhlAn 4** (ژن نشانگر) |
| :--- | :--- | :--- |
| منطق | هر k-mer رید در پایگاه همه‌ی ژنوم‌ها جست‌وجو می‌شود | ریدها روی کمابیش ۵ میلیون **ژن نشانگر** ویژه‌ی هر شاخه هم‌تراز می‌شوند |
| خروجی | شمار رید برای هر تاکسون | فراوانی نسبی، نزدیک‌تر به **سهم سلول** |
| ریدهای طبقه‌بندی‌شده | بیشتر ریدها | تنها ریدهای روی نشانگرها (درصد کم، و طبیعی) |
| ضعف | مثبت ساختگی بسیار بی پالایش | گونه‌ی بی‌نشانگر دیده نمی‌شود |

<div dir="ltr">

```bash
metaphlan clean_R1.fastq.gz,clean_R2.fastq.gz --input_type fastq --nproc 8 -o sample_profile.txt
```

</div>

(نام برخی گزینه‌ها میان نسخه‌های 4.0 و 4.1 عوض شده است؛ `metaphlan --help` نسخه‌ی خودتان را ببینید.)

### ‏HUMAnN 3: «چه می‌کنند؟»

‏HUMAnN ریدها را نخست روی پن‌ژنوم گونه‌هایی که MetaPhlAn یافته هم‌تراز می‌کند (ChocoPhlAn)؛ ریدهای مانده را با جست‌وجوی ترجمه‌شده روی پروتئین‌های UniRef90 می‌سنجد. خروجی‌ها:
- ‏`genefamilies.tsv`: فراوانی خانواده‌های ژنی UniRef90؛ با `humann_regroup_table` به KO یا EC تبدیل می‌شود.
- ‏`pathabundance.tsv`: فراوانی مسیرهای MetaCyc، **به تفکیک گونه**.

**پیوند با بخش ۰۰:** برخی ژن‌ها (مانند gyrA) در هیچ مسیر متابولیکی نیستند؛ پروفایل «تنها مسیر» آن‌ها را نمی‌بیند. برای ژن‌های مقاومت، پایگاه ویژه (CARD، بخش ۰۸) لازم است.

> 📺 **فیلم:** *Introduction to Shotgun Metagenomic Data Analysis with bioBakery*: https://www.youtube.com/watch?v=T4sviwz9DCk (N. Segata) · *Taxonomic, functional, and strain-level profiling with bioBakery 3*: https://www.youtube.com/watch?v=t2KkNtE80ro
> 📄 **مرجع:** Beghini F, et al. (2021). *Integrating taxonomic, functional, and strain-level profiling of diverse microbial communities with bioBakery 3.* eLife 10:e65088. https://doi.org/10.7554/eLife.65088

---

## ۹. سه اشتباه رایج

‏**۱. ‏`--confidence 0` بی هیچ پالایشی.** روی این داده ۷ گونه‌ی ساختگی در برابر ۲ واقعی. یک confidence آزموده و/یا کمترین شمار رید را به‌کار ببرید و گزارش کنید.

**۲. آستانه‌ی فراوانی دلخواه (۱٪).** بازیابی ۰٫۹۵ ← ۰٫۵۷. آستانه را با هدف برگزینید، و تنوع را **پیش از** آن حساب کنید.

**۳. سنجیدن پروفایل دو ابزار یا دو پایگاه با هم.** تاکسونومی و تعریف فراوانی‌شان فرق دارد. در یک پژوهش، روش را ثابت نگه دارید.

---

## 📘 برای کنجکاوها

- ‏**‏CAMI:** چالش‌های CAMI ابزارهای پروفایل را روی داده‌ی شبیه‌سازی‌شده‌ی بزرگ می‌سنجند؛ نتیجه‌ی CAMI II (۲۰۲۲) نشان داد هیچ ابزاری در همه‌ی سنجه‌ها برتر نیست.
- **داده‌ی ترکیبی (*compositional*):** فراوانی نسبی جمعش ۱ است؛ اگر یک گونه بالا رود، بقیه «پایین» می‌آیند حتی اگر شمار سلولشان عوض نشده باشد. روش‌هایی مانند تبدیل CLR برای همین ساخته شده‌اند.
- ‏**‏Krona:** ‏`kreport2krona.py` (KrakenTools) و `ktImportText` یک نمودار دایره‌ای تعاملی از `.kreport` می‌سازند.

---

## جمع‌بندی

- درستی، بازیابی و Bray–Curtis سه نگاه گوناگون به یک پروفایل‌اند؛ با پاسخ معلوم هر سه سنجیدنی‌اند.
- ‏Kraken2: بازیابی بالا، درستی پایین؛ `--confidence 0.1` روی این پایگاه هر دو سنجه‌ی خطا را بهتر کرد.
- آستانه‌ی ۱٪ درستی را بالا برد ولی ۹ گونه‌ی واقعی را پاک کرد.
- گونه‌ی غایب از پایگاه بی‌صدا «طبقه‌بندی‌نشده» می‌ماند؛ گروه‌های بسیار نزدیک را در سطح گروه گزارش کنید.
- **این‌همه با پایگاه تمرینی بود؛ برای کار واقعی، پایگاه کامل (Standard یا PlusPF) و کالیبره کردن دوباره لازم است.**

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
python3 $S/evaluate_profile.py profile/bracken/S_c0.bracken S                      # truth vs estimate
python3 $S/evaluate_profile.py profile/bracken/S_c0.bracken S --min-frac 0.01     # with a 1% filter
CONF=0.1 bash $S/run_profile.sh                                                   # Kraken2 --confidence 0.1
bracken -d DB -i S.kreport -o S.genus.bracken -r 125 -l G -t 10                   # genus level
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| درستی (*precision*) | سهم گونه‌های گزارش‌شده که واقعاً هستند |
| بازیابی (*recall*) | سهم گونه‌های واقعی که گزارش شدند |
| ‏F1 | میانگین هم‌ساز درستی و بازیابی |
| ‏mock community | جامعه‌ی ساختگی با ترکیب معلوم، برای سنجیدن روش |
| گروه گونه‌ای (*species complex*) | چند گونه‌ی بسیار نزدیک که با ریدهای کوتاه جدا نمی‌شوند |
| پروفایل عملکردی | فراوانی ژن‌ها و مسیرهای متابولیکی نمونه |

---

## منابع

**مستند و مقاله**
- Lu J, et al. (2022). *Metagenome analysis using the Kraken software suite.* Nature Protocols 17:2815–2839. https://doi.org/10.1038/s41596-022-00738-y
- Meyer F, et al. (2022). *Critical Assessment of Metagenome Interpretation: the second round of challenges.* Nature Methods 19:429–440. https://doi.org/10.1038/s41592-022-01431-4
- Blanco-Míguez A, et al. (2023). *Extending and improving metagenomic taxonomic profiling with uncharacterized species using MetaPhlAn 4.* Nature Biotechnology 41:1633–1644. https://doi.org/10.1038/s41587-023-01688-w
- Beghini F, et al. (2021). *Integrating taxonomic, functional, and strain-level profiling of diverse microbial communities with bioBakery 3.* eLife 10:e65088. https://doi.org/10.7554/eLife.65088
- MetaPhlAn: https://github.com/biobakery/MetaPhlAn · HUMAnN: https://github.com/biobakery/humann · KrakenTools: https://github.com/jenniferlu717/KrakenTools

**کتاب**
- Nagarajan M (ed.) (2018). *Metagenomics: Perspectives, Methods, and Applications*. Academic Press.
- Beiko RG, Hsiao W, Parkinson J (eds.) (2018). *Microbiome Analysis: Methods and Protocols*. Methods Mol Biol 1849. Humana Press.

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins University). دوره‌ای ویژه‌ی سنجش پروفایل متاژنوم در Coursera نیافتیم؛ نزدیک‌ترین: https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Linux* (The Linux Foundation). دوره‌ای ویژه در edX نیافتیم؛ نزدیک‌ترین: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux
- YouTube: *Introduction to Shotgun Metagenomic Data Analysis with bioBakery* (N. Segata، World of Microbiome 2023): https://www.youtube.com/watch?v=T4sviwz9DCk
- YouTube: *Taxonomic, functional, and strain-level profiling with bioBakery 3* (Francesco Beghini، Microbiome Virtual International Forum): https://www.youtube.com/watch?v=t2KkNtE80ro

<sub>نشانی‌های YouTube و DOIها در 2026-10-13 وارسی شدند؛ نشانی‌های Coursera و edX در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
