<div dir="rtl">

# ماژول ۰۱: اسمبلی و ارزیابی کیفیت ژنوم

| | |
| :--- | :--- |
| **بخش** | `07_Bacterial_Genomics` |
| **پیش‌نیاز** | بخش ۰۶، ماژول‌های [کنترل کیفیت](../../06_Metagenomics/01_Read_QC_Trimming/) و [Bowtie2/samtools](../../06_Metagenomics/02_Host_Removal_Alignment/)؛ [Biopython](../../03_Python/04_Biopython_Seq/) |
| **زمان تقریبی** | ۵ ساعت (۲ درس × ۱ ساعت + ۳ ساعت تمرین) |
| **ابزار** | اجراشده: Python 3 + Biopython (`repeat_report.py`)؛ از مستندات: SPAdes 4.x، Shovill 1.1، QUAST 5.x، CheckM2 1.1 |
| **داده** | ژنوم *E. coli* K-12 بخش ۰۱ (`01_Linux/99_scripts_data/data`)؛ تمرین‌های تفسیری روی داده‌ی **فرضی** |
| **وضعیت** | ✍️ نوشته‌شده (قالب تازه، 2026-10-21). محاسبه‌ی تکرارها اجراشده (2026-10-15)؛ اسمبلی، QUAST و CheckM2 اجرا نشده‌اند (STYLE_GUIDE، بخش ۵.۱) |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. اسمبلی de novo با گراف de Bruijn را توضیح دهید و بگویید چرا تکرارهای بلندتر از k و رید، اسمبلی را می‌شکنند.
2. سقف اسمبلی Illumina را برای یک ژنوم از روی تکرارهایش برآورد کنید.
3. یک ایزوله را با SPAdes (`--isolate`) یا Shovill اسمبل کنید و گزینه‌ها را توجیه کنید.
4. کیفیت اسمبلی را با N50/NG50، طول کل، GC، CheckM2 و پوشش هر کانتیگ بسنجید و دام‌های N50 را بشناسید.
5. اسمبلی آلوده، مخلوط، ناقص یا از گونه‌ی نادرست را تشخیص دهید و معیار پذیرش بنویسید.

## ترتیب مطالعه
1. ‏[01_lesson_assembly.md](01_lesson_assembly.md): اسمبلی ژنوم باکتری؛ چرا تکه‌تکه می‌شود؟
2. ‏[02_lesson_assembly_qc.md](02_lesson_assembly_qc.md): اسمبلی خوب است؟
3. ‏[03_exercises.md](03_exercises.md): تمرین‌ها؛ زیر عنوان هر تمرین راهنمایی آمده است.
4. ‏[04_solutions.md](04_solutions.md): پاسخ تشریحی.
5. اسکریپت: [99_scripts_data/01_Assembly_Quality/scripts/repeat_report.py](../99_scripts_data/01_Assembly_Quality/scripts/repeat_report.py) (k-merهای تکراری و سقف N50 یک ژنوم کامل؛ ۸ ثانیه روی *E. coli*).

## ورودی و خروجی
- **ورودی در کار واقعی:** ریدهای Illumina بریده‌شده‌ی هر ایزوله.
- **خروجی** (ورودی ماژول ۰۲، آنوتیشن): `contigs.fa` پالوده + جدول QUAST/CheckM2 + تصمیم پذیرش.

</div>
