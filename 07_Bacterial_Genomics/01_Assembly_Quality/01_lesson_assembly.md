<div dir="rtl">

# درس ۱: اسمبلی ژنوم باکتری؛ چرا تکه‌تکه می‌شود؟

**بخش:** `07_Bacterial_Genomics` · **ماژول:** `01_Assembly_Quality` · **پیش‌نیاز:** بخش ۰۶، ماژول [کنترل کیفیت ریدها](../../06_Metagenomics/01_Read_QC_Trimming/)؛ [پایتون و Biopython](../../03_Python/04_Biopython_Seq/) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** Python 3 + Biopython (اجراشده)؛ SPAdes 4.x و Shovill 1.1 (از مستندات) · **آخرین بازبینی:** 2026-10-21

> ✍️ **وضعیت این درس: نوشته‌شده، اسمبلی اجرا نشده.** اسمبلی یک ژنوم کامل سنگین است و در این دوره اجرا نمی‌شود (STYLE_GUIDE، بخش ۵.۱). خروجی‌ها دو گونه‌اند:
> - **اجراشده:** محاسبه‌ی سبک تکرارها روی ژنوم *E. coli* K-12 (اسکریپت `repeat_report.py`، ۸ ثانیه، 2026-10-15).
> - **از مستندات:** با نام منبع.
>
> هیچ عدد دیگری از اجرای واقعی اسمبلر در این درس نیست.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. منطق اسمبلی de novo با گراف de Bruijn را با یک نمونه‌ی کوچک دنبال کنید.
2. بگویید چرا تکرارهای بلندتر از k و رید، اسمبلی را می‌شکنند، و سقف اسمبلی Illumina را برای یک ژنوم برآورد کنید.
3. پوشش (*coverage*) را پیش از اسمبلی حساب کنید.
4. یک ایزوله را با SPAdes (`--isolate`) یا Shovill اسمبل کنید و گزینه‌ها را توجیه کنید.

**پیش از آغاز:** همه‌ی ماژول‌های این بخش در یک پوشه‌ی پروژه کار می‌کنند. ژنوم *E. coli* K-12 را از بخش ۰۱ دارید (اگر نه، `download.sh` همان پوشه):

<div dir="ltr">

```bash
conda activate bioinfo_course                 # Python + Biopython (parts 02-03)
mkdir -p ~/genomes && cd ~/genomes
G=~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data
S=~/Bioinformatics_Learning-main/07_Bacterial_Genomics/99_scripts_data/01_Assembly_Quality/scripts
ls $G/ecoli_k12.fna $G/ecoli_k12.gff
```

</div>

---

## ۱. داستان

یک آزمایشگاه بالینی ایزوله‌ی *E. coli* مقاوم به چند دارو دارد و آن را با Illumina (2×150) توالی‌یابی کرده است. پرسش‌های بعدی (کدام ژن مقاومت؟ روی کروموزوم یا پلاسمید؟ کدام سکانس‌تایپ؟ چقدر نزدیک به ایزوله‌ی بیمار دیگر؟) همه یک چیز می‌خواهند: **توالی ژنوم**. ولی دستگاه تنها میلیون‌ها تکه‌ی ۱۵۰ بازی داده است.

**اسمبلی de novo** این تکه‌ها را بی ژنوم مرجع کنار هم می‌گذارد. خروجی آن کمابیش هرگز «یک کروموزوم کامل» نیست؛ بیشتر **۵۰ تا ۲۰۰ کانتیگ** (*contig*: تکه‌ی پیوسته‌ی بازسازی‌شده). این درس می‌گوید چرا، و درس ۲ می‌گوید چگونه بفهمیم اسمبلی «به اندازه‌ی کافی خوب» است.

---

## ۲. مفهوم: گراف de Bruijn

### ۲.۱ چرا گراف؟

روش قدیمی (*Overlap–Layout–Consensus*) همه‌ی ریدها را دوبه‌دو می‌سنجد. با ده میلیون رید یعنی کمابیش ۱۰¹⁴ سنجش: برای ریدهای کوتاه شدنی نیست. **گراف de Bruijn** راه دیگری دارد:
1. هر رید را به **k-mer**ها بشکن (بخش ۰۶، ماژول ۰۳).
2. هر k-mer یک **پیکان** است: از (k−1) باز نخستش به (k−1) باز آخرش.
3. ژنوم = مسیری که از همه‌ی پیکان‌ها می‌گذرد.

شمار k-merهای جدا کمابیش برابر طول ژنوم است، نه شمار ریدها؛ پس حافظه با **اندازه‌ی ژنوم** بالا می‌رود، نه با ژرفای توالی‌یابی.

### ۲.۲ یک نمونه‌ی کوچک (اجراشده با پایتون)

توالی ۲۰ بازی `ATGCGTACGTTAGCGTACGA` یک تکرار ۷ بازی (`GCGTACG`) را در دو جا دارد (جایگاه ۳ و ۱۳):

| k | ‏k-mer روی هم | ‏k-mer جدا | گره‌ی دوراهی (ابهام) |
| ---: | ---: | ---: | :--- |
| 4 | 17 | 13 | `CGT` ← {`GTA`، `GTT`}؛ `ACG` ← {`CGT`، `CGA`} |
| 6 | 15 | 13 | `GTACG` ← {`TACGT`، `TACGA`} |
| 8 | 13 | 13 | `GCGTACG` ← {`CGTACGT`، `CGTACGA`} |
| **9** | 12 | 12 | **هیچ**؛ یک مسیر یکتا |

در k = 8 هیچ k-merی تکراری نیست، ولی گره‌ی ۷ بازی `GCGTACG` هنوز **دو** خروجی دارد. اسمبلر نمی‌داند پس از تکرار به `T` برود یا به `A`؛ پس **کانتیگ را همان‌جا می‌بُرد**.

**قاعده:** تکراری به طول R تنها وقتی حل می‌شود که k ≥ R + 2 باشد، یا یک رید (یا جفت رید) از دو سوی تکرار بگذرد.

<details>
<summary>✋ امتحان کن: تکرار ۷ بازی است. چرا k = 8 بس نبود و k = 9 بس بود؟</summary>

گره‌ها (k−1) بازی‌اند. با k = 8، گره ۷ بازی است و **خود تکرار** یک گره می‌شود که دو راه پس از آن دارد. با k = 9، گره‌ها ۸ بازی‌اند و هر گره یک باز پیش یا پس از تکرار را هم دارد؛ پس دو نسخه‌ی تکرار دو گره‌ی **جدا** می‌شوند. 7 + 2 = 9.

</details>

### ۲.۳ برگزیدن k

| ‏k کوچک | ‏k بزرگ |
| :--- | :--- |
| ‏✅ k-merها حتی در نواحی کم‌پوشش دیده می‌شوند | ✅ تکرارهای بیشتری حل می‌شوند |
| ❌ تکرارهای کوتاه گراف را گره می‌زنند | ‏❌ k-mer باید **کامل و بی‌خطا** در رید باشد؛ در پوشش کم، گراف پاره می‌شود |

راه SPAdes: **چند k** (برای نمونه 21، 33، 55، 77، و برای ریدهای ۱۵۰ بازی تا 127) را پشت سر هم اجرا می‌کند و گراف هر k را با آگاهی از k پیشین می‌سازد. به گفته‌ی راهنمای SPAdes، همه‌ی kها باید **فرد** و **کمتر از ۱۲۸** باشند؛ اگر `-k` ندهید، خودش از روی طول رید برمی‌گزیند. **چرا فرد؟** با k فرد، هیچ k-merی با مکمل وارونه‌ی خودش برابر نیست؛ پس دو رشته‌ی DNA در گراف جدا می‌مانند.

---

## ۳. گام ۱: تکرارهای *E. coli* K-12، سقف اسمبلی Illumina

در ژنوم K-12 چه تکرارهای بلندی هست؟ از GFF همان ژنوم:

| گونه‌ی تکرار | شمار | طول هر نسخه |
| :--- | ---: | :--- |
| اپرون rRNA ‏(16S–23S–5S) | ۷ | کمابیش ۵٫۱ کیلوباز (برای نمونه *rrnH*: 223,771 تا 228,875) |
| توالی درج‌شونده (IS) | ۵۰ | ۱۰۲ تا ۱٬۷۴۸ باز، میانه‌ی ۱٬۱۹۵ (۱۱ نسخه IS5، ۸ نسخه IS1، ۷ نسخه IS2، …) |

هر دو از رید ۱۵۰ بازی، و حتی از قطعه‌ی ۳۰۰ تا ۵۰۰ بازی جفت ریدها، بلندترند. اسکریپت آماده‌ی `repeat_report.py` تکرارها را از دو نگاه می‌سنجد:

<div dir="ltr">

```bash
python3 $S/repeat_report.py $G/ecoli_k12.fna $G/ecoli_k12.gff
```

</div>

<div dir="ltr">

```text
== k-mer view
k	positions_in_repeated_kmers_%
21	2.83
55	2.21
77	2.04
127	1.79
== annotation view (cut at rRNA operons + IS elements; genome treated as linear)
repeat blocks: 49  (87394 bp)
contigs: 50  total: 4554258  largest: 360732  N50: 173810  L50: 10
```

</div>

| بخش خروجی | معنی |
| :--- | :--- |
| ‏`k-mer view` | برای هر k، درصد جایگاه‌هایی از ژنوم که k-mer آن‌ها (روی هر دو رشته) بیش از یک بار در ژنوم آمده |
| ‏`annotation view` | اگر یک اسمبلر **بی‌نقص** ژنوم را تنها روی rRNAها و ISها ببُرد، چه کانتیگ‌هایی می‌ماند |
| ‏`N50`، `L50` | درس ۲؛ فعلاً: «نیمی از ژنوم در کانتیگ‌هایی ۱۷۴ کیلوبازی یا بلندتر است، و ۱۰ کانتیگ بزرگ بس است» |

تفسیر:
- با k = 21، **۲٫۸٪** ژنوم در k-merهای تکراری است؛ با k = 127 هنوز **۱٫۸٪**. k بزرگ‌تر کمک می‌کند، ولی تکرارهای بلند سر جایشان می‌مانند.
- اسمبلر بی‌نقص: **۵۰ کانتیگ**، **N50 کمابیش ۱۷۴ کیلوباز**. **این سقف اسمبلی Illumina برای این ژنوم است**، نه نشانه‌ی کار بد. اسمبلی واقعی بیشتر کانتیگ دارد (خطا، پوشش ناهموار، پروفاژها).
- جمع کانتیگ‌ها ۴٬۵۵۴٬۲۵۸ باز است، **۸۷ کیلوباز کمتر** از ژنوم (۴٬۶۴۱٬۶۵۲): نسخه‌های یک تکرار در اسمبلی تنها **یک بار** می‌آیند (فشرده می‌شوند).

**پیامد زیستی مهم:** ژن‌های مقاومت آنتی‌بیوتیکی بیشتر کنار عناصر IS و روی پلاسمیدها هستند. پس **همان ناحیه‌ای که برای ما مهم است، بیشتر می‌شکند**. پاسخ «این ژن روی کروموزوم است یا پلاسمید؟» با اسمبلی Illumina بیشتر **قطعی نیست** (درس ۲، بخش ۸).

> 📺 **فیلم:** *de Bruijn graph assembly for DNA sequences*: https://www.youtube.com/watch?v=OY9Q_rUCGDw (Rob Edwards)
> 📄 **مرجع:** Compeau PEC, Pevzner PA, Tesler G (2011). *How to apply de Bruijn graphs to genome assembly.* Nature Biotechnology 29:987–991. https://doi.org/10.1038/nbt.2023

---

## ۴. گام ۲: پوشش، پیش از اسمبلی

<div dir="ltr">

```text
coverage = (number of reads × read length) / genome size
```

</div>

نمونه: ۲ میلیون **جفت** رید ۱۵۰ بازی برای ژنوم ۵ مگابازی: (4,000,000 × 150) / 5,000,000 = **۱۲۰×**.

| پوشش | پیامد |
| :--- | :--- |
| کمتر از کمابیش ۳۰× | گراف پاره می‌شود؛ صدها کانتیگ کوتاه |
| ۵۰× تا ۱۵۰× | گستره‌ی خوب برای ایزوله‌ی باکتری |
| بسیار بالا (برای نمونه ۵۰۰×) | خطاهای سیستماتیک هم «پوشش کافی» پیدا می‌کنند و پیکان‌های ساختگی می‌سازند؛ زمان و حافظه بی‌دلیل بالا می‌رود |

شمار بازهای ریدها را `seqkit stats` (بخش ۰۲) می‌دهد؛ ستون `sum_len`. اگر پوشش کمتر از ۳۰× است، مشکل اسمبلی **با پارامتر** حل نمی‌شود؛ تنها توالی‌یابی بیشتر.

---

## ۵. گام ۳: اسمبلی با SPAdes (از مستندات)

> منابع لازم برای یک ایزوله‌ی ۵ مگابازی: ۸ هسته، ۱۶ گیگابایت حافظه، ۱۵ تا ۶۰ دقیقه. نصب با Bioconda (`spades`) در یک محیط جدا. ریدها پیش از اسمبلی با fastp بریده می‌شوند (بخش ۰۶، ماژول ۰۱).

<div dir="ltr">

```bash
spades.py --isolate -1 trim_R1.fastq.gz -2 trim_R2.fastq.gz -o spades_out -t 8 -m 16
```

</div>

| بخش | چیست | بی آن چه می‌شود |
| :--- | :--- | :--- |
| ① `--isolate` | به گفته‌ی راهنمای SPAdes: «برای داده‌ی Illumina ایزوله با پوشش بالا به‌شدت توصیه می‌شود؛ کیفیت اسمبلی و زمان اجرا را بهتر می‌کند». با `--careful` **سازگار نیست** | حالت پیش‌فرض (برای داده‌ی چندمنظوره) |
| ② `-1` / `-2` | ریدهای جفتی | — |
| ③ `-o spades_out` | پوشه‌ی خروجی | — (اجباری) |
| ④ `-t 8` | هسته‌ها | ۱۶ (پیش‌فرض) |
| ⑤ `-m 16` | سقف حافظه (گیگابایت)؛ اگر بیشتر لازم شود، SPAdes می‌ایستد | ۲۵۰ (پیش‌فرض) |

گزینه‌های دیگر: `-k` (فهرست kها؛ بیشتر لازم نیست)، `--cov-cutoff auto` (کانتیگ‌های کم‌پوشش را خودش بردارد)، `--plasmid` (plasmidSPAdes: **تنها** پلاسمیدها را اسمبل می‌کند).

خروجی‌های مهم در `spades_out/`:
- ‏**`contigs.fasta`**: کانتیگ‌ها، با نام‌هایی مانند `>NODE_1_length_263154_cov_8.9…` (طول و **پوشش k-mer** در خود نام).
- ‏`scaffolds.fasta`: کانتیگ‌هایی که با جفت ریدها به هم وصل شده‌اند؛ فاصله‌ها با `N` پر شده.
- ‏**`assembly_graph.gfa`**: خود گراف. با **Bandage** باز کنید تا ببینید کانتیگ‌ها کجا به هم گره خورده‌اند (تکرارها).

> 📺 **فیلم:** *Module 17: Genome Assembly w/ SPAdes*: https://www.youtube.com/watch?v=A84bYOyKA0M (UNH)
> 📄 **مرجع:** Bankevich A, et al. (2012). *SPAdes.* J Comput Biol 19:455–477. https://doi.org/10.1089/cmb.2012.0021

---

## ۶. گام ۴: Shovill، پیشنهادی برای ایزوله‌ها (از مستندات)

‏**Shovill** دستوری است که SPAdes را با گام‌های پیرامونش یکجا اجرا می‌کند. به گفته‌ی README رسمی:
1. برآورد اندازه‌ی ژنوم و طول رید (اگر `--gsize` ندهید، با `mash`)
2. زیرنمونه‌گیری تا ژرفای معقول (پیش‌فرض `--depth 150`)
3. برداشتن آداپتور (تنها با `--trim`)
4. تصحیح محافظه‌کارانه‌ی خطای ریدها (Lighter)
5. یکی کردن جفت‌های هم‌پوشان (FLASh)
6. اسمبلی با SPAdes (یا SKESA یا Megahit)
7. تصحیح خطاهای کوچک اسمبلی با نشاندن ریدها روی کانتیگ‌ها (Pilon)
8. برداشتن کانتیگ‌های بسیار کوتاه، کم‌پوشش، یا تک‌بازی
9. نام‌گذاری مرتب کانتیگ‌ها

<div dir="ltr">

```bash
shovill --outdir shovill_out --R1 trim_R1.fastq.gz --R2 trim_R2.fastq.gz \
  --gsize 5M --cpus 8 --ram 16 --minlen 200
```

</div>

| بخش | چیست |
| :--- | :--- |
| ① `--gsize 5M` | اندازه‌ی ژنوم؛ برای زیرنمونه‌گیری |
| ② `--cpus 8 --ram 16` | هسته و حافظه |
| ③ `--minlen 200` | کانتیگ‌های کوتاه‌تر از ۲۰۰ باز کنار بروند؛ کمابیش همیشه ساختگی یا تکه‌ی تکرارند، و NCBI هم آن‌ها را نمی‌پذیرد |

‏**هشدار README:** Shovill برای **ایزوله**ی باکتری است، نه متاژنوم یا ژنوم‌های بزرگ (برای متاژنوم: MEGAHIT یا metaSPAdes).

خروجی (**از مستندات**: بخش Quick Start در README رسمی Shovill، روی داده‌ی آزمون کوچک خودش):

<div dir="ltr">

```text
Final assembly in: test/contigs.fa
It contains 17 (min=150) contigs totalling 169611 bp.
```

</div>

<div dir="ltr">

```text
>contig00001 len=52653 cov=32.7 corr=1 origname=NODE_3 date=20180327 sw=shovill/1.0.1
```

</div>

| بخش سرآیند | معنی |
| :--- | :--- |
| `len` | طول کانتیگ |
| `cov` | میانگین پوشش k-mer |
| `corr` | شمار تصحیح‌های پس از اسمبلی (گام ۷) |
| `origname` | نام اصلی در خروجی SPAdes |

پوشش هر کانتیگ را از همین سرآیند با `sed -E` (بخش ۰۱) درمی‌آورید:

<div dir="ltr">

```bash
grep '>' shovill_out/contigs.fa | sed -E 's/.*len=([0-9]+) cov=([0-9.]+).*/\1\t\2/' | sort -k2,2n | head
```

</div>

‏(جدولی دو ستونی از طول و پوشش، مرتب از کم‌پوشش‌ترین؛ درس ۲ آن را تفسیر می‌کند.)

> 📺 **فیلم:** *GTN Tutorial: Genome Assembly of a bacterial genome (MRSA) sequenced using Illumina MiSeq*: https://www.youtube.com/watch?v=rRHH77qtZHg (Galaxy Project)
> 📄 **مرجع:** Shovill: https://github.com/tseemann/shovill

---

## ۷. سه اشتباه رایج

**۱. انتظار یک کانتیگ از Illumina.** تکرارهای بلندتر از رید و قطعه (rRNA، IS) با هیچ k یا پارامتری حل نمی‌شوند. ۵۰ تا ۲۰۰ کانتیگ طبیعی است؛ برای ژنوم بسته، ریدهای بلند (درس ۲، بخش ۸).

‏**۲. ‏`--careful` همراه `--isolate`.** SPAdes این دو را سازگار نمی‌داند؛ برای ایزوله `--isolate` را برگزینید.

**۳. اسمبلی پیش از حساب پوشش.** با ۲۰× صدها کانتیگ کوتاه می‌گیرید و ژن‌هایی را از دست می‌دهید؛ هیچ پارامتری آن را جبران نمی‌کند. پوشش را نخست حساب کنید.

---

## 📘 برای کنجکاوها

- ‏**‏Bandage:** گراف `assembly_graph.gfa` را می‌کشد. یک اپرون rRNA به شکل گرهی دیده می‌شود که به هفت جای گوناگون وصل است.
- **ریدهای بلند:** Nanopore (R10.4) و PacBio HiFi ریدهای ده‌ها کیلوبازی می‌دهند و از روی rRNA و IS می‌گذرند؛ با Flye، Trycycler یا Autocycler، ژنوم باکتری کامل و بسته شدنی است.
- ‏**‏SKESA و MEGAHIT:** اسمبلرهای دیگر de Bruijn؛ SKESA محافظه‌کارتر است (کانتیگ کمتر ساختگی)، MEGAHIT برای متاژنوم.

---

## جمع‌بندی

- ‏de Bruijn ریدها را به k-mer می‌شکند؛ تکراری به طول R تنها با k ≥ R + 2 یا ریدی بلندتر از آن حل می‌شود.
- در *E. coli* K-12، تنها ۷ اپرون rRNA و ۵۰ عنصر IS سقف اسمبلی Illumina را **کمابیش ۵۰ کانتیگ و N50 کمابیش ۱۷۴ کیلوباز** می‌گذارند.
- پوشش را پیش از اسمبلی حساب کنید؛ ۵۰× تا ۱۵۰× خوب است.
- ‏SPAdes با `--isolate`، یا Shovill (زیرنمونه‌گیری، تصحیح، پالایش، `--minlen 200`).

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
python3 $S/repeat_report.py genome.fna genome.gff [--k 21 127]   # repeats and the Illumina ceiling
seqkit stats -a -T trim_R*.fastq.gz                              # sum_len -> coverage
spades.py --isolate -1 R1.fq.gz -2 R2.fq.gz -o spades_out -t 8 -m 16
shovill --outdir shovill_out --R1 R1.fq.gz --R2 R2.fq.gz --gsize 5M --cpus 8 --ram 16 --minlen 200
grep '>' shovill_out/contigs.fa | sed -E 's/.*len=([0-9]+) cov=([0-9.]+).*/\1\t\2/' | sort -k2,2n
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| اسمبلی de novo | بازسازی ژنوم از ریدها، بی ژنوم مرجع |
| کانتیگ (*contig*) | تکه‌ی پیوسته‌ی بازسازی‌شده |
| اسکافولد (*scaffold*) | کانتیگ‌هایی که با جفت ریدها کنار هم گذاشته شده‌اند؛ فاصله‌ها `N` |
| گراف de Bruijn | گرافی که هر k-mer در آن یک پیکان میان دو (k−1)-mer است |
| پوشش (*coverage*) | میانگین شمار ریدهایی که روی هر باز ژنوم می‌افتند |
| ‏IS (*insertion sequence*) | عنصر متحرک کوتاه (کمابیش ۱ تا ۲ کیلوباز) که در ژنوم جابه‌جا می‌شود |

---

## منابع

**مستند و مقاله**
- Compeau PEC, Pevzner PA, Tesler G (2011). *How to apply de Bruijn graphs to genome assembly.* Nature Biotechnology 29:987–991. https://doi.org/10.1038/nbt.2023
- Bankevich A, et al. (2012). *SPAdes: a new genome assembly algorithm and its applications to single-cell sequencing.* J Comput Biol 19:455–477. https://doi.org/10.1089/cmb.2012.0021
- Prjibelski A, et al. (2020). *Using SPAdes de novo assembler.* Current Protocols in Bioinformatics 70:e102. https://doi.org/10.1002/cpbi.102
- Wick RR, et al. (2015). *Bandage: interactive visualization of de novo genome assemblies.* Bioinformatics 31:3350–3352. https://doi.org/10.1093/bioinformatics/btv383
- SPAdes manual: https://github.com/ablab/spades/blob/main/docs/running.md · Shovill README: https://github.com/tseemann/shovill

**کتاب**
- ‏Compeau P, Pevzner P (2015). *Bioinformatics Algorithms: An Active Learning Approach*, 2nd ed. Active Learning Publishers. (فصل ۳: اسمبلی ژنوم و گراف de Bruijn)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Genome Sequencing (Bioinformatics II)* (UC San Diego)؛ گراف de Bruijn و اسمبلی: https://www.coursera.org/learn/genome-sequencing
- ‏edX: *Introduction to Linux* (The Linux Foundation). دوره‌ای ویژه‌ی اسمبلی ژنوم در edX نیافتیم؛ نزدیک‌ترین: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux
- YouTube: *de Bruijn graph assembly for DNA sequences* (Rob Edwards, San Diego State University): https://www.youtube.com/watch?v=OY9Q_rUCGDw
- YouTube: *Module 17: Genome Assembly w/ SPAdes* (Hubbard Center for Genome Studies, UNH): https://www.youtube.com/watch?v=A84bYOyKA0M
- YouTube: *GTN Tutorial: Genome Assembly of a bacterial genome (MRSA) sequenced using Illumina MiSeq* (Galaxy Project): https://www.youtube.com/watch?v=rRHH77qtZHg

<sub>نشانی‌های YouTube و DOIها در 2026-10-15 وارسی شدند؛ نشانی‌های Coursera و edX در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
