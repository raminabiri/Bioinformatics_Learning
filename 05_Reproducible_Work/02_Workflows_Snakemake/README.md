<div dir="rtl">

# ماژول ۰۸: پایپلاین و مدیریت جریان کار (Workflows & Pipelines)

| | |
| :--- | :--- |
| **بخش** | `05_Reproducible_Work` |
| **پیش‌نیاز** | ماژول‌های ۰۱ تا ۰۷؛ داده‌ی بخش ۰۶ (`bash 06_Metagenomics/data/download.sh`) |
| **زمان تقریبی** | ۵ ساعت (۲ ساعت درس + ۳ ساعت تمرین) |
| **ابزارها** | Snakemake 9.25.2، fastp 0.23.4، FastQC 0.12.1، MultiQC 1.25.1، Bowtie2 2.5.4، samtools 1.20 |
| **وضعیت** | ✅ تست‌شده — 2026-10-14 |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. تفاوت اسکریپت خطی Bash و مدیر جریان کار را توضیح دهید و ابزار مناسب (Bash، Snakemake، Nextflow/nf-core) را انتخاب کنید.
2. یک Snakefile با wildcard، `config.yaml`، `params`، `threads` و `log` بنویسید.
3. با dry run پیش‌بینی کنید بعد از تغییر ورودی، پارامتر یا فایل میانی چه چیزی دوباره اجرا می‌شود.
4. ‏workflow را با rule‌های جدید گسترش دهید (جدول QC و حذف میزبان).

## فایل‌ها
- ‏[01_lesson.md](01_lesson.md) — متن درس
- ‏[02_exercises.md](02_exercises.md) — تمرین‌ها
- ‏[03_solutions.md](03_solutions.md) — پاسخ تشریحی
- ‏[workflow/Snakefile](../99_scripts_data/02_Workflows_Snakemake/workflow/Snakefile) و [workflow/config.yaml](../99_scripts_data/02_Workflows_Snakemake/workflow/config.yaml) — نسخه‌ی Snakemake پایپلاین QC بخش ۰۶
- ‏[workflow/Snakefile_solution](../99_scripts_data/02_Workflows_Snakemake/workflow/Snakefile_solution) — پاسخ تمرین‌های ۴ و ۵ (جدول QC + حذف میزبان)

</div>
