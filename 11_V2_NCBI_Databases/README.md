<div dir="rtl">

# بخش ۱۱ (نسخه‌ی ۲): پایگاه‌های داده‌ی NCBI (NCBI Databases)

همه‌ی پایگاه‌های مهم NCBI، هم با مرورگر و هم با دستور. نسخه‌ی ۱ تنها Gene، Nucleotide، SRA، Datasets و PubChem را دید؛ این بخش بقیه را کامل می‌کند و برای هر پایگاه یک پرسش زیستی واقعی دارد.

| | |
| :--- | :--- |
| **پیش‌نیاز** | بخش‌های ۰۰، ۰۲ (ماژول ۰۵) و ۰۳ (ماژول ۰۵) |
| **داده‌ی مشترک (پیشنهادی)** | ژن *rpoB* از *E. coli* (رشته‌ی نسخه‌ی ۱)، ژن انسانی NR3C1، داده‌ی GEO ‏GSE52778، واریانت شناخته‌شده‌ی CFTR ‏(rs113993960) |
| **وضعیت** | ✅ نوشته و اجرا شده (2026-10-27)؛ نقشه‌ی کامل در [V2_ROADMAP.md](../V2_ROADMAP.md) |

| ماژول | عنوان | ابزار و پایگاه | وضعیت |
| :---: | :--- | :--- | :---: |
| ۰۱ | ‏[Entrez و E-utilities از خط فرمان](01_Entrez_EDirect/) | EDirect (`esearch`، `efetch`، `elink`، `esummary`، `xtract`)، Biopython Entrez، `curl` | ✅ |
| ۰۲ | ‏[Gene، RefSeq، Protein و Taxonomy](02_Gene_RefSeq_Protein_Taxonomy/) | NCBI Gene، RefSeq، Protein، Identical Protein Groups، Taxonomy، CDD | ✅ |
| ۰۳ | ‏[BioProject، BioSample و SRA Toolkit](03_BioProject_BioSample_SRA/) | BioProject، BioSample، SRA Run Selector، SRA Toolkit (`prefetch`، `fasterq-dump`) | ✅ |
| ۰۴ | ‏[GEO: داده‌ی بیان ژن](04_GEO/) | ‏GEO (GSE، GSM، GPL، GDS)، GEO2R، جدول شمارش آماده‌ی NCBI، GEOquery (اسکریپت آماده) | ✅ |
| ۰۵ | [واریانت و پایگاه‌های بالینی](05_Variation_Clinical/) | dbSNP، ClinVar، dbVar، MedGen، GTR، Variation Viewer | ✅ |
| ۰۶ | ‏[PubMed، PMC و کاوش متن](06_Literature_PubMed_PMC/) | PubMed، MeSH، PMC Open Access، PubTator3، EDirect | ✅ |
| ۰۷ | ‏[BLAST+ و ابزارهای وابسته](07_BLAST_Suite_Tools/) | BLAST+ (`blastn`، `blastp`، `tblastn`، `makeblastdb`، `-remote`)، ORFfinder، Primer-BLAST، CD-Search | ✅ |
| ۰۸ | ‏[Pathogen Detection و NCBI Virus](08_Pathogen_Virus_Resources/) | ‏NCBI Pathogen Detection، Isolates Browser، MicroBIGG-E، NCBI Virus، Datasets برای ویروس‌ها | ✅ |

</div>
