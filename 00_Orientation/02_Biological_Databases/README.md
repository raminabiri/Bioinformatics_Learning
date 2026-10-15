# ماژول ۰۲: دیتابیس‌های زیستی و دریافت داده (Biological Databases & Data Retrieval)

| | |
| :--- | :--- |
| **بخش** | `00_Orientation` |
| **پیش‌نیاز** | ماژول ۰۱؛ برای بخش عملی: آشنایی اولیه با ترمینال ([01_Bash_Linux](../../01_Computing_Foundations/01_Bash_Linux/)) |
| **زمان تقریبی** | ۵ ساعت (۲٫۵ ساعت درس + ۲٫۵ ساعت تمرین) |
| **ابزارها (نسخه‌ی تست‌شده)** | NCBI Datasets CLI 18.38.0، curl، jq 1.7، awk |
| **داده** | از دیتابیس‌های عمومی و با اسکریپت‌های `scripts/` دریافت می‌شود |
| **وضعیت** | ✅ تست‌شده — 2026-10-12 |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. دیتابیس‌های اولیه و ثانویه را از هم تشخیص دهید و برای هر نوع داده منبع درست را انتخاب کنید.
2. نوع و منشأ هر شناسه (PRJ/SAM/SRX/SRR، GCA/GCF، NC/NP/WP، UniProt، PDB) را از روی پیشوندش بخوانید.
3. با `datasets`، ENA Portal API، UniProt REST، RCSB، KEGG و AlphaFold API داده را به‌صورت تکرارپذیر دریافت کنید.
4. با cross-referenceها یک ژن را بین دیتابیس‌ها دنبال کنید.
5. جدول Run↔Sample یک پروژه را بسازید و تله‌ی «هر Run یک نمونه» را تشخیص دهید.

## فایل‌ها
- [01_lesson.md](01_lesson.md) — متن درس
- [02_exercises.md](02_exercises.md) — تمرین‌ها
- [03_solutions.md](03_solutions.md) — پاسخ تشریحی
- [scripts/gene_tour.sh](scripts/gene_tour.sh) — دنبال‌کردن یک ژن در ۸ دیتابیس
- [scripts/project_summary.sh](scripts/project_summary.sh) — خلاصه‌ی Run/Sample یک پروژه‌ی ENA (پاسخ تمرین چالشی)

## اجرا
```bash
conda activate bioinfo_course
cd 00_Orientation/02_Biological_Databases
bash scripts/gene_tour.sh                       # rpoB
bash scripts/gene_tour.sh gyrA 511145 "fluoroquinolone resistance"
```
