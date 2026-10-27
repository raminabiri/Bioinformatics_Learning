<div dir="rtl">

# ماژول ۰۶: درگاه‌های بیان و سرطان (GTEx, HPA, Expression Atlas, GDC, cBioPortal) — نسخه‌ی ۲

| | |
| :--- | :--- |
| **بخش** | `12_V2_Global_Databases_Browsers` |
| **پیش‌نیاز** | ماژول‌های [11/04](../../11_V2_NCBI_Databases/04_GEO/) (GSE52778)، [11/05](../../11_V2_NCBI_Databases/05_Variation_Clinical/) (واریانت و dbGaP) و [12/01](../01_Ensembl_BioMart/) (نسخه‌ی شناسه‌ها)؛ `curl`، `jq`، `awk` |
| **زمان تقریبی** | ۳ ساعت (یک درس، نزدیک به ۹۰ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏GTEx API v2 (داده‌ی v11)، Human Protein Atlas 25.1، Expression Atlas، GDC API (Release 46.0)، cBioPortal API (v7.2.0)؛ OncoPrint و نمودار بقا (وب، ✍️) |
| **داده** | ‏NR3C1 و FKBP5 در بافت‌های سالم؛ بازتحلیل E-GEOD-52778؛ TP53 و KRAS در TCGA-LUAD و روده‌ی بزرگ (PanCancer Atlas) |
| **منابع رایانه** | تنها درخواست وب (بزرگ‌ترین فایل ۳ مگابایت) |
| **وضعیت** | ✅ اجرا شده (2026-10-27)؛ نمودارهای cBioPortal ✍️ |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. بیان یک ژن را در بافت‌های سالم از GTEx و HPA بگیرید و نسخه‌ی داده و شناسه را جور کنید.
2. بازتحلیل یک آزمایش GEO را از Expression Atlas بگیرید و با تحلیل خود بسنجید.
3. پروژه‌های TCGA را در GDC بشناسید و داده‌ی باز را از کنترل‌شده (dbGaP) جدا کنید.
4. جهش‌های یک ژن را در cBioPortal بشمارید و امضای جهشی را بخوانید.

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس؛ GTEx، HPA، Expression Atlas، GDC و TCGA، cBioPortal.
2. ‏[02_exercises.md](02_exercises.md): ۷ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** نام و شناسه‌ی ژن‌ها از 12/01؛ همه‌ی داده از API درگاه‌ها.
- **خروجی:** `nr3c1_gtex.json`، `e52778.tsv` (بازتحلیل؛ برای سنجش با DESeq2 در بخش ۱۳)، `tp53_luad.json`.

</div>
