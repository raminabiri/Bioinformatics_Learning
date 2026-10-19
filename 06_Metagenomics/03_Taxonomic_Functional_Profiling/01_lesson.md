# درس: پروفایل تاکسونومیک (Kraken2 + Bracken) و معرفی پروفایل عملکردی

**بخش:** `06_Metagenomics` · **ماژول:** `03_Taxonomic_Functional_Profiling` · **پیش‌نیاز:** ماژول ۰۲ · **زمان:** ۲٫۵ ساعت · **ابزار:** Kraken2 2.17.1، Bracken 3.0.1 · **آخرین تست:** 2026-10-13

---

> ## ⚠️ دیتابیس این درس فقط برای تمرین است
> برای اینکه درس روی هر لپ‌تاپی و با اینترنت کند اجرا شود، یک **دیتابیس تمرینی کوچک** از ۴۵ ژنوم (۲۶۳ مگابایت) می‌سازیم. این دیتابیس فقط برای **فهم منطق ابزار و سنجش خطاها** مناسب است.
>
> **برای کار پژوهشی واقعی حتماً دیتابیس کامل لازم است**، مثلاً از مجموعه‌های رسمی Kraken2 در https://benlangmead.github.io/aws-indexes/k2 (نسخه‌ی 2026-06-26):
>
> | مجموعه | حجم دانلود | حجم ایندکس | محتوا |
> | :--- | ---: | ---: | :--- |
> | Standard | 79.6 GB | 103.1 GB | RefSeq: باکتری، آرکی، ویروس، انسان، وکتورها |
> | Standard-16 / Standard-8 | 11.2 / 5.5 GB | 14.9 / 7.5 GB | همان، فشرده‌شده تا ۱۶ یا ۸ گیگابایت حافظه (کمی کم‌دقت‌تر) |
> | PlusPF | 84.8 GB | 109.9 GB | Standard + پروتوزوآ و قارچ‌ها |
> | GTDB v226 | 500.9 GB | 644.0 GB | ژنوم‌های نماینده‌ی GTDB |
>
> نتایجی که با دیتابیس تمرینی می‌گیریم (درصدها، تعداد گونه‌های کاذب) **قابل تعمیم به داده‌ی واقعی نیست**. فقط نوع خطاها و منطق تفسیر قابل تعمیم است.

---

## ۱. مسئله

پروفایل تاکسونومیک به سؤال «**چه کسانی و به چه نسبتی در نمونه هستند؟**» جواب می‌دهد. این عدد ساده ظاهر می‌شود ولی سه منبع خطای جدی دارد:

1. **دیتابیس:** ابزار فقط چیزی را می‌شناسد که در دیتابیس هست. گونه‌ی غایب یا «گم» می‌شود یا به نزدیک‌ترین خویشاوند نسبت داده می‌شود.
2. **شباهت گونه‌ها:** ریدهای کوتاه از نواحی حفاظت‌شده بین چند گونه مشترک‌اند.
3. **تعریف فراوانی:** «درصد ریدها» با «درصد سلول‌ها» یکی نیست (اندازه‌ی ژنوم متفاوت است)، و ریدهای طبقه‌بندی‌نشده هم باید جایی حساب شوند.

مزیت داده‌ی این دوره این است که **جواب درست را می‌دانیم** (`data/ground_truth_species.tsv`). پس هر سه نوع خطا را می‌شود **اندازه گرفت**، نه حدس زد.

## ۲. مفاهیم

### ۲.۱ دو رویکرد اصلی
| | **k-mer (Kraken2)** | **ژن نشانگر (MetaPhlAn 4)** |
| :--- | :--- | :--- |
| منطق | هر k-mer (k=35) رید را در دیتابیس جستجو می‌کند. هر k-mer به **LCA** (پایین‌ترین جد مشترک) ژنوم‌هایی که آن را دارند نگاشت شده است | ریدها روی ~۵ میلیون ژن نشانگر **کلاد-اختصاصی** map می‌شوند |
| خروجی | تعداد رید به ازای هر taxon (همه‌ی سطوح) | فراوانی نسبی، نزدیک به «فراوانی سلولی» |
| سرعت | خیلی سریع | سریع |
| ریدهای طبقه‌بندی‌شده | بیشتر ریدها | فقط ریدهای روی نشانگرها (درصد کم، و این طبیعی است) |
| نقطه‌ضعف | false positive زیاد بدون فیلتر؛ وابستگی شدید به دیتابیس | گونه‌های بدون نشانگر دیده نمی‌شوند |

### ۲.۲ چرا Bracken؟
Kraken2 هر رید را به **LCA** نسبت می‌دهد. ریدی که بین *E. coli* و *Shigella* مشترک است در سطح جنس یا خانواده می‌ماند. پس شمارش سطح گونه‌ی Kraken2 **کمتر از واقعیت** است. Bracken با یک مدل احتمالاتی (بر اساس اینکه ریدهای هر ژنوم معمولاً در کدام سطح طبقه‌بندی می‌شوند) این ریدها را **بین گونه‌ها دوباره تقسیم** می‌کند. برای این کار باید با **طول رید** داده ساخته شده باشد (`bracken-build -l`).

### ۲.۳ آستانه‌ی confidence
`--confidence c` در Kraken2 می‌گوید: رید را فقط وقتی به یک taxon نسبت بده که دست‌کم کسر `c` از k-merهای رید آن taxon یا زیرشاخه‌هایش را تأیید کنند. در غیر این صورت رید را به سطح بالاتر ببر. مقدار پیش‌فرض ۰ است، یعنی کمترین سخت‌گیری. برای کاهش false positive در عمل مقادیر کوچکی مثل ۰٫۱ رایج است. مقدار مناسب به دیتابیس و داده بستگی دارد و باید آزمایش شود (گام ۴).

## ۳. کار عملی

### گام ۱: ساخت دیتابیس تمرینی (یک‌بار؛ حدود ۱۳۰ مگابایت دانلود)
```bash
cd 06_Metagenomics
bash 03_Taxonomic_Functional_Profiling/scripts/build_practice_db.sh
```
محتوای دیتابیس در [practice_db_genomes.tsv](practice_db_genomes.tsv) آمده و **عمداً طوری طراحی شده که شبیه دنیای واقعی باشد**:
- **۲۱ گونه‌ی موجود در نمونه‌ها**، ولی با **سویه‌ی دیگری** غیر از سویه‌ای که ریدها از آن شبیه‌سازی شده‌اند. مثلاً *E. coli* با سویه‌ی ST540، نه K-12. در نمونه‌ی واقعی هم سویه‌ی شما تقریباً هیچ‌وقت عیناً در دیتابیس نیست.
- **۲۴ گونه‌ی نزدیک (decoy):** *Shigella sonnei/flexneri* و *Escherichia fergusonii* کنار *E. coli*، *Acinetobacter pittii* کنار *A. baumannii*، *Phocaeicola dorei* کنار *Bacteroides*، و مانند این‌ها.
- ***Candida albicans* (قارچ) عمداً حذف شده**، با اینکه ۳٫۵٪ ریدهای `minigut_sample2` از آن است.

خروجی ساخت (2026-10-13): ۹۲ توالی، 169.3 Mb، فایل `hash.k2d` به حجم 263 MB، و زمان ساخت ۱۸ ثانیه.

### گام ۲: اجرای Kraken2 و Bracken
```bash
bash 03_Taxonomic_Functional_Profiling/scripts/run_profile.sh
```
هسته‌ی اسکریپت:
```bash
kraken2 --db work/03_profile/kraken2_practice_db --threads 8 --paired --confidence 0 \
        --report minigut.kreport --output minigut.kraken \
        work/02_host/clean/minigut_R1.fastq.gz work/02_host/clean/minigut_R2.fastq.gz
bracken -d work/03_profile/kraken2_practice_db -i minigut.kreport -o minigut.bracken -r 125 -l S -t 10
```
```text
== minigut (confidence 0, Bracken -r 125): 47428 sequences classified (95.15%)
== minigut_sample2 (confidence 0, Bracken -r 150): 21364 sequences classified (85.50%)
```

### گام ۳: خواندن گزارش Kraken2
ستون‌های `.kreport`: درصد، ریدهای کلاد (خود taxon و زیرشاخه‌ها)، ریدهای مستقیماً به همین taxon، رتبه، taxid، نام.
```text
 51.37	25605	25605	S	817	      Bacteroides fragilis
  3.02	1503	1503	S	357276	      Phocaeicola dorei
 40.63	20253	4909	F	543	      Enterobacteriaceae
 20.16	10051	300	G	561	        Escherichia
 18.02	8981	8981	S	562	          Escherichia coli
  1.54	770	770	S	564	          Escherichia fergusonii
 10.48	5225	1312	G	620	        Shigella
```
نمونه‌ی `minigut` فقط *B. fragilis* و *E. coli* دارد، ولی Kraken2 ریدها را بین **۹ گونه** پخش کرده است. فایل `.kraken` به ازای هر رید taxid اختصاص‌یافته را دارد. چون نام رید منشأ واقعی را می‌گوید، می‌توانیم دقیق ببینیم ۲۱٬۰۱۸ جفت‌رید *E. coli* کجا رفته‌اند:

| مقصد ریدهای *E. coli* | جفت‌رید | % |
| :--- | ---: | ---: |
| *E. coli* (گونه) | 8,981 | 42.7 |
| Enterobacteriaceae (خانواده؛ LCA) | 4,909 | 23.4 |
| *Shigella sonnei* | 2,241 | 10.7 |
| *Shigella flexneri* | 1,672 | 8.0 |
| *Shigella* (جنس) | 1,312 | 6.2 |
| *E. fergusonii* | 770 | 3.7 |
| طبقه‌بندی‌نشده | 765 | 3.6 |
| *Escherichia* (جنس) | 300 | 1.4 |

```bash
awk -F'\t' '$2 ~ /^NC_000913/ {print $3}' work/03_profile/kraken/minigut_c0.kraken | sort | uniq -c | sort -rn
```

**چرا این‌قدر *Shigella*؟** این خطای ابزار نیست، **واقعیت زیستی** است. *Shigella* از نظر فیلوژنتیک چند دودمان درون گونه‌ی *E. coli* است (Pupo و همکاران، ۲۰۰۰) و فقط به دلایل بالینی و تاریخی نام جنس جدا دارد. نواحی‌ای از ژنوم K-12 که در سویه‌ی *E. coli* دیتابیس (ST540) نیست ولی در *Shigella* هست، به *Shigella* نسبت داده می‌شوند. **درس:** در سطح گونه، مرزهای تاکسونومیک همیشه با مرزهای ژنومی منطبق نیستند.

### گام ۴: سنجش دقت با ground truth
اسکریپت [scripts/evaluate_profile.py](scripts/evaluate_profile.py) خروجی Bracken را با ترکیب واقعی مقایسه می‌کند:
```bash
python3 03_Taxonomic_Functional_Profiling/scripts/evaluate_profile.py work/03_profile/bracken/minigut_c0.bracken minigut
```
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

خلاصه‌ی هر دو نمونه با دو آستانه‌ی confidence:

| نمونه | `--confidence` | گونه‌ی پیش‌بینی‌شده | TP | FP | FN | precision | recall | Bray-Curtis |
| :--- | :-: | -: | -: | -: | -: | :-: | :-: | :-: |
| minigut | 0 | 9 | 2 | 7 | 0 | 0.222 | 1.000 | 0.187 |
| minigut | 0.1 | 6 | 2 | 4 | 0 | 0.333 | 1.000 | 0.156 |
| minigut_sample2 | 0 | 28 | 20 | 8 | 1 | 0.714 | 0.952 | 0.099 |
| minigut_sample2 | 0.1 | 27 | 20 | 7 | 1 | 0.741 | 0.952 | 0.092 |

**تفسیر:**
- **Recall بالا، precision پایین** الگوی کلاسیک Kraken2 است: هر چه هست را پیدا می‌کند، ولی چیزهایی که نیست را هم «پیدا» می‌کند.
- **`--confidence 0.1`** هم false positive و هم خطای فراوانی (Bray-Curtis) را کم کرد، بدون اینکه گونه‌ی واقعی از دست برود.
- **تنها FN نمونه‌ی ۲ *Candida albicans* است.** ۸۷۳ از ۸۷۴ جفت‌رید آن «طبقه‌بندی‌نشده» ماندند، چون در دیتابیس نبود. **ابزار به شما نمی‌گوید چه چیزی را نمی‌شناسد.** «۱۴٫۵٪ طبقه‌بندی‌نشده» همیشه باید پرسیده شود: چه چیزی در این ریدهاست؟
- **فراوانی *E. coli* در `minigut` ۲۷٪ برآورد شد در برابر ۴۲٪ واقعی.** ۱۵ واحد درصد به *Shigella* و *E. fergusonii* رفت. در گزارش سطح **جنس** یا «گروه *E. coli/Shigella*»، این خطا عمدتاً ناپدید می‌شود. انتخاب سطح تاکسونومیک گزارش، تصمیم علمی است.

### گام ۵: فیلتر فراوانی کم، یک شمشیر دولبه
فیلتر رایج «گونه‌های زیر ۱٪ را حذف کن» را امتحان کنید:
```bash
python3 03_Taxonomic_Functional_Profiling/scripts/evaluate_profile.py work/03_profile/bracken/minigut_sample2_c0.bracken minigut_sample2 --min-frac 0.01 | tail -2
```
```text
species predicted=13  TP=12  FP=1  FN=9
precision=0.923  recall=0.571  F1=0.706  Bray-Curtis=0.111
```
precision از ۰٫۷۱ به ۰٫۹۲ رسید، ولی **recall از ۰٫۹۵ به ۰٫۵۷ سقوط کرد**: ۹ گونه‌ی واقعی با فراوانی زیر ۱٪ حذف شدند. در یک جامعه‌ی واقعی با دم بلند گونه‌های کم‌فراوان، چنین آستانه‌ای بخش بزرگی از تنوع را پاک می‌کند. **آستانه را با هدف تحلیل انتخاب و گزارش کنید.**

## ۴. پروفایل عملکردی و MetaPhlAn (معرفی؛ در این دوره اجرا نمی‌شود)

> این بخش **در محیط دوره تست نشده** است. دیتابیس‌های لازم حجیم‌اند (ده‌ها گیگابایت) و با اینترنت فعلی سرور دوره دانلود نشدند. دستورها از مستندات رسمی‌اند و روی سرور پژوهشی با دیتابیس کامل اجرا می‌شوند.

**MetaPhlAn 4** (bioBakery):
```bash
metaphlan clean_R1.fastq.gz,clean_R2.fastq.gz --input_type fastq --nproc 8 -o sample_profile.txt
# نام برخی گزینه‌ها بین نسخه‌های 4.0 و 4.1 تغییر کرده است؛ `metaphlan --help` نسخه‌ی خودتان را ببینید
```
خروجی فراوانی نسبی در همه‌ی سطوح است و برای گونه‌های بدون ژنوم کشت‌شده از «SGB»ها (species-level genome bins) استفاده می‌کند.

**HUMAnN 3** پروفایل **عملکردی** می‌سازد: ریدها اول روی پن‌ژنوم گونه‌های شناسایی‌شده توسط MetaPhlAn map می‌شوند (ChocoPhlAn). ریدهای باقی‌مانده با جستجوی ترجمه‌شده روی UniRef90 بررسی می‌شوند. خروجی‌ها:
- `genefamilies.tsv`: فراوانی خانواده‌های ژنی UniRef90، که می‌شود آن‌ها را به KO یا EC تبدیل کرد (`humann_regroup_table`).
- `pathabundance.tsv`: فراوانی مسیرهای MetaCyc، **به تفکیک گونه (stratified)**.

**ارتباط با بخش ۰۰:** در تمرین gyrA دیدیم برخی ژن‌ها در هیچ مسیر KEGG نیستند. پروفایل «فقط مسیر» این ژن‌ها را نمی‌بیند. برای ژن‌های مقاومت از دیتابیس اختصاصی (CARD، بخش ۰۸) استفاده کنید.

## ۵. دام‌ها (Pitfalls)

| دام | چرا مشکل است | راه درست |
| :--- | :--- | :--- |
| گزارش بدون نسخه‌ی دیتابیس | نتیجه با هر نسخه فرق می‌کند | نام، نسخه و تاریخ دیتابیس را بنویسید |
| `--confidence 0` بدون فیلتر | false positive زیاد (اینجا ۷ گونه‌ی کاذب در برابر ۲ واقعی) | confidence مناسب و/یا آستانه‌ی حداقل رید |
| نادیده گرفتن ریدهای طبقه‌بندی‌نشده | ارگانیسم غایب از دیتابیس دیده نمی‌شود (*Candida*) | درصد unclassified را گزارش و بررسی کنید |
| تفسیر سطح گونه برای گروه‌های بسیار نزدیک | *E. coli/Shigella*، *A. baumannii/pittii*، *B. cereus/anthracis/thuringiensis* | سطح بالاتر یا «complex» گزارش کنید |
| «درصد رید» = «درصد سلول» | ژنوم بزرگ‌تر رید بیشتری تولید می‌کند | صریحاً بگویید کدام است؛ MetaPhlAn به فراوانی سلولی نزدیک‌تر است |
| آستانه‌ی فراوانی دلخواه (۱٪) | تنوع کم‌فراوان پاک می‌شود (recall ۰٫۹۵ ← ۰٫۵۷) | آستانه را با هدف انتخاب و گزارش کنید |
| مقایسه‌ی پروفایل دو ابزار یا دو دیتابیس | تاکسونومی و تعریف فراوانی متفاوت | در یک مطالعه یک روش را ثابت نگه دارید |

## ۶. جمع‌بندی
- Kraken2 ریدها را با k-mer و LCA طبقه‌بندی می‌کند. Bracken ریدهای سطوح بالاتر را بین گونه‌ها تقسیم می‌کند.
- با ground truth دیدیم: recall بالا، precision پایین. گونه‌های نزدیک (*Shigella*) سهم بزرگی از ریدها را می‌گیرند. گونه‌ی غایب از دیتابیس بی‌صدا «طبقه‌بندی‌نشده» می‌ماند.
- `--confidence 0.1` خطاها را کم کرد. آستانه‌ی فراوانی ۱٪ precision را بالا برد ولی نیمی از گونه‌ها را حذف کرد.
- **این همه با دیتابیس تمرینی بود. برای کار واقعی، دیتابیس کامل (مثلاً Standard یا PlusPF) لازم است.**

## ۷. منابع

### مقالات
- Wood DE, Lu J, Langmead B (2019). Improved metagenomic analysis with Kraken 2. *Genome Biology* 20:257. https://doi.org/10.1186/s13059-019-1891-0
- Lu J, et al. (2017). Bracken: estimating species abundance in metagenomics data. *PeerJ Computer Science* 3:e104. https://doi.org/10.7717/peerj-cs.104
- Lu J, et al. (2022). Metagenome analysis using the Kraken software suite. *Nature Protocols* 17:2815–2839. https://doi.org/10.1038/s41596-022-00738-y
- Blanco-Míguez A, et al. (2023). Extending and improving metagenomic taxonomic profiling with uncharacterized species using MetaPhlAn 4. *Nature Biotechnology* 41:1633–1644. https://doi.org/10.1038/s41587-023-01688-w
- Beghini F, et al. (2021). Integrating taxonomic, functional, and strain-level profiling of diverse microbial communities with bioBakery 3. *eLife* 10:e65088. https://doi.org/10.7554/eLife.65088
- Meyer F, et al. (2022). Critical Assessment of Metagenome Interpretation: the second round of challenges (CAMI II). *Nature Methods* 19:429–440. https://doi.org/10.1038/s41592-022-01431-4
- Pupo GM, et al. (2000). Multiple independent origins of *Shigella* clones of *Escherichia coli*. *PNAS* 97(19):10567–10572. https://doi.org/10.1073/pnas.180094797

### مستندات
- Kraken2: https://github.com/DerrickWood/kraken2/wiki/Manual · دیتابیس‌های آماده: https://benlangmead.github.io/aws-indexes/k2
- Bracken: https://github.com/jenniferlu717/Bracken
- MetaPhlAn: https://github.com/biobakery/MetaPhlAn · HUMAnN: https://github.com/biobakery/humann

### ویدیوهای آموزشی
- The Bioinformatics Chat — *#13 Bracken with Jennifer Lu* (گفتگو با نویسنده‌ی Bracken): https://www.youtube.com/watch?v=xbJ-0wtTzf4
- Galaxy Project — *GTN Tutorial: Taxonomic Profiling and Visualization of Metagenomic Data*: https://www.youtube.com/watch?v=jszMnBKm6ig
- World of Microbiome 2023 — N. Segata, *Introduction to Shotgun Metagenomic Data Analysis with bioBakery*: https://www.youtube.com/watch?v=T4sviwz9DCk
- Microbiome Virtual International Forum — Francesco Beghini, *Taxonomic, functional, and strain-level profiling with bioBakery 3*: https://www.youtube.com/watch?v=t2KkNtE80ro

> لینک‌ها در تاریخ 2026-10-13 بررسی شدند (`_tools/check_links.sh`).
