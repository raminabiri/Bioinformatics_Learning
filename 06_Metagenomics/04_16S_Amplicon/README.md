# ماژول ۰۷: تحلیل آمپلیکون 16S rRNA (16S rRNA Amplicon Analysis)

| | |
| :--- | :--- |
| **بخش** | `06_Metagenomics` |
| **پیش‌نیاز** | 01_Read_QC_Trimming (FASTQ و کیفیت)؛ آمار پایه (آزمون ناپارامتری، p-value) |
| **زمان تقریبی** | ۸ ساعت (درس ۳ ساعت + تمرین ۵ ساعت) |
| **ابزارها (نسخه‌ی تست‌شده)** | QIIME 2 2026.7 (q2-dada2، q2-feature-classifier با scikit-learn 1.7.1، q2-diversity)، vsearch، MAFFT، FastTree |
| **داده** | آموزش رسمی QIIME 2 «Atacama soils»، زیرنمونه‌ی ۱٪ (EMP paired-end، V4، 2×151) + مرجع SILVA 138 برای ناحیه‌ی V4؛ حدود ۵۳ مگابایت: `bash 04_16S_Amplicon/data/download.sh` |
| **وضعیت** | ✅ تست‌شده — 2026-10-14 |

> ⚠️ **فقط برای تمرین.** داده یک زیرنمونه‌ی ۱٪ است (میانه‌ی ۲۴۳ رید در هر نمونه بعد از DADA2) و طبقه‌بند فقط تا سطح **جنس** و فقط برای ناحیه‌ی V4 آموزش دیده است. در پژوهش واقعی: داده‌ی کامل (ده‌ها هزار رید در نمونه)، مرجع کامل SILVA 138.2 / GTDB / Greengenes2 که با RESCRIPt برای ناحیه‌ی پرایمرهای خودتان آماده شده، و کنترل‌های منفی و mock community در همان ران.

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. تفاوت 16S و shotgun را در سؤال، تفکیک تاکسونومیک و محدودیت‌ها توضیح دهید.
2. داده‌ی چندگانه‌شده‌ی EMP را import و demultiplex کنید و نرخ تخصیص بارکد را تفسیر کنید.
3. پارامترهای DADA2 (`trim-left`، `trunc-len`) را با طول آمپلیکون و کیفیت توجیه کنید و افت رید در هر مرحله را بخوانید.
4. یک طبقه‌بند Naive Bayes سازگار با نسخه‌ی scikit-learn خودتان بسازید و نتیجه را با vsearch مقایسه کنید.
5. تنوع آلفا و بتا را محاسبه و با آزمون درست (Kruskal-Wallis، PERMANOVA، PERMDISP، مدل چندمتغیره) گزارش کنید و **مخدوش‌شدگی (confounding)** را تشخیص دهید.

## فایل‌ها
- [01_lesson.md](01_lesson.md): درس
- [02_exercises.md](02_exercises.md): تمرین‌ها
- [03_solutions.md](03_solutions.md): پاسخ تشریحی
- [data/download.sh](data/download.sh): دانلود داده و مرجع (با md5)
- [scripts/train_classifier.sh](scripts/train_classifier.sh): آموزش طبقه‌بند (یک بار)
- [scripts/run_16s.sh](scripts/run_16s.sh): کل ماژول در یک اسکریپت (بعد از حل تمرین‌ها اجرا کنید)
- [scripts/check.sh](scripts/check.sh): خودسنجی خروجی‌ها

## ورودی و خروجی
- **ورودی:** `04_16S_Amplicon/data/raw/{forward,reverse,barcodes}.fastq.gz` و `sample_metadata.tsv`
- **خروجی** (ورودی ماژول 02/03، تحلیل در R): `work/04_16s/`

```text
work/04_16s/
├── demux.qza, demux.qzv               ریدهای جداشده به تفکیک نمونه
├── table.qza, rep-seqs.qza            جدول ASV و توالی ASVها (DADA2)
├── denoising-stats.qza                افت رید در هر مرحله‌ی DADA2
├── taxonomy.qza, taxa-bar-plots.qzv   طبقه‌بندی و نمودار میله‌ای
├── rooted-tree.qza                    درخت فیلوژنی ASVها
├── core-metrics-results/              تنوع آلفا/بتا و آزمون‌ها
└── exports/                           همان نتایج به‌صورت TSV/FASTA برای تمرین‌ها
```

> نکته‌ی محیط: QIIME 2 محیط اختصاصی خودش را دارد. روی سرور دوره: `export PATH=/data/MicrobiomePipeline/qiime2_env/bin:$PATH`. نصب: https://library.qiime2.org/quickstart/amplicon
