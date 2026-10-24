<div dir="rtl">

# ماژول ۰۲: عامل‌های بیماری‌زایی (Virulence Factors)

| | |
| :--- | :--- |
| **بخش** | `08_AMR_Virulence_Phylogeny` |
| **پیش‌نیاز** | ماژول [۰۱](../01_AMR_Resistance_Genes/)؛ BLAST وب (00/03)؛ اجرای اسکریپت R (بخش ۰۴) |
| **زمان تقریبی** | ۴ ساعت (۲ درس، نزدیک به ۱ ساعت و ۴۵ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏AMRFinderPlus 4.2.7 + stxtyper، BLAST+ 2.17.0، VFDB setA، R/ggplot2 (اجرا شده)؛ ABRicate و Kleborate (از مستندات) |
| **داده** | دو ژنوم شبیه‌سازی‌شده‌ی تازه: `isoD` (شبیه EHEC: ‏eae، stx2a، ehxA) و `isoE` (شبیه ExPEC: ‏papC، sat، cnf1، iutA + blaCTX-M-15)، ساخته با `99_scripts_data/02_Virulence_Factors/scripts/make_virulence_isolates.py`؛ و سه ژنوم ماژول ۰۱ |
| **وضعیت** | ✅ اجرا شده (2026-10-24)، جز بخش ABRicate/Kleborate درس ۲ (✍️ از مستندات) |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. عامل‌های بیماری‌زایی و پاتوتیپ‌های *E. coli* را با ژن‌های نشانگرشان بشناسید.
2. ‏AMRFinderPlus (`--plus`) و stxtyper را برای ژن‌های بیماری‌زایی به کار ببرید.
3. ‏VFDB را با `makeblastdb`/`blastn` بجویید و دام‌های BLAST را بشناسید.
4. امتیازهای Kleborate را برای *Klebsiella* تفسیر کنید.
5. نقشه‌ی حرارتی مقاومت و بیماری‌زایی بسازید و هم‌گرایی را تشخیص دهید.

## ترتیب مطالعه
1. ‏[01_lesson_virulence_amrfinder.md](01_lesson_virulence_amrfinder.md): درس ۱، مفهوم، پاتوتیپ‌ها، AMRFinderPlus و stxtyper.
2. ‏[02_lesson_vfdb_heatmap.md](02_lesson_vfdb_heatmap.md): درس ۲، VFDB با BLAST، ABRicate و Kleborate، نقشه‌ی حرارتی.
3. ‏[03_exercises.md](03_exercises.md): ۸ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
4. ‏[04_solutions.md](04_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** ‏`99_scripts_data/data/virulence_genes.fna` (اپرون stx2a از NCBI X07865.1 و شش ژن از پایگاه AMRFinderPlus)، ژنوم K-12 بخش ۰۱، و جدول‌های `iso?.amr.tsv` ماژول ۰۱.
- **خروجی:** ‏`isoD.amr.tsv`، `isoE.amr.tsv`، `iso?.vfdb.tsv`، `amr_vir_matrix.tsv` و `amr_vir_heatmap.png`؛ ماژول ۰۳ می‌پرسد این ژن‌ها روی کدام عنصر متحرک‌اند.

</div>
