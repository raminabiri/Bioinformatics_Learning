<div dir="rtl">

# درس: برداشتن DNA میزبان با Bowtie2 و samtools

**بخش:** `06_Metagenomics` · **ماژول:** `02_Host_Removal_Alignment` · **پیش‌نیاز:** ماژول [کنترل کیفیت](../01_Read_QC_Trimming/)؛ [SAM/BAM، FLAG و MAPQ](../../02_BioLinux/04_Align_Variant_Formats/) · **زمان:** حدود ۷۵ دقیقه · **ابزار:** Bowtie2 2.5.4، samtools 1.20، wgsim · **خروجی‌ها از اجرای:** 2026-10-13

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. بگویید چرا ریدهای انسانی باید **پیش از** هر تحلیل دیگری برداشته شوند.
2. برای یک ژنوم مرجع، شاخص (*index*) Bowtie2 بسازید و ریدهای جفتی را روی آن هم‌تراز کنید.
3. گزارش Bowtie2 و `samtools flagstat` را بخوانید.
4. با `samtools view -f 12` تنها جفت‌هایی را نگه دارید که **هیچ‌کدام از دو رید** روی میزبان ننشسته‌اند، و آن‌ها را دوباره FASTQ کنید.
5. با یک آزمایش کنترل‌شده (ریدهای انسانی با مبدأ معلوم) بسنجید که برداشتن میزبان چقدر خوب کار کرده است.

**پیش از آغاز:** در پوشه‌ی پروژه باشید؛ ماژول ۰۱ باید `qc/trimmed/` را ساخته باشد. دو تکه‌ی کوچک از ژنوم انسان را با `curl` (بخش ۰۱) بگیرید:

<div dir="ltr">

```bash
conda activate metagenomics
cd ~/meta
mkdir -p host/ref
curl -L -o host/ref/host_chr21_region.fa \
  https://raw.githubusercontent.com/nf-core/test-datasets/mag/host_reference/genome.hg38.chr21_10000bp_region.fa
curl -s -o host/ref/human_chr1_region.fa \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000001.11&rettype=fasta&retmode=text&seq_start=100000001&seq_stop=100300000"
head -n 1 host/ref/*.fa
```

</div>

<div dir="ltr">

```text
==> host/ref/host_chr21_region.fa <==
>chr21part

==> host/ref/human_chr1_region.fa <==
>NC_000001.11:100000001-100300000 Homo sapiens chromosome 1, GRCh38.p14 Primary Assembly
```

</div>

| فایل | چیست | اندازه |
| :--- | :--- | ---: |
| `host_chr21_region.fa` | ناحیه‌ای از کروموزوم ۲۱ انسان (hg38)؛ **مرجع میزبان** ما | ۵۰۰ کیلوباز |
| `human_chr1_region.fa` | ناحیه‌ای از کروموزوم ۱ (GRCh38، ۱۰۰٫۰ تا ۱۰۰٫۳ مگاباز)؛ **بیرون** از مرجع، برای آزمایش بخش ۶ | ۳۰۰ کیلوباز |

> ⚠️ **تنها برای تمرین.** مرجع میزبان این درس ۵۰۰ کیلوباز است. در کار واقعی، **کل** ژنوم انسان (کمابیش ۳٫۱ گیگاباز) به کار می‌رود؛ شاخص آماده‌ی Bowtie2 برای آن از https://benlangmead.github.io/aws-indexes/bowtie گرفته می‌شود (چند گیگابایت). بخش ۶ نشان می‌دهد مرجع ناقص چه بهایی دارد.

---

## ۱. داستان

نمونه‌ی متاژنوم انسانی همیشه مقداری DNA **خود انسان** دارد: در مدفوع کم، ولی در بزاق، خلط، بافت یا خون گاهی بیشتر ریدها. پیش از هر تحلیلی این ریدها باید بروند، به دو دلیل:

1. **اخلاق و قانون:** ریدهای انسانی اطلاعات ژنتیکی شرکت‌کننده‌اند. گذاشتن آن‌ها در پایگاه عمومی (ENA/SRA) با ریدهای میکروبی، حریم خصوصی را می‌شکند و در بیشتر رضایت‌نامه‌ها پذیرفته نیست.
2. **علم:** ریدهای انسانی زمان محاسبه را هدر می‌دهند و گاهی به‌اشتباه به یک باکتری نسبت داده می‌شوند (ماژول ۰۳). **درصد میزبان** خودش یک سنجه‌ی QC است: نمونه‌ای با ۹۵٪ رید انسانی، ژرفای میکروبی کافی ندارد.

---

## ۲. مفهوم به زبان ساده

### ۲.۱ ایده: «بر ژنوم انسان می‌نشیند؟»

هر جفت رید را روی ژنوم میزبان **هم‌تراز** می‌کنیم (بخش ۰۲، ماژول ۰۴: هم‌ترازی = یافتن جایی از مرجع که بیشترین همانندی را دارد). سپس:

<div dir="ltr">

```text
pair: R1 ─────►         ◄───── R2
        lands on host?     lands on host?
           no                 no          -> KEEP (microbial)
           yes                yes         -> remove
           yes                no          -> remove (one human mate is enough)
```

</div>

**قاعده:** جفتی را نگه دار که **هیچ‌کدام** از دو ریدش روی میزبان ننشسته‌اند.

### ۲.۲ شاخص: فهرست الفبایی یک کتاب

یافتن ۵۰٬۰۰۰ رید در یک متن ۳ میلیارد حرفی، با سنجیدن رید با هر جایگاه، سال‌ها طول می‌کشد. Bowtie2 ژنوم را **یک بار** به یک «شاخص» تبدیل می‌کند، همانند فهرست الفبایی پایان یک کتاب: برای هر تکه‌ی کوتاه، جای آن در ژنوم را سریع پیدا می‌کند. سپس هر رید را از چند تکه‌ی کوتاهش (*seed*) پیدا می‌کند و پیرامون آن را باز به باز می‌سنجد.

### ۲.۳ یادآوری FLAG (بخش ۰۲)

| بیت | نام | معنی |
| ---: | :--- | :--- |
| 1 | PAIRED | رید جفتی است |
| 2 | PROPER_PAIR | دو رید با جهت و فاصله‌ی درست نشسته‌اند |
| **4** | **UNMAP** | **خود** این رید ننشسته است |
| **8** | **MUNMAP** | **جفتِ** (*mate*) این رید ننشسته است |
| 64 / 128 | READ1 / READ2 | رید اول یا دوم جفت |
| 256 | SECONDARY | جای دوم یک رید (نه رکورد اصلی) |

پس «هیچ‌کدام ننشسته» = بیت ۴ **و** بیت ۸ هر دو روشن = `-f 12` (چون 4 + 8 = 12).

---

## ۳. گام ۱: ساختن شاخص

<div dir="ltr">

```bash
mkdir -p host/index
bowtie2-build -q host/ref/host_chr21_region.fa host/index/host
ls host/index
```

</div>

<div dir="ltr">

```text
host.1.bt2  host.2.bt2  host.3.bt2  host.4.bt2  host.rev.1.bt2  host.rev.2.bt2
```

</div>

| بخش | چیست | بی آن چه می‌شود |
| :--- | :--- | :--- |
| ① `bowtie2-build` | ابزار ساختن شاخص (همراه Bowtie2) | — |
| ② `-q` | آرام؛ پیام‌های بلند ساختن چاپ نشوند | صدها خط گزارش روی صفحه |
| ③ `host/ref/host_chr21_region.fa` | مرجع (FASTA) | — |
| ④ `host/index/host` | **پیشوند** نام فایل‌های شاخص، نه یک فایل | — |

شش فایل `.bt2` با هم «شاخص» را می‌سازند. در گام بعد تنها **پیشوند** (`host/index/host`) را به Bowtie2 می‌دهیم، نه نام یک فایل. برای ۵۰۰ کیلوباز چند ثانیه؛ برای کل ژنوم انسان چند ساعت و ده‌ها گیگابایت حافظه. برای همین در کار واقعی شاخص آماده را دانلود می‌کنند.

> 📺 **فیلم:** *Burrows-Wheeler Transform*: https://www.youtube.com/watch?v=4n7NPk5lwbI · *FM Index*: https://www.youtube.com/watch?v=kvVGj5V65io (Ben Langmead)
> 📄 **مرجع:** Langmead B, Salzberg SL (2012). *Fast gapped-read alignment with Bowtie 2.* Nature Methods 9:357–359. https://doi.org/10.1038/nmeth.1923

---

## ۴. گام ۲: هم‌ترازی نمونه‌ی `minigut`

<div dir="ltr">

```bash
mkdir -p host/bam host/logs
bowtie2 -p 4 --very-sensitive -x host/index/host \
    -1 qc/trimmed/minigut_R1.fastq.gz -2 qc/trimmed/minigut_R2.fastq.gz \
    2> host/logs/minigut.bowtie2.log \
  | samtools view -b -o host/bam/minigut.unsorted.bam -
cat host/logs/minigut.bowtie2.log
```

</div>

| بخش | چیست | بی آن چه می‌شود |
| :--- | :--- | :--- |
| ① `-p 4` | چهار هسته | کندتر |
| ② `--very-sensitive` | ‏seedهای کوتاه‌تر و تلاش بیشتر | پیش‌فرض (`--sensitive`) ریدهای کمی ناهمسان را کمتر پیدا می‌کند؛ این‌جا **یافتن** همه‌ی ریدهای انسانی مهم است، نه سرعت |
| ③ `-x host/index/host` | پیشوند شاخص | — |
| ④ `-1` / `-2` | ریدهای R1 / R2 (جفتی) | با `-U` ریدها تکی پنداشته می‌شوند |
| ⑤ `2> …log` | ‏Bowtie2 گزارش را در stderr می‌نویسد؛ به فایل | گزارش روی صفحه می‌آید و گم می‌شود |
| ⑥ `\| samtools view -b -o … -` | خروجی SAM (در stdout) را مستقیم به BAM فشرده تبدیل کن؛ `-` = «از ورودی استاندارد بخوان» | یک فایل SAM بزرگ (چند برابر BAM) روی دیسک |

‏Bowtie2 دو چیز می‌نویسد: هم‌ترازی‌ها (SAM) در **stdout** و گزارش در **stderr** (بخش ۰۱، ماژول ۰۴). برای همین می‌توان هم‌زمان SAM را به `samtools` لوله کرد و گزارش را با `2>` نگه داشت.

<div dir="ltr">

```text
49845 reads; of these:
  49845 (100.00%) were paired; of these:
    49845 (100.00%) aligned concordantly 0 times
    0 (0.00%) aligned concordantly exactly 1 time
    0 (0.00%) aligned concordantly >1 times
    ----
    49845 pairs aligned concordantly 0 times; of these:
      0 (0.00%) aligned discordantly 1 time
    ----
    49845 pairs aligned 0 times concordantly or discordantly; of these:
      99690 mates make up the pairs; of these:
        99690 (100.00%) aligned 0 times
        0 (0.00%) aligned exactly 1 time
        0 (0.00%) aligned >1 times
0.00% overall alignment rate
```

</div>

- خط ۱: ۴۹٬۸۴۵ **جفت** (Bowtie2 جفت‌ها را «reads» می‌نامد) همان شمار پس از fastp.
- ‏**concordantly**: دو رید جفت، با جهت درست و فاصله‌ی پذیرفتنی، نشسته‌اند. این‌جا هیچ.
- ‏**0.00% overall alignment rate**: هیچ رید انسانی نیست. این داده شبیه‌سازی‌شده و تنها از ژنوم‌های میکروبی است، پس همین انتظار می‌رفت.

پس **نمی‌توانیم بسنجیم** برداشتن میزبان چقدر خوب کار می‌کند! گام بعد این مشکل را حل می‌کند.

<details>
<summary>✋ امتحان کن: نمونه‌ی <code>minigut_sample2</code> چند جفت پاک می‌دهد؟</summary>

همان شمار ورودی، **۲۴٬۹۸۸** جفت؛ آن هم ۰٫۰۰٪ هم‌ترازی دارد (اسکریپت بخش ۸ هر دو را نشان می‌دهد).

</details>

> 📺 **فیلم:** *#44 Lockdown Learning Bioinformatics-along: Bowtie2*: https://www.youtube.com/watch?v=_NPsnbSedIA
> 📄 **مرجع:** Bowtie2 manual: https://github.com/BenLangmead/bowtie2

---

## ۵. گام ۳: آزمایش کنترل‌شده، ریدهای انسانی با مبدأ معلوم

به `minigut` ریدهای انسانی **شبیه‌سازی‌شده** می‌افزاییم و نام هر رید را با مبدأش آغاز می‌کنیم:

| مبدأ | جفت | در شاخص میزبان هست؟ |
| :--- | ---: | :---: |
| باکتری‌ها (`minigut` پس از QC) | 49,845 | — |
| انسان: ناحیه‌ی chr21 | 5,000 | ✅ |
| انسان: ناحیه‌ی chr1 | 5,000 | ❌ |

ابزار **wgsim** (همراه پروژه‌ی samtools) از یک FASTA ریدهای جفتی ساختگی می‌سازد. اسکریپت آماده:

<div dir="ltr">

```bash
S=~/Bioinformatics_Learning-main/06_Metagenomics/99_scripts_data/02_Host_Removal_Alignment/scripts
bash $S/make_spiked_sample.sh
```

</div>

<div dir="ltr">

```text
file	num_seqs
host/spiked/minigut_spiked_R1.fastq.gz	59845
host/spiked/minigut_spiked_R2.fastq.gz	59845
```

</div>

هسته‌ی اسکریپت، برای chr21:

<div dir="ltr">

```bash
wgsim -N 5000 -1 126 -2 126 -d 350 -s 50 -e 0.002 -r 0.001 -R 0.1 -S 42 \
      host/ref/host_chr21_region.fa human_chr21_R1.fq human_chr21_R2.fq
```

</div>

| گزینه | معنی |
| :--- | :--- |
| `-N 5000` | ۵۰۰۰ جفت |
| `-1 126 -2 126` | طول R1 و R2، همانند داده‌ی ما |
| `-d 350 -s 50` | درازای قطعه: میانگین ۳۵۰، پراکندگی ۵۰ |
| `-e 0.002` | خطای توالی‌یابی ۰٫۲٪ در هر باز |
| `-r 0.001 -R 0.1` | جهش‌های کوچک (همانند تفاوت دو انسان) |
| `-S 42` | **دانه‌ی تصادفی ثابت**: ریدهای شما دقیقاً همین‌ها خواهند بود |

سپس اسکریپت با `sed` (بخش ۰۱) آغاز نام ریدها را `HUMAN_chr21_` یا `HUMAN_chr1_` می‌کند و همه را با ریدهای `minigut` در یک فایل می‌گذارد.

---

## ۶. گام ۴: هم‌ترازی نمونه‌ی آزمایشی

همان دستور گام ۲، با ورودی `host/spiked/minigut_spiked_R*.fastq.gz`:

<div dir="ltr">

```text
59845 reads; of these:
  59845 (100.00%) were paired; of these:
    54773 (91.52%) aligned concordantly 0 times
    1085 (1.81%) aligned concordantly exactly 1 time
    3987 (6.66%) aligned concordantly >1 times
    ----
    54773 pairs aligned concordantly 0 times; of these:
      0 (0.00%) aligned discordantly 1 time
    ----
    54773 pairs aligned 0 times concordantly or discordantly; of these:
      109546 mates make up the pairs; of these:
        109336 (99.81%) aligned 0 times
        66 (0.06%) aligned exactly 1 time
        144 (0.13%) aligned >1 times
8.65% overall alignment rate
```

</div>

- ‏1085 + 3987 = **۵۰۷۲ جفت** concordant نشسته‌اند؛ بیش از ۵۰۰۰ جفت chr21. چرا بیشتر؟ برخی ریدهای chr1 هم نشسته‌اند (بخش ۷).
- ‏**`>1 times`** (۳۹۸۷ جفت): به **چند** جای مرجع به یک اندازه می‌خورند. ناحیه‌ی chr21 ما تکه‌های تکراری بزرگ دارد (بخش ۸).
- ‏۶۶ + ۱۴۴ = **۲۱۰ رید تکی** که جفتشان ننشسته است. این‌ها را هم باید برداشت (قاعده‌ی بخش ۲.۱).

### ‏`samtools flagstat`: همین، از دید BAM

<div dir="ltr">

```bash
samtools sort -o host/bam/minigut_spiked.host.bam host/bam/minigut_spiked.unsorted.bam
samtools index host/bam/minigut_spiked.host.bam
samtools flagstat host/bam/minigut_spiked.host.bam
```

</div>

<div dir="ltr">

```text
119690 + 0 in total (QC-passed reads + QC-failed reads)
119690 + 0 primary
0 + 0 secondary
0 + 0 supplementary
0 + 0 duplicates
0 + 0 primary duplicates
10354 + 0 mapped (8.65% : N/A)
10354 + 0 primary mapped (8.65% : N/A)
119690 + 0 paired in sequencing
59845 + 0 read1
59845 + 0 read2
10144 + 0 properly paired (8.48% : N/A)
10158 + 0 with itself and mate mapped
196 + 0 singletons (0.16% : N/A)
0 + 0 with mate mapped to a different chr
0 + 0 with mate mapped to a different chr (mapQ>=5)
```

</div>

- ‏`samtools sort`: BAM را به ترتیب جایگاه در مرجع مرتب می‌کند؛ `samtools index` فایل `.bai` را می‌سازد (بخش ۰۲) تا BAM با `samtools view` ناحیه‌ای و IGV دیده شود.
- ‏**119690** = ۵۹٬۸۴۵ × ۲: رکوردها **رید تکی**‌اند.
- ‏**10354 mapped**: ریدهایی که نشسته‌اند = 10158 (خودش و جفتش) + 196 (تنها خودش، `singletons`).

---

## ۷. گام ۵: نگه داشتن جفت‌های پاک

<div dir="ltr">

```bash
mkdir -p host/clean
samtools view -b -f 12 -F 256 host/bam/minigut_spiked.unsorted.bam \
  | samtools fastq -1 host/clean/minigut_spiked_R1.fastq.gz -2 host/clean/minigut_spiked_R2.fastq.gz \
                   -0 /dev/null -s /dev/null -n -
```

</div>

| بخش | چیست | بی آن چه می‌شود |
| :--- | :--- | :--- |
| ① `-f 12` | تنها رکوردهایی که بیت ۴ **و** ۸ را دارند: خودش و جفتش هر دو ننشسته | با `-f 4`، رکوردهای R2ای که R1 انسانی دارد هم می‌مانند و جفت‌ها نیمه می‌شوند |
| ② `-F 256` | جای‌های دوم (*secondary*) را کنار بگذار | با `-k` یا `-a`، یک رید چند بار در FASTQ می‌آمد |
| ③ `samtools fastq` | ‏BAM را دوباره FASTQ کن | — |
| ④ `-1` / `-2` | ریدهای اول / دوم جفت، در دو فایل | همه در یک فایل، پشت سر هم |
| ⑤ `-0 /dev/null -s /dev/null` | ریدهای بی‌نشان و تک‌مانده را دور بریز. `/dev/null` «سیاه‌چاله»ی لینوکس است: هر چه در آن بنویسید ناپدید می‌شود | چنین ریدهایی (این‌جا هیچ) در stdout چاپ می‌شدند |
| ⑥ `-n` | نام رید را دست نزن (بی افزودن `/1` و `/2`) | — |
| ⑦ `-` | ورودی از لوله | — |

چرا روی BAM **مرتب‌نشده**؟ Bowtie2 دو رید هر جفت را **پشت سر هم** می‌نویسد. `samtools fastq` از همین ترتیب جفت‌ها را پیدا می‌کند. BAM مرتب‌شده بر پایه‌ی جایگاه، دو رید یک جفت را از هم دور می‌کند.

### چه چیزی ماند؟

چون نام هر رید مبدأش را دارد، می‌شماریم (`sed -E` و گروه `\1`: بخش ۰۱، ماژول ۰۸):

<div dir="ltr">

```bash
zcat host/clean/minigut_spiked_R1.fastq.gz | awk 'NR%4==1' \
  | sed -E 's/^@?(HUMAN_chr[0-9]+|NC_[0-9.]+).*/\1/' | sort | uniq -c
```

</div>

<div dir="ltr">

```text
   4725 HUMAN_chr1
  21018 NC_000913.3
  28827 NC_006347.1
```

</div>

| مبدأ | ورودی | ماند | رفت |
| :--- | ---: | ---: | ---: |
| باکتری (21018 + 28827) | 49,845 | **49,845** | ۰٪ |
| انسان chr21 (در مرجع) | 5,000 | **0** | ۱۰۰٪ |
| انسان chr1 (بیرون از مرجع) | 5,000 | **4,725** | تنها ۵٫۵٪ |

سه درس:
1. **هیچ رید باکتریایی به‌اشتباه نرفت.** (این را **ویژگی** یا *specificity* می‌نامند: ۱۰۰٪.)
2. **همه‌ی ریدهای chr21 رفتند**؛ حتی آن‌هایی که به چند جا می‌خوردند. (**حساسیت** یا *sensitivity* برای ناحیه‌ای که در مرجع هست: ۱۰۰٪.)
3. **مرجع ناقص = برداشتن ناقص.** ۹۴٫۵٪ ریدهای chr1 ماندند، چون آن ناحیه در شاخص نبود. ۲۷۵ جفتی که رفتند، به احتمال زیاد از تکرارهای پراکنده‌ی ژنوم انسان (مانند Alu و L1) بودند که نسخه‌ای در chr21 هم دارند. **در کار واقعی کل ژنوم انسان لازم است** (تمرین ۵: با افزودن chr1 به مرجع، همه‌ی ۱۰٬۰۰۰ جفت انسانی می‌روند).

<details>
<summary>✋ امتحان کن: حساسیت برداشتن میزبان برای <b>همه‌ی</b> ریدهای انسانی چند درصد است؟</summary>

‏(5000 + 275) / 10000 = **۵۲٫۸٪**. عدد ۱۰۰٪ تنها می‌گوید الگوریتم هم‌ترازی خوب کار کرده؛ برداشتن میزبان، به‌خاطر **مرجع**، نیمی از ریدهای انسانی را جا گذاشته است. تمرین ۱ همین را می‌پرسد.

</details>

> 📺 **فیلم:** *SAM flags explained*: https://www.youtube.com/watch?v=qm4NGV79t4o (Bioinformagician)
> 📄 **مرجع:** `samtools flags`: https://www.htslib.org/doc/samtools-flags.html

---

## ۸. گام ۶: MAPQ پایین، و چرا این‌جا مهم نیست

در بخش ۰۲ دیدید که برای فراخوانی واریانت، ریدهای با MAPQ پایین را کنار می‌گذارند. این‌جا چه؟ شمار رکوردهای نشسته‌ی chr21، با و بی مرز MAPQ ≥ ۳۰:

<div dir="ltr">

```bash
samtools view -F 4 host/bam/minigut_spiked.host.bam | grep -c '^HUMAN_chr21'
samtools view -F 4 -q 30 host/bam/minigut_spiked.host.bam | grep -c '^HUMAN_chr21'
```

</div>

<div dir="ltr">

```text
10000
3300
```

</div>

همه‌ی ۱۰٬۰۰۰ رید chr21 (۵۰۰۰ جفت) نشسته‌اند، ولی تنها **۳۳۰۰** تا MAPQ ≥ ۳۰ دارند. چرا؟ ناحیه‌ی chr21 ما **تکه‌های تکراری بزرگ** دارد: ریدی که از آن‌ها می‌آید، به دو جا به یک اندازه می‌خورد و Bowtie2 به آن MAPQ صفر یا یک می‌دهد (همان اپرون‌های rRNA در بخش ۰۲).

برای فراخوانی واریانت این رید دردسر است («از کدام نسخه آمده؟»). برای **برداشتن میزبان** فرقی نمی‌کند: پرسش «انسانی است؟» است، نه «کجای ژنوم انسان؟». پس **در برداشتن میزبان، روی MAPQ پالایش نکنید**؛ وگرنه ۶۷٪ ریدهای انسانی می‌ماندند.

---

## ۹. گام ۷: همه‌ی نمونه‌ها با یک اسکریپت

اسکریپت [`99_scripts_data/02_Host_Removal_Alignment/scripts/run_host_removal.sh`](../99_scripts_data/02_Host_Removal_Alignment/scripts/run_host_removal.sh) گام‌های ۱، ۲، ۴ و ۵ را برای هر نمونه انجام می‌دهد:

<div dir="ltr">

```bash
bash $S/run_host_removal.sh
IN=host/spiked bash $S/run_host_removal.sh minigut_spiked
```

</div>

<div dir="ltr">

```text
== minigut
   0.00% overall alignment rate   clean pairs: 49845
== minigut_sample2
   0.00% overall alignment rate   clean pairs: 24988
== minigut_spiked
   8.65% overall alignment rate   clean pairs: 54570
```

</div>

‏`IN=host/spiked bash …`: یک متغیر را **تنها برای همین اجرا** به اسکریپت می‌دهد (اسکریپت پوشه‌ی ورودی را از `IN` می‌خواند؛ پیش‌فرض `qc/trimmed`). ۵۴٬۵۷۰ = 49,845 باکتری + 4,725 chr1.

خروجی `host/clean/minigut_R*.fastq.gz` و `host/clean/minigut_sample2_R*.fastq.gz` ورودی ماژول ۰۳ است.

---

## ۱۰. سه اشتباه رایج

‏**۱. ‏`--un-conc` به‌جای `-f 12`.** گزینه‌ی رایج `bowtie2 --un-conc-gz` جفت‌هایی را بیرون می‌دهد که «concordant ننشسته‌اند». ولی جفتی که هر دو رید انسانی‌اش نشسته‌اند **با فاصله‌ی بیش از ۵۰۰ باز** (مرز پیش‌فرض `-X 500`) هم concordant نیست، پس می‌ماند. روی همین داده، `--un-conc` دو جفت chr21 و ۲۰۱ جفت chr1 بیشتر جا گذاشت (تمرین ۲).

**۲. پالایش MAPQ در برداشتن میزبان.** با `-q 30`، ‏۶۷٪ ریدهای انسانی در داده‌ی «پاک» می‌مانند (بخش ۸).

**۳. مرجع ناقص.** یک کروموزوم، یا GRCh38 بی توالی‌های alt و decoy. ریدهای نواحی غایب می‌مانند (بخش ۷: ۹۴٫۵٪ ریدهای chr1). کل ژنوم را به کار ببرید؛ بهتر از همه T2T-CHM13 که شکاف‌های GRCh38 را پر کرده است.

---

## 📘 برای کنجکاوها

- **ابزارهای آماده:** **Hostile** (روی T2T-CHM13، با پوشاندن نواحی‌ای از ژنوم انسان که با میکروب‌ها مشترک‌اند) و **KneadData** (bioBakery) همین منطق را با تنظیم‌های بهینه بسته‌بندی کرده‌اند. منطق این درس برای سنجیدن و گزارش آن‌ها لازم است.
- **مرجع بزرگ‌تر، خطر دیگر:** ژنوم انسان تکه‌هایی دارد که به توالی میکروبی می‌مانند (آلودگی‌های قدیمی اسمبلی، ژن‌های بسیار حفاظت‌شده). ریدهای باکتریایی هم ممکن است روی آن‌ها بنشینند و به‌اشتباه بروند. Hostile برای همین آن نواحی را می‌پوشاند.
- ‏**‏FM-index:** شاخص Bowtie2 بر پایه‌ی تبدیل Burrows–Wheeler است؛ فیلم‌های Ben Langmead در منابع آن را گام‌به‌گام نشان می‌دهند.

---

## جمع‌بندی

- برداشتن میزبان = هم‌ترازی روی ژنوم میزبان + نگه داشتن جفت‌هایی که **هر دو** رید ننشسته‌اند (`samtools view -f 12 -F 256` و `samtools fastq`).
- ‏`bowtie2-build` یک بار؛ `bowtie2 -x پیشوند -1 -2` برای هر نمونه؛ گزارش از stderr.
- کیفیت کار به **کامل بودن مرجع** وابسته است، نه به MAPQ.
- آزمایش کنترل‌شده با ریدهای مبدأدار، حساسیت و ویژگی را عددی می‌کند: این‌جا ویژگی ۱۰۰٪، و حساسیت ۱۰۰٪ برای ناحیه‌ای که در مرجع هست.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
bowtie2-build -q ref.fa index/prefix                       # once per reference
bowtie2 -p 4 --very-sensitive -x index/prefix -1 R1.fq.gz -2 R2.fq.gz 2> s.bowtie2.log \
  | samtools view -b -o s.unsorted.bam -                     # SAM -> BAM on the fly
samtools view -b -f 12 -F 256 s.unsorted.bam \
  | samtools fastq -1 clean_R1.fq.gz -2 clean_R2.fq.gz -0 /dev/null -s /dev/null -n -
samtools sort -o s.bam s.unsorted.bam && samtools index s.bam
samtools flagstat s.bam
samtools view -F 4 -q 30 s.bam | wc -l                       # mapped records with MAPQ >= 30
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| میزبان (*host*) | جاندار نمونه‌برداری‌شده (این‌جا انسان) |
| شاخص (*index*) | شکل فشرده و جست‌وجوپذیر ژنوم مرجع برای هم‌ترازی سریع |
| ‏concordant | دو رید جفت با جهت و فاصله‌ی درست نشسته‌اند |
| ‏mate | رید دیگر همان جفت |
| حساسیت (*sensitivity*) | سهم ریدهای انسانی که برداشته شدند |
| ویژگی (*specificity*) | سهم ریدهای میکروبی که دست‌نخورده ماندند |
| ‏spike-in | افزودن ریدهای معلوم به نمونه برای سنجش روش |
| ‏`/dev/null` | فایل ویژه‌ی لینوکس که هر چه در آن نوشته شود، دور ریخته می‌شود |

---

## منابع

**مستند و مقاله**
- Langmead B, Salzberg SL (2012). *Fast gapped-read alignment with Bowtie 2.* Nature Methods 9:357–359. https://doi.org/10.1038/nmeth.1923
- Danecek P, et al. (2021). *Twelve years of SAMtools and BCFtools.* GigaScience 10(2):giab008. https://doi.org/10.1093/gigascience/giab008
- Constantinides B, et al. (2023). *Hostile: accurate decontamination of microbial host sequences.* Bioinformatics 39(12):btad728. https://doi.org/10.1093/bioinformatics/btad728
- Nurk S, et al. (2022). *The complete sequence of a human genome.* Science 376:44–53. https://doi.org/10.1126/science.abj6987
- Bowtie2 manual: https://github.com/BenLangmead/bowtie2 · Pre-built indexes: https://benlangmead.github.io/aws-indexes/bowtie
- `samtools flags`: https://www.htslib.org/doc/samtools-flags.html · `samtools fastq`: https://www.htslib.org/doc/samtools-fasta.html
- wgsim: https://github.com/lh3/wgsim

**کتاب**
- ‏Compeau P, Pevzner P (2015). *Bioinformatics Algorithms: An Active Learning Approach*, 2nd ed. Active Learning Publishers. (فصل «Combinatorial Pattern Matching»: تبدیل Burrows-Wheeler)
- ‏Buffalo V (2015). *Bioinformatics Data Skills*. O'Reilly. (فصل ۱۱: داده‌ی هم‌ترازی)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Algorithms for DNA Sequencing* (Johns Hopkins University, Ben Langmead)؛ شاخص و هم‌ترازی ریدها: https://www.coursera.org/learn/dna-sequencing
- ‏edX: *Introduction to Linux* (The Linux Foundation). دوره‌ای ویژه‌ی برداشتن میزبان در edX نیافتیم؛ نزدیک‌ترین: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux
- ‏YouTube: *Burrows-Wheeler Transform* (Ben Langmead، سازنده‌ی Bowtie): https://www.youtube.com/watch?v=4n7NPk5lwbI
- YouTube: *FM Index* (Ben Langmead): https://www.youtube.com/watch?v=kvVGj5V65io
- YouTube: *SAM flags explained* (Bioinformagician): https://www.youtube.com/watch?v=qm4NGV79t4o

<sub>نشانی‌های YouTube و DOIها در 2026-10-13 وارسی شدند؛ نشانی Coursera در وارسی پایان دوره سنجیده می‌شود.</sub>

</div>
