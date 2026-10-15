# ماژول ۰۳: پروفایل تاکسونومیک و عملکردی (Taxonomic & Functional Profiling)

| | |
| :--- | :--- |
| **بخش** | `03_Metagenomics` |
| **پیش‌نیاز** | ماژول ۰۲ (ریدهای پاک از میزبان)؛ برای تحلیل‌های بعدی: بخش ۰۲ (Python/R) |
| **زمان تقریبی** | ۶ ساعت (۲٫۵ ساعت درس + ۳٫۵ ساعت تمرین) |
| **ابزارها (نسخه‌ی تست‌شده)** | Kraken2 2.17.1، Bracken 3.0.1؛ MetaPhlAn 4 و HUMAnN 3 فقط معرفی (اجرا نشده) |
| **داده** | `work/02_host/clean/` + `data/ground_truth_species.tsv` + **دیتابیس تمرینی** (حدود ۱۳۰ MB دانلود) |
| **وضعیت** | 🟢 بخش Kraken2/Bracken تست‌شده (2026-10-13)؛ بخش MetaPhlAn/HUMAnN معرفی و تست‌نشده |

> ⚠️ **دیتابیس این ماژول فقط برای تمرین است** (۴۵ ژنوم، ۲۶۳ MB). برای کار پژوهشی دیتابیس کامل لازم است، مثلاً Kraken2 Standard (79.6 GB) یا PlusPF (84.8 GB) از https://benlangmead.github.io/aws-indexes/k2. جزئیات در درس آمده است.

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. منطق طبقه‌بندی k-mer/LCA در Kraken2 و بازتوزیع Bracken را توضیح دهید و تفاوتش را با رویکرد ژن نشانگر (MetaPhlAn) بگویید.
2. پروفایل تاکسونومیک بسازید و **دقت آن را با ترکیب واقعی بسنجید** (precision، recall، Bray-Curtis).
3. اثر confidence، آستانه‌ی فراوانی و سطح تاکسونومیک را روی نتیجه آزمایش و انتخاب خود را توجیه کنید.
4. محدودیت‌های اساسی را تشخیص دهید: گونه‌ی غایب از دیتابیس، کمپلکس‌های گونه‌ای، و فراوانی رید در برابر سلول.

## فایل‌ها
- [01_lesson.md](01_lesson.md) — متن درس
- [02_exercises.md](02_exercises.md) — تمرین‌ها
- [03_solutions.md](03_solutions.md) — پاسخ تشریحی
- [practice_db_genomes.tsv](practice_db_genomes.tsv) — فهرست ۴۵ ژنوم دیتابیس تمرینی
- [scripts/build_practice_db.sh](scripts/build_practice_db.sh) — ساخت دیتابیس تمرینی (دانلود حدود ۱۳۰ MB؛ یک‌بار)
- [scripts/run_profile.sh](scripts/run_profile.sh) — Kraken2 + Bracken برای نمونه‌ها
- [scripts/evaluate_profile.py](scripts/evaluate_profile.py) — مقایسه با ground truth
- [scripts/check.sh](scripts/check.sh) — خودسنجی

## ورودی و خروجی
- **ورودی:** `work/02_host/clean/<sample>_R{1,2}.fastq.gz`
- **خروجی:** `work/03_profile/kraken/*.kreport`، `work/03_profile/bracken/*.bracken`. جدول‌های فراوانی برای تحلیل در R/Python (بخش ۰۲).
