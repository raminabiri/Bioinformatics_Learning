# ماژول 02: آنوتیشن ژنوم: باکتری، فاژ و ویروس، یوکاریوت (Genome Annotation)

| | |
| :--- | :--- |
| **بخش** | `07_Bacterial_Genomics` |
| **پیش‌نیاز** | 01_Assembly_Quality؛ 02_Programming_Data_Analysis/01 (GFF و Biopython) |
| **زمان تقریبی** | ۸ ساعت (سه درس ۵ ساعت + تمرین ۳ ساعت) |
| **ابزارها (اجراشده)** | Pyrodigal 3.7.1، barrnap 1.10.5، ARAGORN 1.2.41، tRNAscan-SE 2.0.13 |
| **ابزارها (مستندات‌شده)** | Bakta 1.12.1 (DB v6.0)، Prokka 1.15.6، Pharokka 1.10، Phold، geNomad، CheckV، VADR، RepeatModeler2/RepeatMasker، BRAKER4، Funannotate 1.9، BUSCO |
| **داده** | *E. coli* K-12 (ماژول 01/01)؛ SARS-CoV-2 `NC_045512.2` و کروموزوم I مخمر `NC_001133.9` (اسکریپت‌ها دانلود می‌کنند، کمتر از ۵۰۰ کیلوبایت) |
| **وضعیت** | ✍️ نوشته‌شده — 2026-10-15. بخش‌های سبک اجرا و خروجی‌ها واقعی‌اند؛ Bakta، Prokka و ابزارهای فاژ، ویروس و یوکاریوت اجرا نشده‌اند (سیاست دوره) |

تأکید ماژول بر **باکتری** است (درس ۱، کامل). فاژ و ویروس (درس ۲) و یوکاریوت با تمرکز بر قارچ و مخمر (درس ۳) نشان می‌دهند **چه چیزی فرق می‌کند** و چه ابزاری لازم است.

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. آنوتیشن ساختاری و عملکردی را از هم جدا کنید و خروجی GFF3/GenBank را بخوانید.
2. پیش‌بینی ژن را با مرجع مقایسه کنید و خطاهای رایج را بشناسید: کدون آغاز، sORF، سلنوسیستئین، جابه‌جایی چارچوب، ژن کاذب.
3. Bakta و Prokka را با گزینه‌های درست اجرا کنید و نسخه‌ی دیتابیس را گزارش کنید.
4. پروفاژ را در ژنوم باکتری پیدا و تفسیر کنید (اینتگراز، tRNA مرزی، GC)، و فاژ را با Pharokka/Phold آنوتیت کنید.
5. توضیح دهید چرا ویروس‌های یوکاریوتی (پلی‌پروتئین، frameshift) آنوتیشن بر اساس مرجع (VADR) می‌خواهند.
6. مسیر آنوتیشن یوکاریوت (ماسک تکرار، شواهد، BRAKER4 یا Funannotate، BUSCO) را طراحی کنید.

## فایل‌ها
- [01_lesson_prokaryote.md](01_lesson_prokaryote.md): باکتری و آرکی
- [02_lesson_phage_virus.md](02_lesson_phage_virus.md): فاژ، پروفاژ و ویروس
- [03_lesson_eukaryote.md](03_lesson_eukaryote.md): یوکاریوت (قارچ و مخمر)
- [04_exercises.md](04_exercises.md): تمرین‌ها
- [05_solutions.md](05_solutions.md): پاسخ تشریحی
- [scripts/light_annotation.sh](scripts/light_annotation.sh): Pyrodigal، barrnap، ARAGORN، tRNAscan-SE روی *E. coli* (۱۴ ثانیه)
- [scripts/compare_genecalls.py](scripts/compare_genecalls.py): مقایسه‌ی پیش‌بینی ژن با آنوتیشن مرجع
- [scripts/virus_demo.sh](scripts/virus_demo.sh): ابزار ORF روی SARS-CoV-2
- [scripts/yeast_demo.sh](scripts/yeast_demo.sh): ابزار باکتریایی روی کروموزوم I مخمر

## ورودی و خروجی
- **ورودی در کار واقعی:** `contigs.fa` پذیرفته‌شده از ماژول ۰۱
- **خروجی** (ورودی ماژول ۰۶ تا ۰۸ و بخش ۰۸): GFF3، GenBank، FAA/FFN و جدول ویژگی‌ها برای هر ایزوله، با نسخه‌ی ابزار و دیتابیس
