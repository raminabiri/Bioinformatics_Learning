<div dir="rtl">

# ماژول ۰۳: دیدن ریدها و واریانت‌ها با IGV (IGV, igv.js and samtools tview) — نسخه‌ی ۲

| | |
| :--- | :--- |
| **بخش** | `12_V2_Global_Databases_Browsers` |
| **پیش‌نیاز** | ‏BAM، VCF، samtools و bcftools ([02/04](../../02_BioLinux/04_Align_Variant_Formats/))؛ GFF ([02/03](../../02_BioLinux/03_Annotation_Formats/))؛ مرورگر ژنوم ([12/02](../02_UCSC_Genome_Browser/)) |
| **زمان تقریبی** | ۳ ساعت (یک درس، نزدیک به ۸۰ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏IGV رومیزی 2.19.8 (لپ‌تاپ هنرجو، ✍️)؛ samtools 1.24، bcftools 1.24، igv-reports 1.16.0 (`envs/databases.yml`) |
| **داده** | ‏`resistant.bam` و `resistant.vcf.gz` از 02/04 (سویه‌ی مقاوم شبیه‌سازی‌شده، ۴ واریانت معلوم، خطای ۰٫۲٪)؛ ژنوم و GFF ‏*E. coli* K-12 از بخش ۰۱ |
| **منابع رایانه** | چند ثانیه؛ igv-reports ‏۵۶ مگابایت حافظه |
| **وضعیت** | ✅ اجرا شده (2026-10-27)؛ IGV رومیزی و batch ✍️ |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. ژنوم، GFF، BAM و VCF را در IGV ببینید و نشانه‌هایش را بخوانید.
2. همان نما و شمارش‌ها را روی سرور با `samtools tview` و `mpileup` بگیرید.
3. یک SNP واقعی را از خطای توالی‌یابی و از ریدهای جابه‌جا (MAPQ پایین، ژن‌های تکراری) جدا کنید.
4. از واریانت‌ها گزارش HTML (igv-reports) یا تصویر تکرارپذیر (IGV batch) بسازید.

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس؛ IGV، `tview`، شمارش شواهد، MAPQ و tufA/tufB، حذف در VCF، igv-reports، batch.
2. ‏[02_exercises.md](02_exercises.md): ۷ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** داده‌ی 02/04 و بخش ۰۱ (پیوند نمادین، بی کپی)؛ اسکریپت batch ‏[`rpoB_snapshots.igv.txt`](../99_scripts_data/03_IGV_Visualization/scripts/rpoB_snapshots.igv.txt).
- **خروجی:** `report.html` (igv-reports)، `alts.tsv` (همه‌ی جایگاه‌های نابرابر)، و تصویرهای IGV (روی لپ‌تاپ).

</div>
