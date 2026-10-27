<div dir="rtl">

# درس ۲: ‏EDirect و `xtract`؛ جدول ژن‌های مقاومت در یک لوله

**بخش:** `11_V2_NCBI_Databases` · **ماژول:** `01_Entrez_EDirect` · **پیش‌نیاز:** [درس ۱](01_lesson_eutils.md)؛ لوله (`|`)، `sort` و `awk` از بخش [۰۱](../../01_Linux/)؛ ‏`Bio.Entrez` از ماژول [03/05](../../03_Python/05_Biopython_GenBank/) · **زمان:** حدود ۷۵ دقیقه · **ابزار:** EDirect 24.0 (`esearch`، `esummary`، `elink`، `efilter`، `efetch`، `xtract`)، Biopython 1.87 · **آخرین بازبینی:** 2026-10-27

> ✅ **وضعیت: اجرا شده.** همه‌ی خروجی‌ها واقعی‌اند (2026-10-27). هر لوله زیر ۱۰ ثانیه و چند ده مگابایت حافظه.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. ‏EDirect را نصب کنید و بدانید هر دستورش کدام ابزار E-utilities را صدا می‌زند.
2. جست‌وجو، خلاصه، پیوند و دریافت را در **یک لوله** بنویسید؛ سرور تاریخچه خودکار است.
3. با `xtract` و گزینه‌ی `-block` از XML یک **جدول** درست بسازید.
4. دام **نام‌های دیگر ژن** (alias) را بشناسید: `acrB[gene]` دو ژن می‌دهد.
5. با `efilter` نتیجه‌ی یک پیوند را پالایش کنید.
6. همین جدول را با یک اسکریپت Biopython هم بسازید.

**پیش از آغاز:** EDirect را با Mamba یا Conda از کانال bioconda نصب کنید (بخش ۰۲)، یا با اسکریپت رسمی NCBI:

<div dir="ltr">

```bash
conda install -c conda-forge -c bioconda entrez-direct     # or the official installer:
# sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"
esearch -version
xtract -version
cd ~/ncbi/m01
P=~/Bioinformatics_Learning-main/11_V2_NCBI_Databases/99_scripts_data
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
24.0
24.0
```

</div>

---

## ۱. داستان

در درس ۱ برای دو ژن، سه درخواست `curl` نوشتیم و `WebEnv` را با `grep` و `cut` از XML بیرون کشیدیم و به گام بعد دادیم. کار درست بود ولی شکننده. حالا پرسش بزرگ‌تری داریم: در بخش ۰۸ دیدید مقاومت در *E. coli* بیشتر از جهش در پنج ژن می‌آید: **rpoB** و **rpoC** (ریفامپیسین)، **gyrA** و **parC** (کینولون‌ها) و **acrB** (پمپ برون‌ریز). می‌خواهیم برای هر پنج ژن **جای ژن، رشته، طول و پروتئین RefSeq** را در یک جدول داشته باشیم. ‏**EDirect** همان E-utilities است، ولی هر ابزار یک دستور جدای خط فرمان است و همه با `|` به هم می‌چسبند؛ WebEnv را خودشان جابه‌جا می‌کنند.

---

## ۲. مفهوم به زبان ساده

### ۲.۱ هر دستور EDirect = یک ابزار E-utilities

| دستور EDirect | ابزار E-utilities | تفاوت |
| :--- | :--- | :--- |
| ‏`esearch -db gene -query "…"` | ‏`esearch.fcgi` + `usehistory=y` | خروجی یک «برگه»ی کوچک XML است: WebEnv، QueryKey و Count |
| ‏`esummary` | ‏`esummary.fcgi` | برگه را از لوله می‌خواند |
| ‏`elink -target protein` | ‏`elink.fcgi` + `cmd=neighbor_history` | برگه‌ی تازه با فهرست پیوندها |
| ‏`efilter -query "…"` | ‏`esearch.fcgi` روی همان فهرست | پالایش نتیجه‌ی گام پیش |
| ‏`efetch -format fasta` | ‏`efetch.fcgi` | ‏`-format` = ‏`rettype` |
| ‏`xtract` | (روی رایانه‌ی خودتان) | ‏XML → جدول جدا شده با Tab |

**تشبیه:** درس ۱ خودتان برگه‌ی امانت را از این باجه به آن باجه می‌بردید؛ در EDirect یک نوار نقاله برگه را می‌برد.

### ‏۲.۲ ‏`xtract`: از درخت XML به جدول

پاسخ‌های NCBI **درخت**‌اند: هر `DocumentSummary` (یک ژن) شاخه‌هایی دارد، و یکی از آن‌ها `GenomicInfo` است با `ChrStart` و `ChrStop`. سه گزینه‌ی اصلی `xtract`:

| گزینه | معنا |
| :--- | :--- |
| ‏`-pattern X` | هر شاخه‌ی `X` **یک سطر** خروجی |
| ‏`-element A B` | فیلدهای `A` و `B` را در آن سطر بنویس (جدا با Tab) |
| ‏`-block Y` | تنها **درون** شاخه‌ی `Y` بگرد؛ فیلدهای پس از آن از همین شاخه‌اند |

> 📺 **فیلم:** ‏NLM، *Downloading NCBI Biological Data and Creating Custom Reports Using the Command Line* (ضبط کارگاه EDirect، 2023): https://www.nlm.nih.gov/ncbi/workshops/2023-04_custom-reports/workshop-video.html
> 📄 **مرجع:** Kans J. *Entrez Direct: E-utilities on the Unix Command Line.* NCBI Bookshelf: https://www.ncbi.nlm.nih.gov/books/NBK179288/

---

## ۳. گام ۱: نخستین `esearch`

**چرا؟** ببینیم EDirect به جای فهرست UID چه برمی‌گرداند.

<div dir="ltr">

```bash
esearch -db gene -query "rpoB[preferred symbol] AND txid511145[Organism:noexp]"
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```xml
<ENTREZ_DIRECT>
  <Db>gene</Db>
  <WebEnv>MCID_6ae07020a455cd69c3079be2</WebEnv>
  <QueryKey>1</QueryKey>
  <Count>1</Count>
  <Step>1</Step>
  <Elapsed>0</Elapsed>
</ENTREZ_DIRECT>
```

</div>

**توضیح خروجی:** هیچ UIDی چاپ نشد! تنها **برگه** (`ENTREZ_DIRECT`): نام پایگاه، WebEnv، QueryKey و شمار (۱). این برگه برای دستور بعدی لوله است، نه برای چشم شما. ‏`Step` شماره‌ی گام در لوله است.

> **یادداشت سرور دوره:** روی سرور ما هر دستور EDirect در خروجی خطا (stderr) سطرهایی مانند `curl: (56) OpenSSL SSL_read: … unexpected eof` چاپ می‌کند، ولی خودش دوباره می‌کوشد و نتیجه درست است (در یک نوبت آزمون ۲۲ سطر از این پیام آمد و همه‌ی نتیجه‌ها درست بودند). در این پیام‌ها نشانی ایمیل و کلید API شما هم چاپ می‌شود؛ پس اگر خروجی را با کسی بخش می‌کنید، stderr را جدا کنید: `2> edirect.log`.

---

## ۴. گام ۲: لوله‌ی `esearch | esummary | xtract`

<div dir="ltr">

```bash
esearch -db gene -query "rpoB[preferred symbol] AND txid511145[Organism:noexp]" \
  | esummary \
  | xtract -pattern DocumentSummary -element Id Name Description
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
948488	rpoB	RNA polymerase subunit beta
```

</div>

یک سطر، سه ستون جدا با Tab. ‏`Id` شناسه‌ی ژن است (در XML ‏`esummary` به شکل `<DocumentSummary uid="948488">`؛ ‏`xtract` نام ویژه‌ی `Id` را برای آن دارد).

### ۴.۱ دام: `-element` بی `-block`

حالا مختصات را هم بخواهیم:

<div dir="ltr">

```bash
esummary -db gene -id 948488 | xtract -pattern DocumentSummary -element Name ChrStart ChrStop
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
rpoB	4181244	999999999	4185272
```

</div>

**چهار ستون به جای سه!** همان `ChrStart` دوم درس ۱ (فیلد مرتب‌سازی با `999999999`) دوباره آمد، و بدتر، در **ستون سوم** جایی که انتظار `ChrStop` را داشتید. اگر این خروجی را بی نگاه به `awk` بدهید، طول ژن را حدود ۹۹۵ میلیون باز حساب می‌کند. راه درست: به `xtract` بگویید `ChrStart` و `ChrStop` را **تنها درون** `GenomicInfoType` بجوید:

<div dir="ltr">

```bash
esummary -db gene -id 948488 \
  | xtract -pattern DocumentSummary -element Name -block GenomicInfoType -element ChrAccVer ChrStart ChrStop
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
rpoB	NC_000913.3	4181244	4185272
```

</div>

درست. **قاعده:** هر جا یک فیلد ممکن است در چند شاخه‌ی XML بیاید، `-block` بگذارید.

<details>
<summary>✋ امتحان کن: چرا `esummary -db gene -id 948488` بی `esearch` کار کرد؟</summary>

‏`esummary` اگر برگه‌ای از لوله نگیرد، `-db` و `-id` را می‌پذیرد. پس می‌توانید هم از یک جست‌وجو آغاز کنید و هم از شناسه‌هایی که از پیش دارید. همین برای `efetch` و `elink` هم درست است.

</details>

> 📺 **فیلم:** ‏NLM، ضبط کارگاه EDirect (بالا).
> 📄 **مرجع:** ‏Kans J. *Entrez Direct*، بخش «Extracting Data from XML» (`-pattern`، `-element`، `-block`): https://www.ncbi.nlm.nih.gov/books/NBK179288/

---

## ۵. گام ۳: جدول پنج ژن مقاومت

<div dir="ltr">

```bash
Q='(rpoB[preferred symbol] OR rpoC[preferred symbol] OR gyrA[preferred symbol] OR parC[preferred symbol] OR acrB[preferred symbol]) AND txid511145[Organism:noexp]'
esearch -db gene -query "$Q" \
  | esummary \
  | xtract -pattern DocumentSummary -element Id Name -block GenomicInfoType -element ChrStart ChrStop \
  | sort -k2,2 > genes5.tsv
cat genes5.tsv
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`Q='…'` | پرسش بلند را یک بار در متغیر بگذارید؛ تک‌نقل‌قول تا پوسته به کروشه‌ها و پرانتزها دست نزند |
| ‏`( … OR … )` | پنج نام با «یا»؛ پرانتز لازم است، وگرنه `AND` تنها به آخری می‌چسبد |
| ‏`"$Q"` | متغیر درون جفت‌نقل‌قول، تا فاصله‌ها پرسش را نشکنند |
| ‏`sort -k2,2` | بر پایه‌ی ستون دوم (نام ژن) مرتب کن |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
945108	acrB	484402	481253
946614	gyrA	2339419	2336792
947499	parC	3165972	3163714
948488	rpoB	4181244	4185272
948487	rpoC	4185349	4189572
```

</div>

در سه ژن `ChrStart` **بزرگ‌تر** از `ChrStop` است: این ژن‌ها روی **رشته‌ی منفی**‌اند. NCBI جای آغاز ژن را (کُدون آغاز) در `ChrStart` می‌گذارد، و روی رشته‌ی منفی آغاز ژن عدد بزرگ‌تر است. با `awk` رشته و طول را بیفزاییم:

<div dir="ltr">

```bash
awk -F'\t' 'BEGIN{OFS="\t"} {s=($3>$4)?"-":"+"; l=($3>$4)?$3-$4+1:$4-$3+1; print $2,$1,s,l}' genes5.tsv
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`-F'\t'` و `OFS="\t"` | ورودی و خروجی جدا با Tab |
| ‏`s=($3>$4)?"-":"+"` | ‏`شرط ? الف : ب` یعنی «اگر شرط درست است الف، وگرنه ب»؛ کوتاه‌شده‌ی `if … else`. پس اگر آغاز بزرگ‌تر از پایان است رشته `-`، وگرنه `+` |
| ‏`l=…+1` | طول با در نظر گرفتن هر دو سر |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
acrB	945108	-	3150
gyrA	946614	-	2628
parC	947499	-	2259
rpoB	948488	+	4029
rpoC	948487	+	4224
```

</div>

**وارسی با پاسخ معلوم:** rpoB ‏۴۰۲۹ باز = ۱۳۴۲ اسید آمینه + کُدون پایان (درس ۱). gyrA ‏۲۶۲۸ باز = ۸۷۵ × ۳ + ۳ (درس ۱، گام ۶). هر دو جور درمی‌آیند. نکته‌ی زیستی: `rpoC` تنها ۷۷ باز پس از پایان `rpoB` (4185272) آغاز می‌شود (4185349)؛ این دو در یک **اپرون** (operon) با هم رونویسی می‌شوند.

---

## ۶. گام ۴: دام نام‌های دیگر؛ `[gene]` یا `[preferred symbol]`؟

**چرا گام ۳ با `[preferred symbol]` بود؟** همین جدول را با `[gene]` بسازیم:

<div dir="ltr">

```bash
S='(rpoB[gene] OR rpoC[gene] OR gyrA[gene] OR parC[gene] OR acrB[gene]) AND txid511145[Organism:noexp]'
esearch -db gene -query "$S" | xtract -pattern ENTREZ_DIRECT -element Count
esearch -db gene -query "acrB[gene] AND txid511145[Organism:noexp]" \
  | esummary | xtract -pattern DocumentSummary -element Id Name OtherAliases
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
6
948211	gyrB	b3699, Cou, ECK3691, acrB, himB, hisU, hopA, nalC, parA, pcbA, pcpA
945108	acrB	b0462, ECK0456, acrE
```

</div>

**توضیح خروجی:**
- با `[gene]` **شش** ژن، نه پنج. ژن ششم **gyrB** است!
- چرا؟ ‏`[gene]` نام اصلی **و همه‌ی نام‌های دیگر** (`OtherAliases`) را می‌جوید. یکی از نام‌های قدیمی gyrB «acrB» است: در ژنتیک کلاسیک، پیش از شناخت ژن‌ها، هر جهش‌یافته نامی از رفتارش می‌گرفت و گاهی یک نام به دو ژن جدا رسید. پس `acrB[gene]` هم gyrB را می‌آورد و هم acrB را.
- ‏`[preferred symbol]` تنها **نام رسمی کنونی** را می‌جوید: ‏`acrB[preferred symbol]` تنها `945108` را می‌دهد.

| برچسب | می‌جوید | کی |
| :--- | :--- | :--- |
| ‏`[gene]` (`GENE`) | نام رسمی + همه‌ی نام‌های دیگر | وقتی نام قدیمی یک ژن را از یک مقاله دارید و نمی‌دانید نام امروزی‌اش چیست |
| ‏`[preferred symbol]` (`PREF`) | تنها نام رسمی | ساختن جدول و هر جا شمار باید دقیق باشد |

<details>
<summary>✋ امتحان کن: یک مقاله‌ی قدیمی از جهش «nalA» در مقاومت به نالیدیکسیک اسید می‌گوید. nalA امروز کدام ژن است؟</summary>

<div dir="ltr">

```bash
esearch -db gene -query "nalA[gene] AND txid511145[Organism:noexp]" | esummary \
  | xtract -pattern DocumentSummary -element Id Name OtherAliases
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
946614	gyrA	b2231, ECK2223, hisW, nalA, nfxA, norA, parD
```

</div>

‏**gyrA**. این همان جای سودمند `[gene]` است: نام قدیمی از مقاله را به نام امروزی می‌رساند.

</details>

> 📺 **فیلم:** *E-Utilities Introduction* (NLM)، بخش جست‌وجو و فیلدها: https://www.youtube.com/watch?v=BCG-M5k-gvE
> 📄 **مرجع:** ‏ESearch و برچسب‌های فیلد در *The E-utilities In-Depth*: https://www.ncbi.nlm.nih.gov/books/NBK25499/ · Brown GR, et al. (2015). Nucleic Acids Res 43:D36–D42. https://doi.org/10.1093/nar/gku1055

---

## ۷. گام ۵: از ژن به پروتئین RefSeq؛ و یک دام در `elink`

**چرا؟** جدول، شناسه‌ی پروتئین و توالی را کم دارد. در درس ۱ با `linkname=gene_protein_refseq` تنها پروتئین RefSeq را گرفتیم. ‏`elink` در EDirect گزینه‌ی `-name` دارد؛ بیازماییم:

<div dir="ltr">

```bash
R='rpoB[preferred symbol] AND txid511145[Organism:noexp]'
esearch -db gene -query "$R" | elink -target protein -name gene_protein_refseq | xtract -pattern ENTREZ_DIRECT -element Count
esearch -db gene -query "$R" | elink -target protein | xtract -pattern ENTREZ_DIRECT -element Count
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
13
13
```

</div>

**هر دو ۱۳!** در EDirect 24.0، وقتی `elink` برگه را از لوله می‌گیرد، `-name` به کار گرفته نمی‌شود و **همه‌ی** پروتئین‌های پیوندی می‌آیند (درس ۱: ۱ RefSeq + ۱۲ رکورد دیگر). برای پنج ژن این ۸۷ پروتئین شد، با پنج پروتئین که هر کدام بارها تکرار شده بودند. **این دام بی‌صداست:** هیچ پیامی نمی‌دهد. پس همیشه `Count` را بسنجید.

راه درست: **`efilter`** فهرست پیوندها را با یک پرسش پالایش می‌کند. فیلتر `refseq[filter]` تنها رکوردهای RefSeq را نگه می‌دارد:

<div dir="ltr">

```bash
esearch -db gene -query "$Q" | elink -target protein | efilter -query "refseq[filter]" | efetch -format acc
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
NP_418415.1
NP_418414.1
NP_417491.1
NP_416734.1
NP_414995.1
```

</div>

دقیقاً پنج پروتئین `NP_`. حالا توالی‌ها، و طول هر کدام:

<div dir="ltr">

```bash
esearch -db gene -query "$Q" | elink -target protein | efilter -query "refseq[filter]" \
  | efetch -format fasta > prot5.faa
awk '/^>/{if(h)print h"\t"n; h=$1; n=0; next}{n+=length($0)} END{print h"\t"n}' prot5.faa
grep '^>' prot5.faa | cut -d' ' -f2- | cut -c1-45
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
>NP_418415.1	1407
>NP_418414.1	1342
>NP_417491.1	752
>NP_416734.1	875
>NP_414995.1	1049
RNA polymerase subunit beta' [Escherichia col
RNA polymerase subunit beta [Escherichia coli
DNA topoisomerase IV subunit A [Escherichia c
DNA gyrase subunit A [Escherichia coli str. K
multidrug efflux pump RND permease AcrB [Esch
```

</div>

‏rpoC (β′، ۱۴۰۷)، rpoB (β، ۱۳۴۲)، parC (۷۵۲)، gyrA (۸۷۵) و acrB (۱۰۴۹). طول‌ها با طول ژن‌های گام ۳ جورند: ۴۲۲۴ = ۱۴۰۷ × ۳ + ۳، ‏۲۲۵۹ = ۷۵۲ × ۳ + ۳، ‏۳۱۵۰ = ۱۰۴۹ × ۳ + ۳.

> 📺 **فیلم:** ‏NLM، ضبط کارگاه EDirect (بالا).
> 📄 **مرجع:** ‏Kans J. *Entrez Direct*، بخش‌های ELink و EFilter: https://www.ncbi.nlm.nih.gov/books/NBK179288/

---

## ۸. گام ۶: شمار مقاله‌ها

<div dir="ltr">

```bash
for g in rpoB gyrA; do
  n=$(esearch -db gene -query "$g[preferred symbol] AND txid511145[Organism:noexp]" \
      | elink -target pubmed | xtract -pattern ENTREZ_DIRECT -element Count)
  echo "$g $n"
done
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
rpoB 350
gyrA 202
```

</div>

‏rpoB: ‏**۳۵۰**؛ همان عدد درس ۱ (۳۵۱ `<Id>` منهای ژن آغاز). ‏EDirect این تفریق را خودش کرده است. ‏`for` و `$( … )` همان‌هایی‌اند که در بخش ۰۱ دیدید؛ EDirect تنها چند دستور تازه‌ی پوسته است و با همه‌ی ابزارهای لینوکس جور می‌شود.

---

## ۹. گام ۷: همین جدول با Biopython

**چرا؟** اگر کار بعدی‌تان در پایتون است (مانند pandas در بخش ۰۳)، بهتر است داده را همان‌جا بگیرید. ‏`Bio.Entrez` همان E-utilities است. اسکریپت [gene_table.py](../99_scripts_data/01_Entrez_EDirect/scripts/gene_table.py):

<div dir="ltr">

```python
Entrez.email = os.environ.get("ENTREZ_EMAIL", "your.name@example.org")
Entrez.api_key = os.environ.get("NCBI_API_KEY")      # None = no key: at most 3 requests per second

found = Entrez.read(Entrez.esearch(db="gene", term=query, retmax=100))
ids = found["IdList"]
summary = Entrez.read(Entrez.esummary(db="gene", id=",".join(ids)))
for doc in summary["DocumentSummarySet"]["DocumentSummary"]:
    info = doc["GenomicInfo"][0]
    start, stop = int(info["ChrStart"]), int(info["ChrStop"])
    strand = "-" if start > stop else "+"
```

</div>

| بخش | کار |
| :--- | :--- |
| ‏`os.environ.get(…)` | ایمیل و کلید را از متغیرهای محیطی بخوان؛ هیچ‌کدام در اسکریپت نوشته نمی‌شود |
| ‏`Entrez.read(…)` | ‏XML پاسخ را به فهرست و دیکشنری پایتون برگردان |
| ‏`id=",".join(ids)` | همه‌ی UIDها در **یک** درخواست، نه یک درخواست برای هر ژن |
| ‏`doc["GenomicInfo"][0]` | همان کار `-block GenomicInfoType`: تنها درون این شاخه |

<div dir="ltr">

```bash
export ENTREZ_EMAIL="your.name@example.org"      # your own email
python3 $P/01_Entrez_EDirect/scripts/gene_table.py "$Q"
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
# query: (rpoB[preferred symbol] OR rpoC[preferred symbol] OR gyrA[preferred symbol] OR parC[preferred symbol] OR acrB[preferred symbol]) AND txid511145[Organism:noexp]
# hits: 5
id	symbol	chr_acc	start	stop	strand	length
948488	rpoB	NC_000913.3	4181244	4185272	+	4029
948487	rpoC	NC_000913.3	4185349	4189572	+	4224
946614	gyrA	NC_000913.3	2339419	2336792	-	2628
945108	acrB	NC_000913.3	484402	481253	-	3150
947499	parC	NC_000913.3	3165972	3163714	-	2259
```

</div>

همان عددهای گام ۳، از راهی دیگر. ترتیب سطرها همان ترتیب پیش‌فرض پاسخ NCBI است، نه الفبایی.

> 📺 **فیلم:** *Accessing NCBI databases and tools with Biopython (Entrez)*: https://www.youtube.com/watch?v=tl4xqdfIBh0 (Lana Dominkovic)
> 📄 **مرجع:** Biopython Tutorial and Cookbook، فصل «Accessing NCBI's Entrez databases»: https://biopython.org/docs/latest/Tutorial/chapter_entrez.html · Cock PJA, et al. (2009). *Biopython.* Bioinformatics 25:1422–1423. https://doi.org/10.1093/bioinformatics/btp163

---

## ۱۰. سه اشتباه رایج

1. ‏**‏`-element` بی `-block`.** ‏`xtract -element ChrStart ChrStop` ستون `999999999` را میان داده می‌گذارد و ستون‌ها جابه‌جا می‌شوند (گام ۲). هر فیلد تکراری را با `-block` در شاخه‌ی خودش بجویید.
2. ‏**‏`[gene]` برای جدول.** ‏`acrB[gene]` ژن gyrB را هم می‌آورد (گام ۴). برای جدول `[preferred symbol]`، و همیشه `Count` را با شمار ژن‌هایی که خواسته‌اید بسنجید.
3. **باور به `elink -name` در لوله.** در EDirect 24.0 بی‌صدا نادیده گرفته می‌شود (گام ۵). ‏`efilter -query "refseq[filter]"` بگذارید و شمار را بسنجید.

---

## 📘 برای کنجکاوها

- ‏**`xtract -outline`** ساختار درختی هر پاسخ XML را نشان می‌دهد؛ پیش از نوشتن `-pattern` و `-block` نگاهش کنید: `esummary -db gene -id 948488 | xtract -outline`.
- ‏**`-if` و `-equals`** در `xtract` سطرها را پالایش می‌کنند (مانند `grep`، ولی بر پایه‌ی یک فیلد)؛ در ماژول 11/02 به کارشان می‌گیریم.
- ‏**`nquire`** و **`einfo`** هم در EDirect هستند؛ `einfo -db gene -fields` همان فیلدهای درس ۱ را جدول‌وار می‌دهد.
- ‏**سویه‌ی W3110:** همان پرسش با `[orgn]` به جای `noexp` (درس ۱) شش ژن داد. با اسکریپت گام ۷ ببینید: rpoB در W3110 روی **رشته‌ی منفی** است، چون W3110 یک **وارونگی** (inversion) بزرگ کروموزومی نسبت به MG1655 دارد (تمرین ۶).

---

## جمع‌بندی

- ‏EDirect همان E-utilities است، با برگه‌ی `ENTREZ_DIRECT` که WebEnv را از راه لوله جابه‌جا می‌کند.
- ‏`xtract -pattern … -element … -block …` ‏XML را به جدول برمی‌گرداند؛ `-block` جلوی ستون‌های نادرست را می‌گیرد.
- ‏`[preferred symbol]` برای جدول دقیق؛ `[gene]` برای یافتن نام‌های قدیمی (nalA → gyrA؛ acrB → gyrB هم).
- ‏`elink | efilter -query "refseq[filter]" | efetch` پنج پروتئین RefSeq را داد: ۱۴۰۷، ۱۳۴۲، ۷۵۲، ۸۷۵ و ۱۰۴۹ اسید آمینه.
- ‏Biopython (`gene_table.py`) همان جدول را با کلید و ایمیل از متغیرهای محیطی داد.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
esearch -db DB -query "QUERY"                                    # -> ENTREZ_DIRECT ticket
esearch … | xtract -pattern ENTREZ_DIRECT -element Count         # how many?
esearch … | esummary | xtract -pattern DocumentSummary -element Id Name -block GenomicInfoType -element ChrStart ChrStop
esearch … | elink -target protein | efilter -query "refseq[filter]" | efetch -format fasta
esearch … | elink -target pubmed | xtract -pattern ENTREZ_DIRECT -element Count
esummary -db gene -id UID | xtract -outline                      # see the XML tree
python3 gene_table.py "QUERY"                                    # same table with Biopython
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏EDirect | دستورهای خط فرمان NCBI روی E-utilities |
| برگه‌ی `ENTREZ_DIRECT` | ‏XML کوچکی که میان دستورهای لوله WebEnv و QueryKey را جابه‌جا می‌کند |
| ‏`xtract` | ابزار EDirect برای بیرون کشیدن فیلدها از XML به جدول |
| ‏pattern / element / block | واحد هر سطر / فیلد چاپی / شاخه‌ای که جست‌وجو در آن می‌ماند |
| نام دیگر (alias) | نام قدیمی یا جایگزین یک ژن |
| نام رسمی (preferred symbol) | نام کنونی و پذیرفته‌شده‌ی ژن |
| ‏`efilter` | پالایش فهرست روی سرور با یک پرسش تازه |
| ‏`refseq[filter]` | فیلتری که تنها رکوردهای RefSeq را نگه می‌دارد |
| رشته‌ی منفی (minus strand) | ژنی که روی رشته‌ی مکمل خوانده می‌شود؛ در Gene آغاز > پایان |
| اپرون (operon) | چند ژن پشت سر هم که با هم رونویسی می‌شوند |
| وارونگی (inversion) | برگشتن یک تکه‌ی کروموزوم در جای خودش |

---

## منابع

**مقاله و مستند**
- ‏Kans J. *Entrez Direct: E-utilities on the Unix Command Line.* Entrez Programming Utilities Help, NCBI Bookshelf: https://www.ncbi.nlm.nih.gov/books/NBK179288/
- ‏Sayers EW, et al. (2025). *Database resources of the National Center for Biotechnology Information in 2025.* Nucleic Acids Res 53(D1):D20–D29. https://doi.org/10.1093/nar/gkae979
- ‏Brown GR, et al. (2015). *Gene: a gene-centered information resource at NCBI.* Nucleic Acids Res 43(D1):D36–D42. https://doi.org/10.1093/nar/gku1055
- ‏Cock PJA, et al. (2009). *Biopython: freely available Python tools for computational molecular biology and bioinformatics.* Bioinformatics 25(11):1422–1423. https://doi.org/10.1093/bioinformatics/btp163
- ‏Biopython Tutorial and Cookbook، فصل Entrez: https://biopython.org/docs/latest/Tutorial/chapter_entrez.html

**کتاب**
- ‏Buffalo V (2015). *Bioinformatics Data Skills.* O'Reilly. (فصل ۳: پوسته و لوله‌ها؛ فصل ۷: کار با داده‌ی جدولی در خط فرمان)
- ‏Pevsner J (2015). *Bioinformatics and Functional Genomics*, 3rd ed. Wiley-Blackwell. (فصل ۲: Entrez، Gene و RefSeq)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Access Bioinformatics Databases with Biopython*: https://www.coursera.org/projects/access-bioinformatics-databases-with-biopython
- ‏edX: *Introduction to Genomic Data Science* (UC San Diego): https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science
- ‏YouTube: *E-Utilities Introduction* (National Library of Medicine): https://www.youtube.com/watch?v=BCG-M5k-gvE
- ‏YouTube: *Accessing NCBI databases and tools with Biopython (Entrez)* (Lana Dominkovic): https://www.youtube.com/watch?v=tl4xqdfIBh0
- ‏NLM: ضبط کارگاه *Downloading NCBI Biological Data and Creating Custom Reports Using the Command Line*: https://www.nlm.nih.gov/ncbi/workshops/2023-04_custom-reports/workshop-video.html

<sub>همه‌ی دستورها در 2026-10-27 روی سرور دوره با EDirect 24.0 و Biopython 1.87 اجرا شدند. رفتار `elink -name` در لوله با دو اجرای جدا (با و بی `-name`) سنجیده شد. DOIها با doi.org و صفحه‌های NCBI با درخواست مستقیم وارسی شدند.</sub>

</div>
