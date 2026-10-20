<div dir="rtl">

# ماژول ۰۴: فرمت‌های هم‌ترازی و واریانت: SAM/BAM و VCF

| | |
| :--- | :--- |
| **بخش** | `02_BioLinux` |
| **پیش‌نیاز** | ماژول [فرمت‌های آنوتیشن](../03_Annotation_Formats/) |
| **زمان تقریبی** | ۳ ساعت |
| **ابزار** | samtools 1.20، bcftools 1.21 |
| **وضعیت** | ✅ قالب تازه (2026-10-20) |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. ستون‌های SAM، به‌ویژه FLAG، MAPQ و CIGAR را بخوانید.
2. با samtools ریدها را بشمارید و گزینش کنید و پوشش را بسنجید.
3. ‏VCF را بخوانید و با bcftools گزینش کنید.
4. یک جهش مقاومت به ریفامپیسین (rpoB H526Y) را پیدا کنید و به کدونش برسید.

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس.
2. ‏[02_exercises.md](02_exercises.md): تمرین‌ها؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.

## داده
در پوشه‌ی [99_scripts_data/04_Align_Variant_Formats/data](../99_scripts_data/04_Align_Variant_Formats/data/): `resistant.bam` و `resistant.vcf.gz` (با ایندکس‌هایشان)، از یک «سویه‌ی مقاوم» شبیه‌سازی‌شده. چگونگی ساخت: [make_examples.sh](../99_scripts_data/04_Align_Variant_Formats/scripts/make_examples.sh).

</div>
