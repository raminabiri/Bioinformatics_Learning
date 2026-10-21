<div dir="rtl">

# ماژول ۰۲: آنوتیشن ژنوم؛ باکتری، فاژ و ویروس، یوکاریوت

| | |
| :--- | :--- |
| **بخش** | `07_Bacterial_Genomics` |
| **پیش‌نیاز** | ماژول [اسمبلی](../01_Assembly_Quality/)؛ [فرمت GFF](../../02_BioLinux/03_Annotation_Formats/)؛ [Biopython و GenBank](../../03_Python/05_Biopython_GenBank/) |
| **زمان تقریبی** | ۷ ساعت (سه درس کمابیش ۳٫۵ ساعت + ۳٫۵ ساعت تمرین) |
| **ابزار (اجراشده)** | ‏Pyrodigal 3.7.1، barrnap، ARAGORN 1.2.41، tRNAscan-SE 2.0.13؛ محیط [`envs/bacterial_genomics.yml`](../../envs/bacterial_genomics.yml) |
| **ابزار (از مستندات)** | Bakta 1.12.1، Prokka 1.15.6، Pharokka 1.10، Phold، geNomad، CheckV، VADR، RepeatModeler2/RepeatMasker، BRAKER4، Funannotate 1.9، BUSCO |
| **داده** | ‏*E. coli* K-12 بخش ۰۱؛ SARS-CoV-2 `NC_045512.2` و کروموزوم I مخمر `NC_001133.9` (اسکریپت‌ها با `curl` دانلود می‌کنند؛ کمتر از ۵۰۰ کیلوبایت) |
| **وضعیت** | ✍️ نوشته‌شده (قالب تازه، 2026-10-21). بخش‌های سبک اجراشده (2026-10-15) و خروجی‌ها واقعی‌اند؛ Bakta، Prokka و ابزارهای فاژ، ویروس و یوکاریوت اجرا نشده‌اند |

تأکید ماژول بر **باکتری** است (درس ۱). فاژ و ویروس (درس ۲) و یوکاریوت (درس ۳) نشان می‌دهند **چه چیزی فرق می‌کند** و چه ابزاری لازم است.

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. آنوتیشن ساختاری و کارکردی را از هم جدا کنید و خروجی GFF3/GenBank را بخوانید.
2. پیش‌بینی ژن را با مرجع بسنجید و خطاهای رایج را بشناسید: کدون آغاز، پروتئین کوچک، سلنوسیستئین، جابه‌جایی چارچوب، ژن کاذب.
3. ‏Bakta و Prokka را با گزینه‌های درست اجرا کنید و نسخه‌ی پایگاه را گزارش کنید.
4. پروفاژ را در ژنوم باکتری بیابید و تفسیر کنید، و ابزارهای فاژ (Pharokka، Phold، geNomad، CheckV) را بشناسید.
5. بگویید چرا ویروس‌های یوکاریوتی و ژنوم‌های یوکاریوتی ابزار ویژه می‌خواهند (VADR؛ BRAKER4، Funannotate، BUSCO).

## ترتیب مطالعه
1. ‏[01_lesson_prokaryote.md](01_lesson_prokaryote.md): باکتری و آرکی.
2. ‏[02_lesson_phage_virus.md](02_lesson_phage_virus.md): فاژ، پروفاژ و ویروس.
3. ‏[03_lesson_eukaryote.md](03_lesson_eukaryote.md): یوکاریوت (قارچ و مخمر).
4. ‏[05_exercises.md](05_exercises.md): تمرین‌ها؛ زیر عنوان هر تمرین راهنمایی آمده است.
5. ‏[06_solutions.md](06_solutions.md): پاسخ تشریحی.
6. اسکریپت‌ها: [99_scripts_data/02_Genome_Annotation/scripts](../99_scripts_data/02_Genome_Annotation/scripts/) (`light_annotation.sh`، `compare_genecalls.py`، `virus_demo.sh`، `yeast_demo.sh`).

## ورودی و خروجی
- **ورودی در کار واقعی:** `contigs.fa` پذیرفته‌شده از ماژول ۰۱.
- **خروجی** (ورودی ماژول‌های ۰۴ و ۰۵ و بخش ۰۸): GFF3، GenBank، FAA/FFN و جدول ویژگی‌ها برای هر ایزوله، با نسخه‌ی ابزار و پایگاه. اسکریپت‌های این ماژول خروجی را در `~/genomes/annotation/` می‌نویسند.

</div>
