<div dir="rtl">

# درس: فرمت‌های توالی؛ FASTA، FASTQ، کیفیت Phred، seqkit و samtools faidx

**بخش:** `02_BioLinux` · **ماژول:** `02_Sequence_Formats` · **پیش‌نیاز:** ماژول [Conda و Bioconda](../01_Conda_Bioconda/) · **زمان:** حدود ۷۵ دقیقه · **ابزار:** seqkit 2.13.0، samtools 1.20 · **آخرین اجرا:** 2026-10-20

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. ساختار دقیق FASTA و FASTQ را بشناسید و قاعده‌های آن‌ها را بگویید.
2. **کیفیت Phred** را از نویسه‌های خط چهارم FASTQ بخوانید.
3. با `seqkit` آمار، طول، GC و کیفیت فایل‌های توالی را بگیرید، ریدها را گزینش کنید، و یک الگو را روی هر دو رشته جستجو کنید.
4. با `samtools faidx` یک FASTA را ایندکس کنید و هر ناحیه‌ای (مانند یک ژن) را بی خواندن کل فایل بیرون بکشید.

**پیش از آغاز:**

<div dir="ltr">

```bash
conda activate bioinfo_course
cd ~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data      # داده‌ی بخش ۰۱
```

</div>

---

## ۱. داستان: کارهای بخش ۰۱، با یک دستور

در بخش لینوکس برای دانستن طول ژنوم، شمار ریدها یا درصد GC، چند دستور را با لوله به هم وصل کردیم (`grep -v | tr -d | wc -c`…). این کار برای یادگرفتن عالی بود، ولی برای کار روزمره کند است و جای خطا دارد. ابزارهای ویژه‌ی بیوانفورماتیک همین کارها را **با یک دستور** و بی خطاهای بی‌صدا انجام می‌دهند، چون فرمت را می‌شناسند. در این درس دو ابزار از آن‌ها را می‌بینیم:
- ‏**`seqkit`**: چاقوی سوئیسی FASTA و FASTQ.
- ‏**`samtools faidx`**: برداشتن هر ناحیه از یک FASTA بزرگ، در کسری از ثانیه.

پیش از ابزارها، خود فرمت‌ها را دقیق بشناسیم.

---

## ‏۲. FASTA، دقیق

<div dir="ltr">

```text
>NC_000913.3 Escherichia coli str. K-12 substr. MG1655, complete genome
AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGCTTCTGAACTG
GTTACCTGCCGTGAGTAAATTAAAATTTTATTGACTTAGGTCACTAAATACTTTAACCAATATAGGCATAGCGCACAGAC
…
```

</div>

| بخش | قاعده |
| :--- | :--- |
| خط عنوان | با `>` آغاز می‌شود |
| **شناسه** | نخستین واژه پس از `>`، تا نخستین فاصله: `NC_000913.3`. بیشتر ابزارها **تنها همین** را نگه می‌دارند |
| توضیح | بقیه‌ی خط عنوان (اختیاری) |
| توالی | یک یا چند خط پس از عنوان، تا عنوان بعدی. در ژنوم‌ها، خط‌ها در بسیاری از موارد ۶۰ یا ۸۰ حرف‌اند |
| چند توالی | یک فایل می‌تواند هزاران توالی داشته باشد؛ هر کدام با عنوان خودش |

پسوندهای رایج: `.fa`، `.fasta`، `.fna` (نوکلئوتید)، `.faa` (اسیدآمینه).

---

## ‏۳. FASTQ و کیفیت Phred

<div dir="ltr">

```text
@NC_006347.1_0/1                                ← ۱: نام رید (با @)
AACGTTGGCTCGTCTGACAAGCAAAGGTAAGAACAAAGG…        ← ۲: توالی
+                                               ← ۳: جداکننده (گاهی نام دوباره پس از +)
BBBBBFFFFFFFFFFFFFFFFFF/FFFFFFFFFFFFFFF…        ← ۴: کیفیت؛ هم‌طول خط ۲
```

</div>

**هر نویسه‌ی خط ۴، کیفیت بازِ روبه‌رویش در خط ۲ است.** کیفیت یعنی دستگاه چقدر مطمئن است که این باز را درست خوانده.

### نمره‌ی Phred
کیفیت با **نمره‌ی Phred** (Q) سنجیده می‌شود:

‏$$Q = -10 \log_{10} P_{خطا}$$

| Q | احتمال خطا | یعنی |
| :-: | :-: | :--- |
| 10 | ۱ در ۱۰ | ۹۰٪ درست |
| 20 | ۱ در ۱۰۰ | ۹۹٪ درست |
| 30 | ۱ در ۱٬۰۰۰ | ۹۹٫۹٪ درست |
| 40 | ۱ در ۱۰٬۰۰۰ | ۹۹٫۹۹٪ درست |

هر ۱۰ واحد Q، خطا را **ده برابر** کمتر می‌کند. Q30 را در بسیاری از موارد مرز «کیفیت خوب» می‌دانند.

### از نویسه به عدد: Phred+33
برای این‌که هر کیفیت **یک نویسه** شود، Q را با ۳۳ جمع می‌کنند و نویسه‌ای را که آن کد ASCII را دارد می‌نویسند. وارونه: **Q = کد نویسه − ۳۳**. کد ASCII هر نویسه را با `printf` می‌شود دید (نقل‌قول تکی پیش از نویسه یعنی «کد آن را بده»):

<div dir="ltr">

```bash
printf '%d\n' "'F"
```

</div>

<div dir="ltr">

```text
70
```

</div>

پس `F` = ۷۰ − ۳۳ = **Q37**. جدول نویسه‌های رایج (همه با همین فرمان به دست آمدند):

| نویسه | کد ASCII | Q | احتمال خطا |
| :-: | :-: | :-: | :-: |
| `!` | 33 | 0 | ۱ (حدس محض) |
| `+` | 43 | 10 | ۱ در ۱۰ |
| `/` | 47 | 14 | نزدیک ۱ در ۲۵ |
| `5` | 53 | 20 | ۱ در ۱۰۰ |
| `?` | 63 | 30 | ۱ در ۱٬۰۰۰ |
| `@` | 64 | 31 | نزدیک ۱ در ۱٬۲۶۰ |
| `B` | 66 | 33 | نزدیک ۱ در ۲٬۰۰۰ |
| `F` | 70 | 37 | نزدیک ۱ در ۵٬۰۰۰ |
| `I` | 73 | 40 | ۱ در ۱۰٬۰۰۰ |

**پس خط کیفیت رید بالا (`BBBBBFFFF…/FFF…`) یعنی:** پنج باز نخست Q33، بیشتر بازها Q37، و یک باز (`/`) با Q14، یعنی جایی که دستگاه کمتر مطمئن بوده است.

<details>
<summary>✋ <b>امتحان کن:</b> چرا <code>grep -c '^@'</code> برای شمردن ریدها خطرناک است؟ (جدول بالا را نگاه کنید.)</summary>

نویسه‌ی `@` یعنی Q31، کیفیتی بسیار رایج. پس **خط کیفیت** هم می‌تواند با `@` آغاز شود، و `grep` آن را هم یک «رید» می‌شمارد. روش درست: شمار خط‌ها ÷ ۴ (بخش ۰۱)، یا `seqkit stats` (بخش ۴ همین درس).
</details>

> 📺 **فیلم:** *Understanding Phred Scores for FASTQ format*: https://www.youtube.com/watch?v=kgTf8-odrnY
> 📄 **مرجع:** Cock PJA, et al. (2010). *The Sanger FASTQ file format…* Nucleic Acids Res 38:1767–1771. https://doi.org/10.1093/nar/gkp1137

---

## ‏۴. `seqkit stats`: کارت شناسایی فایل‌ها

<div dir="ltr">

```bash
seqkit stats ecoli_k12.fna host_chr21_region.fa sample.fasta
```

</div>

<div dir="ltr">

```text
file                  format  type     num_seqs    sum_len    min_len    avg_len    max_len
ecoli_k12.fna         FASTA   DNA             1  4,641,652  4,641,652  4,641,652  4,641,652
host_chr21_region.fa  FASTA   DNA             1    500,000    500,000    500,000    500,000
sample.fasta          FASTA   Protein         1         14         14         14         14
```

</div>

### کالبدشکافی

| بخش دستور | یعنی |
| :--- | :--- |
| `seqkit` | نام ابزار؛ کارهایش زیرفرمان‌اند (`stats`، `seq`، `grep`…) |
| `stats` | زیرفرمان: آمار خلاصه |
| فایل‌ها | یک یا چند FASTA یا FASTQ، ساده یا `.gz` |

| ستون خروجی | یعنی |
| :--- | :--- |
| `format` / `type` | فرمت و نوع توالی را **خودش** تشخیص داد (DNA یا Protein) |
| `num_seqs` | شمار توالی‌ها (یا ریدها) |
| `sum_len` | جمع طول‌ها |
| `min_len` / `avg_len` / `max_len` | کوتاه‌ترین، میانگین و بلندترین |

**این خروجی یعنی:** همان عددهایی که در بخش ۰۱ با چند دستور به دست آوردیم (طول ژنوم ۴٬۶۴۱٬۶۵۲، تکه‌ی ۵۰۰ کیلوبازی، پروتئین ۱۴ اسیدآمینه‌ای)، این بار با یک دستور و برای سه فایل با هم. `seqkit` خط‌های چندگانه‌ی FASTA را خودش درست می‌چسباند.

### روی FASTQ: همه‌ی چهار فایل

<div dir="ltr">

```bash
seqkit stats fastq/*.fastq.gz
```

</div>

<div dir="ltr">

```text
file                               format  type  num_seqs    sum_len  min_len  avg_len  max_len
fastq/minigut_R1.fastq.gz          FASTQ   DNA     50,000  6,300,000      126      126      126
fastq/minigut_R2.fastq.gz          FASTQ   DNA     50,000  6,300,000      126      126      126
fastq/minigut_sample2_R1.fastq.gz  FASTQ   DNA     24,993  3,773,943      151      151      151
fastq/minigut_sample2_R2.fastq.gz  FASTQ   DNA     24,993  3,773,943      151      151      151
```

</div>

همان جدول ماژول ۰۹ لینوکس (حلقه + `zcat` + `awk`)، با یک دستور.

### ‏`-a`: آمار کیفیت هم

<div dir="ltr">

```bash
seqkit stats -a -T fastq/minigut_R1.fastq.gz
```

</div>

ستون‌های پایانی خروجی:

<div dir="ltr">

```text
Q20(%)	Q30(%)	AvgQual	GC(%)	sum_n
96	92	27.24	46.79	0
```

</div>

| گزینه یا ستون | یعنی |
| :--- | :--- |
| `-a` | همه‌ی آمارها (*all*)، از جمله کیفیت |
| `-T` | خروجی جدولی با Tab (برای `cut` و `awk`) |
| `Q20(%)` / `Q30(%)` | درصد بازهایی که کیفیت ≥ ۲۰ / ≥ ۳۰ دارند |
| `GC(%)` | درصد GC؛ همان ۴۶٫۷۹ ماژول ۰۹ لینوکس ✓ |
| `sum_n` | شمار بازهای `N` |

**۹۲٪ بازها Q30 یا بالاتر دارند**؛ داده‌ی خوبی است.

---

## ‏۵. `seqkit fx2tab`: یک ردیف برای هر توالی

<div dir="ltr">

```bash
seqkit fx2tab -n -l -g ecoli_k12.fna host_chr21_region.fa
```

</div>

<div dir="ltr">

```text
NC_000913.3 Escherichia coli str. K-12 substr. MG1655, complete genome	4641652	50.79
chr21part	500000	40.05
```

</div>

| گزینه | یعنی |
| :--- | :--- |
| `fx2tab` | ‏FASTA/FASTQ را به **جدول** (یک ردیف برای هر توالی) تبدیل کن |
| `-n` | تنها نام، نه خود توالی |
| `-l` | ستون طول |
| `-g` | ستون درصد GC |

‏**GC ژنوم *E. coli* ۵۰٫۷۹٪**، همان عدد ماژول ۰۸ لینوکس. برای کروموزوم ۲۱، **۴۰٫۰۵٪**: `seqkit` بازهای `N` را خودش کنار گذاشت (ماژول ۰۸، تمرین ۱).

برای FASTQ، `-q` میانگین کیفیت هر رید را می‌دهد:

<div dir="ltr">

```bash
seqkit fx2tab -n -q fastq/minigut_R1.fastq.gz | head -n 3
```

</div>

<div dir="ltr">

```text
NC_006347.1_0/1	30.44
NC_006347.1_1/1	28.17
NC_006347.1_2/1	30.37
```

</div>

---

## ۶. گزینش و جستجو

### ‏`seqkit grep`: ریدهای دلخواه
ریدهای *E. coli* (نامشان با `NC_000913` آغاز می‌شود) را از نمونه‌ی `minigut` بیرون بکشیم:

<div dir="ltr">

```bash
seqkit grep -r -p '^NC_000913' fastq/minigut_R1.fastq.gz | seqkit stats -T
```

</div>

<div dir="ltr">

```text
file	format	type	num_seqs	sum_len	min_len	avg_len	max_len
-	FASTQ	DNA	21088	2657088	126	126.0	126
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `grep` | زیرفرمان جستجو روی **نام** توالی‌ها (نه مانند `grep` لینوکس روی هر خط) |
| `-r` | الگو یک عبارت منظم است (*regex*) |
| `-p '^NC_000913'` | الگو (*pattern*): نامی که با `NC_000913` آغاز شود |
| `\| seqkit stats` | خروجی (FASTQ کامل، ۴ خط برای هر رید) را بی‌درنگ بشمار؛ `-` یعنی «ورودی از لوله» |

**۲۱٬۰۸۸ رید**، همان عدد ماژول ۰۵ لینوکس. ولی این بار خروجی **ریدهای کامل** است (نام، توالی، +، کیفیت)، که می‌شود با `-o ecoli_reads.fq.gz` در یک فایل تازه ریخت و به ابزارهای دیگر داد.

### ‏`seqkit locate`: جستجوی الگو روی **هر دو** رشته

<div dir="ltr">

```bash
seqkit locate -p GAATTC ecoli_k12.fna | head -n 3
```

</div>

<div dir="ltr">

```text
seqID	patternName	pattern	strand	start	end	matched
NC_000913.3	GAATTC	gaattc	+	3842	3847	gaattc
NC_000913.3	GAATTC	gaattc	+	12889	12894	gaattc
```

</div>

هر ردیف یک رخداد است، با رشته (`strand`) و جای آغاز و پایان. شمار رخدادها:

<div dir="ltr">

```bash
seqkit locate -p GAATTC ecoli_k12.fna | tail -n +2 | wc -l
seqkit locate -P -p GAATTC ecoli_k12.fna | tail -n +2 | wc -l
```

</div>

<div dir="ltr">

```text
1292
646
```

</div>

- ‏`tail -n +2` یعنی «از خط ۲ تا پایان»: خط عنوان ستون‌ها را کنار می‌گذارد.
- بی `-P`، هر دو رشته جستجو شد: **۱٬۲۹۲**. با `-P` (*only positive strand*) تنها رشته‌ی مثبت: **۶۴۶**، دقیقاً همان عدد درستی که در ماژول ۰۸ لینوکس با `tr -d '\n'` به دست آوردیم. ✓
- چرا ۱٬۲۹۲ دقیقاً دو برابر است؟ `GAATTC` **پالیندروم** است (مکمل معکوسش خودش است)، پس هر جایگاه روی هر دو رشته یک بار دیده می‌شود.

‏`seqkit` خط‌های FASTA را خودش می‌چسباند؛ پس خطای «مرز خط» ماژول ۰۵ لینوکس را ندارد.

<details>
<summary>✋ <b>امتحان کن:</b> رشته‌ی مثبت ژنوم چند <code>ATG</code> دارد؟ با عدد ماژول ۰۸ لینوکس بسنجید.</summary>

<div dir="ltr">

```bash
seqkit locate -P -p ATG ecoli_k12.fna | tail -n +2 | wc -l
```

</div>

پاسخ: **76282**، دقیقاً همان عدد `tr -d '\n' | grep -o ATG | wc -l`. ✓
</details>

> 📺 **فیلم:** *Techniques to manipulate FASTQ files (2)*: https://www.youtube.com/watch?v=wWm7hEqbbaA (SeqKit، seqtk)
> 📄 **مرجع:** Shen W, et al. (2016). *SeqKit.* PLoS ONE 11:e0163962. https://doi.org/10.1371/journal.pone.0163962

---

## ‏۷. `samtools faidx`: هر ناحیه، بی‌درنگ

برای برداشتن یک ژن از ژنوم، لازم نیست کل فایل را بخوانید. نخست یک **ایندکس** می‌سازیم:

<div dir="ltr">

```bash
samtools faidx ecoli_k12.fna
cat ecoli_k12.fna.fai
```

</div>

<div dir="ltr">

```text
NC_000913.3	4641652	72	80	81
```

</div>

**این خروجی یعنی:** فایل تازه‌ی `ecoli_k12.fna.fai` (ایندکس) برای هر توالی یک ردیف دارد:

| ستون | مقدار | یعنی |
| :-: | :--- | :--- |
| 1 | `NC_000913.3` | نام توالی |
| 2 | `4641652` | طول |
| 3 | `72` | جای نخستین باز در فایل (بایت). خط عنوان ۷۱ نویسه + ۱ پایان‌خط = ۷۲ (ماژول ۰۳ لینوکس) |
| 4 | `80` | باز در هر خط |
| 5 | `81` | بایت در هر خط (۸۰ + پایان‌خط) |

با این پنج عدد، `samtools` بی خواندن کل فایل حساب می‌کند هر باز کجای فایل است و مستقیم به آن‌جا می‌پرد.

### بیرون کشیدن یک ناحیه
ناحیه به شکل **`نام:آغاز-پایان`** نوشته می‌شود (شماره‌گذاری از ۱، هر دو سر جزو ناحیه؛ مانند GFF):

<div dir="ltr">

```bash
samtools faidx ecoli_k12.fna NC_000913.3:4181245-4181304
```

</div>

<div dir="ltr">

```text
>NC_000913.3:4181245-4181304
ATGGTTTACTCCTATACCGAGAAAAAACGTATTCGTAAGGATTTTGGTAAACGTCCACAA
```

</div>

همان ۶۰ نوکلئوتید نخست rpoB در بخش ۰۰. کل ژن:

<div dir="ltr">

```bash
samtools faidx ecoli_k12.fna NC_000913.3:4181245-4185273 > rpoB.fa
seqkit stats rpoB.fa
```

</div>

‏`rpoB.fa` یک FASTA با **۴٬۰۲۹ باز** است، همان طول ژن rpoB.

### ژن روی رشته‌ی منفی: `-i`
‏gyrA روی رشته‌ی **منفی** است (۲٬۳۳۶٬۷۹۳ تا ۲٬۳۳۹٬۴۲۰). با `-i` (*reverse complement*) مکمل معکوس را می‌گیریم، یعنی خود ژن، از کدون آغاز:

<div dir="ltr">

```bash
samtools faidx -i ecoli_k12.fna NC_000913.3:2339391-2339420
```

</div>

<div dir="ltr">

```text
>NC_000913.3:2339391-2339420/rc
ATGAGCGACCTTGCGAGAGAAATTACACCG
```

</div>

‏**`ATGAGCGACCTTGCG…`**: همان آغاز gyrA که در بخش ۰۰ (تمرین ترجمه) و ماژول ۰۸ لینوکس دیدیم. ۳۰ باز **پایانی** ناحیه‌ی ژنومی، پس از مکمل معکوس، ۳۰ باز **آغازین** ژن‌اند، چون ژن از سر بزرگ‌تر خوانده می‌شود.

---

## ۸. سه اشتباه رایج

| اشتباه | چه می‌شود | به جایش |
| :--- | :--- | :--- |
| شمردن ریدها با `grep -c '^@'` | `@` در خط کیفیت هم هست (Q31) و شمار نادرست می‌شود | ‏`seqkit stats` یا خط‌ها ÷ ۴ |
| نام ناحیه بی شناسه‌ی درست (`samtools faidx ecoli_k12.fna chr:1-100`) | خطا یا خروجی خالی، چون نام توالی `NC_000913.3` است، نه `chr` | نام را از ستون یکم `.fai` بردارید |
| فراموش کردن `-i` برای ژن رشته‌ی منفی | توالی **وارونه و مکمل** ژن به دست می‌آید؛ ترجمه‌اش بی‌معناست | برای ژن‌های `-`: `samtools faidx -i` |

---

## ۹. جمع‌بندی

- ‏FASTA: عنوان `>` + توالی (چندخطی)؛ شناسه = نخستین واژه‌ی عنوان.
- ‏FASTQ: چهار خط؛ کیفیت هر باز = کد ASCII نویسه − ۳۳ (Phred+33)؛ Q30 = یک خطا در هزار.
- ‏`seqkit stats` (`-a` برای کیفیت و GC)، `fx2tab -n -l -g -q`، `grep -r -p` برای گزینش، `locate -p` (با `-P` تنها رشته‌ی مثبت).
- ‏`samtools faidx file` ایندکس می‌سازد؛ `samtools faidx file نام:آغاز-پایان` ناحیه را می‌دهد؛ `-i` مکمل معکوس.

---

## کارت دستورهای این درس

| می‌خواهم… | دستور |
| :--- | :--- |
| آمار چند فایل | `seqkit stats *.fa` |
| آمار با کیفیت و GC | `seqkit stats -a -T file.fastq.gz` |
| طول و GC هر توالی | `seqkit fx2tab -n -l -g file.fa` |
| میانگین کیفیت هر رید | `seqkit fx2tab -n -q file.fastq.gz` |
| ریدهایی با نام دلخواه | `seqkit grep -r -p '^NAME' in.fq.gz -o out.fq.gz` |
| جای یک الگو (رشته‌ی مثبت) | `seqkit locate -P -p GAATTC file.fa` |
| ‏FASTQ به FASTA | `seqkit fq2fa in.fq.gz > out.fa` |
| ایندکس FASTA | `samtools faidx file.fa` |
| یک ناحیه | `samtools faidx file.fa NC_000913.3:4181245-4185273` |
| ناحیه، مکمل معکوس | `samtools faidx -i file.fa name:start-end` |
| کد ASCII یک نویسه | `printf '%d\n' "'F"` |

---

<details>
<summary>📘 <b>برای کنجکاوها (اختیاری):</b> چرا میانگین کیفیت seqkit کمتر از میانگین ساده است؟</summary>

رید یکم `minigut_R1` این نویسه‌های کیفیت را دارد: ۱۱۲ تا `F` (Q37)، ۸ تا `B` (Q33)، ۴ تا `<` (Q27) و ۲ تا `/` (Q14). میانگین **ساده‌ی** این عددها **۳۶٫۰۶** است، ولی `seqkit fx2tab -q` عدد **۳۰٫۴۴** را داد.

دلیل: Q یک مقیاس **لگاریتمی** است. `seqkit` (مانند بسیاری از ابزارها) نخست هر Q را به **احتمال خطا** برمی‌گرداند، میانگین احتمال‌ها را می‌گیرد، و آن را دوباره به Q تبدیل می‌کند. دو باز با Q14 (هر کدام نزدیک به ۴٪ خطا) سهم بسیار بیشتری از خطای کل رید دارند تا ۱۱۲ باز با Q37 (هر کدام ۰٫۰۲٪). میانگین ساده‌ی Qها خطا را **کمتر از واقع** نشان می‌دهد. پس هنگام سنجش «میانگین کیفیت» دو ابزار، ببینید هر کدام چگونه آن را حساب کرده است.
</details>

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| شناسه (identifier) | نخستین واژه‌ی خط عنوان FASTA/FASTQ |
| نمره‌ی Phred (Q) | ‏Q = −۱۰ log₁₀(احتمال خطا)؛ Q30 = یک خطا در هزار |
| Phred+33 | نوشتن Q به شکل نویسه‌ای با کد ASCII برابر Q + ۳۳ |
| ASCII | جدولی که به هر نویسه یک عدد می‌دهد (`F` = ۷۰) |
| ایندکس (`.fai`) | فایل کوچکی که جای هر توالی را در FASTA نگه می‌دارد تا دسترسی مستقیم شدنی شود |
| ناحیه (region) | `نام:آغاز-پایان`، شماره‌گذاری از ۱ و دوسر بسته |
| پالیندروم (palindrome) | توالی‌ای که مکمل معکوسش خودش است (`GAATTC`) |

---

## منابع

### مقاله و راهنمای رسمی
- Shen W, et al. (2016). SeqKit: A Cross-Platform and Ultrafast Toolkit for FASTA/Q File Manipulation. *PLoS ONE* 11(10):e0163962. https://doi.org/10.1371/journal.pone.0163962
- راهنمای seqkit: https://bioinf.shenwei.me/seqkit/
- Cock PJA, et al. (2010). The Sanger FASTQ file format for sequences with quality scores, and the Solexa/Illumina FASTQ variants. *Nucleic Acids Res.* 38(6):1767–1771. https://doi.org/10.1093/nar/gkp1137
- راهنمای samtools faidx: https://www.htslib.org/doc/samtools-faidx.html

### کتاب
- ‏Buffalo V (2015). *Bioinformatics Data Skills*. O'Reilly. (فصل ۱۰: کار با داده‌ی توالی؛ FASTA، FASTQ و کیفیت)

### فیلم‌های آموزشی

**Coursera:**
- ‏Johns Hopkins University — *Command Line Tools for Genomic Data Science*. بخش فرمت‌های توالی: https://www.coursera.org/learn/genomic-tools

**edX:**
- ‏IsraelX — *Essentials of Genomics and Biomedical Informatics*. بخش توالی‌یابی نسل جدید و فایل‌های آن: https://www.edx.org/learn/medicine/israelx-essentials-of-genomics-and-biomedical-informatics

**YouTube:**
- GenoMediCon — *Essential Genomic File Formats for Beginners: FASTA, FASTQ, SAM/BAM, and VCF Explained*: https://www.youtube.com/watch?v=BaVBesblyxw

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. همه‌ی دستورها در 2026-10-20 با seqkit 2.13.0 و samtools 1.20 اجرا شدند. `seqkit` پیام‌های پیشرفت و `[INFO]` را در stderr می‌نویسد؛ آن‌ها را از خروجی‌های بالا برداشته‌ایم.

</div>
