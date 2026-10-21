<div dir="rtl">

# ماژول ۰۳: نخستین گردش کار با Snakemake

| | |
| :--- | :--- |
| **بخش** | `05_Reproducible_Work` |
| **پیش‌نیاز** | ماژول [شاخه و GitHub](../02_Git_Branches_GitHub/)؛ بخش‌های [لینوکس](../../01_Linux/) و [پایتون](../../03_Python/) |
| **زمان تقریبی** | ۲٫۵ ساعت |
| **ابزار** | ‏Snakemake 9.25.2، seqkit 2.13.0؛ محیط `envs/workflow.yml` |
| **داده** | فایل‌های FASTQ بخش ۰۱ (`01_Linux/99_scripts_data/data/fastq`) |
| **وضعیت** | ✅ قالب تازه (2026-10-21)؛ ساختن محیط conda به‌صورت آنلاین هنوز آزموده نشده |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. یک Snakefile با قاعده‌های `input` / `output` / `shell` بنویسید.
2. با wildcard، `expand` و `rule all` یک قاعده را برای همه‌ی نمونه‌ها به کار ببرید.
3. با `snakemake -n` پیش‌بینی کنید چه چیزی، و چرا، اجرا می‌شود.
4. خطاهای رایج (آکولادهای awk، ورودی گمشده، دستور شکست‌خورده، فرورفتگی) را بشناسید.

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس.
2. ‏[02_exercises.md](02_exercises.md): تمرین‌ها؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.
4. ‏Snakefile کامل درس: [99_scripts_data/03_Snakemake_First/workflow](../99_scripts_data/03_Snakemake_First/workflow/).

</div>
