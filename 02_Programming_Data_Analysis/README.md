# بخش ۰۲: برنامه‌نویسی و تحلیل داده (Programming & Data Analysis)

Python و R برای اتصال ابزارها، خواندن خروجی‌ها، آمار و رسم نمودار. در بخش‌های ۰۳ به بعد هر خروجی ابزار (جدول فراوانی، گزارش QC، جدول ژن‌های مقاومت) با همین مهارت‌ها تحلیل می‌شود.

| ماژول | عنوان | ابزارهای اصلی | وضعیت |
| :---: | :--- | :--- | :---: |
| 01 | [Python و Biopython](01_Python_Biopython/) | Python 3.13، Biopython 1.88 | ✅ تست‌شده |
| 02 | [پردازش جدول‌ها با pandas و NumPy](02_Pandas_NumPy/) | pandas، NumPy، matplotlib، seaborn | ⚪ طراحی‌شده |
| 03 | [R، Bioconductor و آمار](03_R_Bioconductor_Stats/) | R 4.x، tidyverse، ggplot2، phyloseq، vegan، DESeq2 | ⚪ طراحی‌شده |

## داده‌ی مشترک بخش
- ژنوم و پروتئین‌های *E. coli* K-12 (`GCF_000005845.2`) از بخش ۰۰.
- گزارش‌های JSON fastp و `ground_truth.tsv` از بخش ۰۳.
- در R: داده‌ی نمونه‌ی بسته‌های phyloseq/vegan و جدول‌های پروفایل بخش ۰۳.

## رشته‌ی مشترک دوره
تمرین‌ها روی همان داده‌های بخش ۰۰ و ۰۳ ساخته می‌شوند. مثلاً محاسبه‌ی GC و طول همه‌ی ژن‌ها از GFF، و مقایسه‌ی پروفایل Kraken2 با ground truth در pandas.
