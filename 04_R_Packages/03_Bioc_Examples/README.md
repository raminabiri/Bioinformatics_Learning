<div dir="rtl">

# ماژول ۰۳: سه نمونه‌ی واقعی؛ DESeq2، vegan و ggtree

| | |
| :--- | :--- |
| **بخش** | `04_R_Packages` |
| **پیش‌نیاز** | ماژول [اجرای Rscript](../02_Run_Rscript/) |
| **زمان تقریبی** | ۳ ساعت |
| **ابزار** | R 4.6.1، DESeq2 1.52.0، vegan 2.7.6، ape 5.8.1، ggtree 4.2.0؛ Python 3.13 + pandas |
| **داده** | شمارش RNA-seq **شبیه‌سازی‌شده** برای ژن‌های E. coli (با پاسخ معلوم)؛ `ground_truth.tsv` بخش ۰۱؛ داده‌ی woodmouse بسته‌ی ape |
| **وضعیت** | ✅ قالب تازه (2026-10-20) |

> این ماژول **اجرا و خواندن خروجی** بسته‌ها را یاد می‌دهد، نه آمار پشت آن‌ها را (دوره‌ی جداگانه‌ی آمار و R).

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. ‏DESeq2 را روی جدول شمارش اجرا کنید، `log2FoldChange` و `padj` را بخوانید و نتیجه را با پاسخ معلوم بسنجید.
2. تنوع آلفا و Bray–Curtis را با vegan حساب کنید و اثر سطح طبقه‌بندی را ببینید.
3. یک درخت Newick را بخوانید و با ggtree رسم کنید.

## ترتیب مطالعه
1. ‏[01_lesson_deseq2.md](01_lesson_deseq2.md): بیان افتراقی با DESeq2.
2. ‏[02_lesson_vegan.md](02_lesson_vegan.md): تنوع میکروبی با vegan.
3. ‏[03_lesson_ggtree.md](03_lesson_ggtree.md): رسم درخت با ggtree.
4. ‏[04_exercises.md](04_exercises.md): تمرین‌ها؛ زیر عنوان هر تمرین راهنمایی آمده است.
5. ‏[05_solutions.md](05_solutions.md): پاسخ تشریحی.
6. اسکریپت‌ها و نمودارها: [99_scripts_data/03_Bioc_Examples](../99_scripts_data/03_Bioc_Examples/).

</div>
