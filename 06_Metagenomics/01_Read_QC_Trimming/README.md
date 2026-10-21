<div dir="rtl">

# ماژول ۰۱: کنترل کیفیت و بریدن ریدها

| | |
| :--- | :--- |
| **بخش** | `06_Metagenomics` |
| **پیش‌نیاز** | بخش‌های ۰۱ تا ۰۵؛ به‌ویژه [فرمت FASTQ](../../02_BioLinux/02_Sequence_Formats/)، [پایتون](../../03_Python/) و [Snakemake](../../05_Reproducible_Work/04_Snakemake_Pipeline/) |
| **زمان تقریبی** | ۴ ساعت (۲ درس × ۱ ساعت + ۲ ساعت تمرین) |
| **ابزار** | ‏FastQC 0.12.1، fastp 0.23.4، MultiQC 1.25.1؛ محیط [`envs/metagenomics.yml`](../../envs/metagenomics.yml) |
| **داده** | ریدهای بخش ۰۱ (`01_Linux/99_scripts_data/data/fastq`)، در پوشه‌ی پروژه‌ی `~/meta/raw` |
| **وضعیت** | ✅ قالب تازه (2026-10-21)؛ خروجی‌ها از اجرای 2026-10-12؛ ساختن محیط conda به‌صورت آنلاین هنوز آزموده نشده |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. گزارش FastQC را **برای داده‌ی متاژنوم** تفسیر کنید: کدام FAIL منتظره است و کدام مشکل.
2. خلاصه‌ی FastQC را از خط فرمان بخوانید و با MultiQC نمونه‌ها را کنار هم ببینید.
3. بریدن آداپتور، بریدن کیفیت و پالایش کیفیت را در fastp از هم جدا کنید و پارامتر را با سنجش روی داده‌ی خودتان برگزینید.
4. جفت ماندن R1 و R2 را بسنجید و عددهای گزارش JSON را با پایتون جدول کنید.

## ترتیب مطالعه
1. ‏[01_lesson_fastqc.md](01_lesson_fastqc.md): آیا ریدها سالم‌اند؟ FastQC و MultiQC.
2. ‏[02_lesson_trimming.md](02_lesson_trimming.md): بریدن و پالایش با fastp.
3. ‏[03_exercises.md](03_exercises.md): تمرین‌ها؛ زیر عنوان هر تمرین راهنمایی آمده است.
4. ‏[04_solutions.md](04_solutions.md): پاسخ تشریحی.
5. اسکریپت‌ها و گردش کار: [99_scripts_data/01_Read_QC_Trimming](../99_scripts_data/01_Read_QC_Trimming/) (`scripts/run_qc.sh`، `scripts/check.sh`، `workflow/Snakefile`).

## ورودی و خروجی

<div dir="ltr">

```text
~/meta/
├── raw/                 4 FASTQ files (input)
└── qc/
    ├── fastqc_raw/      FastQC of raw reads
    ├── multiqc_raw/     one report for all raw files
    ├── trimmed/         trimmed reads   <- input of module 02
    ├── fastp/           fastp JSON / HTML / log per sample
    ├── fastqc_trimmed/  FastQC after trimming
    └── multiqc_trimmed/ one report: FastQC + fastp
```

</div>

</div>
