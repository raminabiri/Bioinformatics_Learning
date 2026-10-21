<div dir="rtl">

# درس ۲: اسمبلی خوب است؟ N50، QUAST، CheckM2 و معیار پذیرش

**بخش:** `07_Bacterial_Genomics` · **ماژول:** `01_Assembly_Quality` · **پیش‌نیاز:** [درس ۱](01_lesson_assembly.md)؛ [Bowtie2 و samtools](../../06_Metagenomics/02_Host_Removal_Alignment/) · **زمان:** حدود ۶۰ دقیقه · **ابزار (از مستندات):** seqkit، QUAST 5.x، CheckM2 1.1، Bowtie2، samtools · **آخرین بازبینی:** 2026-10-21

> ✍️ **وضعیت: نوشته‌شده، اجرا نشده.** QUAST و CheckM2 (با پایگاه داده‌ی کمابیش ۳ گیگابایتی) در این دوره اجرا نشده‌اند. دستورها و تعریف‌ها از مستندات رسمی‌اند؛ هیچ خروجی ساختگی نشان داده نمی‌شود. تمرین‌های تفسیری روی جدول‌های **فرضی** با برچسب روشن کار می‌کنند.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. ‏N50، L50 و NG50 را با دست حساب کنید و دام‌هایشان را بشناسید.
2. گزارش QUAST و CheckM2 را بخوانید.
3. با پوشش و GC هر کانتیگ، پلاسمید، تکرار فشرده و آلودگی را از هم جدا کنید.
4. برای پذیرش یا رد یک اسمبلی، معیار بنویسید.
5. بگویید کِی ریدهای بلند لازم است.

---

## ۱. داستان

درس ۱ گفت اسمبلی Illumina تکه‌تکه است، و این طبیعی است. ولی «طبیعی تکه‌تکه» با «خراب» فرق دارد. اسمبلی می‌تواند **ناقص** (پوشش کم)، **آلوده** (دو گونه در کشت)، **مخلوط** (دو سویه از یک گونه)، یا **از گونه‌ی نادرست** (برچسب اشتباه) باشد. هر کدام نتیجه‌ی بعدی (ژن مقاومت، MLST، فیلوژنی) را خراب می‌کند. این درس سنجه‌های هر کدام را می‌آموزد.

---

## ۲. مفهوم: N50 با دست

‏**N50:** کانتیگ‌ها را از بلند به کوتاه بچینید و طول‌ها را پشت سر هم جمع بزنید. نخستین کانتیگی که جمع را به **نیمی از طول کل** برساند، N50 است؛ رتبه‌اش **L50**.

نمونه‌ی کوچک (**فرضی**): کانتیگ‌هایی به طول ۵۰، ۳۰، ۱۰، ۵، ۵ کیلوباز. طول کل ۱۰۰؛ نیمه ۵۰.

| رتبه | طول | جمع |
| ---: | ---: | ---: |
| **1** | **50** | **50** ≥ 50 |
| 2 | 30 | 80 |

پس **N50 = ۵۰ کیلوباز** و **L50 = ۱**. یعنی «نیمی از اسمبلی در کانتیگ‌هایی ۵۰ کیلوبازی یا بلندتر است».

‏**‏NG50** همین است، ولی نیمه‌ی **طول ژنوم مرجع** (نه طول اسمبلی) را می‌گیرد؛ برای سنجیدن اسمبلی‌هایی با اندازه‌ی گوناگون بهتر است.

**سه دام N50:**
1. تنها **پیوستگی** را می‌سنجد، نه **درستی** را. اسمبلری که دو ناحیه‌ی بی‌ربط را به هم بچسباند، N50 بزرگ‌تری می‌گیرد.
2. برداشتن کانتیگ‌های کوتاه N50 را **بالا** می‌برد، بی آنکه اسمبلی بهتر شده باشد (تمرین ۱). همیشه کمترین طول کانتیگ را گزارش کنید.
3. در اسمبلی **آلوده**، طول کل بزرگ‌تر از انتظار است و N50 کمابیش دیده نمی‌شود (تمرین ۱).

<details>
<summary>✋ امتحان کن: کانتیگ‌های ۴۰، ۴۰، ۱۰، ۱۰ کیلوباز. N50 و L50؟</summary>

طول کل ۱۰۰، نیمه ۵۰. جمع: ۴۰، سپس ۸۰ ≥ ۵۰. پس **N50 = ۴۰** و **L50 = ۲**.

</details>

---

## ۳. گام ۱: آمار پایه با seqkit

<div dir="ltr">

```bash
seqkit stats -a -T shovill_out/contigs.fa
seqkit fx2tab -n -l -g shovill_out/contigs.fa | sort -k2,2nr | head      # name, length, GC per contig
```

</div>

‏`seqkit stats -a` (بخش ۰۲) شمار کانتیگ، طول کل، بلندترین کانتیگ، **N50** و **GC٪** را می‌دهد؛ برای بیشتر کارها بس است. `fx2tab -n -l -g` برای هر کانتیگ نام، طول و GC را در یک سطر می‌نویسد.

---

## ۴. گام ۲: QUAST، پیوستگی و سنجش با مرجع (از مستندات)

<div dir="ltr">

```bash
quast.py shovill_out/contigs.fa -o quast_out -t 8                                     # no reference
quast.py shovill_out/contigs.fa -r ecoli_k12.fna -g ecoli_k12.gff -o quast_ref -t 8   # with a reference
```

</div>

| بخش | چیست |
| :--- | :--- |
| ① `contigs.fa` | یک یا چند اسمبلی (برای سنجیدن کنار هم) |
| ② `-o` | پوشه‌ی خروجی؛ گزارش در `report.tsv` و `report.html` |
| ③ `-r` / `-g` | ژنوم مرجع و آنوتیشن آن (اختیاری) |
| ④ `-t` | هسته‌ها |

تعریف‌ها، به گفته‌ی راهنمای QUAST:

| سنجه | تعریف | نکته |
| :--- | :--- | :--- |
| `# contigs` | شمار کانتیگ‌های ≥ `--min-contig` | **پیش‌فرض ۵۰۰ باز**؛ کانتیگ‌های کوتاه‌تر شمرده نمی‌شوند |
| `Total length` | جمع طول کانتیگ‌ها | باید به اندازه‌ی ژنوم گونه نزدیک باشد (*E. coli*: کمابیش ۴٫۵ تا ۵٫۵ مگاباز) |
| `N50` / `NG50` / `L50` | بخش ۲ | |
| `GC (%)` | درصد GC | با GC گونه بسنجید (*E. coli* ≈ ۵۰٫۸٪) |
| `# misassemblies` | (با مرجع) کانتیگی که دو بخشش دور از هم، در جهت وارونه یا روی دو کروموزوم گوناگون مرجع می‌نشیند | در ایزوله‌ی بالینی، شاید **بازآرایی واقعی** نسبت به K-12 باشد |
| `Genome fraction (%)` | (با مرجع) درصد بازهای مرجع که پوشیده شده‌اند | در سویه‌ی دیگر هرگز ۱۰۰٪ نیست |
| `Duplication ratio` | (با مرجع) بازهای هم‌ترازشده‌ی اسمبلی ÷ بازهای پوشیده‌ی مرجع | بالاتر از کمابیش ۱٫۰۵ = هم‌پوشانی کانتیگ‌ها یا آلودگی هم‌گونه |

---

## ۵. گام ۳: CheckM2، کامل بودن و آلودگی (از مستندات)

<div dir="ltr">

```bash
checkm2 database --download --path ~/databases          # once, about 3 GB
checkm2 predict --threads 8 --input shovill_out/contigs.fa --output-directory checkm2_out \
  --database_path ~/databases/CheckM2_database/uniref100.KO.1.dmnd
```

</div>

خروجی اصلی: `checkm2_out/quality_report.tsv`، با ستون‌های `Name`، `Completeness`، `Contamination`، `Completeness_Model_Used`، `Contig_N50`، `Genome_Size`، `GC_Content` و چند ستون دیگر.

چگونه کار می‌کند؟ (به گفته‌ی README و مقاله‌ی CheckM2) ژن‌ها را پیش‌بینی و کارکردشان را با پایگاه DIAMOND تعیین می‌کند؛ سپس یک **مدل یادگیری ماشین** از الگوی بود و نبود کارکردها، کامل بودن و آلودگی را **پیش‌بینی** می‌کند. دو مدل کامل بودن دارد: **specific** (برای جانداران نزدیک به داده‌ی آموزش) و **general** (برای دودمان‌های تازه)؛ برگزیدن خودکار است و در `Completeness_Model_Used` می‌آید.

**تفسیر برای ایزوله:**
- ‏*E. coli* گونه‌ای شناخته‌شده است؛ ایزوله‌ی سالم باید **کامل بودن نزدیک ۱۰۰٪** و **آلودگی نزدیک ۰٪** داشته باشد.
- **آلودگی بالا** = بیشتر **مخلوط** (دو سویه یا دو گونه در کشت، یا آلودگی در آزمایشگاه).
- **مخلوط دو سویه‌ی یک گونه** آلودگی را کمتر از واقع نشان می‌دهد: ژن‌های کمابیش یکسان در اسمبلی فشرده می‌شوند. نشانه‌های بهتر: طول کل بیشتر از انتظار، و ده‌ها کانتیگ با پوشش کمابیش نیمِ بقیه (تمرین ۴).

---

## ۶. گام ۴: نشاندن ریدها روی اسمبلی

همان ابزارهای بخش ۰۶، ماژول ۰۲:

<div dir="ltr">

```bash
bowtie2-build shovill_out/contigs.fa asm
bowtie2 -p 8 -x asm -1 trim_R1.fastq.gz -2 trim_R2.fastq.gz 2> asm.bowtie2.log | samtools sort -o asm.bam
samtools index asm.bam
samtools coverage asm.bam | sort -k6,6n | head
```

</div>

‏`samtools coverage` برای هر کانتیگ یک سطر دارد؛ ستون ۶ (`coverage`) درصد پوشیده‌شده و ستون ۷ (`meandepth`) میانگین ژرفاست. درصد ریدهایی که **روی اسمبلی** نمی‌نشینند (آخرین خط `asm.bowtie2.log`) باید کم باشد؛ اگر زیاد است، بخشی از ژنوم اسمبل نشده یا ریدها آلوده‌اند.

| پوشش کانتیگ (نسبت به میانه‌ی کروموزوم) | تفسیر محتمل |
| :--- | :--- |
| کمابیش ۱× | کروموزوم |
| ۲× تا ۱۰× | پلاسمید چندنسخه‌ای، یا تکرار فشرده (برای نمونه rRNA ≈ ۷×) |
| بسیار کم (برای نمونه ۰٫۱×) | **آلودگی** (ایزوله یا گونه‌ی دیگر)، یا ساختگی |
| ‏GC بسیار دور از بقیه + پوشش دیگر | آلودگی یا عنصر اکتسابی |

---

## ۷. گام ۵: معیار پذیرش

یک نمونه‌ی رایج، برگرفته از استانداردهای MIMAG و GTDB و آستانه‌های گردش‌کارهای پایش ژنومی. **مقدار دقیق را هر آزمایشگاه برای گونه‌ی خودش تعیین و گزارش می‌کند.**

| سنجه | آستانه‌ی رایج | منطق |
| :--- | :--- | :--- |
| پوشش ریدها | ≥ ۳۰× (بهتر ≥ ۵۰×) | کمتر: اسمبلی پاره، واریانت‌ها نامطمئن |
| Completeness (CheckM2) | ≥ ۹۵٪ | ژنوم ناقص = شاید ژن مقاومت گم شده باشد |
| Contamination (CheckM2) | ≤ ۵٪ | ‏MIMAG «کیفیت بالا»: کامل بودن > ۹۰٪ و آلودگی < ۵٪ |
| Total length | در گستره‌ی شناخته‌شده‌ی گونه | بسیار بزرگ = مخلوط؛ بسیار کوچک = ناقص یا گونه‌ی نادرست |
| ‏GC٪ | ± ۱٪ از مقدار گونه | |
| شمار کانتیگ (≥ ۵۰۰ باز) | برای نمونه < ۵۰۰ | بیشتر: پوشش کم یا داده‌ی بی‌کیفیت |
| شناسایی گونه | با ANI (fastANI، skani) یا Kraken2 | «واقعاً *E. coli* است؟» |

---

## ۸. فراتر از Illumina: کِی ریدهای بلند؟

| هدف | ‏Illumina بس است؟ |
| :--- | :--- |
| ‏MLST، cgMLST، بود و نبود ژن مقاومت | ✅ |
| فیلوژنی بر پایه‌ی SNP (ماژول ۰۵) | ✅ (با نشاندن روی مرجع) |
| ژن مقاومت روی **کدام پلاسمید**؟ ساختار پلاسمید؟ | ❌ ← اسمبلی هیبرید (Unicycler) یا ریدهای بلند (Flye + اصلاح) |
| ژنوم **کامل و بسته** (یک کانتیگ دایره‌ای برای هر replicon) | ‏❌ ← Nanopore یا PacBio |
| شمار نسخه‌های ژن‌های تکراری، جابه‌جایی IS | ❌ |

---

## ۹. سه اشتباه رایج

**۱. داوری تنها با N50.** پیوستگی ≠ درستی؛ با برداشتن کانتیگ‌های کوتاه بالا می‌رود و آلودگی را نشان نمی‌دهد. N50 + طول کل + CheckM2 + پوشش هر کانتیگ.

**۲. نادیده گرفتن پوشش و GC هر کانتیگ.** آلودگی و پلاسمید در طول کل و N50 پنهان می‌مانند؛ نمودار پوشش در برابر GC آن‌ها را جدا می‌کند.

**۳. «ژن روی کروموزوم است» از اسمبلی Illumina.** مرز کانتیگ بیشتر همان IS کنار ژن مقاومت است. بنویسید «روی کانتیگ X؛ replicon نامعلوم»، یا ریدهای بلند بگیرید.

---

## 📘 برای کنجکاوها

- ‏**‏CheckM1 در برابر CheckM2:** CheckM1 ژن‌های تک‌نسخه‌ای ویژه‌ی هر دودمان را می‌شمرد؛ «آلودگی» = چند نسخه از ژنی که باید یک نسخه باشد. CheckM2 به درخت مرجع وابسته نیست و برای دودمان‌های کم‌نماینده درست‌تر است.
- **امتیاز کیفیت GTDB:** ‏`completeness − 5 × contamination ≥ 50`؛ برای MAGها (ژنوم‌های بازسازی‌شده از متاژنوم)، و برای ایزوله بسیار شل.
- ‏**‏misassembly ساختگی:** QUAST با مرجع K-12 بازآرایی واقعی یک سویه‌ی بالینی را هم «misassembly» می‌شمارد؛ با مرجع نزدیک‌تر یا با نشاندن ریدها بسنجید.

---

## جمع‌بندی

- ‏N50 = طول کانتیگی که جمع تجمعی را به نیمه می‌رساند؛ بی کمترین طول کانتیگ سنجیدنی نیست.
- کیفیت = پیوستگی (QUAST) + کامل بودن و آلودگی (CheckM2) + پوشش و GC هر کانتیگ (نشاندن ریدها) + شناسایی گونه.
- معیار پذیرش را پیش از دیدن داده بنویسید و گزارش کنید.
- برای «کدام پلاسمید؟» و «ژنوم بسته»، ریدهای بلند.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
seqkit stats -a -T contigs.fa                                   # N50, total length, GC
seqkit fx2tab -n -l -g contigs.fa | sort -k2,2nr               # length and GC per contig
quast.py contigs.fa [-r ref.fna -g ref.gff] -o quast_out -t 8
checkm2 predict --threads 8 --input contigs.fa --output-directory checkm2_out --database_path DB.dmnd
bowtie2-build contigs.fa asm && bowtie2 -x asm -1 R1 -2 R2 2> log | samtools sort -o asm.bam
samtools index asm.bam && samtools coverage asm.bam            # meandepth per contig
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| ‏N50 / L50 | طول / رتبه‌ی کانتیگی که جمع تجمعی را به نیمه‌ی اسمبلی می‌رساند |
| ‏NG50 | همان، با نیمه‌ی طول ژنوم مرجع |
| کامل بودن (*completeness*) | سهم ژن‌های منتظره که در اسمبلی پیدا شد |
| آلودگی (*contamination*) | نشانه‌ی ژنوم دوم در اسمبلی |
| ‏misassembly | پیوند نادرست دو ناحیه‌ی دور ژنوم در یک کانتیگ |
| ‏ANI | میانگین همسانی نوکلئوتیدی دو ژنوم؛ مرز گونه کمابیش ۹۵٪ |
| ‏replicon | واحد مستقل همانندسازی: کروموزوم یا پلاسمید |

---

## منابع

**مستند و مقاله**
- Gurevich A, et al. (2013). *QUAST: quality assessment tool for genome assemblies.* Bioinformatics 29:1072–1075. https://doi.org/10.1093/bioinformatics/btt086
- Chklovski A, et al. (2023). *CheckM2: a rapid, scalable and accurate tool for assessing microbial genome quality using machine learning.* Nature Methods 20:1203–1212. https://doi.org/10.1038/s41592-023-01940-w
- Bowers RM, et al. (2017). *Minimum information about a single amplified genome (MISAG) and a metagenome-assembled genome (MIMAG) of bacteria and archaea.* Nature Biotechnology 35:725–731. https://doi.org/10.1038/nbt.3893
- Wick RR, et al. (2017). *Unicycler: resolving bacterial genome assemblies from short and long sequencing reads.* PLoS Comput Biol 13:e1005595. https://doi.org/10.1371/journal.pcbi.1005595
- Kolmogorov M, et al. (2019). *Assembly of long, error-prone reads using repeat graphs.* Nature Biotechnology 37:540–546. https://doi.org/10.1038/s41587-019-0072-8
- QUAST manual: https://quast.sourceforge.net/docs/manual.html · CheckM2: https://github.com/chklovski/CheckM2

**فیلم و دوره‌ی آموزشی**
- Coursera: *Genome Sequencing (Bioinformatics II)* (UC San Diego): https://www.coursera.org/learn/genome-sequencing
- ‏edX: *Introduction to Linux* (The Linux Foundation). دوره‌ای ویژه‌ی ارزیابی اسمبلی در edX نیافتیم؛ نزدیک‌ترین: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux
- YouTube: *Module 18: Assembly Metrics w/ QUAST* (Hubbard Center for Genome Studies, UNH): https://www.youtube.com/watch?v=eGlNmC6AuN8
- ‏YouTube: *CheckM for Genome Consistency* (Rob Edwards؛ منطق ژن‌های نشانگر در CheckM1): https://www.youtube.com/watch?v=sLtSDs3sh6k

<sub>نشانی‌های YouTube و DOIها در 2026-10-15 وارسی شدند؛ نشانی‌های Coursera و edX در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
