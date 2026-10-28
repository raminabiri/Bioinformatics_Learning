<div dir="rtl">

# ماژول ۰۲: هم‌ترازی و شمارش (HISAT2, featureCounts, Salmon, kallisto) — نسخه‌ی ۲

| | |
| :--- | :--- |
| **بخش** | `13_V2_RNAseq_Transcriptomics` |
| **پیش‌نیاز** | ماژول [13/01](../01_Design_QC/) (داده‌ی `~/rnaseq`)؛ SAM/BAM و CIGAR ([02/04](../../02_BioLinux/04_Align_Variant_Formats/))؛ GTF ([02/03](../../02_BioLinux/03_Annotation_Formats/))؛ `Rscript` ([04](../../04_R_Packages/)) |
| **زمان تقریبی** | ۳ ساعت (یک درس، نزدیک به ۹۰ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏HISAT2 2.2.3، samtools 1.24، featureCounts 2.1.1، Salmon 2.8.0، kallisto 0.52.0، R 4.5.3 + tximport 1.38.2 (`envs/rnaseq.yml`)؛ STAR ✍️ |
| **داده** | مینی‌ژنوم و شش نمونه‌ی 13/01، با پاسخ معلوم (`truth_counts.tsv`) |
| **منابع رایانه** | هر گام کمتر از ۲ ثانیه و کمتر از ۲۲۰ مگابایت |
| **وضعیت** | ✅ اجرا شده (2026-10-28)؛ STAR از مستندات |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. ریدها را با HISAT2 روی ژنوم هم‌تراز کنید و ریدهای پیوندخورده و چندجایی را بخوانید.
2. با featureCounts جدول شمارش بسازید و رشته‌ویژگی را درست تنظیم کنید.
3. با Salmon و kallisto بشمارید و با tximport به سطح ژن برسید.
4. هر روش را با پاسخ معلوم بسنجید و محدودیت شمارش رونوشت را بشناسید.

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس؛ HISAT2، featureCounts و دام رشته، Salmon و برچسب گمراه‌کننده‌ی کتابخانه، tximport، رونوشت در برابر ژن، kallisto.
2. ‏[02_exercises.md](02_exercises.md): ۷ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** `~/rnaseq/ref` و `~/rnaseq/reads` (13/01)؛ اسکریپت‌های [`compare_counts.R`](../99_scripts_data/02_Alignment_Quantification/scripts/compare_counts.R) و [`isoform_share.py`](../99_scripts_data/02_Alignment_Quantification/scripts/isoform_share.py) (هر دو روی ویندوز هم اجرا می‌شوند).
- **خروجی:** `bam/`، `counts/fc_s2.txt`، `salmon_isr/`، و **`gene_counts_salmon.tsv`** (ورودی 13/03).

</div>
