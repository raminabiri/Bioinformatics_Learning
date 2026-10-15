# ماژول ۰۱: کنترل کیفیت و پیرایش ریدها (Read QC & Trimming)

| | |
| :--- | :--- |
| **بخش** | `03_Metagenomics` |
| **پیش‌نیاز** | 01_Bash_Linux، 02_Conda_Environments، 03_Bio_File_Formats (فرمت FASTQ) |
| **زمان تقریبی** | ۶ ساعت (۲ درس × ۱٫۵ ساعت + ۳ ساعت تمرین) |
| **ابزارها (نسخه‌ی تست‌شده)** | FastQC 0.12.1، fastp 0.23.4، MultiQC 1.25.1 |
| **داده** | `../data/raw/` (دانلود: `bash data/download.sh` از پوشه‌ی بخش) |
| **وضعیت** | ✅ تست‌شده — 2026-10-12 |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. گزارش FastQC را **برای داده‌ی متاژنومی** تفسیر کنید و بگویید کدام هشدارها انتظار می‌رود و کدام واقعاً مشکل‌اند.
2. با MultiQC گزارش چند نمونه و چند ابزار را تجمیع و مقایسه کنید.
3. تفاوت **فیلتر کیفیت**، **پیرایش کیفیت** (`cut_front`/`cut_tail`/`cut_right`) و **پیرایش آداپتور** را در fastp توضیح دهید و پارامتر مناسب را با داده توجیه کنید.
4. حفظ جفت‌بودن ریدها و سهم ریدهای باقی‌مانده را بسنجید.

## فایل‌ها
- [01_lesson_fastqc.md](01_lesson_fastqc.md) — ارزیابی کیفیت با FastQC و MultiQC
- [02_lesson_trimming.md](02_lesson_trimming.md) — پیرایش و فیلتر با fastp
- [03_exercises.md](03_exercises.md) — تمرین‌ها
- [04_solutions.md](04_solutions.md) — پاسخ تشریحی
- [scripts/run_qc.sh](scripts/run_qc.sh) — کل ماژول در یک اسکریپت (بعد از حل تمرین‌ها اجرا کنید)
- [scripts/check.sh](scripts/check.sh) — خودسنجی خروجی‌ها

## ورودی و خروجی
- **ورودی:** `data/raw/<sample>_R{1,2}.fastq.gz`
- **خروجی** (ورودی ماژول ۰۲): `work/01_qc/trimmed/<sample>_R{1,2}.fastq.gz`، به‌علاوه‌ی گزارش‌ها در `work/01_qc/`

```text
work/01_qc/
├── fastqc_raw/        گزارش FastQC ریدهای خام
├── multiqc_raw/       گزارش تجمیعی خام
├── trimmed/           ریدهای پیرایش‌شده   ← ورودی ماژول بعد
├── fastp_reports/     گزارش HTML/JSON و log هر نمونه
├── fastqc_trimmed/    گزارش FastQC بعد از پیرایش
└── multiqc_trimmed/   گزارش تجمیعی FastQC + fastp
```
