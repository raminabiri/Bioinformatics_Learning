<div dir="rtl">

# درس: Ensembl و BioMart؛ از نام ژن به شناسه، رونوشت و جدول

**بخش:** `12_V2_Global_Databases_Browsers` · **ماژول:** `01_Ensembl_BioMart` · **پیش‌نیاز:** ماژول‌های [11/02](../../11_V2_NCBI_Databases/02_Gene_RefSeq_Protein_Taxonomy/) (RefSeq و MANE) و [11/04](../../11_V2_NCBI_Databases/04_GEO/) (ژن‌های پاسخ به دگزامتازون)؛ `curl` و `jq` ([02/05](../../02_BioLinux/05_Data_Download/))؛ دیکشنری و فهرست پایتون ([03/02](../../03_Python/02_Python_Lists_Loops/)) · **زمان:** حدود ۹۰ دقیقه · **ابزار:** curl 8.20.0، jq، Python 3 با requests 2.34.2؛ Ensembl REST (release 116)؛ BioMart (release 116، بر سایت بایگانی) · **آخرین بازبینی:** 2026-10-27

> ✅ **وضعیت: اجرا شده.** همه‌ی خروجی‌ها واقعی‌اند (2026-10-27، Ensembl release 116). گام‌های مرورگر وب با برچسب ✍️ از مستندات نوشته شده‌اند. در روز اجرا سرورهای Ensembl بارها پاسخ ‏HTTP 500 و 503 دادند؛ دستورها با تکرار پاسخ گرفتند (بخش ۹).

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. شناسه‌های Ensembl (**ENSG**، **ENST**، **ENSP**) و **نسخه**‌ی آن‌ها را بخوانید و بدانید هر کدام به چه اشاره دارد.
2. با **Ensembl REST** و `curl` یک ژن، رونوشت‌هایش، رونوشت **canonical** و شناسه‌های هم‌ارزش در NCBI را بگیرید.
3. با یک درخواست **POST** چند ژن را یک‌جا بپرسید.
4. با **BioMart** جدول ویژگی ژن‌ها، رونوشت **MANE Select** و ارتولوگ‌های موش بسازید.
5. با یک اسکریپت پایتون (`requests`) نام ژن را به شناسه‌ی Ensembl و NCBI برگردانید و پاسخ‌های «سرور شلوغ است» را مدیریت کنید.

**پیش از آغاز:**

<div dir="ltr">

```bash
mkdir -p ~/global/m01 && cd ~/global/m01
R=https://rest.ensembl.org
J="content-type=application/json"
P=~/Bioinformatics_Learning-main/12_V2_Global_Databases_Browsers/99_scripts_data
```

</div>

‏`J` بخش پایانی همه‌ی نشانی‌های REST است: از سرور می‌خواهد پاسخ را **JSON** بدهد.

---

## ۱. داستان

در ماژول 11/04 از داده‌ی GSE52778 هشت ژن پاسخ به دگزامتازون را یافتید: **NR3C1** (خود گیرنده)، **FKBP5**، **TSC22D3**، **ZBTB16**، **PER1**، **DUSP1**، **KLF15** و **CRISPLD2**. جدول شما شناسه‌ی **NCBI Gene** داشت (برای نمونه 2908 برای NR3C1). اکنون همکاری جدول بیان را از GTEx یا Expression Atlas (ماژول 12/06) برایتان فرستاده است، ولی ستون نخست آن چنین است: `ENSG00000113580`. این شناسه از **Ensembl** است، بزرگ‌ترین پایگاه ژنوم بیرون از NCBI. بسته‌ی `airway` و DESeq2 در بخش ۱۳ هم همین شناسه‌ها را به کار می‌برند.

پس باید بتوانید میان این دو جهان رفت‌وآمد کنید: نام ژن ← شناسه‌ی Ensembl ← شناسه‌ی NCBI، و بدانید کدام رونوشت «همان» `NM_000176.3` درس 11/02 است.

**پاسخ معلوم:** از 11/02 می‌دانید رونوشت MANE Select ژن NR3C1 ‏`NM_000176.3` است و پروتئینش **۷۷۷** اسید آمینه دارد. از 11/01 هم می‌دانید ژن rpoB در *E. coli* K-12 از باز 4181245 تا 4185273 است و پروتئینش **۱۳۴۲** اسید آمینه دارد. Ensembl باید همین‌ها را بدهد.

---

## ۲. مفهوم به زبان ساده

### ‏۲.۱ ‏Ensembl چیست و با NCBI چه فرقی دارد؟

‏Ensembl پروژه‌ی مشترک **EMBL-EBI** (هینکستون، انگلستان) است. کار اصلی‌اش **آنوتیشن** است: روی هر ژنوم، جای ژن‌ها، رونوشت‌ها و پروتئین‌ها را با برنامه‌های خودکار و بازبینی دستی می‌گذارد. NCBI هم همین کار را با RefSeq می‌کند. پس برای ژنوم انسان **دو آنوتیشن** جدا داریم:

| | NCBI | Ensembl |
| :--- | :--- | :--- |
| نام آنوتیشن | RefSeq | ‏Ensembl/GENCODE (برای انسان و موش) |
| ژن | Gene ID ‏(`2908`) | ‏`ENSG00000113580` |
| رونوشت | ‏`NM_000176.3` | ‏`ENST00000394464.7` |
| پروتئین | ‏`NP_000167.1` | ‏`ENSP00000377977` |
| جایگاه | ‏www.ncbi.nlm.nih.gov | ‏www.ensembl.org |

هر دو روی **یک** ژنوم مرجع (GRCh38) کار می‌کنند، ولی رونوشت‌هایشان همیشه یکی نیست. برای همین دو پایگاه با هم پروژه‌ی **MANE** را ساختند (مقاله‌ی Morales و همکاران، ۲۰۲۲): برای هر ژن انسانی یک رونوشت که در هر دو پایگاه **باز به باز یکسان** است (11/02).

‏**GENCODE** نام آنوتیشن انسان و موش در Ensembl است. GTEx، TCGA و بیشتر داده‌های RNA-seq انسانی شناسه‌ی GENCODE/Ensembl دارند.

### ۲.۲ خواندن یک شناسه‌ی Ensembl

<div dir="ltr">

```text
ENSG00000113580.17
│  │└──────────┘ └─ version: changes when the gene model changes
│  │     └──────── 11-digit stable number
│  └────────────── G = gene, T = transcript, P = protein, E = exon
└───────────────── ENS = Ensembl, human (mouse = ENSMUS, zebrafish = ENSDAR)
```

</div>

- ‏**stable ID** (بی نسخه) در همه‌ی نسخه‌های Ensembl ثابت می‌ماند. **نسخه** (`.17`) هر بار که مدل ژن عوض شود، بالا می‌رود.
- گونه در پیشوند است: `ENSMUSG` ژن موش، `ENSDARG` ژن گورخرماهی. انسان پیشوند گونه ندارد.

### ۲.۳ نسخه‌ی Ensembl (release) و سایت تازه

‏Ensembl هر سال چند **release** شماره‌دار می‌دهد. مختصات و مدل ژن‌ها میان releaseها گاهی عوض می‌شوند. پس در هر گزارش بنویسید از کدام release داده گرفته‌اید (این درس: **116**).

**تغییر بزرگ ۲۰۲۶:** ‏release 116 آخرین release روی **سایت قدیمی** Ensembl بود (Yates و همکاران، ۲۰۲۶). از تابستان ۲۰۲۶ نشانی **www.ensembl.org** سایت **تازه**‌ی Ensembl را باز می‌کند (پیش‌تر beta.ensembl.org). سایت قدیمی، از جمله **BioMart**، در **بایگانی** مانده است. نسخه‌ی 116 آن در **jun2026.archive.ensembl.org** است و انتظار می‌رود چند سال بماند. سرور **REST** هنوز همان `rest.ensembl.org` است و release 116 را می‌دهد.

### ‏۲.۴ ‏REST API چیست؟

وقتی صفحه‌ی ژنی را در مرورگر باز می‌کنید، سرور HTML برای چشم شما می‌فرستد. **REST API** همان داده را برای **برنامه** می‌فرستد: نشانی می‌دهید و پاسخ JSON می‌گیرید. E-utilities در 11/01 هم چنین بود. در Ensembl هر کار یک **endpoint** است:

<div dir="ltr">

```text
https://rest.ensembl.org/lookup/symbol/homo_sapiens/NR3C1?content-type=application/json
└──────── server ──────┘└── endpoint ──┘└─ species ─┘└gene┘└──────── options ─────────┘
```

</div>

**قاعده‌ی سرور:** بیش از **۱۵ درخواست در ثانیه** نفرستید. اگر تند بروید، پاسخ `429` می‌گیرید.

---

## ۳. گام ۰: مرورگر وب Ensembl (✍️)

**چرا؟** پیش از کار با API، یک بار ژن را با چشم ببینید.

✍️ **گام‌ها (از مستندات و آموزش‌های Ensembl؛ سایت تازه با جاوااسکریپت ساخته شده و از سرور دوره دیده نشد):**
1. ‏www.ensembl.org را باز کنید. در جعبه‌ی جست‌وجو گونه را **Human** بگذارید و `NR3C1` بنویسید.
2. در نتیجه‌ها ژن `ENSG00000113580` را بزنید. نمای ژنوم ناحیه‌ی 5q31 را با ژن و رونوشت‌هایش نشان می‌دهد. رونوشت‌های کدکننده و ناکدکننده رنگ جدا دارند.
3. در فهرست رونوشت‌ها دنبال برچسب‌هایی چون **MANE Select** و **Ensembl canonical** بگردید؛ گام ۲ همین را با REST نشان می‌دهد.
4. برای دیدن **سایت قدیمی** با همان داده (release 116) به jun2026.archive.ensembl.org بروید. در آن‌جا برگه‌ی **Transcript table** همه‌ی رونوشت‌ها را در جدول نشان می‌دهد.

> 📺 **فیلم:** *Introduction to the Ensembl Genome Browser – Webinar 2: Genes & transcripts* (Ensembl Training): https://www.youtube.com/watch?v=j5JtUCrhXaQ
> 📄 **مرجع:** Yates AD, et al. (2026). *Ensembl 2026.* Nucleic Acids Res 54(D1):D1053–D1060. https://doi.org/10.1093/nar/gkaf1239

---

## ۴. گام ۱: یک ژن از REST

**چرا؟** از نام ژن به شناسه‌ی Ensembl و جایگاهش برسیم.

<div dir="ltr">

```bash
curl -sS "$R/lookup/symbol/homo_sapiens/NR3C1?$J" \
  | jq '{id, version, display_name, biotype, seq_region_name, start, end, strand, assembly_name, canonical_transcript}'
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`lookup/symbol` | «ژنی با این نماد را پیدا کن» |
| ‏`homo_sapiens` | نام گونه با `_` (یا `human`) |
| ‏`jq '{id, version, …}'` | از JSON بلند، تنها این کلیدها را نگه دار |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```json
{
  "id": "ENSG00000113580",
  "version": 17,
  "display_name": "NR3C1",
  "biotype": "protein_coding",
  "seq_region_name": "5",
  "start": 143277931,
  "end": 143435512,
  "strand": -1,
  "assembly_name": "GRCh38",
  "canonical_transcript": "ENST00000394464.7"
}
```

</div>

**توضیح خروجی:**
- ‏`seq_region_name: "5"`: کروموزوم ۵، **بی** پیشوند `chr` (‏UCSC در 12/02 می‌نویسد `chr5`).
- ‏`start` و `end` با شمارش **از ۱** (1-based) است، مانند NCBI. ژن ۱۵۷٬۵۸۲ باز درازا دارد.
- ‏`strand: -1`: ژن روی رشته‌ی **منفی** است؛ پس آغاز رونویسی در `end` است، نه `start`.
- ‏`canonical_transcript`: رونوشتی که Ensembl نماینده‌ی ژن می‌داند (گام ۲).

<details>
<summary>✋ امتحان کن: اگر به جای <code>NR3C1</code> بنویسید <code>nr3c1</code> (حروف کوچک) چه می‌شود؟ و <code>mouse</code> به جای <code>homo_sapiens</code>؟</summary>

‏`lookup/symbol` به بزرگی و کوچکی حروف حساس نیست و برای انسان همان `ENSG00000113580` را می‌دهد. با `mouse` ژن موش را می‌گیرید: `ENSMUSG00000024431` (نامش `Nr3c1`). پیشوند `ENSMUS` گونه را نشان می‌دهد.

</details>

---

## ۵. گام ۲: همه‌ی رونوشت‌ها و رونوشت canonical

**چرا؟** یک ژن چند رونوشت دارد. باید بدانیم کدام را گزارش کنیم.

‏`expand=1` همه‌ی رونوشت‌ها و پروتئین‌ها را هم در پاسخ می‌آورد. پاسخ بزرگ است (۶۳ کیلوبایت)، پس آن را در فایل می‌نویسیم و چند بار با `jq` می‌خوانیم:

<div dir="ltr">

```bash
curl -sS "$R/lookup/id/ENSG00000113580?expand=1;$J" > nr3c1.json
jq '.Transcript | length' nr3c1.json
jq -r '.Transcript[].biotype' nr3c1.json | sort | uniq -c
jq -r '.Transcript[] | select(.is_canonical == 1)
       | [.id, .version, .display_name, .start, .end, .Translation.id, .Translation.length] | @tsv' nr3c1.json
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`;` در نشانی | جداکننده‌ی گزینه‌ها در Ensembl REST (‏`&` هم کار می‌کند) |
| ‏`.Transcript[]` | هر عضو فهرست رونوشت‌ها، یکی‌یکی |
| ‏`select(.is_canonical == 1)` | تنها رونوشتی که این کلیدش ۱ است |
| ‏`@tsv` | فهرست را با Tab در یک سطر بنویس |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
32
      1 nonsense_mediated_decay
     28 protein_coding
      3 protein_coding_CDS_not_defined
ENST00000394464	7	NR3C1-203	143277934	143403686	ENSP00000377977	777
```

</div>

**توضیح خروجی:**
- ‏NR3C1 در Ensembl **۳۲** رونوشت دارد: ۲۸ کدکننده‌ی پروتئین، یکی که با **NMD** (تجزیه‌ی mRNA دارای کدون پایان زودرس) از میان می‌رود، و سه که کدکننده‌اند ولی CDS کاملشان روشن نیست.
- رونوشت canonical ‏`ENST00000394464.7` با نام `NR3C1-203` است و پروتئین `ENSP00000377977` با **۷۷۷** اسید آمینه می‌سازد. این همان طول `NP_000167.1` در 11/02 است. ✅
- آغاز این رونوشت 143277934 است، سه باز پس از آغاز ژن (143277931)، چون ژن از کناره‌های **همه**‌ی رونوشت‌ها ساخته می‌شود.

### ‏۵.۱ ‏canonical، MANE و GENCODE primary

| برچسب | معنا |
| :--- | :--- |
| ‏**Ensembl canonical** | برای هر ژن **یک** رونوشت نماینده؛ در انسان اگر رونوشت MANE Select باشد، همان است |
| ‏**MANE Select** | رونوشتی که در RefSeq و Ensembl باز به باز یکسان است (11/02) |
| ‏**GENCODE primary** | رونوشت‌های پشتیبانی‌شده‌ی اصلی؛ زیرمجموعه‌ای از همه |

<details>
<summary>✋ امتحان کن: درازای رونوشت canonical چند باز است و درازای <code>NM_000176.3</code> در 11/02 چند باز بود؟</summary>

با `jq -r '.Transcript[] | select(.is_canonical == 1) | .length' nr3c1.json` پاسخ **6778** است. ‏`NM_000176.3` هم ۶۷۷۸ باز بود. یکسان بودن درازا با MANE جور است، ولی برای اطمینان باید برچسب MANE را دید (گام ۶).

</details>

> 📺 **فیلم:** *EMBL-EBI, programmatically: Ensembl* (EMBL-EBI): https://www.youtube.com/watch?v=R2R9YOK8VQs
> 📄 **مرجع:** Yates A, et al. (2015). *The Ensembl REST API: Ensembl Data for Any Language.* Bioinformatics 31(1):143–145. https://doi.org/10.1093/bioinformatics/btu613 · فهرست endpointها: https://rest.ensembl.org

---

## ۶. گام ۳: شناسه‌های هم‌ارز (xrefs)

**چرا؟** کدام شناسه‌های NCBI، HGNC و OMIM با این ژن و رونوشت جفت‌اند؟ Ensembl این پیوندها را **xref** (cross-reference) می‌نامد.

<div dir="ltr">

```bash
curl -sS "$R/xrefs/id/ENST00000394464?$J" > xref_tx.json
jq -r '.[] | .dbname' xref_tx.json | sort | uniq -c
jq -r '.[] | select(.dbname == "RefSeq_mRNA" or .dbname == "CCDS") | [.dbname, .display_id] | @tsv' xref_tx.json

curl -sS "$R/xrefs/id/ENSG00000113580?$J" > xref_gene.json
jq -r '.[] | select(.dbname == "EntrezGene" or .dbname == "HGNC" or .dbname == "MIM_GENE")
       | [.dbname, .primary_id, .display_id] | @tsv' xref_gene.json
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
      1 CCDS
    113 GO
      1 HGNC_trans_name
     28 Reactome_transcript
     10 RefSeq_mRNA
      1 UCSC
CCDS	CCDS4278.1
RefSeq_mRNA	NM_001364180.2
RefSeq_mRNA	NM_000176.3
RefSeq_mRNA	NM_001204258.2
RefSeq_mRNA	NM_001204259.2
RefSeq_mRNA	NM_001204260.2
RefSeq_mRNA	NM_001204261.2
RefSeq_mRNA	NM_001204262.2
RefSeq_mRNA	NM_001204263.2
RefSeq_mRNA	NM_001204264.2
RefSeq_mRNA	NM_001364182.1
EntrezGene	2908	NR3C1
HGNC	HGNC:7978	NR3C1
MIM_GENE	138040	NUCLEAR RECEPTOR SUBFAMILY 3, GROUP C, MEMBER 1; NR3C1 [*138040]
```

</div>

**توضیح خروجی:**
- ‏`EntrezGene 2908`: همان NCBI Gene ID ‏11/02. پل میان دو جهان همین xref است.
- ‏۱۱۳ پیوند **GO** و ۲۸ پیوند **Reactome**: کارکرد و مسیر ژن (ماژول 12/05).
- ‏**CCDS**: پروژه‌ی مشترک NCBI، Ensembl و UCSC که CDSهای یکسان را برچسب می‌زند؛ پیش‌درآمد MANE.
- **چرا ۱۰ رونوشت RefSeq؟** این‌جا یک رونوشت Ensembl با ده `NM_` جفت شده است. با `esummary` در NCBI (11/01) دیدیم که **هشت** تای آن‌ها، از `NM_000176.3` تا `NM_001204264.2`، همه «transcript variant 1» با درازای ۶۷۷۸ باز هستند: **یک** mRNA. ولی NCBI برای هر **AUG آغاز** درون‌قاب (ایزوفرم‌های ترجمه‌ای گیرنده‌ی گلوکوکورتیکوئید، مانند `NP_001191187.1` که با `MDFYK…` آغاز می‌شود) یک `NM_` جدا ساخته است. Ensembl یک رونوشت با یک پروتئین ۷۷۷ اسید آمینه‌ای نگه داشته است. دو variant دیگر (9 و 11) تنها در درازای UTR فرق دارند.

**درس این گام:** نگاشت میان پایگاه‌ها **یک به یک نیست**. همیشه شمار جفت‌ها را ببینید.

<details>
<summary>✋ امتحان کن: شناسه‌ی UniProt (Swiss-Prot) پروتئین canonical چیست؟</summary>

با `external_db` می‌توان xrefها را صاف کرد:

<div dir="ltr">

```bash
curl -sS "$R/xrefs/id/ENSP00000377977?external_db=Uniprot/SWISSPROT;$J" | jq -r '.[].primary_id'
```

</div>

پاسخ: `P04150`، همان پروتئین گیرنده‌ی گلوکوکورتیکوئید در UniProt (ماژول 12/04).

</details>

---

## ۷. گام ۴: توالی پروتئین و ارتولوگ‌ها

**چرا؟** دو کار رایج دیگر: گرفتن توالی، و یافتن همان ژن در گونه‌ی دیگر (**ارتولوگ**: ژن‌هایی در دو گونه که از یک ژن نیای مشترک آمده‌اند).

<div dir="ltr">

```bash
curl -sS "$R/sequence/id/ENST00000394464?type=protein;$J" > prot.json
jq -r '.seq | length' prot.json
jq -r '.seq[0:60]' prot.json

curl -sS "$R/homology/symbol/human/NR3C1?type=orthologues;target_species=mouse;target_species=danio_rerio;sequence=none;$J" \
  | jq -r '.data[0].homologies[] | [.target.species, .target.id, .type, (.target.perc_id*10|round/10)] | @tsv'
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`sequence/id/ENST…?type=protein` | توالی پروتئینِ این رونوشت (به جای `cdna` یا `cds`) |
| ‏`.seq[0:60]` | ۶۰ نویسه‌ی نخست رشته |
| ‏`homology/symbol` | هومولوگ‌های این ژن در گونه‌های دیگر |
| ‏`target_species=…` | تنها این گونه‌ها (چند بار می‌آید) |
| ‏`sequence=none` | توالی هم‌ترازی را نفرست؛ پاسخ کوچک می‌ماند |
| ‏`perc_id*10\|round/10` | درصد یکسانی، گرد با یک رقم اعشار |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
777
MDSKESLTPGREENPSSVLAQERGDVMDFYKTLRGGATVKVSASSPSLAVASQSDSKQRR
mus_musculus	ENSMUSG00000024431	ortholog_one2one	88.5
danio_rerio	ENSDARG00000025032	ortholog_one2one	49.2
```

</div>

**توضیح خروجی:**
- پروتئین ۷۷۷ اسید آمینه دارد و با `MDSKESLTPG…` آغاز می‌شود، همان آغاز `NP_000167.1`.
- ‏`ortholog_one2one`: در موش و گورخرماهی هر کدام **یک** ارتولوگ هست. (اگر یکی از دو گونه نسخه‌ی دوم ژن را داشت، `one2many` می‌دیدید.)
- پروتئین موش ۸۸٫۵٪ با انسان یکسان است و گورخرماهی ۴۹٫۲٪. هرچه دودمان دورتر، یکسانی کمتر (11/02، Taxonomy).

---

## ۸. گام ۵: چند ژن با یک درخواست (POST)

**چرا؟** برای هشت ژن، هشت بار `curl` نزنیم. درخواست **POST** فهرست را در **بدنه**‌ی درخواست می‌فرستد، نه در نشانی.

<div dir="ltr">

```bash
curl -sS -X POST "$R/lookup/symbol/homo_sapiens" \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"symbols": ["NR3C1","FKBP5","TSC22D3","ZBTB16","PER1","DUSP1","KLF15","CRISPLD2"]}' > dex.json
jq -r 'to_entries[] | [.key, .value.id, .value.seq_region_name, .value.start, .value.end, .value.strand] | @tsv' dex.json
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`-X POST` | گونه‌ی درخواست: POST (پیش‌فرض `curl` ‏GET است) |
| ‏`-H "Content-Type: …"` | «بدنه‌ای که می‌فرستم JSON است» |
| ‏`-H "Accept: …"` | «پاسخ را JSON می‌خواهم» (به جای `?content-type=` در نشانی) |
| ‏`-d '{…}'` | بدنه‌ی درخواست: فهرست نمادها |
| ‏`to_entries[]` | پاسخ یک دیکشنری است (`نماد: اطلاعات`)؛ هر جفت را جدا کن |
| ‏`.key` / `.value.id` | نماد ژن / شناسه‌ی Ensembl |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
FKBP5	ENSG00000096060	6	35572945	35728622	-1
CRISPLD2	ENSG00000103196	16	84819975	84920768	1
TSC22D3	ENSG00000157514	X	107713221	107777342	-1
NR3C1	ENSG00000113580	5	143277931	143435512	-1
DUSP1	ENSG00000120129	5	172766992	172771198	-1
KLF15	ENSG00000163884	3	126342635	126357462	-1
ZBTB16	ENSG00000109906	11	114058335	114256765	1
PER1	ENSG00000179094	17	8140467	8156506	-1
```

</div>

**توضیح خروجی:**
- ترتیب سطرها با ترتیب فهرست شما یکی **نیست**: دیکشنری JSON ترتیب ثابتی ندارد. اگر ترتیب مهم است، پس از آن `sort` بزنید.
- ‏TSC22D3 روی کروموزوم **X** است. DUSP1 و NR3C1 هر دو روی کروموزوم ۵ هستند، ولی ۳۰ میلیون باز از هم دور.
- سقف هر POST ‏`lookup/symbol` ‏**۱۰۰۰** نماد است.

<details>
<summary>✋ امتحان کن: اگر فهرست، نام قدیمی <code>GILZ</code> را به جای <code>TSC22D3</code> داشت چه می‌شد؟</summary>

پاسخ برای `GILZ` هیچ کلیدی ندارد؛ نماد در پاسخ نمی‌آید و **خطایی** هم نمی‌گیرید. ‏`lookup/symbol` تنها **نماد رسمی** HGNC را می‌شناسد. نام‌های دیگر را در 11/01 دیدید (acrB[gene] ← gyrB هم). در اسکریپت گام ۷ این حالت را با برچسب `NOT_FOUND` نشان می‌دهیم.

</details>

---

## ۹. گام ۶: BioMart؛ جدول بدون برنامه‌نویسی

**چرا؟** BioMart برای کسی ساخته شد که برنامه‌نویسی نمی‌داند: **صافی** (filter) می‌گذارید، **ستون** (attribute) برمی‌گزینید و جدول TSV می‌گیرید. برای هزاران ژن هم سریع است.

### ۹.۱ در مرورگر (✍️)

✍️ **گام‌ها (از راهنمای BioMart و فیلم Ensembl؛ نسخه‌ی 116 در سایت بایگانی):**
1. ‏https://jun2026.archive.ensembl.org/biomart/martview را باز کنید.
2. **Database:** ‏*Ensembl Genes 116*؛ **Dataset:** ‏*Human genes (GRCh38.p14)*.
3. در سمت چپ **Filters** ← *GENE* ← *Input external references ID list*، گزینه‌ی *Gene Name(s)* را بزنید و هشت نام را هر کدام در یک سطر بنویسید.
4. ‏**Attributes** ← *Features*: ‏*Gene stable ID*، *Gene name*، *Chromosome/scaffold name*، *Gene start*، *Gene end*، *Strand*، *Gene type* و از بخش *EXTERNAL* ‏*NCBI gene (formerly Entrezgene) ID*.
5. دکمه‌ی **Results** بالای صفحه ← خروجی TSV را دانلود کنید.
6. دکمه‌ی **XML** بالای صفحه، همین پرسش را به شکل XML نشان می‌دهد. آن را نگه دارید؛ گام بعد همین است.

### ۹.۲ همان پرسش با `curl`

پرسش XML (فایل `dex_query.xml` در `99_scripts_data/01_Ensembl_BioMart/data/`):

<div dir="ltr">

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query virtualSchemaName="default" formatter="TSV" header="1" uniqueRows="1">
  <Dataset name="hsapiens_gene_ensembl" interface="default">
    <Filter name="external_gene_name" value="NR3C1,FKBP5,TSC22D3,ZBTB16,PER1,DUSP1,KLF15,CRISPLD2"/>
    <Attribute name="ensembl_gene_id"/>
    <Attribute name="external_gene_name"/>
    <Attribute name="chromosome_name"/>
    <Attribute name="start_position"/>
    <Attribute name="end_position"/>
    <Attribute name="strand"/>
    <Attribute name="gene_biotype"/>
    <Attribute name="entrezgene_id"/>
  </Dataset>
</Query>
```

</div>

<div dir="ltr">

```bash
M=https://jun2026.archive.ensembl.org/biomart/martservice
cp $P/01_Ensembl_BioMart/data/dex_query.xml .
curl -sS -G --data-urlencode "query@dex_query.xml" $M > dex_mart.tsv
column -t -s $'\t' dex_mart.tsv
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`hsapiens_gene_ensembl` | دیتاست ژن‌های انسان |
| ‏`<Filter … value="a,b,c"/>` | صافی؛ چند مقدار با `,` |
| ‏`<Attribute name=…/>` | هر ستون خروجی |
| ‏`header="1"` | سطر نام ستون‌ها را هم بده |
| ‏`-G --data-urlencode "query@file"` | محتوای فایل را کدگذاری کن و با GET بفرست (‏`@` یعنی «از این فایل بخوان») |
| ‏`column -t -s $'\t'` | ستون‌ها را با Tab جدا کن و زیر هم بچین |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
Gene stable ID   Gene name  Chromosome/scaffold name  Gene start (bp)  Gene end (bp)  Strand  Gene type       NCBI gene (formerly Entrezgene) ID
ENSG00000157514  TSC22D3    X                         107713221        107777342      -1      protein_coding  1831
ENSG00000163884  KLF15      3                         126342635        126357462      -1      protein_coding  28999
ENSG00000120129  DUSP1      5                         172766992        172771198      -1      protein_coding  1843
ENSG00000103196  CRISPLD2   16                        84819975         84920768       1       protein_coding  83716
ENSG00000113580  NR3C1      5                         143277931        143435512      -1      protein_coding  2908
ENSG00000096060  FKBP5      6                         35572945         35728622       -1      protein_coding  2289
ENSG00000179094  PER1       17                        8140467          8156506        -1      protein_coding  5187
ENSG00000109906  ZBTB16     11                        114058335        114256765      1       protein_coding  7704
```

</div>

**توضیح خروجی:**
- همان مختصات REST (گام ۵)، و این بار با **NCBI Gene ID** کنار هر ژن. شناسه‌های NCBI با 11/04 یکی‌اند (FKBP5 ‏2289، TSC22D3 ‏1831…). ✅
- اگر پاسخ به جای جدول با `<html>` آغاز شد، سرور در دسترس نیست: چند دقیقه بعد دوباره بزنید (بخش ۱۱).

### ۹.۳ رونوشت MANE و ارتولوگ موش با BioMart

همان قالب XML را با صافی و ستون‌های دیگر به کار می‌بریم (فایل‌ها در همان پوشه‌ی `data/`). نخست رونوشت‌های NR3C1 با برچسب canonical و MANE:

<div dir="ltr">

```bash
cp $P/01_Ensembl_BioMart/data/nr3c1_tx.xml .
grep '<Attribute' nr3c1_tx.xml
curl -sS -G --data-urlencode "query@nr3c1_tx.xml" $M > nr3c1_tx.tsv
tail -n +2 nr3c1_tx.tsv | wc -l
awk -F'\t' 'NR == 1 || $5 != ""' nr3c1_tx.tsv
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
    <Attribute name="ensembl_transcript_id"/>
    <Attribute name="transcript_biotype"/>
    <Attribute name="transcript_length"/>
    <Attribute name="transcript_is_canonical"/>
    <Attribute name="transcript_mane_select"/>
32
Transcript stable ID	Transcript type	Transcript length (including UTRs and CDS)	Ensembl Canonical	RefSeq match transcript (MANE Select)
ENST00000394464	protein_coding	6778	1	NM_000176.3
```

</div>

‏`awk` تنها سرخط (`NR == 1`) و سطرهایی را نگه می‌دارد که ستون پنجم (MANE) خالی نیست. پاسخ معلوم تأیید شد: **`ENST00000394464` = `NM_000176.3`** (MANE Select)، و همان رونوشت canonical است. ✅

سپس ارتولوگ موش برای هر هشت ژن (`dex_mouse.xml`؛ ستون‌ها: `external_gene_name`، `mmusculus_homolog_associated_gene_name`، `mmusculus_homolog_orthology_type`، `mmusculus_homolog_perc_id`):

<div dir="ltr">

```bash
cp $P/01_Ensembl_BioMart/data/dex_mouse.xml .
curl -sS -G --data-urlencode "query@dex_mouse.xml" $M | column -t -s $'\t'
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
Gene name  Mouse gene name  Mouse homology type  %id. target Mouse gene identical to query gene
TSC22D3    Tsc22d3          ortholog_one2one     86.5
KLF15      Klf15            ortholog_one2one     85.0962
DUSP1      Dusp1            ortholog_one2one     96.4578
CRISPLD2   Crispld2         ortholog_one2one     77.0624
NR3C1      Nr3c1            ortholog_one2one     90.2188
FKBP5      Fkbp5            ortholog_one2one     87.0897
PER1       Per1             ortholog_one2one     91.938
ZBTB16     Zbtb16           ortholog_one2one     96.7311
```

</div>

همه یک‌به‌یک‌اند؛ پس یافته‌های موش (آزمایش‌های دگزامتازون روی موش) را می‌شود به این ژن‌ها برگرداند. برای NR3C1 این‌جا ۹۰٫۲ آمده و در گام ۴ ‏۸۸٫۵: ستون BioMart «درصدی از پروتئین **انسان** که در موش یکسان است» و عدد گام ۴ همان نسبت از دید پروتئین **موش** است (در گام ۴، `source.perc_id` هم ۹۰٫۲ بود). همیشه بدانید درصد نسبت به کدام توالی است.

<details>
<summary>✋ امتحان کن: نام ستون‌های BioMart (مانند <code>transcript_mane_select</code>) را از کجا بیابیم؟</summary>

در مرورگر، دکمه‌ی **XML** نام درونی هر ستونی را که برگزیده‌اید نشان می‌دهد. از خط فرمان هم فهرست کامل را می‌گیرید:

<div dir="ltr">

```bash
curl -sS "$M?type=attributes&dataset=hsapiens_gene_ensembl" | cut -f1,2 | grep -i mane
```

</div>

خروجی واقعی (2026-10-27؛ فهرست کامل ۳۱۷۶ ستون دارد):

<div dir="ltr">

```
transcript_mane_select	RefSeq match transcript (MANE Select)
transcript_mane_plus_clinical	RefSeq match transcript (MANE Plus Clinical)
```

</div>

</details>

> 📺 **فیلم:** *Introduction to the Ensembl Genome Browser – Webinar 6: BioMart* (Ensembl Training): https://www.youtube.com/watch?v=rUh4Sa7e-GM
> 📄 **مرجع:** Kinsella RJ, et al. (2011). *Ensembl BioMarts: a hub for data retrieval across taxonomic space.* Database 2011:bar030. https://doi.org/10.1093/database/bar030

---

## ۱۰. گام ۷: اسکریپت پایتون با `requests`

**چرا؟** `curl` و `jq` برای نگاه سریع خوب‌اند. ولی برای فهرست بلند، **تکرار هنگام خطا** و جدول تمیز، پایتون بهتر است. بسته‌ی **`requests`** همان کار `curl` را در پایتون می‌کند.

### ‏۱۰.۱ ‏`requests` در سه خط

<div dir="ltr">

```python
import requests
r = requests.get("https://rest.ensembl.org/lookup/symbol/homo_sapiens/NR3C1",
                 headers={"Accept": "application/json"})
print(r.status_code, r.json()["id"])
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
200 ENSG00000113580
```

</div>

همین سه خط را پنج بار پشت هم اجرا کردیم. یک بار 200 گرفتیم و چهار بار 503 یا 500. در آن چهار بار، `r.json()` با این خطا ایستاد، چون پاسخ صفحه‌ی HTML بود نه JSON:

<div dir="ltr">

```
requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

</div>

پس پیش از `r.json()` همیشه `r.status_code` را بسنجید. اسکریپت بخش ۱۰.۲ همین کار را می‌کند.

- ‏`requests.get(نشانی, headers=…)`: درخواست GET. ‏`requests.post(…, json=دیکشنری)` درخواست POST با بدنه‌ی JSON است.
- ‏`r.status_code`: کد پاسخ. **200** = درست؛ **400** = درخواست نادرست؛ **429** = تند رفتید؛ **500/503** = سرور گرفتار است.
- ‏`r.json()`: پاسخ JSON را به **دیکشنری** و **فهرست** پایتون (03/02) برمی‌گرداند.

### ۱۰.۲ اسکریپت `ens_ids.py`

اسکریپت در `99_scripts_data/01_Ensembl_BioMart/scripts/ens_ids.py` است. کارش:
1. همه‌ی نمادها را با **یک POST** به `lookup/symbol` می‌فرستد (گام ۵).
2. برای هر ژن یافته‌شده، با GET به `xrefs/id/…?external_db=EntrezGene` شناسه‌ی NCBI را می‌گیرد (گام ۳).
3. برای پاسخ‌های 429 و 500 تا 504 دوباره می‌کوشد. پیش از هر کوشش بیشتر صبر می‌کند (۳، ۶، ۹… ثانیه).
4. نمادی را که نیافت، با `NOT_FOUND` نشان می‌دهد.

هسته‌ی اسکریپت، تابع `ask` است:

<div dir="ltr">

```python
def ask(method, path, **kwargs):
    """Send one request; retry on busy-server answers; return the JSON answer."""
    for attempt in range(1, 7):
        r = requests.request(method, SERVER + path, headers=HEADERS, timeout=90, **kwargs)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 429:                       # too many requests: wait as told
            wait = float(r.headers.get("Retry-After", 5))
        elif r.status_code in (500, 502, 503, 504):    # busy server: wait a bit longer each time
            wait = 3 * attempt
        else:                                          # 400 = bad request: retrying will not help
            sys.exit(f"{method} {path}: HTTP {r.status_code} {r.text[:200]}")
        print(f"  {path}: HTTP {r.status_code}, retry {attempt} in {wait:.0f} s", file=sys.stderr)
        time.sleep(wait)
    sys.exit(f"{method} {path}: gave up")
```

</div>

| بخش | کار |
| :--- | :--- |
| ‏`requests.request(method, …)` | همان `get` یا `post`، با نام روش در یک متغیر |
| ‏`**kwargs` | هر گزینه‌ی دیگر (مانند `json=` یا `params=`) را دست‌نخورده به `requests` بده |
| ‏`timeout=90` | اگر سرور ۹۰ ثانیه پاسخ نداد، رها کن (وگرنه برنامه برای همیشه می‌ماند) |
| ‏`Retry-After` | سرور در پاسخ 429 می‌گوید چند ثانیه صبر کنید |
| ‏`file=sys.stderr` | پیام‌ها به stderr؛ جدول خروجی (stdout) تمیز می‌ماند |

اجرا با هشت نماد رسمی و یک نام قدیمی:

<div dir="ltr">

```bash
python3 $P/01_Ensembl_BioMart/scripts/ens_ids.py NR3C1 FKBP5 TSC22D3 ZBTB16 PER1 DUSP1 KLF15 CRISPLD2 GILZ > dex_ids.tsv
column -t dex_ids.tsv
```

</div>

**خروجی واقعی (2026-10-27؛ پیام‌های stderr):**

<div dir="ltr">

```
  /lookup/symbol/homo_sapiens: HTTP 503, retry 1 in 3 s
  /xrefs/id/ENSG00000179094: HTTP 503, retry 1 in 3 s
  /xrefs/id/ENSG00000179094: HTTP 500, retry 2 in 6 s
  /xrefs/id/ENSG00000179094: HTTP 500, retry 3 in 9 s
```

</div>

**خروجی واقعی (جدول):**

<div dir="ltr">

```
symbol    ensembl_id          chrom  start      end        strand  biotype         canonical_transcript  ncbi_gene_id
NR3C1     ENSG00000113580.17  5      143277931  143435512  -1      protein_coding  ENST00000394464.7     2908
FKBP5     ENSG00000096060.17  6      35572945   35728622   -1      protein_coding  ENST00000357266.9     2289
TSC22D3   ENSG00000157514.20  X      107713221  107777342  -1      protein_coding  ENST00000372383.9     1831
ZBTB16    ENSG00000109906.17  11     114058335  114256765  1       protein_coding  ENST00000335953.9     7704
PER1      ENSG00000179094.19  17     8140467    8156506    -1      protein_coding  ENST00000317276.9     5187
DUSP1     ENSG00000120129.8   5      172766992  172771198  -1      protein_coding  ENST00000239223.4     1843
KLF15     ENSG00000163884.6   3      126342635  126357462  -1      protein_coding  ENST00000296233.4     28999
CRISPLD2  ENSG00000103196.14  16     84819975   84920768   1       protein_coding  ENST00000262424.10    83716
GILZ      NOT_FOUND           -      -          -          -       -               -                     -
```

</div>

**توضیح خروجی:**
- همان شناسه‌های BioMart، این بار **با نسخه** (`.17`، `.20`…) و رونوشت canonical. ترتیب سطرها همان ترتیب ورودی است، چون اسکریپت روی فهرست `symbols` می‌چرخد، نه روی دیکشنری پاسخ.
- آن روز سرور چهار بار 500 یا 503 داد. اسکریپت صبر کرد و در کوشش بعد پاسخ گرفت. بی تابع `ask`، برنامه با خطا می‌ایستاد یا صفحه‌ی HTML خطا را JSON می‌پنداشت.
- ‏`GILZ` نماد رسمی نیست؛ `NOT_FOUND` گرفت (تمرین ۴ راه یافتن نماد رسمی را نشان می‌دهد).
- زمان: در روز شلوغ ۲۸۷ ثانیه، بیشترش صبر. در روز آرام چند ثانیه. حافظه: ۳۴ مگابایت.

> 📺 **فیلم:** *EMBL-EBI, programmatically: Ensembl* (همان فیلم گام ۲؛ بخش REST در پایتون): https://www.youtube.com/watch?v=R2R9YOK8VQs
> 📄 **مرجع:** راهنمای `requests`: https://requests.readthedocs.io · نمونه‌های پایتون Ensembl REST: https://github.com/Ensembl/ensembl-rest/wiki

---

## ۱۱. گام ۸: ‏Ensembl برای باکتری‌ها

**چرا؟** Ensembl تنها برای مهره‌داران نیست. باکتری‌ها، گیاهان، قارچ‌ها و بی‌مهرگان پیش‌تر در **Ensembl Genomes** بودند (Ensembl Bacteria و…). در سایت تازه همه یک‌جا هستند و همان سرور REST آن‌ها را هم می‌دهد. تنها نام گونه بلند است:

<div dir="ltr">

```bash
EC=escherichia_coli_str_k_12_substr_mg1655_gca_000005845
curl -sS "$R/info/genomes/$EC?$J" | jq -c '{division, assembly_accession, assembly_name, base_count, taxonomy_id}'
curl -sS "$R/lookup/symbol/$EC/rpoB?$J" | jq -c '{id, display_name, seq_region_name, start, end, strand, canonical_transcript}'
curl -sS "$R/sequence/id/b3987?type=protein;species=$EC;$J" | jq -r '.seq | length'
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
{"division":"EnsemblBacteria","assembly_accession":"GCA_000005845.2","assembly_name":"ASM584v2","base_count":4641652,"taxonomy_id":511145}
{"id":"b3987","display_name":"rpoB","seq_region_name":"Chromosome","start":4181245,"end":4185273,"strand":1,"canonical_transcript":"AAC76961."}
1342
```

</div>

**توضیح خروجی:**
- ژنوم ۴٬۶۴۱٬۶۵۲ باز است، همان `NC_000913.3` (11/01)، و TaxID ‏511145 همان K-12 MG1655 است (11/02).
- ‏rpoB از 4181245 تا 4185273 روی رشته‌ی مثبت است، **باز به باز** همان NCBI. ✅ پروتئینش ۱۳۴۲ اسید آمینه دارد. ✅
- شناسه‌ی ژن `b3987` است، نه `ENSG…`: Ensembl برای باکتری‌ها شناسه‌ی **locus tag** خود ژنوم را نگه می‌دارد. رونوشت `AAC76961` هم همان شناسه‌ی پروتئین **GenBank** است (تمرین ۱ ماژول 11/02)، چون آنوتیشن از ENA (همتای اروپایی GenBank) آمده است.

> 📺 **فیلم:** *Introduction to the Ensembl Genome Browser – Webinar 2: Genes & transcripts* (همان فیلم گام ۰): https://www.youtube.com/watch?v=j5JtUCrhXaQ
> 📄 **مرجع:** Yates AD, et al. (2022). *Ensembl Genomes 2022: an expanding genome resource for non-vertebrates.* Nucleic Acids Res 50(D1):D996–D1003. https://doi.org/10.1093/nar/gkab1007

---

## ۱۲. سه اشتباه رایج

1. **فراموش کردن release و نسخه.** پرسش BioMart بالا را روی بایگانی **release 114** (may2025.archive.ensembl.org) هم زدیم. ‏FKBP5 در 114 از 35573585 تا 35728583 بود و در 116 از 35572945 تا 35728622. KLF15، DUSP1، ZBTB16 و CRISPLD2 هم مختصات دیگری داشتند. ‏API ‏GTEx (12/06) برای NR3C1 ‏`ENSG00000113580.14` را می‌دهد (آنوتیشن GENCODE v26)، در حالی که Ensembl 116 ‏`.17` است. همیشه release را بنویسید و برای جفت کردن جدول‌ها، نسخه را جدا کنید (`cut -d. -f1`).
2. **جدی نگرفتن پاسخ‌های 500 و 503.** پاسخ خطای Ensembl یک صفحه‌ی **HTML** است. `jq` با پیام `parse error: Invalid numeric literal` می‌ایستد، `r.json()` در پایتون با `JSONDecodeError`، و BioMart جدولی می‌دهد که با `<html>` آغاز می‌شود. پیش از خواندن، کد پاسخ را بسنجید (`curl -w '%{http_code}'` یا `r.status_code`) و چند بار با درنگ دوباره بکوشید.
3. **یکی دانستن نگاشت شناسه‌ها.** یک ENST با ده NM جفت شد (گام ۳)؛ نماد قدیمی (`GILZ`) هیچ پاسخی نداد؛ و `seq_region_name` در Ensembl `5` است ولی در UCSC `chr5`. پس از هر نگاشت، شمار سطرها را پیش و پس بشمارید.

---

## 📘 برای کنجکاوها

- ‏**‏BioMart در R:** بسته‌ی `biomaRt` در Bioconductor همین پرسش‌ها را از R می‌فرستد (`useEnsembl(biomart = "genes", host = "https://jun2026.archive.ensembl.org")`). در بخش ۱۳ کنار DESeq2 آن را می‌بینید.
- ‏**‏Ensembl canonical extended:** در release 116 برچسب تازه‌ای آمد (`ens_canon_extended`): رونوشت canonical با دو سر 5′ و 3′ بلندتر، بر پایه‌ی داده‌ی رید بلند. برای NR3C1 مقدارش ۰ است.
- ‏**‏VEP:** ابزار پیش‌بینی پیامد واریانت Ensembl همان endpoint REST را دارد (`/vep/human/hgvs/…`). واریانت‌ها در 11/05 آمدند و جای تحلیل کاملشان دوره‌ی جداگانه‌ی ژنومیک پزشکی است.

---

## جمع‌بندی

- ‏Ensembl آنوتیشن جداگانه‌ای از RefSeq است: ‏ENSG/ENST/ENSP با نسخه. MANE رونوشتی است که در هر دو یکسان است. برای NR3C1: ‏`ENST00000394464` = `NM_000176.3`، پروتئین ۷۷۷ اسید آمینه.
- ‏release 116 آخرین release سایت قدیمی است. سایت تازه در www.ensembl.org است و BioMart در jun2026.archive.ensembl.org.
- ‏REST: ‏`lookup` (ژن و رونوشت)، `xrefs` (پیوند به NCBI و…)، `sequence`، `homology`؛ چند ژن با یک POST.
- ‏BioMart: صافی + ستون ← جدول TSV؛ از مرورگر یا با XML و `curl`.
- در پایتون، `requests` با تکرار هنگام 429/500/503 کار را پایدار می‌کند.
- ‏Ensembl Bacteria: ‏rpoB با همان مختصات NCBI و شناسه‌ی locus tag ‏(`b3987`).

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
R=https://rest.ensembl.org; J="content-type=application/json"
curl -sS "$R/lookup/symbol/homo_sapiens/SYMBOL?$J"                   # gene by symbol
curl -sS "$R/lookup/id/ENSG…?expand=1;$J"                             # gene + transcripts + proteins
curl -sS "$R/xrefs/id/ENST…?$J"                                       # cross-references (RefSeq, CCDS, GO…)
curl -sS "$R/xrefs/id/ENSG…?external_db=EntrezGene;$J"                # only NCBI Gene ID
curl -sS "$R/sequence/id/ENST…?type=protein;$J"                       # sequence (cdna, cds, protein, genomic)
curl -sS "$R/homology/symbol/human/SYMBOL?type=orthologues;target_species=mouse;sequence=none;$J"
curl -sS -X POST "$R/lookup/symbol/homo_sapiens" -H "Content-Type: application/json" \
     -H "Accept: application/json" -d '{"symbols":["A","B"]}'        # many genes at once
M=https://jun2026.archive.ensembl.org/biomart/martservice
curl -sS -G --data-urlencode "query@query.xml" $M                     # BioMart XML query -> TSV
curl -sS "$M?type=attributes&dataset=hsapiens_gene_ensembl"           # list attribute names
python3 ens_ids.py SYMBOL ... > table.tsv                             # symbols -> Ensembl + NCBI IDs
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏Ensembl | پایگاه ژنوم و آنوتیشن EMBL-EBI |
| ‏GENCODE | آنوتیشن Ensembl برای انسان و موش |
| ‏ENSG / ENST / ENSP | شناسه‌ی ژن / رونوشت / پروتئین Ensembl |
| ‏stable ID و نسخه | شناسه‌ی ثابت، و عددی که با تغییر مدل بالا می‌رود |
| ‏release | نسخه‌ی شماره‌دار همه‌ی پایگاه (این درس: 116) |
| رونوشت canonical | رونوشت نماینده‌ی یک ژن در Ensembl |
| ‏MANE Select | رونوشتی که در RefSeq و Ensembl یکسان است |
| ‏CCDS | برچسب CDSهای یکسان در NCBI، Ensembl و UCSC |
| ‏REST API | دسترسی برنامه‌ای به داده با نشانی وب و پاسخ JSON |
| ‏endpoint | یک کار معین در API (مانند `lookup/symbol`) |
| ‏GET / POST | گونه‌ی درخواست: داده در نشانی / داده در بدنه |
| کد پاسخ HTTP | ‏200 درست، 400 درخواست نادرست، 429 تند رفتن، 500/503 گرفتاری سرور |
| ‏xref | پیوند یک رکورد به شناسه‌اش در پایگاه دیگر |
| ارتولوگ | ژن‌هایی در دو گونه که از یک ژن نیای مشترک آمده‌اند |
| ‏BioMart | ابزار ساخت جدول با صافی و ستون |
| صافی (filter) / ستون (attribute) | چه سطرهایی / چه ستون‌هایی در جدول BioMart |
| ‏locus tag | شناسه‌ی ژن در آنوتیشن یک ژنوم باکتری (مانند `b3987`) |

---

## منابع

**مقاله و مستند**
- ‏Yates AD, et al. (2026). *Ensembl 2026.* Nucleic Acids Res 54(D1):D1053–D1060. https://doi.org/10.1093/nar/gkaf1239
- ‏Dyer SC, et al. (2025). *Ensembl 2025.* Nucleic Acids Res 53(D1):D948–D957. https://doi.org/10.1093/nar/gkae1071
- ‏Yates A, et al. (2015). *The Ensembl REST API: Ensembl Data for Any Language.* Bioinformatics 31(1):143–145. https://doi.org/10.1093/bioinformatics/btu613
- ‏Kinsella RJ, et al. (2011). *Ensembl BioMarts: a hub for data retrieval across taxonomic space.* Database 2011:bar030. https://doi.org/10.1093/database/bar030
- ‏Morales J, et al. (2022). *A joint NCBI and EMBL-EBI transcript set for clinical genomics and research.* Nature 604:310–315. https://doi.org/10.1038/s41586-022-04558-8
- ‏Frankish A, et al. (2023). *GENCODE: reference annotation for the human and mouse genomes in 2023.* Nucleic Acids Res 51(D1):D942–D949. https://doi.org/10.1093/nar/gkac1071
- ‏Yates AD, et al. (2022). *Ensembl Genomes 2022.* Nucleic Acids Res 50(D1):D996–D1003. https://doi.org/10.1093/nar/gkab1007
- راهنمای REST: https://rest.ensembl.org · آموزش BioMart (EMBL-EBI Training): https://www.ebi.ac.uk/training/online/courses/ensembl-browser-series/data-export-with-biomart/ · فهرست بایگانی‌ها (هر بایگانی دست‌کم پنج سال): https://jun2026.archive.ensembl.org/info/website/archives/index.html
- خبر سایت تازه (EMBL-EBI، 2026-08-25): https://www.ebi.ac.uk/about/news/updates-from-data-resources/ensembl-new-website/

**کتاب**
- ‏Baxevanis AD, Bader GD, Wishart DS, eds. (2020). *Bioinformatics*, 4th ed. Wiley. (فصل ۴: *Genome Browsers*، نوشته‌ی Tyra G. Wolfsberg؛ Ensembl و UCSC)
- ‏Pevsner J (2015). *Bioinformatics and Functional Genomics*, 3rd ed. Wiley-Blackwell. (فصل ۲: دسترسی به داده‌های توالی؛ Ensembl و BioMart)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins): https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Genomic Data Science* (UC San Diego): https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science
- ‏YouTube: *Introduction to the Ensembl Genome Browser – Webinar 2: Genes & transcripts* (Ensembl Training): https://www.youtube.com/watch?v=j5JtUCrhXaQ
- ‏YouTube: *Introduction to the Ensembl Genome Browser – Webinar 6: BioMart* (Ensembl Training): https://www.youtube.com/watch?v=rUh4Sa7e-GM
- ‏YouTube: *EMBL-EBI, programmatically: Ensembl* (EMBL-EBI): https://www.youtube.com/watch?v=R2R9YOK8VQs

<sub>همه‌ی دستورها در 2026-10-27 روی سرور دوره اجرا شدند (Ensembl REST و BioMart، release 116). در آن روز REST و BioMart بارها 500/503 دادند و BioMart 116 نزدیک به ۱۵ دقیقه یکسره «Service unavailable» بود؛ پاسخ‌ها با تکرار گرفته شدند. سایت تازه‌ی Ensembl با جاوااسکریپت ساخته شده و از سرور دیده نشد، پس گام‌های مرورگر (✍️) از مستندات‌اند. DOIها با Crossref وارسی شدند؛ فیلم‌ها با noembed (هر سه از کانال‌های رسمی Ensembl و EMBL-EBI)؛ فصل کتاب Baxevanis از فهرست کتابخانه‌ای. Coursera از سرور در دسترس نیست (451).</sub>

</div>
