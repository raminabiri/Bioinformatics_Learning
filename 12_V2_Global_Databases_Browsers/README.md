<div dir="rtl">

# بخش ۱۲ (نسخه‌ی ۲): پایگاه‌ها و مرورگرهای ژنومی جهانی (Global Databases and Genome Browsers)

پایگاه‌های بزرگ بیرون از NCBI و مرورگرهای ژنوم. نسخه‌ی ۱ هیچ مرورگر ژنومی (IGV، UCSC، Ensembl) آموزش نداد.

| | |
| :--- | :--- |
| **پیش‌نیاز** | بخش‌های ۰۰، ۰۲ و بخش ۱۱ |
| **داده‌ی مشترک (پیشنهادی)** | ناحیه‌ی *rpoB* با BAM و VCF نسخه‌ی ۱ (02/04 و 07/05)، ژن‌های انسانی پاسخ به گلوکوکورتیکوئید |
| **وضعیت** | ✅ همه‌ی شش ماژول نوشته و اجرا شدند (2026-10-27). نقشه‌ی کامل در [V2_ROADMAP.md](../V2_ROADMAP.md) |
| **محیط** | [`envs/databases.yml`](../envs/databases.yml) (liftOver، samtools، bcftools، igv-reports، HMMER)؛ بیشتر بخش وب و REST است |

| ماژول | عنوان | ابزار و پایگاه | وضعیت |
| :---: | :--- | :--- | :---: |
| ۰۱ | ‏[Ensembl و BioMart](01_Ensembl_BioMart/) | Ensembl، Ensembl Bacteria، BioMart، Ensembl REST | ✅ |
| ۰۲ | [مرورگر ژنوم UCSC](02_UCSC_Genome_Browser/) | UCSC Genome Browser، Table Browser، liftOver | ✅ |
| ۰۳ | [دیدن ریدها و واریانت‌ها با IGV](03_IGV_Visualization/) | ‏IGV (رومیزی)، igv.js، `samtools` | ✅ |
| ۰۴ | [خانواده و دامنه‌ی پروتئین](04_Protein_Families_Domains/) | ‏InterPro، InterProScan (وب)، Pfam، HMMER (`hmmscan`)، eggNOG-mapper | ✅ |
| ۰۵ | [هستی‌شناسی ژن و پایگاه‌های مسیر](05_Pathway_Ontology_Resources/) | QuickGO، AmiGO، KEGG، Reactome، WikiPathways، MSigDB | ✅ |
| ۰۶ | [درگاه‌های بیان و سرطان](06_Expression_Cancer_Portals/) | Expression Atlas، GTEx، Human Protein Atlas، GDC، cBioPortal | ✅ |

</div>
