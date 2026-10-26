<div dir="rtl">

# درس: فرمت‌های آنوتیشن؛ GFF، BED، GenBank و تله‌ی شماره‌گذاری

**بخش:** `02_BioLinux` · **ماژول:** `03_Annotation_Formats` · **پیش‌نیاز:** ماژول [فرمت‌های توالی](../02_Sequence_Formats/) · **زمان:** حدود ۷۵ دقیقه · **ابزار:** awk، curl، seqkit 2.13.0 · **آخرین اجرا:** 2026-10-20

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. ساختار کامل GFF3 را بشناسید، از جمله پیوند پدر و فرزند (`ID` و `Parent`) و ستون فاز.
2. فرق **شماره‌گذاری از ۱** (GFF) و **شماره‌گذاری از ۰** (BED) را بفهمید و میانشان درست تبدیل کنید.
3. یک فایل BED بسازید و با آن توالی ژن‌ها را بیرون بکشید.
4. یک رکورد GenBank را دانلود کنید و بخش‌هایش (سرآیند، FEATURES، ORIGIN) را بخوانید.

**پیش از آغاز:**

<div dir="ltr">

```bash
conda activate bioinfo_course
cd ~/Bioinformatics_Learning-main/02_BioLinux/99_scripts_data/03_Annotation_Formats/data
G=~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data      # ژنوم و GFF بخش ۰۱
```

</div>

این پوشه سه فایل نمونه‌ی آماده دارد: `rpoB.gff3`، `rpoB.bed` و `rpoB.gb`. در این درس خودتان هم آن‌ها را می‌سازید.

---

## ۱. داستان: «جای ژن» در سه زبان

پیش از این، جای rpoB را در فایل GFF دیدیم: از ۴٬۱۸۱٬۲۴۵ تا ۴٬۱۸۵٬۲۷۳. ولی ابزارهای گوناگون **جای چیزها روی ژنوم** را با فرمت‌های گوناگون می‌نویسند:
- ‏**GFF** (و GTF): فهرست کامل ژن‌ها با آگاهی‌های بسیار؛ خروجی برنامه‌های آنوتیشن.
- ‏**BED**: تنها «کجا»، کوتاه و ساده؛ زبان بسیاری از ابزارهای ژنومیک.
- ‏**GenBank**: توالی **و** آنوتیشن **و** مقاله‌ها با هم، در یک فایل خوانا برای آدم‌ها.

یک تفاوت کوچک میان این فرمت‌ها، یعنی این‌که شماره‌گذاری از **۰** آغاز شود یا از **۱**، یکی از رایج‌ترین خطاهای بی‌صدای بیوانفورماتیک است. این درس آن را با یک نمونه‌ی واقعی نشان می‌دهد.

---

## ‏۲. GFF3، کامل

### ساختن یک GFF کوچک برای rpoB
همه‌ی خط‌هایی را برمی‌داریم که با rpoB **هم‌پوشانی** دارند. یک «چیز» با rpoB هم‌پوشان است اگر **پیش از پایان rpoB آغاز شود** و **پس از آغاز rpoB پایان یابد**:

<div dir="ltr">

```bash
{ grep '^##' $G/ecoli_k12.gff | head -n 3; awk -F'\t' '$4<=4185273 && $5>=4181245' $G/ecoli_k12.gff; } > my_rpoB.gff3
cut -f1-8 my_rpoB.gff3
```

</div>

<div dir="ltr">

```text
##gff-version 3
##sequence-region NC_000913.3 1 4641652
##species https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=511145
NC_000913.3	RefSeq	region	1	4641652	.	+	.
NC_000913.3	RefSeq	gene	4181245	4185273	.	+	.
NC_000913.3	RefSeq	CDS	4181245	4185273	.	+	0
```

</div>

#### کالبدشکافی دستور

| تکه | یعنی |
| :--- | :--- |
| `{ …; …; }` | دو دستور را **گروه** کن تا خروجی هر دو با هم در یک فایل برود (فاصله پس از `{` و `;` پیش از `}` لازم است) |
| `grep '^##' … \| head -n 3` | سه خط سرآیند GFF |
| `$4<=4185273 && $5>=4181245` | شرط هم‌پوشانی: آغاز ≤ پایان rpoB **و** پایان ≥ آغاز rpoB |
| `> my_rpoB.gff3` | خروجی گروه در فایل |

**این خروجی یعنی:** سه چیز با rpoB هم‌پوشانی دارند: `region` (کل کروموزوم، که با همه چیز هم‌پوشان است)، خود **ژن**، و **CDS** آن.

### پدر و فرزند: `ID` و `Parent`
ستون ۹ خط ژن با `ID=gene-b3987` آغاز می‌شود و ستون ۹ خط CDS با `ID=cds-NP_418414.1;Parent=gene-b3987`. یعنی:

<div dir="ltr">

```text
gene  (ID=gene-b3987, Name=rpoB)
 └── CDS  (ID=cds-NP_418414.1, Parent=gene-b3987)
```

</div>

‏**CDS فرزند ژن است.** در یوکاریوت‌ها این درخت بلندتر است: ژن ← mRNA (ترنسکریپت) ← چند exon و چند CDS (یکی برای هر exon). `Parent` همه‌ی این‌ها را به هم وصل می‌کند.

### ستون ۸: فاز
ستون فاز تنها برای CDS معنا دارد (`0`، `1` یا `2`): **چند باز از آغاز این تکه باید رد شود تا به نخستین کدون کامل برسیم.** برای ژن باکتریایی که یک تکه‌ی پیوسته است، همیشه `0` است. در ژن‌های یوکاریوتی چند-exonی، exon دوم ممکن است وسط یک کدون آغاز شود و فاز `1` یا `2` بگیرد.

### GTF
‏**GTF** نسخه‌ی کهنه‌تر و همانند GFF است که در RNA-seq رایج است. همان ۹ ستون، ولی ستون ۹ به شکل `gene_id "X"; transcript_id "Y";` نوشته می‌شود. ابزارها هر دو را می‌شناسند، ولی جابه‌جا به کار بردنشان خطا می‌دهد.

> 📺 **فیلم:** *Understanding Bioinformatics File Formats: GFF3 and GTF*: https://www.youtube.com/watch?v=2Y7zxh1BiFs (Bioinformagician)
> 📄 **مرجع:** GFF3 specification: https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md

---

## ‏۳. BED، و شماره‌گذاری از صفر

### ساختن BED برای rpoB

<div dir="ltr">

```bash
awk -F'\t' 'BEGIN{OFS="\t"} $3=="gene" && $9 ~ /Name=rpoB;/ {print $1, $4-1, $5, "rpoB", 0, $7}' $G/ecoli_k12.gff
```

</div>

<div dir="ltr">

```text
NC_000913.3	4181244	4185273	rpoB	0	+
```

</div>

#### کالبدشکافی

| تکه | یعنی |
| :--- | :--- |
| `BEGIN{OFS="\t"}` | پیش از خواندن نخستین خط (`BEGIN`)، جداکننده‌ی **خروجی** (*Output Field Separator*) را Tab بگذار؛ وگرنه `print` با فاصله جدا می‌کند |
| `$4-1` | **آغاز منهای یک**: تبدیل از شماره‌گذاری GFF به BED |
| `$5` | پایان، بی تغییر |
| `"rpoB", 0, $7` | نام، امتیاز (این‌جا ۰)، رشته |

**شش ستون BED:**

| ستون | نام | اجباری؟ |
| :-: | :--- | :-: |
| 1 | نام کروموزوم | ✅ |
| 2 | آغاز (**از ۰**) | ✅ |
| 3 | پایان | ✅ |
| 4 | نام | — |
| 5 | امتیاز | — |
| 6 | رشته (`+` یا `-`) | — |

### دو شیوه‌ی شماره‌گذاری

چرا آغاز در GFF **۴٬۱۸۱٬۲۴۵** است و در BED **۴٬۱۸۱٬۲۴۴**، در حالی که هر دو همان ژن‌اند؟ بازها را مانند خانه‌های یک خط‌کش تصور کنید:

<div dir="ltr">

```text
                 باز:   A   T   G   G   T   T
  شماره از ۱ (GFF):     1   2   3   4   5   6        ← شماره‌ی خود باز
  شماره از ۰ (BED):   0   1   2   3   4   5   6      ← شماره‌ی «مرز» میان بازها
```

</div>

| شیوه | فرمت‌ها | سه باز نخست `ATG` | طول |
| :--- | :--- | :-: | :--- |
| **از ۱، دوسر بسته** `[آغاز، پایان]` | ‏GFF، GTF، SAM، VCF، GenBank، نشانی ناحیه در samtools | `1–3` | پایان − آغاز **+ ۱** |
| **از ۰، نیمه‌باز** `[آغاز، پایان)` | ‏BED، و درون Python | `0–3` | پایان − آغاز |

در BED، آغاز **مرز پیش از** باز یکم است و پایان **مرز پس از** باز آخر. پس `0 3` یعنی «از مرز ۰ تا مرز ۳»: سه باز. **قاعده‌ی تبدیل: آغاز BED = آغاز GFF − ۱؛ پایان یکی است.**

### آزمون واقعی: BED درست و BED نادرست
با `seqkit subseq --bed` توالی بازه‌های یک فایل BED را از ژنوم برمی‌داریم:

<div dir="ltr">

```bash
seqkit subseq --bed rpoB.bed $G/ecoli_k12.fna | seqkit fx2tab -n -l
seqkit subseq --bed rpoB.bed $G/ecoli_k12.fna | seqkit subseq -r 1:12 | tail -n 1
```

</div>

<div dir="ltr">

```text
NC_000913.3_4181245-4185273:+ rpoB	4029
ATGGTTTACTCC
```

</div>

**درست:** ۴٬۰۲۹ باز، آغازشده با `ATG`. (`seqkit` در نام خروجی، ناحیه را به شیوه‌ی از ۱ نوشته است.) حالا یک BED **نادرست** می‌سازیم که آغاز GFF را بی تبدیل نوشته است (`4181245`):

<div dir="ltr">

```bash
printf 'NC_000913.3\t4181245\t4185273\trpoB_wrong\t0\t+\n' > wrong.bed
seqkit subseq --bed wrong.bed $G/ecoli_k12.fna | seqkit fx2tab -n -l
seqkit subseq --bed wrong.bed $G/ecoli_k12.fna | seqkit subseq -r 1:12 | tail -n 1
```

</div>

<div dir="ltr">

```text
NC_000913.3_4181246-4185273:+ rpoB_wrong	4028
TGGTTTACTCCT
```

</div>

**نادرست:** ۴٬۰۲۸ باز، و `A` کدون آغاز گم شده است (`TGG…`). هیچ پیام خطایی نیامد. اگر این توالی را ترجمه کنید، **قاب خواندن جابه‌جا** شده و همه‌ی پروتئین بی‌معنا می‌شود. به این خطا **«یکی کم یا زیاد»** (off-by-one) می‌گویند.

### ‏BED برای همه‌ی ژن‌ها

<div dir="ltr">

```bash
awk -F'\t' 'BEGIN{OFS="\t"} $3=="gene" {print $1, $4-1, $5, ".", 0, $7}' $G/ecoli_k12.gff > genes.bed
wc -l genes.bed
seqkit subseq --bed genes.bed $G/ecoli_k12.fna | seqkit stats -T
```

</div>

<div dir="ltr">

```text
4506 genes.bed
file	format	type	num_seqs	sum_len	min_len	avg_len	max_len
-	FASTA	DNA	4506	4043784	27	897.4	7020
```

</div>

**این خروجی یعنی:** ۴٬۵۰۶ ژن، جمعاً ۴٬۰۴۳٬۷۸۴ باز (۸۷٪ ژنوم)، از ۲۷ تا ۷٬۰۲۰ باز، با میانگین **۸۹۷٫۴**؛ همان میانگین ماژول awk. ✓ `.` در ستون ۴ یعنی «نام ندارد». نکته: برای ژن‌هایی که ستون ۶ آن‌ها `-` است، `seqkit` **خودش مکمل معکوس** را برمی‌گرداند؛ پس همه‌ی ژن‌ها از کدون آغاز شروع می‌شوند.

<details>
<summary>✋ <b>امتحان کن:</b> ژن gyrA در GFF از ۲٬۳۳۶٬۷۹۳ تا ۲٬۳۳۹٬۴۲۰ است (رشته‌ی منفی). ردیف BED آن چیست؟</summary>

<div dir="ltr">

```text
NC_000913.3	2336792	2339420	gyrA	0	-
```

</div>

آغاز یکی کم می‌شود (۲٬۳۳۶٬۷۹۲)، پایان همان می‌ماند. طول: ۲٬۳۳۹٬۴۲۰ − ۲٬۳۳۶٬۷۹۲ = ۲٬۶۲۸، همان طول در GFF (پایان − آغاز + ۱). ✓
</details>

> 📺 **فیلم:** *BED Format and BEDtools a Practical Tutorial*: https://www.youtube.com/watch?v=Cf1xd0GRxu4
> 📄 **مرجع:** UCSC, BED format: https://genome.ucsc.edu/FAQ/FAQformat.html#format1

---

## ‏۴. GenBank: توالی و آنوتیشن در یک فایل

### دانلود با `curl`
رکورد GenBank ناحیه‌ی rpoB را از NCBI E-utilities می‌گیریم (همان نوع پرسش API که در بخش ۰۲، ماژول دریافت داده، بیشتر می‌بینید):

<div dir="ltr">

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000913.3&rettype=gbwithparts&retmode=text&seq_start=4181245&seq_stop=4185273" > my_rpoB.gb
```

</div>

| تکه‌ی نشانی | یعنی |
| :--- | :--- |
| `efetch.fcgi` | «رکورد را بیاور» |
| `db=nuccore&id=NC_000913.3` | از پایگاه نوکلئوتید، این شناسه |
| `rettype=gbwithparts&retmode=text` | به شکل GenBank کامل، متنی |
| `seq_start=…&seq_stop=…` | تنها این ناحیه (شماره از ۱) |

### بخش‌های فایل

<div dir="ltr">

```bash
head -n 12 my_rpoB.gb
```

</div>

<div dir="ltr">

```text
LOCUS       NC_000913               4029 bp    DNA     linear   CON 02-SEP-2026
DEFINITION  Escherichia coli str. K-12 substr. MG1655, complete genome.
ACCESSION   NC_000913 REGION: 4181245..4185273
VERSION     NC_000913.3
DBLINK      BioProject: PRJNA57779
            BioSample: SAMN02604091
KEYWORDS    RefSeq.
SOURCE      Escherichia coli str. K-12 substr. MG1655
  ORGANISM  Escherichia coli str. K-12 substr. MG1655
            Bacteria; Pseudomonadati; Pseudomonadota; Gammaproteobacteria;
            Enterobacterales; Enterobacteriaceae; Escherichia.
REFERENCE   1  (bases 1 to 4029)
```

</div>

| بخش | چه دارد |
| :--- | :--- |
| **سرآیند** (`LOCUS` تا `REFERENCE`) | نام، طول (۴٬۰۲۹ bp)، شناسه‌ی نسخه‌دار، پروژه، رده‌بندی موجود، و مقاله‌ها |
| **FEATURES** | ژن‌ها و CDSها، هر کدام با `/نام="مقدار"` |
| **ORIGIN** | خود توالی، با شماره‌ی باز در آغاز هر خط |
| `//` | پایان رکورد |

### یک CDS در بخش FEATURES

<div dir="ltr">

```bash
grep -A 10 '^     CDS' my_rpoB.gb
```

</div>

<div dir="ltr">

```text
     CDS             1..4029
                     /gene="rpoB"
                     /locus_tag="b3987"
                     /gene_synonym="ECK3978; ftsR; groN; nitB; rif; ron; sdgB;
                     stl; stv; tabD"
                     /EC_number="2.7.7.6"
                     /codon_start=1
                     /transl_table=11
                     /product="RNA polymerase subunit beta"
                     /protein_id="NP_418414.1"
                     /db_xref="UniProtKB/Swiss-Prot:P0A8V2"
```

</div>

‏(`grep -A 10` یعنی «خط یافته‌شده و ۱۰ خط پس از آن».)

**این خروجی یعنی:**
- `1..4029`: جای CDS **نسبت به همین رکورد** (که خودش از ۴٬۱۸۱٬۲۴۵ ژنوم آغاز می‌شد)، نه نسبت به کل ژنوم.
- ‏`/transl_table=11`: جدول کد ژنتیکی باکتری‌ها.
- ‏`/product`، `/protein_id` و `/db_xref`: نام پروتئین و پیوند به RefSeq و UniProt (بخش ۰۰).
- یکی از نام‌های دیگر ژن (`/gene_synonym`) **`rif`** است؛ یادگار کشف آن از راه مقاومت به ریفامپیسین.

پس از این‌ها `/translation="MVYSYTEKKRIRKDFGKRPQ…"` می‌آید: **توالی پروتئین**، که در بخش ۰۳ دوره با Biopython از همین فایل می‌خوانیم.

> 📺 **فیلم:** *GenBank Tutorial*: https://www.youtube.com/watch?v=JAxpmKg0KL0
> 📄 **مرجع:** NCBI, GenBank sample record: https://www.ncbi.nlm.nih.gov/genbank/samplerecord/

---

## ۵. سه اشتباه رایج

| اشتباه | چه می‌شود | به جایش |
| :--- | :--- | :--- |
| آغاز GFF را بی تبدیل در BED نوشتن | یک باز گم می‌شود؛ کدون آغاز و قاب خواندن خراب (بخش ۳) | آغاز BED = آغاز GFF − ۱ |
| طول بازه‌ی BED را مانند GFF حساب کردن (`+1`) | یک باز بیشتر | در BED: پایان − آغاز |
| فراموش کردن `OFS="\t"` در `awk` | ‏BED با فاصله ساخته می‌شود و برخی ابزارها آن را نمی‌خوانند | `BEGIN{OFS="\t"}` |

---

## ۶. جمع‌بندی

- ‏GFF3: ۹ ستون؛ پیوند پدر و فرزند با `ID` و `Parent`؛ فاز در ستون ۸ برای CDS. GTF همانند آن، با ستون ۹ دیگرگونه.
- ‏BED: سه ستون اجباری (کروموزوم، آغاز، پایان) و سه اختیاری (نام، امتیاز، رشته)؛ **شماره از ۰، نیمه‌باز**.
- تبدیل GFF ← BED: آغاز − ۱، پایان همان. خطای off-by-one بی‌صداست ولی قاب خواندن را خراب می‌کند.
- ‏`seqkit subseq --bed` توالی بازه‌های BED را برمی‌دارد و برای رشته‌ی منفی مکمل معکوس می‌دهد.
- ‏GenBank: سرآیند، FEATURES (با `/qualifier`ها) و ORIGIN؛ مختصات نسبت به خود رکورد.

---

## کارت دستورهای این درس

| می‌خواهم… | دستور |
| :--- | :--- |
| خط‌های GFF هم‌پوشان با یک بازه | `awk -F'\t' '$4<=END && $5>=START' file.gff` |
| ‏GFF به BED (همه‌ی ژن‌ها) | `awk -F'\t' 'BEGIN{OFS="\t"} $3=="gene" {print $1,$4-1,$5,".",0,$7}' f.gff > genes.bed` |
| توالی بازه‌های BED | `seqkit subseq --bed genes.bed genome.fa` |
| ‏GenBank یک ناحیه از NCBI | `curl -s "…efetch.fcgi?db=nuccore&id=ID&rettype=gbwithparts&retmode=text&seq_start=S&seq_stop=E"` |
| خط یافته و N خط پس از آن | ‏`grep -A N 'الگو' file` |
| دو دستور، یک خروجی | `{ cmd1; cmd2; } > out` |

---

<details>
<summary>📘 <b>برای کنجکاوها (اختیاری):</b> GenBank برای ژن رشته‌ی منفی، و چرا Python از ۰ می‌شمارد</summary>

**رشته‌ی منفی:** افزودن `&strand=2` به نشانی efetch، رکورد را برای **رشته‌ی دیگر** می‌دهد. برای gyrA (۲٬۳۳۶٬۷۹۳ تا ۲٬۳۳۹٬۴۲۰، `strand=2`) رکوردی ۲٬۶۲۸ bp می‌گیرید که CDS آن `1..2628` است و ORIGIN آن با `atgagcgacc…` آغاز می‌شود: همان آغاز ژن.

**چرا از ۰؟** در بیشتر زبان‌های برنامه‌نویسی (Python، C) خانه‌های یک رشته از ۰ شماره می‌خورند و برش `[0:3]` سه نویسه‌ی نخست است: درست همان منطق BED. پس BED برای برنامه‌ها طبیعی است و GFF برای آدم‌ها. در بخش ۰۳ (پایتون) این را دوباره می‌بینید.
</details>

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| آنوتیشن (annotation) | فهرست چیزهای شناخته‌شده روی ژنوم (ژن، CDS، RNA…) با جایشان |
| GFF3 / GTF | فرمت‌های ۹ ستونی آنوتیشن |
| BED | فرمت ساده‌ی بازه‌ها؛ شماره از ۰ |
| GenBank | فرمت NCBI برای توالی + آنوتیشن + ارجاع‌ها |
| هم‌پوشانی (overlap) | دو بازه که دست‌کم یک باز مشترک دارند |
| off-by-one | خطای «یکی کم یا زیاد» در تبدیل شماره‌گذاری |
| نیمه‌باز (half-open) | بازه‌ای که آغازش جزو آن است و پایانش نه: `[آغاز، پایان)` |

---

## منابع

### راهنمای رسمی فرمت‌ها
- GFF3 specification: https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md
- UCSC — BED format: https://genome.ucsc.edu/FAQ/FAQformat.html#format1
- ‏NCBI — GenBank sample record (توضیح همه‌ی بخش‌ها): https://www.ncbi.nlm.nih.gov/genbank/samplerecord/
- NCBI E-utilities (efetch): https://www.ncbi.nlm.nih.gov/books/NBK25499/

### کتاب
- ‏Buffalo V (2015). *Bioinformatics Data Skills*. O'Reilly. (فصل ۹: کار با داده‌ی بازه‌ای؛ BED و GFF و شماره‌گذاری از صفر)

### فیلم‌های آموزشی

**Coursera:**
- ‏Johns Hopkins University — *Command Line Tools for Genomic Data Science*. بخش ویژگی‌های ژنومی و BED: https://www.coursera.org/learn/genomic-tools

**edX:**
- IsraelX — *Essentials of Genomics and Biomedical Informatics*: https://www.edx.org/learn/medicine/israelx-essentials-of-genomics-and-biomedical-informatics

**YouTube:**
- GenoMediCon — *Essential Genomic File Formats for Beginners: FASTA, FASTQ, SAM/BAM, and VCF Explained*: https://www.youtube.com/watch?v=BaVBesblyxw

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. همه‌ی دستورها در 2026-10-20 با mawk 1.3.4، GNU grep 3.11 و seqkit 2.13.0 اجرا شدند. پیام‌های `[INFO]` `seqkit` برداشته شده‌اند.

</div>
