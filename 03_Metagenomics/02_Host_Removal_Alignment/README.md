# ماژول ۰۲: حذف DNA میزبان و مبانی همترازی (Host Removal & Read Alignment)

| | |
| :--- | :--- |
| **بخش** | `03_Metagenomics` |
| **پیش‌نیاز** | ماژول ۰۱ (ریدهای پیرایش‌شده)؛ فرمت SAM/BAM (01/03) |
| **زمان تقریبی** | ۵ ساعت (۲ ساعت درس + ۳ ساعت تمرین) |
| **ابزارها (نسخه‌ی تست‌شده)** | Bowtie2 2.5.4، samtools 1.20، wgsim 1.20 |
| **داده** | `work/01_qc/trimmed/` + `data/host/` (دانلود با `bash data/download.sh`) |
| **وضعیت** | ✅ تست‌شده — 2026-10-13 |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. دلیل علمی و اخلاقی حذف ریدهای میزبان را توضیح دهید.
2. ایندکس Bowtie2 بسازید، ریدهای PE را همتراز و خروجی SAM/BAM را با samtools بررسی کنید (FLAG، MAPQ، flagstat).
3. جفت‌هایی را نگه دارید که **هیچ mate‌شان** روی میزبان ننشسته است، و بدانید چرا `--un-conc` برای این کار نشت دارد.
4. حساسیت و ویژگی حذف میزبان را با یک آزمایش کنترل‌شده (ریدهای با منشأ معلوم) اندازه بگیرید.

## فایل‌ها
- [01_lesson.md](01_lesson.md) — متن درس
- [02_exercises.md](02_exercises.md) — تمرین‌ها
- [03_solutions.md](03_solutions.md) — پاسخ تشریحی
- [scripts/make_spiked_sample.sh](scripts/make_spiked_sample.sh) — ساخت نمونه‌ی کنترل (minigut + ریدهای انسانی شبیه‌سازی‌شده)
- [scripts/run_host_removal.sh](scripts/run_host_removal.sh) — حذف میزبان برای همه‌ی نمونه‌ها
- [scripts/check.sh](scripts/check.sh) — خودسنجی

## ورودی و خروجی
- **ورودی:** `work/01_qc/trimmed/<sample>_R{1,2}.fastq.gz`
- **خروجی** (ورودی ماژول ۰۳): `work/02_host/clean/<sample>_R{1,2}.fastq.gz`، و برای بررسی `work/02_host/bam/` و `work/02_host/logs/`

> فایل `_old_draft_lesson.md` پیش‌نویس قبلی است (ناقص و برای ژنوم انسانی). فقط برای مرجع نگه داشته شده است.
