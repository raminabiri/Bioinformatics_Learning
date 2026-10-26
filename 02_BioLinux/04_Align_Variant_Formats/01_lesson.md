<div dir="rtl">

# درس: فرمت‌های هم‌ترازی و واریانت؛ SAM/BAM و VCF

**بخش:** `02_BioLinux` · **ماژول:** `04_Align_Variant_Formats` · **پیش‌نیاز:** ماژول [فرمت‌های آنوتیشن](../03_Annotation_Formats/) · **زمان:** حدود ۹۰ دقیقه · **ابزار:** samtools 1.20، bcftools 1.21 · **آخرین اجرا:** 2026-10-20

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. بگویید هم‌ترازی (alignment) ریدها با ژنوم مرجع چیست و خروجی‌اش (SAM/BAM) چه دارد.
2. ۱۱ ستون SAM را بخوانید، به‌ویژه **FLAG**، **MAPQ** و **CIGAR**.
3. با `samtools` ریدها را بشمارید، گزینش کنید، یک ناحیه را ببینید و پوشش (عمق) را بسنجید.
4. ساختار VCF را بشناسید و با `bcftools` واریانت‌ها را ببینید، بشمارید و گزینش کنید.
5. یک جهش مقاومت به ریفامپیسین را در داده‌ی واقعی‌نما پیدا کنید و به کدون آن برسید.

**پیش از آغاز:**

<div dir="ltr">

```bash
conda activate bioinfo_course
cd ~/Bioinformatics_Learning-main/02_BioLinux/99_scripts_data/04_Align_Variant_Formats/data
G=~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data      # ژنوم و GFF بخش ۰۱
ls
```

</div>

<div dir="ltr">

```text
bowtie2.log  resistant.bam  resistant.bam.bai  resistant.vcf.gz  resistant.vcf.gz.tbi
```

</div>

---

## ۱. داستان: سویه‌ی بیمار، بالاخره

از بخش ۰۰ با یک فرضیه همراهیم: سویه‌ای از *E. coli* به ریفامپیسین مقاوم است، شاید چون ژن rpoB آن جهش دارد. در این پوشه، داده‌ی **همان سویه** است (شبیه‌سازی‌شده، ولی با همان روندی که داده‌ی واقعی دارد):

1. ‏DNA سویه توالی‌یابی شده و **۳٬۰۰۰ جفت رید** ۱۵۰ بازی از ناحیه‌ی ۳۰ کیلوبازی پیرامون rpoB به دست آمده است.
2. ریدها با یک برنامه‌ی **هم‌ترازی** (bowtie2؛ در بخش ۰۶ یاد می‌گیرید) روی ژنوم **مرجع** *E. coli* K-12 گذاشته شده‌اند: برای هر رید، جایی از ژنوم که بیشترین همانندی را دارد پیدا شده است. نتیجه: `resistant.bam`.
3. با یک برنامه‌ی **فراخوانی واریانت** (bcftools)، جاهایی که ریدها با مرجع فرق دارند پیدا شده‌اند. نتیجه: `resistant.vcf.gz`.

پرسش این درس: **آیا rpoB این سویه جهش دارد؟ کدام کدون؟**

(چگونگی ساختن این دو فایل در [make_examples.sh](../99_scripts_data/04_Align_Variant_Formats/scripts/make_examples.sh) آمده است. لازم نیست اجرایش کنید؛ ابزارهایش را در بخش ۰۶ یاد می‌گیرید.)

---

## ۲. هم‌ترازی چیست؟ (یادآوری از بخش ۰۰)

در ماژول ابزارهای وب (بخش ۰۰) دو پروتئین را **هم‌تراز** کردیم. این‌جا همان کار با **میلیون‌ها رید کوتاه** و **یک ژنوم بزرگ** انجام می‌شود:

<div dir="ltr">

```text
مرجع:  …ACCCGCTGTCTGAGATTACGCACAAACGTCGTATCTCCGC…
رید:              GTCTGAGATTACGTACAAACGTCGTA
                              ↑
                    یک جای ناهمسان: C در مرجع، T در رید
```

</div>

اگر ریدهای فراوانی روی یک جا **همان** ناهمسانی را داشته باشند، به احتمال زیاد یک **جهش واقعی** است، نه خطای دستگاه. فایل SAM/BAM جای هر رید و چگونگی هم‌ترازی‌اش را نگه می‌دارد.

> 📺 **فیلم:** *Aligning Sequencing Reads to Reference*: https://www.youtube.com/watch?v=fSnAeYHnPCw
> 📄 **مرجع:** Li H, Homer N (2010). *A survey of sequence alignment algorithms for next-generation sequencing.* Brief Bioinform 11:473–483. https://doi.org/10.1093/bib/bbq015

---

## ‏۳. SAM و BAM

- ‏**SAM** (*Sequence Alignment/Map*): فرمت متنی؛ هر خط یک رید.
- ‏**BAM**: همان SAM، **فشرده و دودویی** (binary)؛ چندین برابر کوچک‌تر و تندتر. با `cat` خوانده نمی‌شود؛ `samtools view` آن را به SAM برمی‌گرداند.
- ‏**`.bai`**: ایندکس BAM (مانند `.fai` برای FASTA)؛ برای پرش مستقیم به یک ناحیه. BAM باید **مرتب** (بر پایه‌ی جای ریدها) باشد تا ایندکس شود.

### سرآیند

<div dir="ltr">

```bash
samtools view -H resistant.bam
```

</div>

<div dir="ltr">

```text
@HD	VN:1.5	SO:coordinate
@SQ	SN:NC_000913.3	LN:4641652
@RG	ID:resistant	SM:resistant
@PG	ID:bowtie2	PN:bowtie2	VN:2.5.4	CL:"…bowtie2-align-s --wrapper basic-0 -p 4 -x … "
@PG	ID:samtools	PN:samtools	PP:bowtie2	VN:1.20	CL:samtools sort -o resistant.bam -
```

</div>

(خط‌های بلند را کوتاه کرده‌ایم.)

| خط | یعنی |
| :--- | :--- |
| `@HD … SO:coordinate` | نسخه‌ی فرمت؛ ریدها بر پایه‌ی **جا** مرتب‌اند |
| `@SQ SN:… LN:…` | نام و طول توالی مرجع |
| `@RG … SM:resistant` | «گروه رید»: نام نمونه |
| `@PG` | **تاریخچه‌ی برنامه‌ها**: کدام برنامه، کدام نسخه، با چه دستوری (`CL:`) |

‏**`@PG` یک دفترچه‌ی دوباره‌پذیری خودکار است**: هر کس این BAM را بگیرد، می‌بیند با bowtie2 2.5.4 ساخته و با samtools 1.20 مرتب شده. هرگز سرآیند را دور نریزید. (`samtools view` خودش هم یک خط `@PG` تازه برای همین فرمان می‌افزاید.)

### بدنه: ۱۱ ستون

<div dir="ltr">

```bash
samtools view resistant.bam | head -n 2 | cut -f1-9
```

</div>

<div dir="ltr">

```text
resistant_region_9_313_0:0:0_1:0:0_a4c	163	NC_000913.3	227127	1	150M	=	227282	305
resistant_region_70_338_3:0:0_0:0:0_415	163	NC_000913.3	227188	1	150M	=	227307	269
```

</div>

| ستون | نام | در رید یکم | یعنی |
| :-: | :--- | :--- | :--- |
| 1 | QNAME | `resistant_region_9_…` | نام رید |
| 2 | **FLAG** | `163` | یک عدد که چند ویژگی «بله/نه» را با هم نگه می‌دارد (پایین) |
| 3 | RNAME | `NC_000913.3` | روی کدام توالی مرجع |
| 4 | **POS** | `227127` | جای نخستین باز رید (**شماره از ۱**، مانند GFF) |
| 5 | **MAPQ** | `1` | اطمینان از جای رید (پایین) |
| 6 | **CIGAR** | `150M` | چگونگی هم‌ترازی (پایین) |
| 7 | RNEXT | `=` | جفتش روی **همان** توالی است |
| 8 | PNEXT | `227282` | جای جفتش |
| 9 | TLEN | `305` | طول قطعه‌ی DNA (از آغاز یک رید تا پایان جفتش) |
| 10 | SEQ | `GCGTAGTCGA…` | توالی رید |
| 11 | QUAL | … | کیفیت (مانند FASTQ) |

پس از این ۱۱ ستون، **برچسب‌های اختیاری** می‌آیند، به شکل `نام:نوع:مقدار`. برای رید یکم:

<div dir="ltr">

```text
AS:i:0	XS:i:0	XN:i:0	XM:i:0	XO:i:0	XG:i:0	NM:i:0	MD:Z:150	YS:i:-4	YT:Z:CP	RG:Z:resistant
```

</div>

برای نمونه `NM:i:0` یعنی رید با مرجع **صفر** تفاوت دارد، و `AS` و `XS` امتیاز بهترین و دومین جای ممکن‌اند. (برچسب‌ها را هر برنامه‌ی هم‌ترازی به شیوه‌ی خودش می‌نویسد.)

**صبر کنید!** این ریدها از ناحیه‌ی rpoB (۴٫۱۷ تا ۴٫۲ میلیون) آمده بودند، ولی جایشان **۲۲۷٬۱۲۷** است و MAPQ آن‌ها **۱**. چرا؟ پاسخ در بخش «MAPQ» است.

### ‏FLAG: چند پاسخ «بله/نه» در یک عدد

‏`samtools flags` معنای یک FLAG را می‌گوید:

<div dir="ltr">

```bash
samtools flags 163
samtools flags 99
```

</div>

<div dir="ltr">

```text
0xa3	163	PAIRED,PROPER_PAIR,MREVERSE,READ2
0x63	99	PAIRED,PROPER_PAIR,MREVERSE,READ1
```

</div>

| نام | یعنی |
| :--- | :--- |
| `PAIRED` | رید یکی از یک جفت است (paired-end) |
| `PROPER_PAIR` | دو رید جفت با فاصله و جهت درست هم‌تراز شده‌اند |
| `REVERSE` / `MREVERSE` | خود رید / جفتش روی رشته‌ی منفی هم‌تراز شده |
| `READ1` / `READ2` | این رید R1 است یا R2 |

‏FLAG جمع چند عدد (۱، ۲، ۴، ۸، ۱۶…) است که هر کدام یک ویژگی‌اند؛ `samtools flags` این جمع را برایتان باز می‌کند. در این BAM تنها چهار FLAG هست:

<div dir="ltr">

```bash
samtools view resistant.bam | cut -f2 | sort | uniq -c | sort -rn
```

</div>

<div dir="ltr">

```text
   1520 83
   1520 163
   1480 99
   1480 147
```

</div>

همه‌ی آن‌ها `PROPER_PAIR`‌اند: هر ۶٬۰۰۰ رید با جفتش درست هم‌تراز شده است.

### ‏MAPQ: «چقدر مطمئنم که این رید از این‌جا آمده؟»

<div dir="ltr">

```bash
samtools view resistant.bam | cut -f5 | sort -n | uniq -c | sort -rn | head -n 4
```

</div>

<div dir="ltr">

```text
   5498 42
    314 1
    134 6
     20 30
```

</div>

‏**MAPQ** هم مانند کیفیت Phred است: MAPQ ۴۲ (بیشینه در bowtie2) یعنی جای رید کمابیش قطعی است؛ MAPQ ۰ یا ۱ یعنی رید **به چند جای ژنوم به یک اندازه می‌خورد** و برنامه یکی را **تصادفی** برگزیده است.

۳۱۴ رید MAPQ ۱ دارند. کجا گذاشته شده‌اند؟

<div dir="ltr">

```bash
samtools view resistant.bam | awk '$5<=1' | cut -f4 | awk '{print int($1/100000)*100000}' | sort -n | uniq -c
```

</div>

<div dir="ltr">

```text
     24 200000
     54 2700000
     50 3400000
      6 3900000
     26 4000000
     90 4100000
     64 4200000
```

</div>

**این خروجی یعنی:** این ریدها در **هفت** ناحیه‌ی گوناگون پخش شده‌اند. ناحیه‌ی ۳۰ کیلوبازی ما بخشی از یک **اپرون rRNA** (rrnB) را دارد، و *E. coli* هفت اپرون rRNA کمابیش یکسان دارد. ریدهای rRNA به هر هفت جا به یک اندازه می‌خورند، پس برنامه هر کدام را تصادفی در یکی گذاشت. (`int($1/100000)*100000` جای هر رید را به ۱۰۰ هزار پایین گرد می‌کند تا بشود شمرد.) **درس:** برای فراخوانی واریانت، ریدهای MAPQ پایین را کنار می‌گذارند:

<div dir="ltr">

```bash
samtools view -c resistant.bam
samtools view -c -q 30 resistant.bam
```

</div>

<div dir="ltr">

```text
6000
5532
```

</div>

‏`-c` (*count*) تنها می‌شمارد؛ `-q 30` تنها ریدهای MAPQ ≥ ۳۰ را نگه می‌دارد: **۵٬۵۳۲** رید.

### ‏CIGAR: رید چگونه روی مرجع نشسته است؟

<div dir="ltr">

```bash
samtools view resistant.bam | cut -f6 | sort | uniq -c | sort -rn | head -n 3
```

</div>

<div dir="ltr">

```text
   5962 150M
      2 9M1D141M
      2 95M1D55M
```

</div>

‏CIGAR یک «دستور» کوتاه است: عدد + حرف، پشت سر هم.

| حرف | یعنی |
| :-: | :--- |
| `M` | هم‌تراز (یکسان **یا** ناهمسان؛ هر دو `M`اند) |
| `I` | **افزایش**: این بازها در رید هستند، در مرجع نه |
| `D` | **کاهش** (deletion): این بازها در مرجع هستند، در رید نه |
| `S` | بریده‌شده (soft-clip): بخشی از رید که هم‌تراز نشد |

- ‏`150M`: همه‌ی ۱۵۰ باز پشت سر هم هم‌ترازند.
- ‏`95M1D55M`: ۹۵ باز هم‌تراز، سپس **۱ باز از مرجع در رید نیست**، سپس ۵۵ باز دیگر. این ریدها روی **کاهش یک‌بازی** این سویه نشسته‌اند (بخش ۵).

> 📺 **فیلم:** *Understanding Bioinformatics File Formats: SAM/BAM*: https://www.youtube.com/watch?v=vh6l9aPFUgU (Bioinformagician)
> 📄 **مرجع:** Li H, et al. (2009). *The Sequence Alignment/Map format and SAMtools.* Bioinformatics 25:2078–2079. https://doi.org/10.1093/bioinformatics/btp352

---

## ۴. یک ناحیه، و پوشش

### ریدهای یک جای ژنوم
چون BAM مرتب و ایندکس‌شده است، می‌شود مستقیم به یک ناحیه پرید. نشانی ناحیه مانند `samtools faidx` است. جای ۴٬۱۸۲٬۸۲۰ را در rpoB می‌خواهیم:

<div dir="ltr">

```bash
samtools view -c resistant.bam NC_000913.3:4182820-4182820
```

</div>

<div dir="ltr">

```text
34
```

</div>

**۳۴ رید** این جای ژنوم را پوشانده‌اند.

### عمق در هر باز: `samtools depth`

<div dir="ltr">

```bash
samtools depth -a -r NC_000913.3:4182818-4182822 resistant.bam
```

</div>

<div dir="ltr">

```text
NC_000913.3	4182818	34
NC_000913.3	4182819	34
NC_000913.3	4182820	34
NC_000913.3	4182821	34
NC_000913.3	4182822	34
```

</div>

ستون سوم **عمق** است: چند رید هر باز را دیده‌اند (`-a`: بازهای با عمق صفر را هم نشان بده؛ `-r`: تنها این ناحیه).

### خلاصه‌ی پوشش: `samtools coverage`

<div dir="ltr">

```bash
samtools coverage -r NC_000913.3:4170001-4200000 resistant.bam
```

</div>

<div dir="ltr">

```text
#rname	startpos	endpos	numreads	covbases	coverage	meandepth	meanbaseq	meanmapq
NC_000913.3	4170001	4200000	5776	29982	99.94	28.88	27	40.4
```

</div>

**این خروجی یعنی:** در این ۳۰ کیلوباز، ۹۹٫۹۴٪ بازها دست‌کم یک رید دارند و **میانگین عمق ۲۸٫۸۸** است (کمابیش همان ۳۰ برابری که در درس «بیوانفورماتیک چیست؟» حساب کردیم). برای فراخوانی مطمئن واریانت در باکتری، عمق ۲۰ تا ۳۰ برابر کافی شمرده می‌شود.

---

## ‏۵. VCF: فهرست تفاوت‌ها

‏**VCF** (*Variant Call Format*) فایلی متنی است که هر خط آن **یک جای ژنوم است که نمونه با مرجع فرق دارد**. در بسیاری از موارد با `bgzip` فشرده (`.vcf.gz`) و با `tabix` ایندکس (`.tbi`) می‌شود.

### سرآیند

<div dir="ltr">

```bash
bcftools view -h resistant.vcf.gz | wc -l
bcftools view -h resistant.vcf.gz | tail -n 1
```

</div>

<div dir="ltr">

```text
31
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	resistant
```

</div>

۳۰ خط `##` (تعریف هر برچسب، نسخه‌ی برنامه‌ها، و حتی دستوری که VCF را ساخت) و یک خط `#CHROM` (نام ستون‌ها). ستون دهم به بعد **نمونه‌ها**یند؛ این‌جا یک نمونه: `resistant`.

### بدنه

<div dir="ltr">

```bash
bcftools view -H resistant.vcf.gz | cut -f1-7,9,10
```

</div>

<div dir="ltr">

```text
NC_000913.3	4175500	.	C	T	225.417	.	GT:PL:AD	1:255,0:0,27
NC_000913.3	4182820	.	C	T	225.417	.	GT:PL:AD	1:255,0:0,33
NC_000913.3	4188999	.	CG	C	228.393	.	GT:PL:AD	1:255,0:1,38
NC_000913.3	4193210	.	G	A	225.417	.	GT:PL:AD	1:255,0:0,28
```

</div>

(ستون ۸، INFO، بسیار بلند است و آن را برداشته‌ایم.)

| ستون | یعنی | در خط دوم |
| :-: | :--- | :--- |
| CHROM, POS | کجا (شماره از ۱) | ‏`NC_000913.3` جای ۴٬۱۸۲٬۸۲۰ |
| REF | باز(های) **مرجع** | `C` |
| ALT | باز(های) **نمونه** | `T` |
| QUAL | اطمینان (Phred) که این‌جا واقعاً تفاوتی هست | ۲۲۵٫۴ (بسیار بالا) |
| FORMAT | برچسب‌های ستون نمونه، به ترتیب | `GT:PL:AD` |
| نمونه | مقدار همان برچسب‌ها | `1` : `255,0` : `0,33` |

- ‏**GT** (ژنوتیپ) = `1`: نمونه ALT را دارد. باکتری **هاپلوئید** است، پس GT یک عدد دارد (در انسان دیپلوئید، `0/1` یا `1/1`).
- ‏**AD** = `0,33`: **صفر** رید مرجع (`C`) و **۳۳** رید جایگزین (`T`) را نشان دادند. پس همه‌ی ریدها جهش را دارند.

### ‏SNP و indel
سه ردیف SNP‌اند (یک باز به یک باز). ردیف سوم یک **indel** است: `REF=CG`، `ALT=C`، یعنی `G` پس از `C` حذف شده است. **در VCF، indel همیشه با یک باز «لنگر» پیش از خود نوشته می‌شود**؛ پس POS (۴٬۱۸۸٬۹۹۹) باز لنگر است و خود حذف در ۴٬۱۸۹٬۰۰۰ است. همان کاهشی است که در CIGAR (`…1D…`) دیدیم.

### ‏`bcftools query`: تنها ستون‌های دلخواه

<div dir="ltr">

```bash
bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t%QUAL\t%INFO/DP\n' resistant.vcf.gz
```

</div>

<div dir="ltr">

```text
NC_000913.3	4175500	C	T	225.417	27
NC_000913.3	4182820	C	T	225.417	34
NC_000913.3	4188999	CG	C	228.393	39
NC_000913.3	4193210	G	A	225.417	29
```

</div>

‏`-f` قالب خروجی است (مانند `printf`): `%POS` جای، `%INFO/DP` عمق از ستون INFO، `\t` Tab و `\n` پایان خط. عمق در جای ۴٬۱۸۲٬۸۲۰ **۳۴** است، همان `samtools depth`. ✓

### شمردن و گزینش

<div dir="ltr">

```bash
bcftools stats resistant.vcf.gz | grep -E '^SN.*(records|SNPs|indels)'
bcftools view -H -r NC_000913.3:4181245-4185273 resistant.vcf.gz | cut -f1-5
```

</div>

<div dir="ltr">

```text
SN	0	number of records:	4
SN	0	number of SNPs:	3
SN	0	number of indels:	1
NC_000913.3	4182820	.	C	T
```

</div>

- ‏`bcftools stats` خلاصه می‌دهد: **۴ واریانت، ۳ SNP، ۱ indel**.
- ‏`-r` (*region*) تنها ناحیه‌ی **rpoB** (۴٬۱۸۱٬۲۴۵ تا ۴٬۱۸۵٬۲۷۳): **یک واریانت**، در ۴٬۱۸۲٬۸۲۰.

> 📺 **فیلم:** *Understanding File Formats in Bioinformatics: VCF and gVCF*: https://www.youtube.com/watch?v=cBDZSGf9HRE (Bioinformagician)
> 📄 **مرجع:** Danecek P, et al. (2011). *The variant call format and VCFtools.* Bioinformatics 27:2156–2158. https://doi.org/10.1093/bioinformatics/btr330

---

## ۶. از جای ژنومی به کدون: H526Y

‏rpoB روی رشته‌ی **مثبت** از ۴٬۱۸۱٬۲۴۵ آغاز می‌شود. جهش در ۴٬۱۸۲٬۸۲۰ است:

‏$$\text{فاصله از آغاز ژن} = 4{,}182{,}820 - 4{,}181{,}245 = 1{,}575$$

‏$$\text{کدون} = \lfloor 1575 / 3 \rfloor + 1 = 526 \qquad \text{جای درون کدون} = 1575 \bmod 3 + 1 = 1$$

<div dir="ltr">

```bash
echo $(( (4182820-4181245)/3 + 1 )) $(( (4182820-4181245)%3 + 1 ))
```

</div>

<div dir="ltr">

```text
526 1
```

</div>

جهش **باز یکم کدون ۵۲۶** است. کدون ۵۲۶ در مرجع `CAC` (هیستیدین، H) است (این را در ماژول ابزارهای وب، بخش ۰۰، و با `samtools faidx` می‌بینید). با جهش C → T می‌شود **`TAC` (تیروزین، Y)**:

<div dir="ltr">

```text
مرجع:   CAC  →  His (H)
سویه:    TAC  →  Tyr (Y)
```

</div>

**این همان H526Y است**: یکی از سه جایگاه کلیدی ناحیه‌ی RRDR (D516، H526، S531) در بخش ۰۰، و از شناخته‌شده‌ترین جهش‌های مقاومت به ریفامپیسین در *E. coli*. **فرضیه‌ی داستان ما پشتیبانی شد.**

(باز هم یادآوری بخش ۰۰: این یک **همبستگی** است. اثبات علّی آزمایش می‌خواهد، مانند وارد کردن همین جهش در سویه‌ی حساس.)

---

## ۷. سه اشتباه رایج

| اشتباه | چه می‌شود | به جایش |
| :--- | :--- | :--- |
| ‏`cat` یا `head` روی BAM | نویسه‌های بی‌معنا (BAM دودویی و فشرده است) | `samtools view` |
| نادیده گرفتن MAPQ | ریدهای چندجایی (مانند rRNA) واریانت‌های ساختگی می‌سازند | ‏`samtools view -q 30`؛ در فراخوانی، کنار گذاشتن MAPQ پایین |
| «واریانت در VCF نیست» = «تفاوتی نیست» | شاید آن ناحیه اصلاً رید نداشته | پوشش (`samtools depth`/`coverage`) را هم گزارش کنید |

---

## ۸. جمع‌بندی

- ‏**SAM/BAM**: هر رید یک خط؛ ۱۱ ستون اجباری + برچسب‌ها؛ سرآیند `@PG` تاریخچه‌ی برنامه‌هاست. BAM مرتب + `.bai` برای دسترسی به ناحیه.
- ‏**FLAG** چند ویژگی را در یک عدد دارد (`samtools flags`)؛ **MAPQ** اطمینان از جای رید (۰–۱ = چندجایی)؛ **CIGAR** چگونگی هم‌ترازی (`M`، `I`، `D`، `S`).
- ‏`samtools view -c`، `-q`، و ناحیه؛ `samtools depth` و `coverage` برای پوشش.
- ‏**VCF**: هر خط یک تفاوت با مرجع؛ REF، ALT، QUAL، و ستون نمونه (GT، AD). indel با باز لنگر.
- `bcftools view -h/-H/-r`، `query -f`، `stats`.
- جای ژنومی ← کدون: (جای − آغاز ژن) ÷ ۳ + ۱ (برای ژن رشته‌ی مثبت).

---

## کارت دستورهای این درس

| می‌خواهم… | دستور |
| :--- | :--- |
| سرآیند BAM | `samtools view -H file.bam` |
| چند رید نخست (۹ ستون) | `samtools view file.bam \| head \| cut -f1-9` |
| شمار ریدها | `samtools view -c file.bam` |
| تنها MAPQ ≥ ۳۰ | `samtools view -q 30 file.bam` |
| ریدهای یک ناحیه | `samtools view file.bam chr:start-end` |
| معنای یک FLAG | `samtools flags 163` |
| خلاصه‌ی FLAGها | `samtools flagstat file.bam` |
| عمق هر باز | `samtools depth -a -r chr:start-end file.bam` |
| خلاصه‌ی پوشش | `samtools coverage -r chr:start-end file.bam` |
| سرآیند / بدنه‌ی VCF | `bcftools view -h` / `-H file.vcf.gz` |
| ستون‌های دلخواه VCF | `bcftools query -f '%POS\t%REF\t%ALT\n' file.vcf.gz` |
| واریانت‌های یک ناحیه | `bcftools view -H -r chr:start-end file.vcf.gz` |
| آمار VCF | `bcftools stats file.vcf.gz \| grep ^SN` |

---

<details>
<summary>📘 <b>برای کنجکاوها (اختیاری):</b> FLAG دقیقاً چگونه ساخته می‌شود؟ و CRAM</summary>

هر ویژگی یک «بیت» است با ارزش ۱، ۲، ۴، ۸، … . FLAG جمع ویژگی‌های «بله» است:

| ارزش | ویژگی |
| :-: | :--- |
| 1 | PAIRED |
| 2 | PROPER_PAIR |
| 4 | ‏UNMAP (رید هم‌تراز نشده) |
| 8 | ‏MUNMAP (جفتش هم‌تراز نشده) |
| 16 | REVERSE |
| 32 | MREVERSE |
| 64 | READ1 |
| 128 | READ2 |
| 256 | SECONDARY |
| 2048 | SUPPLEMENTARY |

‏163 = 128 + 32 + 2 + 1 = READ2 + MREVERSE + PROPER_PAIR + PAIRED. ✓ با `samtools view -f 4` تنها ریدهای **هم‌ترازنشده** را برمی‌دارید و با `-F 4` تنها هم‌ترازشده‌ها را (`-f` یعنی «باید این بیت را داشته باشد»، `-F` یعنی «نباید»). این را در بخش ۰۶ برای جدا کردن ریدهای میزبان به کار می‌بریم.

‏**CRAM** نسخه‌ی فشرده‌تر BAM است که تنها **تفاوت‌ها با مرجع** را نگه می‌دارد؛ پس برای خواندنش همان FASTA مرجع لازم است.
</details>

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| هم‌ترازی (alignment / mapping) | پیدا کردن جای هر رید روی ژنوم مرجع |
| SAM / BAM | فرمت متنی / دودویی فشرده‌ی ریدهای هم‌ترازشده |
| FLAG | عددی که چند ویژگی «بله/نه» هر رید را با هم نگه می‌دارد |
| MAPQ | اطمینان (Phred) از جای هم‌ترازی؛ ۰–۱ = چندجایی |
| CIGAR | رشته‌ی کوتاهی که چگونگی هم‌ترازی را می‌گوید (`150M`، `95M1D55M`) |
| عمق / پوشش (depth / coverage) | شمار ریدهایی که یک باز را دیده‌اند |
| واریانت (variant) | جایی که نمونه با مرجع فرق دارد |
| VCF | فرمت متنی فهرست واریانت‌ها |
| SNP / indel | تفاوت یک‌بازی / افزایش یا کاهش باز |
| ژنوتیپ (GT) | کدام آلل(ها) در نمونه هست |

---

## منابع

### راهنمای رسمی و مقاله
- ویژگی‌نامه‌ی رسمی SAM و VCF (hts-specs): https://samtools.github.io/hts-specs/
- Li H, et al. (2009). The Sequence Alignment/Map format and SAMtools. *Bioinformatics* 25(16):2078–2079. https://doi.org/10.1093/bioinformatics/btp352
- Danecek P, et al. (2021). Twelve years of SAMtools and BCFtools. *GigaScience* 10(2):giab008. https://doi.org/10.1093/gigascience/giab008
- راهنمای samtools و bcftools: https://www.htslib.org/doc/
- Jin DJ, Gross CA (1988). Mapping and sequencing of mutations in the *Escherichia coli rpoB* gene that lead to rifampicin resistance. *J Mol Biol* 202(1):45–58. https://doi.org/10.1016/0022-2836(88)90517-7

### کتاب
- ‏Buffalo V (2015). *Bioinformatics Data Skills*. O'Reilly. (فصل ۱۱: کار با داده‌ی هم‌ترازی؛ SAM و BAM)

### فیلم‌های آموزشی

**Coursera:**
- ‏Johns Hopkins University — *Command Line Tools for Genomic Data Science*. هفته‌های SAMtools و BCFtools: https://www.coursera.org/learn/genomic-tools

**edX:**
- ‏IsraelX — *Essentials of Genomics and Biomedical Informatics*. بخش واریانت‌های ژنومی: https://www.edx.org/learn/medicine/israelx-essentials-of-genomics-and-biomedical-informatics

**YouTube:**
- Bioinformagician — *Understanding Bioinformatics File Formats: SAM/BAM*: https://www.youtube.com/watch?v=vh6l9aPFUgU
- Bioinformagician — *Understanding File Formats in Bioinformatics: VCF and gVCF*: https://www.youtube.com/watch?v=cBDZSGf9HRE

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. همه‌ی دستورها در 2026-10-20 با samtools 1.20 و bcftools 1.21 اجرا شدند. داده شبیه‌سازی‌شده است؛ روندش در `make_examples.sh` آمده است.

</div>
