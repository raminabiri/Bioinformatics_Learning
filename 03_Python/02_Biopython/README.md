# ماژول 01: Python و Biopython (Python & Biopython)

| | |
| :--- | :--- |
| **بخش** | `03_Python` |
| **پیش‌نیاز** | 01_Computing_Foundations (Bash، فرمت‌ها) |
| **زمان تقریبی** | ۶ ساعت (درس ۳ ساعت + تمرین ۳ ساعت) |
| **ابزارها (نسخه‌ی تست‌شده)** | Python 3.13، Biopython 1.88 |
| **داده** | ژنوم و GFF *E. coli* K-12 (`NC_000913.3`) از ماژول 01/01: `bash ../../01_Linux/99_scripts_data/02_Bash/data/download.sh` |
| **وضعیت** | ✅ تست‌شده — 2026-10-14 |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. مختصات GFF (مبنای ۱، دوسر بسته) و Entrez (مبنای ۰) را درست به برش Python تبدیل کنید.
2. با `Bio.SeqIO` و `Bio.Seq` CDSها را استخراج، مکمل معکوس و با کد ۱۱ ترجمه کنید (`cds=True`).
3. ستون ۹ GFF3 را درست بخوانید (percent-encoding).
4. با `Bio.Entrez` از NCBI داده بگیرید (email، محدودیت نرخ، timeout).
5. یک اسکریپت خط فرمان با `argparse` بسازید که هم اجرا و هم import شود.
6. استثناهای زیستی (سلنوسیستئین، کدون آغاز ATT) را از باگ تشخیص دهید.

## فایل‌ها
- [01_lesson.md](01_lesson.md): درس
- [02_exercises.md](02_exercises.md): تمرین‌ها
- [03_solutions.md](03_solutions.md): پاسخ تشریحی
- [scripts/cds_table.py](../99_scripts_data/02_Biopython/scripts/cds_table.py): جدول همه‌ی CDSها (طول، GC، GC3، کیفیت ترجمه)
- [scripts/gc_outliers.py](../99_scripts_data/02_Biopython/scripts/gc_outliers.py): ژن‌های با GC غیرعادی (تمرین ۲)
- [scripts/codon_usage.py](../99_scripts_data/02_Biopython/scripts/codon_usage.py): فراوانی کدون، کل ژنوم یا زیرمجموعه (تمرین ۵)
- [scripts/entrez_tour.py](../99_scripts_data/02_Biopython/scripts/entrez_tour.py): نسخه‌ی Python بخشی از `gene_tour.sh` (تمرین ۴؛ اینترنت لازم است)

## ورودی و خروجی
- **ورودی:** `ecoli_k12.fna` و `ecoli_k12.gff`
- **خروجی** (ورودی ماژول 02/02، pandas): `cds_table.tsv` با ۴٬۳۰۰ CDS
