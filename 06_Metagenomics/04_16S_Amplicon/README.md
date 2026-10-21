<div dir="rtl">

# ماژول ۰۴: آمپلیکون 16S rRNA با QIIME 2

| | |
| :--- | :--- |
| **بخش** | `06_Metagenomics` |
| **پیش‌نیاز** | ماژول [کنترل کیفیت](../01_Read_QC_Trimming/) (FASTQ و کیفیت)؛ [تنوع و Bray–Curtis در vegan](../../04_R_Packages/03_Bioc_Examples/) |
| **زمان تقریبی** | ۶ ساعت (۲ درس × ۱٫۲۵ ساعت + ۳٫۵ ساعت تمرین) |
| **ابزار** | ‏QIIME 2 amplicon 2026.7 (q2-dada2، q2-feature-classifier با scikit-learn 1.7.1، q2-diversity)، vsearch، MAFFT، FastTree؛ محیط رسمی QIIME 2 (نصب: https://library.qiime2.org/quickstart/amplicon) |
| **داده** | آموزش رسمی QIIME 2 «Atacama soils»، زیرنمونه‌ی ۱٪ (EMP paired-end، V4، 2×151) + مرجع SILVA 138 برای ناحیه‌ی V4؛ کمابیش ۵۳ مگابایت با `download.sh` |
| **وضعیت** | ✅ قالب تازه (2026-10-21)؛ خروجی‌ها از اجرای 2026-10-14/15 |

> ⚠️ **تنها برای تمرین.** داده یک زیرنمونه‌ی ۱٪ است (میانه‌ی ۲۴۳ رید در هر نمونه پس از DADA2) و طبقه‌بند تنها تا سطح **جنس** و تنها برای ناحیه‌ی V4 آموزش دیده است. در پژوهش واقعی: داده‌ی کامل (ده‌ها هزار رید در هر نمونه)، مرجع کامل SILVA 138.2 / GTDB / Greengenes2 که با RESCRIPt برای پرایمرهای خودتان آماده شده، و کنترل منفی و mock community در همان ران.

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. فرق 16S و shotgun را در پرسش، تفکیک تاکسونومیک و محدودیت‌ها بگویید.
2. داده‌ی چندگانه‌ی EMP را وارد QIIME 2 کنید، نمونه‌ها را جدا کنید و درصد تخصیص بارکد را تفسیر کنید.
3. پارامترهای DADA2 (`trim-left`، `trunc-len`) را با کیفیت و طول آمپلیکون توجیه کنید و افت رید هر مرحله را بخوانید.
4. طبقه‌بند Naive Bayes سازگار با نسخه‌ی scikit-learn خودتان بسازید و نتیجه را با vsearch بسنجید.
5. تنوع آلفا و بتا را حساب کنید، با آزمون درست (Kruskal–Wallis، PERMANOVA، PERMDISP، مدل چندمتغیره) گزارش کنید و **درهم‌آمیختگی** را بشناسید.

## ترتیب مطالعه
1. ‏[01_lesson_qiime_dada2.md](01_lesson_qiime_dada2.md): از ریدها تا جدول ASV.
2. ‏[02_lesson_taxonomy_diversity.md](02_lesson_taxonomy_diversity.md): نام‌گذاری، تنوع و یک دام آماری.
3. ‏[03_exercises.md](03_exercises.md): تمرین‌ها؛ زیر عنوان هر تمرین راهنمایی آمده است.
4. ‏[04_solutions.md](04_solutions.md): پاسخ تشریحی.
5. اسکریپت‌ها: [99_scripts_data/04_16S_Amplicon](../99_scripts_data/04_16S_Amplicon/) (`data/download.sh`، `scripts/train_classifier.sh`، `scripts/run_16s.sh`، `scripts/check.sh`).

## ورودی و خروجی

<div dir="ltr">

```text
~/amplicon/
├── data/                      raw/{forward,reverse,barcodes}.fastq.gz, sample_metadata.tsv, db/ (SILVA V4)
├── demux.qza, demux.qzv       reads per sample
├── table.qza, rep-seqs.qza    ASV table and ASV sequences (DADA2)
├── denoising-stats.qza        read loss at each DADA2 step
├── taxonomy.qza, taxa-bar-plots.qzv
├── rooted-tree.qza            ASV tree
├── core-metrics-results/      alpha/beta diversity and tests
└── exports/                   the same results as TSV/FASTA for the exercises
```

</div>

</div>
