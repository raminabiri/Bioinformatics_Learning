<div dir="rtl">

# ماژول ۰۱: ساختار سه‌بعدی پروتئین (Protein Structure: PDB, AlphaFold, PyMOL)

| | |
| :--- | :--- |
| **بخش** | `09_Structural_Bioinformatics` |
| **پیش‌نیاز** | پایتون (بخش ۰۳)؛ ماژول 08/01 (جایگاه‌های rpoB) |
| **زمان تقریبی** | ۴ ساعت (۲ درس، نزدیک به ۲ ساعت، و تمرین‌ها) |
| **ابزار** | ‏gemmi 0.7.5، PyMOL 3.1.0 (اجرا شده)؛ ColabFold، AlphaFold Server و SWISS-MODEL (از مستندات) |
| **داده** | ساختارهای تجربی RNA پلیمراز *E. coli* با ریفامپیسین: 5UAC (وحشی)، 5UAL (S531L)، 5UAH (D516V)؛ مدل AlphaFold ‏AF-P0A8V2-F1 (RpoB)؛ ‏1L2Y (NMR) |
| **وضعیت** | ✅ اجرا شده (2026-10-24)، جز ساختن مدل تازه با ColabFold/AlphaFold 3 (✍️، به GPU نیاز دارد) |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. روش‌های تعیین ساختار و معنای وضوح، B-factor و R-free را بگویید.
2. ساختار را از PDB بگیرید، با gemmi بخوانید و باقی‌مانده‌های جایگاه اتصال را پیدا کنید.
3. با یک اسکریپت PyMOL تصویری تکرارپذیر بسازید.
4. ‏pLDDT و PAE را تفسیر کنید و مدل AlphaFold را با ساختار تجربی (RMSD) بسنجید.
5. جهش‌های مقاومت rpoB (ماژول 08/01) را روی ساختار ببینید.

## ترتیب مطالعه
1. ‏[01_lesson_pdb.md](01_lesson_pdb.md): درس ۱، PDB، mmCIF، gemmi و PyMOL.
2. ‏[02_lesson_alphafold.md](02_lesson_alphafold.md): درس ۲، AlphaFold، pLDDT/PAE و RMSD.
3. ‏[03_exercises.md](03_exercises.md): ۷ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
4. ‏[04_solutions.md](04_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** فایل‌های mmCIF از RCSB؛ مدل AlphaFold از AlphaFold DB (یا `99_scripts_data/data/AF-P0A8V2-F1_from_RCSB-CSM.pdb.gz`).
- **خروجی:** فهرست باقی‌مانده‌های جایگاه، `rif_pocket.png`، جدول pLDDT و RMSD؛ ورودی ماژول ۰۳ (داکینگ در همین جایگاه).

</div>
