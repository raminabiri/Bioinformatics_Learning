<div dir="rtl">

# درس: BioProject، BioSample و SRA؛ از یک پروژه‌ی ۵۹۵ گیگابایتی تا یک فایل FASTQ سنجیده

**بخش:** `11_V2_NCBI_Databases` · **ماژول:** `03_BioProject_BioSample_SRA` · **پیش‌نیاز:** ماژول [11/01](../01_Entrez_EDirect/)؛ ماژول [02/05](../../02_BioLinux/05_Data_Download/) (دریافت همین اجرا از ENA) · **زمان:** حدود ۹۰ دقیقه (به‌اضافه‌ی زمان دانلود) · **ابزار:** curl 8.20.0، EDirect 24.0، SRA Toolkit 3.4.1 (`prefetch`، `vdb-validate`، `fasterq-dump`، `fastq-dump`) · **آخرین بازبینی:** 2026-10-27

> ✅ **وضعیت: اجرا شده.** همه‌ی خروجی‌ها واقعی‌اند (2026-10-27). دانلود ۱۰۰ مگابایت روی سرور دوره ۶ دقیقه طول کشید؛ `fasterq-dump` ‏۲ ثانیه و ۱۹۱ مگابایت حافظه.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. سلسله‌مراتب **BioProject → BioSample → Experiment → Run** را توضیح دهید و شناسه‌های هر کدام (`PRJ…`، `SAM…`، `…X`، `…R`) را بشناسید.
2. جدول **runinfo** همه‌ی اجراهای یک پروژه را بگیرید و پیش از دانلود، حجم، گونه‌ی کتابخانه و شمار نمونه‌ها را بسنجید.
3. فراداده‌ی یک **BioSample** (کشور، سال، گونه‌ی نمونه) را بخوانید.
4. با **SRA Toolkit** یک اجرا را بگیرید، درستی‌اش را بسنجید و به FASTQ برگردانید.
5. نتیجه را با پاسخ معلوم ماژول 02/05 (ENA) بسنجید.

**پیش از آغاز:** SRA Toolkit را در یک محیط جدا نصب کنید (بخش ۰۲):

<div dir="ltr">

```bash
conda create -n sra -c conda-forge -c bioconda sra-tools=3.4.1
conda activate sra
fasterq-dump --version
mkdir -p ~/ncbi/m03 && cd ~/ncbi/m03
B=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
fasterq-dump : 3.4.1
```

</div>

---

## ۱. داستان

در ماژول 02/05 فایل `ERR688359.fastq.gz` را از ENA گرفتید و شمار ریدهایش (۱٬۱۵۸٬۱۸۹) را با گزارش ENA سنجیدید. ولی این فایل از کجا آمده بود؟ از کدام بیمار، کدام کشور، کدام پروژه؟ چند فایل دیگر از همان نمونه هست؟ اگر بخواهید همه‌ی پروژه را دوباره تحلیل کنید، چقدر فضا و زمان لازم دارید؟ پاسخ این پرسش‌ها در **فراداده** (metadata) است: داده درباره‌ی داده. در این درس همان فایل را این بار از سوی NCBI دنبال می‌کنیم: از پروژه تا نمونه تا خود ریدها.

---

## ۲. مفهوم به زبان ساده

### ۲.۱ چهار لایه

| لایه | پرسش | شناسه (NCBI / ENA / DDBJ) | نمونه در این درس |
| :--- | :--- | :--- | :--- |
| ‏**BioProject** | چه پژوهشی؟ | ‏`PRJNA…` / `PRJEB…` / `PRJDB…` | ‏`PRJEB7774` |
| ‏**BioSample** | کدام نمونه‌ی زیستی؟ | ‏`SAMN…` / `SAMEA…` / `SAMD…` | ‏`SAMEA3136648` |
| ‏**Experiment** | کدام کتابخانه و دستگاه؟ | ‏`SRX…` / `ERX…` / `DRX…` | ‏`ERX633360` |
| ‏**Run** | کدام فایل داده؟ | ‏`SRR…` / `ERR…` / `DRR…` | ‏`ERR688359` |

یک پروژه چندین نمونه دارد، هر نمونه چندین آزمایش، و هر آزمایش یک یا چند run. **تشبیه:** پروژه یک کتاب است، نمونه یک فصل، آزمایش یک بخش، و run یک صفحه.

سه پایگاه NCBI (آمریکا)، ENA (اروپا) و DDBJ (ژاپن) در **INSDC** با هم کار می‌کنند و داده‌ها را هر روز میان خود جابه‌جا می‌کنند. پس `ERR688359` که در ENA ثبت شده، در SRA هم هست؛ پیشوند `E` تنها می‌گوید کجا ثبت شد.

> 📺 **فیلم:** *NCBI's Sequence Read Archive: Downloading sequences* (Dranalytics): https://www.youtube.com/watch?v=evlIjjlIUBA
> 📄 **مرجع:** Barrett T, et al. (2012). *BioProject and BioSample databases at NCBI: facilitating capture and organization of metadata.* Nucleic Acids Res 40(D1):D57–D63. https://doi.org/10.1093/nar/gkr1163 · Katz K, et al. (2022). *The Sequence Read Archive: a decade more of explosive growth.* Nucleic Acids Res 50(D1):D387–D390. https://doi.org/10.1093/nar/gkab1053

---

## ۳. گام ۱: پروژه؛ و دوباره دام برچسب فیلد

<div dir="ltr">

```bash
esearch -db bioproject -query "PRJEB7774" | esummary \
  | xtract -pattern DocumentSummary -element Project_Acc Project_Title Organism_Name Project_Data_Type Submitter_Organization Registration_Date
esearch -db bioproject -query "PRJEB7774[Project Accession]" | xtract -pattern ENTREZ_DIRECT -element Count
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
PRJEB103230	TPA metagenomic assembly of the PRJEB7774 data set	Other	ETH ZURICH	2025/12/31 00:00
PRJEB90943	SPIRE v01 TPA metagenomic analyses (assembly & MAGs) of project spire_study_120	Other	European Molecular Biology Laboratory	2025/10/27 00:00
PRJNA987980	Microbiome Pipeline Benchmarking	Raw sequence reads	GMT Science	2023/06/27 00:00
PRJEB25190	EMG produced TPA metagenomics assembly of the Gut microbiome development along the colorectal adenoma-carcinoma sequence (AT_CRC) data set.	Other	EMG	2018/02/28 00:00
PRJEB7774	Gut microbiome development along the colorectal adenoma-carcinoma sequence	Other	Beijing Genome Institute	2015/03/05 00:00
1
```

</div>

**توضیح خروجی:**
- بی برچسب، **پنج** پروژه آمد! چهار پروژه‌ی دیگر داده‌ی PRJEB7774 را **دوباره تحلیل** کرده‌اند (TPA = Third Party Annotation؛ اسمبلی و MAG در ۲۰۱۸ تا ۲۰۲۵) و نام PRJEB7774 را در شرح خود دارند. این نشان می‌دهد داده‌ی عمومی چقدر دوباره به کار می‌آید.
- با `[Project Accession]` تنها **یک**: پروژه‌ی اصلی BGI (۲۰۱۵): «تکامل میکروبیوم روده در مسیر آدنوم تا سرطان روده‌ی بزرگ» (Feng و همکاران، ۲۰۱۵).
- ستون `Organism_Name` برای این پروژه تهی است، چون نمونه‌ها **متاژنوم**‌اند، نه یک جاندار (بخش ۱۸).

---

## ۴. گام ۲: جدول runinfo؛ پیش از دانلود بشمارید

**چرا؟** پیش از گرفتن حتی یک فایل باید بدانید پروژه چند run دارد، هر کدام چه گونه است و روی هم چقدر حجم دارد. ‏SRA برای هر run یک سطر **runinfo** (CSV) می‌دهد.

<div dir="ltr">

```bash
curl -sS -G "$B/esearch.fcgi" --data-urlencode db=sra --data-urlencode usehistory=y \
     --data-urlencode "term=PRJEB7774[BioProject]" > hs.xml
grep -oE '<Count>[^<]*' hs.xml | head -1
WE=$(grep -o '<WebEnv>[^<]*' hs.xml | cut -d'>' -f2)
curl -sS "$B/efetch.fcgi?db=sra&query_key=1&WebEnv=$WE&rettype=runinfo&retmode=text" > runinfo.csv
wc -l < runinfo.csv
head -1 runinfo.csv | tr ',' '\n' | head -30 | tr '\n' ' '; echo
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
<Count>312
313
Run ReleaseDate LoadDate spots bases spots_with_mates avgLength size_MB AssemblyName download_path Experiment LibraryName LibraryStrategy LibrarySelection LibrarySource LibraryLayout InsertSize InsertDev Platform Model SRAStudy BioProject Study_Pubmed_id ProjectID Sample BioSample SampleType TaxID ScientificName SampleName
```

</div>

‏**۳۱۲** run (۳۱۳ سطر با سرستون). ستون‌های مهم: `spots` (شمار ریدها یا جفت‌ریدها)، `avgLength`، `size_MB` (ستون ۸)، `LibraryLayout` (۱۶)، `Model` (۲۰) و `BioSample` (۲۶). حالا خلاصه:

<div dir="ltr">

```bash
cut -d, -f13,16,19,20 runinfo.csv | sort | uniq -c
cut -d, -f26 runinfo.csv | tail -n +2 | sort -u | wc -l
awk -F, 'NR>1 && $16=="SINGLE"{s+=$8;n++} NR>1 && $16=="PAIRED"{p+=$8;m++} END{print "single",n,s; print "paired",m,p}' runinfo.csv
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
      1 LibraryStrategy,LibraryLayout,Platform,Model
    156 WGS,PAIRED,ILLUMINA,Illumina HiSeq 2000
    156 WGS,SINGLE,ILLUMINA,Illumina HiSeq 2000
156
single 156 12460
paired 156 582717
```

</div>

**توضیح خروجی:**
- همه **WGS** (تعیین توالی کل DNA، نه آمپلیکون 16S) روی **HiSeq 2000**.
- **۱۵۶** نمونه، و برای **هر** نمونه دو run: یک **PAIRED** و یک **SINGLE**. ‏BGI پس از جفت کردن ریدها، ریدهایی را که جفتشان دور ریخته شده بود جدا ثبت کرده است.
- حجم: ریدهای جفت **۵۸۲٬۷۱۷ مگابایت** (حدود ۵۸۳ گیگابایت) و تک‌ها تنها ۱۲٬۴۶۰ مگابایت. روی هم نزدیک به **۵۹۵ گیگابایت**، و این حجم فشرده‌ی SRA است؛ FASTQ بازشده نزدیک به سه و نیم برابر است (گام ۵).
- ‏`ERR688359` که در 02/05 گرفتید، run **تک** یک نمونه است، نه همه‌ی داده‌ی آن نمونه:

<div dir="ltr">

```bash
grep SAMEA3136648 runinfo.csv | cut -d, -f1,4,5,7,8,16,26
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
ERR688506,32474886,6094123641,187,4647,PAIRED,SAMEA3136648
ERR688359,1158189,102874412,88,96,SINGLE,SAMEA3136648
```

</div>

داده‌ی اصلی این نمونه `ERR688506` است: ‏**۳۲٫۵ میلیون** جفت‌رید، ‏۴٫۶ گیگابایت، میانگین طول ۱۸۷ (دو رید نزدیک به ۹۴ بازی). ‏`ERR688359` تنها **۳٫۴٪** ریدهای این نمونه است. برای یک کار آموزشی، کوچک بودنش خوب است؛ برای یک تحلیل واقعی، باید هر دو را برداشت.

<details>
<summary>✋ امتحان کن: کوچک‌ترین run این پروژه کدام است؟</summary>

<div dir="ltr">

```bash
sort -t, -k8,8n runinfo.csv | grep -v '^Run' | head -2 | cut -d, -f1,4,7,8,16,26
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
ERR710417,403547,88,32,SINGLE,SAMEA3178936
ERR710423,493903,86,40,SINGLE,SAMEA3178943
```

</div>

‏`ERR710417`: ‏۳۲ مگابایت. ‏`sort -t,` جداکننده را ویرگول می‌گذارد و `-k8,8n` بر پایه‌ی ستون ۸ (حجم) عددی مرتب می‌کند. برای آزمودن یک گردش کار، کوچک‌ترین run بهترین گزینه است.

</details>

> 📺 **فیلم:** *How to Obtain FASTQ from SRA (NCBI) using prefetch and fastq-dump* (Luís Miguel Gonçalves): https://www.youtube.com/watch?v=dYyj8sFxago
> 📄 **مرجع:** ‏SRA Run Selector (همین جدول در مرورگر): https://www.ncbi.nlm.nih.gov/Traces/study/ · مستندات SRA: https://www.ncbi.nlm.nih.gov/sra/docs/

---

## ۵. گام ۳: BioSample؛ نمونه از کجا آمده است؟

<div dir="ltr">

```bash
curl -sS "$B/esearch.fcgi?db=biosample&term=SAMEA3136648" | grep -oE '<Count>[^<]*' | head -1
curl -sS -G "$B/esearch.fcgi" --data-urlencode db=biosample --data-urlencode "term=SAMEA3136648[accn]" > bsq.xml
grep -oE '<(Count|Id)>[^<]*' bsq.xml | head -2
id=$(grep -o '<Id>[^<]*' bsq.xml | head -1 | cut -d'>' -f2)
curl -sS "$B/efetch.fcgi?db=biosample&id=$id" > bs.xml
grep -oE '<Title>[^<]*|<Organism taxonomy_id="[0-9]+" taxonomy_name="[^"]*"' bs.xml
grep -oE '<Attribute attribute_name="[^"]*"[^>]*>[^<]*' bs.xml | sed -E 's/<Attribute attribute_name="([^"]*)"[^>]*>/\1 = /' | grep -vE '^(ENA|INSDC)'
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`[accn]` | تنها در فیلد accession بجوی |
| ‏`<Attribute attribute_name="…">` | هر ویژگی نمونه یک برچسب با نام ویژگی در آن |
| ‏`sed -E 's/…(نام)…/\1 = /'` | ‏`\1` همان بخش درون پرانتز نخست است: نام ویژگی را نگه دار، بقیه‌ی برچسب را با ` = ` جایگزین کن |
| ‏`grep -vE '^(ENA\|INSDC)'` | ویژگی‌های اداری ENA و INSDC را کنار بگذار |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
<Count>95
<Count>1
<Id>3391450
<Title>Stool sample from controls
<Organism taxonomy_id="408170" taxonomy_name="human gut metagenome"
External Id = SAMEA3136648
Submitter Id = 31009
collection date = 2013
environment (biome) = human gut
environment (feature) = human-associated habitat
environment (material) = faeces
geographic location (country and/or sea) = Austria
geographic location (latitude) = 47.80151
geographic location (longitude) = 13.04292
human gut environmental package = human-gut
investigation type = metagenome
project name = Gut microbiome development along the colorectal adenoma-carcinoma sequence
sample name = 31009
sequencing method = Illumina
```

</div>

**توضیح خروجی:**
- **۹۵** نمونه بی برچسب! همه‌ی MAGهایی (ژنوم‌های بازسازی‌شده از متاژنوم) که از این نمونه ساخته شده‌اند، شناسه‌ی آن را در ویژگی «derived from» دارند. ‏`[accn]` یکی را برمی‌گزیند.
- نمونه‌ی **مدفوع** یک فرد **گروه شاهد** (control)، از **اتریش**، گردآوری ۲۰۱۳. جاندار «human gut metagenome» (TaxID 408170): همه‌ی میکروب‌های روده با هم.
- این‌ها همان چیزهایی‌اند که برای گزینش نمونه نیاز دارید: «تنها بیماران سرطان»، «تنها اتریش»، … . فراداده‌ی ناقص («missing») در SRA فراوان است؛ پیش از برنامه‌ریزی، کامل بودنش را بسنجید.

---

## ۶. گام ۴: SRA Toolkit؛ `prefetch` و `vdb-validate`

**چرا دو گام؟** ‏`prefetch` فایل فشرده‌ی SRA را می‌گیرد (و اگر بریده شد، از همان جا ادامه می‌دهد)؛ تبدیل به FASTQ جدا و روی رایانه‌ی شما انجام می‌شود.

<div dir="ltr">

```bash
/usr/bin/time -f "time=%es maxRSS=%MKB" prefetch ERR688359
ls -la ERR688359/
vdb-validate ERR688359 2>&1 | tail -2
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
2026-10-27T10:57:43 prefetch.3.4.1:  SRA Normalized Format file is being retrieved
2026-10-27T10:57:43 prefetch.3.4.1:  Downloading via HTTPS...
2026-10-27T11:03:49 prefetch.3.4.1:  HTTPS download succeed
2026-10-27T11:03:49 prefetch.3.4.1:  'ERR688359' is valid: 100771369 bytes were streamed from 100769032
2026-10-27T11:03:49 prefetch.3.4.1: 1) 'ERR688359' was downloaded successfully
time=369.19s maxRSS=6828KB
-rw-rw-r-- 1 ubuntu ubuntu 100771369 Oct 27 14:33 ERR688359.sra
2026-10-27T11:04:04 vdb-validate.3.4.1 warn: Couldn't determine SRA Platform; type of table '…/ERR688359/ERR688359.sra' is indeterminate.
2026-10-27T11:04:04 vdb-validate.3.4.1 info: Table 'ERR688359.sra' is consistent
```

</div>

**توضیح خروجی:**
- ‏**SRA Normalized Format**: فایل کامل با کیفیت همه‌ی بازها. گونه‌ی دیگر، **SRA Lite**، کیفیت‌ها را ساده می‌کند و کوچک‌تر است؛ برای فراخوانی واریانت مناسب نیست.
- ‏۱۰۰٫۸ مگابایت در **۶ دقیقه** (نزدیک به ۲۸۰ کیلوبایت در ثانیه از سرور ما). با همین سرعت، ۵۹۵ گیگابایت پروژه نزدیک به **۲۵ روز** می‌شد (تمرین ۷).
- ‏`warn: Couldn't determine SRA Platform` تنها یک هشدار است: در این فایل ستون دستگاه پر نشده (از runinfo می‌دانیم HiSeq 2000 بود)؛ سطر پایانی (`is consistent`) است که درستی را می‌گوید.
- ‏`prefetch` تنها **۷ مگابایت** حافظه گرفت. ‏`is valid` و `is consistent`: فایل سالم رسیده است (`vdb-validate` چک‌سام md5 هر ستون را می‌سنجد).

---

## ۷. گام ۵: `fasterq-dump`؛ از SRA به FASTQ

<div dir="ltr">

```bash
/usr/bin/time -f "time=%es maxRSS=%MKB" fasterq-dump --threads 2 --progress ERR688359
ls -la *.fastq
head -4 ERR688359.fastq
echo "reads: $(( $(wc -l < ERR688359.fastq) / 4 ))"
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`fasterq-dump ERR688359` | پوشه‌ی `ERR688359/` را می‌یابد و FASTQ می‌سازد |
| ‏`--threads 2` | دو رشته‌ی پردازشی (بخش ۰۵: منابع را خودتان تعیین کنید) |
| ‏`$(( … / 4 ))` | حساب پوسته: شمار سطرها بخش بر ۴ = شمار ریدها |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
spots read      : 1,158,189
reads read      : 1,158,189
reads written   : 1,158,189
time=2.18s maxRSS=191112KB
-rw-rw-r-- 1 ubuntu ubuntu 364476846 Oct 27 14:34 ERR688359.fastq
@ERR688359.1 FCD1R36ACXX:8:1101:13034:1994#TGAATCAT length=96
AGAAGAACGCGATCTTAACTTCACTCTGAACAAGAACGGAGAAATATTACGTTTTAAAATCACCAACTGCCCCCTCGCAGACCTCAAATATGCCAA
+ERR688359.1 FCD1R36ACXX:8:1101:13034:1994#TGAATCAT length=96
DFEFHGGHDGIHGIIIJJJJJIIIJJIIIJJIJIJJJIGIIGIGGHIGIJJ@EHFHHHFFFEF>CBDACCDBDBDDDDDDBDBDDCCCADEDDDDD
reads: 1158189
```

</div>

**توضیح خروجی:**
- ‏**۱٬۱۵۸٬۱۸۹** رید: درست همان عدد ENA در ماژول 02/05 (`read_count`). پاسخ معلوم برقرار است.
- ‏FASTQ بازشده **۳۶۴ مگابایت** است، ۳٫۶ برابر فایل SRA. ‏`fasterq-dump` فشرده نمی‌کند؛ اگر نگه می‌دارید، `gzip` بزنید (بخش ۰۲).
- ‏۲ ثانیه و **۱۹۱ مگابایت** حافظه. برای run جفت ۴٫۶ گیگابایتی همین نمونه، فایل‌های موقت چند برابر حجم می‌خواهد؛ پیش از اجرا فضای دیسک را با `df -h .` بسنجید.
- سرخط NCBI با ENA فرق دارد: NCBI ‏`length=96` می‌افزاید و سرخط را در سطر `+` تکرار می‌کند؛ ENA ‏`/1` در پایان دارد و سطر `+` تهی است. توالی و کیفیت **یکسان‌اند** (تمرین ۵).

<details>
<summary>✋ امتحان کن: چطور بی دانلود کامل، چند رید نخست را ببینیم؟</summary>

<div dir="ltr">

```bash
fastq-dump -X 2 -Z ERR688359 | cut -c1-70
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
@ERR688359.1 FCD1R36ACXX:8:1101:13034:1994#TGAATCAT length=96
AGAAGAACGCGATCTTAACTTCACTCTGAACAAGAACGGAGAAATATTACGTTTTAAAATCACCAACTGC
+ERR688359.1 FCD1R36ACXX:8:1101:13034:1994#TGAATCAT length=96
DFEFHGGHDGIHGIIIJJJJJIIIJJIIIJJIJIJJJIGIIGIGGHIGIJJ@EHFHHHFFFEF>CBDACC
@ERR688359.2 FCD1R36ACXX:8:1101:1323:2068#TGAATCAT length=74
CACGCTCAGTCCAAGGAAAATAGTAGCAGCATTCATAATACTGTTGGCTACCGCGTCAAACAGAAGGCTT
+ERR688359.2 FCD1R36ACXX:8:1101:1323:2068#TGAATCAT length=74
DAD8C@<D32+22AA1ACFE9?**1*1?<BFG<**::?*?B*99*??<B*880;';=<E@)...(..6;=
```

</div>

‏`-X 2` تنها دو spot نخست، `-Z` به خروجی استاندارد. ‏`fastq-dump` (ابزار قدیمی‌تر) هنوز برای همین نگاه سریع سودمند است. رید دوم ۷۴ باز است: BGI ریدها را پیش از ثبت **بریده** بود.

</details>

> 📺 **فیلم:** *How to Obtain FASTQ from SRA (NCBI) using prefetch and fastq-dump*: https://www.youtube.com/watch?v=dYyj8sFxago
> 📄 **مرجع:** ‏SRA Toolkit wiki (نصب، `prefetch`، `fasterq-dump`): https://github.com/ncbi/sra-tools/wiki

---

## ۸. سه اشتباه رایج

1. **دانلود پیش از شمردن.** پروژه‌ای که «۱۵۶ نمونه» دارد، ۵۹۵ گیگابایت است. نخست runinfo، `size_MB` و `df -h`.
2. **برداشتن تنها یک run از نمونه.** ‏`ERR688359` تنها ۳٫۴٪ ریدهای نمونه‌ی SAMEA3136648 است. همه‌ی runهای یک BioSample را با ستون ۲۶ runinfo پیدا کنید.
3. **جست‌وجوی شناسه بی برچسب.** ‏`PRJEB7774` ‏۵ پروژه و `SAMEA3136648` ‏۹۵ نمونه داد. ‏`[Project Accession]`، `[accn]` و `[BioProject]` بگذارید.

---

## 📘 برای کنجکاوها

- ‏**`--split-files` و `--split-3`:** برای run جفت، `fasterq-dump` به گونه‌ی پیش‌فرض دو فایل `_1.fastq` و `_2.fastq` می‌سازد، و ریدهای بی‌جفت را در فایل سوم (`--split-3`). تمرین ۳ همین را روی `ERR688506` با سه spot نشان می‌دهد.
- ‏**SRA در ابر:** همه‌ی SRA روی AWS و Google Cloud هم هست؛ اگر محاسبه را همان‌جا انجام دهید، دانلود ندارید. ماژول 11/08 (Pathogen Detection) به داده‌ی AMR در ابر اشاره می‌کند.
- ‏**ENA یا SRA؟** برای دانلود ساده‌ی FASTQ، ENA فایل `fastq.gz` آماده و md5 می‌دهد (02/05)؛ SRA Toolkit فایل را خودش می‌سنجد و برای فرمت‌های ویژه (کیفیت کامل، چند فایل) انعطاف بیشتری دارد.

---

## جمع‌بندی

- ‏BioProject → BioSample → Experiment → Run؛ پیشوندها (`PRJEB`، `SAMEA`، `ERX`، `ERR`) جای ثبت و لایه را می‌گویند.
- ‏runinfo پیش از دانلود: ‏PRJEB7774 = ‏۳۱۲ run، ۱۵۶ نمونه، هر نمونه یک run جفت و یک تک، ۵۹۵ گیگابایت.
- ‏BioSample ‏SAMEA3136648: مدفوع گروه شاهد، اتریش، ۲۰۱۳.
- ‏`prefetch` → `vdb-validate` → `fasterq-dump`: ‏۱٬۱۵۸٬۱۸۹ رید، برابر با ENA، با توالی و کیفیت یکسان.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
esearch -db bioproject -query "PRJxx[Project Accession]" | esummary | xtract -pattern DocumentSummary -element Project_Acc Project_Title
curl … esearch db=sra term=PRJxx[BioProject] usehistory=y; efetch db=sra rettype=runinfo   # runinfo.csv
cut -d, -f13,16,19,20 runinfo.csv | sort | uniq -c        # strategy, layout, platform, model
curl … esearch db=biosample term=SAMxx[accn]; efetch db=biosample                          # attributes
prefetch RUN && vdb-validate RUN && fasterq-dump --threads 2 RUN
fastq-dump -X 2 -Z RUN                                      # quick look, no full download
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| فراداده (metadata) | داده درباره‌ی داده: نمونه از کجا، کی، با کدام دستگاه |
| ‏BioProject | رکورد یک پژوهش و همه‌ی داده‌هایش |
| ‏BioSample | رکورد یک نمونه‌ی زیستی با ویژگی‌هایش |
| ‏Experiment | یک کتابخانه‌ی توالی‌یابی از یک نمونه، روی یک دستگاه |
| ‏Run | یک بسته‌ی داده‌ی خام از یک Experiment |
| ‏spot | واحد SRA: یک رید یا یک جفت‌رید |
| ‏INSDC | همکاری NCBI، ENA و DDBJ برای هم‌سان نگه داشتن داده‌ها |
| ‏runinfo | جدول CSV یک سطر برای هر run |
| ‏TPA | ثبت تحلیل دوباره‌ی داده‌ی دیگران (Third Party Annotation) |
| ‏MAG | ژنومی که از داده‌ی متاژنوم بازسازی شده است |
| ‏SRA Lite | گونه‌ی سبک‌تر فایل SRA با کیفیت ساده‌شده |

---

## منابع

**مقاله و مستند**
- ‏Barrett T, et al. (2012). *BioProject and BioSample databases at NCBI: facilitating capture and organization of metadata.* Nucleic Acids Res 40(D1):D57–D63. https://doi.org/10.1093/nar/gkr1163
- ‏Katz K, et al. (2022). *The Sequence Read Archive: a decade more of explosive growth.* Nucleic Acids Res 50(D1):D387–D390. https://doi.org/10.1093/nar/gkab1053
- ‏Feng Q, et al. (2015). *Gut microbiome development along the colorectal adenoma–carcinoma sequence.* Nature Communications 6:6528. https://doi.org/10.1038/ncomms7528 (پروژه‌ی PRJEB7774)
- ‏SRA Toolkit wiki: https://github.com/ncbi/sra-tools/wiki · مستندات SRA: https://www.ncbi.nlm.nih.gov/sra/docs/

**کتاب**
- ‏Buffalo V (2015). *Bioinformatics Data Skills.* O'Reilly. (فصل ۶: داده‌ی بیوانفورماتیک؛ دانلود، چک‌سام و فشرده‌سازی)
- ‏Pevsner J (2015). *Bioinformatics and Functional Genomics*, 3rd ed. Wiley-Blackwell. (فصل ۹: توالی‌یابی نسل نو و SRA)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins): https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Genomic Data Science* (UC San Diego): https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science
- ‏YouTube: *How to Obtain FASTQ from SRA (NCBI) using prefetch and fastq-dump* (Luís Miguel Gonçalves): https://www.youtube.com/watch?v=dYyj8sFxago
- ‏YouTube: *NCBI's Sequence Read Archive: Downloading sequences* (Dranalytics): https://www.youtube.com/watch?v=evlIjjlIUBA

<sub>همه‌ی دستورها در 2026-10-27 روی سرور دوره اجرا شدند؛ SRA Toolkit 3.4.1 از بسته‌ی bioconda ‏`sra-tools-3.4.1`. DOIها با doi.org و صفحه‌ها با درخواست مستقیم (HTTP 200) وارسی شدند؛ فیلم‌ها با noembed.</sub>

</div>
