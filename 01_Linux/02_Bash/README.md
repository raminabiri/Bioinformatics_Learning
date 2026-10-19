<div dir="rtl">

# ماژول ۰۲: خط فرمان لینوکس (Bash)

| | |
| :--- | :--- |
| **بخش** | `01_Linux` |
| **برای چه کسی** | کسی که تا حالا با ترمینال کار نکرده است |
| **پیش‌نیاز** | ماژول [آماده‌سازی کامپیوتر](../01_Setup_Computer/) |
| **زمان تقریبی** | ۵ ساعت (۳ درس، روی هم نزدیک به ۲٫۵ ساعت + ۲٫۵ ساعت تمرین) |
| **ابزار** | bash 5، دستورهای پایه‌ی لینوکس (GNU coreutils)، grep، awk، sed |
| **داده** | ژنوم و GFF *E. coli* K-12، چهار فایل FASTQ کوچک و یک ناحیه از کروموزوم ۲۱ انسان؛ همه با `bash download.sh` در پوشه‌ی [99_scripts_data/02_Bash/data](../99_scripts_data/02_Bash/data/)، نزدیک به ۱۲ مگابایت، تنها با `curl` |
| **وضعیت** | ✅ بازنویسی در قالب تازه (2026-10-19) |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. در ترمینال میان پوشه‌ها جابه‌جا شوید و فایل‌ها را بسازید، کپی کنید و جابه‌جا کنید.
2. به فایل‌های بزرگ و فشرده نگاه کنید، بی‌آنکه بازشان کنید (`head`، `wc`، `less`، `zcat`).
3. با لوله (`|`) و `grep`، `cut`، `sort`، `uniq` و `awk` از فایل‌های GFF و FASTQ پرسش کنید.
4. با حلقه یک کار را روی چندین فایل تکرار کنید و یک اسکریپت ایمن (`set -euo pipefail`) بنویسید.

## ترتیب مطالعه
1. [01_lesson_files.md](01_lesson_files.md): ترمینال، پوشه‌ها و نگاه کردن به فایل‌ها.
2. [02_lesson_text_tools.md](02_lesson_text_tools.md): پرسیدن از فایل‌ها با grep، cut، sort، uniq و awk.
3. [03_lesson_scripts.md](03_lesson_scripts.md): متغیر، حلقه و اسکریپت.
4. [04_exercises.md](04_exercises.md): ۱۱ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
5. [05_solutions.md](05_solutions.md): پاسخ تشریحی.

## اسکریپت‌ها و داده
- [scripts/count_reads.sh](../99_scripts_data/02_Bash/scripts/count_reads.sh): شمار ریدها و میانگین طول در فایل‌های FASTQ (درس ۳).
- [scripts/fasta_stats.sh](../99_scripts_data/02_Bash/scripts/fasta_stats.sh): آمار یک فایل FASTA (پاسخ تمرین ۱۱).
- [data/download.sh](../99_scripts_data/02_Bash/data/download.sh): دانلود داده. `data/sample.fasta` یک فایل پروتئینی کوچک برای تمرین ۱۱ است.

</div>
