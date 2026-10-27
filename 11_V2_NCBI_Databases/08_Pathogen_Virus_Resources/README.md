<div dir="rtl">

# ماژول ۰۸: Pathogen Detection، MicroBIGG-E و NCBI Virus (Pathogen and Virus Resources) — نسخه‌ی ۲

| | |
| :--- | :--- |
| **بخش** | `11_V2_NCBI_Databases` |
| **پیش‌نیاز** | ماژول [08/01](../../08_AMR_Virulence_Phylogeny/01_AMR_Resistance_Genes/) (AMRFinderPlus، blaCTX-M-15)؛ ماژول‌های [11/02](../02_Gene_RefSeq_Protein_Taxonomy/) (Datasets) و [11/07](../07_BLAST_Suite_Tools/) (gyrA S83/D87) |
| **زمان تقریبی** | ۳ ساعت (یک درس، نزدیک به ۹۰ دقیقه، تمرین‌ها و زمان دانلود) |
| **ابزار** | ‏curl 8.20.0، Python 3، NCBI Datasets CLI 18.38.0؛ Isolates Browser، MicroBIGG-E و NCBI Virus (✍️ وب) |
| **داده** | ‏Pathogen Detection *E. coli/Shigella* (`PDG000000004.6392`، ۵۹۱٬۸۱۰ ایزوله، ۵۵۳ MB)؛ CCHFV (۵۴۷۱ رکورد)؛ SARS-CoV-2 مرجع. پاسخ معلوم: NC_045512.2 = ‏۲۹٬۹۰۳ باز |
| **منابع رایانه** | ‏۵۵۳ MB دانلود (۲۶ دقیقه روی سرور دوره)؛ اسکریپت ۴ ثانیه و ۲۷۲ MB حافظه |
| **وضعیت** | ✅ اجرا شده (2026-10-27)، جز صفحه‌های وب (✍️) |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. خوشه‌های SNP در Pathogen Detection را بخوانید.
2. ژن‌های AMR صدها هزار ایزوله را از FTP جدول کنید؛ همان پرسش MicroBIGG-E.
3. ژنوم‌های ویروسی را با NCBI Datasets جدول کنید و بگیرید.
4. سوگیری نمونه‌گیری در داده‌ی عمومی را بشناسید.

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس؛ FTP Pathogen Detection، blaCTX-M-15، خوشه‌ها، NCBI Virus.
2. ‏[02_exercises.md](02_exercises.md): ۷ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** نام گروه بیماری‌زا و نام ژن؛ نام ویروس.
- **خروجی:** خلاصه‌ی جهانی یک ژن AMR (کشور، دهه، همراهان، خوشه‌ها)؛ جدول ژنوم‌های ویروس.
- **اسکریپت:** [amr_summary.py](../99_scripts_data/08_Pathogen_Virus_Resources/scripts/amr_summary.py).

</div>
