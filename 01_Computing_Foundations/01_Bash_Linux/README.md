# ماژول ۰۱: خط فرمان لینوکس (Bash Command Line)

| | |
| :--- | :--- |
| **بخش** | `01_Computing_Foundations` |
| **پیش‌نیاز** | ندارد |
| **زمان تقریبی** | ۶ ساعت (۳ ساعت درس + ۳ ساعت تمرین) |
| **ابزارها** | bash 5، GNU coreutils، grep، awk، sed |
| **داده** | ژنوم و GFF مرجع *E. coli* K-12 (`bash data/download.sh`، حدود ۳ MB)؛ برای تمرین‌های ۴ و ۵: FASTQهای بخش ۰۳ |
| **وضعیت** | ✅ تست‌شده — 2026-10-13 |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. در سیستم فایل لینوکس جابه‌جا شوید و فایل‌ها و مجوزها را مدیریت کنید.
2. فایل‌های بزرگ (و فشرده) را بدون باز کردن کامل بررسی کنید.
3. با pipe و `grep`، `cut`، `sort`، `uniq`، `awk` و `sed` فایل‌های FASTA، FASTQ و GFF را خلاصه و فیلتر کنید.
4. یک اسکریپت امن (`set -euo pipefail`) با حلقه و آرگومان بنویسید.
5. خطاهای بی‌صدای رایج را تشخیص دهید، مثل شمارش الگو در FASTA چندخطی.

## فایل‌ها
- [01_lesson.md](01_lesson.md) — متن درس
- [02_exercises.md](02_exercises.md) — تمرین‌ها
- [03_solutions.md](03_solutions.md) — پاسخ تشریحی
- [scripts/fasta_stats.sh](scripts/fasta_stats.sh) — پاسخ تمرین چالشی
- [data/download.sh](data/download.sh) — دانلود داده؛ `data/sample.fasta` فایل نمونه‌ی کوچک پروتئینی است
