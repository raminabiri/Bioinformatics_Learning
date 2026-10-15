# درس: دیتابیس‌های زیستی و دریافت داده

**بخش:** `00_Orientation` · **ماژول:** `02_Biological_Databases` · **پیش‌نیاز:** ماژول ۰۱ · **زمان:** ۲٫۵ ساعت · **ابزار:** `curl`، `jq`، NCBI Datasets CLI 18.38 · **آخرین تست:** 2026-10-12

---

## ۱. مسئله

هر تحلیل بیوانفورماتیک دست‌کم یک دیتابیس عمومی را مصرف می‌کند: ژنوم مرجع، دیتابیس تاکسونومی، دیتابیس ژن‌های مقاومت، ساختار پروتئین. سه مهارت لازم است:

1. **بدانید هر نوع داده کجا نگه‌داری می‌شود** و کدام منبع «اولیه» (داده‌ی خام ثبت‌شده توسط پژوهشگران) و کدام «ثانویه/curated» (پالایش‌شده و آنوتیت‌شده) است.
2. **شناسه‌ها را بخوانید.** از روی `GCF_000005845.2` یا `SRR390728` باید بفهمید با چه نوع رکوردی سروکار دارید.
3. **داده را تکرارپذیر دریافت کنید.** یعنی با خط فرمان یا API، با شناسه‌ی نسخه‌دار، نه با کلیک و کپی از مرورگر.

## ۲. نقشه‌ی دیتابیس‌ها

| دسته | دیتابیس | محتوا | اولیه/ثانویه |
| :--- | :--- | :--- | :--- |
| **توالی نوکلئوتیدی** | INSDC = GenBank (NCBI) + ENA (EMBL-EBI) + DDBJ | توالی‌های ثبت‌شده توسط پژوهشگران | اولیه |
| **ریدهای خام** | SRA (NCBI)، ENA، DRA | فایل‌های توالی‌یابی (FASTQ/BAM) + metadata | اولیه |
| **پروژه و نمونه** | BioProject، BioSample | توصیف مطالعه و هر نمونه‌ی زیستی | اولیه (metadata) |
| **مرجع curated** | RefSeq (NCBI)، Ensembl | ژنوم، ترنسکریپت و پروتئین غیرتکراری و آنوتیت‌شده | ثانویه |
| **پروتئین** | UniProtKB (Swiss-Prot / TrEMBL)، UniRef، UniParc | توالی و عملکرد پروتئین | ثانویه |
| **دومین و خانواده** | InterPro (شامل Pfam) | دومین‌ها و خانواده‌های پروتئینی | ثانویه |
| **ساختار** | wwPDB (RCSB PDB، PDBe، PDBj)، AlphaFold DB | ساختار تجربی؛ مدل‌های پیش‌بینی‌شده | اولیه (PDB) / محاسباتی (AFDB) |
| **عملکرد و مسیر** | KEGG، Gene Ontology، Reactome، MetaCyc، eggNOG | مسیرهای متابولیک، اصطلاحات عملکردی، ارتولوگ‌ها | ثانویه |
| **تاکسونومی** | NCBI Taxonomy، GTDB | رده‌بندی موجودات | ثانویه |
| **تخصصی (در این دوره)** | SILVA (rRNA)، CARD و AMRFinderPlus (مقاومت)، VFDB (ضراوت)، PubMLST (تایپینگ)، ZINC/ChEMBL/PubChem (ترکیبات) | — | ثانویه |
| **مقالات** | PubMed، Europe PMC | چکیده و متن کامل مقالات | — |

**INSDC** (International Nucleotide Sequence Database Collaboration) یعنی سه آرشیو NCBI، EMBL-EBI و DDBJ **هر روز داده‌هایشان را با هم همگام می‌کنند**. توالی‌ای که در ENA ثبت شده، در GenBank هم پیدا می‌شود؛ فقط پیشوند شناسه نشان می‌دهد کجا ثبت شده. در عمل برای دانلود ریدها **ENA** اغلب راحت‌تر است، چون فایل `fastq.gz` آماده و `md5` می‌دهد. SRA فایل را در فرمت خودش نگه می‌دارد و باید با SRA Toolkit تبدیل شود.

## ۳. خواندن شناسه‌ها (Accessions)

### ۳.۱ سلسله‌مراتب داده‌ی خام
```text
BioProject   PRJNA… / PRJEB… / PRJDB…   ← یک مطالعه
  └─ BioSample  SAMN… / SAMEA… / SAMD…   ← یک نمونه‌ی زیستی (یک فرد، یک ایزوله، یک نمونه‌ی خاک)
       └─ Experiment  SRX… / ERX… / DRX…  ← یک کتابخانه‌ی توالی‌یابی
            └─ Run   SRR… / ERR… / DRR…   ← یک اجرای دستگاه = فایل(های) FASTQ
(Study  SRP… / ERP… / DRP…  ← شناسه‌ی قدیمی‌تر مطالعه در SRA، معادل BioProject)
```
حرف دوم پیشوند نشان می‌دهد رکورد کجا ثبت شده: **N/S** = NCBI، **E** = EBI، **D** = DDBJ. مثال واقعی (بررسی‌شده با ENA API):

```text
run_accession  study_accession  secondary_study_accession  sample_accession  experiment_accession  library_strategy  instrument_model
SRR390728      PRJNA172563      SRP020237                  SAMN00630374      SRX079566             RNA-Seq           Illumina Genome Analyzer IIx
```

### ۳.۲ ژنوم‌ها و رکوردهای RefSeq
| پیشوند | معنی | مثال |
| :--- | :--- | :--- |
| `GCA_` | اسمبلی ثبت‌شده در INSDC (GenBank) | `GCA_000005845.2` |
| `GCF_` | نسخه‌ی RefSeq همان اسمبلی (با آنوتیشن یکدست NCBI) | `GCF_000005845.2` |
| `NC_` | مولکول ژنومی کامل RefSeq (کروموزوم، پلاسمید) | `NC_000913.3` |
| `NZ_` | توالی ژنومی RefSeq حاصل از پروژه‌ی WGS | `NZ_…` |
| `NM_` / `NR_` | mRNA / RNA غیرکدکننده‌ی curated | — |
| `NP_` / `YP_` | پروتئین curated | `NP_418414.1` (RpoB) |
| `XM_` / `XP_` | mRNA / پروتئین پیش‌بینی‌شده‌ی محاسباتی | — |
| `WP_` | پروتئین **غیرتکراری** پروکاریوتی؛ یک `WP_` برای همه‌ی ژنوم‌هایی که دقیقاً همان توالی را دارند | — |

**نسخه (`.2`، `.3`) بخشی از شناسه است.** `NC_000913.3` با `NC_000913.2` فرق دارد، چون توالی عوض شده است. در Methods همیشه شناسه‌ی **نسخه‌دار** بنویسید.

### ۳.۳ UniProt
- **Swiss-Prot (reviewed):** مدخل‌هایی که curator انسانی بازبینی کرده است. در نسخه‌ی 2026_03 (2026-09-02) **۵۷۵٬۷۴۸ مدخل** دارد.
- **TrEMBL (unreviewed):** آنوتیشن خودکار، با **۱۴۹٬۴۳۰٬۶۳۵ مدخل** در همان نسخه.
- عدد اول حدود ۲۶۰ برابر کوچک‌تر است. یعنی بیشتر پروتئین‌هایی که در تحلیل‌ها می‌بینید **آنوتیشن خودکار** دارند و ادعای عملکردی آن‌ها را باید با احتیاط پذیرفت.
- **UniRef100/90/50:** خوشه‌بندی توالی‌ها با شباهت ۱۰۰، ۹۰ و ۵۰ درصد، برای جستجوی سریع‌تر و غیرتکراری. HUMAnN (بخش ۰۳) از UniRef90 استفاده می‌کند.

### ۳.۴ ساختار: PDB در برابر AlphaFold DB
- **PDB:** ساختار **تجربی** (X-ray، cryo-EM، NMR). کیفیت را با **resolution** (هرچه کمتر بهتر) و R-free (برای X-ray) بسنجید.
- **AlphaFold DB:** **مدل پیش‌بینی‌شده**. اطمینان هر باقی‌مانده با **pLDDT** سنجیده می‌شود: بالای ۹۰ خیلی بالا، ۷۰ تا ۹۰ قابل اعتماد، ۵۰ تا ۷۰ کم، و زیر ۵۰ خیلی کم (معمولاً ناحیه‌ی بی‌نظم). برای موقعیت نسبی دومین‌ها باید **PAE** را هم دید.
- مدل AlphaFold جایگزین ساختار تجربی نیست. لیگاند، کوفاکتور، کمپلکس و تغییرات پس از ترجمه را معمولاً ندارد.

### ۳.۵ تاکسونومی: NCBI در برابر GTDB
- **NCBI Taxonomy** هر taxon را با یک **taxid** عددی مشخص می‌کند (مثلاً `511145` = *E. coli* K-12 MG1655). رده‌بندی تاریخی است و بر اساس منابع منتشرشده ساخته شده.
- **GTDB** رده‌بندی را از روی **فیلوژنی ژنوم‌ها** و با نرمال‌سازی رتبه‌ها می‌سازد. به همین دلیل برخی نام‌ها با NCBI فرق دارند و بعضی جنس‌ها با پسوندهایی مثل `_A` تقسیم شده‌اند.
- در متاژنومیکس (بخش ۰۳) حتماً بنویسید پروفایل با کدام تاکسونومی و کدام نسخه ساخته شده است، چون نتیجه‌ی دو سیستم مستقیماً قابل مقایسه نیست.

## ۴. روش‌های دسترسی

| روش | کِی | ابزار |
| :--- | :--- | :--- |
| وب | جستجوی اکتشافی، دیدن یک رکورد | سایت هر دیتابیس |
| ابزار خط فرمان رسمی | دانلود ژنوم، ژن، ریدها | `datasets` (NCBI)، EDirect (`esearch`/`efetch`)، SRA Toolkit (`prefetch`/`fasterq-dump`) |
| REST API | کوئری‌های برنامه‌نویسی‌شده، اتصال دیتابیس‌ها به هم | ENA Portal API، UniProt REST، RCSB Search/Data API، KEGG REST، AlphaFold API |
| FTP/HTTPS مستقیم | دانلود حجیم | ENA FTP، NCBI FTP |

قاعده‌ی کار در این دوره: **هر داده‌ای که در تحلیل استفاده می‌شود باید با یک اسکریپت دانلود شود**، مثل `data/download.sh` در هر بخش. آن اسکریپت باید شناسه‌ی نسخه‌دار و md5 را ثبت کند.

> **مجوزها:** بیشتر این دیتابیس‌ها برای استفاده‌ی آکادمیک آزادند، ولی شرایط یکسان نیست. مثلاً **KEGG**: API آن برای استفاده‌ی آکادمیک آزاد است، اما دانلود انبوه از FTP اشتراک می‌خواهد. قبل از ساختن ابزاری که دیتابیسی را بازتوزیع می‌کند، مجوزش را بخوانید.

## ۵. کار عملی: «سفر یک ژن»

ژن **rpoB** (زیرواحد β آنزیم RNA پلیمراز) را در *E. coli* K-12 MG1655 در هشت دیتابیس دنبال می‌کنیم. جهش در این ژن عامل اصلی **مقاومت به ریفامپیسین** است و در بخش ۰۵ دوباره به آن برمی‌گردیم.

```bash
conda activate bioinfo_course
cd 00_Orientation/02_Biological_Databases
bash scripts/gene_tour.sh          # پیش‌فرض: rpoB در taxid 511145
```

خروجی واقعی (2026-10-12):
```text
== 1. NCBI Taxonomy
taxid=511145  name=Escherichia coli str. K-12 substr. MG1655
== 2. NCBI Genome (reference assembly)
GCF_000005845.2  Complete Genome  length=4641652  GC=51%  genes=4651
== 3. NCBI Gene
GeneID=948488  symbol=rpoB  locus_tag=b3987  RNA polymerase subunit beta
== 4. UniProtKB (reviewed / Swiss-Prot)
Entry	Length	Protein names	EC number
P0A8V2	1342	DNA-directed RNA polymerase subunit beta (RNAP subunit beta) (EC 2.7.7.6) ...	2.7.7.6
== 5. KEGG (via UniProt cross-reference)
ENTRY       b3987             CDS       T00007
ORTHOLOGY   K03043  DNA-directed RNA polymerase subunit beta [EC:2.7.7.6]
PATHWAY     eco03020  RNA polymerase
== 6. AlphaFold DB
model=AF-P0A8V2-F1  mean_pLDDT=90.06
== 7. PDB (experimental structures that contain this UniProt sequence)
entries=391  first: 10MA, 10MB, 10MC, 10MD, 10ME
== 8. PubMed (literature)
PubMed hits for "rpoB AND rifampicin resistance": 1885
```

**تفسیر و نکته‌ها:**
- **پیوند بین دیتابیس‌ها از راه cross-reference است.** اسکریپت شناسه‌ی KEGG را از درون رکورد UniProt برمی‌دارد (`uniProtKBCrossReferences`). رکورد UniProt چند شناسه‌ی KEGG دارد (`eco:b3987` برای MG1655 و `ecj:JW3950` برای W3110)؛ ما فقط `eco:` را برداشتیم. **این یعنی همیشه دقیقاً بدانید کدام سویه را می‌خواهید.**
- **`K03043` یک ortholog در KEGG است** (KO). همین شناسه در بخش ۰۳ در پروفایل عملکردی متاژنوم ظاهر می‌شود: یعنی «ژنی با این عملکرد در جامعه هست»، فارغ از اینکه مال کدام باکتری است.
- **۳۹۱ ساختار PDB** برای یک پروتئین یعنی RNA پلیمراز *E. coli* از پرمطالعه‌ترین ماشین‌های مولکولی است. برای پروتئینی که هیچ ساختار تجربی ندارد، مدل AlphaFold (اینجا با میانگین pLDDT برابر ۹۰) نقطه‌ی شروع است.
- **اعداد متغیرند.** تعداد ساختارها و مقالات با زمان زیاد می‌شود. برای همین در تمرین‌ها و Methods «در تاریخ X» می‌نویسیم.

### دانلود تکرارپذیر یک ژنوم
```bash
datasets download genome accession GCF_000005845.2 --include genome,protein,gff3 --filename ecoli_k12.zip
unzip -o ecoli_k12.zip
find ncbi_dataset -type f
```
```text
ncbi_dataset/data/dataset_catalog.json
ncbi_dataset/data/assembly_data_report.jsonl
ncbi_dataset/data/GCF_000005845.2/protein.faa
ncbi_dataset/data/GCF_000005845.2/genomic.gff
ncbi_dataset/data/GCF_000005845.2/GCF_000005845.2_ASM584v2_genomic.fna
```

### پیدا کردن و دانلود ریدهای یک Run از ENA
```bash
curl -s "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=ERR688359&result=read_run&fields=run_accession,fastq_ftp,fastq_md5,fastq_bytes,read_count&format=tsv"
```
```text
run_accession	fastq_ftp	fastq_md5	fastq_bytes	read_count
ERR688359	ftp.sra.ebi.ac.uk/vol1/fastq/ERR688/ERR688359/ERR688359.fastq.gz	891ae71035f90e8fefe6699bbeb0f90a	103709762	1158189
```
با همین URL و `wget` فایل دانلود می‌شود و با `md5sum` سلامت آن چک می‌شود (تمرین ۳).

## ۶. دام‌ها (Pitfalls)

| دام | چرا مشکل است | راه درست |
| :--- | :--- | :--- |
| شناسه بدون نسخه (`NC_000913`) | توالی بین نسخه‌ها عوض می‌شود | همیشه `NC_000913.3` |
| مخلوط کردن GCA و GCF | آنوتیشن متفاوت؛ نام کروموزوم‌ها هم فرق دارد | یکی را انتخاب کنید و در کل پروژه ثابت نگه دارید |
| فرض «هر Run یک نمونه» | تعداد نمونه را کاذب بالا می‌برد | جدول Run↔Sample را از ENA بگیرید |
| اعتماد کامل به آنوتیشن TrEMBL یا «hypothetical protein» | آنوتیشن خودکار و گاهی منتقل‌شده‌ی اشتباه | شواهد (evidence) را ببینید؛ Swiss-Prot را ترجیح دهید |
| مقایسه‌ی نتایج NCBI Taxonomy با GTDB | نام‌ها و مرز taxonها فرق دارد | یک سیستم را انتخاب و نسخه‌اش را ثبت کنید |
| دانلود دستی از مرورگر | قابل تکرار نیست | اسکریپت + شناسه + md5 |

## ۷. جمع‌بندی
- INSDC (GenBank/ENA/DDBJ) و SRA/ENA آرشیوهای **اولیه**اند. RefSeq، UniProt، KEGG و GTDB منابع **ثانویه/curated** هستند.
- پیشوند و نسخه‌ی هر شناسه نوع و منشأ رکورد را می‌گوید. همیشه شناسه‌ی نسخه‌دار ثبت کنید.
- دیتابیس‌ها با cross-reference به هم وصل‌اند و با API می‌شود آن‌ها را برنامه‌نویسی‌شده و تکرارپذیر به هم زنجیر کرد.

## ۸. منابع

### مقالات مرجع دیتابیس‌ها (شماره‌ی سالانه‌ی Database در Nucleic Acids Research)
- Sayers EW, et al. (2025). Database resources of the National Center for Biotechnology Information in 2025. *Nucleic Acids Res.* https://doi.org/10.1093/nar/gkae979
- The UniProt Consortium (2025). UniProt: the Universal Protein Knowledgebase in 2025. *Nucleic Acids Res.* https://doi.org/10.1093/nar/gkae1010
- Yuan D, et al. (2024). The European Nucleotide Archive in 2023. *Nucleic Acids Res.* https://doi.org/10.1093/nar/gkad1067
- Katz K, et al. (2022). The Sequence Read Archive: a decade more of explosive growth. *Nucleic Acids Res.* https://doi.org/10.1093/nar/gkab1053
- INSDC (2025). The International Nucleotide Sequence Database Collaboration (INSDC): enhancing global participation. *Nucleic Acids Res.* https://doi.org/10.1093/nar/gkae1058
- Burley SK, et al. (2025). Updated resources for exploring experimentally-determined PDB structures and Computed Structure Models at the RCSB Protein Data Bank. *Nucleic Acids Res.* https://doi.org/10.1093/nar/gkae1091
- Varadi M, et al. (2024). AlphaFold Protein Structure Database in 2024. *Nucleic Acids Res.* https://doi.org/10.1093/nar/gkad1011
- Kanehisa M, et al. (2025). KEGG: biological systems database as a model of the real world. *Nucleic Acids Res.* https://doi.org/10.1093/nar/gkae909
- Parks DH, et al. (2022). GTDB: an ongoing census of bacterial and archaeal diversity. *Nucleic Acids Res.* https://doi.org/10.1093/nar/gkab776
- O'Leary NA, et al. (2024). Exploring and retrieving sequence and metadata for species across the tree of life with NCBI Datasets. *Scientific Data*. https://doi.org/10.1038/s41597-024-03571-y

### مستندات رسمی API و ابزارها
- NCBI Datasets: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/
- Entrez Direct (EDirect): https://www.ncbi.nlm.nih.gov/books/NBK179288/
- ENA Portal API: https://www.ebi.ac.uk/ena/portal/api/
- UniProt REST API: https://www.uniprot.org/help/api
- RCSB PDB Search API: https://search.rcsb.org/
- AlphaFold DB API: https://alphafold.ebi.ac.uk/api-docs
- KEGG REST API: https://www.kegg.jp/kegg/rest/keggapi.html

### ویدیوهای آموزشی
- EMBL-EBI — *European Nucleotide Archive: An Introduction*: https://www.youtube.com/watch?v=p2-mE45Ezyk
- EMBL-EBI — *Nucleotide sequencing data submission and retrieval at the ENA*: https://www.youtube.com/watch?v=1qvG9mtxSYo
- Nuala O'Leary (NCBI), Tree of Life — *Easy programmatic access to NCBI genome data with NCBI Datasets*: https://www.youtube.com/watch?v=Ru5MzGG_rcE
- EMBL-EBI — *A guide to UniProt for students and biological scientists*: https://www.youtube.com/watch?v=_VJVs2dcGPY
- EMBL-EBI — *EMBL-EBI, programmatically: UniProt*: https://www.youtube.com/watch?v=r7bq_HVO98Y
- EMBL-EBI — *Accessing and interpreting predicted protein structures from AlphaFold database*: https://www.youtube.com/watch?v=5k8Lm9w9mpY
- RCSB PDB — *Exploring PDB Structures in 3D with Mol\*: Introductory Guide*: https://www.youtube.com/watch?v=EdgmALgbJpM
- Bioinformagician — *How to download sequencing data from SRA NCBI*: https://www.youtube.com/watch?v=zE851fWCYQg

> همه‌ی لینک‌ها در تاریخ 2026-10-12 بررسی شدند: DOIها از طریق Crossref، ویدیوها از طریق YouTube oEmbed (در دسترس و عمومی) و صفحات مستندات با درخواست HTTP.
