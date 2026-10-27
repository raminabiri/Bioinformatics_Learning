<div dir="rtl">

# درس: هستی‌شناسی ژن و پایگاه‌های مسیر؛ GO، KEGG، Reactome، WikiPathways و MSigDB

**بخش:** `12_V2_Global_Databases_Browsers` · **ماژول:** `05_Pathway_Ontology_Resources` · **پیش‌نیاز:** ماژول [12/01](../01_Ensembl_BioMart/) (هشت ژن پاسخ به دگزامتازون و شناسه‌هایشان)؛ ماژول [12/04](../04_Protein_Families_Domains/) (دامنه‌ها)؛ `curl`، `jq`، `awk` · **زمان:** حدود ۹۰ دقیقه · **ابزار:** QuickGO API، KEGG REST، Reactome Content و Analysis Service (release 97)، WikiPathways JSON، MSigDB (2026.2.Hs)؛ AmiGO (وب، ✍️) · **آخرین بازبینی:** 2026-10-27

> ✅ **وضعیت: اجرا شده.** همه‌ی خروجی‌ها واقعی‌اند (2026-10-27). جست‌وجوی کلیدواژه در MSigDB نام‌نویسی (ایمیل) می‌خواهد و از سرور انجام نشد (✍️)؛ دانلود هر مجموعه‌ژن با نامش بی نام‌نویسی کار کرد.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. سه شاخه‌ی **GO** و ساختار گرافی آن را توضیح دهید و **کدهای شاهد** (IDA، IPI، IEA…) را بخوانید.
2. آنوتیشن‌های GO یک پروتئین را با **QuickGO API** بگیرید و تجربی را از خودکار جدا کنید.
3. یک ژن را در **KEGG** (مسیر و KO) و **Reactome** دنبال کنید.
4. مسیرهای **WikiPathways** و مجموعه‌ژن‌های **MSigDB** را بیابید و بدانید با هم چه فرقی دارند.
5. یک **تحلیل غنی‌سازی** کوچک در Reactome بزنید و یک دام بزرگ آن (شمردن ایزوفرم‌ها) را ببینید؛ پیش‌زمینه‌ی بخش ۱۴.

**پیش از آغاز:**

<div dir="ltr">

```bash
mkdir -p ~/global/m05 && cd ~/global/m05
P=~/Bioinformatics_Learning-main/12_V2_Global_Databases_Browsers/99_scripts_data
cp $P/05_Pathway_Ontology_Resources/data/* .        # dex8_symbols.txt, dex8_ids.tsv, hallmark_names.txt
cat dex8_ids.tsv
```

</div>

<div dir="ltr">

```
symbol	ncbi_gene_id
NR3C1	2908
FKBP5	2289
TSC22D3	1831
ZBTB16	7704
PER1	5187
DUSP1	1843
KLF15	28999
CRISPLD2	83716
```

</div>

---

## ۱. داستان

در 11/04 هشت ژن یافتید که دگزامتازون آن‌ها را در سلول‌های راه هوایی جابه‌جا می‌کند، و در 12/01 شناسه‌هایشان را در Ensembl و NCBI. پرسش بعدی هر زیست‌شناس: «این ژن‌ها **چه می‌کنند** و **با هم** در کدام فرایندند؟». برای این پرسش پنج منبع بزرگ هست: **GO** (کارکرد هر ژن)، **KEGG**، **Reactome** و **WikiPathways** (مسیرها) و **MSigDB** (مجموعه‌ژن‌ها برای غنی‌سازی). بخش ۱۴ تحلیل غنی‌سازی را کامل آموزش می‌دهد؛ این درس منبع‌ها را می‌شناساند.

**پاسخ معلوم:** گیرنده‌ی گلوکوکورتیکوئید (NR3C1) یک **عامل رونویسی وابسته به لیگاند** است که با **Hsp90** همراه است؛ FKBP5 هم‌یار Hsp90 است؛ PER1 ژن **ساعت شبانه‌روزی** است؛ گلوکوکورتیکوئیدها ساعت بدن را تنظیم می‌کنند. منبع خوب باید این‌ها را نشان دهد.

---

## ۲. مفهوم به زبان ساده

### ‏۲.۱ ‏Gene Ontology: واژه‌نامه‌ی کارکرد

‏GO یک **واژه‌نامه‌ی کنترل‌شده** است: به جای این‌که هر کس بنویسد «اتصال به DNA» یا «DNA-binding» یا «binds DNA»، همه **یک** شناسه می‌گذارند: `GO:0003677`. سه شاخه:

| شاخه | پرسش | نمونه برای GR |
| :--- | :--- | :--- |
| ‏**MF** ‏(molecular function) | مولکول به تنهایی چه می‌کند؟ | فعالیت گیرنده‌ی هسته‌ای |
| ‏**BP** ‏(biological process) | در کدام برنامه‌ی بزرگ‌تر شرکت دارد؟ | تنظیم رونویسی |
| ‏**CC** ‏(cellular component) | کجای سلول است؟ | هسته، سیتوپلاسم |

اصطلاح‌ها یک **گراف** (DAG) می‌سازند، نه درخت: هر اصطلاح می‌تواند **چند پدر** داشته باشد. اگر ژنی «فعالیت گیرنده‌ی گلوکوکورتیکوئید» دارد، خودبه‌خود همه‌ی پدرانش را هم دارد (قاعده‌ی **true path**).

### ۲.۲ کد شاهد (evidence code)

هر **آنوتیشن** (ژن + اصطلاح GO) یک کد دارد که می‌گوید از کجا آمده است:

| کد | معنا | اعتبار |
| :--- | :--- | :--- |
| ‏**IDA** | سنجش مستقیم (Inferred from Direct Assay) | آزمایشی |
| ‏**IPI** | برهم‌کنش فیزیکی (Physical Interaction) | آزمایشی |
| ‏**IMP** / **IGI** | جهش یا برهم‌کنش ژنی | آزمایشی |
| ‏**EXP** / **IEP** | آزمایشی کلی / الگوی بیان | آزمایشی |
| ‏**IBA** / **ISS** / **ISA** | از خویشاوندان دودمانی یا شباهت توالی | استنباطی، بازبینی‌شده |
| ‏**TAS** / **NAS** / **IC** | گفته‌ی نویسنده‌ی مقاله یا داور | نظر کارشناس |
| ‏**IEA** | خودکار، بی بازبینی انسان (برای نمونه از دامنه‌های InterPro، 12/04) | خودکار |

### ۲.۳ مسیر در برابر مجموعه‌ژن

- **مسیر** (KEGG، Reactome، WikiPathways): نقشه‌ای با **پیکان‌ها**: کدام پروتئین کدام را فعال می‌کند، کدام واکنش پس از کدام است.
- **مجموعه‌ژن** (MSigDB): تنها **فهرست** نام ژن‌ها، بی پیکان؛ برای نمونه «ژن‌هایی که با TNF بالا می‌روند». برای غنی‌سازی بس است.

---

## ۳. گام ۱: ‏GO با QuickGO

### ۳.۱ همه‌ی آنوتیشن‌های GR

<div dir="ltr">

```bash
Q=https://www.ebi.ac.uk/QuickGO/services
H="Accept: application/json"
curl -sS -H "$H" "$Q/annotation/search?geneProductId=P04150&limit=200" > gr_go.json
jq '.numberOfHits' gr_go.json
jq -r '.results[].goAspect' gr_go.json | sort | uniq -c
jq -r '.results[].goEvidence' gr_go.json | sort | uniq -c | sort -rn
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`annotation/search` | آنوتیشن‌های GO؛ QuickGO از پایگاه GOA ‏(EMBL-EBI) |
| ‏`geneProductId=P04150` | شناسه‌ی UniProt ‏GR (12/04) |
| ‏`limit=200` | بیشینه‌ی سطر در یک صفحه (پیش‌فرض ۲۵) |
| ‏`-H "Accept: application/json"` | پاسخ JSON بخواه |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
147
     32 biological_process
     47 cellular_component
     68 molecular_function
     39 IPI
     39 IDA
     34 IEA
     16 TAS
      6 IBA
      6 EXP
      3 IMP
      2 ISA
      1 ISS
      1 IC
```

</div>

**توضیح خروجی:**
- ‏۱۴۷ آنوتیشن. یک اصطلاح می‌تواند چند بار بیاید، با کدهای گوناگون یا از مقاله‌های گوناگون.
- ‏۸۷ تا (IDA ‏۳۹ + IPI ‏۳۹ + EXP ‏۶ + IMP ‏۳) **آزمایشی**‌اند، و ۳۴ تا (۲۳٪) **IEA**، یعنی خودکار. GR از پرپژوهش‌ترین پروتئین‌هاست؛ برای بیشتر پروتئین‌ها (به‌ویژه در گونه‌های کم‌پژوهش) بیشترِ آنوتیشن‌ها IEA است.

### ۳.۲ کدام اصطلاح، با کدام شاهد؟

‏QuickGO تنها شناسه می‌دهد. نام‌ها را با endpoint ‏`ontology/go/terms` می‌گیریم و با `awk` به آنوتیشن‌ها می‌چسبانیم (همان الگوی جفت کردن دو فایل در 12/02):

<div dir="ltr">

```bash
ids=$(jq -r '[.results[] | select(.goAspect == "molecular_function") | .goId] | unique | join(",")' gr_go.json)
curl -sS -H "$H" "$Q/ontology/go/terms/$ids" | jq -r '.results[] | "\(.id)\t\(.name)"' > mf_names.tsv
jq -r '.results[] | select(.goAspect == "molecular_function") | "\(.goId)\t\(.goEvidence)"' gr_go.json | sort -u \
  | awk -F'\t' 'NR == FNR {name[$1] = $2; next} {ev[$1] = ev[$1] " " $2} END {for (g in ev) print g "\t" name[g] "\t" ev[g]}' mf_names.tsv - \
  | sort -t$'\t' -k2,2 | grep -E 'glucocorticoid|steroid|Hsp90|estrogen|zinc|nuclear receptor'
```

</div>

**تکه‌به‌تکه:** ‏`unique | join(",")` شناسه‌های یکتا را با `,` به هم می‌چسباند (QuickGO چند شناسه را در یک درخواست می‌پذیرد). در `awk`، ‏`NR == FNR` یعنی «هنوز فایل نخست را می‌خوانی» (نام‌ها را نگه دار)؛ `-` یعنی فایل دوم ورودی لوله است؛ و `ev[$1] = ev[$1] " " $2` کدهای هر اصطلاح را کنار هم می‌گذارد.

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
GO:0034056	estrogen response element binding	 IBA
GO:0051879	Hsp90 protein binding	 IPI
GO:0004883	nuclear glucocorticoid receptor activity	 IEA TAS
GO:0004879	nuclear receptor activity	 IBA IDA
GO:0003707	nuclear steroid receptor activity	 IEA
GO:0005496	steroid binding	 IDA IEA
GO:1990239	steroid hormone binding	 IDA
GO:0008270	zinc ion binding	 IEA
```

</div>

**توضیح خروجی:**
- ‏**Hsp90 protein binding** با IPI: آزمایش برهم‌کنش. ✅ همان پاسخ معلوم.
- **ویژه‌ترین** اصطلاح، «nuclear glucocorticoid receptor activity»، **هیچ** شاهد IDA ندارد: تنها IEA و TAS. پدرش «nuclear receptor activity» IDA دارد. یعنی آزمایش‌ها چیزی کلی‌تر را سنجیده‌اند و کارشناس (TAS) گام آخر را برداشته است.
- ‏**estrogen response element binding** با **IBA**: از خویشاوندان (گیرنده‌های دیگر خانواده‌ی NR3) به GR رسیده است. GR در واقع به **عنصر پاسخ گلوکوکورتیکوئید** (GRE) می‌چسبد. ‏IBA سودمند است، ولی گاهی ویژگی یک عضو خانواده را به همه می‌دهد.
- ‏**zinc ion binding** با IEA: از دامنه‌ی انگشت روی (12/04) آمده است؛ همان کاری که InterPro2GO خودکار می‌کند.

### ۳.۳ گراف: پدران یک اصطلاح

<div dir="ltr">

```bash
anc=$(curl -sS -H "$H" "$Q/ontology/go/terms/GO:0004883/ancestors?relations=is_a" | jq -r '.results[0].ancestors | join(",")')
curl -sS -H "$H" "$Q/ontology/go/terms/$anc" | jq -r '.results[] | "\(.id)\t\(.name)"'
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
GO:0038023	signaling receptor activity
GO:0003674	molecular_function
GO:0004883	nuclear glucocorticoid receptor activity
GO:0004879	nuclear receptor activity
GO:0098531	ligand-modulated transcription factor activity
GO:0060089	molecular transducer activity
GO:0003700	DNA-binding transcription factor activity
GO:0003707	nuclear steroid receptor activity
GO:0000981	DNA-binding transcription factor activity, RNA polymerase II-specific
GO:0140110	transcription regulator activity
```

</div>

مسیرهای `is_a` از این اصطلاح تا ریشه را هم می‌شود گرفت (`…/paths/GO:0003674?relations=is_a`)؛ با هم چیده (شکل را ما از آن مسیرها کشیدیم):

<div dir="ltr">

```text
molecular_function
├── molecular transducer activity
│     └── signaling receptor activity ───────────────────────────┐
└── transcription regulator activity                             │
      └── DNA-binding transcription factor activity              │
            ├── DNA-binding TF activity, RNA polymerase II-specific ┤
            └── ligand-modulated transcription factor activity ──┤
                                                                 ▼
                                               nuclear receptor activity      (3 parents)
                                                 └── nuclear steroid receptor activity
                                                       └── nuclear glucocorticoid receptor activity
```

</div>

‏«nuclear receptor activity» **سه پدر** دارد: هم «گیرنده‌ی پیام» است، هم «عامل رونویسی RNA پلیمراز II» و هم «عامل رونویسی وابسته به لیگاند». این همان DAG است. پس اگر بپرسید «کدام ژن‌ها عامل رونویسی‌اند؟»، GR هم می‌آید، بی آن‌که کسی دستی چنین آنوتیشنی گذاشته باشد.

✍️ **در مرورگر:** ‏https://www.ebi.ac.uk/QuickGO/ (‏`P04150` را بجویید؛ دکمه‌ی فیلتر **Evidence** برای جدا کردن IEA) یا **AmiGO** (https://amigo.geneontology.org؛ ابزار رسمی کنسرسیوم GO).

> 📺 **فیلم:** *An introduction to QuickGo* (EMBL-EBI): https://www.youtube.com/watch?v=_QRgN0yLPn0 · *Exploring Gene Ontology (GO) annotations, tools and resources* (EMBL-EBI): https://www.youtube.com/watch?v=6Am2VMbyTm4
> 📄 **مرجع:** Ashburner M, et al. (2000). *Gene Ontology: tool for the unification of biology.* Nat Genet 25:25–29. https://doi.org/10.1038/75556 · Gene Ontology Consortium (2023). *The Gene Ontology knowledgebase in 2023.* Genetics 224(1):iyad031. https://doi.org/10.1093/genetics/iyad031 · Binns D, et al. (2009). *QuickGO.* Bioinformatics 25:3045–3046. https://doi.org/10.1093/bioinformatics/btp536 · کدهای شاهد: https://geneontology.org/docs/guide-go-evidence-codes/

---

## ۴. گام ۲: ‏KEGG

‏KEGG (کیوتو) مسیرهای سوخت‌وساز، پیام‌رسانی و بیماری را با **شماره‌های ثابت** نگه می‌دارد. هر ژن در هر گونه به یک **KO** (KEGG Orthology، گروه ارتولوگ) و از آن به مسیرها وصل است. مسیرهای انسان پیشوند `hsa` دارند و *E. coli* K-12 ‏`eco`.

### ۴.۱ هشت ژن در مسیرهای انسان

<div dir="ltr">

```bash
K=https://rest.kegg.jp
q=$(tail -n +2 dex8_ids.tsv | cut -f2 | sed 's/^/hsa:/' | paste -sd+)
echo "$q"
curl -sS "$K/link/pathway/$q" > dex_path.tsv
curl -sS "$K/list/pathway/hsa" > hsa_pathways.tsv
wc -l < hsa_pathways.tsv
awk -F'\t' 'NR == FNR {n["path:" $1] = $2; next} {print $1 "\t" $2 "\t" n[$2]}' hsa_pathways.tsv dex_path.tsv \
  | sed 's/ - Homo sapiens (human)//'
cut -f1 dex_path.tsv | sort -u | wc -l
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`hsa:2908` | شناسه‌ی ژن در KEGG = پیشوند گونه + **NCBI Gene ID** (برای انسان) |
| ‏`paste -sd+` | همه را با `+` به هم بچسبان؛ KEGG چند شناسه را در یک درخواست می‌پذیرد |
| ‏`link/pathway/…` | پیوند ژن‌ها به مسیرها |
| ‏`list/pathway/hsa` | همه‌ی مسیرهای انسان با نامشان |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
hsa:2908+hsa:2289+hsa:1831+hsa:7704+hsa:5187+hsa:1843+hsa:28999+hsa:83716
372
hsa:2908	path:hsa04080	Neuroactive ligand-receptor interaction
hsa:2289	path:hsa04915	Estrogen signaling pathway
hsa:7704	path:hsa05200	Pathways in cancer
hsa:7704	path:hsa05202	Transcriptional misregulation in cancer
hsa:7704	path:hsa05221	Acute myeloid leukemia
hsa:5187	path:hsa04710	Circadian rhythm
hsa:5187	path:hsa04713	Circadian entrainment
hsa:1843	path:hsa04010	MAPK signaling pathway
hsa:1843	path:hsa04726	Serotonergic synapse
hsa:1843	path:hsa05012	Parkinson disease
hsa:1843	path:hsa05418	Fluid shear stress and atherosclerosis
5
```

</div>

**توضیح خروجی:**
- ‏KEGG ‏۳۷۲ مسیر انسانی دارد، ولی **هیچ** مسیر «پیام‌رسانی گلوکوکورتیکوئید» ندارد. ‏NR3C1 تنها در «Neuroactive ligand-receptor interaction» است: فهرستی کلی از گیرنده‌ها، نه مسیر کار GR.
- تنها **۵** ژن از ۸ در هیچ مسیری هستند. **TSC22D3، KLF15 و CRISPLD2** در هیچ مسیر KEGG نیستند. در یک تحلیل غنی‌سازی (بخش ۱۴)، این سه ژن **نادیده** گرفته می‌شوند.
- ‏FKBP5 در «Estrogen signaling»: چون همه‌ی گیرنده‌های استروئیدی Hsp90 و FKBPها را به کار می‌برند و KEGG آن را تنها در این مسیر کشیده است.
- ‏PER1 در «Circadian rhythm». ✅

### ‏۴.۲ ‏KO و مسیر در باکتری

<div dir="ltr">

```bash
curl -sS "$K/link/ko/eco:b3987"
curl -sS "$K/link/pathway/eco:b3987"
curl -sS "$K/link/eco/path:eco03020" | cut -f2 | paste -sd+ | xargs -I{} curl -sS "$K/list/{}"
curl -sS "$K/link/genes/ko:K03043" | cut -f2 | cut -d: -f1 | sort -u | wc -l
```

</div>

**تکه‌به‌تکه:** شناسه‌ی ژن *E. coli* در KEGG همان locus tag است (`b3987`، 12/01). ‏`xargs -I{}` فهرست ساخته‌شده را جای `{}` در دستور بعدی می‌گذارد. ‏`cut -d: -f1` از `eco:b3987` تنها پیشوند گونه را نگه می‌دارد.

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
eco:b3987	ko:K03043
eco:b3987	path:eco03020
eco:b3295	rpoA; RNA polymerase subunit alpha
eco:b3649	rpoZ; RNA polymerase subunit omega
eco:b3987	rpoB; RNA polymerase subunit beta
eco:b3988	rpoC; RNA polymerase subunit beta'
9972
```

</div>

- ‏rpoB در KO ‏**K03043** و مسیر «RNA polymerase» (eco03020) است. آن مسیر چهار ژن دارد: **rpoA، rpoB، rpoC، rpoZ**، همان آنزیم هسته‌ای α₂ββ′ω. ✅
- ‏K03043 در **۹۹۷۲** گونه‌ی KEGG هست: کمابیش هر باکتری. ‏KO همان «ارتولوگ» 12/01 و 12/04 است، این‌بار در سطح همه‌ی ژنوم‌ها.

**یادداشت پروانه:** ‏KEGG REST برای کار دانشگاهی آزاد است؛ کار تجاری و دانلود کامل پروانه می‌خواهد (https://www.kegg.jp/kegg/legal.html).

> 📺 **فیلم:** *Exploring Pathway Database KEGG!* (INSILICO SCHOLAR): https://www.youtube.com/watch?v=Iq1c_0o9koI
> 📄 **مرجع:** Kanehisa M, et al. (2025). *KEGG: biological systems database as a model of the real world.* Nucleic Acids Res 53(D1):D672–D677. https://doi.org/10.1093/nar/gkae909 · راهنمای REST: https://www.kegg.jp/kegg/rest/keggapi.html

---

## ۵. گام ۳: ‏Reactome

‏Reactome مسیرها را به شکل **واکنش‌های** دقیق، با شاهد مقاله برای هر گام، و سلسله‌مراتبی (از «بیان ژن» تا یک واکنش) می‌سازد. داده‌اش باز است و API آن بی کلید کار می‌کند.

### ۵.۱ مسیرهای GR

<div dir="ltr">

```bash
R=https://reactome.org/ContentService
curl -sS "$R/data/database/version"; echo
curl -sS "$R/data/mapping/UniProt/P04150/pathways?species=9606" | jq -r '.[] | "\(.stId)\t\(.displayName)"'
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
97
R-HSA-3371497	HSP90 chaperone cycle for steroid hormone receptors (SHR) in the presence of ligand
R-HSA-383280	Nuclear Receptor transcription pathway
R-HSA-4090294	SUMOylation of intracellular receptors
R-HSA-8849473	PTK6 Expression
R-HSA-8939902	Regulation of RUNX2 expression and activity
R-HSA-9615017	FOXO-mediated transcription of oxidative stress, metabolic and neuronal genes
R-HSA-9679191	Potential therapeutics for SARS
R-HSA-9768777	Regulation of NPAS4 gene transcription
```

</div>

- ‏Reactome نسخه‌ی **97**. این‌ها **پایین‌ترین** مسیرهایی‌اند که GR در آن‌ها مستقیم آمده است (در 12/01، Ensembl ‏۲۸ پیوند Reactome داد، چون مسیرهای بالاتر را هم می‌شمرد).
- ‏**«HSP90 chaperone cycle for steroid hormone receptors»**: همان کار GR با Hsp90 و FKBP5. ✅
- ‏«Potential therapeutics for SARS»: دگزامتازون یکی از درمان‌های کووید-۱۹ شد؛ Reactome هدف دارو را در این مسیر گذاشته است.

### ۵.۲ تحلیل غنی‌سازی: هشت ژن با هم

**چرا؟** «آیا هشت ژن ما بیش از انتظار تصادفی در یک مسیر هستند؟». این **تحلیل بیش‌نمایی** (over-representation analysis، ORA) است و بخش ۱۴ آن را از پایه می‌سازد. این‌جا تنها یک نگاه:

<div dir="ltr">

```bash
A=https://reactome.org/AnalysisService
curl -sS -X POST -H "Content-Type: text/plain" --data-binary @dex8_symbols.txt \
  "$A/identifiers/projection?pageSize=8&page=1&sortBy=ENTITIES_PVALUE&order=ASC&resource=TOTAL" > ora.json
jq -r '"found pathways: \(.pathwaysFound)  not found: \(.identifiersNotFound)"' ora.json
jq -r '.pathways[] | [.stId, .name[0:55], "\(.entities.found)/\(.entities.total)", (.entities.pValue | tostring), (.entities.fdr | tostring)] | @tsv' ora.json
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`--data-binary @file` | محتوای فایل را دست‌نخورده (با خط‌های تازه) بفرست |
| ‏`identifiers/projection` | شناسه‌ها را به انسان «نگاشت» کن و ORA بزن |
| ‏`sortBy=ENTITIES_PVALUE&order=ASC` | از کمترین p-value |
| ‏`.entities.found/total` | چند «موجودیت» از ورودی در مسیر یافت شد / مسیر چند موجودیت دارد |
| ‏`fdr` | ‏p-value تصحیح‌شده برای آزمون‌های بسیار (بخش ۱۴) |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
found pathways: 57  not found: 0
R-HSA-383280	Nuclear Receptor transcription pathway	9/86	8.881784197001252E-16	5.062616992290714E-14
R-HSA-212436	Generic Transcription Pathway	12/1574	8.641491011651681E-8	0.0000024196174832624706
R-HSA-73857	RNA Polymerase II Transcription	12/1678	1.756863049484636E-7	0.0000033380397940208084
R-HSA-74160	Gene expression (Transcription)	12/1922	7.80396238853065E-7	0.00001092554734394291
R-HSA-9909396	Circadian clock	5/148	0.0000011287612000643321	0.000012416373200707653
R-HSA-9931510	Phosphorylated BMAL1:CLOCK (ARNTL:CLOCK) activates expr	3/32	0.000009888209006714277	0.00008899388106042849
R-HSA-9931521	The CRY:PER:kinase complex represses transactivation by	2/21	0.0003449792063955348	0.0027598336511642785
R-HSA-9022699	MECP2 regulates neuronal receptors and channels	2/32	0.0007942108595119235	0.0055594760165834645
```

</div>

نخستین مسیر p-value ‏8.9×10⁻¹⁶ دارد! ولی «۹ موجودیت» از ۸ ژن؟ ببینیم کدام‌ها:

<div dir="ltr">

```bash
T=$(jq -r '.summary.token' ora.json)
curl -sS "$A/token/$T/found/entities/R-HSA-383280?resource=TOTAL" | jq -c '.identifiers[] | {id, isoforms: .mapsTo[0].ids}'
```

</div>

<div dir="ltr">

```
{"id":"NR3C1","isoforms":["P04150-5","P04150-6","P04150-7","P04150-8","P04150-9","P04150-1","P04150-2","P04150-3","P04150-4"]}
```

</div>

**این مهم‌ترین نکته‌ی این گام است:** هر ۹ «موجودیت» از **یک ژن** آمده‌اند: NR3C1 در Reactome ‏۹ **ایزوفرم** پروتئینی دارد و هر کدام جدا شمرده شده است. ‏p-value شگفت‌انگیز ساخته‌ی شمارش است، نه زیست‌شناسی. ‏`token` شناسه‌ی همین تحلیل روی سرور Reactome است و مدتی می‌ماند (با آن نتیجه را در مرورگر هم باز می‌کنید: `https://reactome.org/PathwayBrowser/#/DTAB=AN&ANALYSIS=TOKEN`).
- مسیرهای **Circadian clock** (‏PER1 و KLF15؛ Reactome هر دو را هدف کمپلکس BMAL1:CLOCK می‌داند) زیست‌شناسی واقعی‌تری‌اند. ✅ پاسخ معلوم.
- در بخش ۱۴ می‌بینید ابزارهای ORA چگونه این را با شمردن **ژن** (نه ایزوفرم) و با **پس‌زمینه**‌ی درست درست می‌کنند. در تمرین ۵ همین تحلیل را بی NR3C1 می‌زنید.

> 📺 **فیلم:** *Reactome Pathway Browser 3.0 – Short introduction* (Reactome): https://www.youtube.com/watch?v=ogJn_pgEjHY · *Reactome's Analysis Tools* (Reactome Knowledgebase): https://www.youtube.com/watch?v=rxEpA-lJguE
> 📄 **مرجع:** Milacic M, et al. (2024). *The Reactome Pathway Knowledgebase 2024.* Nucleic Acids Res 52(D1):D672–D678. https://doi.org/10.1093/nar/gkad1025 · Fabregat A, et al. (2017). *Reactome pathway analysis: a high-performance in-memory approach.* BMC Bioinformatics 18:142. https://doi.org/10.1186/s12859-017-1559-2

---

## ۶. گام ۴: ‏WikiPathways

‏WikiPathways مسیرهایی است که پژوهشگران خودشان، مانند ویکی‌پدیا، می‌کشند و بازبینی می‌کنند. پس مسیرهای «تازه» و ویژه (یک دارو، یک بیماری) را زودتر دارد. فهرست همه‌ی مسیرها با ژن‌هایشان یک فایل JSON است:

<div dir="ltr">

```bash
curl -sS -o wp_xref.json "https://www.wikipathways.org/json/findPathwaysByXref.json"
jq '.pathwayInfo | length' wp_xref.json
jq -r '.pathwayInfo[] | select(.species == "Homo sapiens")
       | [.id, .name, (.ncbigene | split(", ") | map(ltrimstr("ncbigene:")) | join(","))] | @tsv' wp_xref.json > wp_hs.tsv
wc -l < wp_hs.tsv
tail -n +2 dex8_ids.tsv | while IFS=$'\t' read sym id; do
  n=$(awk -F'\t' -v g=$id '{k = split($3, a, ","); for (i = 1; i <= k; i++) if (a[i] == g) {print $1; break}}' wp_hs.tsv | wc -l)
  echo -e "$sym\t$n"
done
grep -i 'glucocorticoid' wp_hs.tsv | cut -f1,2
awk -F'\t' '$1 == "WP2880" {print $3}' wp_hs.tsv | tr ',' '\n' | grep -xFf <(tail -n +2 dex8_ids.tsv | cut -f2)
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`.ncbigene \| split(", ") \| map(ltrimstr("ncbigene:"))` | رشته‌ی `ncbigene:2908, ncbigene:…` را به فهرست عددها برگردان |
| ‏`while IFS=$'\t' read sym id` | هر سطر جدول را بخوان و دو ستونش را در دو متغیر بگذار |
| ‏`grep -xFf <(…)` | سطرهایی که **درست** (‏`-x`) با یکی از شناسه‌های فهرست یکی‌اند (‏`-f`، متن ساده ‏`-F`) |

**خروجی واقعی (2026-10-27؛ فایل ۱۲ مگابایت):**

<div dir="ltr">

```
2218
1131
NR3C1	16
FKBP5	4
TSC22D3	2
ZBTB16	7
PER1	7
DUSP1	5
KLF15	3
CRISPLD2	0
WP2880	Glucocorticoid receptor pathway
WP4523	Classical pathway of steroidogenesis with glucocorticoid and mineralocorticoid metabolism
WP5280	Glucocorticoid biosynthesis
WP5743	Glucocorticoid receptor activation leading to hepatic steatosis
2908
1831
```

</div>

**توضیح خروجی:**
- ‏۲۲۱۸ مسیر در همه‌ی گونه‌ها، ۱۱۳۱ برای انسان.
- پوشش بهتر از KEGG: هفت ژن از هشت دست‌کم در یک مسیرند (تنها CRISPLD2 در هیچ‌کدام). ‏NR3C1 در ۱۶ مسیر.
- ‏WikiPathways مسیر ویژه‌ی **«Glucocorticoid receptor pathway»** (WP2880) دارد، که KEGG نداشت. ولی از هشت ژن ما تنها **NR3C1 و TSC22D3** در آن‌اند؛ FKBP5، شناخته‌شده‌ترین هدف GR، نیست. هیچ مسیری کامل نیست.
- در میان ۱۶ مسیر NR3C1 یکی **«Albuterol and budesonide therapy for asthma»** (WP5503) است: درست همان داروهای آزمایش GSE52778 (آلبوترول و یک گلوکوکورتیکوئید).

> 📺 **فیلم:** برای WikiPathways فیلم رسمی وارسی‌شده‌ای نیافتیم؛ راهنمای سایت: https://www.wikipathways.org/help.html
> 📄 **مرجع:** Agrawal A, et al. (2024). *WikiPathways 2024: next generation pathway database.* Nucleic Acids Res 52(D1):D679–D689. https://doi.org/10.1093/nar/gkad960

---

## ۷. گام ۵: ‏MSigDB

‏**MSigDB** (مؤسسه‌ی Broad و UC San Diego) بزرگ‌ترین بایگانی **مجموعه‌ژن** است، در چند **مجموعه** (collection): **H** (Hallmark، ۵۰ مجموعه‌ی پالایش‌شده)، **C2** (مسیرها و آزمایش‌های منتشرشده، از جمله KEGG و Reactome)، **C5** (GO)، **C7** (ایمنی) و… . نسخه‌ی کنونی **2026.2.Hs**. یک مجموعه را با نامش، بی نام‌نویسی، به شکل JSON می‌گیرید:

<div dir="ltr">

```bash
M=https://www.gsea-msigdb.org/gsea/msigdb/human
curl -sS "$M/download_geneset.jsp?geneSetName=HALLMARK_TNFA_SIGNALING_VIA_NFKB&fileType=json" > tnfa.json
jq -r 'to_entries[0] | "\(.key)\t\(.value.systematicName)\tPMID \(.value.pmid)\t\(.value.geneSymbols | length) genes"' tnfa.json
jq -r 'to_entries[0].value.geneSymbols[]' tnfa.json | grep -xFf dex8_symbols.txt
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
HALLMARK_TNFA_SIGNALING_VIA_NFKB	M5890	PMID 26771021	200 genes
DUSP1
PER1
```

</div>

برای دیدن جای هشت ژن در **همه**‌ی ۵۰ مجموعه‌ی Hallmark، نام‌ها در `hallmark_names.txt` است. هر کدام را می‌گیریم (یک ثانیه درنگ) و هم‌پوشانی را می‌شماریم:

<div dir="ltr">

```bash
mkdir -p hall
for n in $(cat hallmark_names.txt); do
  curl -sS -o hall/$n.json "$M/download_geneset.jsp?geneSetName=$n&fileType=json"; sleep 1
done
for n in $(cat hallmark_names.txt); do
  jq -r --rawfile d dex8_symbols.txt 'to_entries[0] | "\(.key)\t\(.value.geneSymbols | length)\t\([.value.geneSymbols[] | select(IN(($d | split("\n"))[]))] | join(","))"' hall/$n.json
done | awk -F'\t' '$3 != ""' | sed 's/HALLMARK_//'
```

</div>

**تکه‌به‌تکه:** ‏`--rawfile d file` محتوای فایل را چون یک رشته در متغیر `$d` به jq می‌دهد؛ `IN(…)` می‌پرسد «آیا این نام در آن فهرست هست؟».

**خروجی واقعی (2026-10-27؛ ۵۰ دانلود در نزدیک به ۷۵ ثانیه):**

<div dir="ltr">

```
ANDROGEN_RESPONSE	101	FKBP5
ESTROGEN_RESPONSE_EARLY	200	FKBP5
ESTROGEN_RESPONSE_LATE	200	FKBP5
HEME_METABOLISM	200	NR3C1
HYPOXIA	200	DUSP1,NR3C1
KRAS_SIGNALING_DN	200	ZBTB16
P53_PATHWAY	200	ZBTB16
TNFA_SIGNALING_VIA_NFKB	200	DUSP1,PER1
UV_RESPONSE_DN	144	DUSP1,NR3C1
```

</div>

**توضیح خروجی:**
- **هیچ** مجموعه‌ی Hallmark «پاسخ به گلوکوکورتیکوئید» نیست. FKBP5 در پاسخ **آندروژن** و **استروژن** است: همه‌ی گیرنده‌های استروئیدی FKBP5 را روشن می‌کنند.
- ‏TSC22D3، KLF15 و CRISPLD2 در **هیچ** Hallmark نیستند.
- بیشتر مجموعه‌ها ۲۰۰ ژن دارند و هیچ‌کدام بیشتر نه؛ کوچک‌ترین ۳۲ ژن.

✍️ **جست‌وجو در MSigDB** (برای نمونه «dexamethasone» یا «glucocorticoid»، که مجموعه‌های C2 از آزمایش‌های منتشرشده را می‌یابد) و دانلود کامل مجموعه‌ها (فایل‌های GMT) **نام‌نویسی رایگان** با ایمیل می‌خواهد: https://www.gsea-msigdb.org/gsea/login.jsp. از سرور دوره، صفحه‌ی جست‌وجو تنها فرم ورود را برگرداند، و سرور دانلود (data.broadinstitute.org) پاسخ نداد.

> 📺 **فیلم:** فیلم رسمی وارسی‌شده‌ای برای MSigDB نیافتیم؛ راهنمای MSigDB: https://www.gsea-msigdb.org/gsea/msigdb/help.jsp
> 📄 **مرجع:** Liberzon A, et al. (2015). *The Molecular Signatures Database Hallmark Gene Set Collection.* Cell Syst 1:417–425. https://doi.org/10.1016/j.cels.2015.12.004

---

## ۸. سه اشتباه رایج

1. **شمردن آنوتیشن‌ها به جای خواندن آن‌ها.** ‏GR ‏۱۴۷ آنوتیشن دارد، ولی ویژه‌ترین اصطلاحش تنها IEA و TAS است؛ FKBP5 ‏۵۷ بار «protein binding» دارد (تمرین ۱). کد شاهد و ویژگی اصطلاح را ببینید، نه شمار.
2. **باور کورکورانه به p-value غنی‌سازی.** ‏p = 8.9×10⁻¹⁶ از ایزوفرم‌های **یک** ژن آمد. همیشه ببینید **کدام ژن‌ها** نتیجه را ساخته‌اند.
3. **فراموش کردن پوشش پایگاه.** سه ژن از هشت در KEGG در هیچ مسیری نیستند و هیچ منبعی همه‌ی هدف‌های GR را در یک مسیر ندارد. «در هیچ مسیری غنی نشد» گاهی یعنی «پایگاه این ژن‌ها را نمی‌شناسد». چند منبع را با هم ببینید.

---

## 📘 برای کنجکاوها

- ‏**GO-CAM:** ‏GO مدل‌های تازه‌ای دارد که چند آنوتیشن را با پیکان به هم وصل می‌کنند (مانند یک مسیر کوچک): https://geneontology.org/docs/gocam-overview/
- ‏**GO slim:** زیرمجموعه‌ی کوچکی از اصطلاح‌های کلی، برای خلاصه کردن هزاران ژن (فیلم QuickGO در منابع).
- **آنوتیشن باکتری:** ‏RpoB ‏*E. coli* ‏۵۴ آنوتیشن دارد و بیشترش آزمایشی است؛ ولی اصطلاح‌هایی چون «flagellum assembly» از ComplexPortal و با کد NAS آمده‌اند. احتمالاً چون کمپلکس RNA پلیمراز با یک فاکتور سیگمای ویژه (σ28 برای ژن‌های تاژک) آن فرایند را راه می‌اندازد و آنوتیشن کمپلکس به همه‌ی زیرواحدها رسیده است. ‏GO اصطلاحی برای «پاسخ به ریفامپیسین» برای RpoB ندارد: GO کار طبیعی پروتئین را می‌نویسد، نه اثر داروها (بخش ۱۵).

---

## جمع‌بندی

- ‏GO = سه شاخه (MF، BP، CC) در یک DAG؛ هر آنوتیشن یک کد شاهد دارد (IDA/IPI آزمایشی … IEA خودکار).
- ‏KEGG: ژن ← KO ← مسیر؛ برای GR مسیر ویژه ندارد و ۳ ژن از ۸ را در هیچ مسیری ندارد. ‏rpoB: ‏K03043، مسیر RNA polymerase با چهار زیرواحد.
- ‏Reactome: مسیرهای واکنشی با API باز؛ تحلیل غنی‌سازی آن ۹ ایزوفرم NR3C1 را ۹ بار شمرد.
- ‏WikiPathways: مسیرهای جامعه‌محور، از جمله «Glucocorticoid receptor pathway»؛ پوشش بهتر ولی ناقص.
- ‏MSigDB: مجموعه‌ژن‌ها برای غنی‌سازی؛ Hallmark ‏۵۰ مجموعه و بی مجموعه‌ی گلوکوکورتیکوئید.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
Q=https://www.ebi.ac.uk/QuickGO/services
curl -sS -H "Accept: application/json" "$Q/annotation/search?geneProductId=UNIPROT&limit=200"   # GO annotations
curl -sS -H "Accept: application/json" "$Q/ontology/go/terms/GO:a,GO:b"                          # term names
curl -sS -H "Accept: application/json" "$Q/ontology/go/terms/GO:x/ancestors?relations=is_a"      # parents
K=https://rest.kegg.jp
curl -sS "$K/link/pathway/hsa:ID+hsa:ID"           # genes -> pathways (hsa: + NCBI Gene ID)
curl -sS "$K/list/pathway/hsa"                     # pathway names
curl -sS "$K/link/ko/eco:b3987"                    # gene -> KO
R=https://reactome.org/ContentService
curl -sS "$R/data/mapping/UniProt/ACC/pathways?species=9606"
curl -sS -X POST -H "Content-Type: text/plain" --data-binary @genes.txt "https://reactome.org/AnalysisService/identifiers/projection"
curl -sS "https://www.wikipathways.org/json/findPathwaysByXref.json"                           # all pathways + genes
curl -sS "https://www.gsea-msigdb.org/gsea/msigdb/human/download_geneset.jsp?geneSetName=NAME&fileType=json"
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏Gene Ontology (GO) | واژه‌نامه‌ی کنترل‌شده‌ی کارکرد ژن‌ها |
| ‏MF / BP / CC | کارکرد مولکولی / فرایند زیستی / جای سلولی |
| ‏DAG | گرافی که هر گره می‌تواند چند پدر داشته باشد و چرخه ندارد |
| آنوتیشن GO | جفت «ژن + اصطلاح GO» با یک کد شاهد و یک منبع |
| کد شاهد | نشان این‌که آنوتیشن از آزمایش، استنباط یا رایانه آمده است |
| ‏KO | گروه ارتولوگ KEGG (مانند K03043 برای rpoB) |
| مسیر (pathway) | نقشه‌ی پیکان‌دار برهم‌کنش‌ها و واکنش‌ها |
| مجموعه‌ژن (gene set) | فهرست ژن‌ها بی پیکان، برای غنی‌سازی |
| ‏Hallmark | ۵۰ مجموعه‌ژن پالایش‌شده‌ی MSigDB |
| تحلیل بیش‌نمایی (ORA) | آزمون این‌که فهرست شما بیش از انتظار در یک مجموعه است |
| ‏FDR | ‏p-value تصحیح‌شده برای آزمون‌های بسیار |
| ایزوفرم | گونه‌های پروتئینی یک ژن (از رونوشت‌ها یا AUGهای گوناگون، 12/01) |

---

## منابع

**مقاله و مستند**
- ‏Ashburner M, et al. (2000). *Gene Ontology: tool for the unification of biology.* Nat Genet 25:25–29. https://doi.org/10.1038/75556
- ‏Gene Ontology Consortium (2023). *The Gene Ontology knowledgebase in 2023.* Genetics 224(1):iyad031. https://doi.org/10.1093/genetics/iyad031
- ‏Binns D, et al. (2009). *QuickGO: a web-based tool for Gene Ontology searching.* Bioinformatics 25:3045–3046. https://doi.org/10.1093/bioinformatics/btp536
- ‏Carbon S, et al. (2009). *AmiGO: online access to ontology and annotation data.* Bioinformatics 25:288–289. https://doi.org/10.1093/bioinformatics/btn615
- ‏Kanehisa M, et al. (2025). *KEGG: biological systems database as a model of the real world.* Nucleic Acids Res 53(D1):D672–D677. https://doi.org/10.1093/nar/gkae909
- ‏Milacic M, et al. (2024). *The Reactome Pathway Knowledgebase 2024.* Nucleic Acids Res 52(D1):D672–D678. https://doi.org/10.1093/nar/gkad1025
- ‏Fabregat A, et al. (2017). *Reactome pathway analysis: a high-performance in-memory approach.* BMC Bioinformatics 18:142. https://doi.org/10.1186/s12859-017-1559-2
- ‏Agrawal A, et al. (2024). *WikiPathways 2024: next generation pathway database.* Nucleic Acids Res 52(D1):D679–D689. https://doi.org/10.1093/nar/gkad960
- ‏Liberzon A, et al. (2015). *The Molecular Signatures Database Hallmark Gene Set Collection.* Cell Syst 1:417–425. https://doi.org/10.1016/j.cels.2015.12.004

**کتاب**
- ‏Pevsner J (2015). *Bioinformatics and Functional Genomics*, 3rd ed. Wiley-Blackwell. (فصل‌های کارکرد ژن، Gene Ontology و مسیرها)
- ‏Dessimoz C, Škunca N, eds. (2017). *The Gene Ontology Handbook.* Methods Mol Biol 1446. Humana Press. دسترسی آزاد: https://doi.org/10.1007/978-1-4939-3743-1

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Bioconductor for Genomic Data Science* (Johns Hopkins؛ مجموعه‌ژن‌ها و آنوتیشن در R): https://www.coursera.org/learn/bioconductor
- ‏edX: *Introduction to Genomic Data Science* (UC San Diego): https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science
- ‏YouTube: *An introduction to QuickGo* (EMBL-EBI): https://www.youtube.com/watch?v=_QRgN0yLPn0
- ‏YouTube: *How to use QuickGO and GO slims for your research* (EMBL-EBI): https://www.youtube.com/watch?v=Pa5Ll8WByr4
- ‏YouTube: *Reactome: Exploring biological pathways (demo)* (EMBL-EBI): https://www.youtube.com/watch?v=drYbmwAIhUM

<sub>همه‌ی دستورها در 2026-10-27 روی سرور دوره اجرا شدند (QuickGO، KEGG REST، Reactome 97، WikiPathways، MSigDB 2026.2.Hs). جست‌وجوی MSigDB و سرور GMT آن از سرور در دسترس نبود. DOIها با Crossref وارسی شدند؛ فیلم‌ها با noembed. برای WikiPathways و MSigDB فیلم رسمی وارسی‌شده‌ای نیافتیم.</sub>

</div>
