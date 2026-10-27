<div dir="rtl">

# درس: درگاه‌های بیان و سرطان؛ GTEx، Human Protein Atlas، Expression Atlas، GDC و cBioPortal

**بخش:** `12_V2_Global_Databases_Browsers` · **ماژول:** `06_Expression_Cancer_Portals` · **پیش‌نیاز:** ماژول‌های [11/04](../../11_V2_NCBI_Databases/04_GEO/) (GSE52778 و log2FC)، [11/05](../../11_V2_NCBI_Databases/05_Variation_Clinical/) (واریانت و dbGaP) و [12/01](../01_Ensembl_BioMart/) (شناسه و نسخه‌ی Ensembl)؛ `curl`، `jq`، `awk` · **زمان:** حدود ۹۰ دقیقه · **ابزار:** GTEx API v2 (داده‌ی GTEx v11)، Human Protein Atlas (25.1)، Expression Atlas، GDC API (Data Release 46.0)، cBioPortal API (v7.2.0) · **آخرین بازبینی:** 2026-10-27

> ✅ **وضعیت: اجرا شده.** همه‌ی خروجی‌ها واقعی‌اند (2026-10-27). نمودارهای بقا و OncoPrint در cBioPortal وب‌اند و از مستندات نوشته شدند (✍️).

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. بیان یک ژن را در **بافت‌های سالم** انسان از **GTEx** و **Human Protein Atlas** بگیرید و بخوانید.
2. نتیجه‌ی بازتحلیل یک آزمایش GEO را از **Expression Atlas** بگیرید و با تحلیل خودتان (11/04) بسنجید.
3. پروژه‌های سرطان **TCGA** را در **GDC** بشناسید و داده‌ی **باز** را از **کنترل‌شده** (dbGaP) جدا کنید.
4. جهش‌های یک ژن را در یک مطالعه‌ی **cBioPortal** بشمارید و **امضای جهشی** را ببینید.

**پیش از آغاز:**

<div dir="ltr">

```bash
mkdir -p ~/global/m06 && cd ~/global/m06
G=https://gtexportal.org/api/v2
X=https://www.ebi.ac.uk/gxa
GD=https://api.gdc.cancer.gov
C=https://www.cbioportal.org/api
```

</div>

---

## ۱. داستان

دو پرسش، دو گونه درگاه:
1. **بافت سالم:** گیرنده‌ی گلوکوکورتیکوئید (NR3C1) **کجا** در بدن بیان می‌شود؟ اگر دگزامتازون برای آسم داده شود، کدام بافت‌ها هم پاسخ می‌دهند؟ آیا دیگران پاسخ هشت ژن ما (11/04) را در همان داده تأیید کرده‌اند؟
2. **سرطان:** ‏**TP53** پرجهش‌ترین ژن سرطان‌های انسان است. در سرطان ریه چند درصد بیماران جهش دارند و جهش‌ها چه شکلی‌اند؟

**پاسخ معلوم:** ‏GR در کمابیش همه‌ی بافت‌ها هست (همه‌ی سلول‌ها به کورتیزول پاسخ می‌دهند). ‏TP53 در نزدیک به نیمی از آدنوکارسینومای ریه جهش دارد (Cancer Genome Atlas Research Network، ۲۰۱۴)، و جهش‌های ریه‌ی سیگاری‌ها بیشتر **G→T** است (Pfeifer و همکاران، ۲۰۰۲).

---

## ۲. مفهوم به زبان ساده

| درگاه | چه دارد | داده از |
| :--- | :--- | :--- |
| ‏**GTEx** | بیان ژن در ۵۴ بافت **سالم** نزدیک به هزار اهداکننده‌ی درگذشته؛ و eQTL | ‏RNA-seq |
| ‏**Human Protein Atlas** (HPA) | بیان **پروتئین** (رنگ‌آمیزی پادتن) و RNA در بافت‌ها، سلول‌ها، تک‌سلول و جای سلولی | پادتن + RNA-seq |
| ‏**Expression Atlas** (EMBL-EBI) | هزاران آزمایش GEO/ArrayExpress که **دوباره و یکسان** تحلیل شده‌اند | بازتحلیل |
| ‏**GDC** (NCI) | داده‌ی خام و پردازش‌شده‌ی **TCGA** و پروژه‌های سرطان دیگر | توالی‌یابی تومور |
| ‏**cBioPortal** | همان داده‌های سرطان، **خلاصه** و آماده‌ی تحلیل: جهش‌ها، بیان، بقا | پردازش‌شده |

**داده‌ی کنترل‌شده:** داده‌ای که می‌تواند **فرد** را شناسایی کند (ریدهای خام، واریانت‌های ارثی، ژنوتیپ‌ها) را نمی‌شود آزاد گذاشت. در آمریکا این داده‌ها در **dbGaP** هستند و دسترسی‌شان درخواست رسمی، کد اخلاق و تأیید کمیته می‌خواهد. داده‌ی **خلاصه** (بیان میانگین، جهش‌های سوماتیک تومور) باز است.

---

## ۳. گام ۱: ‏GTEx

### ۳.۱ نسخه‌ها و شناسه‌ی ژن

<div dir="ltr">

```bash
curl -sS "$G/metadata/dataset" | jq -r '.[] | select(.datasetId | test("^gtex_v")) | "\(.datasetId)\t\(.gencodeVersion)\t\(.genomeBuild)\t\(.rnaSeqSampleCount)"'
for v in v26 v47; do
  curl -sS "$G/reference/gene?geneId=NR3C1&gencodeVersion=$v" | jq -r --arg v $v '.data[0] | "\($v)\t\(.gencodeId)"'
done
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
gtex_v7	v19	GRCh37/hg19	11688
gtex_v8	v26	GRCh38/hg38	17382
gtex_v10	v39	GRCh38/hg38	19788
gtex_v11	v47	GRCh38/hg38	19788
v26	ENSG00000113580.14
v47	ENSG00000113580.15
```

</div>

**توضیح خروجی:**
- چهار نسخه‌ی GTEx، هر کدام با نسخه‌ی **GENCODE** خودش (12/01) و شمار نمونه‌های RNA-seq. ‏v11 تازه‌ترین است: ۱۹٬۷۸۸ نمونه.
- شناسه‌ی NR3C1 در GENCODE v26 ‏`.14` و در v47 ‏`.15` است؛ و در Ensembl 116 (12/01) ‏`.17`. هر نسخه‌ی GTEx شناسه‌ی نسخه‌دار خودش را می‌خواهد (همان تمرین ۶ ماژول 12/01).

### ۳.۲ بیان NR3C1 در بافت‌ها

<div dir="ltr">

```bash
id=$(curl -sS "$G/reference/gene?geneId=NR3C1&gencodeVersion=v47" | jq -r '.data[0].gencodeId')
curl -sS "$G/expression/medianGeneExpression?gencodeId=$id&datasetId=gtex_v11&itemsPerPage=100" > nr3c1_gtex.json
jq '.data | length' nr3c1_gtex.json
jq -r '.data[] | "\(.median)\t\(.tissueSiteDetailId)"' nr3c1_gtex.json | sort -gr | sed -n '1,5p;$p'
jq -r '.data[] | select(.tissueSiteDetailId == "Lung" or .tissueSiteDetailId == "Whole_Blood") | "\(.median)\t\(.tissueSiteDetailId)"' nr3c1_gtex.json
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`medianGeneExpression` | میانه‌ی بیان ژن در هر بافت (TPM) |
| ‏`datasetId=gtex_v11` | نسخه‌ی داده؛ باید با نسخه‌ی شناسه (v47) جور باشد |
| ‏`sort -gr` | مرتب کردن عددی (با پشتیبانی اعشار و نماد علمی)، از بزرگ به کوچک |
| ‏`sed -n '1,5p;$p'` | پنج سطر نخست و سطر پایانی |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
54
52.0879	Cells_EBV-transformed_lymphocytes
35.7116	Nerve_Tibial
35.5645	Adipose_Subcutaneous
34.4736	Cells_Cultured_fibroblasts
34.2031	Artery_Tibial
4.8988	Pancreas
26.2805	Lung
14.457	Whole_Blood
```

</div>

**توضیح خروجی:**
- ‏NR3C1 در **هر ۵۴** بافت بیان می‌شود، از ۴٫۹ ‏TPM (پانکراس) تا ۵۲ (لنفوسیت‌های کشت‌شده). ✅ پاسخ معلوم.
- ریه ۲۶ TPM، نزدیک میانه‌ی بافت‌ها: دگزامتازون استنشاقی هدف کافی دارد.
- ‏**TPM** (transcripts per million) مانند CPM ‏(11/04) است، با تصحیح طول ژن؛ پس ژن‌های گوناگون را هم می‌شود سنجید.

✍️ **در مرورگر:** ‏https://gtexportal.org ← نام ژن ← نمودار جعبه‌ای (violin) همه‌ی بافت‌ها، و برگه‌های **eQTL** (واریانت‌هایی که بیان این ژن را در یک بافت تغییر می‌دهند) و **تک‌سلول**.

> 📺 **فیلم:** *GTEx Portal: Visualizing Bulk RNA-Seq Gene Expression on the GTEx Portal* (Broad Institute): https://www.youtube.com/watch?v=WjHkb_y_yFk · *GTEx Portal: Retrieving GTEx Gene Expression Data via API* (Broad Institute): https://www.youtube.com/watch?v=NFyO0Pi0QJo
> 📄 **مرجع:** GTEx Consortium (2020). *The GTEx Consortium atlas of genetic regulatory effects across human tissues.* Science 369:1318–1330. https://doi.org/10.1126/science.aaz1776 · راهنمای API: https://gtexportal.org/api/v2/redoc

---

## ۴. گام ۲: ‏Human Protein Atlas

‏HPA برای هر ژن یک فایل JSON دارد (نشانی: شناسه‌ی Ensembl ژن):

<div dir="ltr">

```bash
curl -sS "https://www.proteinatlas.org/ENSG00000113580.json" > hpa.json
jq -r '["RNA tissue specificity", "RNA tissue distribution", "RNA single cell type specificity",
        "RNA single cell type specific nCPM", "Subcellular main location", "Reliability (IF)", "Protein class"][] as $k
       | "\($k)\t\(.[$k] | tostring | .[0:110])"' hpa.json
```

</div>

**تکه‌به‌تکه:** ‏`[…][] as $k` فهرست نام کلیدها را یکی‌یکی در `$k` می‌گذارد؛ `.[$k]` مقدار آن کلید است (کلیدها فاصله و پرانتز دارند، پس نمی‌شود `.RNA tissue…` نوشت). ‏`tostring | .[0:110]` فهرست‌ها را رشته می‌کند و کوتاه.

**خروجی واقعی (2026-10-27؛ HPA ‏25.1):**

<div dir="ltr">

```
RNA tissue specificity	Low tissue specificity
RNA tissue distribution	Detected in all
RNA single cell type specificity	Cell type enhanced
RNA single cell type specific nCPM	{"Corticotrophs":"1168.5","Myonuclei":"691.5","Neutrophils":"1012.2","pDCs":"861.8"}
Subcellular main location	["Nucleoplasm","Cytosol"]
Reliability (IF)	Supported
Protein class	["Disease related genes","FDA approved drug targets","Human disease related genes","Nuclear receptors","Plasma
```

</div>

**توضیح خروجی:**
- ‏«Low tissue specificity» و «Detected in all»: همان یافته‌ی GTEx، از داده‌ی دیگر. ✅
- در **تک‌سلول**، بیشترین بیان در **کورتیکوتروف‌ها**ست: سلول‌های هیپوفیز که ACTH می‌سازند. کورتیزول از همین‌جا با **بازخورد منفی** ساخت خودش را کم می‌کند. یک یافته‌ی زیستی درست، از یک سطر JSON.
- جای سلولی **هسته و سیتوزول**: GR بی هورمون در سیتوپلاسم با Hsp90 می‌ماند و با هورمون به هسته می‌رود (12/05). «Supported» یعنی رنگ‌آمیزی پادتن با داده‌های دیگر جور است.
- ‏«FDA approved drug targets»: هدف دگزامتازون، پردنیزولون و…

✍️ **در مرورگر:** ‏https://www.proteinatlas.org/ENSG00000113580-NR3C1 ← برگه‌های **Tissue** (تصویر رنگ‌آمیزی پادتن در هر بافت)، **Single cell**، **Subcellular** (تصویر ایمونوفلورسانس) و **Cancer** (پیش‌آگهی در TCGA).

> 📺 **فیلم:** *The Human Protein Atlas Tutorial Series: Protein expression by tissue*: https://www.youtube.com/watch?v=tOmNdhjXuRg
> 📄 **مرجع:** Uhlén M, et al. (2015). *Tissue-based map of the human proteome.* Science 347:1260419. https://doi.org/10.1126/science.1260419

---

## ۵. گام ۳: ‏Expression Atlas؛ پاسخ معلوم از دست دیگران

**چرا؟** در 11/04 نگاه نخست خودتان را به GSE52778 انداختید (CPM و log2FC، بی آمار). ‏Expression Atlas هزاران آزمایش GEO را با یک خط لوله‌ی **یکسان** (شمارش ریدها و آزمون آماری) دوباره تحلیل کرده است. آیا GSE52778 در آن هست؟

<div dir="ltr">

```bash
curl -sS "$X/json/experiments" | jq -r '.experiments[] | select(.experimentAccession == "E-GEOD-52778")
    | [.experimentAccession, .experimentType, .numberOfAssays, .experimentDescription] | @tsv'
curl -sS -o e52778.tsv "$X/experiments-content/E-GEOD-52778/resources/DifferentialSecondaryDataFiles.RnaSeq/analytics"
head -1 e52778.tsv | tr '\t' '\n' | cat -n
awk -F'\t' '$2 ~ /^(NR3C1|FKBP5|TSC22D3|ZBTB16|PER1|DUSP1|KLF15|CRISPLD2)$/ {print $2 "\t" $8 "\t" $7}' e52778.tsv | sort -k2,2gr
awk -F'\t' 'NR > 1 && $7 != "NA" && $7 < 0.05 {n++; if ($8 > 0) up++} END {print "dex significant:", n, " up:", up, " down:", n - up}' e52778.tsv
```

</div>

**تکه‌به‌تکه:** آزمایش‌های GEO در Expression Atlas نام `E-GEOD-` + شماره‌ی GSE می‌گیرند. ‏`tr '\t' '\n' | cat -n` نام ستون‌ها را یکی در هر سطر با شماره نشان می‌دهد تا بدانیم ستون ۷ و ۸ کدام‌اند.

**خروجی واقعی (2026-10-27؛ فایل ۳ مگابایت):**

<div dir="ltr">

```
E-GEOD-52778	Differential	16	Human Airway Smooth Muscle Transcriptome Changes in Response to Asthma Medications
     1	Gene ID
     2	Gene Name
     3	'albuterol' vs 'untreated'.p-value
     4	'albuterol' vs 'untreated'.log2foldchange
     5	'albuterol and dexamethasone' vs 'untreated'.p-value
     6	'albuterol and dexamethasone' vs 'untreated'.log2foldchange
     7	'dexamethasone' vs 'untreated'.p-value
     8	'dexamethasone' vs 'untreated'.log2foldchange
ZBTB16	5.1	6.86058922235706e-50
KLF15	3.4	1.64473317212109e-22
FKBP5	3.3	1.40689523620271e-30
PER1	3	7.73341351007452e-42
DUSP1	2.8	7.40591581311764e-47
TSC22D3	2.8	4.05182798467439e-19
CRISPLD2	2.4	5.03939771621054e-23
NR3C1	-1	1.99837866703494e-08
dex significant: 2142  up: 1233  down: 909
```

</div>

**توضیح خروجی:**
- ‏GSE52778 بازتحلیل شده است: ۱۶ نمونه، سه مقایسه (آلبوترول، هر دو، دگزامتازون در برابر بی‌تیمار).
- **هفت** ژن با دگزامتازون بالا رفته‌اند (log2FC ‏۲٫۴ تا ۵٫۱، یعنی ۵ تا ۳۴ برابر) و **NR3C1 پایین** (‏−۱، نصف). درست همان نتیجه‌ی نگاه نخست شما در 11/04، این‌بار با آمار و p-value بسیار کوچک. ✅ ‏ZBTB16 بیشترین تغییر را دارد.
- در کل ۲۱۴۲ ژن با آستانه‌ی ۰٫۰۵ تغییر کرده‌اند: ۱۲۳۳ بالا و ۹۰۹ پایین. بخش ۱۳ همین تحلیل را با DESeq2 خودتان می‌سازید و می‌توانید با این فایل بسنجید.
- این‌که ستون «p-value» این فایل خام است یا برای آزمون‌های بسیار تصحیح شده، در خود فایل گفته نشده است. پیش از به کار بردن آستانه، آن را در راهنمای Expression Atlas (https://www.ebi.ac.uk/gxa/FAQ.html) بسنجید؛ بخش ۱۴ فرق این دو را باز می‌کند.

> 📺 **فیلم:** *Expression Atlas – Gene expression across different species and biological conditions* (EMBL-EBI): https://www.youtube.com/watch?v=uKgwBCdcqfQ
> 📄 **مرجع:** Moreno P, et al. (2022). *Expression Atlas update: gene and protein expression in multiple species.* Nucleic Acids Res 50(D1):D129–D140. https://doi.org/10.1093/nar/gkab1030

---

## ۶. گام ۴: ‏GDC و TCGA

‏**TCGA** (The Cancer Genome Atlas) بیش از ۱۱ هزار بیمار در ۳۳ گونه سرطان را توالی‌یابی کرد. داده‌اش اکنون در **GDC** (Genomic Data Commons، NCI) است، کنار پروژه‌های تازه‌تر (CPTAC، …).

<div dir="ltr">

```bash
curl -sS "$GD/status" | jq -r '.data_release'
curl -sS -G "$GD/projects" --data-urlencode 'filters={"op":"in","content":{"field":"program.name","value":["TCGA"]}}' \
     --data-urlencode "size=0" | jq '.data.pagination.total'
curl -sS -G "$GD/projects/TCGA-LUAD" --data-urlencode "expand=summary" | jq -c '.data | {project_id, name, cases: .summary.case_count, files: .summary.file_count}'
F='{"op":"in","content":{"field":"cases.project.project_id","value":["TCGA-LUAD"]}}'
curl -sS -G "$GD/files" --data-urlencode "filters=$F" --data-urlencode "facets=access" --data-urlencode "size=0" \
  | jq -r '.data.aggregations.access.buckets[] | "\(.doc_count)\t\(.key)"'
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`-G --data-urlencode` | پارامترها را کدگذاری کن و با GET بفرست (12/01، BioMart) |
| ‏`filters={"op":"in",…}` | صافی GDC به شکل JSON: «فیلد X یکی از این مقدارها باشد» |
| ‏`size=0` | خود رکوردها را نفرست؛ تنها شمار و facetها |
| ‏`facets=access` | شمار فایل‌ها بر پایه‌ی مقدار فیلد `access` |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
Data Release 46.0 - August 10, 2026
33
{"project_id":"TCGA-LUAD","name":"Lung Adenocarcinoma","cases":585,"files":36740}
22687	controlled
14053	open
```

</div>

**توضیح خروجی:**
- ‏GDC ‏Release 46، با **۳۳** پروژه‌ی TCGA. ‏TCGA-LUAD (آدنوکارسینومای ریه) ‏۵۸۵ بیمار و ۳۶٬۷۴۰ فایل دارد.
- **۲۲٬۶۸۷ فایل (۶۲٪) کنترل‌شده**‌اند: ریدهای خام (BAM)، واریانت‌های ارثی و فایل‌های جهش با جزئیات. تنها ۱۴٬۰۵۳ فایل باز است (جهش‌های سوماتیک پالایش‌شده، بیان، داده‌ی بالینی). برای کنترل‌شده‌ها درخواست **dbGaP** (پروژه‌ی TCGA ‏`phs000178`) و تأیید نهاد پژوهشی لازم است.

**یک دام:** شمردن جهش‌های TP53 با facet روی تغییر اسید آمینه:

<div dir="ltr">

```bash
F2='{"op":"in","content":{"field":"ssm.consequence.transcript.gene.symbol","value":["TP53"]}}'
curl -sS -G "$GD/ssm_occurrences" --data-urlencode "filters=$F2" --data-urlencode "facets=ssm.consequence.transcript.aa_change" \
     --data-urlencode "size=0" | jq -r '.data.aggregations["ssm.consequence.transcript.aa_change"].buckets[:6][] | "\(.doc_count)\t\(.key)"'
```

</div>

<div dir="ltr">

```
229	r136h
229	r175h
185	r234c
181	r209q
181	r248q
185	r273c
```

</div>

‏`r175h` و `r136h` هر دو **۲۲۹** بار؛ و `r248q` و `r209q` هر دو ۱۸۱. این‌ها **یک** جهش‌اند با شماره‌گذاری دو **رونوشت** گوناگون TP53: ‏۱۷۵ − ۳۹ = ۱۳۶ (ایزوفرم Δ40p53 که ۳۹ اسید آمینه‌ی آغاز را ندارد). ‏GDC هر جهش را روی همه‌ی رونوشت‌ها گزارش می‌کند و facet همه را می‌شمارد. باز همان درس 11/07 و 12/04: **همیشه بگویید کدام رونوشت**. برای جهش‌ها روی رونوشت canonical، cBioPortal ساده‌تر است.

> 📺 **فیلم:** برای GDC فیلم رسمی وارسی‌شده‌ای نیافتیم؛ راهنمای GDC API: https://docs.gdc.cancer.gov/API/Users_Guide/Getting_Started/
> 📄 **مرجع:** Grossman RL, et al. (2016). *Toward a Shared Vision for Cancer Genomic Data.* N Engl J Med 375:1109–1112. https://doi.org/10.1056/NEJMp1607591 · Mailman MD, et al. (2007). *The NCBI dbGaP database of genotypes and phenotypes.* Nat Genet 39:1181–1186. https://doi.org/10.1038/ng1007-1181

---

## ۷. گام ۵: ‏cBioPortal

‏cBioPortal همان داده‌ی TCGA (و صدها مطالعه‌ی دیگر) را به شکل آماده‌ی تحلیل دارد. ما مطالعه‌ی **PanCancer Atlas** ریه را برمی‌گزینیم (همه‌ی ۳۳ سرطان TCGA در ۲۰۱۸ با یک خط لوله دوباره پردازش شدند).

<div dir="ltr">

```bash
curl -sS "$C/info" | jq -r '.portalVersion'
curl -sS "$C/studies/luad_tcga_pan_can_atlas_2018" | jq -c '{studyId, name, allSampleCount}'
curl -sS -X POST -H "Content-Type: application/json" \
  "$C/molecular-profiles/luad_tcga_pan_can_atlas_2018_mutations/mutations/fetch?projection=DETAILED" \
  -d '{"entrezGeneIds": [7157], "sampleListId": "luad_tcga_pan_can_atlas_2018_all"}' > tp53_luad.json
jq 'length' tp53_luad.json
jq '[.[].sampleId] | unique | length' tp53_luad.json
jq -r '.[].mutationType' tp53_luad.json | sort | uniq -c | sort -rn | head -4
jq -r '.[].proteinChange' tp53_luad.json | sort | uniq -c | sort -rn | head -5
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`molecular-profiles/…_mutations` | پروفایل جهش این مطالعه (هر مطالعه پروفایل بیان، CNA و… هم دارد) |
| ‏`"entrezGeneIds": [7157]` | ‏TP53 با NCBI Gene ID (11/02) |
| ‏`sampleListId: …_all` | همه‌ی نمونه‌های مطالعه |
| ‏`projection=DETAILED` | جزئیات کامل (باز مرجع و جهش‌یافته، جایگاه) |

**خروجی واقعی (2026-10-27؛ cBioPortal v7.2.0):**

<div dir="ltr">

```
v7.2.0
{"studyId":"luad_tcga_pan_can_atlas_2018","name":"Lung Adenocarcinoma (TCGA, PanCancer Atlas)","allSampleCount":566}
314
295
    195 Missense_Mutation
     55 Nonsense_Mutation
     24 Frame_Shift_Del
     23 Splice_Site
     10 X125_splice
      6 R273L
      6 R158L
      5 X126_splice
      5 G245V
```

</div>

**توضیح خروجی:**
- ‏۳۱۴ جهش در **۲۹۵** نمونه از ۵۶۶: ‏**۵۲٪** آدنوکارسینوماهای ریه TP53 جهش‌یافته دارند. ✅ پاسخ معلوم. (برخی نمونه‌ها دو جهش دارند.)
- بیشترشان **missense**‌اند (یک اسید آمینه عوض شده؛ پروتئین هست ولی کار نمی‌کند یا بدتر)، و بقیه پروتئین را کوتاه می‌کنند (nonsense، frameshift، splice).
- پرتکرارترین‌ها **R273L**، **R158L**، **G245V**: هر سه از جهش **G→T** (یا C→A روی رشته‌ی دیگر). این **امضای دود تنباکو**ست: بنزوپیرن به G می‌چسبد و هنگام همانندسازی، روبه‌رویش A گذاشته می‌شود. تمرین ۴ این را با شمردن همه‌ی جهش‌ها در ریه و روده‌ی بزرگ می‌سنجد.

✍️ **در مرورگر:** ‏https://www.cbioportal.org ← مطالعه‌ی *Lung Adenocarcinoma (TCGA, PanCancer Atlas)* ← **Query by gene**: ‏`TP53 KRAS EGFR` ← برگه‌ی **OncoPrint** (هر ستون یک بیمار، هر سطر یک ژن؛ می‌بینید جهش KRAS و EGFR کمتر با هم می‌آیند)، **Mutations** (نقشه‌ی جهش‌ها روی دامنه‌های پروتئین، مانند 12/04)، و **Comparison/Survival** (منحنی کاپلان-مایر بقا برای بیماران با و بی جهش).

> 📺 **فیلم:** *cBioPortal Webinar 1: Introduction* (cBioPortal): https://www.youtube.com/watch?v=fPIAxH--cSo · *cBioPortal Webinar 5: API & R Client* (cBioPortal): https://www.youtube.com/watch?v=Nq12o2i0yaw
> 📄 **مرجع:** Cerami E, et al. (2012). *The cBio Cancer Genomics Portal.* Cancer Discov 2:401–404. https://doi.org/10.1158/2159-8290.CD-12-0095 · Gao J, et al. (2013). *Integrative Analysis of Complex Cancer Genomics and Clinical Profiles Using the cBioPortal.* Sci Signal 6:pl1. https://doi.org/10.1126/scisignal.2004088 · Hoadley KA, et al. (2018). *Cell-of-Origin Patterns Dominate the Molecular Classification of 10,000 Tumors from 33 Types of Cancer.* Cell 173:291–304. https://doi.org/10.1016/j.cell.2018.03.022

---

## ۸. سه اشتباه رایج

1. **آمیختن نسخه‌ها.** ‏GTEx v8 با GENCODE v26 و v11 با v47؛ شناسه‌ی نسخه‌دار یکی به کار دیگری نمی‌آید. نسخه‌ی داده و آنوتیشن را با هم بنویسید.
2. **شمردن یک جهش چند بار.** در GDC، ‏R175H و R136H یک جهش‌اند روی دو رونوشت؛ در cBioPortal یک بیمار گاهی دو جهش TP53 دارد (۳۱۴ جهش، ۲۹۵ نمونه). درصد بیماران را از **نمونه‌های یکتا** بشمارید.
3. **پنداشتن این‌که همه‌ی داده باز است.** ‏۶۲٪ فایل‌های TCGA-LUAD کنترل‌شده‌اند. برای پایان‌نامه‌ای که ریدهای خام بیماران را می‌خواهد، ماه‌ها پیش درخواست dbGaP بدهید؛ و هرگز داده‌ی کنترل‌شده را در گیت‌هاب یا ابر عمومی نگذارید.

---

## 📘 برای کنجکاوها

- ‏**eQTL در GTEx:** برگه‌ی eQTL نشان می‌دهد کدام SNPها بیان NR3C1 را در کدام بافت جابه‌جا می‌کنند؛ پیوند GWAS و بیان (بخش ۱۹).
- **امضاهای جهشی (COSMIC SBS):** الگوی ۹۶ گانه‌ی جهش‌ها (هر جانشینی با باز پیش و پس) را به فرایندهایی چون دود (SBS4)، UV ‏(SBS7) یا پیری (SBS1) نسبت می‌دهد (Alexandrov و همکاران، ۲۰۱۳).
- ‏**TCGA در R:** بسته‌ی `TCGAbiolinks` همین داده‌های باز GDC را به R می‌آورد؛ و `cBioPortalData` همان API ‏cBioPortal را.

---

## جمع‌بندی

- ‏GTEx (‏v11، ۵۴ بافت): ‏NR3C1 در همه‌ی بافت‌ها، ۴٫۹ تا ۵۲ TPM. ‏HPA ‏(25.1): «Low tissue specificity»، بیشینه در کورتیکوتروف‌ها، هسته و سیتوزول.
- ‏Expression Atlas بازتحلیل E-GEOD-52778 را دارد: هفت ژن بالا، NR3C1 پایین؛ تأیید 11/04.
- ‏GDC (Release 46): ‏۳۳ پروژه‌ی TCGA؛ TCGA-LUAD ‏۵۸۵ بیمار و ۶۲٪ فایل‌ها کنترل‌شده (dbGaP). جهش‌ها روی چند رونوشت شمرده می‌شوند.
- ‏cBioPortal: ‏TP53 در ۵۲٪ آدنوکارسینومای ریه، با جهش‌های G→T (امضای دود).

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
G=https://gtexportal.org/api/v2
curl -sS "$G/metadata/dataset"                                                    # GTEx versions
curl -sS "$G/reference/gene?geneId=SYMBOL&gencodeVersion=v47"                     # versioned gene id
curl -sS "$G/expression/medianGeneExpression?gencodeId=ID&datasetId=gtex_v11&itemsPerPage=100"
curl -sS "https://www.proteinatlas.org/ENSG….json"                                # HPA summary of one gene
curl -sS "https://www.ebi.ac.uk/gxa/json/experiments"                             # Expression Atlas experiments
curl -sS "https://www.ebi.ac.uk/gxa/experiments-content/E-GEOD-N/resources/DifferentialSecondaryDataFiles.RnaSeq/analytics"
GD=https://api.gdc.cancer.gov
curl -sS -G "$GD/files" --data-urlencode 'filters={…}' --data-urlencode "facets=access" --data-urlencode "size=0"
C=https://www.cbioportal.org/api
curl -sS -X POST -H "Content-Type: application/json" "$C/molecular-profiles/STUDY_mutations/mutations/fetch?projection=DETAILED" \
     -d '{"entrezGeneIds": [ID], "sampleListId": "STUDY_all"}'
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏GTEx | پروژه‌ی بیان ژن در بافت‌های سالم انسان |
| ‏TPM | رونوشت در هر میلیون، با تصحیح طول ژن |
| ‏eQTL | واریانتی که بیان یک ژن را تغییر می‌دهد |
| ‏HPA | اطلس پروتئین انسان: پادتن، RNA، تک‌سلول، جای سلولی |
| ‏Expression Atlas | بازتحلیل یکسان آزمایش‌های بیان (EMBL-EBI) |
| ‏TCGA / GDC | پروژه‌ی ژنوم سرطان / درگاه داده‌ی سرطان NCI |
| داده‌ی کنترل‌شده (dbGaP) | داده‌ی قابل شناسایی فرد، با دسترسی پس از تأیید |
| جهش سوماتیک | جهشی که تنها در تومور است، نه در سلول‌های دیگر فرد |
| ‏missense / nonsense / frameshift | جانشینی اسید آمینه / کدون پایان زودرس / جابه‌جایی چارچوب |
| ‏OncoPrint | جدول تصویری ژن × بیمار برای جهش‌ها |
| امضای جهشی | الگوی جهش‌ها که فرایند سازنده‌شان را نشان می‌دهد (مانند G→T برای دود) |
| ‏PanCancer Atlas | بازپردازش یکسان همه‌ی سرطان‌های TCGA (۲۰۱۸) |

---

## منابع

**مقاله و مستند**
- ‏GTEx Consortium (2020). *The GTEx Consortium atlas of genetic regulatory effects across human tissues.* Science 369:1318–1330. https://doi.org/10.1126/science.aaz1776
- ‏Uhlén M, et al. (2015). *Tissue-based map of the human proteome.* Science 347:1260419. https://doi.org/10.1126/science.1260419
- ‏Moreno P, et al. (2022). *Expression Atlas update: gene and protein expression in multiple species.* Nucleic Acids Res 50(D1):D129–D140. https://doi.org/10.1093/nar/gkab1030
- ‏Grossman RL, et al. (2016). *Toward a Shared Vision for Cancer Genomic Data.* N Engl J Med 375:1109–1112. https://doi.org/10.1056/NEJMp1607591
- ‏Cerami E, et al. (2012). *The cBio Cancer Genomics Portal.* Cancer Discov 2:401–404. https://doi.org/10.1158/2159-8290.CD-12-0095
- ‏Gao J, et al. (2013). *Integrative Analysis of Complex Cancer Genomics and Clinical Profiles Using the cBioPortal.* Sci Signal 6:pl1. https://doi.org/10.1126/scisignal.2004088
- ‏Hoadley KA, et al. (2018). *Cell-of-Origin Patterns Dominate the Molecular Classification of 10,000 Tumors from 33 Types of Cancer.* Cell 173:291–304. https://doi.org/10.1016/j.cell.2018.03.022
- ‏Pfeifer GP, et al. (2002). *Tobacco smoke carcinogens, DNA damage and p53 mutations in smoking-associated cancers.* Oncogene 21:7435–7451. https://doi.org/10.1038/sj.onc.1205803
- ‏Alexandrov LB, et al. (2013). *Signatures of mutational processes in human cancer.* Nature 500:415–421. https://doi.org/10.1038/nature12477
- ‏Mailman MD, et al. (2007). *The NCBI dbGaP database of genotypes and phenotypes.* Nat Genet 39:1181–1186. https://doi.org/10.1038/ng1007-1181

**کتاب**
- ‏Weinberg RA (2013). *The Biology of Cancer*, 2nd ed. Garland Science. (فصل ۹: p53 و آپوپتوز)
- ‏Pevsner J (2015). *Bioinformatics and Functional Genomics*, 3rd ed. Wiley-Blackwell. (فصل سرطان و ژنوم: TCGA)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Genomic Medicine Gets Personal* (Georgetown): https://www.coursera.org/learn/genomic-medicine
- ‏edX: *Essentials of Genomics and Biomedical Informatics* (IsraelX): https://www.edx.org/learn/medicine/israelx-essentials-of-genomics-and-biomedical-informatics
- ‏YouTube: *cBioPortal Webinar 2: Mutation Details & Patient View* (cBioPortal): https://www.youtube.com/watch?v=uJsp9kd2jIk
- ‏YouTube: *GTEx Portal: Visualizing Bulk RNA-Seq Gene Expression on the GTEx Portal* (Broad Institute): https://www.youtube.com/watch?v=WjHkb_y_yFk
- ‏YouTube: *Expression Atlas – Gene expression across different species and biological conditions* (EMBL-EBI): https://www.youtube.com/watch?v=uKgwBCdcqfQ

<sub>همه‌ی دستورها در 2026-10-27 روی سرور دوره اجرا شدند (GTEx API v2، HPA 25.1، Expression Atlas، GDC Release 46.0، cBioPortal v7.2.0). نمودارهای OncoPrint و بقا وب‌اند (✍️). DOIها با Crossref وارسی شدند؛ فیلم‌ها با noembed. شماره‌ی فصل کتاب Weinberg در وارسی پایانی سنجیده شود.</sub>

</div>
