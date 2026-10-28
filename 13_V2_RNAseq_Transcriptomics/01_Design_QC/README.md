<div dir="rtl">

# ماژول ۰۱: طراحی آزمایش و کنترل کیفیت (RNA-seq Design and QC) — نسخه‌ی ۲

| | |
| :--- | :--- |
| **بخش** | `13_V2_RNAseq_Transcriptomics` |
| **پیش‌نیاز** | ‏FastQC ([06/01](../../06_Metagenomics/01_Read_QC_Trimming/))؛ GSE52778 ([11/04](../../11_V2_NCBI_Databases/04_GEO/))؛ Ensembl ([12/01](../../12_V2_Global_Databases_Browsers/01_Ensembl_BioMart/))؛ Conda ([02/01](../../02_BioLinux/01_Conda_Bioconda/)) |
| **زمان تقریبی** | ۳ ساعت (یک درس، نزدیک به ۸۰ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏FastQC 0.13.0، MultiQC 1.35، Python 3 (`envs/rnaseq.yml`) |
| **داده** | داده‌ی مشترک بخش ۱۳: مینی‌ژنوم ۲۰ ژن انسانی (Ensembl 116) و شش نمونه‌ی شبیه‌سازی‌شده (۳ شاهد، ۳ دگزامتازون) با پاسخ معلوم؛ ساخته با [`make_data.sh`](../99_scripts_data/shared/data/make_data.sh) |
| **منابع رایانه** | ساخت داده ۲ تا ۱۲ دقیقه (بسته به سرور Ensembl)، ۲۷ مگابایت؛ FastQC ‏۷ ثانیه و ۵۲۶ مگابایت |
| **وضعیت** | ✅ اجرا شده (2026-10-28) |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. تکرار زیستی و فنی را از هم جدا کنید و توان آماری را به شمار تکرار پیوند دهید.
2. گونه‌های کتابخانه (polyA، کاهش rRNA، رشته‌ویژه) را بشناسید.
3. اثر دسته و درهم‌آمیختگی را پیش از آزمایش ببینید و طرح جفتی بسازید.
4. ‏FastQC و MultiQC را روی RNA-seq بخوانید و FAILهای عادی را از نگران‌کننده جدا کنید.

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس؛ تکرار، کتابخانه، دسته، طرح GSE52778، ساختن داده‌ی بخش ۱۳، FastQC و MultiQC.
2. ‏[02_exercises.md](02_exercises.md): ۶ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** [`genes.tsv`](../99_scripts_data/shared/data/genes.tsv) (۲۰ ژن، CPM پایه و log2FC درست)؛ اسکریپت‌های [`make_mini_genome.py`](../99_scripts_data/shared/scripts/make_mini_genome.py) و [`simulate_reads.py`](../99_scripts_data/shared/scripts/simulate_reads.py).
- **خروجی:** `~/rnaseq/ref/` و `~/rnaseq/reads/` (ورودی همه‌ی ماژول‌های بخش ۱۳)، `~/rnaseq/qc/`.

</div>
