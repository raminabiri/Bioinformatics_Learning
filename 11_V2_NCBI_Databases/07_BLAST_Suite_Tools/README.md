<div dir="rtl">

# ماژول ۰۷: BLAST+ و ابزارهای کنارش (BLAST suite, Primer-BLAST, ORF, CD-Search) — نسخه‌ی ۲

| | |
| :--- | :--- |
| **بخش** | `11_V2_NCBI_Databases` |
| **پیش‌نیاز** | ماژول‌های [00/03](../../00_Orientation/03_Web_Tools/)، [08/03](../../08_AMR_Virulence_Phylogeny/03_Mobile_Elements_CRISPR/)، [09/01](../../09_Structural_Bioinformatics/01_Protein_Structure/)، [11/01](../01_Entrez_EDirect/) و [11/02](../02_Gene_RefSeq_Protein_Taxonomy/) |
| **زمان تقریبی** | ۳٫۵ ساعت (یک درس، نزدیک به ۱۰۰ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏BLAST+ 2.17.0 (`makeblastdb`، `blastp`، `blastx`، `tblastn`، `blastn -task blastn-short`، `-remote`)، Biopython 1.87، CD-Search API؛ Primer-BLAST و ORFfinder (✍️ وب) |
| **داده** | ژنوم *E. coli* K-12 (`NC_000913.3`)، RpoB و GyrA سل (`NP_215181.1`، `NP_214520.1`)، پنج پروتئین 11/01. پاسخ معلوم: S450↔S531، H445↔H526، D435↔D516؛ A90↔S83، D94↔D87 |
| **منابع رایانه** | هر جست‌وجوی محلی زیر ۰٫۲ ثانیه و ۷۵ MB |
| **وضعیت** | ✅ اجرا شده (2026-10-27)، جز صفحه‌های وب Primer-BLAST و ORFfinder (✍️) |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. گونه‌ی BLAST درست را برای هر پرسش برگزینید.
2. ‏E-value، bit score، همانندی و پوشش را درست بخوانید.
3. شماره‌ی جایگاه‌ها را با یک هم‌ترازی از یک گونه به گونه‌ی دیگر ببرید.
4. برای یک ژن آغازگر PCR بسازید و ویژگی آن را بسنجید.
5. ‏ORF، دامنه‌های حفظ‌شده و BLAST راه دور را به کار ببرید.

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس؛ blastp، نگاشت جایگاه‌ها، tblastn، E-value، آغازگر، ORF، CD-Search، BLAST راه دور.
2. ‏[02_exercises.md](02_exercises.md): ۷ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** پروتئین‌ها و ژنوم از 11/01.
- **خروجی:** جدول نگاشت جایگاه‌ها، دو آغازگر سنجیده برای RRDR، جای دامنه‌های GR.
- **اسکریپت‌ها:** [map_positions.py](../99_scripts_data/07_BLAST_Suite_Tools/scripts/map_positions.py)، [six_frames.py](../99_scripts_data/07_BLAST_Suite_Tools/scripts/six_frames.py).

</div>
