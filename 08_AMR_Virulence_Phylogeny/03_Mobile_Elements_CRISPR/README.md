<div dir="rtl">

# ماژول ۰۳: عنصرهای ژنتیکی متحرک و CRISPR (Mobile Genetic Elements & CRISPR)

| | |
| :--- | :--- |
| **بخش** | `08_AMR_Virulence_Phylogeny` |
| **پیش‌نیاز** | ماژول‌های [۰۱](../01_AMR_Resistance_Genes/) و [۰۲](../02_Virulence_Factors/)؛ GFF/GenBank از بخش ۰۲ |
| **زمان تقریبی** | ۴ ساعت (۲ درس، نزدیک به ۱ ساعت و ۴۰ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏AMRFinderPlus 4.2.7، BLAST+ 2.17.0 با پایگاه PlasmidFinder، Python (`gene_context.py`، `find_crispr.py`) (اجرا شده)؛ MOB-suite، MobileElementFinder، CRISPRCasFinder و MinCED (از مستندات) |
| **داده** | پلاسمید **واقعی** pEK499 (EU935739.1، IncFII/FIA، از *E. coli* ‏ST131) روی کروموزوم K-12 = ایزوله‌ی `isoF`؛ کروموزوم K-12 برای CRISPR |
| **وضعیت** | ✅ اجرا شده (2026-10-24)، جز بخش‌های MOB-suite و ابزارهای عمومی CRISPR (✍️ از مستندات) |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. پلاسمید، IS، ترانسپوزون، اینتگرون و جزیره‌ی ژنومی را از هم جدا کنید.
2. پلاسمید را با پایگاه PlasmidFinder تایپ کنید (رپلیکون، گروه Inc).
3. ژن مقاومت را به IS یا اینتگرون کنارش نسبت دهید و ژن بریده به دست IS را بشناسید.
4. محدودیت اسمبلی short-read در بازسازی پلاسمید و کار MOB-suite را توضیح دهید.
5. سامانه‌ی CRISPR-Cas را در ژنوم پیدا کنید و spacerها را تفسیر کنید.

## ترتیب مطالعه
1. ‏[01_lesson_plasmids_is.md](01_lesson_plasmids_is.md): درس ۱، پلاسمید pEK499، رپلیکون، IS و اینتگرون.
2. ‏[02_lesson_crispr.md](02_lesson_crispr.md): درس ۲، CRISPR-Cas در K-12.
3. ‏[03_exercises.md](03_exercises.md): ۸ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
4. ‏[04_solutions.md](04_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** ‏pEK499 (FASTA و GenBank، با E-utilities)، `genomes/isoC.fna`، پایگاه PlasmidFinder.
- **خروجی:** ‏`isoF.amr.tsv`، `isoF.pf.tsv`، فهرست ژن–IS، `k12_spacers.fna`؛ ماژول ۰۴ پرسش «یک سویه یا یک پلاسمید؟» را با فیلوژنی پی می‌گیرد.

</div>
