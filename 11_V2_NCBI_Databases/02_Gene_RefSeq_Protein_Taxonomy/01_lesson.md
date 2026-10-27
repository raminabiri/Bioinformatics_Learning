<div dir="rtl">

# درس: Gene، RefSeq، Protein، IPG، CDD و Taxonomy؛ از یک ژن به همه‌ی چهره‌هایش

**بخش:** `11_V2_NCBI_Databases` · **ماژول:** `02_Gene_RefSeq_Protein_Taxonomy` · **پیش‌نیاز:** ماژول [11/01](../01_Entrez_EDirect/) (E-utilities، EDirect، `xtract`، سرور تاریخچه) · **زمان:** حدود ۹۰ دقیقه · **ابزار:** curl 8.20.0، EDirect 24.0، NCBI Datasets CLI 18.38.0 · **آخرین بازبینی:** 2026-10-27

> ✅ **وضعیت: اجرا شده.** همه‌ی خروجی‌ها واقعی‌اند (2026-10-27). شمار رکوردها (به‌ویژه در IPG) هر هفته بالا می‌رود؛ شناسه‌ها و طول‌ها نه.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. فرق **GenBank** و **RefSeq** را بگویید و پیشوندهای RefSeq (`NC_`، `NG_`، `NM_`، `NR_`، `NP_`، `XM_`، `XP_`، `WP_`) را بخوانید.
2. از یک ژن انسانی (NR3C1، گیرنده‌ی گلوکوکورتیکوئید) به همه‌ی رونوشت‌ها و پروتئین‌هایش برسید و **رونوشت MANE** را بشناسید.
3. با **IPG** (Identical Protein Groups) ببینید یک پروتئین باکتریایی در چند ژنوم و چند گونه تکرار شده است.
4. دامنه‌های حفظ‌شده‌ی یک پروتئین را از **CDD** بگیرید.
5. جایگاه یک جاندار را در **Taxonomy** بیابید و دودمان (lineage) آن را چاپ کنید.

**پیش از آغاز:**

<div dir="ltr">

```bash
mkdir -p ~/ncbi/m02 && cd ~/ncbi/m02
B=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
```

</div>

---

## ۱. داستان

در ماژول 11/01 ژن *rpoB* سیزده رکورد پروتئین داشت ولی تنها یکی RefSeq بود. چرا یک پروتئین سیزده بار ثبت می‌شود؟ کدام را باید برداشت؟ و در ژن‌های انسانی که هر ژن چندین **رونوشت** (transcript) دارد، کدام رونوشت «همان» ژن است؟ در این درس دو ژن رشته‌ی دوره را کنار هم می‌گذاریم: **rpoB** باکتریایی (یک ژن، یک پروتئین، ولی در صدها هزار ژنوم) و **NR3C1** انسانی (یک ژن، ۲۲ رونوشت). ‏NR3C1 گیرنده‌ی داروی **دگزامتازون** است که در ماژول 11/04 (GEO) و بخش ۱۳ (RNA-seq) دوباره می‌بینیدش.

---

## ۲. مفهوم به زبان ساده

### ‏۲.۱ ‏GenBank در برابر RefSeq

| | GenBank | RefSeq |
| :--- | :--- | :--- |
| **چه کسی می‌نویسد** | پژوهشگران (ثبت‌کننده) | ‏NCBI، از روی رکوردهای GenBank |
| **تکرار** | یک توالی ممکن است ده‌ها بار ثبت شود | یک رکورد برای هر مولکول در هر جاندار |
| **دگرگونی** | تنها ثبت‌کننده می‌تواند دگرگون کند | ‏NCBI به‌روز می‌کند (نسخه بالا می‌رود) |
| **accession** | دو حرف + شش رقم (`AAC76961`) | دو حرف + `_` (`NP_418414`) |

**تشبیه:** GenBank مانند همه‌ی نسخه‌های دست‌نویس یک کتاب در کتابخانه‌های گوناگون است؛ RefSeq یک ویراست ویراستاری‌شده از همان کتاب.

### ۲.۲ پیشوندهای RefSeq

| پیشوند | مولکول | نمونه در این درس |
| :--- | :--- | :--- |
| ‏`NC_` | کروموزوم یا ژنوم کامل | ‏`NC_000913.3` (*E. coli* K-12)، `NC_000005.10` (کروموزوم ۵ انسان) |
| ‏`NG_` | ناحیه‌ی ژنومی یک ژن (RefSeqGene) | ‏`NG_009062.1` (NR3C1) |
| ‏`NM_` / `NR_` | ‏mRNA کدکننده / RNA ناکدکننده، **بازبینی‌شده** | ‏`NM_000176.3`، `NR_157096.2` |
| ‏`XM_` / `XR_` | همان، ولی **پیش‌بینی** رایانه‌ای | ‏(NR3C1 ندارد؛ تمرین ۶) |
| ‏`NP_` / `XP_` | پروتئین از `NM_` / از `XM_` | ‏`NP_000167.1`، `NP_418414.1` |
| ‏`WP_` | پروتئین **ناوابسته به یک ژنوم** در باکتری‌ها | ‏`WP_000263098.1` |

حرف **N** یعنی رکورد را کارشناس دیده یا از شواهد تجربی آمده؛ **X** یعنی پیش‌بینی خودکار. در گزارش، تا جای ممکن `NM_`/`NP_` به کار ببرید.

> 📺 **فیلم:** *RefSeq and NCBI Gene* (ClinGen Resource؛ Terence Murphy از NCBI): https://www.youtube.com/watch?v=1ndnACFDpmc
> 📄 **مرجع:** O'Leary NA, et al. (2016). *Reference sequence (RefSeq) database at NCBI: current status, taxonomic expansion, and functional annotation.* Nucleic Acids Res 44(D1):D733–D745. https://doi.org/10.1093/nar/gkv1189

---

## ۳. گام ۱: ژن NR3C1 و همه‌ی مولکول‌هایش

**چرا؟** نخست باید بدانیم ژن کجاست و چند رونوشت و پروتئین به آن پیوند دارد.

<div dir="ltr">

```bash
esearch -db gene -query "NR3C1[preferred symbol] AND human[orgn]" | esummary \
  | xtract -pattern DocumentSummary -element Id Name Description -block GenomicInfoType -element ChrAccVer ChrStart ChrStop
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
2908	NR3C1	nuclear receptor subfamily 3 group C member 1	NC_000005.10	143435511	143277930
```

</div>

‏Gene ID **2908** روی کروموزوم ۵ (`NC_000005.10`، اسمبلی GRCh38). آغاز > پایان، پس **رشته‌ی منفی**؛ طول ناحیه ۱۵۷٬۵۸۲ باز. ژن انسانی بسیار بلندتر از ژن باکتریایی است، چون بیشترش **اینترون** است.

حالا شمار پیوندها با سه نام پیوند (درس 11/01: «شمار `<Id>` منهای یک»):

<div dir="ltr">

```bash
for ln in gene_nuccore gene_nuccore_refseqrna gene_nuccore_refseqgene; do
  echo "$ln $(curl -sS "$B/elink.fcgi?dbfrom=gene&db=nuccore&id=2908&linkname=$ln" | grep -c '<Id>')"; sleep 0.4
done
for ln in gene_protein gene_protein_refseq; do
  echo "$ln $(curl -sS "$B/elink.fcgi?dbfrom=gene&db=protein&id=2908&linkname=$ln" | grep -c '<Id>')"; sleep 0.4
done
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
gene_nuccore 126
gene_nuccore_refseqrna 23
gene_nuccore_refseqgene 2
gene_protein 192
gene_protein_refseq 22
```

</div>

**توضیح خروجی (پس از کم کردن یک):**
- ‏**۱۲۵** رکورد نوکلئوتیدی (بیشترشان GenBank: کلون‌ها، cDNAها، رکوردهای قدیمی)، ولی تنها **۲۲** رونوشت RefSeq و **۱** RefSeqGene.
- ‏**۱۹۱** پروتئین، ولی تنها **۲۱** پروتئین RefSeq.
- **دام:** اگر `elink -target nuccore | efetch` را بی پالایش بزنید، صدها رکورد ناخواسته می‌گیرید و زمان زیادی می‌برد. ما در آزمون این درس همین را دیدیم: لوله‌ی بی‌پالایش پیش از رسیدن به پاسخ از مرز زمان (`timeout`) گذشت. **همیشه نخست بشمارید، سپس بگیرید.**

---

## ۴. گام ۲: رونوشت‌های RefSeq و پیشوندهایشان

**چرا؟** می‌خواهیم ببینیم ۲۲ رونوشت از کدام گونه‌اند. با سرور تاریخچه (11/01، گام ۶):

<div dir="ltr">

```bash
curl -sS "$B/elink.fcgi?dbfrom=gene&db=nuccore&id=2908&linkname=gene_nuccore_refseqrna&cmd=neighbor_history" > h.xml
WE=$(grep -o '<WebEnv>[^<]*' h.xml | cut -d'>' -f2)
QK=$(grep -o '<QueryKey>[^<]*' h.xml | cut -d'>' -f2); echo "QK=$QK"
curl -sS "$B/efetch.fcgi?db=nuccore&query_key=$QK&WebEnv=$WE&rettype=acc" > nr3c1_rna.acc
wc -l < nr3c1_rna.acc
cut -c1-3 nr3c1_rna.acc | sort | uniq -c
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`cmd=neighbor_history` بی `esearch` | ‏`elink` با یک `id` هم می‌تواند فهرست را روی سرور بگذارد و WebEnv تازه بدهد |
| ‏`rettype=acc` | تنها accession.version هر رکورد، یک در هر سطر |
| ‏`cut -c1-3` | سه نویسه‌ی نخست = پیشوند (`NM_`، `NR_`، …) |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
QK=1
22
     21 NM_
      1 NR_
```

</div>

‏**۲۱** ‏mRNA کدکننده (`NM_`) و **۱** ‏RNA ناکدکننده (`NR_`). هیچ `XM_`ی نیست: NR3C1 ژنی پرپژوهش است و همه‌ی رونوشت‌هایش بازبینی شده‌اند. ‏۲۱ رونوشت کدکننده یعنی ۲۱ پروتئین (`NP_`)؛ همان ۲۱ گام ۱. این‌ها **ایزوفرم**‌های گیرنده‌اند: از **پیرایش جایگزین** (alternative splicing) و آغازگاه‌های گوناگون ترجمه می‌آیند (مانند GRα و GRβ).

### ۴.۱ کدام رونوشت؟ MANE Select

با ۲۱ رونوشت، کدام را برای گزارش یک جهش بنویسید؟ **MANE** (Matched Annotation from NCBI and EMBL-EBI) برای هر ژن انسانی کدکننده **یک** رونوشت برگزیده دارد که در NCBI و Ensembl یکسان است.

<div dir="ltr">

```bash
curl -sS "$B/efetch.fcgi?db=nuccore&id=NM_000176.3&rettype=gb&retmode=text" > NM_000176.gb
grep -E '^(LOCUS|DEFINITION|KEYWORDS)' NM_000176.gb
grep -E '/protein_id|^ +CDS' NM_000176.gb | head -2
grep -c '^ \+exon' NM_000176.gb
grep -i 'MANE Ensembl' NM_000176.gb
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
LOCUS       NM_000176               6778 bp    mRNA    linear   PRI 28-APR-2025
DEFINITION  Homo sapiens nuclear receptor subfamily 3 group C member 1 (NR3C1),
KEYWORDS    RefSeq; MANE Select.
     CDS             490..2823
                     /protein_id="NP_000167.1"
9
            MANE Ensembl match     :: ENST00000394464.7/ ENSP00000377977.2
```

</div>

**توضیح خروجی:**
- ‏`KEYWORDS … MANE Select`: این همان رونوشت برگزیده است، و همتای Ensembl آن `ENST00000394464.7` (بخش ۱۲ این شناسه‌ها را می‌کاود).
- ‏`CDS 490..2823`: بخش کدکننده از باز ۴۹۰ تا ۲۸۲۳ این mRNA؛ پیش از آن **5′ UTR** و پس از آن **3′ UTR** است. طول CDS: ‏۲۸۲۳ − ۴۹۰ + ۱ = ۲۳۳۴ = ۷۷۸ کُدون، یعنی **۷۷۷** اسید آمینه + کُدون پایان.
- ‏**۹** اگزون.

بسنجیم:

<div dir="ltr">

```bash
curl -sS "$B/efetch.fcgi?db=protein&id=NP_000167.1&rettype=fasta&retmode=text" | grep -v '>' | tr -d '\n' | wc -c
curl -sS "$B/efetch.fcgi?db=protein&id=NP_000167.1&rettype=fasta&retmode=text" | head -1
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
777
>NP_000167.1 glucocorticoid receptor isoform alpha [Homo sapiens]
```

</div>

‏**۷۷۷** اسید آمینه: **GRα**، ایزوفرم اصلی گیرنده‌ی گلوکوکورتیکوئید.

> 📺 **فیلم:** *RefSeqGene* (National Library of Medicine): https://www.youtube.com/watch?v=zs46Ur0m0mc
> 📄 **مرجع:** Morales J, et al. (2022). *A joint NCBI and EMBL-EBI transcript set for clinical genomics and research.* Nature 604:310–315. https://doi.org/10.1038/s41586-022-04558-8

---

## ۵. گام ۳: NCBI Datasets؛ همان پاسخ در یک دستور

**چرا؟** ‏**NCBI Datasets** ابزار تازه‌تر NCBI است: به جای ساختن پرسش Entrez، شیء زیستی (ژن، ژنوم، ویروس) را با نامش می‌خواهید و پاسخ را در **JSON** می‌گیرید. ‏`dataformat` آن را به جدول برمی‌گرداند.

<div dir="ltr">

```bash
datasets --version
datasets summary gene symbol NR3C1 --taxon human --as-json-lines \
  | dataformat tsv gene --fields gene-id,symbol,tax-id,chromosomes,transcript-count,protein-count,swissprot-accessions
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`summary gene symbol NR3C1` | خلاصه‌ی ژن را با نامش بخواه (بی دانلود توالی) |
| ‏`--taxon human` | جاندار؛ نام یا TaxID |
| ‏`--as-json-lines` | هر ژن یک سطر JSON (برای لوله) |
| ‏`dataformat tsv gene --fields …` | ‏JSON → جدول Tab‌دار با ستون‌های برگزیده |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
datasets version: 18.38.0
NCBI GeneID	Symbol	Taxonomic ID	Chromosomes	Transcripts	Proteins	SwissProt Accessions
2908	NR3C1	9606	5	22	21	P04150
```

</div>

همان ۲۲ رونوشت و ۲۱ پروتئین گام ۲، از راهی دیگر، همراه با شناسه‌ی UniProt/Swiss-Prot (`P04150`). ‏`datasets` نسخه‌ی تازه‌تر را هم گزارش می‌کند (سطری درباره‌ی 18.40.0 در stderr)؛ برای این درس فرقی ندارد.

> 📺 **فیلم:** *How to Download Large Datasets from NCBI using Datasets Command Line* (SOBP): https://www.youtube.com/watch?v=85TzdIqzJhs
> 📄 **مرجع:** O'Leary NA, et al. (2024). *Exploring and retrieving sequence and metadata for species across the tree of life with NCBI Datasets.* Scientific Data 11. https://doi.org/10.1038/s41597-024-03571-y

---

## ۶. گام ۴: پروتئین‌های یکسان (IPG) و `WP_`

**چرا؟** در 11/01 پروتئین rpoB در MG1655 سیزده رکورد داشت. ولی همین پروتئین، **حرف به حرف یکسان**، در ژنوم‌های بی‌شمار دیگر هم هست. ‏**IPG** همه‌ی رکوردهای پروتئینی با توالی یکسان را در یک «گروه» می‌گذارد.

<div dir="ltr">

```bash
curl -sS -G "$B/esearch.fcgi" --data-urlencode db=ipg --data-urlencode "term=NP_418414.1" | grep -oE '<(Count|Id)>[^<]*' | head -2
curl -sS "$B/esummary.fcgi?db=ipg&id=1258700" > ipg_sum.xml
grep -oE '<(Accession|Title|Slen|Organism|ProteinCount|TaxIdCount|SpeciesCount|GeneraCount|AssemblyCount)>[^<]*' ipg_sum.xml
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
<Count>1
<Id>1258700
<Title>DNA-directed RNA polymerase subunit beta
<ProteinCount>402479
<Accession>WP_000263098.1
<Slen>1342
<Organism>Bacteria
<TaxIdCount>3258
<SpeciesCount>409
<GeneraCount>6
<AssemblyCount>446378
```

</div>

**توضیح خروجی:**
- همین توالی ۱۳۴۲ اسید آمینه‌ای در **۴۰۲٬۴۷۹** رکورد پروتئینی، از **۴۴۶٬۳۷۸** اسمبلی ژنوم، **۴۰۹** گونه و **۶** جنس آمده است! ‏rpoB بسیار **حفظ‌شده** است (آنزیم پایه‌ی رونویسی) و *E. coli* پرتوالی‌یابی‌شده‌ترین باکتری است؛ و *Shigella* و چند جنس نزدیک همین توالی را دارند.
- ‏`Organism` تنها **Bacteria** است، چون گروه چند جنس را در بر دارد.
- نماینده‌ی گروه **`WP_000263098.1`** است. ‏`WP_` برای همین کار ساخته شد: به جای ۴۰۰ هزار `NP_`/`YP_` برای هر ژنوم، **یک** رکورد ناوابسته به ژنوم برای هر توالی پروتئین یکسان.

پیوند مستقیم از `NP_` به `WP_` (نام پیوند `protein_protein_ref2wp`؛ UID ‏`16131817` همان `NP_418414.1` است، درس 11/01):

<div dir="ltr">

```bash
w=$(curl -sS "$B/elink.fcgi?dbfrom=protein&db=protein&id=16131817&linkname=protein_protein_ref2wp" \
    | grep -o '<Id>[^<]*' | cut -d'>' -f2 | tail -n +2)
echo "WP uid: $w"
curl -sS "$B/efetch.fcgi?db=protein&id=$w&rettype=acc"
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
WP uid: 446185243
WP_000263098.1
```

</div>

‏`tail -n +2` از سطر دوم به بعد را می‌دهد؛ یعنی شناسه‌ی آغاز (نخستین `<Id>`) را کنار می‌گذارد.

<details>
<summary>✋ امتحان کن: چرا `efetch -format ipg` (گزارش کامل IPG) را برای rpoB نزنیم؟</summary>

چون یک سطر برای **هر** یک از ۴۰۲٬۴۷۹ رکورد می‌دهد. ما آن را آزمودیم: پس از دو دقیقه فایل از ۳۷ مگابایت گذشته بود و هنوز می‌آمد؛ آن را بستیم. برای پروتئین‌های پرتکرار `esummary` (چند عدد) بس است. گزارش کامل IPG برای پروتئین‌های کم‌یاب (مانند یک ژن مقاومت تازه) سودمند است.

</details>

> 📺 **فیلم:** *RefSeq and NCBI Gene* (بخش پروتئین‌های باکتریایی): https://www.youtube.com/watch?v=1ndnACFDpmc
> 📄 **مرجع:** صفحه‌ی راهنمای Identical Protein Groups: https://www.ncbi.nlm.nih.gov/ipg/docs/about/ · O'Leary NA, et al. (2016). Nucleic Acids Res 44:D733–D745 (بخش WP_). https://doi.org/10.1093/nar/gkv1189

---

## ۷. گام ۵: دامنه‌های حفظ‌شده (CDD)

**چرا؟** پروتئین از **دامنه**‌ها (domain) ساخته شده است: بخش‌هایی که جدا تا می‌خورند و کار جدایی دارند. ‏**CDD** (Conserved Domain Database) مدل این دامنه‌هاست و NCBI آن‌ها را از پیش روی پروتئین‌ها نگاشته است.

<div dir="ltr">

```bash
elink -db protein -id 4504133 -target cdd | esummary | xtract -pattern DocumentSummary -element Accession Title
```

</div>

‏`4504133` UID پروتئین `NP_000167.1` (GRα) است (نخستین `<Id>` در پاسخ `elink` برای آن).

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
pfam02155	GCR
cd07172	NR_DBD_GR_PR
cd07076	NR_LBD_GR
```

</div>

همان لوله با `-element Accession Title Subtitle` (شرح هر کدام؛ `cut -c1-110` سطرها را کوتاه می‌کند):

<div dir="ltr">

```
pfam02155	GCR	Glucocorticoid receptor
cd07172	NR_DBD_GR_PR	DNA-binding domain of glucocorticoid receptor (GR) is composed of two C4-type zinc finger
cd07076	NR_LBD_GR	Ligand binding domain of the glucocorticoid receptor, a member of the nuclear receptor super
```

</div>

**توضیح خروجی:** سه دامنه = سه بخش کارکردی گیرنده:
- ‏**GCR** (`pfam02155`): بخش آغازی (N-terminal) که رونویسی را فعال می‌کند.
- ‏**DBD** (`cd07172`): دامنه‌ی **اتصال به DNA** با دو «انگشت روی» (zinc finger)؛ به توالی‌های پاسخ به گلوکوکورتیکوئید (GRE) در پیش‌برِ ژن‌های هدف می‌چسبد.
- ‏**LBD** (`cd07076`): دامنه‌ی **اتصال لیگاند**؛ جایی که دگزامتازون می‌نشیند.

پیشوند هر شناسه منبع مدل را می‌گوید: `cd` = مدل خود NCBI، `pfam` = از Pfam، `PRK`/`TIGR` = خانواده‌های پروتئینی بزرگ، `cl` = ابرخانواده.

**دام:** این پیوندها برای همه‌ی رکوردها از پیش ساخته نشده‌اند. برای `NP_418414.1` (rpoB) پیوند CDD **نبود**؛ برای `WP_000263098.1` بود (تمرین ۵). اگر پیوندی نیامد، **CD-Search** (https://www.ncbi.nlm.nih.gov/Structure/cdd/wrpsb.cgi) را با خود توالی بزنید.

> 📺 **فیلم:** *Gene Conserved Domains* (Abnova): https://www.youtube.com/watch?v=UX7amIyT3xw
> 📄 **مرجع:** Wang J, et al. (2023). *The conserved domain database in 2023.* Nucleic Acids Res 51(D1):D384–D388. https://doi.org/10.1093/nar/gkac1096

---

## ۸. گام ۶: Taxonomy؛ جاندار در درخت زندگی

**چرا؟** هر رکورد NCBI به یک **TaxID** بسته است. در 11/01 دیدید `txid511145` یک زیرسویه و `[orgn]` یک گروه است. ‏Taxonomy می‌گوید هر TaxID کجای درخت است.

<div dir="ltr">

```bash
efetch -db taxonomy -id 511145,562,9606 -format xml \
  | xtract -pattern Taxon -element TaxId ScientificName Rank Division
efetch -db taxonomy -id 511145 -format xml \
  | xtract -pattern Taxon -block LineageEx -sep ' > ' -element ScientificName
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`-pattern Taxon` | هر جاندار یک سطر |
| ‏`Rank` | رده (species، genus، …) |
| ‏`Division` | بخش بزرگ (Bacteria، Primates، …) |
| ‏`-block LineageEx` | همه‌ی نیاکان، از ریشه |
| ‏`-sep ' > '` | جداکننده‌ی میان چند مقدار یک فیلد (به جای Tab) |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
562	Escherichia coli	species	Bacteria
9606	Homo sapiens	species	Primates
511145	Escherichia coli str. K-12 substr. MG1655	no rank	Bacteria
cellular organisms > Bacteria > Pseudomonadati > Pseudomonadota > Gammaproteobacteria > Enterobacterales > Enterobacteriaceae > Escherichia > Escherichia coli > Escherichia coli K-12
```

</div>

**توضیح خروجی:**
- ترتیب خروجی ترتیب ورودی نیست (562 پیش از 511145 آمد). اگر ترتیب مهم است، با ستون `TaxId` جفت کنید، نه با شماره‌ی سطر.
- ‏MG1655 رده‌ی **no rank** دارد: زیر گونه، NCBI رده‌ی رسمی برای «زیرسویه» ندارد (برای برخی سویه‌ها رده‌ی `strain` می‌گذارد؛ تمرین ۴).
- دودمان: *E. coli* K-12 → *E. coli* → *Escherichia* → Enterobacteriaceae → … → Bacteria. ‏`Pseudomonadota` نام تازه‌ی Proteobacteria است (بازنگری رده‌بندی ۲۰۲۱ تا ۲۰۲۴)؛ در مقاله‌های پیش از ۲۰۲۱ نام قدیمی را می‌بینید.

> 📺 **فیلم:** *E-Utilities Introduction* (NLM؛ بخش پایگاه‌ها): https://www.youtube.com/watch?v=BCG-M5k-gvE
> 📄 **مرجع:** Schoch CL, et al. (2020). *NCBI Taxonomy: a comprehensive update on curation, resources and tools.* Database 2020:baaa062. https://doi.org/10.1093/database/baaa062

---

## ۹. سه اشتباه رایج

1. **برداشتن نخستین رکورد GenBank.** ‏NR3C1 ‏۱۹۱ پروتئین دارد؛ بسیاری تکه‌ای، قدیمی یا تکراری‌اند. برای انسان `NM_`/`NP_` و رونوشت **MANE Select**، و برای باکتری `WP_` یا `NP_` ژنوم مرجع.
2. **گزارش بی نسخه.** ‏`NM_000176` بی `.3` نمی‌گوید کدام توالی. مختصات یک جهش در نام‌گذاری HGVS (مانند `NM_000176.3:c.…`) تنها با نسخه معنا دارد، چون با هر نسخه ممکن است UTR جابه‌جا شود.
3. **گرفتن همه‌ی پیوندها بی شمردن.** ‏`elink -target nuccore | efetch` برای یک ژن انسانی صدها رکورد می‌آورد (گام ۱). نخست `Count` یا `grep -c '<Id>'`، سپس `linkname` یا `efilter`.

---

## 📘 برای کنجکاوها

- ‏**RefSeqGene (`NG_`)** ناحیه‌ی ژن با چند هزار باز پیرامونش است و پایه‌ی نام‌گذاری HGVS در سطح ژنوم (`NG_009062.1:g.…`) در آزمایشگاه‌های بالینی. ماژول 11/05 همین را می‌کاود.
- ‏**`datasets download gene symbol NR3C1 --taxon human`** یک فایل zip با توالی ژن، رونوشت‌ها و پروتئین‌ها می‌دهد؛ برای بیش از چند ژن ساده‌تر از E-utilities است.
- ‏**Swiss-Prot** (`P04150`) پایگاه پروتئین بازبینی‌شده‌ی UniProt است، بیرون از NCBI؛ در بخش ۱۲ با InterPro به آن برمی‌گردیم.

---

## جمع‌بندی

- ‏GenBank بایگانی ثبت‌هاست؛ RefSeq ویراست بی‌تکرار NCBI. پیشوند (`NC_`، `NG_`، `NM_`، `NR_`، `NP_`، `XM_`، `WP_`) گونه‌ی مولکول و میزان بازبینی را می‌گوید.
- ‏NR3C1 (Gene ID 2908): ‏۲۱ ‏`NM_` + ۱ ‏`NR_`، ‏۲۱ ‏`NP_`؛ MANE Select ‏`NM_000176.3` → ‏`NP_000167.1` (GRα، ۷۷۷ اسید آمینه، ۹ اگزون).
- ‏IPG: پروتئین rpoB (`WP_000263098.1`) در ۴۰۲ هزار رکورد و ۴۰۹ گونه یکسان است.
- ‏CDD: سه دامنه‌ی GR (بخش فعال‌کننده، DBD، LBD).
- ‏Taxonomy: ‏`xtract -block LineageEx` دودمان را می‌دهد؛ ترتیب خروجی را با TaxID جفت کنید.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
curl -sS "$B/elink.fcgi?dbfrom=gene&db=nuccore&id=GENEID&linkname=gene_nuccore_refseqrna" | grep -c '<Id>'   # minus 1
curl -sS "$B/efetch.fcgi?db=nuccore&id=NM_x.v&rettype=gb&retmode=text" | grep -E '^(LOCUS|KEYWORDS)'
datasets summary gene symbol SYMBOL --taxon TAXON --as-json-lines | dataformat tsv gene --fields gene-id,symbol,transcript-count,protein-count
curl -sS -G "$B/esearch.fcgi" --data-urlencode db=ipg --data-urlencode "term=PROTEIN_ACC"   # then esummary db=ipg
elink -db protein -id UID -target cdd | esummary | xtract -pattern DocumentSummary -element Accession Title
efetch -db taxonomy -id TAXID -format xml | xtract -pattern Taxon -block LineageEx -sep ' > ' -element ScientificName
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏RefSeq | مجموعه‌ی توالی مرجع بی‌تکرار و بازبینی‌شده‌ی NCBI |
| رونوشت (transcript) | یک مولکول RNA ساخته‌شده از ژن |
| ایزوفرم (isoform) | گونه‌های گوناگون یک پروتئین از یک ژن |
| پیرایش جایگزین (alternative splicing) | پیوند دادن اگزون‌ها به چند ترتیب گوناگون |
| ‏MANE Select | رونوشت برگزیده‌ی مشترک NCBI و Ensembl برای هر ژن انسانی |
| ‏CDS | بخش کدکننده‌ی پروتئین در یک mRNA |
| ‏UTR | بخش ترجمه‌نشده‌ی پیش (5′) یا پس (3′) از CDS |
| ‏IPG | گروه همه‌ی رکوردهای پروتئینی با توالی یکسان |
| ‏`WP_` | پروتئین RefSeq ناوابسته به یک ژنوم (باکتری‌ها) |
| دامنه (domain) | بخش جدا تاخورده و کارکردی یک پروتئین |
| ‏CDD | پایگاه مدل‌های دامنه‌ی حفظ‌شده در NCBI |
| دودمان (lineage) | زنجیره‌ی نیاکان یک جاندار در رده‌بندی |
| ‏rank | رده‌ی رده‌بندی (species، genus، …) |

---

## منابع

**مقاله و مستند**
- ‏O'Leary NA, et al. (2016). *Reference sequence (RefSeq) database at NCBI: current status, taxonomic expansion, and functional annotation.* Nucleic Acids Res 44(D1):D733–D745. https://doi.org/10.1093/nar/gkv1189
- ‏Morales J, et al. (2022). *A joint NCBI and EMBL-EBI transcript set for clinical genomics and research.* Nature 604:310–315. https://doi.org/10.1038/s41586-022-04558-8
- ‏O'Leary NA, et al. (2024). *Exploring and retrieving sequence and metadata for species across the tree of life with NCBI Datasets.* Scientific Data 11. https://doi.org/10.1038/s41597-024-03571-y
- ‏Wang J, et al. (2023). *The conserved domain database in 2023.* Nucleic Acids Res 51(D1):D384–D388. https://doi.org/10.1093/nar/gkac1096
- ‏Schoch CL, et al. (2020). *NCBI Taxonomy: a comprehensive update on curation, resources and tools.* Database 2020:baaa062. https://doi.org/10.1093/database/baaa062
- ‏Brown GR, et al. (2015). *Gene: a gene-centered information resource at NCBI.* Nucleic Acids Res 43(D1):D36–D42. https://doi.org/10.1093/nar/gku1055

**کتاب**
- ‏Pevsner J (2015). *Bioinformatics and Functional Genomics*, 3rd ed. Wiley-Blackwell. (فصل ۲: GenBank، RefSeq و accession)
- ‏Baxevanis AD, Bader GD, Wishart DS (eds.) (2020). *Bioinformatics*, 4th ed. Wiley. (فصل‌های پایگاه‌های توالی و پایگاه‌های پروتئین)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Access Bioinformatics Databases with Biopython*: https://www.coursera.org/projects/access-bioinformatics-databases-with-biopython
- ‏edX: *Introduction to Genomic Data Science* (UC San Diego): https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science
- ‏YouTube: *RefSeq and NCBI Gene* (ClinGen Resource): https://www.youtube.com/watch?v=1ndnACFDpmc
- ‏YouTube: *RefSeqGene* (National Library of Medicine): https://www.youtube.com/watch?v=zs46Ur0m0mc
- ‏YouTube: *Gene Conserved Domains* (Abnova): https://www.youtube.com/watch?v=UX7amIyT3xw
- ‏YouTube: *How to Download Large Datasets from NCBI using Datasets Command Line*: https://www.youtube.com/watch?v=85TzdIqzJhs

<sub>همه‌ی دستورها در 2026-10-27 روی سرور دوره اجرا شدند. DOIها با doi.org وارسی شدند؛ عنوان و کانال فیلم‌های YouTube با noembed وارسی شد.</sub>

</div>
