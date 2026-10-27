<div dir="rtl">

# ماژول ۰۱: ژن‌ها و جهش‌های مقاومت آنتی‌بیوتیکی (Antimicrobial Resistance)

| | |
| :--- | :--- |
| **بخش** | `08_AMR_Virulence_Phylogeny` |
| **پیش‌نیاز** | بخش [۰۷](../../07_Bacterial_Genomics/)؛ `cut`، `sort`، `uniq`، `awk` از بخش [۰۱](../../01_Linux/) |
| **زمان تقریبی** | ۴ ساعت (۲ درس، نزدیک به ۱ ساعت و ۴۵ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏AMRFinderPlus 4.2.7 (اجرا شده)؛ RGI/CARD و ABRicate 1.4.0 (از مستندات) |
| **داده** | سه ژنوم *E. coli* **شبیه‌سازی‌شده** با پاسخ معلوم (K-12 + ژن‌ها و جهش‌های افزوده)، ساخته با `99_scripts_data/01_AMR_Resistance_Genes/scripts/make_mock_isolates.py` |
| **مسیر ویندوز** | ‏✍️ [00_lesson_windows.md](00_lesson_windows.md) (پایتون و BLAST+ اجرا شده؛ ابزارهای وب از مستندات) |
| **وضعیت** | درس ۱ ✅ اجرا شده (2026-10-24؛ هر اجرا نزدیک به ۸۰ ثانیه، بیشینه‌ی حافظه ۱۸۳ مگابایت). درس ۲ ✍️ نوشته‌شده (RGI و ABRicate روی سرور نصب نیستند) |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. ژن ذاتی، ژن اکتسابی و جهش نقطه‌ای مقاومت را از هم جدا کنید.
2. ‏AMRFinderPlus را با `--organism` و `--plus` اجرا کنید و ستون‌های Scope، Subclass و Method را بخوانید.
3. ‏RGI (CARD) و ABRicate را اجرا کنید و بگویید چرا نتیجه‌ی ابزارها فرق دارد.
4. ژنوتیپ را با فنوتیپ بسنجید و یک گزارش کمینه بنویسید.

## ترتیب مطالعه
0. ‏[00_lesson_windows.md](00_lesson_windows.md): **مسیر ویندوز** (بی لینوکس): همان سه ژنوم با پایتون، BLAST+، ResFinder و CARD وب. اگر لینوکس دارید، از درس ۱ آغاز کنید.
1. ‏[01_lesson_amrfinder.md](01_lesson_amrfinder.md): درس ۱، AMRFinderPlus روی سه ژنوم با پاسخ معلوم.
2. ‏[02_lesson_card_abricate.md](02_lesson_card_abricate.md): درس ۲، CARD/RGI، ABRicate، اختلاف ابزارها، ژنوتیپ و فنوتیپ.
3. ‏[03_exercises.md](03_exercises.md): ۸ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
4. ‏[04_solutions.md](04_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** ژنوم K-12 بخش ۰۱ (`ecoli_k12.fna`، `ecoli_k12.gff`) و `99_scripts_data/data/acquired_genes.fna` (سه ژن از پایگاه AMRFinderPlus 2026-08-07.1).
- **خروجی:** ‏`iso?.amr.tsv` و `iso?.mut_all.tsv` در `~/amr`؛ ورودی ماژول ۰۲ (بیماری‌زایی) و ۰۳ (ژن مقاومت روی کدام contig است؟).

</div>
